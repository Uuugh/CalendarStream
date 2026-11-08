"""Holds: Calendar payload validation and safe response excerpt.
Depends on: app/calendars/errors.py.
Used by: app/calendars/downloads.py, app/calsync.py.
Reads/writes: values supplied by callers.
Dart note: calendar data adapters; inject transports and limits; preserve the compatibility facade.
"""

import re
from .errors import SourceError


def _snippet(body: bytes, n: int = 300) -> str:
    text = re.sub(r"<[^>]+>", " ", body[:4000].decode("utf-8", "replace"))
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m[1])), text)
    return re.sub(r"\s+", " ", text).strip()[:n]


def check_calendar(body: bytes):
    """Make sure an uploaded file is an iCalendar file."""
    if b"BEGIN:VCALENDAR" not in body[:2000]:
        raise SourceError(
            "That file isn't a calendar (.ics) file: "
            + (_snippet(body, 120) or "it's empty")
        )
