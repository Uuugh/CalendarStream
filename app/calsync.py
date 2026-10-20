"""Download the schedule from United's CCS+ Calendar Sync and prepare it for Google Calendar.

CCS+ Calendar Sync (CCS+ Settings > Schedule Settings > Calendar syncing) serves the schedule
as an iCalendar file behind HTTP Basic authentication:
    username = your UID, password = the Calendar Sync password created in CCS+.
Apple Calendar can subscribe to it directly; Google Calendar can't send a username and
password, so this app downloads it on a timer and republishes it as a feed Google can use.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import httpx
from icalendar import Calendar

from . import __version__

USER_AGENT = f"calendar_stream/{__version__} (iCalendar subscription client)"


# --- Results / errors ------------------------------------------------------

class AuthError(Exception):
    """401: UID or Calendar Sync password rejected."""


class BlockedError(Exception):
    """403 or similar: the server refused the request (e.g. Akamai 'Access Denied')."""


class SourceError(Exception):
    """Anything else: network trouble, server errors, or a response that isn't a calendar."""


@dataclass
class Download:
    status: int
    body: bytes = b""
    etag: str = ""
    last_modified: str = ""
    not_modified: bool = False
    debug: dict | None = None


@dataclass
class Event:
    title: str
    start: str            # ISO datetime in the display time zone, or ISO date for all-day
    end: str
    all_day: bool = False
    location: str = ""
    description: str = ""
    uid: str = ""


@dataclass
class Defaults:
    """How to treat events that have a start but no end (DTEND/DURATION)."""
    mode: str = "hours"     # "hours" or "allday"
    hours: float = 1.0
    allday_24h: bool = True  # timed events lasting a whole number of days (24 h, 48 h…) become all-day


# --- Download --------------------------------------------------------------

def _snippet(body: bytes, n: int = 300) -> str:
    text = re.sub(r"<[^>]+>", " ", body[:4000].decode("utf-8", "replace"))
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m[1])), text)
    return re.sub(r"\s+", " ", text).strip()[:n]


