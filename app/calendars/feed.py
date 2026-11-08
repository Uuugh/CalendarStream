"""Holds: iCalendar feed serialization.
Depends on: app/calendars/event.py.
Used by: app/calsync.py.
Reads/writes: supplied events, the UTC clock, and produced iCalendar bytes.
Dart note: calendar domain functions; use an iCalendar adapter for parsing and writing.
"""

from __future__ import annotations
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from icalendar import Calendar, Event as VEvent, Alarm
from .event import Event


def build_feed(events: list[Event], name: str, tz_name: str, color: str = "") -> bytes:
    """A calendar file written from events (hidden ones left out), for a feed source."""
    cal = new_calendar()
    _calendar_props(cal, name, tz_name, color)
    stamp = datetime.now(ZoneInfo("UTC"))
    for e in events:
        if e.hidden:
            continue
        ev = VEvent()
        ev.add("uid", e.uid)
        ev.add("dtstamp", stamp)
        if e.free:
            ev.add("transp", "TRANSPARENT")
        _write_fields(
            ev,
            e,
            {"custom": "added", "rule": "rule"}.get(
                e.origin, "edited" if e.edited else "source"
            ),
        )
        _write_alarms(ev, e)
        cal.add_component(ev)
    return cal.to_ical()


def _write_alarms(ev, e: Event):
    """The event's reminders, as VALARMs (a calendar app shows them; some ignore subscribed ones)."""
    for minutes in e.alarm_minutes():
        a = Alarm()
        a.add("action", "DISPLAY")
        a.add("description", e.title)
        a.add("trigger", timedelta(minutes=-minutes))
        ev.add_component(a)


def _calendar_props(cal, name: str, tz_name: str, color: str):
    for prop in (
        "X-WR-CALNAME",
        "X-WR-TIMEZONE",
        "REFRESH-INTERVAL",
        "X-PUBLISHED-TTL",
        "NAME",
        "X-APPLE-CALENDAR-COLOR",
    ):
        cal.pop(prop, None)
    if color:
        cal.add("x-apple-calendar-color", color.upper())
    cal.add("x-wr-calname", name)
    cal.add("name", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    cal.add("x-published-ttl", "PT1H")


def new_calendar() -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//calendar_stream//EN")
    cal.add("version", "2.0")
    return cal


def _utc(iso: str) -> datetime:
    return datetime.fromisoformat(iso).astimezone(ZoneInfo("UTC"))


def _write_times(ev, e: Event):
    for prop in ("DTSTART", "DTEND", "DURATION"):
        ev.pop(prop, None)
    if e.all_day:
        ev.add("dtstart", date.fromisoformat(e.start[:10]))
        ev.add("dtend", date.fromisoformat(e.end[:10]))
    else:  # UTC keeps the feed valid whatever time zones the file defines
        ev.add("dtstart", _utc(e.start))
        ev.add("dtend", _utc(e.end))


def notes_with_meeting(e: Event) -> str:
    """An event's notes as the feeds and Google get them: its online meeting link first, then a blank line, then the notes."""
    if not e.meeting:
        return e.description
    return e.meeting + ("\n\n" + e.description if e.description else "")


def _write_fields(ev, e: Event, marker: str):
    for prop in (
        "SUMMARY",
        "LOCATION",
        "DESCRIPTION",
        "X-ALT-DESC",
        "X-CALENDAR-STREAM",
        "URL",
    ):
        ev.pop(prop, None)
    ev.add("summary", e.title)
    _write_times(ev, e)
    if e.location:
        ev.add("location", e.location)
    # (0.2.8-beta.28, F6) the online meeting: the event's URL (Apple shows its video button) and the first line of the notes (a link in every app)
    notes = notes_with_meeting(e)
    if e.meeting:
        ev.pop("URL", None)
        ev.add("url", e.meeting)
    if notes:
        ev.add("description", notes)
    ev.add("x-calendar-stream", marker)


def empty_feed(name: str, tz_name: str) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//calendar_stream//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    return cal.to_ical()
