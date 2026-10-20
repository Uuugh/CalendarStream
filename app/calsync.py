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

from icalendar import Calendar


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
    start: str            # ISO datetime in the display time zone, or ISO date for all-day (end exclusive)
    end: str
    all_day: bool = False
    location: str = ""
    description: str = ""
    uid: str = ""
    origin: str = "united"   # "united" (from CCS+) or "custom" (added on the status page)
    edited: bool = False     # a United event changed on the status page
    stale: bool = False      # United changed this event after it was edited here
    hidden: bool = False     # left out of the Google feed
    free: bool = False       # shown as "free" rather than "busy" (CCS+ sends most items as TRANSP:TRANSPARENT)

    def fingerprint(self) -> str:
        """Identifies United's version of an event, to notice when it changes after an edit."""
        key = "|".join([self.title, self.start, self.end, str(self.all_day), self.location, self.description])
        return hashlib.sha1(key.encode()).hexdigest()


@dataclass
class Defaults:
    """How to treat events that have a start but no end (DTEND/DURATION)."""
    mode: str = "hours"     # "hours" or "allday"
    hours: float = 1.0
    allday_24h: bool = True  # timed events lasting a whole number of days (24 h, 48 h…) become all-day


# --- Download --------------------------------------------------------------
#
# Downloads use the curl program. United's Akamai protection answers curl normally, but holds
# or refuses requests from Python HTTP libraries. curl identifies itself as curl.

import asyncio
import json as _json
import os
import shutil
import tempfile
from urllib.parse import urlparse

CURL = shutil.which("curl") or "curl"
_curl_version = ""


def _snippet(body: bytes, n: int = 300) -> str:
    text = re.sub(r"<[^>]+>", " ", body[:4000].decode("utf-8", "replace"))
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m[1])), text)
    return re.sub(r"\s+", " ", text).strip()[:n]


