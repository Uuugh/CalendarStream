"""Calendars (sources): Sync Now and Verify, add, move, remove, import and export .ics, a feed's link,
the CCS+ sign-in, how often each is checked, its name, color and note, and uploading a file by hand.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import asyncio
import json
import re
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlparse

from fastapi import Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse, Response

from .. import main as core
from ..main import (_FIELDS, _is_async, _moved, _opt_day, _sid, all_rules, app, apply_calendar, background,
    calendar_color, calendar_name, Change, check_csrf, COLOR_RE, customs_for, destinations, ensure_local,
    event_alarms, event_links, google, google_redirect_uri, gui_auth, lang_for, last_local, logins, MAX_INTERVAL,
    MIN_INTERVAL, new_local, now, rebuild, RULES_PARSE, save_destinations, save_rules, sent_fields, skey,
    SOURCE_BASES, source_ids, SOURCE_PRESETS, sources, st, start_source, State, state, states, stop_source, store,
    TZ, united_original)
from .. import i18n, rules as rules_mod
from ..calsync import build_feed, check_calendar, parse_feed, SourceError
from ..config import DEFAULT_CALENDAR_URL, settings
from ..logins import LoginError


@app.post("/run", dependencies=[Depends(gui_auth)])
async def run_now(request: Request, csrf: str = Form(""), sid: str = Form("ccs")):
    """Sync now: download a source straight away, even while automatic checks are paused. From the
    page's script it answers at once; the page then follows the source in /api/status and updates
    its status and the calendar in place when it's done."""
    check_csrf(csrf)
    sid = _sid(sid)
    if not st(sid).running:
        background(core.run_once(manual=True, sid=sid))
        await asyncio.sleep(0.5)
    if _is_async(request):
        return {"ok": True, "running": st(sid).running}
    return RedirectResponse(f"/#src-{sid}", status_code=303)


async def _wait_idle(S: State, seconds: int = 120):
    """Wait for a source's download in progress to finish."""
    for _ in range(seconds * 4):
        if not S.running:
            return
        await asyncio.sleep(0.25)


@app.post("/verify", dependencies=[Depends(gui_auth)])
async def verify(request: Request, csrf: str = Form(""), kind: str = Form(""), sid: str = Form("")):
    """After a login was saved from its Save button: check it now (CCS+ downloads, Google checks the
    client, a feed downloads) and say whether it worked, for "✓ Validated" / "✗ Verification failed"."""
    check_csrf(csrf)
    lang = lang_for(request)
    if kind == "ccs":
        await _wait_idle(state)
        await core.run_once(manual=True)
        await _wait_idle(state)
        ok, message = bool(state.last_auth_ok) and state.status == "ok", state.message
    elif kind == "google":
        if not google.configured:
            return JSONResponse({"ok": False, "message": str(i18n.message(lang, "Enter the client secret too."))})
        check = await google.check_client(google_redirect_uri(request))
        ok = check.get("ok") is True
        message = check.get("message", "")
        if ok and check.get("redirect_ok") is False:
            message = f"Google doesn't list {check.get('redirect_uri')} under Authorised redirect URIs; add it to the client in Google Cloud"
        state.record("info" if ok else "warn", f"Google OAuth client checked: {message}")
    elif kind == "feed":
        S = st(_sid(sid))
        await _wait_idle(S)
        await core.run_once(manual=True, sid=sid)
        await _wait_idle(S)
        ok, message = S.status == "ok", S.message
    else:
        raise HTTPException(400, "Unknown kind of login.")
    return JSONResponse({"ok": ok, "message": str(i18n.message(lang, message)) if message else ""})


# --- Adding and removing sources and destinations ---------------------------------------------

def _feed_link(url: str) -> str:
    """A feed link as entered: webcal:// is the same as https://; only https:// is downloaded."""
    url = url.strip()
    if url.lower().startswith("webcal://"):
        url = "https://" + url[9:]
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise HTTPException(400, "The feed link must start with https:// (or webcal://).")
    return url


