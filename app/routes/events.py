"""Events: the event pop-up (/event), saving, reverting, restoring, deleting, reminders, links between
events.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import re
import secrets
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, Response

from .. import main as core
from ..main import (_is_async, _parse_month, _range_text, _span, ALARM_CHOICES, alarm_text, all_rules, ALL_ZONES,
    app, calendar_color, calendar_name, Change, check_csrf, COMMON_ZONES, COPY_ICON, dates_for, delete_events,
    display_tz, display_zone, event_alarms, EVENT_COLORS, event_links, event_templates, gui_auth, lang_for, now,
    page, rebuild, rule_label, show_duration, source, source_ids, state, store, TRASH_ICON, TZ, united_original,
    unmark_deleted, valid_zone)
from .. import rules as rules_mod
from ..calsync import Event
from ..gsync import GOOGLE_COLORS


# --- Edit and add events --------------------------------------------------

def _back(month: str | None) -> str:
    y, m = _parse_month(month)
    return f"/?month={y}-{m:02d}#cal"


def _form_values(e: Event, start_tz: ZoneInfo | None = None, end_tz: ZoneInfo | None = None, clock=None) -> dict:
    """Split an event into the edit form's fields (end date shown inclusive). Times are given as
    "HH:MM" and as shown on the page (`clock`: 12- or 24-hour), each in its own time zone."""
    start_tz = start_tz or display_tz()
    end_tz = end_tz or start_tz
    clock = clock or (lambda dt: f"{dt:%H:%M}")
    if e.all_day:
        first = date.fromisoformat(e.start[:10])
        last = max(first, date.fromisoformat(e.end[:10]) - timedelta(days=1))
        s_ = datetime.combine(first, datetime.min.time().replace(hour=9))
        t_ = datetime.combine(last, datetime.min.time().replace(hour=10))
    else:
        s_, t_ = datetime.fromisoformat(e.start).astimezone(start_tz), datetime.fromisoformat(e.end).astimezone(end_tz)
    return {"start_date": f"{s_:%Y-%m-%d}", "start_time": f"{s_:%H:%M}", "start_label": clock(s_),
            "end_date": f"{t_:%Y-%m-%d}", "end_time": f"{t_:%H:%M}", "end_label": clock(t_)}


def _saved_zones(uid: str) -> tuple[str, str]:
    """The time zones an event was last saved with on the event page, if any."""
    data = store.get_edits().get(uid) or next((c for c in store.get_customs() if c["uid"] == uid), None) or {}
    start = data.get("start_tz") if valid_zone(data.get("start_tz") or "") else ""
    end = data.get("end_tz") if valid_zone(data.get("end_tz") or "") else ""
    return start, end or start


@app.get("/event", dependencies=[Depends(gui_auth)])
def edit_event(request: Request, uid: str = "", date_: str = Query("", alias="date"), month: str | None = None,
               copy: str = "", embed: str = "", link: str = ""):
    """The event page: edit an event (uid), add one on `date`, or add a copy of one (`copy`). With
    `embed`, it's shown in a pop-up on the status page (0.2.8: on a computer; a phone opens the page);
    with `link`, opened at "Linked to" (the event's Link icon, 0.2.8-beta.10)."""
    if copy:
        found = store.get_event(copy)
        if not found:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        if not source_ids():
            raise HTTPException(400, "Add a calendar source first (Calendar Sources → +).")
        e = Event(title=found.title, start=found.start, end=found.end, all_day=found.all_day, location=found.location,
                  description=found.description, origin="custom", color=found.color,
                  source=found.source if found.source in source_ids() else source_ids()[0])
        uid = ""
    elif uid:
        e = store.get_event(uid)
        if not e:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        if e.origin == "rule":
            raise HTTPException(400, "This event is made by a rule; change the rule or its event template instead.")
    else:   # new event on a given day
        if not source_ids():
            raise HTTPException(400, "Add a calendar source first (Calendar Sources → +).")
        try:
            day = date.fromisoformat(date_)
        except ValueError:
            day = now().date()
        e = Event(title="", start=day.isoformat(), end=(day + timedelta(days=1)).isoformat(), all_day=False,
                  origin="custom", source=source_ids()[0])       # the default calendar: the top one
        e.start = datetime.combine(day, datetime.min.time().replace(hour=9), display_tz()).isoformat()
        e.end = datetime.combine(day, datetime.min.time().replace(hour=10), display_tz()).isoformat()
    original = united_original(uid, e.source) if e.origin == "united" and uid else None
    lang = lang_for(request)
    tag_color = e.rule_color
    start_zone, end_zone = _saved_zones(uid) if uid else ("", "")
    start_zone, end_zone = start_zone or display_zone(), end_zone or start_zone or display_zone()
    return page(request, "event.html", {
        "e": e, "f": _form_values(e, ZoneInfo(start_zone), ZoneInfo(end_zone), dates_for(lang).clock),
        "start_zone": start_zone, "end_zone": end_zone, "zones": ALL_ZONES, "common_zones": COMMON_ZONES,
        "is_new": not uid, "original": original,
        "colors": GOOGLE_COLORS.values(), "auto_color": tag_color or calendar_color(e.source) or "",
        "sources": [{"id": sid, "name": calendar_name(sid), "type": (source(sid) or {}).get("type"),
                     "color": calendar_color(sid) or ""} for sid in source_ids()],
        "tag_color": tag_color or "",
        "is_copy": bool(copy), "trash": TRASH_ICON, "copy_icon": COPY_ICON,
        "src_type": (source(e.source) or {}).get("type", "ccs"), "src_name": calendar_name(e.source),
        "templates": [{**t, "length": show_duration(t["minutes"])} for t in event_templates()],
        "original_range": _range_text(original, *_span(original)[2:], lang) if original else "",
        "csrf": core.CSRF_TOKEN, "month": month or (e.start[:7]), "tz": display_zone(), "embed": embed == "1",
        "default_sid": (source_ids() or [""])[0],
        "link": event_links().get(uid) if uid else None, "open_link": link == "1",
        "link_label": link_label((event_links().get(uid) or {}).get("to", ""), lang) if uid else "",
        "event_rules": event_rules(e) if uid else [],
    }, lang=lang)


def event_rules(e: Event) -> list[dict]:
    """The rules an event follows (Link › Rule › its rule, 0.2.8-beta.15): those of its calendar whose If
    matches it, highest first."""
    rs = rules_mod.Ruleset(rules_mod.for_source(all_rules(), e.source), TZ)
    info = rules_mod.event_info(e, TZ)
    found = []
    for r, test in rs.rules:
        try:
            if test(e, info):
                found.append({"id": r["id"], "label": rule_label(r)})
        except (ValueError, KeyError):
            continue
    return found


def link_label(to: str, lang: str) -> str:
    """How a picked event shows on Link to's line (0.2.8-beta.23, F1): "Title · date"; "" when it's gone."""
    other = store.get_event(to) if to else None
    if other is None or other.deleted:
        return ""
    return f"{other.title} · {dates_for(lang).day(_span(other)[0])}"


@app.get("/event/pick", dependencies=[Depends(gui_auth)])
def pick_event(request: Request, uid: str = "", month: str | None = None):
    """Link to › Event's small calendar (0.2.8-beta.23, F1): one month of the calendar, with its own ‹ › Today,
    to pick the event to link to. It adds and edits nothing; this event and the ones rules make can't be picked."""
    y, m = _parse_month(month)
    lang = lang_for(request)
    events = [e for e in store.load_events() if not e.deleted]
    cal = core.cal_view(events, "month", date(y, m, 1), lang)
    today = now().astimezone(display_tz()).date()
    d = dates_for(lang)
    shown = {it["e"].uid: it["e"] for week in cal["weeks"] for day in week for it in day["items"]}
    starts = {u: d.day(_span(e)[0]) for u, e in shown.items()}      # (a picked event shows as "Title · its first day")
    return page(request, "event-pick.html", {"cal": cal, "uid": uid, "this_month": f"{today:%Y-%m}", "starts": starts}, lang=lang)


def save_link(uid: str, to: str, delete: bool, move: bool):
    """Link an event to another one (or unlink it, with no `to`)."""
    found = event_links()
    other = store.get_event(to) if to and to != uid else None
    if other is None:
        found.pop(uid, None)
    else:
        found[uid] = {"to": other.uid, "src": other.source, "at": other.start, "delete": delete, "move": move}
    store.set("event_links", found)


def _event_back(month: str, embed: str) -> RedirectResponse:
    """After the event page: back to the calendar, or (in the pop-up) a page that tells it to close."""
    return RedirectResponse("/event/done" if embed == "1" else _back(month), status_code=303)


@app.get("/event/done", dependencies=[Depends(gui_auth)])
def event_done():
    """Shown in the event pop-up after a save: it tells the status page to close the pop-up and
    bring the calendar up to date."""
    html = ("<!doctype html><meta charset=utf-8><title>Saved</title>"
            "<script>parent.postMessage('calendarstream:event-saved', location.origin)</script>")
    return Response(html, media_type="text/html")


CLOCK_RE = re.compile(r"^\s*(\d{1,2})(?:[:.h]?(\d{2}))?\s*(?:([ap])\.?\s*m?\.?)?\s*$", re.I)


def parse_clock(text: str) -> str:
    """A time as typed on the event page, as "HH:MM": "9:30", "9:30pm", "930", "21:30", "2130",
    "9 pm", "9h30". Raises ValueError when it isn't a time."""
    m = CLOCK_RE.match(text or "")
    if not m:
        raise ValueError(text)
    digits, minute, ampm = m.group(1), m.group(2), (m.group(3) or "").lower()
    if minute is None and len(digits) > 2:          # "930" → 9:30 (handled by the regex as 9 + 30)
        raise ValueError(text)
    h, mi = int(digits), int(minute or 0)
    if ampm:
        if not 1 <= h <= 12:
            raise ValueError(text)
        h = h % 12 + (12 if ampm == "p" else 0)
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ValueError(text)
    return f"{h:02d}:{mi:02d}"


def _event_from_form(title, all_day, start_date, start_time, end_date, end_time, location, description,
                     color: str = "", start_tz: str = "", end_tz: str = "") -> dict:
    title = " ".join((title or "").split())
    color = (color or "").lower()
    if color and color not in EVENT_COLORS:
        raise HTTPException(400, "Choose one of the colors offered.")
    if not title:
        raise HTTPException(400, "The event needs a title.")
    try:
        sd, ed = date.fromisoformat(start_date), date.fromisoformat(end_date or start_date)
        if all_day:
            if ed < sd:
                raise HTTPException(400, "The last day is before the first day.")
            start, end = sd.isoformat(), (ed + timedelta(days=1)).isoformat()
        else:
            stz = ZoneInfo(start_tz) if valid_zone(start_tz) else display_tz()
            etz = ZoneInfo(end_tz) if valid_zone(end_tz) else stz
            s_ = datetime.combine(sd, datetime.strptime(parse_clock(start_time or "0:00"), "%H:%M").time(), stz)
            t_ = datetime.combine(ed, datetime.strptime(parse_clock(end_time or "0:00"), "%H:%M").time(), etz)
            if t_ <= s_:
                raise HTTPException(400, "The end has to be after the start.")
            start, end = s_.isoformat(), t_.isoformat()
    except ValueError:
        raise HTTPException(400, "Check the dates and times.")
    return {"title": title[:200], "start": start, "end": end, "all_day": bool(all_day),
            "location": (location or "").strip()[:200], "description": (description or "").strip()[:4000],
            "color": color,
            # remembered so the event page opens in the same time zones next time
            "start_tz": start_tz if valid_zone(start_tz) else "", "end_tz": end_tz if valid_zone(end_tz) else ""}


@app.post("/event/save", dependencies=[Depends(gui_auth)])
async def save_event(csrf: str = Form(""), uid: str = Form(""), month: str = Form(""), title: str = Form(""),
                     all_day: str = Form(""), start_date: str = Form(""), start_time: str = Form(""),
                     end_date: str = Form(""), end_time: str = Form(""), location: str = Form(""),
                     description: str = Form(""), hidden: str = Form(""), color: str = Form(""),
                     start_tz: str = Form(""), end_tz: str = Form(""), end_tz_differs: str = Form(""),
                     source_: str = Form("", alias="source"), embed: str = Form(""), link_to: str = Form(""),
                     link_delete: str = Form(""), link_move: str = Form("")):
    """Save the event page: an edit of a source's event, or an added event (into `source`). end_tz is
    only used when "The end is in a different time zone" is ticked."""
    check_csrf(csrf)
    end_tz = end_tz if end_tz_differs else start_tz      # one time zone for both unless asked otherwise
    known = store.get_event(uid) if uid else None
    ch = Change(whole=[known.source if known else (source_ if source_ in source_ids() else (source_ids() or ["ccs"])[0])])
    data = _event_from_form(title, all_day, start_date, start_time, end_date, end_time, location, description,
                            color, start_tz, end_tz)
    current, done = known, ""
    if current and current.origin == "rule":
        raise HTTPException(400, "This event is made by a rule; change the rule or its event template instead.")
    if current and current.origin == "united":
        original = united_original(uid, current.source)
        if not original:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        was_hidden = bool((store.get_edits().get(uid) or {}).get("hidden"))     # (F11.3: Hide and Show have their own button)
        unchanged = not hidden and uid not in store.get_edits() and all(
            data[k] == getattr(current, k) for k in ("title", "start", "end", "all_day", "location", "description", "color"))
        if not unchanged:       # (only its link changed: it isn't marked as edited)
            store.set_edit(uid, {**data, "hidden": bool(hidden) or was_hidden, "base": original.fingerprint()})
            done = f"Edited \"{original.title}\" ({original.start[:10]})" + (" and hid it from Google" if hidden and not was_hidden else "")
        sid = current.source
        save_link(uid, link_to, bool(link_delete), bool(link_move))
    else:
        sid = current.source if current else (source_ if source_ in source_ids() else (source_ids() or [""])[0])
        if sid not in source_ids():
            raise HTTPException(400, "Add a calendar source first (Calendar Sources → +).")
        new_uid = uid if current else f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(new_uid, {**data, "source": sid})
        save_link(new_uid, link_to, bool(link_delete), bool(link_move))
        done = f"{'Updated' if current else 'Added'} \"{data['title']}\" ({data['start'][:10]})"
    rebuild(sid)
    if done:
        ch.done("Event", done)
    state.save()
    return _event_back(month or data["start"][:7], embed)


@app.post("/event/hide", dependencies=[Depends(gui_auth)])
async def hide_event(request: Request, csrf: str = Form(""), uid: str = Form(""), show: str = Form(""),
                     month: str = Form(""), embed: str = Form("")):
    """Hide an event from a calendar source from every feed, or Show it again (0.2.8-beta.22, F11.3): its
    source would only send it again if it were deleted. It stays on the page, struck through; Undo in History."""
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e or e.origin != "united" or e.deleted:
        raise HTTPException(400 if e else 404, "Only an event from a calendar source can be hidden or shown." if e
                            else "That event isn't in the current schedule any more.")
    original = united_original(uid, e.source)
    if not original:
        raise HTTPException(404, "That event isn't in the current schedule any more.")
    ch = Change(whole=[e.source])
    edit = store.get_edits().get(uid)
    if show:
        if edit and edit.get("hidden"):
            rest = {k: v for k, v in edit.items() if k not in ("hidden", "base")}
            same = all(rest.get(k) == getattr(original, k) for k in ("title", "start", "end", "all_day", "location", "description", "color")) \
                and set(rest) <= {"title", "start", "end", "all_day", "location", "description", "color"}
            if same:            # hidden was its only change: it's as its source has it again
                store.delete_edit(uid)
            else:
                store.set_edit(uid, {**edit, "hidden": False})
        done = f"Showed \"{e.title}\" ({e.start[:10]}) in the feeds again"
    else:
        core._hide(e)
        done = f"Hid \"{e.title}\" ({e.start[:10]}) from the feeds"
    rebuild(e.source)
    ch.done("Event", done)
    state.save()
    if _is_async(request):
        return {"ok": True}
    return _event_back(month or e.start[:7], embed)


@app.post("/event/revert", dependencies=[Depends(gui_auth)])
async def revert_event(csrf: str = Form(""), uid: str = Form(""), month: str = Form(""), embed: str = Form("")):
    check_csrf(csrf)
    e = store.get_event(uid)
    ch = Change(whole=[e.source] if e else [])
    store.delete_edit(uid)
    rebuild(e.source if e else None)
    ch.done("Event", f"Reverted \"{e.title if e else ''}\" to its calendar’s version")
    return _event_back(month, embed)


@app.post("/event/restore", dependencies=[Depends(gui_auth)])
async def restore_event(request: Request, csrf: str = Form(""), uid: str = Form("")):
    """Restore a deleted event (0.2.8-beta.15): it's back as it was, and taken out of its History line's Undo."""
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e or not e.deleted or e.deleted == "gone":
        raise HTTPException(404, "That event can't be restored any more.")
    unmark_deleted(uid)
    store.forget_deleted(uid)
    rebuild(e.source)
    state.record("info", f"Restored \"{e.title}\" ({e.start[:10]})", kind="Event")
    return {"ok": True} if _is_async(request) else RedirectResponse("/#cal", status_code=303)


@app.post("/event/alarms", dependencies=[Depends(gui_auth)])
async def set_alarms(request: Request, csrf: str = Form(""), uid: str = Form(""), minutes: list[str] = Form([]),
                     month: str = Form("")):
    """An event's reminders (the bell on an event): sent to Google (up to five) and written into the feeds.
    Kept by event, so they stay through new downloads and edits."""
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e:
        raise HTTPException(404, "That event isn't in the current schedule any more.")
    chosen = sorted({int(m) for m in minutes if m.isdigit() and int(m) in ALARM_CHOICES})[:5]
    saved = event_alarms()
    if chosen:
        saved[uid] = ",".join(map(str, chosen))
    else:
        saved.pop(uid, None)
    store.set("event_alarms", saved)
    rebuild(e.source)
    state.record("info", f"Reminders for \"{e.title}\" ({e.start[:10]}): "
                 + (", ".join(alarm_text(m) for m in chosen) if chosen else "none"))
    return {"ok": True} if _is_async(request) else RedirectResponse(_back(month), status_code=303)


@app.post("/event/delete", dependencies=[Depends(gui_auth)])
async def delete_event(request: Request, csrf: str = Form(""), uid: str = Form(""), month: str = Form(""),
                       embed: str = Form("")):
    """Delete an event (the bin on an event). One added here is deleted; a source's own event would
    come back with the next download, so it's hidden from every destination instead (Edit → untick
    Hide brings it back)."""
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e:
        raise HTTPException(404, "That event isn't in the current schedule any more.")
    if e.origin == "rule":
        raise HTTPException(400, "This event is made by a rule; change the rule or its event template instead.")
    if e.deleted:
        raise HTTPException(400, "That event is already deleted; History › Undo brings it back.")
    if e.origin != "custom" and not united_original(uid, e.source):
        raise HTTPException(404, "That event isn't in the current schedule any more.")
    # (0.2.8-beta.15) kept struck through until its Undo pops off History; a source's own event stays hidden after
    delete_events([e], "calendarstream", f"Deleted \"{e.title}\" ({e.start[:10]})")
    rebuild(e.source)
    if _is_async(request):
        return {"ok": True}
    return _event_back(month, embed)
