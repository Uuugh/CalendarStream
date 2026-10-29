"""Download calendars (United's CCS+ Calendar Sync, or any .ics feed) and prepare them for Google Calendar.

CCS+ Calendar Sync (CCS+ Settings > Schedule Settings > Calendar syncing) serves the schedule
as an iCalendar file behind HTTP Basic authentication:
    username = your UID, password = the Calendar Sync password created in CCS+.
Apple Calendar can subscribe to it directly; Google Calendar can't send a username and
password, so this app downloads it on a timer and republishes it as a feed Google can use.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
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


@dataclass
class Defaults:
    """How to treat events that have a start but no end (DTEND/DURATION)."""
    mode: str = "hours"     # "hours" or "allday"; "rules": leave it to the rules (the end is the start, no_end set)
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


async def download(url: str, username: str = "", password: str = "", etag: str = "", last_modified: str = "",
                   timeout: float = 60.0, connect_timeout: float = 20.0, who: str = "CCS+") -> Download:
    """Download a calendar. `username`/`password` are sent with HTTP Basic (CCS+); feeds send none.
    `who` names the server in messages ("CCS+", or the feed's host)."""
    host = urlparse(url).hostname or url
    with tempfile.TemporaryDirectory(prefix="calsync-") as tmp:
        body_path, head_path = os.path.join(tmp, "body"), os.path.join(tmp, "headers")
        # Credentials go to curl on stdin (a config file), never on the command line.
        config = [f"url = {_q(url)}", f'header = {_q("Accept: text/calendar, */*;q=0.5")}']
        if username:
            config.append(f"user = {_q(f'{username}:{password}')}")
        if etag:
            config.append(f"header = {_q('If-None-Match: ' + etag)}")
        if last_modified:
            config.append(f"header = {_q('If-Modified-Since: ' + last_modified)}")
        # https only (also after redirects), at most 5 redirects and 5 MB, like a hand upload
        args = [CURL, "--silent", "--show-error", "--location", "--config", "-",
                "--proto", "=https", "--proto-redir", "=https", "--max-redirs", "5", "--max-filesize", str(5 * 1024 * 1024),
                "--connect-timeout", str(int(connect_timeout)), "--max-time", str(int(timeout)),
                "--output", body_path, "--dump-header", head_path, "--write-out", "%{json}"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *args, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
        except FileNotFoundError:
            raise SourceError("curl isn't installed in this container (it's needed to download calendars).")
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
                          + ("United's bot protection may be holding the request; "
                             "use Upload & publish in the CCS+ Calendar Sync box in the meantime." if who == "CCS+" else
                             "Try again later."))
    if code == 1:
        raise SourceError(("The Calendar Sync link" if who == "CCS+" else "The feed link")
                          + " must start with https://, and may only redirect to https:// addresses (CalendarStream only downloads over https).")
    if code == 47:
        raise SourceError(f"{host} redirected too many times; check the "
                          + ("Calendar Sync link." if who == "CCS+" else "feed link."))
    if code == 63:
        raise SourceError(f"{host} sent more than 5 MB, which is too large for a schedule.")
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
    if status == 401 and who != "CCS+":
        raise AuthError(f"{host} wants a login (HTTP 401). Use the calendar's public or secret .ics "
                        "link, which works without one.")
    if status == 401:
        raise AuthError("CCS+ rejected the UID or Calendar Sync password (HTTP 401). Check both in "
                        "the CCS+ Calendar Sync box (the Calendar Sync password, not your CCS login).")
    if status == 403:
        server = headers.get("server", "")
        ref = re.search(r"Reference\s*#?\s*([\w.]+)", _snippet(body, 1000))
        who = "Akamai (United's bot protection)" if "akamai" in server.lower() else (server or "the server")
        raise BlockedError(f"Access denied by {who}, HTTP 403" + (f", reference {ref[1]}" if ref else "") + ".")
    if status >= 400:
        raise SourceError(f"{who} answered HTTP {status}: {_snippet(body, 160) or 'no details'}")
    if b"BEGIN:VCALENDAR" not in body[:2000]:
        raise SourceError(f"{who} answered, but not with a calendar file "
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


def _event(ev, tz: ZoneInfo, defaults: Defaults, uid: str = "", source: str = "ccs") -> Event | None:
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
    elif isinstance(start, datetime) and start.astimezone(tz).time() == datetime.min.time():
        # Starts at midnight with no end: CCS+ uses this for day codes (RDO, HDO, VRDO…) -> all-day
        start, end = _set_all_day(ev, start.astimezone(tz).date(), 1)
    elif isinstance(start, datetime) and defaults.mode == "rules":
        end, no_end = start, True       # any other timed event with no end: the rules decide
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
    return Event(
        title=str(ev.get("SUMMARY", "(no title)")),
        start=start.isoformat() if all_day else start.astimezone(tz).isoformat(),
        end=end.isoformat() if all_day else end.astimezone(tz).isoformat(),
        all_day=all_day,
        location=str(ev.get("LOCATION", "")),
        description=str(ev.get("DESCRIPTION", "")).strip()[:2000],
        uid=uid or str(ev.get("UID", "")) or hashlib.sha1(f"{start}|{ev.get('SUMMARY')}".encode()).hexdigest(),
        free=str(ev.get("TRANSP", "")).upper() == "TRANSPARENT",
        source=source,
        no_end=no_end,
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


MAX_FEED_EVENTS = 5000   # occurrences kept from one feed (a daily event over three years is ~1,100)


def parse_feed(raw: bytes, tz_name: str, defaults: Defaults, source: str, first: date, last: date):
    """Read a calendar feed (any .ics link). Repeating events are expanded into their occurrences
    between `first` and `last`. Each event's UID is "<source>/<UID>" (plus "/<start>" for an
    occurrence of a repeating event), so feeds can't collide with each other or with CCS+.
    Returns (events, content hash)."""
    import recurring_ical_events
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
        uid = str(ev.get("UID", "")) or hashlib.sha1(f"{ev.get('DTSTART')}|{ev.get('SUMMARY')}".encode()).hexdigest()
        repeats = "RRULE" in ev or "RDATE" in ev or "RECURRENCE-ID" in ev
        key = f"{source}/{uid}" + (f"/{ev['DTSTART'].dt.isoformat()}" if repeats and "DTSTART" in ev else "")
        if key in seen:
            continue
        seen.add(key)
        e = _event(ev, tz, defaults, uid=key, source=source)
        if e:
            events.append(e)
        if len(events) >= MAX_FEED_EVENTS:
            break
    events.sort(key=lambda e: e.start)
    return events, hashlib.sha256(raw).hexdigest()


def apply_changes(base: list[Event], edits: dict, customs: list[dict], source: str) -> list[Event]:
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
    return Event(title=ed["title"], start=ed["start"], end=ed["end"], all_day=bool(ed["all_day"]),
                 location=ed.get("location", ""), description=ed.get("description", ""), uid=original.uid,
                 origin="united", edited=True, stale=ed.get("base") != original.fingerprint(),
                 hidden=bool(ed.get("hidden")), free=original.free, color=ed.get("color", ""), source=original.source,
                 deleted=ed.get("deleted", ""))


def _custom(c: dict, source: str) -> Event:
    return Event(title=c["title"], start=c["start"], end=c["end"], all_day=bool(c["all_day"]),
                 location=c.get("location", ""), description=c.get("description", ""), uid=c["uid"],
                 origin="custom", color=c.get("color", ""), source=source, hidden=bool(c.get("deleted")),
                 deleted=c.get("deleted", ""))


def build_feed(events: list[Event], name: str, tz_name: str, color: str = "") -> bytes:
    """A calendar file written from events (hidden ones left out), for a feed source."""
    from icalendar import Event as VEvent
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
        _write_fields(ev, e, {"custom": "added", "rule": "rule"}.get(e.origin, "edited" if e.edited else "source"))
        _write_alarms(ev, e)
        cal.add_component(ev)
    return cal.to_ical()


def _write_alarms(ev, e: Event):
    """The event's reminders, as VALARMs (a calendar app shows them; some ignore subscribed ones)."""
    from icalendar import Alarm
    for minutes in e.alarm_minutes():
        a = Alarm()
        a.add("action", "DISPLAY")
        a.add("description", e.title)
        a.add("trigger", timedelta(minutes=-minutes))
        ev.add_component(a)


def _calendar_props(cal, name: str, tz_name: str, color: str):
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


def empty_feed(name: str, tz_name: str) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//calendar_stream//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", name)
    cal.add("x-wr-timezone", tz_name)
    cal.add("refresh-interval;value=duration", "PT1H")
    return cal.to_ical()
