"""Calendar event model.

Holds: Event.
Depends on: no other app files.
Used by: app/calendars/edits.py, app/calendars/feed.py, app/calendars/parsing.py, app/calsync.py, app/links.py, app/rule_engine/matching.py, app/rule_engine/ruleset.py, app/rules.py, app/services/calendar_view.py, app/services/deletions.py, app/services/event_history.py, app/services/event_links.py, app/services/google_sync.py, app/services/publishing.py, app/services/route_helpers.py.
  app/links.py, app/rule_engine/matching.py, app/rule_engine/ruleset.py, app/rules.py,
  app/services/calendar_view.py, app/services/deletions.py, app/services/event_history.py,
  app/services/event_links.py, app/services/google_sync.py, app/services/publishing.py,
  app/services/route_helpers.py.
Reads/writes: nothing.
Dart note: Event data model in the calendars/domain layer.
"""
import hashlib
from dataclasses import dataclass, field

@dataclass
class Event:
    title: str
    start: str            # ISO datetime in the display time zone, or ISO date for all-day (end exclusive)
    end: str
    all_day: bool = False
    location: str = ""
    description: str = ""
    uid: str = ""
    origin: str = "united"   # "united" (from the source: CCS+ or a feed), "custom" (added on the status
                             # page) or "rule" (made by a rule from a template)
    edited: bool = False     # a United event changed on the status page
    stale: bool = False      # United changed this event after it was edited here
    hidden: bool = False     # left out of the Google feed
    free: bool = False       # shown as "free" rather than "busy" (CCS+ sends most items as TRANSP:TRANSPARENT)
    color: str = ""          # a color chosen for this event on the status page (#rrggbb); overrides rules
    source: str = "ccs"      # the calendar source it belongs to ("ccs" or a feed source's ID)
    alarms: str = ""         # reminders, minutes before the start ("15,60"), set on the status page (0.2.8)
    rule_color: str = ""     # the color its rules give it (#rrggbb), or ""; its own color still wins (0.2.8)
    deleted: str = ""        # 0.2.8-beta.15: deleted, but kept (struck through, greyed) until its Undo pops off:
                             # "<where>|<when>" (where: calendarstream, google, united, feed); "gone" after that
    meeting: str = ""        # 0.2.8-beta.28, F6: its online meeting (a Zoom, Google Meet, Teams or Webex link), or ""
    # Not stored: set while a download is read, for the rules (app/rules.py)
    no_end: bool = field(default=False, compare=False)    # it had no end time (its end is its start)
    ruled: bool = field(default=False, compare=False)     # a rule changed its time

    def alarm_minutes(self) -> list[int]:
        """The reminders, as minutes before the start, earliest first."""
        return sorted({int(x) for x in self.alarms.split(",") if x.strip().isdigit()}, reverse=True)

    def fingerprint(self) -> str:
        """Identifies United's version of an event, to notice when it changes after an edit."""
        key = "|".join([self.title, self.start, self.end, str(self.all_day), self.location, self.description])
        return hashlib.sha1(key.encode()).hexdigest()