def _q(value: str) -> str:
    """Quote a value for a curl config file."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "").replace("\r", "") + '"'


def _parse_headers(raw: str) -> dict:
    """Headers of the final response (curl writes one block per redirect)."""
    blocks = [b for b in re.split(r"\r?\n\r?\n", raw.strip()) if b.strip()]
    headers: dict[str, str] = {}
    for line in (blocks[-1].splitlines()[1:] if blocks else []):
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    return headers


async def curl_version() -> str:
    global _curl_version
    if not _curl_version:
        try:
            proc = await asyncio.create_subprocess_exec(CURL, "--version", stdout=asyncio.subprocess.PIPE)
            out, _ = await proc.communicate()
            _curl_version = out.decode().split(" (")[0].strip() or "curl"
        except FileNotFoundError:
            _curl_version = "curl not installed"
    return _curl_version


async def download(url: str, username: str, password: str, etag: str = "", last_modified: str = "",
                   timeout: float = 60.0, connect_timeout: float = 20.0) -> Download:
    host = urlparse(url).hostname or url
    with tempfile.TemporaryDirectory(prefix="calsync-") as tmp:
        body_path, head_path = os.path.join(tmp, "body"), os.path.join(tmp, "headers")
        # Credentials go to curl on stdin (a config file), never on the command line.
        config = [f"url = {_q(url)}", f"user = {_q(f'{username}:{password}')}",
                  f'header = {_q("Accept: text/calendar, */*;q=0.5")}']
        if etag:
            config.append(f"header = {_q('If-None-Match: ' + etag)}")
        if last_modified:
            config.append(f"header = {_q('If-Modified-Since: ' + last_modified)}")
        args = [CURL, "--silent", "--show-error", "--location", "--config", "-",
                "--connect-timeout", str(int(connect_timeout)), "--max-time", str(int(timeout)),
                "--output", body_path, "--dump-header", head_path, "--write-out", "%{json}"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *args, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        except FileNotFoundError:
            raise SourceError("curl isn't installed in this container (it's needed to download from CCS+).")
        out, err = await proc.communicate(("\n".join(config) + "\n").encode())
        try:
            info = _json.loads(out.decode() or "{}")
        except ValueError:
            info = {}
        body = open(body_path, "rb").read() if os.path.exists(body_path) else b""
        headers = _parse_headers(open(head_path, encoding="latin-1").read()) if os.path.exists(head_path) else {}

    code = proc.returncode
    status = int(info.get("http_code") or info.get("response_code") or 0)
    connected = float(info.get("time_connect") or 0) > 0
    if code == 28:
        if not connected:
            raise SourceError(f"Couldn't connect to {host} within {int(connect_timeout)} seconds "
                              "(network, DNS or firewall problem on this server).")
        raise SourceError(f"Connected to {host}, but it sent no reply within {int(timeout)} seconds. "
                          "United's bot protection may be holding the request; "
                          "use Setup > Upload Calendar.ics in the meantime.")
    if code in (6, 7):
        raise SourceError(f"Couldn't reach {host}: {err.decode().strip() or f'curl error {code}'}")
    if code != 0 and not status:
        raise SourceError(f"Download from {host} failed: {err.decode().strip() or f'curl error {code}'}")

    keep = ("content-type", "content-length", "content-disposition", "etag", "last-modified",
            "server", "date", "cache-control", "www-authenticate")
    debug = {
        "url": info.get("url_effective", url), "status": status,
        "elapsed_s": round(float(info.get("time_total") or 0), 2), "bytes": len(body),
        "client": await curl_version(), "headers": {k: v for k, v in headers.items() if k in keep},
    }
    if status == 304:
        return Download(304, not_modified=True, etag=etag, last_modified=last_modified, debug=debug)
    if status == 401:
        raise AuthError("CCS+ rejected the UID or Calendar Sync password (HTTP 401). Check CCS_USER.txt "
                        "(your UID) and CCS_PASSWORD.txt (the Calendar Sync password, not your CCS login).")
    if status == 403:
        server = headers.get("server", "")
        ref = re.search(r"Reference\s*#?\s*([\w.]+)", _snippet(body, 1000))
        who = "Akamai (United's bot protection)" if "akamai" in server.lower() else (server or "the server")
        raise BlockedError(f"Access denied by {who}, HTTP 403" + (f", reference {ref[1]}" if ref else "") + ".")
    if status >= 400:
        raise SourceError(f"CCS+ answered HTTP {status}: {_snippet(body, 160) or 'no details'}")
    if b"BEGIN:VCALENDAR" not in body[:2000]:
        raise SourceError("CCS+ answered, but not with a calendar file "
                          f"({headers.get('content-type', 'unknown type')}): {_snippet(body, 160)}")
    return Download(status, body=body, etag=headers.get("etag", ""),
                    last_modified=headers.get("last-modified", ""), debug=debug)


def check_calendar(body: bytes):
    """Make sure an uploaded file is an iCalendar file."""
    if b"BEGIN:VCALENDAR" not in body[:2000]:
        raise SourceError("That file isn't a calendar (.ics) file: " + (_snippet(body, 120) or "it's empty"))


# --- Processing ------------------------------------------------------------

def _as_dt(value, tz: ZoneInfo):
    """Normalise a DTSTART/DTEND value to (aware datetime | date)."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=tz)
    return value


# How close to a whole number of days an event must be to count as "24 hours".
# CCS+ writes full reserve/sick days as 00:01–23:59:59, which is 1 min 1 s short.
ALLDAY_TOLERANCE = timedelta(minutes=5)


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


