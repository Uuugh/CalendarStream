"""Holds: Application composition and backward compatible public API.
Depends on: app/calendars/view_helpers.py, app/calsync.py, app/config.py, app/google/health.py, app/google/traffic_log.py, app/gsync.py, app/i18n.py, app/icons.py, app/item_order.py, app/links.py, app/log_tail.py, app/logins.py, app/routes/__init__.py, app/routes/account.py, app/routes/events.py, app/routes/page.py, app/routes/rules.py, app/rules.py, app/runtime/change.py, app/runtime/state.py, app/secretbox.py, app/services/accounts.py, app/services/addresses.py, app/services/administrator.py, app/services/authentication.py, app/services/calendar_destinations.py, app/services/calendar_sources.py, app/services/calendar_view.py, app/services/clock.py, app/services/deletions.py, app/services/event_history.py, app/services/event_links.py, app/services/event_templates.py, app/services/field_error.py, app/services/google_changes.py, app/services/google_job.py, app/services/google_sync.py, app/services/google_view.py, app/services/history.py, app/services/http.py, app/services/invites.py, app/services/lifecycle.py, app/services/logging_setup.py, app/services/page_settings.py, app/services/publishing.py, app/services/route_helpers.py, app/services/rule_migration.py, app/services/rule_settings.py, app/services/source_jobs.py, app/services/update_jobs.py, app/store.py, app/updates.py.
Used by: external callers and tests.
Reads/writes: constructs runtime state, logging and app resources; feature services own storage and network operations.
Dart note: application composition root; bind feature services and retain the legacy Python API.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import ipaddress
import calendar as pycal
import json
import logging
import re
import secrets
import socket
import threading
from collections import deque
from contextlib import asynccontextmanager
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlencode, urlparse
from zoneinfo import ZoneInfo, available_timezones

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler as default_http_error
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from markupsafe import Markup, escape
from fastapi.templating import Jinja2Templates

from . import __version__, i18n, icons
from . import links as links_mod
from . import rules as rules_mod
from .calsync import (
    AuthError,
    BlockedError,
    Defaults,
    Event,
    SourceError,
    apply_changes,
    build_feed,
    download,
    parse,
    parse_feed,
)
from .config import normalise_public_url, settings
from .google.health import GoogleHealth
from .google.traffic_log import TrafficLog as GoogleTrafficLog
from .gsync import (
    CALENDAR_COLORS,
    GOOGLE_COLORS,
    Google,
    GoogleError,
    nearest_calendar_color,
    nearest_color_id,
)
from .logins import Logins
from .secretbox import SecretBox
from .store import Store, from_iso, iso
from .updates import (
    FREQUENCIES,
    RELEASES,
    Updater,
    UpdaterError,
    Updates,
    channel as release_channel,
)

from .services import logging_setup as _service_logging_setup
from .services import accounts as _service_accounts
from .services import clock as _service_clock
from .services import calendar_sources as _service_calendar_sources
from .services import calendar_destinations as _service_calendar_destinations
from .services import rule_settings as _service_rule_settings
from .services import rule_migration as _service_rule_migration
from .services import event_templates as _service_event_templates
from .services import page_settings as _service_page_settings
from .services import history as _service_history
from .services import google_changes as _service_google_changes
from .services import google_sync as _service_google_sync
from .services import event_history as _service_event_history
from .services import publishing as _service_publishing
from .services import event_links as _service_event_links
from .services import deletions as _service_deletions
from .services import source_jobs as _service_source_jobs
from .services import update_jobs as _service_update_jobs
from .services import lifecycle as _service_lifecycle
from .services import http as _service_http
from .services import authentication as _service_authentication
from .services import addresses as _service_addresses
from .services import google_view as _service_google_view
from .services import calendar_view as _service_calendar_view
from .services import route_helpers as _service_route_helpers
from .services import administrator as _service_administrator
from .services import invites as _service_invites

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
log = logging.getLogger("calendar_stream")
logging.getLogger("httpx").setLevel(
    logging.WARNING
)  # one line per Google request is too chatty


from .log_tail import _LogTail

LOG_TAIL_LINES = 3000
LOG_TAIL = _LogTail(LOG_TAIL_LINES)


def tail_logs():
    return _service_logging_setup.tail_logs(LOG_TAIL=LOG_TAIL)


TZ = ZoneInfo(settings.timezone)
store = Store(settings.dsn)
box = SecretBox(settings.db_password)
google_traffic = (
    GoogleTrafficLog()
)  # (F59) every account's calls to Google, shared, for the Beta traffic view
google = Google(
    store, box, settings.timezone, traffic=google_traffic
)  # the first Google account (connected in Settings)
ACCOUNT_RE = re.compile(r"^(|a[0-9a-f]{6})$")
_accounts: dict[str, Google] = {"": google}


def google_for(account: str = "") -> Google:
    return _service_accounts.google_for(
        account,
        Google=Google,
        _accounts=_accounts,
        box=box,
        google_traffic=google_traffic,
        settings=settings,
        store=store,
    )


google_health = GoogleHealth(
    store
)  # (0.2.8-beta.35, F58 7) each account's health and back-off


def dest_google(d: dict) -> Google:
    return _service_accounts.dest_google(d, Google=Google, google_for=google_for)


def google_accounts() -> list[str]:
    return _service_accounts.google_accounts(destinations=destinations)


def _shared_grant(g: Google) -> bool:
    return _service_accounts._shared_grant(
        g, Google=Google, google_accounts=google_accounts, google_for=google_for
    )


logins = Logins(store, box)
updates = Updates(store)
updater = Updater()  # the optional updater container behind "Update now"
MAX_AUTH_FAILURES = 2  # pause automatic downloads after this many rejected sign-ins (avoids account lockout)
CSRF_TOKEN = secrets.token_urlsafe(
    24
)  # forms on the status page must carry this; renewed when the login changes
WELCOME_TOKEN = secrets.token_urlsafe(
    24
)  # the first-visit page's own token (shown before any login exists)


def now():
    return _service_clock.now(TZ=TZ)


# --- Calendar sources and destinations ------------------------------------------------
#
# A source is where events come from: United's CCS+ Calendar Sync (ID "ccs", at most one), any .ics
# feed link (type "ics", IDs such as "f3a9c1"), or a local calendar (0.2.8: type "local", IDs such as
# "l3a9c1"), which only holds events added here. The default calendar (kv "default_source", a CalendarStream
# calendar; before 0.2.8-beta.28 the top one) takes the events added here unless another is chosen; the order of
# the sources is only the priority when events conflict. Each source has its own name, color (the
# default color of its events), rules, check interval, status and events. CCS+ keeps the database
# keys used before 0.2 ("calendar_name", "status"…); a feed source's keys are the same plus ":<id>" (skey).
#
# A destination is where events go, independently of the sources: a Google calendar (Autosync) or a
# calendar feed (a link and a subscribe page). There can be several of each; each has its own name
# and the list of sources whose events it gets, with each source's colors and rules. Saved in kv
# "destinations": [{"id": "d1a2b3c", "type": "google" | "feed", "name", "sources": [IDs], "token"}],
# "token" being a feed's stream name. A new install starts with no sources and no destinations.

SOURCE_TYPES = ("ccs", "ics", "local")
DESTINATION_TYPES = {"google": "Google calendar", "feed": "Calendar feed"}
SID_RE = re.compile(r"^(ccs|[fl][0-9a-f]{6})$")
DID_RE = re.compile(r"^d[0-9a-f]{6}$")


def skey(sid: str, base: str) -> str:
    return _service_calendar_sources.skey(sid, base)


def sources() -> list[dict]:
    return _service_calendar_sources.sources(SID_RE=SID_RE, store=store)


def source(sid: str) -> dict | None:
    return _service_calendar_sources.source(sid, sources=sources)


def source_ids() -> list[str]:
    return _service_calendar_sources.source_ids(sources=sources)


def default_sid() -> str:
    return _service_calendar_sources.default_sid(sources=sources, store=store)


def destinations(kind: str | None = None) -> list[dict]:
    return _service_calendar_destinations.destinations(
        kind,
        ACCOUNT_RE=ACCOUNT_RE,
        COLOR_RE=COLOR_RE,
        DESTINATION_TYPES=DESTINATION_TYPES,
        DID_RE=DID_RE,
        _iso_day=_iso_day,
        source_ids=source_ids,
        store=store,
    )


def _iso_day(value) -> str:
    return _service_calendar_destinations._iso_day(value)


def destination(did: str) -> dict | None:
    return _service_calendar_destinations.destination(did, destinations=destinations)


def save_destinations(found: list[dict]):
    return _service_calendar_destinations.save_destinations(found, store=store)


def new_did() -> str:
    return _service_calendar_destinations.new_did(destinations=destinations)


def migrate_sources():
    return _service_calendar_sources.migrate_sources(
        google=google, logins=logins, store=store
    )


def migrate_destinations():
    return _service_calendar_destinations.migrate_destinations(
        calendar_name=calendar_name,
        destinations=destinations,
        google=google,
        new_did=new_did,
        save_destinations=save_destinations,
        settings=settings,
        skey=skey,
        source_ids=source_ids,
        store=store,
    )


def calendar_url() -> str:
    return _service_calendar_sources.calendar_url(settings=settings, store=store)


def source_url(sid: str) -> str:
    return _service_calendar_sources.source_url(
        sid, calendar_url=calendar_url, source=source
    )


def calendar_name(sid: str = "ccs") -> str:
    return _service_calendar_sources.calendar_name(
        sid, settings=settings, skey=skey, source_url=source_url, store=store
    )


COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
DEFAULT_COLOR = "#1d4ed8"  # a calendar's events on this page until a color is chosen (its module's color box)


def calendar_color(sid: str = "ccs") -> str:
    return _service_calendar_sources.calendar_color(
        sid, COLOR_RE=COLOR_RE, skey=skey, store=store
    )


MAX_TAGS, MAX_TAG_LEN = 30, 40

# Rules (app/rules.py, 0.2.8): one ordered list in kv "rules" ("If … Then …"; the order is the priority),
# each saying which calendars it applies to. Events are read with RULES_PARSE: an event with no end
# time keeps its start as its end (and no_end set), and 24-hour events keep their times, so the
# rules ("Items without an end time", "24-hour events") decide what becomes of them.
RULES_PARSE = Defaults(mode="rules", allday_24h=False)
RULE_WHEN = rules_mod.WHEN


def all_rules() -> list[dict]:
    return _service_rule_settings.all_rules(
        rules_mod=rules_mod, source_ids=source_ids, store=store
    )


def rule_used(rid: str) -> list[str]:
    return _service_rule_settings.rule_used(
        rid, calendar_name=calendar_name, store=store
    )


def save_rules(found: list[dict]):
    return _service_rule_settings.save_rules(found, rules_mod=rules_mod, store=store)


def source_rules(sid: str) -> list[dict]:
    return _service_rule_settings.source_rules(
        sid, all_rules=all_rules, rules_mod=rules_mod
    )


def ruleset(sid: str) -> rules_mod.Ruleset:
    return _service_rule_settings.ruleset(
        sid,
        TZ=TZ,
        event_templates=event_templates,
        rules_mod=rules_mod,
        settings=settings,
        source_rules=source_rules,
    )


def color_name(color: str) -> str:
    return _service_rule_settings.color_name(
        color, GOOGLE_COLORS=GOOGLE_COLORS, nearest_color_id=nearest_color_id
    )


def rule_label(r: dict, lang: str = "en") -> str:
    return _service_rule_settings.rule_label(
        r,
        lang,
        color_name=color_name,
        event_templates=event_templates,
        i18n=i18n,
        rules_mod=rules_mod,
    )


def _swatch(color: str) -> str:
    return _service_rule_settings._swatch(color)


def rule_label_html(r: dict, lang: str = "en") -> Markup:
    return _service_rule_settings.rule_label_html(
        r,
        lang,
        _swatch=_swatch,
        color_name=color_name,
        event_templates=event_templates,
        i18n=i18n,
        rule_label=rule_label,
        rules_mod=rules_mod,
    )


def migrate_rules():
    return _service_rule_settings.migrate_rules(
        _migrate_rules_v3=_migrate_rules_v3,
        _v3_rules=_v3_rules,
        rules_mod=rules_mod,
        save_rules=save_rules,
        settings=settings,
        skey=skey,
        source_ids=source_ids,
        store=store,
    )


def share_converted_rules():
    return _service_rule_settings.share_converted_rules(
        all_rules=all_rules, save_rules=save_rules, sources=sources, store=store
    )


def first_named_calendar() -> str:
    return _service_calendar_sources.first_named_calendar(
        calendar_name=calendar_name, sources=sources
    )


def ensure_local():
    return _service_calendar_sources.ensure_local(
        destinations=destinations,
        new_local=new_local,
        save_destinations=save_destinations,
        sources=sources,
        store=store,
    )


def is_local(sid: str) -> bool:
    return _service_calendar_sources.is_local(sid, source=source)


def last_local(sid: str) -> bool:
    return _service_calendar_sources.last_local(sid, is_local=is_local, sources=sources)


def new_local() -> str:
    return _service_calendar_sources.new_local(source_ids=source_ids)


# --- Rules from before 0.2.8, only read to convert them (migrate_rules) ------------------------------
# 0.2.6–0.2.8-beta.1: kv "rule_templates" (the library: one-condition rules of the kinds below, "owner"
# set for a rule local to one source) and each source's "rule_subs" (the ones it uses, in order).
# 0.2.5 and before: each source's own "calendar_tags" and "defaults", converted first (_migrate_rules_v3).

TAG_MODES = {
    "word": "Whole word",
    "contains": "Contains",
    "starts": "Starts with",
    "exact": "Exact title",
}
V3_TYPES = ("color", "event", "changes", "no_end", "allday24")


def _v3_rules(raw: list) -> list[dict]:
    return _service_rule_migration._v3_rules(
        raw,
        COLOR_RE=COLOR_RE,
        MAX_TAG_LEN=MAX_TAG_LEN,
        RULE_WHEN=RULE_WHEN,
        TAG_MODES=TAG_MODES,
        V3_TYPES=V3_TYPES,
        rules_mod=rules_mod,
    )


_V3_KEYS = {
    "color": ("tag", "mode", "case", "color"),
    "event": ("tag", "mode", "case", "template", "when", "offset"),
    "changes": ("tag", "mode", "case"),
    "no_end": ("no_end_mode", "minutes"),
    "allday24": ("allday",),
}


def _v3_add(lib: list[dict], rule: dict) -> str:
    return _service_rule_migration._v3_add(
        lib, rule, _V3_KEYS=_V3_KEYS, _v3_rules=_v3_rules
    )


def _migrate_rules_v3():
    return _service_rule_migration._migrate_rules_v3(
        _v3_add=_v3_add,
        _v3_rules=_v3_rules,
        settings=settings,
        skey=skey,
        source_ids=source_ids,
        store=store,
    )


# --- Event templates ------------------------------------------------------------------------
# Ready-made events: used by "Create event" rules, and offered when adding an event by hand.

MAX_TEMPLATES = 30


def event_templates() -> list[dict]:
    return _service_event_templates.event_templates(
        EVENT_COLORS=EVENT_COLORS, MAX_TEMPLATES=MAX_TEMPLATES, store=store
    )


# Collapsible sections on the status page, and whether each starts open. The open/closed state
# is saved in the database so it's the same in every browser.
SECTIONS = {
    "status": True,
    "activity": False,
    "rules": False,
    "templates": False,
    "googlesync": False,
    "beta": False,
}  # (F59) the Beta: Google Traffic section, below Activity


FOLD_AFTER = (
    24 * 3600
)  # (0.2.8-beta.26, F20) a section or module left open folds again after this many seconds


def section_state() -> dict:
    return _service_page_settings.section_state(
        FOLD_AFTER=FOLD_AFTER, SECTIONS=SECTIONS, store=store
    )


def lang_for(request: Request) -> str:
    return _service_page_settings.lang_for(request, i18n=i18n, store=store)


def page(
    request: Request,
    name: str,
    context: dict,
    status_code: int = 200,
    lang: str | None = None,
):
    return _service_page_settings.page(
        request,
        name,
        context,
        status_code,
        lang,
        FREQUENCIES=FREQUENCIES,
        RELEASES=RELEASES,
        __version__=__version__,
        _local_time=_local_time,
        auto_update=auto_update,
        dates_for=dates_for,
        i18n=i18n,
        iso=iso,
        lang_for=lang_for,
        look=look,
        release_channel=release_channel,
        store=store,
        templates=templates,
        ui_clock=ui_clock,
        ui_theme=ui_theme,
        updater=updater,
        updates=updates,
    )


ANIM_DEFAULT = {"i": 100, "d": 100}


def look() -> dict:
    return _service_page_settings.look(ANIM_DEFAULT=ANIM_DEFAULT, store=store)


THEMES = ("system", "light", "dark")
CLOCKS = ("auto", "12", "24")


def ui_clock() -> str:
    return _service_page_settings.ui_clock(CLOCKS=CLOCKS, store=store)


# The time zone the status page's calendar is shown in. It only changes how the calendar looks
# here; the feed, Google and the server's own clock (TZ in .env) are unaffected.
ALL_ZONES = sorted(
    z
    for z in available_timezones()
    if "/" in z and not z.startswith(("Etc/", "SystemV/", "posix/", "right/"))
)
COMMON_ZONES = [
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Phoenix",
    "America/Los_Angeles",
    "America/Anchorage",
    "Pacific/Honolulu",
    "Pacific/Guam",
    "UTC",
    "Europe/London",
    "Europe/Frankfurt",
    "Asia/Tokyo",
    "Asia/Hong_Kong",
    "Australia/Sydney",
]


def valid_zone(name: str) -> bool:
    return _service_page_settings.valid_zone(name, ALL_ZONES=ALL_ZONES)


def display_zone() -> str:
    return _service_page_settings.display_zone(
        settings=settings, store=store, valid_zone=valid_zone
    )


def display_tz() -> ZoneInfo:
    return _service_page_settings.display_tz(display_zone=display_zone)


def dates_for(lang: str) -> i18n.Dates:
    return _service_page_settings.dates_for(lang, i18n=i18n, ui_clock=ui_clock)


def ui_theme() -> str:
    return _service_page_settings.ui_theme(THEMES=THEMES, store=store)


from .runtime.state import bind_source_state

State = bind_source_state(
    get_TZ=lambda: TZ,
    get_calendar_name=lambda: calendar_name,
    get_from_iso=lambda: from_iso,
    get_iso=lambda: iso,
    get_log=lambda: log,
    get_log_kind=lambda: log_kind,
    get_skey=lambda: skey,
    get_store=lambda: store,
)
State.__module__, State.__qualname__ = __name__, "State"


# --- History, Undo & Logs (0.2.8-beta.15) -------------------------------------------------------
# Every line has a Type. A change made on the page (a calendar, feed, rule, template or event) keeps what
# was there before and after it, so it can be undone, and then redone: a stack, newest first. The newest
# changes are kept (Settings › History: how many); older ones pop off, and what they kept is forgotten.

LOG_KINDS = (
    "Calendar",
    "Feed",
    "Rule",
    "Event",
    "Google",
    "Settings",
    "Update",
    "Sync",
)


def log_kind(msg: str, sid: str = "ccs") -> str:
    return _service_history.log_kind(msg, sid)


# What each kind of module is: its (i), with the person's note after it (0.2.8-beta.15)
MODULE_ABOUT = {
    "local": "Only the events you add here. Goes into every feed.",
    "ccs": "Your United CCS+ schedule, downloaded with your Calendar Sync password.",
    "google": "A Google calendar, read from its secret iCal address.",
    "apple": "An Apple calendar, read from its public link.",
    "feed": "A calendar read from its link (.ics).",
    "gdest": "The same as Google 1-way Sync, and changes made in Google come back here.",
    "gdest1": "CalendarStream writes into a Google calendar within seconds, with rule colors and reminders.",
    "gfeed": "A link any calendar app subscribes to: Google, Apple, Outlook, or send it to someone.",
    "ffeed": "A link any calendar app subscribes to: Google, Apple, Outlook, or send it to someone.",
    "apioff": "Needs Google Calendar API Sync, which your admin turns on in ☰ Settings.",
}

SOURCE_BASES = (
    "calendar_name",
    "calendar_color",
    "calendar_tags",
    "rule_subs",
    "defaults",
    "note",
    "sync_interval",
    "http_cache",
    "status",
    "feed_reads",
    "off",
)
UNDO_KEYS = (
    "sources",
    "default_source",
    "destinations",
    "rules",
    "event_templates",
    "event_alarms",
    "event_links",
    "rule_conflicts_ignored",
)
UNDO_KEEP = 100  # changes remembered for Undo, unless History says otherwise (20 until 0.2.8-beta.23, F15)


def undo_keep() -> int:
    return _service_history.undo_keep(UNDO_KEEP=UNDO_KEEP, store=store)


from .runtime.change import bind_change

Change = bind_change(
    get_SOURCE_BASES=lambda: SOURCE_BASES,
    get_UNDO_KEYS=lambda: UNDO_KEYS,
    get_pop_undo=lambda: pop_undo,
    get_skey=lambda: skey,
    get_state=lambda: state,
    get_store=lambda: store,
)
Change.__module__, Change.__qualname__ = __name__, "Change"


def pop_undo():
    return _service_history.pop_undo(
        finish_deletions=finish_deletions, store=store, undo_keep=undo_keep
    )


def after_restore():
    return _service_history.after_restore(
        ensure_local=ensure_local,
        rebuild=rebuild,
        source_ids=source_ids,
        source_tasks=source_tasks,
        start_source=start_source,
        state=state,
        states=states,
        stop_source=stop_source,
        store=store,
    )


states: dict[str, State] = {}


def st(sid: str) -> State:
    return _service_history.st(sid, State=State, states=states)


state = st("ccs")  # CCS+, and the activity log for everything that isn't a source's


# --- Google Calendar sync --------------------------------------------------------

GOOGLE_FULL_CHECK = timedelta(
    hours=24
)  # how often Google's copy is checked and repaired
GOOGLE_RETRY = timedelta(minutes=15)  # wait after a failed sync before trying again
WATCH_RENEW = timedelta(
    days=1
)  # renew Google's change notifications this long before they end
WATCH_RETRY = timedelta(hours=6)  # after Google refused them, ask again this much later


from .services.google_job import GoogleJob

google_job = GoogleJob()


def request_google_sync(full: bool = False):
    return _service_google_sync.request_google_sync(full, google_job=google_job)


def notify_address() -> str:
    return _service_google_sync.notify_address(public_url=public_url)


async def ensure_watch(sid: str):
    return await _service_google_sync.ensure_watch(
        sid,
        GoogleError=GoogleError,
        WATCH_RENEW=WATCH_RENEW,
        WATCH_RETRY=WATCH_RETRY,
        dest_google=dest_google,
        destination=destination,
        destinations=destinations,
        google=google,
        notify_address=notify_address,
        now=now,
        state=state,
    )


def source_off(sid: str) -> bool:
    return _service_google_sync.source_off(sid, skey=skey, store=store)


def dest_events(d: dict) -> list[Event]:
    return _service_google_sync.dest_events(
        d, Event=Event, TZ=TZ, _span=_span, source_off=source_off, store=store
    )


def event_colorer():
    return _service_google_sync.event_colorer(
        calendar_color=calendar_color, source_ids=source_ids
    )


EARLIEST = date(
    2000, 1, 1
)  # a Google destination with no Start date gets every event from here on


def sync_window_start() -> date:
    return _service_google_sync.sync_window_start(now=now)


# --- Two-way sync (0.2.8-beta.10) -------------------------------------------------------
# Only the calendars CalendarStream makes in Google. A change made there becomes a change here, exactly
# like making it on the status page (CCS+ itself is never touched): an edit of a source's event is an
# edit, one of an added event changes it; an event added in Google goes into a CalendarStream (local)
# calendar; a deletion strikes the event through here (0.2.8-beta.15: Undo in History restores it). A
# rule's events stay read-only (put back). When both sides changed, the newest change wins.

_FIELDS = ("title", "start", "end", "all_day", "location", "description")


def google_held() -> dict:
    return _service_google_changes.google_held(store=store)


def _same_time(a: str, b: str) -> bool:
    return _service_google_changes._same_time(a, b)


async def apply_google_changes(d: dict, changes: list[dict]) -> list[str]:
    return await _service_google_changes.apply_google_changes(
        d,
        changes,
        _FIELDS=_FIELDS,
        _same_time=_same_time,
        calendar_name=calendar_name,
        delete_events=delete_events,
        dest_google=dest_google,
        google_held=google_held,
        rebuild=rebuild,
        source=source,
        state=state,
        store=store,
        united_original=united_original,
    )


_unsigned_said: set[str] = (
    set()
)  # (0.2.8-beta.35, F58 1, I5) Google modules already reported as not signed in


def _say_not_signed_in(mods: list[dict]):
    return _service_google_sync._say_not_signed_in(
        mods, _unsigned_said=_unsigned_said, state=state
    )


async def google_sync_once(full: bool) -> bool:
    return await _service_google_sync.google_sync_once(
        full,
        _say_not_signed_in=_say_not_signed_in,
        _sync_account=_sync_account,
        _unsigned_said=_unsigned_said,
        destinations=destinations,
        event_colorer=event_colorer,
        google=google,
        google_accounts=google_accounts,
        google_for=google_for,
        google_health=google_health,
        google_job=google_job,
    )


COLOR_TRY = 3  # (0.2.8-beta.19) a refused color is tried once per color and per COLOR_TRY (3: beta.21's other ways, I1)

# (0.2.8-beta.21, I1) how History names the way Google took a calendar's color (gsync.COLOR_WAYS)
COLOR_WAY_TEXT = {
    "rgb": "as its RGB color",
    "colorId": "as the nearest of Google's calendar colors",
    "put": "with a full update of the calendar's entry",
}


async def _sync_account(
    g: Google, dests: list[dict], total: int, color_for, full: bool
) -> bool:
    return await _service_google_sync._sync_account(
        g,
        dests,
        total,
        color_for,
        full,
        CALENDAR_COLORS=CALENDAR_COLORS,
        COLOR_TRY=COLOR_TRY,
        COLOR_WAY_TEXT=COLOR_WAY_TEXT,
        EARLIEST=EARLIEST,
        Google=Google,
        GoogleError=GoogleError,
        _remember_calendar=_remember_calendar,
        apply_google_changes=apply_google_changes,
        dest_events=dest_events,
        ensure_watch=ensure_watch,
        google_health=google_health,
        google_held=google_held,
        nearest_calendar_color=nearest_calendar_color,
        state=state,
        store=store,
    )


def _remember_calendar(did: str, g: Google):
    return _service_google_sync._remember_calendar(did, g, Google=Google, store=store)


def _remembered_calendar(did: str) -> str | None:
    return _service_google_sync._remembered_calendar(did, store=store)


async def google_loop():
    return await _service_google_sync.google_loop(
        GOOGLE_FULL_CHECK=GOOGLE_FULL_CHECK,
        GOOGLE_RETRY=GOOGLE_RETRY,
        google_job=google_job,
        google_sync_once=google_sync_once,
        log=log,
        now=now,
    )


def feed_window() -> tuple[date, date]:
    return _service_publishing.feed_window(now=now)


def customs_for(sid: str) -> list[dict]:
    return _service_publishing.customs_for(sid, store=store)


def source_events(
    sid: str, raw: bytes | None, rs: rules_mod.Ruleset | None = None
) -> tuple[list[Event], str]:
    return _service_publishing.source_events(
        sid,
        raw,
        rs,
        Event=Event,
        RULES_PARSE=RULES_PARSE,
        feed_window=feed_window,
        parse=parse,
        parse_feed=parse_feed,
        rules_mod=rules_mod,
        ruleset=ruleset,
        settings=settings,
        source=source,
    )


def event_alarms() -> dict[str, str]:
    return _service_publishing.event_alarms(store=store)


def publish(
    raw: bytes | None, sha: str | None = None, sid: str = "ccs"
) -> tuple[list[Event], list[Event]]:
    return _service_publishing.publish(
        raw,
        sha,
        sid,
        Event=Event,
        TZ=TZ,
        add_change_notes=add_change_notes,
        apply_changes=apply_changes,
        build_feed=build_feed,
        calendar_color=calendar_color,
        calendar_name=calendar_name,
        customs_for=customs_for,
        event_alarms=event_alarms,
        follow_links=follow_links,
        request_google_sync=request_google_sync,
        ruleset=ruleset,
        settings=settings,
        skey=skey,
        source_events=source_events,
        st=st,
        store=store,
    )


# --- Linked events (F3.2; since 0.2.8-beta.27, F3: link rules): see app/links.py ------------------------------------

_following = False


def event_links() -> dict[str, dict]:
    return _service_event_links.event_links(all_rules=all_rules, links_mod=links_mod)


def set_event_links(found: dict[str, dict]):
    return _service_event_links.set_event_links(
        found, all_rules=all_rules, save_rules=save_rules
    )


def link_rule_for(uid: str) -> dict | None:
    return _service_event_links.link_rule_for(uid, all_rules=all_rules)


def migrate_links():
    return _service_event_links.migrate_links(
        all_rules=all_rules,
        links_mod=links_mod,
        rules_mod=rules_mod,
        save_rules=save_rules,
        source_ids=source_ids,
        store=store,
    )


def follow_links(sid: str, events: list[Event]):
    return _service_event_links.follow_links(
        sid,
        events,
        _hide=_hide,
        event_links=event_links,
        links_mod=links_mod,
        rebuild=rebuild,
        set_event_links=set_event_links,
        state=state,
        store=store,
        united_original=united_original,
        get_following=lambda: _following,
        set_following=_set_following,
    )


def _set_following(value):
    global _following
    _following = value


def _hide(e: Event):
    return _service_event_links._hide(
        e, Event=Event, store=store, united_original=united_original
    )


# --- Deleted events (0.2.8-beta.15) -------------------------------------------------------------------
# A deleted event stays on the page, struck through and greyed, saying where it was deleted, until its
# Undo pops off History; it's in no feed meanwhile. Undo (Restore) brings it back. After that it's gone:
# an added event for good, a source's event hidden (its source would only send it again).

DELETED_WHERE = {
    "calendarstream": "Deleted in CalendarStream",
    "google": "Deleted in Google Calendar",
    "rule": "Deleted by a rule",
    "united": "Removed by United (CCS+)",
    "feed": "Gone from the feed",
}


def mark_deleted(e: Event, where: str):
    return _service_deletions.mark_deleted(
        e, where, Event=Event, _hide=_hide, now=now, store=store
    )


def unmark_deleted(uid: str):
    return _service_deletions.unmark_deleted(uid, store=store)


def delete_events(found: list[Event], where: str, msg: str) -> int | None:
    return _service_deletions.delete_events(
        found,
        where,
        msg,
        Event=Event,
        mark_deleted=mark_deleted,
        pop_undo=pop_undo,
        state=state,
    )


def finish_deletions():
    return _service_deletions.finish_deletions(
        rebuild=rebuild, source_ids=source_ids, store=store
    )


def keep_removed(sid: str, previous: list[Event], events: list[Event]):
    return _service_deletions.keep_removed(
        sid,
        previous,
        events,
        Event=Event,
        TZ=TZ,
        calendar_name=calendar_name,
        now=now,
        pop_undo=pop_undo,
        publish=publish,
        skey=skey,
        state=state,
        store=store,
    )


def rebuild(sid: str | None = None):
    return _service_publishing.rebuild(
        sid, publish=publish, skey=skey, source_ids=source_ids, store=store
    )


def preview(sid: str, body: bytes) -> tuple[list[Event], str]:
    return _service_publishing.preview(
        sid, body, Event=Event, source_events=source_events
    )


def _event_time(e: Event, d: i18n.Dates, lang: str = "en") -> str:
    return _service_event_history._event_time(e, d, lang, Event=Event, i18n=i18n)


def record_changes(sid: str, old: list[Event], new: list[Event]) -> int:
    return _service_event_history.record_changes(
        sid,
        old,
        new,
        Event=Event,
        TZ=TZ,
        _event_time=_event_time,
        calendar_name=calendar_name,
        dates_for=dates_for,
        i18n=i18n,
        now=now,
        ruleset=ruleset,
        skey=skey,
        st=st,
        store=store,
    )


def add_change_notes(events: list[Event], sid: str):
    return _service_event_history.add_change_notes(
        events, sid, Event=Event, skey=skey, store=store
    )


def apply_calendar(body: bytes, how: str, sid: str = "ccs") -> bool:
    return _service_publishing.apply_calendar(
        body,
        how,
        sid,
        keep_removed=keep_removed,
        now=now,
        preview=preview,
        publish=publish,
        record_changes=record_changes,
        skey=skey,
        st=st,
        store=store,
    )


async def run_once(manual: bool = False, sid: str = "ccs"):
    return await _service_source_jobs.run_once(
        manual,
        sid,
        AuthError=AuthError,
        BlockedError=BlockedError,
        MAX_AUTH_FAILURES=MAX_AUTH_FAILURES,
        SourceError=SourceError,
        apply_calendar=apply_calendar,
        calendar_url=calendar_url,
        download=download,
        logins=logins,
        now=now,
        run_feed=run_feed,
        source_ids=source_ids,
        state=state,
        store=store,
    )


async def run_feed(sid: str):
    return await _service_source_jobs.run_feed(
        sid,
        AuthError=AuthError,
        BlockedError=BlockedError,
        SourceError=SourceError,
        apply_calendar=apply_calendar,
        download=download,
        now=now,
        skey=skey,
        source_ids=source_ids,
        source_url=source_url,
        st=st,
        store=store,
    )


MIN_INTERVAL, MAX_INTERVAL = 15, 24 * 60  # minutes between automatic downloads


def interval_minutes(sid: str = "ccs") -> int:
    return _service_source_jobs.interval_minutes(
        sid,
        MAX_INTERVAL=MAX_INTERVAL,
        MIN_INTERVAL=MIN_INTERVAL,
        settings=settings,
        skey=skey,
        store=store,
    )


async def loop(sid: str = "ccs"):
    return await _service_source_jobs.loop(
        sid,
        interval_minutes=interval_minutes,
        log=log,
        now=now,
        run_once=run_once,
        st=st,
    )


source_tasks: dict[str, asyncio.Task] = {}


def start_source(sid: str):
    return _service_source_jobs.start_source(
        sid, loop=loop, source=source, source_tasks=source_tasks
    )


def stop_source(sid: str):
    return _service_source_jobs.stop_source(sid, source_tasks=source_tasks)


_background: set[asyncio.Task] = set()


def background(coro):
    return _service_source_jobs.background(coro, _background=_background)


def mark_updating(target: str):
    return _service_update_jobs.mark_updating(
        target, __version__=__version__, store=store
    )


def updating_to() -> str:
    return _service_update_jobs.updating_to(__version__=__version__, store=store)


def auto_update() -> bool:
    return _service_update_jobs.auto_update(store=store)


async def update_loop():
    return await _service_update_jobs.update_loop(
        auto_install=auto_install,
        auto_update=auto_update,
        log=log,
        state=state,
        store=store,
        updater=updater,
        updates=updates,
    )


async def auto_install():
    return await _service_update_jobs.auto_install(
        UpdaterError=UpdaterError,
        auto_update=auto_update,
        mark_updating=mark_updating,
        state=state,
        store=store,
        updater=updater,
        updates=updates,
    )


async def updater_loop():
    return await _service_update_jobs.updater_loop(log=log, updater=updater)


def lifespan(_app):
    return _service_lifecycle.lifespan(
        _app,
        ensure_local=ensure_local,
        google_loop=google_loop,
        import_public_url=import_public_url,
        log=log,
        logins=logins,
        migrate_destinations=migrate_destinations,
        migrate_links=migrate_links,
        migrate_rules=migrate_rules,
        migrate_sources=migrate_sources,
        rebuild=rebuild,
        settings=settings,
        share_converted_rules=share_converted_rules,
        source_ids=source_ids,
        source_tasks=source_tasks,
        start_source=start_source,
        state=state,
        store=store,
        tail_logs=tail_logs,
        update_loop=update_loop,
        updater_loop=updater_loop,
    )


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, version=__version__)


@app.middleware("http")
async def protect(request: Request, call_next):
    return await _service_http.protect(
        request, call_next, __version__=__version__, app=app
    )


templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
# Material Symbols for every page: {{ icon_sprite() }} once at the top of <body>, then {{ icon("delete") }}
# draws one; icon_mask("check") is for stylesheets.
templates.env.globals.update(
    icon=icons.svg, icon_mask=icons.mask, icon_sprite=icons.sprite
)
# The fonts (IBM Plex Sans and Mono): served from here, so pages never load anything from elsewhere.
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return await _service_http.http_error(
        request,
        exc,
        _is_async=_is_async,
        app=app,
        i18n=i18n,
        lang_for=lang_for,
        page=page,
    )


def _is_async(request: Request) -> bool:
    return _service_http._is_async(request)


basic = HTTPBasic(auto_error=False)


# --- Status-page login -------------------------------------------------------

GUI_MAX_FAILURES, GUI_LOCKOUT = 5, timedelta(minutes=15)
_gui_failures: dict[str, list] = {}  # client ip -> [failure count, locked-until]
_global_failures: list[datetime] = []  # every recent failure, from any address
GLOBAL_MAX_FAILURES = (
    50  # in GUI_LOCKOUT, from all addresses together: then everyone waits…
)
_good_ips: dict[str, datetime] = (
    {}
)  # …except addresses that logged in successfully within GOOD_IP_FOR
GOOD_IP_FOR = timedelta(days=7)
_failures_lock = threading.Lock()  # gui_auth runs in worker threads


def _client_ip(request: Request) -> str:
    return _service_authentication._client_ip(request)


_LOCAL_NETS = [
    ipaddress.ip_network(n)
    for n in (
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "127.0.0.0/8",
        "169.254.0.0/16",
        "::1/128",
        "fc00::/7",
        "fe80::/10",
    )
]
_domain_ips: dict = {
    "at": None,
    "ips": set(),
}  # the public addresses' own IPs, looked up at most every 10 minutes


def _own_network(ip: str) -> bool:
    return _service_authentication._own_network(
        ip,
        _LOCAL_NETS=_LOCAL_NETS,
        _domain_ips=_domain_ips,
        now=now,
        public_addresses=public_addresses,
    )


# (0.2.8-beta.19, F6) Two ways back in when the limit for all addresses trips, so it can't lock the owner out of a
# remote server: (a) a browser that has signed in here before carries a signed "known browser" cookie, which gets
# past that limit from anywhere (the limit for its own address still applies, and it still needs the password);
# (b) the moment the limit trips, the container log gets a one-time link, good for an hour, that makes the
# browser opening it a known browser.
KNOWN_COOKIE = "cs_known"
KNOWN_DAYS = 400  # the longest browsers keep a cookie
UNLOCK_FOR = timedelta(hours=1)
_unlock: dict = {"token": None, "until": None}


def _known_sig(issued: int) -> str:
    return _service_authentication._known_sig(issued, _session_key=_session_key)


def known_browser(request: Request) -> bool:
    return _service_authentication.known_browser(
        request,
        KNOWN_COOKIE=KNOWN_COOKIE,
        KNOWN_DAYS=KNOWN_DAYS,
        _known_sig=_known_sig,
        now=now,
    )


def _new_unlock() -> str:
    return _service_authentication._new_unlock(
        UNLOCK_FOR=UNLOCK_FOR,
        _unlock=_unlock,
        now=now,
        public_addresses=public_addresses,
    )


def _check_lockout(ip: str, known: bool = False):
    return _service_authentication._check_lockout(
        ip,
        known,
        GLOBAL_MAX_FAILURES=GLOBAL_MAX_FAILURES,
        GOOD_IP_FOR=GOOD_IP_FOR,
        GUI_LOCKOUT=GUI_LOCKOUT,
        _failures_lock=_failures_lock,
        _global_failures=_global_failures,
        _good_ips=_good_ips,
        _gui_failures=_gui_failures,
        _own_network=_own_network,
        now=now,
    )


def _count_failure(ip: str, what: str = "logins"):
    return _service_authentication._count_failure(
        ip,
        what,
        GLOBAL_MAX_FAILURES=GLOBAL_MAX_FAILURES,
        GUI_LOCKOUT=GUI_LOCKOUT,
        GUI_MAX_FAILURES=GUI_MAX_FAILURES,
        _failures_lock=_failures_lock,
        _global_failures=_global_failures,
        _gui_failures=_gui_failures,
        _new_unlock=_new_unlock,
        log=log,
        now=now,
        state=state,
    )


def _count_success(ip: str):
    return _service_authentication._count_success(
        ip,
        _failures_lock=_failures_lock,
        _good_ips=_good_ips,
        _gui_failures=_gui_failures,
        now=now,
    )


# --- Signing in (0.2.8-beta.15: the page's own sign-in page, not the browser's pop-up) ------------------
# A signed session cookie: the user, when it ends, and a signature that also covers the password's hash,
# so changing the login signs every browser out. HTTP Basic is still accepted from scripts and tools
# that send it; a page asked for without either goes to /login.

SESSION_COOKIE = "cs_session"


def _session_key() -> bytes:
    return _service_authentication._session_key(store=store)


def _session_sig(user: str, until: int) -> str:
    return _service_authentication._session_sig(
        user, until, _session_key=_session_key, logins=logins
    )


def session_user(request: Request) -> str:
    return _service_authentication.session_user(
        request,
        SESSION_COOKIE=SESSION_COOKIE,
        _session_sig=_session_sig,
        logins=logins,
        now=now,
    )


def gui_auth(request: Request, creds: HTTPBasicCredentials | None = Depends(basic)):
    return _service_authentication.gui_auth(
        request,
        creds,
        _check_lockout=_check_lockout,
        _client_ip=_client_ip,
        _count_failure=_count_failure,
        _count_success=_count_success,
        _is_async=_is_async,
        basic=basic,
        known_browser=known_browser,
        logins=logins,
        session_user=session_user,
    )


def check_csrf(token: str, expected: str | None = None):
    return _service_authentication.check_csrf(token, expected, CSRF_TOKEN=CSRF_TOKEN)


def renew_csrf():
    """A new form token, e.g. after the login changed, so a token seen before (such as on the
    first-visit page) can't be used against the new login."""
    global CSRF_TOKEN
    CSRF_TOKEN = _service_authentication.new_csrf_token()