@app.post("/sources/add", dependencies=[Depends(gui_auth)])
async def add_source(csrf: str = Form(""), type_: str = Form("", alias="type"), url: str = Form(""),
                     name: str = Form(""), note: str = Form(""), preset: str = Form("other")):
    """Calendars → +: a preset: a local calendar (events added here only), United's CCS+ Calendar Sync
    (once), a Google or Apple calendar (its private iCal link), or any other .ics feed link."""
    check_csrf(csrf)
    ch = Change()
    found = sources()
    if len(found) >= 10:
        raise HTTPException(400, "Up to 10 calendars can be added.")
    if type_ == "local":
        sid = new_local()
        found.append({"id": sid, "type": "local"})
        name = " ".join(name.split())[:100]
        store.set(f"calendar_name:{sid}", name or "Local")
    elif type_ == "ccs":
        if "ccs" in source_ids():
            raise HTTPException(400, "CCS+ Calendar Sync is already a source.")
        found.append({"id": "ccs", "type": "ccs"})
        sid = "ccs"
    elif type_ == "ics":
        url = _feed_link(url)
        if any(x.get("url") == url for x in found):
            raise HTTPException(400, "That feed is already a source.")
        sid = "f" + secrets.token_hex(3)
        found.append({"id": sid, "type": "ics", "url": url, "preset": preset if preset in SOURCE_PRESETS else "other"})
        name = " ".join(name.split())[:100]
        if name:
            store.set(f"calendar_name:{sid}", name)
    else:
        raise HTTPException(400, "Unknown kind of calendar source.")
    store.set("sources", found)
    ch.done("Calendar", f"Calendar source added: {calendar_name(sid)}")
    if " ".join(note.split()):
        store.set(skey(sid, "note"), " ".join(note.split())[:120])
    if len(source_ids()) == 1 or type_ == "local":     # into the feeds: the first calendar, and a local one
        save_destinations([{**d, "sources": d["sources"] + [sid]} for d in destinations()])
    rebuild(sid)
    start_source(sid)
    return RedirectResponse(f"/#src-{sid}", status_code=303)


@app.post("/sources/move", dependencies=[Depends(gui_auth)])
async def move_source(request: Request, csrf: str = Form(""), sid: str = Form(""), before: str = Form(""),
                      after: str = Form("")):
    """Drag (or ▲ ▼) a calendar module: the order of the calendars. The top one is the default
    calendar for events added here."""
    check_csrf(csrf)
    ch = Change()
    found = sources()
    moved = _moved(found, sid, before, after)
    if moved and moved[0].get("type") != "local":
        raise HTTPException(400, "The top calendar is always a CalendarStream calendar: it's the default for events added here.")
    if moved != found:
        store.set("sources", moved)
        if found[0]["id"] != moved[0]["id"]:
            ch.done("Calendar", f"Default calendar: {calendar_name(moved[0]['id'])}")
    return {"ok": True} if _is_async(request) else RedirectResponse("/#sources", status_code=303)