def parse(raw: bytes, tz_name: str, defaults: Defaults):
    """Read a CCS+ calendar and normalise its events. Returns (Calendar, United's events, content hash)."""
    tz = ZoneInfo(tz_name)
    try:
        cal = Calendar.from_ical(raw)
    except Exception as e:
        raise SourceError(f"The calendar file from CCS+ couldn't be read: {e}")

    events: list[Event] = []
    for ev in cal.walk("VEVENT"):
        if "DTSTART" not in ev:
            continue
        start = _as_dt(ev["DTSTART"].dt, tz)
        if "DTEND" in ev:
            end = _as_dt(ev["DTEND"].dt, tz)
        elif "DURATION" in ev:
            end = start + ev["DURATION"].dt
        elif isinstance(start, datetime) and start.astimezone(tz).time() == datetime.min.time():
            # Starts at midnight with no end: CCS+ uses this for day codes (RDO, HDO, VRDO…) -> all-day
            start, end = _set_all_day(ev, start.astimezone(tz).date(), 1)
        elif isinstance(start, datetime):
            # Any other timed event with no end: apply DEFAULT_EVENT_HOURS
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
            if days >= 1 and abs(dur - timedelta(days=days)) <= ALLDAY_TOLERANCE:
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
            description=str(ev.get("DESCRIPTION", "")).strip()[:2000],
            uid=str(ev.get("UID", "")) or hashlib.sha1(f"{start}|{ev.get('SUMMARY')}".encode()).hexdigest(),
            free=str(ev.get("TRANSP", "")).upper() == "TRANSPARENT",
        ))

    events.sort(key=lambda e: e.start)
    return cal, events, hashlib.sha256(raw).hexdigest()


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
    else:   # UTC keeps the feed valid whatever time zones the file defines
        ev.add("dtstart", _utc(e.start))
        ev.add("dtend", _utc(e.end))


def _write_fields(ev, e: Event, marker: str):
    for prop in ("SUMMARY", "LOCATION", "DESCRIPTION", "X-ALT-DESC", "X-CALENDAR-STREAM"):
        ev.pop(prop, None)
    ev.add("summary", e.title)
    _write_times(ev, e)
    if e.location:
        ev.add("location", e.location)
    if e.description:
        ev.add("description", e.description)
    ev.add("x-calendar-stream", marker)


def render(cal: Calendar, base: list[Event], name: str, tz_name: str,
           edits: dict | None = None, customs: list[dict] | None = None,
           color: str = "") -> tuple[bytes, list[Event]]:
    """Apply edits, hides and added events to a parsed calendar.
    `color` (#rrggbb) is offered to subscribers as the calendar's colour; Apple Calendar uses it,
    Google Calendar ignores it. Returns (feed bytes for Google, all events for the status page)."""
    from icalendar import Event as VEvent

    edits, customs = edits or {}, customs or []
    for prop in ("X-WR-CALNAME", "X-WR-TIMEZONE", "REFRESH-INTERVAL", "X-PUBLISHED-TTL", "NAME",
                 "X-APPLE-CALENDAR-COLOR"):
        cal.pop(prop, None)
    if color:
        cal.add("x-apple-calendar-color", color.upper())
    cal.add("x-wr-calname", name)
    cal.add("name", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    cal.add("x-published-ttl", "PT1H")

    by_uid = {e.uid: e for e in base}
    final: list[Event] = []
    for ev in list(cal.subcomponents):
        if ev.name != "VEVENT":
            continue
        uid = str(ev.get("UID", ""))
        original = by_uid.get(uid)
        if original is None:
            continue
        ed = edits.get(uid)
        if not ed:
            final.append(original)
            continue
        e = Event(title=ed["title"], start=ed["start"], end=ed["end"], all_day=bool(ed["all_day"]),
                  location=ed.get("location", ""), description=ed.get("description", ""), uid=uid,
                  origin="united", edited=True, stale=ed.get("base") != original.fingerprint(),
                  hidden=bool(ed.get("hidden")), free=original.free)
        if e.hidden:
            cal.subcomponents.remove(ev)
        else:
            _write_fields(ev, e, "edited")
        final.append(e)

    stamp = datetime.now(ZoneInfo("UTC"))
    for c in customs:
        e = Event(title=c["title"], start=c["start"], end=c["end"], all_day=bool(c["all_day"]),
                  location=c.get("location", ""), description=c.get("description", ""), uid=c["uid"],
                  origin="custom")
        ev = VEvent()
        ev.add("uid", e.uid)
        ev.add("dtstamp", stamp)
        _write_fields(ev, e, "added")
        cal.add_component(ev)
        final.append(e)

    final.sort(key=lambda e: e.start)
    return cal.to_ical(), final


def process(raw: bytes, name: str, tz_name: str, defaults: Defaults) -> tuple[bytes, list[Event], str]:
    """Parse + render with no edits (used to check a new download)."""
    cal, events, digest = parse(raw, tz_name, defaults)
    feed, final = render(cal, events, name, tz_name)
    return feed, final, digest


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