# --- Links ---------------------------------------------------------------------


def public_url() -> str:
    return _service_addresses.public_url(
        normalise_public_url=normalise_public_url, store=store
    )


def import_public_url():
    return _service_addresses.import_public_url(
        settings=settings, state=state, store=store
    )


def base_url(request: Request) -> str:
    return _service_addresses.base_url(request, public_url=public_url)


def public_addresses() -> list[str]:
    return _service_addresses.public_addresses(public_url=public_url, store=store)


def feed_url(request: Request, token: str, base: str = "") -> str:
    return _service_addresses.feed_url(request, token, base, base_url=base_url)


def subscribe_links(
    request: Request, token: str, base: str = "", name: str = ""
) -> dict:
    return _service_addresses.subscribe_links(
        request, token, base, name, base_url=base_url, feed_url=feed_url
    )


def google_redirect_uri(request: Request) -> str:
    return _service_addresses.google_redirect_uri(request, base_url=base_url)


def _local_time(value: str | None, lang: str = "en") -> str:
    return _service_google_view._local_time(
        value, lang, TZ=TZ, dates_for=dates_for, now=now
    )


def _watch_view(lang: str) -> dict:
    return _service_google_view._watch_view(
        lang,
        _local_time=_local_time,
        destinations=destinations,
        google=google,
        notify_address=notify_address,
    )


