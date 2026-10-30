"""Feeds (destinations): add, move, change and remove them, their stream names, and what a calendar app
reads: the subscribe page and the .ics feed itself.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import hashlib
import re
import secrets
from datetime import timedelta

from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response

from .. import main as core
from ..main import (_did, _is_async, _iso_day, _moved, _shared_grant, app, calendar_color, calendar_name, Change,
    check_csrf, COLOR_RE, dest_events, dest_google, DESTINATION_TYPES, destinations, FieldError,
    first_named_calendar, forget_invites, google_for, google_job, google_view, gui_auth, make_invite, new_did, now,
    page, public_addresses, public_url, request_google_sync, save_destinations, sent_fields, source_ids, st, state,
    store, subscribe_links)
from .. import i18n
from ..calsync import build_feed
from ..config import normalise_public_url, settings
from ..store import from_iso, iso


# --- Who reads the feed --------------------------------------------------------------------
#
# Google Calendar fetches a subscribed feed with its own reader ("Google-Calendar-Importer"). Noting
# when it last came shows whether Google can reach the feed at all: until it has, Google shows the
# subscription under its web address and without events.

def note_feed_read(user_agent: str, did: str):
    kind = "google" if "google" in user_agent.lower() else "other"
    reads = store.get(f"feed_reads:{did}") or {}
    last = from_iso(reads.get(kind))
    if last is None or now() - last > timedelta(minutes=1):     # don't write on every fetch
        reads[kind] = iso(now())
        store.set(f"feed_reads:{did}", reads)


# --- Stream names: the secret part of each feed's links ---------------------------------------

STREAM_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


def dest_for_token(token: str) -> dict | None:
    """The feed destination whose links use this stream name."""
    for d in destinations("feed"):
        if d["token"] and secrets.compare_digest(token.encode(), d["token"].encode()):
            return d
    return None


@app.post("/destinations/move", dependencies=[Depends(gui_auth)])
async def move_destination(request: Request, csrf: str = Form(""), did: str = Form(""), before: str = Form(""),
                           after: str = Form("")):
    """Drag (or ▲ ▼) a feed module: the order of the feeds."""
    check_csrf(csrf)
    found = destinations()
    moved = _moved(found, did, before, after)
    if moved != found:
        save_destinations(moved)
    return {"ok": True} if _is_async(request) else RedirectResponse("/#destinations", status_code=303)


def _stream_value(stream: str, did: str = "") -> str:
    """A stream name typed (or a whole old feed link pasted), checked: the format, and that no other feed uses it."""
    value = stream.strip()
    m = re.search(r"/(?:calendar|subscribe)/([A-Za-z0-9_-]+?)(?:\.ics)?/?$", value)
    if m:
        value = m.group(1)
    if not STREAM_RE.match(value):
        raise FieldError("A stream name is 16 to 128 letters, digits, - or _ (or paste a whole old feed link).", "stream")
    if any(x["token"] == value for x in destinations("feed") if x["id"] != did):
        raise FieldError("Another feed already uses that stream name.", "stream")
    return value


def _dest_dates(d: dict, start: str | None, end: str | None):
    if start is not None or end is not None:
        d["start"], d["end"] = _iso_day(start), _iso_day(end)
        if (start or "").strip() and not d["start"]:
            raise FieldError("Check the date.", "start")
        if (end or "").strip() and not d["end"]:
            raise FieldError("Check the date.", "end")
        if d["start"] and d["end"] and d["end"] < d["start"]:
            raise FieldError("The end is before the start.", "end")


@app.post("/destinations/add", dependencies=[Depends(gui_auth)])
async def add_destination(request: Request, csrf: str = Form(""), type_: str = Form("", alias="type"), name: str = Form(""),
                          public: str = Form(""), note: str = Form(""), stream: str = Form(""), base: str = Form(""),
                          then: str = Form("")):
    """Feeds › + (0.2.8-beta.17): step 1 picks the module, step 2 is the module itself in a pop-up: its label
    and note, a Calendar Feed's link (a stream name typed brings back an old link), the calendars and dates
    (every calendar unless chosen), then Save. A Google module gets an account of its own: nothing is made
    in Google until it's connected (`then`: connect = Connect me, invite = Invite someone, right after)."""
    check_csrf(csrf)
    ch = Change()
    form = await request.form()
    oneway = type_ == "google1"
    type_ = {"google1": "google", "gfeed": "feed"}.get(type_, type_)     # (gfeed: from before beta.17, now a Calendar Feed)
    if type_ not in DESTINATION_TYPES:
        raise HTTPException(400, "Unknown kind of destination.")
    if type_ == "google" and not core.api_on():
        raise HTTPException(400, "Needs Google Calendar API Sync, which your admin turns on in ☰ Settings.")
    if public.strip():
        try:
            store.set("public_url", normalise_public_url(public))
        except ValueError:
            raise HTTPException(400, "Enter the address people use to reach this page, e.g. https://cal.example.com")
        state.record("info", f"Public address set to {public_url()}")
    found = destinations()
    if len(found) >= 20:
        raise HTTPException(400, "Up to 20 destinations can be added.")
    name = " ".join(name.split())[:100] or first_named_calendar()
    did = new_did()
    d = {"id": did, "type": type_, "name": name, "oneway": oneway, "note": " ".join(note.split())[:300],
         "sources": [x for x in source_ids() if x in form.getlist("sources")] if "sources" in form else source_ids(),
         "token": (_stream_value(stream) if stream.strip() else secrets.token_urlsafe(24)) if type_ == "feed" else "",
         "base": base if base in public_addresses() else "",
         # (I4) a Google module's own account, signed in with Connect me or an invite; never the one from before beta.17
         "account": "a" + secrets.token_hex(3) if type_ == "google" else ""}
    start, end = await sent_fields(request, "start", "end")
    _dest_dates(d, start, end)
    found.append(d)
    save_destinations(found)
    kind = ("Google 1-way Sync" if oneway else "Google 2-way Sync") if type_ == "google" else "Calendar Feed"
    ch.done("Feed", f"Destination added: {kind} \"{name}\"")
    if type_ == "google" and then == "connect":
        view = google_view(request)
        if view["redirect_ok"]:
            return RedirectResponse(google_for(d["account"]).sign_in_url(view["redirect_uri"]), status_code=303)
    if type_ == "google" and then == "invite":
        make_invite(d)
        saved = store.get("ui_sections") or {}
        saved[f"dest:{did}"] = True             # open, so the invite link is there to send
        store.set("ui_sections", saved)
    return RedirectResponse(f"/#dest-{did}", status_code=303)


