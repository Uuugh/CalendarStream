"""Holds: publishing.
Depends on: app/calendars/event.py, app/rules.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from .. import rules as rules_mod
from ..calendars.event import Event
from datetime import date
from dataclasses import replace
from datetime import timedelta


def feed_window(*, now) -> tuple[date, date]:
    """Which occurrences of a feed's repeating events are kept: a year back to two years ahead."""
    today = now().date()
    return today - timedelta(days=365), today + timedelta(days=730)


def customs_for(sid: str, *, store) -> list[dict]:
    """Events added on the status page to one source's calendar."""
    return [c for c in store.get_customs() if (c.get("source") or "ccs") == sid]


def source_events(
    sid: str,
    raw: bytes | None,
    rs: rules_mod.Ruleset | None,
    *,
    Event,
    RULES_PARSE,
    feed_window,
    parse,
    parse_feed,
    rules_mod,
    ruleset,
    settings,
    source,
) -> tuple[list[Event], str]:
    """A source's own events from a download (none for a local calendar, or before the first one), with
    its rules' time changes (items without an end time, 24-hour events…), before any edit; and the
    download's hash."""
    if raw is None or (source(sid) or {}).get("type") == "local":
        return [], ""
    if sid == "ccs":
        _, base, digest = parse(raw, settings.timezone, RULES_PARSE)
    else:
        base, digest = parse_feed(
            raw, settings.timezone, RULES_PARSE, sid, *feed_window()
        )
    return (rs or ruleset(sid)).change_times(base), digest


def event_alarms(*, store) -> dict[str, str]:
    """The reminders set on the status page: {event UID: "15,60"} (minutes before the start)."""
    saved = store.get("event_alarms") or {}
    return {str(k): str(v) for k, v in saved.items() if isinstance(saved, dict)}


def publish(
    raw: bytes | None,
    sha: str | None,
    sid: str,
    *,
    Event,
    TZ,
    add_change_notes,
    apply_changes,
    build_feed,
    calendar_color,
    calendar_name,
    customs_for,
    event_alarms,
    follow_links,
    request_google_sync,
    ruleset,
    settings,
    skey,
    source_events,
    st,
    store,
) -> tuple[list[Event], list[Event]]:
    """Build a source's events from its last download (or none yet): its rules' time changes, then the
    edits and the events added here, the events its rules add, its rules' colors and emoji, and the
    reminders; store them. Returns (all its events now, its events before)."""
    rs = ruleset(sid)
    base, digest = source_events(sid, raw, rs)
    add_change_notes(base, sid)
    events = apply_changes(base, store.get_edits(), customs_for(sid), sid)
    events = rs.finish(sorted(events + rs.made(events, TZ), key=lambda e: e.start))
    alarms = event_alarms()
    events = [
        replace(e, alarms=alarms[e.uid]) if e.uid in alarms else e for e in events
    ]
    feed = build_feed(
        events, calendar_name(sid), settings.timezone, calendar_color(sid)
    )
    previous = store.load_events(sid)
    if raw is not None:
        store.save_calendar(skey(sid, "source"), raw, sha or digest)
    store.save_calendar(skey(sid, "feed"), feed, sha or digest)
    store.replace_events(events, sid)
    st(sid).event_count = sum(1 for e in events if not e.hidden)
    request_google_sync()
    follow_links(sid, events)
    return events, previous


def rebuild(sid: str | None, *, publish, skey, source_ids, store):
    """Rebuild a source's feed (or every source's) from its last download, e.g. after an edit or a rename."""
    for one in ([sid] if sid else source_ids()):
        if one not in source_ids():
            continue
        found = store.get_calendar(skey(one, "source"))
        publish(found[0] if found else None, found[1] if found else None, one)


def preview(sid: str, body: bytes, *, Event, source_events) -> tuple[list[Event], str]:
    """A downloaded calendar's events (with its rules' time changes, before edits), and its hash."""
    return source_events(sid, body)


def apply_calendar(
    body: bytes,
    how: str,
    sid: str,
    *,
    keep_removed,
    now,
    preview,
    publish,
    record_changes,
    skey,
    st,
    store,
) -> bool:
    """Publish a calendar file (downloaded or uploaded). Returns False if it was rejected."""
    S = st(sid)
    old_source = store.get_calendar(skey(sid, "source"))
    changed = not old_source or old_source[0] != body
    events_found, digest = preview(sid, body)
    if not events_found and store.event_count(sid) > 0:
        S.status = "error"
        S.message = (
            f"The {how} calendar has no events. Keeping the previous feed "
            f"({S.event_count} events) in case this is a glitch."
        )
        S.record("warn", S.message)
        return False
    if changed and old_source:
        record_changes(sid, preview(sid, old_source[0])[0], events_found)
    events, previous = publish(body, digest, sid)
    if changed and previous:
        keep_removed(sid, previous, events)
    S.status, S.last_success = "ok", now()
    if changed:
        S.last_change = now()
        old_ids, new_ids = {e.uid for e in previous}, {e.uid for e in events}
        added, removed = len(new_ids - old_ids), len(old_ids - new_ids)
        detail = f"{added} new, {removed} removed" if previous else "first copy"
        S.last_detail = detail
        S.message = (
            f"{how[:1].upper()}{how[1:]}: {S.event_count} events in feed ({detail})"
        )
        S.record("info", f"Schedule {how}: {S.event_count} events in feed ({detail})")
    else:
        S.last_detail = "no changes"
        S.message = f"Up to date: {S.event_count} events in feed (no changes)"
        S.record("info", f"Schedule {how}: no changes")
    return True
