"""Holds: Calendar parsing and recurrence expansion.
Depends on: app/calendars/defaults.py, app/calendars/errors.py, app/calendars/event.py, app/calendars/meeting.py.
  app/calendars/meeting.py.
Used by: app/calsync.py.
Reads/writes: supplied calendar bytes and event values only.
Dart note: calendar domain functions; use an iCalendar adapter for parsing and writing.
"""

from __future__ import annotations
import hashlib
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from icalendar import Calendar
import recurring_ical_events

ALLDAY_TOLERANCE = timedelta(minutes=5)

from .errors import SourceError
from .event import Event
from .defaults import Defaults
from .meeting import event_meeting


def _as_dt(value, tz: ZoneInfo):
    """Normalise a DTSTART/DTEND value to (aware datetime | date)."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=tz)
    return value


def _set_all_day(ev, first: date, days: int, note: str = ""):
    """Rewrite a VEVENT as an all-day event covering `days` days from `first`, optionally keeping a note."""
    for prop in ("DTSTART", "DTEND", "DURATION"):
        ev.pop(prop, None)
    ev.add("dtstart", first)
    ev.add("dtend", first + timedelta(days=days))
    if note:
        desc = str(ev.get("DESCRIPTION", ""))
        ev.pop("DESCRIPTION", None)
        ev.add("description", f"{note}\n{desc}".strip())
    return first, first + timedelta(days=days)


def _event(
    ev, tz: ZoneInfo, defaults: Defaults, uid: str = "", source: str = "ccs"
) -> Event | None:
    """One VEVENT as an Event, with the end filled in and 24-hour events made all-day (the VEVENT is
    changed to match). None when it has no start."""
    if "DTSTART" not in ev:
        return None
    start = _as_dt(ev["DTSTART"].dt, tz)
    no_end = False
    if "DTEND" in ev:
        end = _as_dt(ev["DTEND"].dt, tz)
    elif "DURATION" in ev:
        end = start + ev["DURATION"].dt
    elif (
        isinstance(start, datetime)
        and start.astimezone(tz).time() == datetime.min.time()
    ):
        # Starts at midnight with no end: CCS+ uses this for day codes (RDO, HDO, VRDO…) -> all-day
        start, end = _set_all_day(ev, start.astimezone(tz).date(), 1)
    elif isinstance(start, datetime) and defaults.mode == "rules":
        end, no_end = start, True  # any other timed event with no end: the rules decide
    elif isinstance(start, datetime):
        # Any other timed event with no end: apply DEFAULT_EVENT_HOURS
        if defaults.mode == "allday":
            start, end = _set_all_day(
                ev,
                start.astimezone(tz).date(),
                1,
                f"Start: {start.astimezone(tz):%H:%M}",
            )
        else:
            end = start + timedelta(hours=defaults.hours)
            ev.add("dtend", end)
    else:
        end = start + timedelta(days=1)  # all-day with no end = one day (RFC 5545)

    # 24-hour (or 48 h, 72 h…) timed events -> all-day, on the day(s) they start
    if (
        defaults.allday_24h
        and isinstance(start, datetime)
        and isinstance(end, datetime)
    ):
        dur = end - start
        days = round(dur / timedelta(days=1))
        if days >= 1 and abs(dur - timedelta(days=days)) <= ALLDAY_TOLERANCE:
            s_local, e_local = start.astimezone(tz), end.astimezone(tz)
            start, end = _set_all_day(
                ev,
                s_local.date(),
                days,
                f"Original time: {s_local:%a %b %d %H:%M} – {e_local:%a %b %d %H:%M}",
            )

    all_day = not isinstance(start, datetime)
    return Event(
        title=str(ev.get("SUMMARY", "(no title)")),
        start=start.isoformat() if all_day else start.astimezone(tz).isoformat(),
        end=end.isoformat() if all_day else end.astimezone(tz).isoformat(),
        all_day=all_day,
        location=str(ev.get("LOCATION", "")),
        description=str(ev.get("DESCRIPTION", "")).strip()[:2000],
        uid=uid
        or str(ev.get("UID", ""))
        or hashlib.sha1(f"{start}|{ev.get('SUMMARY')}".encode()).hexdigest(),
        free=str(ev.get("TRANSP", "")).upper() == "TRANSPARENT",
        source=source,
        no_end=no_end,
        meeting=event_meeting(ev),
    )


def parse(raw: bytes, tz_name: str, defaults: Defaults):
    """Read a CCS+ calendar and normalise its events. Returns (Calendar, United's events, content hash)."""
    tz = ZoneInfo(tz_name)
    try:
        cal = Calendar.from_ical(raw)
    except Exception as e:
        raise SourceError(f"The calendar file from CCS+ couldn't be read: {e}")

    events: list[Event] = []
    for ev in cal.walk("VEVENT"):
        e = _event(ev, tz, defaults)
        if e:
            events.append(e)

    events.sort(key=lambda e: e.start)
    return cal, events, hashlib.sha256(raw).hexdigest()


def parse_feed(
    raw: bytes,
    tz_name: str,
    defaults: Defaults,
    source: str,
    first: date,
    last: date,
    *,
    max_feed_events: int = 5000,
):
    """Read a calendar feed (any .ics link). Repeating events are expanded into their occurrences
    between `first` and `last`. Each event's UID is "<source>/<UID>" (plus "/<its original start>" for an
    occurrence of a repeating event: its RECURRENCE-ID, so an occurrence the feed moves keeps its edits; review
    #4.1), so feeds can't collide with each other or with CCS+. Over MAX_FEED_EVENTS, the earliest are kept
    (review #4.2). Returns (events, content hash)."""
    tz = ZoneInfo(tz_name)
    try:
        cal = Calendar.from_ical(raw)
        found = recurring_ical_events.of(cal, skip_bad_series=True).between(first, last)
    except Exception as e:
        raise SourceError(f"The calendar file couldn't be read: {e}")
    events: list[Event] = []
    seen: set[str] = set()
    for ev in found:
        if str(ev.get("STATUS", "")).upper() == "CANCELLED":
            continue
        uid = (
            str(ev.get("UID", ""))
            or hashlib.sha1(
                f"{ev.get('DTSTART')}|{ev.get('SUMMARY')}".encode()
            ).hexdigest()
        )
        repeats = "RRULE" in ev or "RDATE" in ev or "RECURRENCE-ID" in ev
        when = ev.get("RECURRENCE-ID") or ev.get("DTSTART")
        key = f"{source}/{uid}" + (
            f"/{when.dt.isoformat()}" if repeats and when is not None else ""
        )
        if key in seen:
            continue
        seen.add(key)
        e = _event(ev, tz, defaults, uid=key, source=source)
        if e:
            events.append(e)
    events.sort(
        key=lambda e: e.start
    )  # (sorted before the limit, so it never drops the near ones)
    return events[:max_feed_events], hashlib.sha256(raw).hexdigest()