def _host_mismatch(request: Request) -> tuple[str, str] | None:
    return _service_google_view._host_mismatch(
        request, _is_ip=_is_ip, public_url=public_url
    )


def _is_ip(host: str) -> bool:
    return _service_google_view._is_ip(host)


def google_view(request: Request, lang: str = "en") -> dict:
    return _service_google_view.google_view(
        request,
        lang,
        _host_mismatch=_host_mismatch,
        _is_ip=_is_ip,
        _local_time=_local_time,
        _watch_view=_watch_view,
        admin_email=admin_email,
        dest_google=dest_google,
        destinations=destinations,
        google=google,
        google_job=google_job,
        google_redirect_uri=google_redirect_uri,
    )


# --- Month view ----------------------------------------------------------------


def _span(
    e: Event, tz: ZoneInfo | None = None
) -> tuple[date, date, datetime | None, datetime | None]:
    return _service_calendar_view._span(e, tz, Event=Event, display_tz=display_tz)


def _hidden_by(e: Event, hide: set[str]) -> bool:
    return _service_calendar_view._hidden_by(e, hide, Event=Event)


from .calendars.view_helpers import _lanes


def cal_view(
    events: list[Event],
    view: str,
    ref: date,
    lang: str = "en",
    pad: int = 0,
    hide: set[str] | None = None,
) -> dict:
    return _service_calendar_view.cal_view(
        events,
        view,
        ref,
        lang,
        pad,
        hide,
        DEFAULT_COLOR=DEFAULT_COLOR,
        Event=Event,
        _hidden_by=_hidden_by,
        _lanes=_lanes,
        _range_text=_range_text,
        _span=_span,
        calendar_color=calendar_color,
        dates_for=dates_for,
        display_tz=display_tz,
        i18n=i18n,
        now=now,
        source_ids=source_ids,
    )