@app.post("/sources/remove", dependencies=[Depends(gui_auth)])
async def remove_source(csrf: str = Form(""), sid: str = Form(""), keep: str = Form("delete"), into: str = Form(""),
                        rules: str = Form("delete")):
    """Remove a calendar (0.2.8-beta.15): its checks stop, it's taken off every feed, and its events are
    merged into another calendar (`keep=merge`, `into`: a calendar's ID, or "new" for a new CalendarStream
    calendar named and colored like it) or deleted. With a merge, its own rules can move with them
    (`rules=move`). The last CalendarStream calendar is emptied instead: it stays, in every feed and rule.
    A CCS+ sign-in is kept (encrypted) only while the removal can be undone. Undo: History."""
    check_csrf(csrf)
    sid = _sid(sid)
    if keep not in ("delete", "merge") or rules not in ("delete", "move"):
        raise HTTPException(400, "Unknown choice.")
    name, emptying = calendar_name(sid), last_local(sid)
    target = ""
    if keep == "merge":
        if into == "new":
            target = new_local()
        elif into in source_ids() and into != sid:
            target = into
        else:
            raise HTTPException(400, "Choose the calendar to merge its events into.")
    ch = Change(sids=[sid] + ([target] if target else []), whole=[sid] + ([target] if target else []))
    if into == "new" and target:
        at = source_ids().index(sid) + (1 if emptying else 0)
        store.set("sources", sources()[:at] + [{"id": target, "type": "local"}] + sources()[at:])
        store.set(f"calendar_name:{target}", name)
        if calendar_color(sid):
            store.set(f"calendar_color:{target}", calendar_color(sid))
        save_destinations([{**d, "sources": d["sources"] + ([target] if sid in d["sources"] else [])} for d in destinations()])
    moved = copy_events(sid, target) if target else 0
    own = [r for r in all_rules() if rules_mod.is_local(r, sid)]
    if target and rules == "move":     # its own rules now apply to the calendar its events went to
        save_rules([{**r, "apply": [target]} if rules_mod.is_local(r, sid) else r for r in all_rules()])
        own = []
    if emptying:
        store.forget_source(sid)
        save_rules([r for r in all_rules() if r not in own])
        note = f"{moved} events merged into {calendar_name(target)}" if target else "its events deleted"
        rebuild(sid)
        if target:
            rebuild(target)
        ch.done("Calendar", f"Emptied {name} ({note})")
        return RedirectResponse("/#sources", status_code=303)
    old_rules = all_rules()       # read while it's still a calendar
    stop_source(sid)
    store.set("sources", [x for x in sources() if x["id"] != sid])
    save_destinations([{**d, "sources": [x for x in d["sources"] if x != sid]} for d in destinations()])
    store.forget_source(sid)
    # its own rules go (unless moved); rules for several calendars are taken off it
    save_rules([{**r, "apply": r["apply"] if r["apply"] == "all" else [x for x in r["apply"] if x != sid]}
                for r in old_rules if not rules_mod.is_local(r, sid)])
    for base in SOURCE_BASES:
        store.delete(skey(sid, base))
    if sid == "ccs":
        logins.clear_ccs()
        store.delete("calendar_url")
        state.__init__("ccs")
    else:
        states.pop(sid, None)
    ensure_local()
    note = ""
    if target:
        rebuild(target)
        note = f"{moved} events merged into {calendar_name(target)}" + (", with its rules" if rules == "move" else "")
    ch.done("Calendar", f"Calendar source removed: {name}" + (f" ({note})" if note else ""))
    return RedirectResponse("/#sources", status_code=303)


# --- Import .ics (0.2.8-beta.15) ---------------------------------------------------------------------
# Into any calendar: the file's events (only those in From–To, unless All) become events added to it, kept
# through its downloads. One already there (the same event: a re-import, or a CalendarStream export of it)
# is asked about: Merge (the file's version updates it) or Delete (the file's copy is dropped).

IMPORT_KEEP = timedelta(minutes=30)


def _import_key(uid: str) -> str:
    return uid.split("/", 1)[1] if uid.startswith("imp/") else uid


def _when(e: dict) -> str:
    return e["start"][:10] + ("" if e["all_day"] else " " + e["start"][11:16])


@app.post("/sources/import", dependencies=[Depends(gui_auth)])
async def import_check(csrf: str = Form(""), sid: str = Form(""), start: str = Form(""), end: str = Form(""),
                       file: UploadFile = File(...)):
    """Step 1: read the file and say which of its events are already in the calendar."""
    check_csrf(csrf)
    sid = _sid(sid)
    body = await file.read(MAX_UPLOAD + 1)
    if len(body) > MAX_UPLOAD:
        raise HTTPException(413, "That file is too large (over 5 MB).")
    today = now().astimezone(TZ).date()
    first, last = _opt_day(start) or today - timedelta(days=3650), _opt_day(end) or today + timedelta(days=3650)
    if last < first:
        first, last = last, first
    try:
        check_calendar(body)
        found, _ = parse_feed(body, settings.timezone, RULES_PARSE, "imp", first, last + timedelta(days=1))
    except SourceError as e:
        raise HTTPException(400, str(e))
    found = [e for e in found if first.isoformat() <= e.start[:10] <= last.isoformat()]
    if not found:
        raise HTTPException(400, "No events in that file between those dates.")
    here = {e.uid: e for e in store.load_events(sid) if e.origin != "rule" and not e.deleted}
    imported = {c.get("import_uid"): c["uid"] for c in customs_for(sid) if c.get("import_uid")}
    rows, conflicts = [], []
    for e in found:
        key = _import_key(e.uid)
        row = {"key": key, **{k: getattr(e, k) for k in _FIELDS}}
        rows.append(row)
        at = here.get(key) or here.get(imported.get(key, ""))
        if at:
            conflicts.append({"key": key, "there": {"title": at.title, "when": _when(at.__dict__)},
                              "file": {"title": e.title, "when": _when(row)}})
    token = secrets.token_hex(8)
    store.set(f"import:{token}", {"sid": sid, "rows": rows, "at": now().isoformat(), "name": file.filename or "Calendar.ics"})
    return {"token": token, "total": len(rows), "conflicts": conflicts}