@app.post("/destinations/update", dependencies=[Depends(gui_auth)])
async def update_destination(request: Request, csrf: str = Form(""), did: str = Form(""), name: str = Form(""),
                             sources_: list[str] = Form([], alias="sources"), start: str | None = Form(None),
                             end: str | None = Form(None), color: str = Form("")):
    """A destination's name and note, the sources it gets and its dates (empty = no limit); a Calendar Feed's
    address and stream name too (0.2.8-beta.17). A refusal names the fields to fix."""
    check_csrf(csrf)
    ch = Change()
    start, end, note, stream, base = await sent_fields(request, "start", "end", "note", "stream", "base")
    d = _did(did)
    _dest_dates(d, start, end)
    if note is not None:
        d["note"] = " ".join(note.split())[:300]
    if d["type"] == "feed" and stream is not None and stream.strip() and stream.strip() != d["token"]:
        d["token"] = _stream_value(stream, did)
        state.record("info", f"Stream name of \"{d['name']}\" changed; links with the old name no longer work")
    if d["type"] == "feed" and base is not None:
        d["base"] = base if base in public_addresses() else ""
    d["name"] = " ".join(name.split())[:100] or d["name"]
    d["sources"] = [x for x in source_ids() if x in sources_]
    if color:
        if not COLOR_RE.match(color):
            raise HTTPException(400, "Choose the color in the color box.")
        d["color"] = color.lower()
    save_destinations([d if x["id"] == did else x for x in destinations()])
    ch.done("Feed", f"Destination \"{d['name']}\": " + (", ".join(calendar_name(x) for x in d["sources"]) or "no sources"))
    if d["type"] == "google":
        request_google_sync(full=True)
    return RedirectResponse(f"/#dest-{did}", status_code=303)