def month_view(events: list[Event], year: int, month: int, lang: str = "en") -> dict:
    return _service_calendar_view.month_view(
        events, year, month, lang, Event=Event, cal_view=cal_view
    )


def _range_text(e: Event, s, t, lang: str = "en") -> str:
    return _service_calendar_view._range_text(
        e, s, t, lang, Event=Event, dates_for=dates_for, i18n=i18n
    )


def _parse_month(value: str | None) -> tuple[int, int]:
    return _service_calendar_view._parse_month(value, now=now)


from .calendars.view_helpers import _opt_day

# --- Helpers the routes of more than one area use (app/routes/) ------------------------------------


def _sid(sid: str) -> str:
    return _service_route_helpers._sid(sid, source_ids=source_ids)


# Calendar Sources → + offers these presets. Google and Apple calendars are calendar feeds (their
# private iCal links), with their own step-by-step help; "other" is any .ics / webcal:// link.
SOURCE_PRESETS = {
    "google": "Google Calendar",
    "apple": "Apple Calendar",
    "other": "Calendar feed",
}


from .item_order import _moved


from .services.field_error import FieldError


def api_on() -> bool:
    return _service_route_helpers.api_on(google=google)


def _did(did: str) -> dict:
    return _service_route_helpers._did(did, destination=destination)


