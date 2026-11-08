"""Extract online meeting links from calendar events.

Holds: meeting_link, event_meeting, MEETING_RE.
Depends on: no other app files.
Used by: app/calendars/parsing.py, app/calsync.py.
Reads/writes: nothing.
Dart note: Meeting link extractor in calendars/domain; accepts event-like values.
"""
import re

# --- Online meetings (0.2.8-beta.28, F6) -----------------------------------------------------------------
_LINK_END = r"[^\s<>\"')\]]+"
MEETING_RE = re.compile(
    r"https?://(?:[\w-]+\.)*(?:zoom\.us|zoomgov\.com)/" + _LINK_END + r"|https?://meet\.google\.com/" + _LINK_END
    + r"|https?://teams\.(?:microsoft|live)\.com/" + _LINK_END + r"|https?://(?:[\w-]+\.)*webex\.com/" + _LINK_END, re.I)


def meeting_link(text: str) -> str:
    """The first Zoom, Google Meet, Teams or Webex link in a text, or ""."""
    m = MEETING_RE.search(text or "")
    return m.group(0).rstrip(".,;:") if m else ""


def event_meeting(ev) -> str:
    """The online meeting of a calendar file's event: its own conference field (RFC 7986 CONFERENCE, Google's and Microsoft's
    extensions), else a meeting link in its notes, location or URL."""
    for prop in ("CONFERENCE", "X-GOOGLE-CONFERENCE", "X-MICROSOFT-SKYPETEAMSMEETINGURL", "X-MICROSOFT-ONLINEMEETINGEXTERNALLINK"):
        got = ev.get(prop)
        for one in (got if isinstance(got, list) else [got]):
            text = str(one or "").strip()
            if text.lower().startswith(("http://", "https://")):
                return text[:500]
    return meeting_link(f"{ev.get('DESCRIPTION', '')}\n{ev.get('LOCATION', '')}\n{ev.get('URL', '')}")[:500]


