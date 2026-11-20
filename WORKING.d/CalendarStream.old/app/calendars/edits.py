"""Holds: Applying event edits and custom events.
Depends on: app/calendars/event.py.
Used by: app/calsync.py.
Reads/writes: supplied calendar bytes and event values only.
Dart note: calendar domain functions; use an iCalendar adapter for parsing and writing.
"""

from __future__ import annotations
from .event import Event


def apply_changes(
    base: list[Event], edits: dict, customs: list[dict], source: str
) -> list[Event]:
    """A feed source's events with the edits, hides and added events made on the status page
    (what render() does for CCS+, without a calendar file to keep)."""
    final = []
    for original in base:
        ed = edits.get(original.uid)
        final.append(_edited(original, ed) if ed else original)
    for c in customs:
        final.append(_custom(c, source))
    final.sort(key=lambda e: e.start)
    return final


def _edited(original: Event, ed: dict) -> Event:
    return Event(
        title=ed["title"],
        start=ed["start"],
        end=ed["end"],
        all_day=bool(ed["all_day"]),
        location=ed.get("location", ""),
        description=ed.get("description", ""),
        uid=original.uid,
        origin="united",
        edited=True,
        stale=ed.get("base") != original.fingerprint(),
        hidden=bool(ed.get("hidden")),
        free=original.free,
        color=ed.get("color", ""),
        source=original.source,
        deleted=ed.get("deleted", ""),
        meeting=ed["meeting"] if "meeting" in ed else original.meeting,
    )


def _custom(c: dict, source: str) -> Event:
    return Event(
        title=c["title"],
        start=c["start"],
        end=c["end"],
        all_day=bool(c["all_day"]),
        location=c.get("location", ""),
        description=c.get("description", ""),
        uid=c["uid"],
        origin="custom",
        color=c.get("color", ""),
        source=source,
        hidden=bool(c.get("deleted")),
        deleted=c.get("deleted", ""),
        meeting=c.get("meeting", ""),
    )