async def sent_fields(request: Request, *names: str) -> list[str | None]:
    return await _service_route_helpers.sent_fields(request, *names)


GOOGLE_SETTINGS = "/?menu=settings#googlesync"  # Google Calendar sync is in ☰ Settings (0.2.8-beta.4)


def show_duration(minutes: int) -> str:
    return _service_route_helpers.show_duration(minutes)


def ignored_conflicts() -> list[str]:
    return _service_route_helpers.ignored_conflicts(store=store)


def united_original(uid: str, sid: str = "ccs") -> Event | None:
    return _service_route_helpers.united_original(
        uid, sid, Event=Event, preview=preview, skey=skey, store=store
    )


EVENT_COLORS = {hex_ for _, hex_ in GOOGLE_COLORS.values()}  # Google's 11 event colors

# Icons for the event tools (Material Symbols): a bin to delete, two sheets to duplicate.
TRASH_ICON = icons.svg("delete", 17, "trashmark")
COPY_ICON = icons.svg("content_copy", 17)


ALARM_CHOICES = (
    0,
    5,
    10,
    15,
    30,
    60,
    120,
    1440,
    2880,
    10080,
)  # minutes before the start


def alarm_text(minutes: int, lang: str = "en") -> str:
    return _service_route_helpers.alarm_text(minutes, lang, i18n=i18n)