@app.post("/sources/import/finish", dependencies=[Depends(gui_auth)])
async def import_finish(request: Request, csrf: str = Form(""), token: str = Form(""), choices: str = Form("{}")):
    """Step 2: add the new events, and Merge or Delete each one already there (`choices`: {key: "merge" | "delete"})."""
    check_csrf(csrf)
    pending = store.get(f"import:{token}") if re.fullmatch(r"[0-9a-f]{16}", token or "") else None
    if not pending or now() - datetime.fromisoformat(pending["at"]) > IMPORT_KEEP:
        raise HTTPException(400, "That import has expired; choose the file again.")
    store.delete(f"import:{token}")
    sid = pending["sid"]
    if sid not in source_ids():
        raise HTTPException(400, "That calendar isn't here any more.")
    try:
        picked = json.loads(choices)
    except ValueError:
        picked = {}
    ch = Change(whole=[sid])
    here = {e.uid: e for e in store.load_events(sid) if e.origin != "rule" and not e.deleted}
    customs = {c["uid"]: c for c in customs_for(sid)}
    imported = {c.get("import_uid"): c["uid"] for c in customs.values() if c.get("import_uid")}
    edits = store.get_edits()
    added = merged = dropped = 0
    for row in pending["rows"]:
        key, data = row["key"], {k: row[k] for k in _FIELDS}
        at = here.get(key) or here.get(imported.get(key, ""))
        if not at:
            store.set_custom(f"cs-{secrets.token_hex(8)}@calendar_stream", {**data, "color": "", "source": sid, "import_uid": key})
            added += 1
        elif picked.get(key) != "merge":
            dropped += 1
        elif at.origin == "custom":
            store.set_custom(at.uid, {**{k: v for k, v in customs[at.uid].items() if k != "uid"}, **data})
            merged += 1
        else:
            original = united_original(at.uid, at.source)
            if original:
                base = edits.get(at.uid) or {"color": at.color, "base": original.fingerprint()}
                store.set_edit(at.uid, {**base, **data})
                merged += 1
    rebuild(sid)
    ch.done("Calendar", f"Imported {pending['name']} into {calendar_name(sid)}: {added} added"
            + (f", {merged} merged" if merged else "") + (f", {dropped} already there" if dropped else ""))
    return {"ok": True, "added": added, "merged": merged} if _is_async(request) else RedirectResponse(f"/#src-{sid}", status_code=303)


@app.get("/sources/export", dependencies=[Depends(gui_auth)])
def export_source(sid: str = ""):
    """A calendar as a .ics file (0.2.8-beta.15: "Download a copy first" when removing it): its events as
    they are now, edits included, without hidden or rule-made ones."""
    sid = _sid(sid)
    events = [e for e in store.load_events(sid) if not e.hidden and e.origin != "rule"]
    body = build_feed(events, calendar_name(sid), settings.timezone, calendar_color(sid))
    safe = re.sub(r"[^A-Za-z0-9 ._-]+", "", calendar_name(sid)).strip() or "calendar"
    return Response(body, media_type="text/calendar; charset=utf-8",
                    headers={"Content-Disposition": f'attachment; filename="{safe}.ics"'})


def copy_events(sid: str, target: str) -> int:
    """A removed calendar's events (as they are now, with edits; not hidden or rule-made ones) as events
    added to calendar `target`, keeping their reminders and links. Returns how many."""
    alarms, found = event_alarms(), event_links()
    n = 0
    for e in store.load_events(sid):
        if e.origin == "rule" or e.hidden:
            continue
        uid = e.uid if e.origin == "custom" else f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(uid, {"title": e.title, "start": e.start, "end": e.end, "all_day": e.all_day, "location": e.location,
                               "description": e.description, "color": e.color, "start_tz": "", "end_tz": "", "source": target})
        if uid != e.uid:
            if e.uid in alarms:
                alarms[uid] = alarms.pop(e.uid)
            if e.uid in found:
                found[uid] = found.pop(e.uid)
        for link in found.values():
            if link["to"] == e.uid:
                link.update(to=uid, src=target)
        n += 1
    store.set("event_alarms", alarms)
    store.set("event_links", found)
    return n


