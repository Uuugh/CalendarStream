"""Holds: event history.
Depends on: app/calendars/event.py, app/i18n.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from .. import i18n
from ..calendars.event import Event
from datetime import date, datetime


def _event_time(e: Event, d: i18n.Dates, lang: str, *, Event, i18n) -> str:
    """An event's day and times in a change note, e.g. "Oct 23 7:15am–9:30am" or "Oct 23 (all day)"."""
    try:
        if e.all_day:
            return f"{d.short(date.fromisoformat(e.start[:10]))} ({i18n.tr(lang, 'all day')})"
        a, b = datetime.fromisoformat(e.start), datetime.fromisoformat(e.end)
        return f"{d.short(a.date())} {d.clock(a)}–{d.clock(b)}"
    except ValueError:
        return f"{e.start} – {e.end}"


def record_changes(
    sid: str,
    old: list[Event],
    new: list[Event],
    *,
    Event,
    TZ,
    _event_time,
    calendar_name,
    dates_for,
    i18n,
    now,
    ruleset,
    skey,
    st,
    store,
) -> int:
    """The "Record changes" rules: for each matching event the source changed (time, title or location),
    a note is added to the event ("Changed Oct 22: time Oct 23 7:15am–9:30am → Oct 23 8:05am–10:20am"),
    kept in kv change_notes:<source> and shown in its description, and a line goes in History and
    Logs; a matching event the source dropped is logged too. Returns how many changes were noted.
    """
    rs = ruleset(sid)
    if not rs.records_changes or not old:
        return 0
    watched = rs.watched
    lang = store.get("ui_lang") if store.get("ui_lang") in i18n.LANGS else "en"
    d, today = dates_for(lang), now().astimezone(TZ).date()
    before, after = {e.uid: e for e in old}, {e.uid for e in new}
    # A repeating event's occurrences have the start in their ID (<source>/<UID>/<start>), so a moved
    # one looks removed and added: pair those up within each series, in order.
    series = lambda uid: uid.rsplit("/", 1)[0] if uid.count("/") >= 2 else uid
    gone = {}
    for b in sorted((b for b in old if b.uid not in after), key=lambda b: b.start):
        gone.setdefault(series(b.uid), []).append(b)
    pairs = {}
    for e in sorted((e for e in new if e.uid not in before), key=lambda e: e.start):
        if gone.get(series(e.uid)):
            pairs[e.uid] = gone[series(e.uid)].pop(0)
    moved = {b.uid for b in pairs.values()}
    notes, count, S = store.get(skey(sid, "change_notes")) or {}, 0, st(sid)
    for e in new:
        b = before.get(e.uid) or pairs.get(e.uid)
        if not b or not (watched(e) or watched(b)):
            continue
        parts = []
        if (b.start, b.end, b.all_day) != (e.start, e.end, e.all_day):
            parts.append(f"time {_event_time(b, d, lang)} → {_event_time(e, d, lang)}")
        if b.title != e.title:
            parts.append(f'title "{b.title}" → "{e.title}"')
        if b.location != e.location:
            parts.append(f"location {b.location or '—'} → {e.location or '—'}")
        if parts:
            notes[e.uid] = (
                notes.get(e.uid, [])
                + [f"Changed {d.short(today)}: " + "; ".join(parts)]
            )[-20:]
            S.record(
                "info", f"{calendar_name(sid)} changed {e.title}: " + "; ".join(parts)
            )
            count += 1
    for uid, b in before.items():
        if uid not in after and uid not in moved and watched(b):
            S.record(
                "info",
                f"{calendar_name(sid)} removed {b.title} ({_event_time(b, d, lang)})",
            )
            notes.pop(uid, None)
    store.set(skey(sid, "change_notes"), notes)
    return count


def add_change_notes(events: list[Event], sid: str, *, Event, skey, store):
    """Put the notes made by "Record changes" rules at the end of their events' descriptions."""
    notes = store.get(skey(sid, "change_notes")) or {}
    for e in events:
        if notes.get(e.uid):
            e.description = (
                e.description.rstrip() + "\n\n" if e.description.strip() else ""
            ) + "\n".join(notes[e.uid])