@app.post("/destinations/remove", dependencies=[Depends(gui_auth)])
async def remove_destination(csrf: str = Form(""), did: str = Form(""), delete: str = Form("")):
    """Remove a destination. A Google calendar is deleted in Google only when asked; a feed's links
    and subscribe page stop working."""
    check_csrf(csrf)
    d = _did(did)
    ch = Change() if d["type"] != "google" else None      # (a Google calendar's removal touches Google: no Undo)
    if ch:
        ch.keys.append(f"feed_reads:{did}")
        ch.before = store.snapshot(ch.keys)
    note = ""
    if d["type"] == "google":
        async with google_job.lock:
            g = dest_google(d)
            if delete == "1":
                note = await g.delete_calendar(did)
            else:
                if g.connected:
                    await g.stop_watch([did])
                g.forget_calendar(did)
            # its own account goes with it, unless another module uses it; a Gmail another account also signed in
            # with keeps its grant in Google (I5: revoking it would sign those out too)
            if d["account"] and not any(x["account"] == d["account"] for x in destinations("google") if x["id"] != did) and g.connected:
                await g.disconnect(delete_calendar=False, revoke=not _shared_grant(g))
            forget_invites(did)
    else:
        store.delete(f"feed_reads:{did}")
    save_destinations([x for x in destinations() if x["id"] != did])
    what = " and its calendar in Google deleted" if d["type"] == "google" and delete == "1" and not note else ""
    msg = f"Destination removed: \"{d['name']}\"{what}" + (f" ({note})" if note else "")
    if ch:
        ch.done("Feed", msg)
    else:
        state.record("warn" if note else "info", msg, kind="Feed")
    return RedirectResponse("/#destinations", status_code=303)


@app.post("/feed/stream", dependencies=[Depends(gui_auth)])
async def set_stream(csrf: str = Form(""), did: str = Form(""), stream: str = Form("")):
    """Set a feed's stream name by hand, e.g. the one from before a reinstall, so old feed links and
    subscriptions work again. A whole old link can be pasted; its stream name is taken from it."""
    check_csrf(csrf)
    d = _did(did)
    if d["type"] != "feed":
        raise HTTPException(400, "Only calendar feeds have a stream name.")
    value = stream.strip()
    m = re.search(r"/(?:calendar|subscribe)/([A-Za-z0-9_-]+?)(?:\.ics)?/?$", value)
    if m:
        value = m.group(1)
    if not STREAM_RE.match(value):
        raise HTTPException(400, "A stream name is 16 to 128 letters, digits, - or _ (or paste a whole old feed link).")
    if any(x["token"] == value for x in destinations("feed") if x["id"] != did):
        raise HTTPException(400, "Another feed already uses that stream name.")
    save_destinations([{**x, "token": value} if x["id"] == did else x for x in destinations()])
    state.record("info", f"Stream name of \"{d['name']}\" changed; links with the old name no longer work")
    return RedirectResponse(f"/#dest-{did}", status_code=303)


@app.get("/subscribe/{token}")
def subscribe(request: Request, token: str):
    """Shareable page (no status-page login needed); the secret token in the URL is the access control."""
    d = dest_for_token(token)
    if not d:
        raise HTTPException(404)
    # Shared with other people: shown in each visitor's browser language.
    lang = i18n.pick(None, request.headers.get("accept-language", ""))
    checked = [st(x).last_success for x in d["sources"] if st(x).last_success]
    return page(request, "subscribe.html", {
        "cfg": settings, "name": d["name"], "links": subscribe_links(request, d["token"]),
        "last_success": max(checked) if checked else None,
        "event_count": sum(1 for e in dest_events(d) if not e.hidden),
    }, lang=lang)


@app.get("/calendar/{token}.ics")
def calendar(token: str, request: Request):
    """The published .ics feed. The token in the address is the only protection (it's secret)."""
    d = dest_for_token(token)
    if not d:
        raise HTTPException(404)
    note_feed_read(request.headers.get("user-agent", ""), d["id"])
    # its own color (0.2.8-beta.15), else its one calendar's: apps that read a calendar's color use it
    color = d["color"] or (calendar_color(d["sources"][0]) if len(d["sources"]) == 1 else "")
    ics = build_feed(dest_events(d), d["name"], settings.timezone, color)
    # An unchanged feed answers "304 Not Modified" (0.2.8-beta.4): calendar apps that ask with the tag
    # they were given last time don't download it all again.
    tag = '"' + hashlib.sha256(ics).hexdigest()[:32] + '"'
    headers = {"Cache-Control": "no-cache", "ETag": tag}
    if tag in [t.strip() for t in request.headers.get("if-none-match", "").split(",")]:
        return Response(status_code=304, headers=headers)
    return Response(ics, media_type="text/calendar; charset=utf-8", headers=headers)