@app.post("/sources/url", dependencies=[Depends(gui_auth)])
async def set_source_url(request: Request, csrf: str = Form(""), sid: str = Form(""), url: str = Form("")):
    """Change a feed source's link, then download it."""
    check_csrf(csrf)
    sid = _sid(sid)
    if sid == "ccs":
        raise HTTPException(400, "Use the Calendar Sync link field for CCS+.")
    url = _feed_link(url)
    store.set("sources", [{**x, "url": url} if x["id"] == sid else x for x in sources()])
    store.delete(skey(sid, "http_cache"))
    st(sid).record("info", f"Feed link changed to {urlparse(url).hostname}")
    if _is_async(request):
        return JSONResponse({"saved": True})      # the page then asks /verify
    background(core.run_once(manual=True, sid=sid))
    await asyncio.sleep(1)
    return RedirectResponse(f"/#src-{sid}", status_code=303)


def _back_to(back: str, anchor: str) -> str:
    """Where a dashboard form returns to: its own box. (`back` is accepted from older pages and ignored:
    the logins no longer appear in Settings.)"""
    return f"/#{anchor}"


@app.post("/setup/ccs", dependencies=[Depends(gui_auth)])
async def set_ccs_login(request: Request, csrf: str = Form(""), uid: str = Form(""), password: str = Form(""),
                        back: str = Form(""), url: str | None = Form(None)):
    """Save the CCS+ Site Address (the Calendar Sync link; empty = United's), UID and Calendar Sync
    password, then download straight away."""
    check_csrf(csrf)
    (url,) = await sent_fields(request, "url")
    if url is not None:
        url = url.strip()
        if not url or url == DEFAULT_CALENDAR_URL:
            store.delete("calendar_url")
        else:
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise HTTPException(400, "The Calendar Sync link must start with https://")
            if url != store.get("calendar_url"):
                store.set("calendar_url", url)
                store.delete("http_cache")
    try:
        logins.save_ccs(uid, password)
    except LoginError as e:
        raise HTTPException(400, str(e))
    state.login_failures = 0
    store.delete("http_cache")
    state.record("info", "CCS+ Username and Calendar Sync password saved")
    if _is_async(request):
        return JSONResponse({"saved": True})      # the page then asks /verify
    if not state.running:
        background(core.run_once(manual=True))
        await asyncio.sleep(1.5)   # usually long enough to show whether CCS+ accepted it
    return RedirectResponse(_back_to(back, "src-ccs"), status_code=303)


@app.post("/setup/interval", dependencies=[Depends(gui_auth)])
async def set_interval(csrf: str = Form(""), minutes: str = Form(""), sid: str = Form("ccs")):
    """Change how often a source is downloaded (saved in the database)."""
    check_csrf(csrf)
    sid = _sid(sid)
    S = st(sid)
    try:
        value = int(minutes)
    except ValueError:
        raise HTTPException(400, "Enter a number of minutes.")
    if not MIN_INTERVAL <= value <= MAX_INTERVAL:
        raise HTTPException(400, f"Choose between {MIN_INTERVAL} and {MAX_INTERVAL} minutes.")
    if sid == "ccs" and value == settings.interval_minutes:
        store.delete("sync_interval")
    else:
        store.set(skey(sid, "sync_interval"), value)
    # The next check counts from the last one (or now, if that time has already passed).
    S.next_run = max(now(), (S.last_attempt or now()) + timedelta(minutes=value))
    S.wake.set()
    S.record("info", f"Checks every {value} min from now on")
    return RedirectResponse(f"/#src-{sid}", status_code=303)


@app.post("/setup/link", dependencies=[Depends(gui_auth)])
async def set_link(csrf: str = Form(""), url: str = Form(""), action: str = Form("save")):
    """Save the Calendar Sync link (action=reset goes back to the default), then download."""
    check_csrf(csrf)
    if action == "reset":
        store.delete("calendar_url")
        state.record("info", "Calendar Sync link reset to the default")
    else:
        url = url.strip()
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise HTTPException(400, "The Calendar Sync link must start with https://")
        store.set("calendar_url", url)
        store.delete("http_cache")
        state.record("info", f"Calendar Sync link set to {parsed.netloc}{parsed.path}")
    state.login_failures = 0
    if not state.running:
        background(core.run_once(manual=True))
    return RedirectResponse("/#src-ccs", status_code=303)


