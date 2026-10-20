"""Build an iCalendar (.ics) feed that Google Calendar can subscribe to."""
from datetime import date, datetime, timezone

from icalendar import Calendar, Event as ICalEvent

from .parser import Event


def build_ics(events: list[Event], name: str, tz_name: str) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//calendar_stream//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    cal.add("x-published-ttl", "PT1H")

    stamp = datetime.now(timezone.utc)
    for e in events:
        ev = ICalEvent()
        ev.add("uid", e.uid)
        ev.add("dtstamp", stamp)
        ev.add("summary", e.title)
        if e.all_day:
            ev.add("dtstart", date.fromisoformat(e.start))
            ev.add("dtend", date.fromisoformat(e.end))
        else:
            # UTC avoids emitting non-standard TZIDs; Google shows it in the viewer's zone.
            ev.add("dtstart", datetime.fromisoformat(e.start).astimezone(timezone.utc))
            ev.add("dtend", datetime.fromisoformat(e.end).astimezone(timezone.utc))
        if e.location:
            ev.add("location", e.location)
        if e.description:
            ev.add("description", e.description)
        cal.add_component(ev)
    return cal.to_ical()
