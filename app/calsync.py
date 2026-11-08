"""Holds: Backward compatible calendar API and transport override wiring.
Depends on: app/calendars/defaults.py, app/calendars/download.py, app/calendars/downloads.py, app/calendars/edits.py, app/calendars/errors.py, app/calendars/event.py, app/calendars/feed.py, app/calendars/meeting.py, app/calendars/parsing.py, app/calendars/validation.py.
Used by: app/google/sync.py, app/main.py, app/routes/destinations.py, app/routes/events.py, app/routes/page.py, app/routes/sources.py, app/store.py.
Reads/writes: delegates to explicit calendar domain and data adapters.
Dart note: calendar data adapters; inject transports and limits; preserve the compatibility facade.
"""

from __future__ import annotations
import logging
from datetime import date, datetime, timedelta
import shutil
from .calendars.errors import AuthError, BlockedError, SourceError, NoReplyError
from .calendars.download import Download
from .calendars.event import Event
from .calendars.defaults import Defaults
from .calendars.meeting import meeting_link, event_meeting, MEETING_RE
from .calendars.validation import _snippet, check_calendar
from .calendars import downloads as _downloads
from .calendars import parsing as _parsing
from .calendars.parsing import _as_dt, _set_all_day, _event, parse
from .calendars.edits import apply_changes, _edited, _custom
from .calendars.feed import (
    build_feed,
    _write_alarms,
    _calendar_props,
    new_calendar,
    _utc,
    _write_times,
    notes_with_meeting,
    _write_fields,
    empty_feed,
)

log = logging.getLogger("calsync")

log = logging.getLogger("calsync")

CURL = shutil.which("curl") or "curl"

_curl_version = ""

BROWSER_PROFILE = "chrome"  # curl_cffi's newest Chrome

MAX_BYTES = 5 * 1024 * 1024  # like a hand upload

MAX_REDIRECTS = 5

CCS_CLIENTS = ("auto", "browser", "browser-patient", "curl")

_PLANS = {
    "curl": [("curl", 1.0, 0)],
    "browser": [("browser", 1.0, 0)],
    "browser-patient": [("browser", 1.5, 0), ("browser", 1.5, 5), ("browser", 1.5, 15)],
    "auto": [("browser", 1.0, 0), ("browser", 2.0, 3), ("curl", 1.0, 0)],
}

PAUSE_SCALE = 1.0  # the tests set 0

_SESSION_EXTRA: dict = {}  # the tests point the browser-like client at their own CA

_KEEP = (
    "content-type",
    "content-length",
    "content-disposition",
    "etag",
    "last-modified",
    "server",
    "date",
    "cache-control",
    "www-authenticate",
)

ALLDAY_TOLERANCE = timedelta(minutes=5)

MAX_FEED_EVENTS = (
    5000  # occurrences kept from one feed (a daily event over three years is ~1,100)
)


def ccs_client(client: str | None = None) -> str:
    return _downloads.ccs_client(client, CCS_CLIENTS=CCS_CLIENTS)


def _q(value: str) -> str:
    return _downloads._q(value)


def _parse_headers(raw: str) -> dict:
    return _downloads._parse_headers(raw)


async def curl_version() -> str:
    global _curl_version
    _curl_version = await _downloads.curl_version(
        CURL=CURL, _curl_version=_curl_version
    )
    return _curl_version


def _no_reply(host: str, timeout: float, who: str) -> NoReplyError:
    return _downloads._no_reply(host, timeout, who)


def _not_https(who: str) -> SourceError:
    return _downloads._not_https(who)


def _too_many_redirects(host: str, who: str) -> SourceError:
    return _downloads._too_many_redirects(host, who)


def _too_large(host: str) -> SourceError:
    return _downloads._too_large(host)


def _finish(
    status: int,
    body: bytes,
    headers: dict,
    debug: dict,
    host: str,
    who: str,
    etag: str,
    last_modified: str,
) -> Download:
    return _downloads._finish(
        status, body, headers, debug, host, who, etag, last_modified
    )


async def _download_curl(
    *,
    url: str,
    username: str,
    password: str,
    etag: str,
    last_modified: str,
    timeout: float,
    connect_timeout: float,
    who: str,
) -> Download:
    return await _downloads._download_curl(
        url=url,
        username=username,
        password=password,
        etag=etag,
        last_modified=last_modified,
        timeout=timeout,
        connect_timeout=connect_timeout,
        who=who,
        CURL=CURL,
        MAX_BYTES=MAX_BYTES,
        MAX_REDIRECTS=MAX_REDIRECTS,
        _KEEP=_KEEP,
        _finish=_finish,
        _no_reply=_no_reply,
        _not_https=_not_https,
        _parse_headers=_parse_headers,
        _q=_q,
        _too_large=_too_large,
        _too_many_redirects=_too_many_redirects,
        curl_version=curl_version,
    )


async def _download_browser(
    *,
    url: str,
    username: str,
    password: str,
    etag: str,
    last_modified: str,
    timeout: float,
    connect_timeout: float,
    who: str,
) -> Download:
    return await _downloads._download_browser(
        url=url,
        username=username,
        password=password,
        etag=etag,
        last_modified=last_modified,
        timeout=timeout,
        connect_timeout=connect_timeout,
        who=who,
        BROWSER_PROFILE=BROWSER_PROFILE,
        MAX_BYTES=MAX_BYTES,
        MAX_REDIRECTS=MAX_REDIRECTS,
        _KEEP=_KEEP,
        _SESSION_EXTRA=_SESSION_EXTRA,
        _finish=_finish,
        _no_reply=_no_reply,
        _not_https=_not_https,
        _too_large=_too_large,
        _too_many_redirects=_too_many_redirects,
    )


async def download(
    url: str,
    username: str = "",
    password: str = "",
    etag: str = "",
    last_modified: str = "",
    timeout: float = 60.0,
    connect_timeout: float = 20.0,
    who: str = "CCS+",
    client: str | None = None,
) -> Download:
    return await _downloads.download(
        url,
        username,
        password,
        etag,
        last_modified,
        timeout,
        connect_timeout,
        who,
        client,
        PAUSE_SCALE=PAUSE_SCALE,
        _PLANS=_PLANS,
        _download_browser=_download_browser,
        _download_curl=_download_curl,
        ccs_client=ccs_client,
        log=log,
    )


def parse_feed(
    raw: bytes, tz_name: str, defaults: Defaults, source: str, first: date, last: date
):
    return _parsing.parse_feed(
        raw, tz_name, defaults, source, first, last, max_feed_events=MAX_FEED_EVENTS
    )