@app.post("/feed/name", dependencies=[Depends(gui_auth)])
async def set_name(csrf: str = Form(""), name: str = Form(""), color: str = Form(""),
                   color_default: str = Form(""), sid: str = Form("ccs")):
    """Save a source's name and color (its (edit) link). A blank name goes back to the default
    (CALENDAR_NAME from .env for CCS+). `color` is only sent when it was changed on the page;
    `color_default` clears it."""
    check_csrf(csrf)
    sid = _sid(sid)
    name = " ".join(name.split())[:100]
    if name and not (sid == "ccs" and name == settings.calendar_name):
        store.set(skey(sid, "calendar_name"), name)
    else:
        store.delete(skey(sid, "calendar_name"))
    notes = [f"name \"{calendar_name(sid)}\""]
    if color_default:
        store.delete(skey(sid, "calendar_color"))
        notes.append("default color")
    elif color:
        if not COLOR_RE.match(color):
            raise HTTPException(400, "Choose the color with the color picker.")
        store.set(skey(sid, "calendar_color"), color.lower())
        notes.append(f"color {color.lower()}")
    rebuild(sid)
    state.record("info", "Calendar settings saved: " + ", ".join(notes))
    return RedirectResponse(f"/#src-{sid}", status_code=303)


def _source_name_color(sid: str, name: str | None, color: str, color_default: str, note: str | None) -> list[str]:
    """Save a source's name, color and note (from its header, editable while Configure is open)."""
    notes = []
    if name is not None:
        name = " ".join(name.split())[:100]
        if name and not (sid == "ccs" and name == settings.calendar_name):
            store.set(skey(sid, "calendar_name"), name)
        else:
            store.delete(skey(sid, "calendar_name"))
        notes.append(f"name \"{calendar_name(sid)}\"")
    if color_default:
        store.delete(skey(sid, "calendar_color"))
        notes.append("default color")
    elif color:
        if not COLOR_RE.match(color):
            raise HTTPException(400, "Choose the color with the color picker.")
        store.set(skey(sid, "calendar_color"), color.lower())
        notes.append(f"color {color.lower()}")
    if note is not None:          # an empty note stays empty (it isn't replaced by the kind of calendar)
        store.set(skey(sid, "note"), " ".join(note.split())[:120])
    return notes


@app.post("/feed/tags", dependencies=[Depends(gui_auth)])
async def set_tags(request: Request, csrf: str = Form(""), sid: str = Form("ccs"), name: str | None = Form(None),
                   color: str = Form(""), color_default: str = Form(""), note: str | None = Form(None)):
    """Save a calendar module's header: its name, color and note (fields while it's expanded). Its rules
    are changed in the rule dialog and moved in place (/rules/…)."""
    check_csrf(csrf)
    name, note = await sent_fields(request, "name", "note")
    sid = _sid(sid)
    ch = Change(sids=[sid])
    notes = _source_name_color(sid, name, color, color_default, note)
    if notes:
        rebuild(sid)
        ch.done("Calendar", f"{calendar_name(sid)} saved: " + ", ".join(notes))
    return RedirectResponse(f"/#src-{sid}", status_code=303)


MAX_UPLOAD = 5 * 1024 * 1024


@app.post("/setup/upload", dependencies=[Depends(gui_auth)])
async def upload(csrf: str = Form(""), file: UploadFile = File(...)):
    """Publish a Calendar.ics downloaded by hand from CCS+ (United's own Google Calendar procedure)."""
    check_csrf(csrf)
    _sid("ccs")
    body = await file.read(MAX_UPLOAD + 1)
    if len(body) > MAX_UPLOAD:
        raise HTTPException(413, "That file is too large for a schedule (over 5 MB).")
    try:
        check_calendar(body)
        store.save_debug("source", body, "text/calendar; charset=utf-8")
        store.delete("http_cache")   # the next automatic download fetches the full file again
        state.last_attempt = now()
        apply_calendar(body, "uploaded by hand")
    except SourceError as e:
        state.record("error", f"Upload rejected: {e}")
        raise HTTPException(400, str(e))
    finally:
        state.save()
    return RedirectResponse("/#src-ccs", status_code=303)
