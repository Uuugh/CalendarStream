"""Calendar event parsing defaults.

Holds: Defaults.
Depends on: nothing.
Used by: app/calsync.py and calendar consumers.
Reads/writes: nothing.
Dart note: Defaults data model in the calendars/domain layer.
"""
from dataclasses import dataclass

@dataclass
class Defaults:
    """How to treat events that have a start but no end (DTEND/DURATION)."""
    mode: str = "hours"     # "hours" or "allday"; "rules": leave it to the rules (the end is the start, no_end set)
    hours: float = 1.0
    allday_24h: bool = True  # timed events lasting a whole number of days (24 h, 48 h…) become all-day