# --- Admin e-mail (Settings) -------------------------------------------------------

EMAIL_RE = re.compile(r"^[^@\s<>\"']{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")


def admin_email() -> str:
    return _service_administrator.admin_email(EMAIL_RE=EMAIL_RE, store=store)


# --- Invite someone (0.2.8-beta.17, F1) -------------------------------------------------------
# A Google module can go to someone else's Google Calendar without their password: an invite is a one-time
# link (7 days) to a page where they sign in to Google themselves; the module's calendar is then made in
# their account. The page needs no login: the unguessable, single-use link is the permission, and the only
# thing it can do is sign that one module's account in. kv "google_invites": token -> {did, account, expires}.
# Its pages: app/routes/google.py.

INVITE_DAYS = 7


def _invites() -> dict:
    return _service_invites._invites(now=now, store=store)


def make_invite(d: dict, account: str | None = None) -> str:
    return _service_invites.make_invite(
        d,
        account,
        INVITE_DAYS=INVITE_DAYS,
        _invites=_invites,
        now=now,
        state=state,
        store=store,
    )


def forget_invites(did: str):
    return _service_invites.forget_invites(did, _invites=_invites, store=store)


# --- The routes, by area (0.2.8-beta.20, F12): app/routes/<area>.py ---------------------------------
# Registered last, in the original matching order, with explicit services and late-bound value providers.
# Route modules never import this composition root. AGENTS.md has the map.