async def download(url: str, username: str, password: str, etag: str = "", last_modified: str = "",
                   timeout: float = 45.0) -> Download:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/calendar, */*;q=0.5"}
    if etag:
        headers["If-None-Match"] = etag
    if last_modified:
        headers["If-Modified-Since"] = last_modified

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            r = await client.get(url, auth=(username, password), headers=headers)
    except httpx.TimeoutException:
        raise SourceError(f"{httpx.URL(url).host} didn't answer within {int(timeout)} seconds.")
    except httpx.HTTPError as e:
        raise SourceError(f"Couldn't connect to {httpx.URL(url).host}: {type(e).__name__}: {e}")

    keep = ("content-type", "content-length", "content-disposition", "etag", "last-modified",
            "server", "date", "cache-control", "www-authenticate")
    debug = {
        "url": str(r.url), "status": r.status_code, "elapsed_s": round(r.elapsed.total_seconds(), 2),
        "bytes": len(r.content), "user_agent": USER_AGENT,
        "headers": {k: v for k, v in r.headers.items() if k.lower() in keep},
    }
    if r.status_code == 304:
        return Download(304, not_modified=True, etag=etag, last_modified=last_modified, debug=debug)
    if r.status_code == 401:
        raise AuthError("CCS+ rejected the UID or Calendar Sync password (HTTP 401). Check CCS_USER.txt "
                        "(your UID) and CCS_PASSWORD.txt (the Calendar Sync password, not your CCS login).")
    if r.status_code == 403:
        server = r.headers.get("server", "")
        ref = re.search(r"Reference\s*#?\s*([\w.]+)", _snippet(r.content, 1000))
        who = "Akamai (United's bot protection)" if "akamai" in server.lower() else (server or "the server")
        raise BlockedError(f"Access denied by {who}, HTTP 403" + (f", reference {ref[1]}" if ref else "") + ".")
    if r.status_code >= 400:
        raise SourceError(f"CCS+ answered HTTP {r.status_code}: {_snippet(r.content, 160) or 'no details'}")
    if b"BEGIN:VCALENDAR" not in r.content[:2000]:
        raise SourceError("CCS+ answered, but not with a calendar file "
                          f"({r.headers.get('content-type', 'unknown type')}): {_snippet(r.content, 160)}")
    return Download(r.status_code, body=r.content, etag=r.headers.get("etag", ""),
                    last_modified=r.headers.get("last-modified", ""), debug=debug)


# --- Processing ------------------------------------------------------------

def _as_dt(value, tz: ZoneInfo):
    """Normalise a DTSTART/DTEND value to (aware datetime | date)."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=tz)
    return value


def _set_all_day(ev, first: date, days: int, note: str):
    """Rewrite a VEVENT as an all-day event covering `days` days from `first`, keeping a note."""
    for prop in ("DTSTART", "DTEND", "DURATION"):
        ev.pop(prop, None)
    ev.add("dtstart", first)
    ev.add("dtend", first + timedelta(days=days))
    desc = str(ev.get("DESCRIPTION", ""))
    ev.pop("DESCRIPTION", None)
    ev.add("description", f"{note}\n{desc}".strip())
    return first, first + timedelta(days=days)


def process(raw: bytes, name: str, tz_name: str, defaults: Defaults) -> tuple[bytes, list[Event], str]:
    """Return (feed bytes for Google, events for the status page, content hash)."""
    tz = ZoneInfo(tz_name)
    try:
        cal = Calendar.from_ical(raw)
    except Exception as e:
        raise SourceError(f"The calendar file from CCS+ couldn't be read: {e}")

    # Calendar-level properties for subscribers
    for prop in ("X-WR-CALNAME", "X-WR-TIMEZONE", "REFRESH-INTERVAL", "X-PUBLISHED-TTL", "NAME"):
        cal.pop(prop, None)
    cal.add("x-wr-calname", name)
    cal.add("name", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    cal.add("x-published-ttl", "PT1H")

    events: list[Event] = []
    for ev in cal.walk("VEVENT"):
        if "DTSTART" not in ev:
            continue
        start = _as_dt(ev["DTSTART"].dt, tz)
        if "DTEND" in ev:
            end = _as_dt(ev["DTEND"].dt, tz)
        elif "DURATION" in ev:
            end = start + ev["DURATION"].dt
        elif isinstance(start, datetime):
            # A timed event with no end: apply DEFAULT_EVENT_HOURS
            if defaults.mode == "allday":
                start, end = _set_all_day(ev, start.astimezone(tz).date(), 1,
                                          f"Start: {start.astimezone(tz):%H:%M}")
            else:
                end = start + timedelta(hours=defaults.hours)
                ev.add("dtend", end)
        else:
            end = start + timedelta(days=1)   # all-day with no end = one day (RFC 5545)

        # 24-hour (or 48 h, 72 h…) timed events -> all-day, on the day(s) they start
        if defaults.allday_24h and isinstance(start, datetime) and isinstance(end, datetime):
            dur = end - start
            days = round(dur / timedelta(days=1))
            if days >= 1 and abs(dur - timedelta(days=days)) <= timedelta(minutes=1):
                s_local, e_local = start.astimezone(tz), end.astimezone(tz)
                start, end = _set_all_day(ev, s_local.date(), days,
                                          f"Original time: {s_local:%a %b %d %H:%M} – {e_local:%a %b %d %H:%M}")

        all_day = not isinstance(start, datetime)
        events.append(Event(
            title=str(ev.get("SUMMARY", "(no title)")),
            start=start.isoformat() if all_day else start.astimezone(tz).isoformat(),
            end=end.isoformat() if all_day else end.astimezone(tz).isoformat(),
            all_day=all_day,
            location=str(ev.get("LOCATION", "")),
            description=str(ev.get("DESCRIPTION", ""))[:2000],
            uid=str(ev.get("UID", "")) or hashlib.sha1(f"{start}|{ev.get('SUMMARY')}".encode()).hexdigest(),
        ))

    events.sort(key=lambda e: e.start)
    feed = cal.to_ical()
    return feed, events, hashlib.sha256(raw).hexdigest()


def empty_feed(name: str, tz_name: str) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//calendar_stream//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    return cal.to_ical()


def today_iso(tz_name: str) -> str:
    return date.today().isoformat() if not tz_name else datetime.now(ZoneInfo(tz_name)).date().isoformat()