from .routes import register_routes

register_routes(
    ALARM_CHOICES=ALARM_CHOICES,
    ALL_ZONES=ALL_ZONES,
    CLOCKS=CLOCKS,
    COLOR_RE=COLOR_RE,
    COMMON_ZONES=COMMON_ZONES,
    COPY_ICON=COPY_ICON,
    Change=Change,
    DELETED_WHERE=DELETED_WHERE,
    DESTINATION_TYPES=DESTINATION_TYPES,
    EARLIEST=EARLIEST,
    EMAIL_RE=EMAIL_RE,
    EVENT_COLORS=EVENT_COLORS,
    FieldError=FieldError,
    GOOGLE_SETTINGS=GOOGLE_SETTINGS,
    KNOWN_COOKIE=KNOWN_COOKIE,
    KNOWN_DAYS=KNOWN_DAYS,
    LOG_KINDS=LOG_KINDS,
    LOG_TAIL=LOG_TAIL,
    MAX_INTERVAL=MAX_INTERVAL,
    MAX_TEMPLATES=MAX_TEMPLATES,
    MIN_INTERVAL=MIN_INTERVAL,
    MODULE_ABOUT=MODULE_ABOUT,
    RULES_PARSE=RULES_PARSE,
    SECTIONS=SECTIONS,
    SESSION_COOKIE=SESSION_COOKIE,
    SOURCE_BASES=SOURCE_BASES,
    SOURCE_PRESETS=SOURCE_PRESETS,
    State=State,
    THEMES=THEMES,
    TRASH_ICON=TRASH_ICON,
    TZ=TZ,
    UNDO_KEEP=UNDO_KEEP,
    WELCOME_TOKEN=WELCOME_TOKEN,
    _FIELDS=_FIELDS,
    _check_lockout=_check_lockout,
    _count_failure=_count_failure,
    _count_success=_count_success,
    _did=_did,
    _hidden_by=_hidden_by,
    _invites=_invites,
    _is_async=_is_async,
    _iso_day=_iso_day,
    _known_sig=_known_sig,
    _local_time=_local_time,
    _moved=_moved,
    _opt_day=_opt_day,
    _parse_month=_parse_month,
    _range_text=_range_text,
    _remember_calendar=_remember_calendar,
    _remembered_calendar=_remembered_calendar,
    _session_key=_session_key,
    _session_sig=_session_sig,
    _shared_grant=_shared_grant,
    _sid=_sid,
    _span=_span,
    _unlock=_unlock,
    admin_email=admin_email,
    after_restore=after_restore,
    alarm_text=alarm_text,
    all_rules=all_rules,
    app=app,
    apply_calendar=apply_calendar,
    auto_update=auto_update,
    background=background,
    base_url=base_url,
    basic=basic,
    cal_view=cal_view,
    calendar_color=calendar_color,
    calendar_name=calendar_name,
    check_csrf=check_csrf,
    customs_for=customs_for,
    dates_for=dates_for,
    default_sid=default_sid,
    delete_events=delete_events,
    dest_events=dest_events,
    dest_google=dest_google,
    destination=destination,
    destinations=destinations,
    display_tz=display_tz,
    display_zone=display_zone,
    ensure_local=ensure_local,
    event_alarms=event_alarms,
    event_links=event_links,
    event_templates=event_templates,
    feed_url=feed_url,
    first_named_calendar=first_named_calendar,
    forget_invites=forget_invites,
    google=google,
    google_accounts=google_accounts,
    google_for=google_for,
    google_job=google_job,
    google_redirect_uri=google_redirect_uri,
    google_traffic=google_traffic,
    google_view=google_view,
    gui_auth=gui_auth,
    ignored_conflicts=ignored_conflicts,
    interval_minutes=interval_minutes,
    is_local=is_local,
    known_browser=known_browser,
    lang_for=lang_for,
    last_local=last_local,
    log=log,
    logins=logins,
    make_invite=make_invite,
    mark_deleted=mark_deleted,
    mark_updating=mark_updating,
    new_did=new_did,
    new_local=new_local,
    notify_address=notify_address,
    now=now,
    page=page,
    pop_undo=pop_undo,
    public_addresses=public_addresses,
    public_url=public_url,
    rebuild=rebuild,
    renew_csrf=renew_csrf,
    request_google_sync=request_google_sync,
    rule_label=rule_label,
    rule_label_html=rule_label_html,
    rule_used=rule_used,
    save_destinations=save_destinations,
    save_rules=save_rules,
    section_state=section_state,
    sent_fields=sent_fields,
    session_user=session_user,
    set_event_links=set_event_links,
    show_duration=show_duration,
    skey=skey,
    source=source,
    source_ids=source_ids,
    source_off=source_off,
    source_rules=source_rules,
    source_url=source_url,
    sources=sources,
    st=st,
    start_source=start_source,
    state=state,
    states=states,
    stop_source=stop_source,
    store=store,
    subscribe_links=subscribe_links,
    templates=templates,
    undo_keep=undo_keep,
    united_original=united_original,
    unmark_deleted=unmark_deleted,
    updater=updater,
    updates=updates,
    valid_zone=valid_zone,
    get_CSRF_TOKEN=lambda: CSRF_TOKEN,
    get___version__=lambda: __version__,
    get__client_ip=lambda: _client_ip,
    get__hide=lambda: _hide,
    get_api_on=lambda: api_on,
    get_cal_view=lambda: cal_view,
    get_google_health=lambda: google_health,
    get_request_google_sync=lambda: request_google_sync,
    get_run_once=lambda: run_once,
    get_updating_to=lambda: updating_to,
)


# Read from main by the tests (and anything written before the split).
from .routes.account import LOGIN_TOKEN, _safe_next  # noqa: E402,F401
from .routes.events import _form_values  # noqa: E402,F401
from .routes.page import print_prefs, ui_view  # noqa: E402,F401
from .routes.rules import parse_duration  # noqa: E402,F401
