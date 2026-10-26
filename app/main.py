"""Web app: status page, month view, .ics feed, and the background loops (CCS+ downloads,
Google sync, update checks)."""
from __future__ import annotations

import asyncio
import gzip
import hashlib
import calendar as pycal
import json
import os
import logging
import platform
import re
import secrets
import threading
from contextlib import asynccontextmanager
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from itertools import zip_longest
from pathlib import Path
from urllib.parse import quote, urlparse
from zoneinfo import ZoneInfo, available_timezones

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.exception_handlers import http_exception_handler as default_http_error
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from markupsafe import Markup, escape
from fastapi.templating import Jinja2Templates

from . import __version__, i18n, icons
from . import links as links_mod
from . import rules as rules_mod
from .calsync import (AuthError, BlockedError, Defaults, Event, SourceError, apply_changes, build_feed,
                      check_calendar, download, parse, parse_feed)
from .config import DEFAULT_CALENDAR_URL, normalise_public_url, settings
from .gsync import GOOGLE_COLORS, Google, GoogleError, nearest_color_id
from .logins import LoginError, Logins
from .secretbox import SecretBox
from .store import Store, from_iso, iso
from .updates import FREQUENCIES, RELEASES, Updater, UpdaterError, Updates, channel as release_channel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("calendar_stream")
logging.getLogger("httpx").setLevel(logging.WARNING)   # one line per Google request is too chatty
TZ = ZoneInfo(settings.timezone)
store = Store(settings.dsn)
box = SecretBox(settings.db_password)
google = Google(store, box, settings.timezone)
logins = Logins(store, box)
updates = Updates(store)
updater = Updater()     # the optional updater container behind "Update now"
MAX_AUTH_FAILURES = 2   # pause automatic downloads after this many rejected sign-ins (avoids account lockout)
CSRF_TOKEN = secrets.token_urlsafe(24)     # forms on the status page must carry this; renewed when the login changes
WELCOME_TOKEN = secrets.token_urlsafe(24)  # the first-visit page's own token (shown before any login exists)


def now():
    return datetime.now(TZ)


# --- Calendar sources and destinations ------------------------------------------------
#
# A source is where events come from: United's CCS+ Calendar Sync (ID "ccs", at most one), any .ics
# feed link (type "ics", IDs such as "f3a9c1"), or a local calendar (0.2.8: type "local", IDs such as
# "l3a9c1"), which only holds events added here. The first source is the default calendar: events
# added here go to it unless another is chosen. Each source has its own name, color (the
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
    """The database key of one of a source's settings."""
    return base if sid == "ccs" else f"{base}:{sid}"


def sources() -> list[dict]:
    """The calendar sources, in their order on the page (the first is the default calendar):
    [{"id", "type", "url"?}, …]."""
    return [x for x in (store.get("sources") or []) if isinstance(x, dict) and SID_RE.match(str(x.get("id", "")))]


def source(sid: str) -> dict | None:
    return next((x for x in sources() if x["id"] == sid), None)


def source_ids() -> list[str]:
    return [x["id"] for x in sources()]


def destinations(kind: str | None = None) -> list[dict]:
    """The destinations (or those of one type), in the order they were added. Sources that were
    removed are left out of their lists."""
    ids = source_ids()
    found = []
    for d in store.get("destinations") or []:
        if not isinstance(d, dict) or not DID_RE.match(str(d.get("id", ""))) or d.get("type") not in DESTINATION_TYPES:
            continue
        if kind and d["type"] != kind:
            continue
        found.append({"id": d["id"], "type": d["type"], "name": " ".join(str(d.get("name") or "").split())[:100] or "CalendarStream",
                      "sources": [x for x in d.get("sources") or [] if x in ids], "token": str(d.get("token") or ""),
                      "start": _iso_day(d.get("start")), "end": _iso_day(d.get("end")),
                      # a feed made by + Google Calendar while Google Calendar sync wasn't set up (0.2.8-beta.4)
                      "for": "google" if d["type"] == "feed" and d.get("for") == "google" else ""})
    return found


def _iso_day(value) -> str:
    """A date as YYYY-MM-DD, or "" (no limit)."""
    try:
        return date.fromisoformat(str(value or "")).isoformat()
    except ValueError:
        return ""


def destination(did: str) -> dict | None:
    return next((d for d in destinations() if d["id"] == did), None)


def save_destinations(found: list[dict]):
    store.set("destinations", [{k: d.get(k, "") for k in ("id", "type", "name", "sources", "token", "start", "end", "for")} for d in found])


def new_did() -> str:
    taken = {d["id"] for d in destinations()}
    while (did := "d" + secrets.token_hex(3)) in taken:
        pass
    return did


def migrate_sources():
    """0.2 added sources and destinations. An install from before keeps what it had: CCS+ as its source,
    and the feed (its links may be in use) plus Google Autosync if it was set up. A new install starts empty."""
    if store.get("sources") is not None:
        return
    had = logins.ccs_configured or store.get_calendar("source") is not None or store.event_count() > 0
    store.set("sources", [{"id": "ccs", "type": "ccs"}] if had else [])
    store.set("destinations", (["feed"] if had else []) + (["google"] if google.configured else []))


def migrate_destinations():
    """0.2.0 kept destinations as two switches ("feed", "google") with a feed link and a Google
    calendar for each source. Each becomes a destination of its own with that one source, keeping
    its stream name (so existing links work) and its Google calendar."""
    raw = store.get("destinations") or []
    if not any(isinstance(d, str) for d in raw):
        return
    ids = source_ids()
    found = [d for d in destinations()]
    if "feed" in raw:
        for sid in ids:
            did = new_did()
            token = settings.feed_token if sid == "ccs" else (store.get(f"feed_token:{sid}") or secrets.token_urlsafe(24))
            found.append({"id": did, "type": "feed", "name": calendar_name(sid), "sources": [sid], "token": token})
            reads = store.get(skey(sid, "feed_reads"))
            if reads:
                store.set(f"feed_reads:{did}", reads)
            save_destinations(found)
    if "google" in raw:
        keys = [k for k in google.calendar_sids() if k in ids]
        for k in keys:
            did = new_did()
            google.rekey(k, did)
            found.append({"id": did, "type": "google", "name": google.cal_info(did).get("calendar_name") or calendar_name(k),
                          "sources": [k], "token": ""})
            save_destinations(found)
        if not keys:     # Autosync was set up but had no calendar yet
            found.append({"id": new_did(), "type": "google", "name": calendar_name(ids[0]) if ids else "CalendarStream",
                          "sources": ids[:1], "token": ""})
    save_destinations(found)


def calendar_url() -> str:
    """The CCS+ Calendar Sync link."""
    return store.get("calendar_url") or settings.calendar_url


def source_url(sid: str) -> str:
    return calendar_url() if sid == "ccs" else str((source(sid) or {}).get("url", ""))


def calendar_name(sid: str = "ccs") -> str:
    """A source's name, set on the status page; for CCS+ else CALENDAR_NAME from .env."""
    saved = store.get(skey(sid, "calendar_name"))
    if saved:
        return saved
    if sid == "ccs":
        return settings.calendar_name
    return urlparse(source_url(sid)).hostname or "Calendar"


COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
DEFAULT_COLOR = "#1d4ed8"   # a calendar's events on this page until a color is chosen (its module's color box)


def calendar_color(sid: str = "ccs") -> str:
    """A source's color (#rrggbb), or "" for none. Validated again on the way out because it is
    written into the page's CSS."""
    color = store.get(skey(sid, "calendar_color")) or ""
    return color.lower() if COLOR_RE.match(color) else ""


MAX_TAGS, MAX_TAG_LEN = 30, 40

# Rules (app/rules.py, 0.2.8): one ordered list in kv "rules" ("If … Then …"; the order is the priority),
# each saying which calendars it applies to. Events are read with RULES_PARSE: an event with no end
# time keeps its start as its end (and no_end set), and 24-hour events keep their times, so the
# rules ("Items without an end time", "24-hour events") decide what becomes of them.
RULES_PARSE = Defaults(mode="rules", allday_24h=False)
RULE_WHEN = rules_mod.WHEN


def all_rules() -> list[dict]:
    """Every rule, highest priority first."""
    return rules_mod.normalize_all(store.get("rules"), source_ids())


def save_rules(found: list[dict]):
    store.set("rules", found[:rules_mod.MAX_RULES])


def source_rules(sid: str) -> list[dict]:
    """The rules a calendar uses, highest priority first."""
    return rules_mod.for_source(all_rules(), sid)


def ruleset(sid: str) -> rules_mod.Ruleset:
    """A calendar's rules, ready to apply to its events. An event with no end time that no rule
    changes gets DEFAULT_EVENT_TYPE / DEFAULT_EVENT_HOURS from .env."""
    return rules_mod.Ruleset(source_rules(sid), TZ, {t["id"]: t for t in event_templates()},
                             (settings.default_event_type, settings.default_event_hours))


def color_name(color: str) -> str:
    return GOOGLE_COLORS[nearest_color_id(color)][0]


def rule_label(r: dict, lang: str = "en") -> str:
    """A rule in one line: its title, else e.g. 'Text contains “RDO” → Color (Tomato)'."""
    tr = lambda text, **kw: str(i18n.tr(lang, text, **kw))
    return rules_mod.label(r, tr, color_name, {t["id"]: t for t in event_templates()})


def _swatch(color: str) -> str:
    return f'<span class="swatch" style="--c:{escape(color)}" aria-hidden="true"></span>'


def rule_label_html(r: dict, lang: str = "en") -> Markup:
    """The rule's line on the page (0.2.8-beta.5): each color's swatch right after the word Color, its
    name in brackets ("Color ■ (Tomato)"); a rule with a title has its first color's swatch before it."""
    text = rule_label(r, lang)
    colors = [a["color"] for a in r["actions"] if a["type"] == "color"]
    if r["title"]:
        return Markup((_swatch(colors[0]) + " " if colors else "") + str(escape(text)))
    html = str(escape(text))
    word = str(escape(str(i18n.tr(lang, "Color"))))
    for c in dict.fromkeys(colors):
        piece = str(escape(f"({color_name(c)})"))
        html = html.replace(f"{word} {piece}", f"{word} {_swatch(c)} {piece}", 1)
    return Markup(html)


def migrate_rules():
    """0.2.8: the rules become one list of "If … Then …" rules (app/rules.py). The rules of 0.2.6–0.2.8-beta.1
    (and, through them, those of 0.2.5 and before) are converted; a new install starts with the two
    predefined ones (items without an end time, 24-hour events), for every calendar."""
    if store.get("rules") is not None:
        return
    if store.get("rules_v3") or store.get("rule_templates") is not None or any(
            store.get(skey(sid, "calendar_tags")) for sid in source_ids()):
        _migrate_rules_v3()
        lib = _v3_rules(store.get("rule_templates") or [])
        subs = {sid: list(store.get(skey(sid, "rule_subs")) or []) for sid in source_ids()}
        save_rules(rules_mod.from_v3(lib, subs, source_ids()))
    else:
        save_rules(rules_mod.starters(settings.default_event_type, settings.default_event_hours, settings.allday_24h))


def share_converted_rules():
    """0.2.8-beta.3, once: rules converted in beta.2 that every calendar used were kept for those
    calendars only, so the Local calendar made after them (and calendars added later) didn't get
    them. A rule for every calendar but the Local ones becomes a rule for All calendars."""
    if store.get("rules_shared_b3") or store.get("rules") is None:
        return
    others = {x["id"] for x in sources() if x.get("type") != "local"}
    found = all_rules()
    for r in found:
        if r["apply"] != "all" and others and set(r["apply"]) == others:
            r["apply"] = "all"
    save_rules(found)
    store.set("rules_shared_b3", True)


def first_named_calendar() -> str:
    """A new feed's name when none is given: the first calendar that comes from somewhere (not a Local
    one, which would name every feed "Local")."""
    named = [x["id"] for x in sources() if x.get("type") != "local"]
    return calendar_name(named[0]) if named else "CalendarStream"


def ensure_local():
    """0.2.8: every install gets a local calendar once, at the top (so it's the default calendar for
    events added here), in every feed. Removed later, it isn't made again."""
    if store.get("local_made"):
        return
    sid = new_local()
    store.set("sources", [{"id": sid, "type": "local"}] + sources())
    store.set(f"calendar_name:{sid}", "Local")
    save_destinations([{**d, "sources": [sid] + d["sources"]} for d in destinations()])
    store.set("local_made", True)


def new_local() -> str:
    taken = set(source_ids())
    while (sid := "l" + secrets.token_hex(3)) in taken:
        pass
    return sid


# --- Rules from before 0.2.8, only read to convert them (migrate_rules) ------------------------------
# 0.2.6–0.2.8-beta.1: kv "rule_templates" (the library: one-condition rules of the kinds below, "owner"
# set for a rule local to one source) and each source's "rule_subs" (the ones it uses, in order).
# 0.2.5 and before: each source's own "calendar_tags" and "defaults", converted first (_migrate_rules_v3).

TAG_MODES = {"word": "Whole word", "contains": "Contains", "starts": "Starts with", "exact": "Exact title"}
V3_TYPES = ("color", "event", "changes", "no_end", "allday24")


def _v3_rules(raw: list) -> list[dict]:
    """Rules as 0.2.6–0.2.8-beta.1 saved them, each with every field."""
    found = []
    for i, t in enumerate(raw if isinstance(raw, list) else []):
        if not isinstance(t, dict):
            continue
        kind = t.get("type") or t.get("action") or "color"
        kind = kind if kind in V3_TYPES else "color"
        tag, color = str(t.get("tag", "")).strip()[:MAX_TAG_LEN], str(t.get("color", ""))
        if kind in ("color", "event") and (not tag or (kind == "color" and not COLOR_RE.match(color))):
            continue
        rid = str(t.get("id") or f"r{i}")
        found.append({"id": rid if re.fullmatch(r"[a-z0-9]{1,16}", rid) else f"r{i}", "type": kind, "tag": tag,
                      "color": color.lower() if COLOR_RE.match(color) else "",
                      "mode": t.get("mode") if t.get("mode") in TAG_MODES else "word", "case": bool(t.get("case")),
                      "template": str(t.get("template") or "")[:16],
                      "when": t.get("when") if t.get("when") in RULE_WHEN else "before_start",
                      "offset": rules_mod._int(t.get("offset"), 0, rules_mod.MAX_OFFSET),
                      "no_end_mode": "allday" if t.get("no_end_mode") == "allday" else "hours",
                      "minutes": rules_mod._int(t.get("minutes"), 5, 24 * 60, 60), "allday": bool(t.get("allday", True)),
                      "owner": str(t.get("owner") or "") if re.fullmatch(r"ccs|f[0-9a-f]{6}", str(t.get("owner") or "")) else ""})
    return found


_V3_KEYS = {"color": ("tag", "mode", "case", "color"), "event": ("tag", "mode", "case", "template", "when", "offset"),
            "changes": ("tag", "mode", "case"), "no_end": ("no_end_mode", "minutes"), "allday24": ("allday",)}


def _v3_add(lib: list[dict], rule: dict) -> str:
    """Add a rule to a 0.2.6 library (unless the same one is there); returns its ID."""
    rule = _v3_rules([rule])[0]
    for r in lib:
        if r["type"] == rule["type"] and r["owner"] == rule["owner"] and all(r[k] == rule[k] for k in _V3_KEYS[r["type"]]):
            return r["id"]
    rid, taken = rule["id"], {r["id"] for r in lib}
    while rid in taken:
        rid = "t" + secrets.token_hex(3)
    lib.append({**rule, "id": rid})
    return rid


def _migrate_rules_v3():
    """0.2.6: every rule into the library; a source's own rules (0.2.5 and before), the rule templates it
    ticked and its two built-in settings became the rules it used, in that order."""
    if store.get("rules_v3"):
        return
    lib = _v3_rules(store.get("rule_templates") or [])
    for sid in source_ids():
        own = _v3_rules(store.get(skey(sid, "calendar_tags")) or [])
        subs = [_v3_add(lib, r) for r in own] + [x for x in store.get(skey(sid, "rule_subs")) or []]
        saved = store.get(skey(sid, "defaults")) or {}
        try:
            hours = float(saved.get("hours", settings.default_event_hours))
        except (TypeError, ValueError):
            hours = settings.default_event_hours
        subs.append(_v3_add(lib, {"type": "no_end", "id": "t" + secrets.token_hex(3),
                                  "no_end_mode": saved.get("mode", settings.default_event_type), "minutes": round(hours * 60)}))
        subs.append(_v3_add(lib, {"type": "allday24", "id": "t" + secrets.token_hex(3),
                                  "allday": saved.get("allday_24h", settings.allday_24h)}))
        store.set(skey(sid, "rule_subs"), list(dict.fromkeys(subs)))
        store.delete(skey(sid, "calendar_tags"))
        store.delete(skey(sid, "defaults"))
    store.set("rule_templates", lib)
    store.set("rules_v3", True)


# --- Event templates ------------------------------------------------------------------------
# Ready-made events: used by "Create event" rules, and offered when adding an event by hand.

MAX_TEMPLATES = 30


def event_templates() -> list[dict]:
    """[{"id", "title", "all_day", "minutes", "location", "description", "color"}, …]"""
    found = []
    for t in store.get("event_templates") or []:
        title = " ".join(str(t.get("title", "")).split())[:200]
        tid = str(t.get("id", ""))
        if not title or not re.fullmatch(r"[a-z0-9]{1,16}", tid):
            continue
        try:
            minutes = max(5, min(24 * 60, int(t.get("minutes") or 60)))
        except (TypeError, ValueError):
            minutes = 60
        color = str(t.get("color") or "").lower()
        found.append({"id": tid, "title": title, "all_day": bool(t.get("all_day")), "minutes": minutes,
                      "location": str(t.get("location") or "")[:200], "description": str(t.get("description") or "")[:2000],
                      "color": color if color in EVENT_COLORS else ""})
    return found[:MAX_TEMPLATES]


# Collapsible sections on the status page, and whether each starts open. The open/closed state
# is saved in the database so it's the same in every browser.
SECTIONS = {"status": True, "activity": False, "rules": False, "templates": False}


def section_state() -> dict:
    """Open/closed: the page's sections, and the Configure part of each source's box ("src:<id>")
    and destination's box ("dest:<id>", "dest:google" for the Google account)."""
    saved = store.get("ui_sections") or {}
    found = {k: bool(saved.get(k, default)) for k, default in SECTIONS.items()}
    found.update({k: bool(v) for k, v in saved.items() if k.startswith(("src:", "dest:"))})
    return found


def lang_for(request: Request) -> str:
    """The language chosen in the status page's language menu, else the browser's."""
    return i18n.pick(store.get("ui_lang"), request.headers.get("accept-language", ""))


def page(request: Request, name: str, context: dict, status_code: int = 200, lang: str | None = None):
    """Render a page in the visitor's language. Templates get `_` (translate a page text),
    `msg` (translate a message made in Python), `dates` and the language menu's details."""
    lang = lang or lang_for(request)
    return templates.TemplateResponse(request, name, {
        **context, "lang": lang, "html_lang": i18n.HTML_LANG[lang], "langs": i18n.LANGS,
        "lang_choice": store.get("ui_lang") if store.get("ui_lang") in i18n.LANGS else "auto",
        "_": lambda text, **kw: i18n.tr(lang, text, **kw), "msg": lambda text: i18n.message(lang, text),
        "dates": dates_for(lang), "theme": ui_theme(), "clock": ui_clock(),
        "update": {"available": updates.available(), "channel": release_channel(), "frequency": updates.frequency(),
                   "frequencies": list(FREQUENCIES), "info": updates.info(), "releases": RELEASES,
                   "checked": _local_time(updates.info().get("checked"), lang),
                   "next": _local_time(iso(updates.next_check(datetime.now(timezone.utc))), lang),
                   "updater": updater.ready, "can_update": updater.ready and not updater.pinned(),
                   "auto": auto_update()}, "version": __version__,
    }, status_code=status_code)


THEMES = ("system", "light", "dark")
CLOCKS = ("auto", "12", "24")


def ui_clock() -> str:
    """12-hour (1:00pm) or 24-hour ("military", 13:00) times on the status page, or "auto" (by language)."""
    clock = store.get("ui_clock")
    return clock if clock in CLOCKS else "auto"


# The time zone the status page's calendar is shown in. It only changes how the calendar looks
# here; the feed, Google and the server's own clock (TZ in .env) are unaffected.
ALL_ZONES = sorted(z for z in available_timezones() if "/" in z and not z.startswith(("Etc/", "SystemV/", "posix/", "right/")))
COMMON_ZONES = ["America/New_York", "America/Chicago", "America/Denver", "America/Phoenix", "America/Los_Angeles",
                "America/Anchorage", "Pacific/Honolulu", "Pacific/Guam", "UTC", "Europe/London", "Europe/Frankfurt",
                "Asia/Tokyo", "Asia/Hong_Kong", "Australia/Sydney"]


def valid_zone(name: str) -> bool:
    return name == "UTC" or name in ALL_ZONES


def display_zone() -> str:
    """The calendar's time zone on the status page: chosen above the calendar, else TZ."""
    name = store.get("ui_tz") or ""
    return name if valid_zone(name) else settings.timezone


def display_tz() -> ZoneInfo:
    return ZoneInfo(display_zone())


def dates_for(lang: str) -> i18n.Dates:
    """Day and month names, and times on the chosen clock."""
    return i18n.Dates(lang, {"12": False, "24": True}.get(ui_clock()))


def ui_theme() -> str:
    """Light / dark / system, saved in the database so every browser uses the same choice."""
    theme = store.get("ui_theme")
    return theme if theme in THEMES else "system"


class State:
    """A source's download status (CCS+ or a feed), saved in the database."""
    def __init__(self, sid: str = "ccs"):
        self.sid = sid
        self.status = "starting"   # ok | auth_failed | blocked | error | paused | running | starting
        self.message = ""
        self.last_attempt: datetime | None = None
        self.last_success: datetime | None = None
        self.last_change: datetime | None = None
        self.last_auth: datetime | None = None
        self.last_auth_ok: bool | None = None
        self.next_run: datetime | None = None
        self.login_failures = 0
        self.event_count = 0
        self.last_detail = ""       # what the last download changed: "3 new, 1 removed", "no changes"…
        self.running = False
        self.wake = asyncio.Event()

    def record(self, level: str, msg: str):
        """Add a line to the activity log (a feed source's lines start with its name)."""
        if self.sid != "ccs":
            msg = f"{calendar_name(self.sid)}: {msg}"
        log.log({"warn": logging.WARNING, "error": logging.ERROR}.get(level, logging.INFO), msg)
        try:
            store.add_log(level, msg)
        except Exception as e:
            log.error("Couldn't write activity log to the database: %s", e)

    _TIMES = ("last_attempt", "last_success", "last_change", "last_auth")
    _SAVED = _TIMES + ("status", "message", "last_auth_ok", "login_failures", "event_count", "last_detail")

    def save(self):
        data = {k: getattr(self, k) for k in self._SAVED}
        for k in self._TIMES:
            data[k] = iso(data[k])
        try:
            store.set(skey(self.sid, "status"), data)
        except Exception as e:
            log.error("Couldn't save status to the database: %s", e)

    def load(self):
        data = store.get(skey(self.sid, "status")) or {}
        for k in self._SAVED:
            if k in data:
                v = data[k]
                if k in self._TIMES:
                    v = from_iso(v)
                    v = v.astimezone(TZ) if v else None
                setattr(self, k, v)
        if self.status == "running":   # container stopped mid-run
            self.status = "starting"


states: dict[str, State] = {}


def st(sid: str) -> State:
    """A source's status (loaded from the database the first time)."""
    if sid not in states:
        states[sid] = State(sid)
        if sid != "ccs":
            states[sid].load()
    return states[sid]


state = st("ccs")      # CCS+, and the activity log for everything that isn't a source's


# --- Google Calendar sync --------------------------------------------------------

GOOGLE_FULL_CHECK = timedelta(hours=24)    # how often Google's copy is checked and repaired
GOOGLE_RETRY = timedelta(minutes=15)       # wait after a failed sync before trying again
WATCH_RENEW = timedelta(days=1)            # renew Google's change notifications this long before they end
WATCH_RETRY = timedelta(hours=6)           # after Google refused them, ask again this much later


class GoogleJob:
    """The background Google sync: woken whenever the published schedule changes."""
    def __init__(self):
        self.wake = asyncio.Event()
        self.full = True                   # the first sync after startup checks everything
        self.running = False
        self.lock = asyncio.Lock()         # one sync (or disconnect) at a time


google_job = GoogleJob()


def request_google_sync(full: bool = False):
    google_job.full = google_job.full or full
    google_job.wake.set()


def notify_address() -> str:
    """Where Google sends change notifications, or "" when there's no public https:// address
    (Google only delivers them to https:// with a valid certificate)."""
    base = public_url()
    host = urlparse(base).hostname or ""
    if not base.startswith("https://") or host in ("localhost", "127.0.0.1") or host.endswith(".local"):
        return ""
    return f"{base}/google/notify"


async def ensure_watch(sid: str):
    """Keep Google's change notifications ("webhooks") running for a destination's calendar: start
    them, move them to a new public address, renew them before they run out. If Google refuses,
    Autosync carries on as before (daily check) and asks again later."""
    address = notify_address()
    if not address or not google.connected or not google.watch_due(sid, address, now(), WATCH_RENEW, WATCH_RETRY):
        return
    before = google.watch_info(sid)
    had = bool(before.get("id")) or any(google.watch_info(d["id"]).get("id") for d in destinations("google") if d["id"] != sid)
    try:
        await google.start_watch(sid, address)
        if not had:
            state.record("info", "Google: instant updates turned on (changes made in Google are checked within seconds)")
    except GoogleError as e:
        if str(e) != before.get("error"):     # say so once, not at every retry
            state.record("warn", f"Google: instant updates aren't available ({e}); changes made in Google are checked daily instead")


def dest_events(d: dict) -> list[Event]:
    """A destination's events: those of its sources, within its dates (Start / End; empty = no limit)."""
    def inside(e: Event) -> bool:
        first, last, _, _ = _span(e, TZ)
        return (not d.get("start") or last.isoformat() >= d["start"]) and (not d.get("end") or first.isoformat() <= d["end"])
    return sorted((e for sid in d["sources"] for e in store.load_events(sid) if inside(e)), key=lambda e: e.start)


def event_colorer():
    """A function giving an event's color: its own, else its rules', else its source's ("" for none)."""
    colors = {sid: calendar_color(sid) for sid in source_ids()}
    return lambda e: e.color or e.rule_color or colors.get(e.source, "")


EARLIEST = date(2000, 1, 1)      # a Google destination with no Start date gets every event from here on


def sync_window_start() -> date:
    """Decision 5: events from the first day of the current month onward are synced."""
    return now().date().replace(day=1)


async def google_sync_once(full: bool) -> bool:
    """Run one sync. Returns False if it failed."""
    async with google_job.lock:
        dests = destinations("google")
        if not (google.configured and google.connected and dests):
            return True
        google_job.running = True
        try:
            color_for = event_colorer()
            for d in dests:
                first = date.fromisoformat(d["start"]) if d.get("start") else EARLIEST
                result = await google.sync(d["id"], dest_events(d), d["name"], color_for, first, full)
                if result.changed or result.notes:
                    who = "Google" if len(dests) == 1 else f"Google, {d['name']}"
                    state.record("info", f"{who}: {result.summary()}"
                                 + ("; " + "; ".join(result.notes) if result.notes else ""))
                await ensure_watch(d["id"])
            return True
        except GoogleError as e:
            message = str(e)
        except Exception as e:      # keep the loop alive whatever happens
            message = f"Google sync failed: {type(e).__name__}: {e}"
        finally:
            google_job.running = False
        if message != google.info().get("last_error"):   # log each new problem once
            state.record("error", f"Google: {message}")
        google.record_error(message)
        return False


async def google_loop():
    next_full = now()
    while True:
        google_job.wake.clear()
        full = google_job.full or now() >= next_full
        google_job.full = False
        try:
            ok = await google_sync_once(full)
        except Exception as e:      # e.g. the database restarting: keep the loop alive, retry later
            log.error("Google sync failed: %s", e)
            ok = False
        if ok and full:
            next_full = now() + GOOGLE_FULL_CHECK
        wait = next_full - now()
        if not ok:
            wait = min(wait, GOOGLE_RETRY)
        try:
            await asyncio.wait_for(google_job.wake.wait(), timeout=max(60, wait.total_seconds()))
            await asyncio.sleep(2)   # let a burst of changes (e.g. several edits) settle first
        except asyncio.TimeoutError:
            pass


def feed_window() -> tuple[date, date]:
    """Which occurrences of a feed's repeating events are kept: a year back to two years ahead."""
    today = now().date()
    return today - timedelta(days=365), today + timedelta(days=730)


def customs_for(sid: str) -> list[dict]:
    """Events added on the status page to one source's calendar."""
    return [c for c in store.get_customs() if (c.get("source") or "ccs") == sid]


def source_events(sid: str, raw: bytes | None, rs: rules_mod.Ruleset | None = None) -> tuple[list[Event], str]:
    """A source's own events from a download (none for a local calendar, or before the first one), with
    its rules' time changes (items without an end time, 24-hour events…), before any edit; and the
    download's hash."""
    if raw is None or (source(sid) or {}).get("type") == "local":
        return [], ""
    if sid == "ccs":
        _, base, digest = parse(raw, settings.timezone, RULES_PARSE)
    else:
        base, digest = parse_feed(raw, settings.timezone, RULES_PARSE, sid, *feed_window())
    return (rs or ruleset(sid)).change_times(base), digest


def event_alarms() -> dict[str, str]:
    """The reminders set on the status page: {event UID: "15,60"} (minutes before the start)."""
    saved = store.get("event_alarms") or {}
    return {str(k): str(v) for k, v in saved.items() if isinstance(saved, dict)}


def publish(raw: bytes | None, sha: str | None = None, sid: str = "ccs") -> tuple[list[Event], list[Event]]:
    """Build a source's events from its last download (or none yet): its rules' time changes, then the
    edits and the events added here, the events its rules add, its rules' colors and emoji, and the
    reminders; store them. Returns (all its events now, its events before)."""
    rs = ruleset(sid)
    base, digest = source_events(sid, raw, rs)
    add_change_notes(base, sid)
    events = apply_changes(base, store.get_edits(), customs_for(sid), sid)
    events = rs.finish(sorted(events + rs.made(events, TZ), key=lambda e: e.start))
    alarms = event_alarms()
    events = [replace(e, alarms=alarms[e.uid]) if e.uid in alarms else e for e in events]
    feed = build_feed(events, calendar_name(sid), settings.timezone, calendar_color(sid))
    previous = store.load_events(sid)
    if raw is not None:
        store.save_calendar(skey(sid, "source"), raw, sha or digest)
    store.save_calendar(skey(sid, "feed"), feed, sha or digest)
    store.replace_events(events, sid)
    st(sid).event_count = sum(1 for e in events if not e.hidden)
    request_google_sync()
    follow_links(sid, events)
    return events, previous


# --- Linked events (F3.2): see app/links.py -------------------------------------------------------

_following = False


def event_links() -> dict[str, dict]:
    return links_mod.clean(store.get("event_links"))


def follow_links(sid: str, events: list[Event]):
    """After a calendar is built: the events linked to its events follow them (deleted with them, moved
    with them), and their calendars are built again."""
    global _following
    found = event_links()
    todo = links_mod.plan(found, sid, events)
    if not todo or _following:    # (a calendar built because of a link: its own links are followed next time)
        return
    touched = set()
    edits = store.get_edits()
    customs = {c["uid"]: c for c in store.get_customs()}
    for step in todo:
        kind, uid = step[0], step[1]
        if kind == "seen":
            found[uid]["at"] = step[2]
            continue
        if kind == "unlink":
            found.pop(uid, None)
            continue
        e = store.get_event(uid)
        if e is None or e.origin == "rule":
            found.pop(uid, None)
            continue
        if kind == "delete":
            if e.origin == "custom":
                store.delete_custom(uid)
            else:
                _hide(e)
            state.record("info", f"Deleted \"{e.title}\" ({e.start[:10]}) with the event it's linked to")
            found.pop(uid, None)
        else:       # move
            start, end = links_mod.shifted(e.start, e.end, step[2])
            if e.origin == "custom" and uid in customs:
                store.set_custom(uid, {**customs[uid], "start": start, "end": end})
            elif e.origin == "united":
                original = united_original(uid, e.source)
                if original:
                    base = edits.get(uid) or {"title": e.title, "all_day": e.all_day, "location": e.location,
                                              "description": e.description, "color": e.color, "base": original.fingerprint()}
                    store.set_edit(uid, {**base, "start": start, "end": end})
            state.record("info", f"Moved \"{e.title}\" to {start[:16].replace('T', ' ')} with the event it's linked to")
        touched.add(e.source)
    store.set("event_links", found)
    _following = True
    try:
        for one in touched:
            rebuild(one)
    finally:
        _following = False


def _hide(e: Event):
    """Hide a source's own event from every destination (deleting it would only bring it back)."""
    original = united_original(e.uid, e.source)
    if not original:
        return
    edit = store.get_edits().get(e.uid) or {
        "title": e.title, "start": e.start, "end": e.end, "all_day": e.all_day, "location": e.location,
        "description": e.description, "color": e.color, "base": original.fingerprint()}
    store.set_edit(e.uid, {**edit, "hidden": True})


def rebuild(sid: str | None = None):
    """Rebuild a source's feed (or every source's) from its last download, e.g. after an edit or a rename."""
    for one in ([sid] if sid else source_ids()):
        if one not in source_ids():
            continue
        found = store.get_calendar(skey(one, "source"))
        publish(found[0] if found else None, found[1] if found else None, one)


def preview(sid: str, body: bytes) -> tuple[list[Event], str]:
    """A downloaded calendar's events (with its rules' time changes, before edits), and its hash."""
    return source_events(sid, body)


def _event_time(e: Event, d: i18n.Dates, lang: str = "en") -> str:
    """An event's day and times in a change note, e.g. "Oct 23 7:15am–9:30am" or "Oct 23 (all day)"."""
    try:
        if e.all_day:
            return f"{d.short(date.fromisoformat(e.start[:10]))} ({i18n.tr(lang, 'all day')})"
        a, b = datetime.fromisoformat(e.start), datetime.fromisoformat(e.end)
        return f"{d.short(a.date())} {d.clock(a)}–{d.clock(b)}"
    except ValueError:
        return f"{e.start} – {e.end}"


def record_changes(sid: str, old: list[Event], new: list[Event]) -> int:
    """The "Record changes" rules: for each matching event the source changed (time, title or location),
    a note is added to the event ("Changed Oct 22: time Oct 23 7:15am–9:30am → Oct 23 8:05am–10:20am"),
    kept in kv change_notes:<source> and shown in its description, and a line goes in Activities and
    Logs; a matching event the source dropped is logged too. Returns how many changes were noted."""
    rs = ruleset(sid)
    if not rs.records_changes or not old:
        return 0
    watched = rs.watched
    lang = store.get("ui_lang") if store.get("ui_lang") in i18n.LANGS else "en"
    d, today = dates_for(lang), now().astimezone(TZ).date()
    before, after = {e.uid: e for e in old}, {e.uid for e in new}
    # A repeating event's occurrences have the start in their ID (<source>/<UID>/<start>), so a moved
    # one looks removed and added: pair those up within each series, in order.
    series = lambda uid: uid.rsplit("/", 1)[0] if uid.count("/") >= 2 else uid
    gone = {}
    for b in sorted((b for b in old if b.uid not in after), key=lambda b: b.start):
        gone.setdefault(series(b.uid), []).append(b)
    pairs = {}
    for e in sorted((e for e in new if e.uid not in before), key=lambda e: e.start):
        if gone.get(series(e.uid)):
            pairs[e.uid] = gone[series(e.uid)].pop(0)
    moved = {b.uid for b in pairs.values()}
    notes, count, S = store.get(skey(sid, "change_notes")) or {}, 0, st(sid)
    for e in new:
        b = before.get(e.uid) or pairs.get(e.uid)
        if not b or not (watched(e) or watched(b)):
            continue
        parts = []
        if (b.start, b.end, b.all_day) != (e.start, e.end, e.all_day):
            parts.append(f"time {_event_time(b, d, lang)} → {_event_time(e, d, lang)}")
        if b.title != e.title:
            parts.append(f'title "{b.title}" → "{e.title}"')
        if b.location != e.location:
            parts.append(f"location {b.location or '—'} → {e.location or '—'}")
        if parts:
            notes[e.uid] = (notes.get(e.uid, []) + [f"Changed {d.short(today)}: " + "; ".join(parts)])[-20:]
            S.record("info", f"{calendar_name(sid)} changed {e.title}: " + "; ".join(parts))
            count += 1
    for uid, b in before.items():
        if uid not in after and uid not in moved and watched(b):
            S.record("info", f"{calendar_name(sid)} removed {b.title} ({_event_time(b, d, lang)})")
            notes.pop(uid, None)
    store.set(skey(sid, "change_notes"), notes)
    return count


def add_change_notes(events: list[Event], sid: str):
    """Put the notes made by "Record changes" rules at the end of their events' descriptions."""
    notes = store.get(skey(sid, "change_notes")) or {}
    for e in events:
        if notes.get(e.uid):
            e.description = (e.description.rstrip() + "\n\n" if e.description.strip() else "") + "\n".join(notes[e.uid])


def apply_calendar(body: bytes, how: str, sid: str = "ccs") -> bool:
    """Publish a calendar file (downloaded or uploaded). Returns False if it was rejected."""
    S = st(sid)
    old_source = store.get_calendar(skey(sid, "source"))
    changed = not old_source or old_source[0] != body
    events_found, digest = preview(sid, body)
    if not events_found and store.event_count(sid) > 0:
        S.status = "error"
        S.message = (f"The {how} calendar has no events. Keeping the previous feed "
                     f"({S.event_count} events) in case this is a glitch.")
        S.record("warn", S.message)
        return False
    if changed and old_source:
        record_changes(sid, preview(sid, old_source[0])[0], events_found)
    events, previous = publish(body, digest, sid)
    S.status, S.last_success = "ok", now()
    if changed:
        S.last_change = now()
        old_ids, new_ids = {e.uid for e in previous}, {e.uid for e in events}
        added, removed = len(new_ids - old_ids), len(old_ids - new_ids)
        detail = f"{added} new, {removed} removed" if previous else "first copy"
        S.last_detail = detail
        S.message = f"{how[:1].upper()}{how[1:]}: {S.event_count} events in feed ({detail})"
        S.record("info", f"Schedule {how}: {S.event_count} events in feed ({detail})")
    else:
        S.last_detail = "no changes"
        S.message = f"Up to date: {S.event_count} events in feed (no changes)"
        S.record("info", f"Schedule {how}: no changes")
    return True


async def run_once(manual: bool = False, sid: str = "ccs"):
    """Download a source now (CCS+ or a feed) and publish it if it changed."""
    if sid != "ccs":
        return await run_feed(sid)
    if state.running or "ccs" not in source_ids():
        return
    if not logins.ccs_configured:
        # Nothing to do until the login is entered; the page shows the boxes for it.
        state.status = "setup"
        state.message = "Enter your CCS+ Username and Calendar Sync password to start downloading the schedule."
        state.save()
        return
    if state.login_failures >= MAX_AUTH_FAILURES and not manual:
        state.status = "paused"
        state.message = (f"Automatic downloads paused after {state.login_failures} rejected sign-ins, to avoid "
                         "locking your account. Check the Username and Calendar Sync password in the CCS+ Calendar Sync box, then press Sync now.")
        state.save()
        return

    state.running, state.status = True, "running"
    state.last_attempt = now()
    try:
        have_source = store.get_calendar("source") is not None
        cache = (store.get("http_cache") or {}) if have_source else {}
        uid, password = logins.ccs()
        dl = await download(calendar_url(), uid, password,
                            etag=cache.get("etag", ""), last_modified=cache.get("last_modified", ""))
        store.save_debug("response", json.dumps(dl.debug, indent=2).encode(), "application/json")
        state.last_auth, state.last_auth_ok, state.login_failures = now(), True, 0

        if dl.not_modified:
            state.status, state.last_success, state.last_detail = "ok", now(), "no changes"
            state.message = f"Up to date: {state.event_count} events in feed (no changes)"
            state.record("info", "Schedule downloaded from CCS+: no changes")
            return

        store.save_debug("source", dl.body, "text/calendar; charset=utf-8")
        if apply_calendar(dl.body, "downloaded from CCS+"):
            store.set("http_cache", {"etag": dl.etag, "last_modified": dl.last_modified})

    except AuthError as e:
        state.last_auth, state.last_auth_ok = now(), False
        state.login_failures += 1
        state.status, state.message = "auth_failed", str(e)
        state.record("error", f"Sign-in rejected: {e}")
    except BlockedError as e:
        state.status, state.message = "blocked", str(e)
        state.record("error", f"Blocked: {e}")
    except SourceError as e:
        state.status, state.message = "error", str(e)
        state.record("error", f"Download failed: {e}")
    except Exception as e:
        state.status, state.message = "error", f"{type(e).__name__}: {e}"
        state.record("error", f"Unexpected error: {state.message}")
    finally:
        state.running = False
        state.save()


async def run_feed(sid: str):
    """Download a feed source (no login) and publish it if it changed."""
    S = st(sid)
    if S.running or sid not in source_ids():
        return
    S.running, S.status = True, "running"
    S.last_attempt = now()
    try:
        url = source_url(sid)
        host = urlparse(url).hostname or url
        have_source = store.get_calendar(skey(sid, "source")) is not None
        cache = (store.get(skey(sid, "http_cache")) or {}) if have_source else {}
        dl = await download(url, etag=cache.get("etag", ""), last_modified=cache.get("last_modified", ""), who=host)
        store.save_debug(skey(sid, "response"), json.dumps(dl.debug, indent=2).encode(), "application/json")
        if dl.not_modified:
            S.status, S.last_success, S.last_detail = "ok", now(), "no changes"
            S.message = f"Up to date: {S.event_count} events in feed (no changes)"
            S.record("info", f"Schedule downloaded from {host}: no changes")
            return
        store.save_debug(skey(sid, "source"), dl.body, "text/calendar; charset=utf-8")
        if apply_calendar(dl.body, f"downloaded from {host}", sid):
            store.set(skey(sid, "http_cache"), {"etag": dl.etag, "last_modified": dl.last_modified})
    except (AuthError, BlockedError, SourceError) as e:
        S.status, S.message = "error", str(e)
        S.record("error", f"Download failed: {e}")
    except Exception as e:
        S.status, S.message = "error", f"{type(e).__name__}: {e}"
        S.record("error", f"Unexpected error: {S.message}")
    finally:
        S.running = False
        S.save()


MIN_INTERVAL, MAX_INTERVAL = 15, 24 * 60   # minutes between automatic downloads


def interval_minutes(sid: str = "ccs") -> int:
    """How often to download a source: set on the status page, else SYNC_INTERVAL_MINUTES (CCS+) or an hour."""
    saved = store.get(skey(sid, "sync_interval"))
    default = settings.interval_minutes if sid == "ccs" else 60
    return saved if isinstance(saved, int) and MIN_INTERVAL <= saved <= MAX_INTERVAL else default


async def loop(sid: str = "ccs"):
    """One source's checks, every interval_minutes."""
    S = st(sid)
    while True:
        try:
            await run_once(sid=sid)
            S.next_run = now() + timedelta(minutes=interval_minutes(sid))
        except Exception as e:      # e.g. the database restarting: keep the loop alive, try again soon
            log.error("Scheduled check failed: %s", e)
            S.next_run = now() + timedelta(minutes=5)
        # Sleep until the next check. S.wake means the interval changed: work out the time again.
        while (remaining := (S.next_run - now()).total_seconds()) > 0:
            S.wake.clear()
            try:
                await asyncio.wait_for(S.wake.wait(), timeout=remaining)
            except asyncio.TimeoutError:
                break


source_tasks: dict[str, asyncio.Task] = {}


def start_source(sid: str):
    """Start a source's checks (when the app starts or the source is added); a local calendar has none."""
    if (source(sid) or {}).get("type") == "local":
        return
    if sid not in source_tasks or source_tasks[sid].done():
        source_tasks[sid] = asyncio.create_task(loop(sid))


def stop_source(sid: str):
    task = source_tasks.pop(sid, None)
    if task:
        task.cancel()


_background: set[asyncio.Task] = set()


def background(coro):
    """Start a task without waiting for it, keeping a reference so it isn't garbage-collected."""
    task = asyncio.create_task(coro)
    _background.add(task)
    task.add_done_callback(_background.discard)
    return task


def auto_update() -> bool:
    """Settings → Updates → Auto-update (beta.3): install a newer version by itself (needs the updater)."""
    return store.get("update_auto") is True


async def update_loop():
    """Settings → Check for updates: look for a newer version of this install's channel when due, and
    with Auto-update on (and the updater running), install it."""
    await asyncio.sleep(30)
    while True:
        try:
            if updates.due(datetime.now(timezone.utc)):
                found = await updates.check()
                if updates.available() and found.get("newest") != found.get("logged"):
                    state.record("info", f"Update available: CalendarStream {found['newest']} "
                                         + ("(Auto-update will install it)" if auto_update() and updater.ready and not updater.pinned()
                                            else "(press Update now next to the version)" if updater.ready and not updater.pinned()
                                            else "(run the installer again to update)"))
                    store.set("update_check", {**found, "logged": found["newest"]})
            await auto_install()
        except Exception as e:      # never let this stop the app
            log.warning("Update check failed: %s", e)
        await asyncio.sleep(3600)


async def auto_install():
    """With Auto-update on: ask the updater for a newer version (once per version, so a failing
    update isn't tried every hour)."""
    target = updates.available()
    if not (target and auto_update() and updater.ready and not updater.pinned()) or store.get("update_auto_tried") == target:
        return
    store.set("update_auto_tried", target)
    try:
        await updater.update()
        state.record("info", f"Auto-update: updating to CalendarStream {target}: downloading, then restarting")
    except UpdaterError as e:
        state.record("warn", f"Auto-update to CalendarStream {target} not started: {e}")


async def updater_loop():
    """Whether the optional updater container is running (checked now and every 5 minutes), so the
    page knows whether to offer "Update now"."""
    while True:
        try:
            await updater.probe()
        except Exception as e:      # never let this stop the app
            log.warning("Updater check failed: %s", e)
        await asyncio.sleep(300)


@asynccontextmanager
async def lifespan(_app):
    await asyncio.to_thread(store.open)       # waits for the database container if needed
    settings.resolve_feed_token(store)
    if store.get("feed_token_manual") and store.get("feed_token"):
        settings.feed_token = store.get("feed_token")      # a stream name entered by hand wins over FEED_TOKEN
    state.load()
    import_public_url()
    migrate_sources()
    migrate_destinations()
    migrate_rules()
    ensure_local()
    share_converted_rules()
    imported = logins.import_old(settings.username, settings.password, settings.gui_user, settings.gui_password)
    if imported:
        state.record("info", "Imported " + " and ".join(imported) + " from the old secret files. They're "
                     "now kept in the database and changed on the status page; the files can be deleted.")
    if not logins.has_page_login:
        # First start: the status page asks for this code before the login can be created.
        log.warning("First-time setup: open the status page and enter the setup code %s", logins.new_setup_code())
    # Re-apply current settings (calendar name, DEFAULT_EVENT_HOURS, edits) to the last download
    try:
        rebuild()
    except Exception as e:
        log.error("Couldn't rebuild the feed from the stored download: %s", e)
    for sid in source_ids():
        start_source(sid)
    tasks = [asyncio.create_task(google_loop()), asyncio.create_task(update_loop()), asyncio.create_task(updater_loop())]
    yield
    tasks += list(source_tasks.values())
    source_tasks.clear()
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    store.close()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, version=__version__)


@app.middleware("http")
async def protect(request: Request, call_next):
    """Refuse form posts sent from other websites (the browser marks them Sec-Fetch-Site: cross-site),
    except Google's change notifications, and add headers that stop other sites framing the pages and
    the pages leaking their address."""
    if (request.method == "POST" and request.headers.get("sec-fetch-site") == "cross-site"
            and request.url.path != "/google/notify"):
        return Response("Cross-site requests aren't accepted.", status_code=403)
    response = await call_next(request)
    # Only this site may show its pages in a frame (the event and print previews do, 0.2.8)
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Content-Security-Policy", "frame-ancestors 'self'")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    # Caching (0.2.8-beta.4): files whose address names the version (?v=…, /assets/…-<version>-…) never
    # change, so browsers keep them a year; other static files (the fonts) a day, then ask again.
    path = request.url.path
    if path.startswith(("/static/", "/assets/")) and response.status_code == 200:
        versioned = request.query_params.get("v") == __version__ or path.startswith(f"/assets/page-{__version__}-")
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable" if versioned else "public, max-age=86400"
    return response
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
# Material Symbols for every page: {{ icon_sprite() }} once at the top of <body>, then {{ icon("delete") }}
# draws one; icon_mask("check") is for stylesheets.
templates.env.globals.update(icon=icons.svg, icon_mask=icons.mask, icon_sprite=icons.sprite)
# The fonts (IBM Plex Sans and Mono): served from here, so pages never load anything from elsewhere.
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


# --- The status page's stylesheet and script, cached (0.2.8-beta.4) -----------------------------------
# They used to be inside every page (about 150 KB, sent again on each load and each in-place save). Now
# they're files the browser keeps: the stylesheet as it is, the script made once per language (its words
# are translated). Both are sent compressed when the browser accepts it: they hold no secrets, so
# compressing them is safe (the pages themselves, which hold the form token, are not compressed).
_ASSETS: dict[str, tuple[bytes, bytes]] = {}


def _asset(key: str, make) -> tuple[bytes, bytes]:
    if key not in _ASSETS:
        raw = make()
        _ASSETS[key] = (raw, gzip.compress(raw, 9))
    return _ASSETS[key]


def _send_asset(request: Request, key: str, make, media_type: str) -> Response:
    raw, packed = _asset(key, make)
    if "gzip" in request.headers.get("accept-encoding", ""):
        return Response(packed, media_type=media_type, headers={"Content-Encoding": "gzip", "Vary": "Accept-Encoding"})
    return Response(raw, media_type=media_type, headers={"Vary": "Accept-Encoding"})


@app.get("/assets/app.css")
def app_css(request: Request):
    return _send_asset(request, "app.css", lambda: (Path(__file__).parent / "static" / "app.css").read_bytes(), "text/css; charset=utf-8")


@app.get("/assets/page-{version}-{lang}.js")
def page_js(request: Request, version: str, lang: str):
    if version != __version__ or lang not in i18n.LANGS:
        raise HTTPException(404)
    make = lambda: templates.env.get_template("page.js").render(
        _=lambda text, **kw: i18n.tr(lang, text, **kw), lang=lang).encode()
    return _send_asset(request, f"page-{lang}.js", make, "text/javascript; charset=utf-8")


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    """Show form errors as a small page in the visitor's language (the API keeps JSON). Sign-in
    prompts (401) and redirects (303) pass through unchanged."""
    if _is_async(request) and exc.status_code not in (303, 401):
        # A login saved from its Save button (see verify): the message, for next to the boxes
        try:
            lang = lang_for(request)
        except Exception:
            lang = "en"
        return JSONResponse({"detail": str(i18n.message(lang, str(exc.detail)))}, status_code=exc.status_code)
    wants_page = "text/html" in request.headers.get("accept", "") and not request.url.path.startswith("/api/")
    if exc.status_code in (303, 401) or not wants_page:
        return await default_http_error(request, exc)
    try:
        lang = lang_for(request)
    except Exception:
        lang = "en"
    return page(request, "error.html", {"detail": exc.detail, "code": exc.status_code},
                status_code=exc.status_code, lang=lang)
def _is_async(request: Request) -> bool:
    """A login form saved by the page's script (Save → Saved → Verifying… → ✓ / ✗), not a plain post."""
    return request.headers.get("x-cs-async") == "1"


basic = HTTPBasic(auto_error=False)


# --- Status-page login -------------------------------------------------------

GUI_MAX_FAILURES, GUI_LOCKOUT = 5, timedelta(minutes=15)
_gui_failures: dict[str, list] = {}   # client ip -> [failure count, locked-until]
_global_failures: list[datetime] = []  # every recent failure, from any address
GLOBAL_MAX_FAILURES = 50               # in GUI_LOCKOUT, from all addresses together: then everyone waits…
_good_ips: dict[str, datetime] = {}    # …except addresses that logged in successfully within GOOD_IP_FOR
GOOD_IP_FOR = timedelta(days=7)
_failures_lock = threading.Lock()      # gui_auth runs in worker threads


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "?"


def _check_lockout(ip: str):
    with _failures_lock:
        locked_until = _gui_failures.get(ip, [0, None])[1]
        if locked_until and now() < locked_until:
            raise HTTPException(429, "Too many failed attempts. Try again later.")
        # A limit for all addresses together, so guessing from many (made-up) addresses doesn't help.
        # Addresses that logged in successfully in the last 7 days (since the last restart) are exempt, so
        # strangers can't lock out the browsers the owner uses.
        cutoff = now() - GUI_LOCKOUT
        while _global_failures and _global_failures[0] < cutoff:
            _global_failures.pop(0)
        trusted = _good_ips.get(ip)
        if len(_global_failures) >= GLOBAL_MAX_FAILURES and not (trusted and now() - trusted < GOOD_IP_FOR):
            raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_failure(ip: str, what: str = "logins"):
    with _failures_lock:
        if len(_gui_failures) > 10_000:      # bounded: forget addresses that aren't locked out first
            for key in [k for k, (_, until) in list(_gui_failures.items()) if not until or until < now()][:5_000]:
                _gui_failures.pop(key, None)
        _global_failures.append(now())
        count = _gui_failures.get(ip, [0, None])[0] + 1
        locked = now() + GUI_LOCKOUT if count >= GUI_MAX_FAILURES else None
        _gui_failures[ip] = [0 if locked else count, locked]
    if locked:
        state.record("warn", f"Status page locked for {ip} after {GUI_MAX_FAILURES} failed {what}")
        raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_success(ip: str):
    with _failures_lock:
        _gui_failures.pop(ip, None)
        if len(_good_ips) > 1_000:
            _good_ips.clear()
        _good_ips[ip] = now()


def gui_auth(request: Request, creds: HTTPBasicCredentials | None = Depends(basic)):
    """The status-page login (HTTP Basic). Before one exists, every page leads to the first-visit form."""
    if not logins.has_page_login:
        raise HTTPException(303, headers={"Location": "/welcome"})
    ip = _client_ip(request)
    _check_lockout(ip)
    if creds and logins.check_page_login(creds.username, creds.password):
        _count_success(ip)
        return
    if creds:   # a real attempt (not just the browser's first, credential-less request)
        _count_failure(ip)
    raise HTTPException(401, headers={"WWW-Authenticate": 'Basic realm="CalendarStream"'})


def check_csrf(token: str, expected: str | None = None):
    if not secrets.compare_digest((token or "").encode(), (expected or CSRF_TOKEN).encode()):
        raise HTTPException(400, "This form has expired. Reload the page and try again.")


def renew_csrf():
    """A new form token, e.g. after the login changed, so a token seen before (such as on the
    first-visit page) can't be used against the new login."""
    global CSRF_TOKEN
    CSRF_TOKEN = secrets.token_urlsafe(24)


# --- Who reads the feed --------------------------------------------------------------------
#
# Google Calendar fetches a subscribed feed with its own reader ("Google-Calendar-Importer"). Noting
# when it last came shows whether Google can reach the feed at all: until it has, Google shows the
# subscription under its web address and without events.

def note_feed_read(user_agent: str, did: str):
    kind = "google" if "google" in user_agent.lower() else "other"
    reads = store.get(f"feed_reads:{did}") or {}
    last = from_iso(reads.get(kind))
    if last is None or now() - last > timedelta(minutes=1):     # don't write on every fetch
        reads[kind] = iso(now())
        store.set(f"feed_reads:{did}", reads)


def feed_reads(lang: str, did: str) -> dict:
    reads = store.get(f"feed_reads:{did}") or {}
    return {k: _local_time(reads.get(k), lang) for k in ("google", "other")}


# --- Stream names: the secret part of each feed's links ---------------------------------------

STREAM_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


def dest_for_token(token: str) -> dict | None:
    """The feed destination whose links use this stream name."""
    for d in destinations("feed"):
        if d["token"] and secrets.compare_digest(token.encode(), d["token"].encode()):
            return d
    return None


# --- Links ---------------------------------------------------------------------

def public_url() -> str:
    """The public address (☰ Settings), or "" (then links use the address the page was opened at).
    Always in normalise_public_url's form."""
    saved = store.get("public_url") or ""
    try:
        return normalise_public_url(saved) if saved else ""
    except ValueError:
        return ""


def import_public_url():
    """PUBLIC_URL used to be set in .env. Copy it into Settings once, so .env no longer needs it
    (an address cleared in Settings later isn't brought back)."""
    if store.get("public_url_imported"):
        return
    if settings.public_base_url and not store.get("public_url"):
        store.set("public_url", settings.public_base_url)
        state.record("info", f"Public address {settings.public_base_url} moved from .env to ☰ Settings "
                             "(PUBLIC_URL can be deleted from .env)")
    store.set("public_url_imported", True)


def base_url(request: Request) -> str:
    return public_url() or str(request.base_url).rstrip("/")


def feed_url(request: Request, token: str) -> str:
    return f"{base_url(request)}/calendar/{token}.ics"


def subscribe_links(request: Request, token: str) -> dict:
    feed = feed_url(request, token)
    return {
        "feed": feed,
        # Opens Google Calendar's "add this calendar?" prompt. Google expects the feed as webcal://.
        "google": "https://calendar.google.com/calendar/r?cid=" + quote("webcal://" + feed.split("://", 1)[1], safe=""),
        # webcal:// hands the feed to Apple Calendar / Outlook / the phone's default calendar app.
        "webcal": "webcal://" + feed.split("://", 1)[1],
        "page": f"{base_url(request)}/subscribe/{token}",
        "is_public": feed.startswith("https://") and not any(
            h in feed for h in ("localhost", "127.0.0.1", "testserver")),
    }


def google_redirect_uri(request: Request) -> str:
    """Where Google sends the browser back after sign-in. It must be listed exactly like this among
    the OAuth client's authorised redirect URIs in Google Cloud."""
    return f"{base_url(request)}/google/callback"


def _local_time(value: str | None, lang: str = "en") -> str:
    """An ISO time as local "15:42" today, or "Oct 19, 15:42" on another day."""
    try:
        when = datetime.fromisoformat(value).astimezone(TZ)
    except (TypeError, ValueError):
        return ""
    return dates_for(lang).when(when, now().date())


def _watch_view(lang: str) -> dict:
    """Instant updates from Google, for the page: on (every source's calendar has them, with the last
    notice) or why not."""
    if not notify_address():
        return {"on": False, "why": "needs a public https:// address (☰ → Public address)"}
    watches = [google.watch_info(d["id"]) for d in destinations("google")]
    for w in watches:
        if w.get("error") and w.get("address") == notify_address():
            return {"on": False, "why": w["error"]}
    if watches and all(w.get("id") for w in watches):
        last = max((w.get("last_notice") or "" for w in watches), default="")
        return {"on": True, "last": _local_time(last or None, lang)}
    return {"on": False, "why": "starts with the next sync"}


def _host_mismatch(request: Request) -> tuple[str, str] | None:
    """(public address host, this page's host) when they differ, e.g. a typo such as ccs vs css."""
    public = urlparse(public_url()).hostname or ""
    here = (request.url.hostname or "").lower()
    if public and here and public != here and here not in ("localhost", "127.0.0.1") and not _is_ip(here):
        return public, here
    return None


def _is_ip(host: str) -> bool:
    import ipaddress
    try:
        ipaddress.ip_address(host.strip("[]"))
        return True
    except ValueError:
        return False


def google_view(request: Request, lang: str = "en") -> dict:
    uri = google_redirect_uri(request)
    host = urlparse(uri).hostname or ""
    info = google.info()
    return {"configured": google.configured, "connected": google.connected, "info": info,
            "client_id": google.client_id, "has_secret": bool(google.client_secret),
            "check": google.client_check(), "checked_at": _local_time(google.client_check().get("at"), lang),
            # Google said it doesn't list this page's redirect URI (only counts for the address checked)
            "redirect_missing": google.client_check().get("redirect_ok") is False
                                and google.client_check().get("redirect_uri") == uri,
            "running": google_job.running, "last_sync": _local_time(info.get("last_sync"), lang),
            "redirect_uri": uri, "watch": _watch_view(lang), "host_mismatch": _host_mismatch(request),
            "admin_email": admin_email(), "on": bool(destinations("google")),
            "calendars": [{"did": d["id"], "name": d["name"], **google.cal_info(d["id"])} for d in destinations("google")],
            "events": sum(int(google.cal_info(d["id"]).get("events") or 0) for d in destinations("google")),
            # Google only sends sign-ins back to https:// addresses with a public domain name (not a bare IP or .local),
            # or to http://localhost on this computer.
            "redirect_ok": (uri.startswith("https://") and not _is_ip(host) and not host.endswith(".local"))
                           or host in ("localhost", "127.0.0.1")}


# --- Month view ----------------------------------------------------------------

def _span(e: Event, tz: ZoneInfo | None = None) -> tuple[date, date, datetime | None, datetime | None]:
    """First and last calendar day an event covers (in `tz`, by default the display time zone)."""
    tz = tz or display_tz()
    if e.all_day:
        first, end = date.fromisoformat(e.start[:10]), date.fromisoformat(e.end[:10])
        return first, max(first, end - timedelta(days=1)), None, None
    s = datetime.fromisoformat(e.start).astimezone(tz)
    t = datetime.fromisoformat(e.end).astimezone(tz)
    last = (t - timedelta(microseconds=1)).date() if t > s else s.date()
    return s.date(), last, s, t


VIEWS = ("month", "week", "day", "list")


def ui_view() -> str:
    """The calendar's view on the status page: month, week, day or list (agenda)."""
    view = store.get("ui_view")
    return view if view in VIEWS else "month"


def cal_view(events: list[Event], view: str, ref: date, lang: str = "en") -> dict:
    """The calendar around `ref`: a month grid, one week, one day, or a list of a month's days
    with events. ‹ › move by a month, week or day."""
    tz = display_tz()
    dates = dates_for(lang)
    hm = dates.clock
    cont = str(i18n.tr(lang, "cont."))
    month_first = ref.replace(day=1)
    month_last = ref.replace(day=pycal.monthrange(ref.year, ref.month)[1])
    if view == "week":
        first_day = ref - timedelta(days=(ref.weekday() + 1) % 7)       # Sunday first, like CCS+
        last_day = first_day + timedelta(days=6)
        prev, nxt = ref - timedelta(days=7), ref + timedelta(days=7)
        title = f"{dates.day(first_day)} – {dates.day(last_day)}, {last_day.year}"
    elif view == "day":
        first_day = last_day = ref
        prev, nxt = ref - timedelta(days=1), ref + timedelta(days=1)
        title = f"{dates.day(ref)}, {ref.year}"
    else:       # month grid or list: the month's weeks / days
        weeks = pycal.Calendar(firstweekday=6).monthdatescalendar(ref.year, ref.month)
        first_day, last_day = (weeks[0][0], weeks[-1][-1]) if view == "month" else (month_first, month_last)
        prev = month_first - timedelta(days=1)
        nxt = month_last + timedelta(days=1)
        title = dates.title(ref)
    colors = {sid: calendar_color(sid) or DEFAULT_COLOR for sid in source_ids()}
    by_day: dict[date, list] = {}
    count = 0
    span_first, span_last = (month_first, month_last) if view in ("month", "list") else (first_day, last_day)
    for e in events:
        d0, d1, s, t = _span(e, tz)
        if d1 < first_day or d0 > last_day:
            continue
        if d1 >= span_first and d0 <= span_last:
            count += 1
        d = max(d0, first_day)
        while d <= min(d1, last_day):
            if s is None:
                when = "" if d == d0 else cont
            elif d0 == d1:
                when = f"{hm(s)}–{hm(t)}"
            elif d == d0:
                when = f"{hm(s)} →"
            elif d == d1:
                when = f"→ {hm(t)}"
            else:
                when = cont
            by_day.setdefault(d, []).append({"e": e, "when": when, "first": d == d0,
                                             "tag_color": e.color or e.rule_color,
                                             "src_color": colors.get(e.source, ""),
                                             "multi": d0 != d1, "range": _range_text(e, s, t, lang)})
            d += timedelta(days=1)
    days = [first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)]
    cell = lambda d: {"date": d, "in_month": d.month == ref.month, "items": by_day.get(d, [])}
    return {
        "view": view, "title": title, "dow": dates.dow, "ref": ref.isoformat(),
        "weeks": [[cell(d) for d in days[i:i + 7]] for i in range(0, len(days), 7)] if view in ("month", "week") else [],
        "days": [cell(d) for d in days if view == "day" or by_day.get(d)] if view in ("day", "list") else [],
        "prev": prev.isoformat(), "next": nxt.isoformat(), "month": f"{ref:%Y-%m}",
        "today": now().astimezone(tz).date(), "count": count,
    }


def month_view(events: list[Event], year: int, month: int, lang: str = "en") -> dict:
    """The month grid (kept for callers from before the other views)."""
    return cal_view(events, "month", date(year, month, 1), lang)


def _range_text(e: Event, s, t, lang: str = "en") -> str:
    """When an event happens, e.g. "Mon Oct 5, 09:00–10:00" or "Mon Oct 5 – Wed Oct 7 (all day)"."""
    dates = dates_for(lang)
    day, hm = dates.day, dates.clock
    if s is None:
        a, b = date.fromisoformat(e.start[:10]), date.fromisoformat(e.end[:10]) - timedelta(days=1)
        return day(a) + ("" if a == b else f" – {day(b)}") + " " + str(i18n.tr(lang, "(all day)"))
    if s.date() == t.date():
        return f"{day(s.date())}, {hm(s)}–{hm(t)}"
    return f"{day(s.date())} {hm(s)} – {day(t.date())} {hm(t)}"


def _parse_month(value: str | None) -> tuple[int, int]:
    try:
        y, m = map(int, (value or "").split("-"))
        if 2000 <= y <= 2100 and 1 <= m <= 12:
            return y, m
    except ValueError:
        pass
    today = now().date()
    return today.year, today.month


# --- Routes ----------------------------------------------------------------------

def source_view(request: Request, sid: str, lang: str, sections: dict) -> dict:
    """One calendar's module on the status page."""
    S = st(sid)
    kind = (source(sid) or {}).get("type", "ccs")
    if kind == "local":       # nothing to download: always fine
        S.status, S.message = "ok", ""
    url = source_url(sid)
    d = dates_for(lang)
    view = {"id": sid, "type": kind, "name": calendar_name(sid), "default": source_ids()[:1] == [sid],
            "color": calendar_color(sid), "s": S, "interval": interval_minutes(sid),
            "url": url, "host": urlparse(url).hostname or url,
            # Configure is folded unless it's been opened, or something needs doing
            "open": sections.get(f"src:{sid}", False) or S.status not in ("ok", "running", "starting")
                    or (sid == "ccs" and not logins.ccs_configured),
            "downloaded": store.get_calendar(skey(sid, "source")) is not None,
            "has_debug": store.has_debug(skey(sid, "source")),
            "last_when": d.when(S.last_success, now().date()) if S.last_success else "",
            # "Last check was successful @ 14:34" / "Last check failed @ 14:49"
            "last_check": ("ok" if S.status in ("ok", "running") and S.last_success else "failed" if S.last_attempt else ""),
            "check_when": d.when(S.last_success if S.status in ("ok", "running") else S.last_attempt, now().date())
                          if (S.last_success or S.last_attempt) else "",
            "added": sum(1 for c in customs_for(sid)),
            # its rules, highest priority first (its own ones first, unless moved)
            "rules": [{**r, "label": rule_label(r, lang), "html": rule_label_html(r, lang), "local": rules_mod.is_local(r, sid)} for r in source_rules(sid)],
            "preset": (source(sid) or {}).get("preset", "other"), "next_when": dates_for(lang).when(S.next_run, now().date()) if S.next_run else "",
            # the note under the title: as set (even empty), else the kind of calendar
            "note": source_note(sid)}
    if sid == "ccs":
        view["setup"] = {
            "uid": logins.ccs()[0], "has_password": bool(logins.ccs()[1]), "configured": logins.ccs_configured,
            "url": url, "url_is_default": url == DEFAULT_CALENDAR_URL, "url_from_gui": bool(store.get("calendar_url")),
            "downloaded": view["downloaded"]}
    return view


def dest_view(request: Request, d: dict, lang: str, sections: dict) -> dict:
    """One destination's box on the status page ("open": its Configure part, as last left)."""
    view = {**d, "names": [calendar_name(x) for x in d["sources"]], "open": sections.get(f"dest:{d['id']}", False)}
    if d["type"] == "feed":
        view.update(feed=feed_url(request, d["token"]), links=subscribe_links(request, d["token"]),
                    reads=feed_reads(lang, d["id"]))
    else:
        cal = google.cal_info(d["id"])
        view.update(cal=cal, last_sync=_local_time(cal.get("last_sync"), lang))
    return view


def _parse_day(value: str | None, month: str | None) -> date:
    """The day the calendar is around: ?date=YYYY-MM-DD, else the first of ?month=YYYY-MM, else today
    (in the display time zone); today's day when only the month is today's."""
    try:
        d = date.fromisoformat(value or "")
        if 2000 <= d.year <= 2100:
            return d
    except ValueError:
        pass
    today = now().astimezone(display_tz()).date()
    if month:
        y, m = _parse_month(month)
        return today if (y, m) == (today.year, today.month) else date(y, m, 1)
    return today


def rule_js(lang: str) -> dict:
    """What the rule dialog's script needs: every rule as saved, and the choices, in the page's language."""
    tr = lambda text: str(i18n.tr(lang, text))
    return {"rules": {r["id"]: r for r in all_rules()},
            "types": {k: tr(v) for k, v in rules_mod.COND_TYPES.items()},
            "ops": {k: [[o, tr(v)] for o, v in ops.items()] for k, ops in rules_mod.OPS.items()},
            "actions": [[k, tr(v)] for k, v in rules_mod.ACTION_TYPES.items()],
            "when": [[k, tr(v)] for k, v in rules_mod.WHEN.items()],
            "templates": [[t["id"], t["title"]] for t in event_templates()],
            "days": [tr(d) for d in rules_mod.DAY_NAMES],
            "calendars": [[sid, calendar_name(sid)] for sid in source_ids()],
            "emoji": ["✈️", "🏝️", "📚", "🏠", "🚗", "⭐", "❗", "🛌", "🎓", "🎉"],
            # Google's 11 event colors: a rule's Color is one of them (0.2.8-beta.5), as an event's is
            "palette": [[hexc, str(i18n.tr(lang, name))] for name, hexc in GOOGLE_COLORS.values()],
            "t": {"and": tr("and"), "or": tr("or"), "weeks": tr("weeks"), "days": tr("days"), "hours": tr("hours"),
                  "minutes": tr("minutes"), "caps": tr("Match capitals exactly"), "remove": tr("Take this line out"),
                  "newEvent": tr("New event…"), "noCalendar": tr("No calendar yet"), "color": tr("Color"), "title": tr("Title"), "location": tr("Location"), "allDay": tr("All day"),
                  "length": tr("Length (hours:minutes)"), "time": tr("Time (hours:minutes)"), "allCalendars": tr("All calendars"),
                  "toAllDay": tr("all-day"), "toLength": tr("a length of"), "changeTo": tr("to"), "emoji": tr("Emoji"),
                  "open": tr("Open a bracket here"), "close": tr("Close a bracket here"),
                  "noEnd": tr("0 = no end time")}}


@app.get("/", dependencies=[Depends(gui_auth)])
def index(request: Request, month: str | None = None, date_: str | None = Query(None, alias="date"),
          view: str | None = None):
    """The status page. `view` shows the calendar in another view this time only (phones open on the
    list until a view has been chosen)."""
    events = store.load_events()
    ref = _parse_day(date_, month)
    history = [{**h, "time": h["time"].astimezone(TZ)} for h in store.recent_log(100)]
    lang = lang_for(request)
    sections = section_state()
    srcs = [source_view(request, sid, lang, sections) for sid in source_ids()]
    return page(request, "index.html", {
        "s": state, "cfg": settings, "history": history, "cal": cal_view(events, view if view in VIEWS else ui_view(), ref, lang), "views": VIEWS,
        "view_explicit": store.get("ui_view") in VIEWS,
        "csrf": CSRF_TOKEN, "name": calendar_name(), "srcs": srcs,
        "dests": [dest_view(request, d, lang, sections) for d in destinations()], "dest_types": DESTINATION_TYPES,
        # every rule, highest priority first, with its label and calendars (All Rules; "+ Add a rule")
        "all_rules": [{**r, "label": rule_label(r, lang), "html": rule_label_html(r, lang),
                       "used": [calendar_name(x) for x in source_ids() if rules_mod.applies(r, x)]} for r in all_rules()],
        "rule_js": rule_js(lang),
        "rule_conflicts": rule_conflicts(lang),
        "linked": linked_titles(),
        "default_dest_name": first_named_calendar(),
        "src_names": {x["id"]: x["name"] for x in srcs},
        "has_ccs": "ccs" in source_ids(), "templates": event_templates(), "event_colors": GOOGLE_COLORS.values(),
        "sections": sections, "zone": display_zone(), "zones": ALL_ZONES, "common_zones": COMMON_ZONES,
        "google": google_view(request, lang), "open_menu": request.query_params.get("menu") == "settings",
        # The first destination offers this page's address as the public one, if it's https:// (an
        # http://<IP>:8080 address would break Google sign-in, as the old installer default did).
        "public": {"url": public_url(), "here": (lambda u: u if u.startswith("https://") else "")(str(request.base_url).rstrip("/"))},
        "page_user": logins.page_user, "admin_email": admin_email(), "trash": TRASH_ICON, "copy_icon": COPY_ICON,
        # Activities and Logs, folded: Healthy unless a problem in the log is still there
        "healthy": not any(st(sid).status in ("auth_failed", "blocked", "error", "paused") for sid in source_ids())
                   and not (google.connected and google.info().get("last_error")),
        "print_prefs": print_prefs(), "print_views": PRINT_VIEWS,
        "alarm_choices": [(m, alarm_text(m, lang)) for m in ALARM_CHOICES],
    }, lang=lang)


def _sid(sid: str) -> str:
    """A source ID from a form, which must be one of the sources."""
    if sid not in source_ids():
        raise HTTPException(400, "That calendar source doesn't exist (any more).")
    return sid


@app.post("/run", dependencies=[Depends(gui_auth)])
async def run_now(request: Request, csrf: str = Form(""), sid: str = Form("ccs")):
    """Sync now: download a source straight away, even while automatic checks are paused. From the
    page's script it answers at once; the page then follows the source in /api/status and updates
    its status and the calendar in place when it's done."""
    check_csrf(csrf)
    sid = _sid(sid)
    if not st(sid).running:
        background(run_once(manual=True, sid=sid))
        await asyncio.sleep(0.5)
    if _is_async(request):
        return {"ok": True, "running": st(sid).running}
    return RedirectResponse(f"/#src-{sid}", status_code=303)


async def _wait_idle(S: State, seconds: int = 120):
    """Wait for a source's download in progress to finish."""
    for _ in range(seconds * 4):
        if not S.running:
            return
        await asyncio.sleep(0.25)


@app.post("/verify", dependencies=[Depends(gui_auth)])
async def verify(request: Request, csrf: str = Form(""), kind: str = Form(""), sid: str = Form("")):
    """After a login was saved from its Save button: check it now (CCS+ downloads, Google checks the
    client, a feed downloads) and say whether it worked, for "✓ Validated" / "✗ Verification failed"."""
    check_csrf(csrf)
    lang = lang_for(request)
    if kind == "ccs":
        await _wait_idle(state)
        await run_once(manual=True)
        await _wait_idle(state)
        ok, message = bool(state.last_auth_ok) and state.status == "ok", state.message
    elif kind == "google":
        if not google.configured:
            return JSONResponse({"ok": False, "message": str(i18n.message(lang, "Enter the client secret too."))})
        check = await google.check_client(google_redirect_uri(request))
        ok = check.get("ok") is True
        message = check.get("message", "")
        if ok and check.get("redirect_ok") is False:
            message = f"Google doesn't list {check.get('redirect_uri')} under Authorised redirect URIs; add it to the client in Google Cloud"
        state.record("info" if ok else "warn", f"Google OAuth client checked: {message}")
    elif kind == "feed":
        S = st(_sid(sid))
        await _wait_idle(S)
        await run_once(manual=True, sid=sid)
        await _wait_idle(S)
        ok, message = S.status == "ok", S.message
    else:
        raise HTTPException(400, "Unknown kind of login.")
    return JSONResponse({"ok": ok, "message": str(i18n.message(lang, message)) if message else ""})


# --- Adding and removing sources and destinations ---------------------------------------------

def _feed_link(url: str) -> str:
    """A feed link as entered: webcal:// is the same as https://; only https:// is downloaded."""
    url = url.strip()
    if url.lower().startswith("webcal://"):
        url = "https://" + url[9:]
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise HTTPException(400, "The feed link must start with https:// (or webcal://).")
    return url


# Calendar Sources → + offers these presets. Google and Apple calendars are calendar feeds (their
# private iCal links), with their own step-by-step help; "other" is any .ics / webcal:// link.
SOURCE_PRESETS = {"google": "Google Calendar", "apple": "Apple Calendar", "other": "Calendar feed"}


def source_note(sid: str) -> str:
    """A calendar's own note (0.2.8-beta.9: shown as a raised (i) after its name), or "" when it has none.
    The header's first line now says what kind of calendar it is, so the old default notes (which said
    that, and were saved by any Save) count as no note."""
    note = store.get(skey(sid, "note")) or ""
    return "" if note.strip() == default_note(sid) else note


def default_note(sid: str) -> str:
    """What kind of calendar it is, as the note said until 0.2.8-beta.9 (to recognise old saved notes)."""
    x = source(sid) or {}
    if x.get("type") == "ccs":
        return "CCS+ Calendar Sync"
    if x.get("type") == "local":
        return "Events added here"
    preset = x.get("preset") if x.get("preset") in SOURCE_PRESETS else "other"
    url = x.get("url") or ""
    return SOURCE_PRESETS[preset] + ("" if preset != "other" else " · " + (urlparse(url).hostname or url))


@app.post("/sources/add", dependencies=[Depends(gui_auth)])
async def add_source(csrf: str = Form(""), type_: str = Form("", alias="type"), url: str = Form(""),
                     name: str = Form(""), note: str = Form(""), preset: str = Form("other")):
    """Calendars → +: a preset: a local calendar (events added here only), United's CCS+ Calendar Sync
    (once), a Google or Apple calendar (its private iCal link), or any other .ics feed link."""
    check_csrf(csrf)
    found = sources()
    if len(found) >= 10:
        raise HTTPException(400, "Up to 10 calendars can be added.")
    if type_ == "local":
        sid = new_local()
        found.append({"id": sid, "type": "local"})
        name = " ".join(name.split())[:100]
        store.set(f"calendar_name:{sid}", name or "Local")
    elif type_ == "ccs":
        if "ccs" in source_ids():
            raise HTTPException(400, "CCS+ Calendar Sync is already a source.")
        found.append({"id": "ccs", "type": "ccs"})
        sid = "ccs"
    elif type_ == "ics":
        url = _feed_link(url)
        if any(x.get("url") == url for x in found):
            raise HTTPException(400, "That feed is already a source.")
        sid = "f" + secrets.token_hex(3)
        found.append({"id": sid, "type": "ics", "url": url, "preset": preset if preset in SOURCE_PRESETS else "other"})
        name = " ".join(name.split())[:100]
        if name:
            store.set(f"calendar_name:{sid}", name)
    else:
        raise HTTPException(400, "Unknown kind of calendar source.")
    store.set("sources", found)
    state.record("info", f"Calendar source added: {calendar_name(sid)}")
    if " ".join(note.split()):
        store.set(skey(sid, "note"), " ".join(note.split())[:120])
    if len(source_ids()) == 1 or type_ == "local":     # into the feeds: the first calendar, and a local one
        save_destinations([{**d, "sources": d["sources"] + [sid]} for d in destinations()])
    rebuild(sid)
    start_source(sid)
    return RedirectResponse(f"/#src-{sid}", status_code=303)


def _moved(items: list[dict], key: str, before: str, after: str) -> list[dict]:
    """`items` with the one whose id is `key` put just above `before` (or just below `after`)."""
    ids = [x["id"] for x in items]
    if key not in ids:
        raise HTTPException(400, "That isn't there (any more).")
    as_rules = rules_mod.move([{"id": x["id"]} for x in items], key, before, after)
    by_id = {x["id"]: x for x in items}
    return [by_id[x["id"]] for x in as_rules]


@app.post("/sources/move", dependencies=[Depends(gui_auth)])
async def move_source(request: Request, csrf: str = Form(""), sid: str = Form(""), before: str = Form(""),
                      after: str = Form("")):
    """Drag (or ▲ ▼) a calendar module: the order of the calendars. The top one is the default
    calendar for events added here."""
    check_csrf(csrf)
    found = sources()
    moved = _moved(found, sid, before, after)
    if moved != found:
        store.set("sources", moved)
        if found[0]["id"] != moved[0]["id"]:
            state.record("info", f"Default calendar: {calendar_name(moved[0]['id'])}")
    return {"ok": True} if _is_async(request) else RedirectResponse("/#sources", status_code=303)


@app.post("/destinations/move", dependencies=[Depends(gui_auth)])
async def move_destination(request: Request, csrf: str = Form(""), did: str = Form(""), before: str = Form(""),
                           after: str = Form("")):
    """Drag (or ▲ ▼) a feed module: the order of the feeds."""
    check_csrf(csrf)
    found = destinations()
    moved = _moved(found, did, before, after)
    if moved != found:
        save_destinations(moved)
    return {"ok": True} if _is_async(request) else RedirectResponse("/#destinations", status_code=303)


@app.post("/sources/remove", dependencies=[Depends(gui_auth)])
async def remove_source(csrf: str = Form(""), sid: str = Form(""), keep: str = Form("delete"), into: str = Form("")):
    """Remove a source: its checks stop, its events and edits go, and it's taken off every
    destination's list (their calendars stay). CCS+'s UID and Calendar Sync password are forgotten too.
    F3.1 (0.2.8-beta.3): its events can be kept first, as a new Local calendar in its place
    (`keep=local`) or added to another calendar (`keep=merge`, `into`)."""
    check_csrf(csrf)
    sid = _sid(sid)
    name = calendar_name(sid)
    target = ""
    if keep == "local" and (source(sid) or {}).get("type") != "local":
        target = new_local()
        at = source_ids().index(sid)
        store.set("sources", sources()[:at] + [{"id": target, "type": "local"}] + sources()[at:])
        store.set(f"calendar_name:{target}", name)
        if calendar_color(sid):
            store.set(f"calendar_color:{target}", calendar_color(sid))
        save_destinations([{**d, "sources": [target if x == sid else x for x in d["sources"]]} for d in destinations()])
        save_rules([{**r, "apply": r["apply"] if r["apply"] == "all" else [target if x == sid else x for x in r["apply"]]}
                    for r in all_rules()])
    elif keep == "merge" and into in source_ids() and into != sid:
        target = into
    elif keep not in ("delete", "local", "merge"):
        raise HTTPException(400, "Unknown choice.")
    moved = copy_events(sid, target) if target else 0
    old_rules = all_rules()       # read while it's still a calendar
    stop_source(sid)
    store.set("sources", [x for x in sources() if x["id"] != sid])
    save_destinations([{**d, "sources": [x for x in d["sources"] if x != sid]} for d in destinations()])
    note = ""
    store.forget_source(sid)
    # its own rules go; rules for several calendars are taken off it
    save_rules([{**r, "apply": r["apply"] if r["apply"] == "all" else [x for x in r["apply"] if x != sid]}
                for r in old_rules if not rules_mod.is_local(r, sid)])
    for base in ("calendar_name", "calendar_color", "calendar_tags", "rule_subs", "defaults", "note", "sync_interval",
                 "http_cache", "status", "feed_reads"):
        store.delete(skey(sid, base))
    if sid == "ccs":
        logins.clear_ccs()
        store.delete("calendar_url")
        state.__init__("ccs")
    else:
        states.pop(sid, None)
    if target:
        rebuild(target)
        note = f"{moved} events kept in {calendar_name(target)}"
    state.record("info", f"Calendar source removed: {name}" + (f" ({note})" if note else ""))
    return RedirectResponse("/#sources", status_code=303)


def copy_events(sid: str, target: str) -> int:
    """A removed calendar's events (as they are now, with edits; not hidden or rule-made ones) as events
    added to calendar `target`, keeping their reminders and links. Returns how many."""
    alarms, found = event_alarms(), event_links()
    n = 0
    for e in store.load_events(sid):
        if e.origin == "rule" or e.hidden:
            continue
        uid = e.uid if e.origin == "custom" else f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(uid, {"title": e.title, "start": e.start, "end": e.end, "all_day": e.all_day, "location": e.location,
                               "description": e.description, "color": e.color, "start_tz": "", "end_tz": "", "source": target})
        if uid != e.uid:
            if e.uid in alarms:
                alarms[uid] = alarms.pop(e.uid)
            if e.uid in found:
                found[uid] = found.pop(e.uid)
        for link in found.values():
            if link["to"] == e.uid:
                link.update(to=uid, src=target)
        n += 1
    store.set("event_alarms", alarms)
    store.set("event_links", found)
    return n


@app.post("/sources/url", dependencies=[Depends(gui_auth)])
async def set_source_url(request: Request, csrf: str = Form(""), sid: str = Form(""), url: str = Form("")):
    """Change a feed source's link, then download it."""
    check_csrf(csrf)
    sid = _sid(sid)
    if sid == "ccs":
        raise HTTPException(400, "Use the Calendar Sync link field for CCS+.")
    url = _feed_link(url)
    store.set("sources", [{**x, "url": url} if x["id"] == sid else x for x in sources()])
    store.delete(skey(sid, "http_cache"))
    st(sid).record("info", f"Feed link changed to {urlparse(url).hostname}")
    if _is_async(request):
        return JSONResponse({"saved": True})      # the page then asks /verify
    background(run_once(manual=True, sid=sid))
    await asyncio.sleep(1)
    return RedirectResponse(f"/#src-{sid}", status_code=303)


@app.post("/destinations/add", dependencies=[Depends(gui_auth)])
async def add_destination(csrf: str = Form(""), type_: str = Form("", alias="type"), name: str = Form(""),
                          public: str = Form("")):
    """Calendar Destinations → +: a Google calendar, or a calendar feed, getting every source's events
    to start with (the list can be changed in its box). The first one asks for the public address
    (it can be changed later in ☰ Settings)."""
    check_csrf(csrf)
    if type_ not in DESTINATION_TYPES:
        raise HTTPException(400, "Unknown kind of destination.")
    # + Google Calendar (0.2.8-beta.4): kept in sync through the Google API when Google Calendar sync is
    # set up in Settings; otherwise a feed for the Google account to subscribe to.
    made_for = ""
    if type_ == "google" and not google.configured:
        type_, made_for = "feed", "google"
    if public.strip():
        try:
            store.set("public_url", normalise_public_url(public))
        except ValueError:
            raise HTTPException(400, "Enter the address people use to reach this page, e.g. https://cal.example.com")
        state.record("info", f"Public address set to {public_url()}")
    found = destinations()
    if len(found) >= 20:
        raise HTTPException(400, "Up to 20 destinations can be added.")
    name = " ".join(name.split())[:100] or first_named_calendar()
    did = new_did()
    found.append({"id": did, "type": type_, "name": name, "sources": source_ids(),
                  "token": secrets.token_urlsafe(24) if type_ == "feed" else "", "for": made_for})
    save_destinations(found)
    state.record("info", f"Destination added: {'Google Calendar (feed)' if made_for else DESTINATION_TYPES[type_]} \"{name}\"")
    if type_ == "google":
        request_google_sync(full=True)
    return RedirectResponse(f"/#dest-{did}", status_code=303)


def _did(did: str) -> dict:
    d = destination(did)
    if not d:
        raise HTTPException(400, "That destination doesn't exist (any more).")
    return d


async def sent_fields(request: Request, *names: str) -> list[str | None]:
    """Form fields as sent: "" when sent empty (e.g. a note cleared), None when not sent at all. (FastAPI
    reads an empty field as None for `str | None`, which can't tell the two apart.)"""
    form = await request.form()
    return [str(form[n]) if n in form else None for n in names]


@app.post("/destinations/update", dependencies=[Depends(gui_auth)])
async def update_destination(request: Request, csrf: str = Form(""), did: str = Form(""), name: str = Form(""),
                             sources_: list[str] = Form([], alias="sources"), start: str | None = Form(None),
                             end: str | None = Form(None)):
    """A destination's name, the sources it gets and its dates (Start / End; empty = no limit)."""
    check_csrf(csrf)
    start, end = await sent_fields(request, "start", "end")
    d = _did(did)
    if start is not None or end is not None:
        d["start"], d["end"] = _iso_day(start), _iso_day(end)
        if (start or "").strip() and not d["start"] or (end or "").strip() and not d["end"]:
            raise HTTPException(400, "Check the dates.")
        if d["start"] and d["end"] and d["end"] < d["start"]:
            raise HTTPException(400, "The end is before the start.")
    d["name"] = " ".join(name.split())[:100] or d["name"]
    d["sources"] = [x for x in source_ids() if x in sources_]
    save_destinations([d if x["id"] == did else x for x in destinations()])
    state.record("info", f"Destination \"{d['name']}\": " + (", ".join(calendar_name(x) for x in d["sources"]) or "no sources"))
    if d["type"] == "google":
        request_google_sync(full=True)
    return RedirectResponse(f"/#dest-{did}", status_code=303)


@app.post("/destinations/remove", dependencies=[Depends(gui_auth)])
async def remove_destination(csrf: str = Form(""), did: str = Form(""), delete: str = Form("")):
    """Remove a destination. A Google calendar is deleted in Google only when asked; a feed's links
    and subscribe page stop working."""
    check_csrf(csrf)
    d = _did(did)
    note = ""
    if d["type"] == "google":
        async with google_job.lock:
            if delete == "1":
                note = await google.delete_calendar(did)
            else:
                if google.connected:
                    await google.stop_watch([did])
                google.forget_calendar(did)
    else:
        store.delete(f"feed_reads:{did}")
    save_destinations([x for x in destinations() if x["id"] != did])
    what = " and its calendar in Google deleted" if d["type"] == "google" and delete == "1" and not note else ""
    state.record("warn" if note else "info", f"Destination removed: \"{d['name']}\"{what}" + (f" ({note})" if note else ""))
    return RedirectResponse("/#destinations", status_code=303)


@app.post("/feed/stream", dependencies=[Depends(gui_auth)])
async def set_stream(csrf: str = Form(""), did: str = Form(""), stream: str = Form("")):
    """Set a feed's stream name by hand, e.g. the one from before a reinstall, so old feed links and
    subscriptions work again. A whole old link can be pasted; its stream name is taken from it."""
    check_csrf(csrf)
    d = _did(did)
    if d["type"] != "feed":
        raise HTTPException(400, "Only calendar feeds have a stream name.")
    value = stream.strip()
    m = re.search(r"/(?:calendar|subscribe)/([A-Za-z0-9_-]+?)(?:\.ics)?/?$", value)
    if m:
        value = m.group(1)
    if not STREAM_RE.match(value):
        raise HTTPException(400, "A stream name is 16 to 128 letters, digits, - or _ (or paste a whole old feed link).")
    if any(x["token"] == value for x in destinations("feed") if x["id"] != did):
        raise HTTPException(400, "Another feed already uses that stream name.")
    save_destinations([{**x, "token": value} if x["id"] == did else x for x in destinations()])
    state.record("info", f"Stream name of \"{d['name']}\" changed; links with the old name no longer work")
    return RedirectResponse(f"/#dest-{did}", status_code=303)


# --- Logins -----------------------------------------------------------------------

@app.get("/welcome")
def welcome(request: Request):
    """First visit: create the status-page login (needs the setup code from the container log)."""
    if logins.has_page_login:
        return RedirectResponse("/", status_code=303)
    return page(request, "welcome.html", {"csrf": WELCOME_TOKEN, "error": ""})


@app.post("/welcome")
def create_login(request: Request, csrf: str = Form(""), code: str = Form(""), user: str = Form(""),
                 password: str = Form(""), confirm: str = Form("")):
    check_csrf(csrf, WELCOME_TOKEN)
    if logins.has_page_login:
        return RedirectResponse("/", status_code=303)
    ip = _client_ip(request)
    _check_lockout(ip)
    error = ""
    if not logins.check_setup_code(code):
        _count_failure(ip, "setup codes")
        error = ("That setup code isn't right. It's in the container log (docker compose logs | grep "
                 "\"setup code\", in the folder with docker-compose.yml).")
    else:
        try:
            logins.set_page_login(user, password, confirm)
        except LoginError as e:
            error = str(e)
    if error:
        return page(request, "welcome.html", {"csrf": WELCOME_TOKEN, "error": error, "user": user}, status_code=400)
    renew_csrf()
    state.record("info", f"Status-page login created for \"{logins.page_user}\"")
    return RedirectResponse("/", status_code=303)


@app.post("/settings/login", dependencies=[Depends(gui_auth)])
def change_login(request: Request, csrf: str = Form(""), current: str = Form(""), user: str = Form(""),
                 password: str = Form(""), confirm: str = Form("")):
    """Change the status-page user name and/or password (Settings menu). Needs the current password."""
    check_csrf(csrf)
    ip = _client_ip(request)
    if not logins.check_page_login(logins.page_user, current):
        _count_failure(ip)
        raise HTTPException(400, "The current password isn't right.")
    try:
        logins.set_page_login(user or logins.page_user, password or current, confirm if password else None)
    except LoginError as e:
        raise HTTPException(400, str(e))
    renew_csrf()
    state.record("info", f"Status-page login changed (user \"{logins.page_user}\")")
    # The browser still holds the old login; it will ask for the new one.
    return RedirectResponse("/", status_code=303)


GOOGLE_SETTINGS = "/?menu=settings#googlesync"      # Google Calendar sync is in ☰ Settings (0.2.8-beta.4)


def _back_to(back: str, anchor: str) -> str:
    """Where a dashboard form returns to: its own box. (`back` is accepted from older pages and ignored:
    the logins no longer appear in Settings.)"""
    return f"/#{anchor}"


@app.post("/setup/ccs", dependencies=[Depends(gui_auth)])
async def set_ccs_login(request: Request, csrf: str = Form(""), uid: str = Form(""), password: str = Form(""),
                        back: str = Form(""), url: str | None = Form(None)):
    """Save the CCS+ Site Address (the Calendar Sync link; empty = United's), UID and Calendar Sync
    password, then download straight away."""
    check_csrf(csrf)
    (url,) = await sent_fields(request, "url")
    if url is not None:
        url = url.strip()
        if not url or url == DEFAULT_CALENDAR_URL:
            store.delete("calendar_url")
        else:
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise HTTPException(400, "The Calendar Sync link must start with https://")
            if url != store.get("calendar_url"):
                store.set("calendar_url", url)
                store.delete("http_cache")
    try:
        logins.save_ccs(uid, password)
    except LoginError as e:
        raise HTTPException(400, str(e))
    state.login_failures = 0
    store.delete("http_cache")
    state.record("info", "CCS+ Username and Calendar Sync password saved")
    if _is_async(request):
        return JSONResponse({"saved": True})      # the page then asks /verify
    if not state.running:
        background(run_once(manual=True))
        await asyncio.sleep(1.5)   # usually long enough to show whether CCS+ accepted it
    return RedirectResponse(_back_to(back, "src-ccs"), status_code=303)


@app.post("/setup/interval", dependencies=[Depends(gui_auth)])
async def set_interval(csrf: str = Form(""), minutes: str = Form(""), sid: str = Form("ccs")):
    """Change how often a source is downloaded (saved in the database)."""
    check_csrf(csrf)
    sid = _sid(sid)
    S = st(sid)
    try:
        value = int(minutes)
    except ValueError:
        raise HTTPException(400, "Enter a number of minutes.")
    if not MIN_INTERVAL <= value <= MAX_INTERVAL:
        raise HTTPException(400, f"Choose between {MIN_INTERVAL} and {MAX_INTERVAL} minutes.")
    if sid == "ccs" and value == settings.interval_minutes:
        store.delete("sync_interval")
    else:
        store.set(skey(sid, "sync_interval"), value)
    # The next check counts from the last one (or now, if that time has already passed).
    S.next_run = max(now(), (S.last_attempt or now()) + timedelta(minutes=value))
    S.wake.set()
    S.record("info", f"Checks every {value} min from now on")
    return RedirectResponse(f"/#src-{sid}", status_code=303)


@app.post("/setup/link", dependencies=[Depends(gui_auth)])
async def set_link(csrf: str = Form(""), url: str = Form(""), action: str = Form("save")):
    """Save the Calendar Sync link (action=reset goes back to the default), then download."""
    check_csrf(csrf)
    if action == "reset":
        store.delete("calendar_url")
        state.record("info", "Calendar Sync link reset to the default")
    else:
        url = url.strip()
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise HTTPException(400, "The Calendar Sync link must start with https://")
        store.set("calendar_url", url)
        store.delete("http_cache")
        state.record("info", f"Calendar Sync link set to {parsed.netloc}{parsed.path}")
    state.login_failures = 0
    if not state.running:
        background(run_once(manual=True))
    return RedirectResponse("/#src-ccs", status_code=303)


@app.post("/feed/name", dependencies=[Depends(gui_auth)])
async def set_name(csrf: str = Form(""), name: str = Form(""), color: str = Form(""),
                   color_default: str = Form(""), sid: str = Form("ccs")):
    """Save a source's name and color (its (edit) link). A blank name goes back to the default
    (CALENDAR_NAME from .env for CCS+). `color` is only sent when it was changed on the page;
    `color_default` clears it."""
    check_csrf(csrf)
    sid = _sid(sid)
    name = " ".join(name.split())[:100]
    if name and not (sid == "ccs" and name == settings.calendar_name):
        store.set(skey(sid, "calendar_name"), name)
    else:
        store.delete(skey(sid, "calendar_name"))
    notes = [f"name \"{calendar_name(sid)}\""]
    if color_default:
        store.delete(skey(sid, "calendar_color"))
        notes.append("default color")
    elif color:
        if not COLOR_RE.match(color):
            raise HTTPException(400, "Choose the color with the color picker.")
        store.set(skey(sid, "calendar_color"), color.lower())
        notes.append(f"color {color.lower()}")
    rebuild(sid)
    state.record("info", "Calendar settings saved: " + ", ".join(notes))
    return RedirectResponse(f"/#src-{sid}", status_code=303)


DURATION_RE = re.compile(r"^\s*(?:(\d{1,3})\s*[:h]\s*(\d{1,2})?|(\d{1,3}(?:[.,]\d+)?)\s*(h|m|min)?)\s*$", re.I)


def parse_duration(text: str, default: int = 0) -> int:
    """Minutes from "1:30", "1h30", "2" (hours), "1.5" (hours), "90m"; `default` when empty.
    Raises ValueError when it isn't a duration."""
    text = (text or "").strip()
    if not text:
        return default
    m = DURATION_RE.match(text)
    if not m:
        raise ValueError(text)
    if m.group(1) is not None:
        return int(m.group(1)) * 60 + int(m.group(2) or 0)
    value = float(m.group(3).replace(",", "."))
    return round(value if (m.group(4) or "").lower() in ("m", "min") else value * 60)


def show_duration(minutes: int) -> str:
    return f"{minutes // 60}:{minutes % 60:02d}"


def _source_name_color(sid: str, name: str | None, color: str, color_default: str, note: str | None) -> list[str]:
    """Save a source's name, color and note (from its header, editable while Configure is open)."""
    notes = []
    if name is not None:
        name = " ".join(name.split())[:100]
        if name and not (sid == "ccs" and name == settings.calendar_name):
            store.set(skey(sid, "calendar_name"), name)
        else:
            store.delete(skey(sid, "calendar_name"))
        notes.append(f"name \"{calendar_name(sid)}\"")
    if color_default:
        store.delete(skey(sid, "calendar_color"))
        notes.append("default color")
    elif color:
        if not COLOR_RE.match(color):
            raise HTTPException(400, "Choose the color with the color picker.")
        store.set(skey(sid, "calendar_color"), color.lower())
        notes.append(f"color {color.lower()}")
    if note is not None:          # an empty note stays empty (it isn't replaced by the kind of calendar)
        store.set(skey(sid, "note"), " ".join(note.split())[:120])
    return notes


@app.post("/feed/tags", dependencies=[Depends(gui_auth)])
async def set_tags(request: Request, csrf: str = Form(""), sid: str = Form("ccs"), name: str | None = Form(None),
                   color: str = Form(""), color_default: str = Form(""), note: str | None = Form(None)):
    """Save a calendar module's header: its name, color and note (fields while it's expanded). Its rules
    are changed in the rule dialog and moved in place (/rules/…)."""
    check_csrf(csrf)
    name, note = await sent_fields(request, "name", "note")
    sid = _sid(sid)
    notes = _source_name_color(sid, name, color, color_default, note)
    if notes:
        rebuild(sid)
        state.record("info", f"{calendar_name(sid)} saved: " + ", ".join(notes))
    return RedirectResponse(f"/#src-{sid}", status_code=303)


def _rule_or_400(rid: str) -> tuple[list[dict], int]:
    found = all_rules()
    i = next((n for n, r in enumerate(found) if r["id"] == rid), None)
    if i is None:
        raise HTTPException(400, "That rule doesn't exist (any more).")
    return found, i


def _rule_done(request: Request, rule: dict | None, anchor: str = "/#rules"):
    if _is_async(request):
        return {"ok": True, "id": rule["id"] if rule else "", "label": rule_label(rule, lang_for(request)) if rule else ""}
    return RedirectResponse(anchor, status_code=303)


@app.post("/rules/save", dependencies=[Depends(gui_auth)])
async def save_rule(request: Request, csrf: str = Form(""), rule: str = Form("")):
    """Save a rule from the rule dialog (`rule`: the rule as JSON, see app/rules.py). A new one goes in
    at its place (one for a single calendar above that calendar's shared rules, others last); a
    changed one keeps its place."""
    check_csrf(csrf)
    try:
        raw = json.loads(rule)
        checked = rules_mod.normalize(raw, source_ids(), {t["id"] for t in event_templates()}, strict=True)
    except (ValueError, TypeError) as e:
        raise HTTPException(400, str(e) if isinstance(e, rules_mod.RuleError) else "That rule couldn't be read.")
    found = all_rules()
    ids = [r["id"] for r in found]
    if raw.get("id") in ids:
        checked["id"] = raw["id"]
        found[ids.index(raw["id"])] = checked
        what = "changed"
    else:
        if len(found) >= rules_mod.MAX_RULES:
            raise HTTPException(400, f"Up to {rules_mod.MAX_RULES} rules can be kept.")
        while checked["id"] in ids:
            checked["id"] = "t" + secrets.token_hex(3)
        found.insert(rules_mod.insert_position(found, checked), checked)
        what = "added"
    save_rules(found)
    rebuild()
    state.record("info", f"Rule {what}: {rule_label(checked)}")
    return _rule_done(request, checked)


@app.post("/rules/clone", dependencies=[Depends(gui_auth)])
async def clone_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id")):
    """All Rules: a copy of a rule, just below it, applying to no calendar yet; it opens in the rule
    dialog to be changed."""
    check_csrf(csrf)
    found, i = _rule_or_400(rid)
    if len(found) >= rules_mod.MAX_RULES:
        raise HTTPException(400, f"Up to {rules_mod.MAX_RULES} rules can be kept.")
    copy = {**found[i], "id": "t" + secrets.token_hex(3), "apply": []}
    found.insert(i + 1, copy)
    save_rules(found)
    state.record("info", f"Rule copied: {rule_label(copy)}")
    return RedirectResponse(f"/?rule={copy['id']}#rules", status_code=303)


@app.post("/rules/delete", dependencies=[Depends(gui_auth)])
async def delete_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id")):
    """Delete a rule (from every calendar)."""
    check_csrf(csrf)
    found, i = _rule_or_400(rid)
    gone = found.pop(i)
    save_rules(found)
    rebuild()
    state.record("info", f"Rule deleted: {rule_label(gone)}")
    return _rule_done(request, None)


@app.post("/rules/move", dependencies=[Depends(gui_auth)])
async def move_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id"), before: str = Form(""),
                    after: str = Form("")):
    """Change a rule's priority: put it just above `before` (or just below `after`). The page sends the
    neighbour it now has in the list it was moved in (All Rules, or a calendar's)."""
    check_csrf(csrf)
    found, _ = _rule_or_400(rid)
    moved = rules_mod.move(found, rid, before, after)
    if moved != found:
        save_rules(moved)
        rebuild()
    return _rule_done(request, next(r for r in moved if r["id"] == rid))


# --- Rule conflicts (F4.2) -----------------------------------------------------------------------

CONFLICT_WHAT = {"color": "color", "emoji": "emoji", "change": "time"}


def ignored_conflicts() -> list[str]:
    return [x for x in store.get("rule_conflicts_ignored") or [] if isinstance(x, str)]


def rule_conflicts(lang: str = "en") -> list[dict]:
    """The rules' conflicts in words, each with what can be done about it (All Rules shows them)."""
    tr = lambda text, **kw: str(i18n.tr(lang, text, **kw))
    found, sids = all_rules(), source_ids()
    by_id = {r["id"]: r for r in found}
    out = []
    for c in rules_mod.conflicts(found, sids, set(ignored_conflicts())):
        a, b = rule_label(by_id[c["a"]], lang), rule_label(by_id[c["b"]], lang)
        where = "" if len(c["calendars"]) == len(sids) else " " + tr("(in {calendars})", calendars=", ".join(calendar_name(x) for x in c["calendars"]))
        if c["kind"] == "duplicate":
            text = tr("“{b}” is the same as “{a}”", a=a, b=b) + where + "."
            fixes = [("merge", tr("Merge them")), ("ignore", tr("Keep both"))]
        else:
            what = tr(CONFLICT_WHAT[c["action"]])
            text = tr("“{b}” never sets the {what}: “{a}” is above it and matches the same events", a=a, b=b, what=what) + where + "."
            fixes = [("up", tr("Put “{b}” first", b=b)), ("drop", tr("Take the {what} out of “{b}”", what=what, b=b)), ("ignore", tr("Keep as is"))]
        out.append({"key": rules_mod.conflict_key(c), "a": c["a"], "b": c["b"], "text": text, "fixes": fixes})
    return out


@app.post("/rules/resolve", dependencies=[Depends(gui_auth)])
async def resolve_rules(request: Request, csrf: str = Form(""), key: str = Form(""), how: str = Form("")):
    """Settle a conflict between two rules (All Rules): put the lower rule first, take the action it
    loses out of it, merge duplicates, or leave them as they are (it's not shown again)."""
    check_csrf(csrf)
    found = all_rules()
    c = next((x for x in rules_mod.conflicts(found, source_ids()) if rules_mod.conflict_key(x) == key), None)
    if c is None:
        raise HTTPException(400, "That conflict isn't there any more.")
    if how not in {"duplicate": ("merge", "ignore"), "shadowed": ("up", "drop", "ignore")}[c["kind"]]:
        raise HTTPException(400, "Unknown choice.")
    ids = [r["id"] for r in found]
    a, b = found[ids.index(c["a"])], found[ids.index(c["b"])]
    if how == "ignore":
        store.set("rule_conflicts_ignored", (ignored_conflicts() + [key])[-200:])
        return _rule_done(request, b)
    if how == "up":
        found = rules_mod.move(found, b["id"], before=a["id"])
    elif how == "merge":
        found[ids.index(a["id"])] = rules_mod.merge(a, b)
        found.pop(ids.index(b["id"]))
    else:
        left = [x for x in b["actions"] if x["type"] != c["action"]]
        if left:
            found[ids.index(b["id"])] = {**b, "actions": left}
        else:
            found.pop(ids.index(b["id"]))
    save_rules(found)
    rebuild()
    state.record("info", f"Rule conflict settled ({how}): {rule_label(b)}")
    return _rule_done(request, a)


@app.post("/rules/apply", dependencies=[Depends(gui_auth)])
async def apply_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id"), sid: str = Form(""),
                     on: str = Form("1")):
    """Add a calendar to a rule's calendars (a calendar module's "+ Add a rule" menu), or take it off
    (the bin on a rule in a calendar module)."""
    check_csrf(csrf)
    sid = _sid(sid)
    found, i = _rule_or_400(rid)
    r = found[i]
    users = list(source_ids()) if r["apply"] == "all" else list(r["apply"])
    users = list(dict.fromkeys(users + [sid])) if on == "1" else [x for x in users if x != sid]
    r["apply"] = "all" if on == "1" and r["apply"] == "all" else users
    save_rules(found)
    rebuild(sid)
    state.record("info", f"Rule {'added to' if on == '1' else 'taken off'} {calendar_name(sid)}: {rule_label(r)}")
    return _rule_done(request, r, f"/#src-{sid}")


@app.post("/templates", dependencies=[Depends(gui_auth)])
async def set_templates(csrf: str = Form(""), tpl_id: list[str] = Form([]), tpl_title: list[str] = Form([]),
                        tpl_kind: list[str] = Form([]), tpl_duration: list[str] = Form([]),
                        tpl_location: list[str] = Form([]), tpl_color: list[str] = Form([])):
    """Save the event templates. Rows with no title are dropped; rules using a removed template stop
    adding events."""
    check_csrf(csrf)
    found = []
    old = {t["id"]: t for t in event_templates()}
    for tid, title, kind, dur, loc, color in zip_longest(tpl_id, tpl_title, tpl_kind, tpl_duration, tpl_location,
                                                         tpl_color, fillvalue=""):
        title = " ".join(title.split())[:200]
        if not title:
            continue
        try:
            minutes = parse_duration(dur, 60)
        except ValueError:
            raise HTTPException(400, f"Check the length of \"{title}\" (e.g. 1:30).")
        if kind != "allday" and not 5 <= minutes <= 24 * 60:
            raise HTTPException(400, f"\"{title}\" can last from 0:05 to 24:00.")
        color = color.lower()
        if color and color not in EVENT_COLORS:
            raise HTTPException(400, "Choose one of the colors offered.")
        tid = tid if re.fullmatch(r"[a-z0-9]{1,16}", tid or "") else "t" + secrets.token_hex(3)
        found.append({"id": tid, "title": title, "all_day": kind == "allday", "minutes": minutes if kind != "allday" else 60,
                      "location": loc.strip()[:200], "description": (old.get(tid) or {}).get("description", ""),
                      "color": color})
    if len(found) > MAX_TEMPLATES:
        raise HTTPException(400, f"Up to {MAX_TEMPLATES} templates can be kept.")
    store.set("event_templates", found)
    rebuild()
    state.record("info", f"Event templates saved: {len(found)}")
    return RedirectResponse("/#templates", status_code=303)


@app.post("/ui/section", dependencies=[Depends(gui_auth)])
async def set_section(csrf: str = Form(""), section: str = Form(""), open_: str = Form("", alias="open")):
    """Remember whether a status-page section is open (the page sends this when it's toggled)."""
    check_csrf(csrf)
    if section not in SECTIONS and not re.fullmatch(r"src:(ccs|f[0-9a-f]{6})|dest:(google|d[0-9a-f]{6})", section):
        raise HTTPException(400, "Unknown section.")
    saved = store.get("ui_sections") or {}
    saved[section] = open_ == "1"
    store.set("ui_sections", saved)
    return Response(status_code=204)


@app.post("/ui/lang", dependencies=[Depends(gui_auth)])
async def set_lang(csrf: str = Form(""), lang: str = Form("")):
    """Remember the status page's language (the language menu sends this); "auto" follows the browser."""
    check_csrf(csrf)
    if lang == "auto":
        store.delete("ui_lang")
    elif lang in i18n.LANGS:
        store.set("ui_lang", lang)
    else:
        raise HTTPException(400, "Unknown language.")
    return Response(status_code=204)


@app.post("/ui/clock", dependencies=[Depends(gui_auth)])
async def set_clock(csrf: str = Form(""), clock: str = Form("")):
    """Remember 12-hour / 24-hour times (the 12h / 24h switch above the calendar); "auto" follows the language."""
    check_csrf(csrf)
    if clock not in CLOCKS:
        raise HTTPException(400, "Unknown time format.")
    if clock == "auto":
        store.delete("ui_clock")
    else:
        store.set("ui_clock", clock)
    return Response(status_code=204)


@app.post("/ui/view", dependencies=[Depends(gui_auth)])
async def set_view(csrf: str = Form(""), view: str = Form("")):
    """Remember the calendar's view (month, week, day or list), chosen above the calendar."""
    check_csrf(csrf)
    if view not in VIEWS:
        raise HTTPException(400, "Unknown view.")
    store.set("ui_view", view)
    return Response(status_code=204)


@app.post("/ui/tz", dependencies=[Depends(gui_auth)])
async def set_display_tz(csrf: str = Form(""), tz: str = Form("")):
    """The time zone the calendar is shown in here; "" goes back to TZ from .env."""
    check_csrf(csrf)
    if not tz or tz == settings.timezone:
        store.delete("ui_tz")
    elif valid_zone(tz):
        store.set("ui_tz", tz)
    else:
        raise HTTPException(400, "Unknown time zone.")
    return Response(status_code=204)


@app.post("/update/now", dependencies=[Depends(gui_auth)])
async def update_now(csrf: str = Form("")):
    """Update now (next to "(vX is available)"): ask the updater container to pull this install's
    image and restart CalendarStream with it. The page then follows along through /api/status:
    still the old version while it downloads, no answer while it restarts, the new version after."""
    check_csrf(csrf)
    target = updates.available()
    if not target:
        raise HTTPException(400, "CalendarStream is already up to date.")
    if updater.pinned():
        raise HTTPException(400, "This install runs an exact version (IMAGE_TAG); choose latest or beta with the installer to update from here.")
    try:
        await updater.update()
    except UpdaterError as e:
        state.record("warn", f"Update to CalendarStream {target} not started: {e}")
        raise HTTPException(502, str(e))
    state.record("info", f"Updating to CalendarStream {target}: downloading, then restarting")
    return {"ok": True, "from": __version__, "to": target}


@app.post("/settings/updates", dependencies=[Depends(gui_auth)])
async def update_settings(csrf: str = Form(""), frequency: str = Form(""), action: str = Form("save"),
                          auto: str = Form(""), autoform: str = Form("")):
    """Settings → Check for updates: how often, Auto-update (the form always sends its tick box, with
    `autoform`), or check now."""
    check_csrf(csrf)
    if frequency:
        try:
            updates.set_frequency(frequency)
        except ValueError:
            raise HTTPException(400, "Unknown update frequency.")
    if autoform and (auto == "1") != auto_update():
        store.set("update_auto", auto == "1")
        state.record("info", "Auto-update " + ("on: newer versions are installed by themselves" if auto == "1" else "off"))
    if action == "check":
        await updates.check()
    return RedirectResponse("/?menu=settings#updates", status_code=303)


PRINT_VIEWS = ("itinerary", "day", "5day", "week", "month")


def print_prefs() -> dict:
    """The last print's choices (Print Preview starts with them): view, weekends, theme; {} before the first."""
    saved = store.get("ui_print") or {}
    return {k: saved[k] for k in ("view", "weekends", "theme") if k in saved} if isinstance(saved, dict) else {}


@app.post("/ui/print", dependencies=[Depends(gui_auth)])
async def set_print(csrf: str = Form(""), view: str = Form(""), weekends: str = Form("1"), theme: str = Form("light")):
    check_csrf(csrf)
    store.set("ui_print", {"view": view if view in PRINT_VIEWS else "month", "weekends": weekends == "1",
                           "theme": "dark" if theme == "dark" else "light"})
    return {"ok": True}


def print_pages(events: list[Event], view: str, first: date, last: date, weekends: bool, lang: str) -> list[dict]:
    """The calendar from `first` to `last` as pages to print: a month, a week (Sunday to Saturday), five
    days (Monday to Friday) or a day per page, or one itinerary (the days with events)."""
    pages: list[dict] = []
    if view == "itinerary":
        days = []
        ref = first.replace(day=1)
        while ref <= last:
            days += [d for d in cal_view(events, "list", ref, lang)["days"] if first <= d["date"] <= last]
            ref = (ref.replace(day=28) + timedelta(days=4)).replace(day=1)
        days = [d for d in days if weekends or d["date"].weekday() < 5]
        return [{"view": view, "title": "", "days": days}]
    if view == "month":
        ref = first.replace(day=1)
        while ref <= last and len(pages) < 24:
            pages.append(cal_view(events, "month", ref, lang))
            ref = (ref.replace(day=28) + timedelta(days=4)).replace(day=1)
    elif view in ("week", "5day"):
        ref = first - timedelta(days=(first.weekday() + 1) % 7)
        while ref <= last and len(pages) < 60:
            pages.append(cal_view(events, "week", ref, lang))
            ref += timedelta(days=7)
    else:
        ref = first
        while ref <= last and len(pages) < 62:
            pages.append(cal_view(events, "day", ref, lang))
            ref += timedelta(days=1)
    # Sunday-first columns: 0 = Sunday … 6 = Saturday; five days are Monday to Friday
    keep = [1, 2, 3, 4, 5] if view == "5day" or (view in ("week", "month") and not weekends) else list(range(7))
    for p in pages:
        p["dow"] = [p["dow"][i] for i in keep]
        p["weeks"] = [[w[i] for i in keep] for w in p["weeks"]]
        p["cols"] = len(keep)
    return pages


@app.get("/print", dependencies=[Depends(gui_auth)])
def print_page(request: Request, view: str = "", start: str = "", end: str = "", weekends: str = "",
               theme: str = ""):
    """Print Preview's page: the calendar as chosen, ready to print (the preview shows it in a frame)."""
    prefs = print_prefs()
    view = view if view in PRINT_VIEWS else prefs.get("view") or {"list": "itinerary"}.get(ui_view(), ui_view())
    today = now().astimezone(display_tz()).date()
    first = _parse_day(start, None) if start else today.replace(day=1)
    last = _parse_day(end, None) if end else first.replace(day=pycal.monthrange(first.year, first.month)[1])
    if last < first:
        first, last = last, first
    last = min(last, first + timedelta(days=731))
    lang = lang_for(request)
    weekends_on = weekends == "1" if weekends else prefs.get("weekends", True)
    return page(request, "print.html", {
        "pages": print_pages(store.load_events(), view, first, last, weekends_on, lang), "view": view,
        "first": first, "last": last, "print_theme": theme if theme in ("light", "dark") else prefs.get("theme", "light"),
        "src_names": {sid: calendar_name(sid) for sid in source_ids()}}, lang=lang)


@app.post("/ui/theme", dependencies=[Depends(gui_auth)])
async def set_theme(csrf: str = Form(""), theme: str = Form("")):
    """Remember the light / dark / system choice (the page sends this when it's changed)."""
    check_csrf(csrf)
    if theme not in THEMES:
        raise HTTPException(400, "Unknown theme.")
    store.set("ui_theme", theme)
    return Response(status_code=204)


# --- Edit and add events --------------------------------------------------

def _back(month: str | None) -> str:
    y, m = _parse_month(month)
    return f"/?month={y}-{m:02d}#cal"


def united_original(uid: str, sid: str = "ccs") -> Event | None:
    """The source's own version of an event, from its last download (United's, for CCS+)."""
    found = store.get_calendar(skey(sid, "source"))
    if not found:
        return None
    base, _ = preview(sid, found[0])
    return next((e for e in base if e.uid == uid), None)


def _form_values(e: Event, start_tz: ZoneInfo | None = None, end_tz: ZoneInfo | None = None, clock=None) -> dict:
    """Split an event into the edit form's fields (end date shown inclusive). Times are given as
    "HH:MM" and as shown on the page (`clock`: 12- or 24-hour), each in its own time zone."""
    start_tz = start_tz or display_tz()
    end_tz = end_tz or start_tz
    clock = clock or (lambda dt: f"{dt:%H:%M}")
    if e.all_day:
        first = date.fromisoformat(e.start[:10])
        last = max(first, date.fromisoformat(e.end[:10]) - timedelta(days=1))
        s_ = datetime.combine(first, datetime.min.time().replace(hour=9))
        t_ = datetime.combine(last, datetime.min.time().replace(hour=10))
    else:
        s_, t_ = datetime.fromisoformat(e.start).astimezone(start_tz), datetime.fromisoformat(e.end).astimezone(end_tz)
    return {"start_date": f"{s_:%Y-%m-%d}", "start_time": f"{s_:%H:%M}", "start_label": clock(s_),
            "end_date": f"{t_:%Y-%m-%d}", "end_time": f"{t_:%H:%M}", "end_label": clock(t_)}


def _saved_zones(uid: str) -> tuple[str, str]:
    """The time zones an event was last saved with on the event page, if any."""
    data = store.get_edits().get(uid) or next((c for c in store.get_customs() if c["uid"] == uid), None) or {}
    start = data.get("start_tz") if valid_zone(data.get("start_tz") or "") else ""
    end = data.get("end_tz") if valid_zone(data.get("end_tz") or "") else ""
    return start, end or start


@app.get("/event", dependencies=[Depends(gui_auth)])
def edit_event(request: Request, uid: str = "", date_: str = Query("", alias="date"), month: str | None = None,
               copy: str = "", embed: str = ""):
    """The event page: edit an event (uid), add one on `date`, or add a copy of one (`copy`). With
    `embed`, it's shown in a pop-up on the status page (0.2.8: on a computer; a phone opens the page)."""
    if copy:
        found = store.get_event(copy)
        if not found:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        if not source_ids():
            raise HTTPException(400, "Add a calendar source first (Calendar Sources → +).")
        e = Event(title=found.title, start=found.start, end=found.end, all_day=found.all_day, location=found.location,
                  description=found.description, origin="custom", color=found.color,
                  source=found.source if found.source in source_ids() else source_ids()[0])
        uid = ""
    elif uid:
        e = store.get_event(uid)
        if not e:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        if e.origin == "rule":
            raise HTTPException(400, "This event is made by a rule; change the rule or its event template instead.")
    else:   # new event on a given day
        if not source_ids():
            raise HTTPException(400, "Add a calendar source first (Calendar Sources → +).")
        try:
            day = date.fromisoformat(date_)
        except ValueError:
            day = now().date()
        e = Event(title="", start=day.isoformat(), end=(day + timedelta(days=1)).isoformat(), all_day=False,
                  origin="custom", source=source_ids()[0])       # the default calendar: the top one
        e.start = datetime.combine(day, datetime.min.time().replace(hour=9), display_tz()).isoformat()
        e.end = datetime.combine(day, datetime.min.time().replace(hour=10), display_tz()).isoformat()
    original = united_original(uid, e.source) if e.origin == "united" and uid else None
    lang = lang_for(request)
    tag_color = e.rule_color
    start_zone, end_zone = _saved_zones(uid) if uid else ("", "")
    start_zone, end_zone = start_zone or display_zone(), end_zone or start_zone or display_zone()
    return page(request, "event.html", {
        "e": e, "f": _form_values(e, ZoneInfo(start_zone), ZoneInfo(end_zone), dates_for(lang).clock),
        "start_zone": start_zone, "end_zone": end_zone, "zones": ALL_ZONES, "common_zones": COMMON_ZONES,
        "is_new": not uid, "original": original,
        "colors": GOOGLE_COLORS.values(), "auto_color": tag_color or calendar_color(e.source) or "",
        "sources": [{"id": sid, "name": calendar_name(sid), "type": (source(sid) or {}).get("type")} for sid in source_ids()],
        "is_copy": bool(copy), "trash": TRASH_ICON, "copy_icon": COPY_ICON,
        "src_type": (source(e.source) or {}).get("type", "ccs"), "src_name": calendar_name(e.source),
        "templates": [{**t, "length": show_duration(t["minutes"])} for t in event_templates()],
        "original_range": _range_text(original, *_span(original)[2:], lang) if original else "",
        "csrf": CSRF_TOKEN, "month": month or (e.start[:7]), "tz": display_zone(), "embed": embed == "1",
        "default_sid": (source_ids() or [""])[0],
        "link": event_links().get(uid) if uid else None, "link_choices": link_choices(e, uid, lang),
    }, lang=lang)


def link_choices(e: Event, uid: str, lang: str) -> list[dict]:
    """The events an event can be linked to (F3.2): those within three weeks of it, in every calendar."""
    try:
        day = date.fromisoformat(e.start[:10])
    except ValueError:
        return []
    first, last = (day - timedelta(days=21)).isoformat(), (day + timedelta(days=22)).isoformat()
    d = dates_for(lang)
    names = {sid: calendar_name(sid) for sid in source_ids()}
    out = []
    for x in sorted(store.load_events(), key=lambda x: x.start):
        if x.uid == uid or x.origin == "rule" or x.hidden or not (first <= x.start[:10] < last):
            continue
        when = d.day(date.fromisoformat(x.start[:10])) + ("" if x.all_day else " " + d.clock(datetime.fromisoformat(x.start).astimezone(display_tz())))
        out.append({"uid": x.uid, "label": f"{when} · {x.title}", "calendar": names.get(x.source, "")})
    return out[:300]


def linked_titles() -> dict[str, str]:
    """{event ID: the title of the event it's linked to}, for the calendar's event details."""
    out = {}
    for uid, link in event_links().items():
        other = store.get_event(link["to"])
        if other:
            out[uid] = other.title
    return out


def save_link(uid: str, to: str, delete: bool, move: bool):
    """Link an event to another one (or unlink it, with no `to`)."""
    found = event_links()
    other = store.get_event(to) if to and to != uid else None
    if other is None:
        found.pop(uid, None)
    else:
        found[uid] = {"to": other.uid, "src": other.source, "at": other.start, "delete": delete, "move": move}
    store.set("event_links", found)


def _event_back(month: str, embed: str) -> RedirectResponse:
    """After the event page: back to the calendar, or (in the pop-up) a page that tells it to close."""
    return RedirectResponse("/event/done" if embed == "1" else _back(month), status_code=303)


@app.get("/event/done", dependencies=[Depends(gui_auth)])
def event_done():
    """Shown in the event pop-up after a save: it tells the status page to close the pop-up and
    bring the calendar up to date."""
    html = ("<!doctype html><meta charset=utf-8><title>Saved</title>"
            "<script>parent.postMessage('calendarstream:event-saved', location.origin)</script>")
    return Response(html, media_type="text/html")


EVENT_COLORS = {hex_ for _, hex_ in GOOGLE_COLORS.values()}   # Google's 11 event colors

# Icons for the event tools (Material Symbols): a bin to delete, two sheets to duplicate.
TRASH_ICON = icons.svg("delete", 17)
COPY_ICON = icons.svg("content_copy", 17)


CLOCK_RE = re.compile(r"^\s*(\d{1,2})(?:[:.h]?(\d{2}))?\s*(?:([ap])\.?\s*m?\.?)?\s*$", re.I)


def parse_clock(text: str) -> str:
    """A time as typed on the event page, as "HH:MM": "9:30", "9:30pm", "930", "21:30", "2130",
    "9 pm", "9h30". Raises ValueError when it isn't a time."""
    m = CLOCK_RE.match(text or "")
    if not m:
        raise ValueError(text)
    digits, minute, ampm = m.group(1), m.group(2), (m.group(3) or "").lower()
    if minute is None and len(digits) > 2:          # "930" → 9:30 (handled by the regex as 9 + 30)
        raise ValueError(text)
    h, mi = int(digits), int(minute or 0)
    if ampm:
        if not 1 <= h <= 12:
            raise ValueError(text)
        h = h % 12 + (12 if ampm == "p" else 0)
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ValueError(text)
    return f"{h:02d}:{mi:02d}"


def _event_from_form(title, all_day, start_date, start_time, end_date, end_time, location, description,
                     color: str = "", start_tz: str = "", end_tz: str = "") -> dict:
    title = " ".join((title or "").split())
    color = (color or "").lower()
    if color and color not in EVENT_COLORS:
        raise HTTPException(400, "Choose one of the colors offered.")
    if not title:
        raise HTTPException(400, "The event needs a title.")
    try:
        sd, ed = date.fromisoformat(start_date), date.fromisoformat(end_date or start_date)
        if all_day:
            if ed < sd:
                raise HTTPException(400, "The last day is before the first day.")
            start, end = sd.isoformat(), (ed + timedelta(days=1)).isoformat()
        else:
            stz = ZoneInfo(start_tz) if valid_zone(start_tz) else display_tz()
            etz = ZoneInfo(end_tz) if valid_zone(end_tz) else stz
            s_ = datetime.combine(sd, datetime.strptime(parse_clock(start_time or "0:00"), "%H:%M").time(), stz)
            t_ = datetime.combine(ed, datetime.strptime(parse_clock(end_time or "0:00"), "%H:%M").time(), etz)
            if t_ <= s_:
                raise HTTPException(400, "The end has to be after the start.")
            start, end = s_.isoformat(), t_.isoformat()
    except ValueError:
        raise HTTPException(400, "Check the dates and times.")
    return {"title": title[:200], "start": start, "end": end, "all_day": bool(all_day),
            "location": (location or "").strip()[:200], "description": (description or "").strip()[:4000],
            "color": color,
            # remembered so the event page opens in the same time zones next time
            "start_tz": start_tz if valid_zone(start_tz) else "", "end_tz": end_tz if valid_zone(end_tz) else ""}


@app.post("/event/save", dependencies=[Depends(gui_auth)])
async def save_event(csrf: str = Form(""), uid: str = Form(""), month: str = Form(""), title: str = Form(""),
                     all_day: str = Form(""), start_date: str = Form(""), start_time: str = Form(""),
                     end_date: str = Form(""), end_time: str = Form(""), location: str = Form(""),
                     description: str = Form(""), hidden: str = Form(""), color: str = Form(""),
                     start_tz: str = Form(""), end_tz: str = Form(""), end_tz_differs: str = Form(""),
                     source_: str = Form("", alias="source"), embed: str = Form(""), link_to: str = Form(""),
                     link_delete: str = Form(""), link_move: str = Form("")):
    """Save the event page: an edit of a source's event, or an added event (into `source`). end_tz is
    only used when "The end is in a different time zone" is ticked."""
    check_csrf(csrf)
    end_tz = end_tz if end_tz_differs else start_tz      # one time zone for both unless asked otherwise
    data = _event_from_form(title, all_day, start_date, start_time, end_date, end_time, location, description,
                            color, start_tz, end_tz)
    current = store.get_event(uid) if uid else None
    if current and current.origin == "rule":
        raise HTTPException(400, "This event is made by a rule; change the rule or its event template instead.")
    if current and current.origin == "united":
        original = united_original(uid, current.source)
        if not original:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        unchanged = not hidden and uid not in store.get_edits() and all(
            data[k] == getattr(current, k) for k in ("title", "start", "end", "all_day", "location", "description", "color"))
        if not unchanged:       # (only its link changed: it isn't marked as edited)
            store.set_edit(uid, {**data, "hidden": bool(hidden), "base": original.fingerprint()})
            state.record("info", f"Edited \"{original.title}\" ({original.start[:10]})"
                         + (" and hid it from Google" if hidden else ""))
        sid = current.source
        save_link(uid, link_to, bool(link_delete), bool(link_move))
    else:
        sid = current.source if current else (source_ if source_ in source_ids() else (source_ids() or [""])[0])
        if sid not in source_ids():
            raise HTTPException(400, "Add a calendar source first (Calendar Sources → +).")
        new_uid = uid if current else f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(new_uid, {**data, "source": sid})
        save_link(new_uid, link_to, bool(link_delete), bool(link_move))
        state.record("info", f"{'Updated' if current else 'Added'} \"{data['title']}\" ({data['start'][:10]})")
    rebuild(sid)
    state.save()
    return _event_back(month or data["start"][:7], embed)


@app.post("/event/revert", dependencies=[Depends(gui_auth)])
async def revert_event(csrf: str = Form(""), uid: str = Form(""), month: str = Form(""), embed: str = Form("")):
    check_csrf(csrf)
    e = store.get_event(uid)
    store.delete_edit(uid)
    rebuild(e.source if e else None)
    state.record("info", "Reverted an event to United's version")
    return _event_back(month, embed)


ALARM_CHOICES = (0, 5, 10, 15, 30, 60, 120, 1440, 2880, 10080)    # minutes before the start


@app.post("/event/alarms", dependencies=[Depends(gui_auth)])
async def set_alarms(request: Request, csrf: str = Form(""), uid: str = Form(""), minutes: list[str] = Form([]),
                     month: str = Form("")):
    """An event's reminders (the bell on an event): sent to Google (up to five) and written into the feeds.
    Kept by event, so they stay through new downloads and edits."""
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e:
        raise HTTPException(404, "That event isn't in the current schedule any more.")
    chosen = sorted({int(m) for m in minutes if m.isdigit() and int(m) in ALARM_CHOICES})[:5]
    saved = event_alarms()
    if chosen:
        saved[uid] = ",".join(map(str, chosen))
    else:
        saved.pop(uid, None)
    store.set("event_alarms", saved)
    rebuild(e.source)
    state.record("info", f"Reminders for \"{e.title}\" ({e.start[:10]}): "
                 + (", ".join(alarm_text(m) for m in chosen) if chosen else "none"))
    return {"ok": True} if _is_async(request) else RedirectResponse(_back(month), status_code=303)


def alarm_text(minutes: int, lang: str = "en") -> str:
    """e.g. "at the start", "15 min before", "1 day before"."""
    tr = lambda text, **kw: str(i18n.tr(lang, text, **kw))
    if minutes == 0:
        return tr("at the start")
    for size, one, many in ((10080, "1 week before", "{n} weeks before"), (1440, "1 day before", "{n} days before"),
                            (60, "1 hour before", "{n} hours before")):
        if minutes % size == 0:
            return tr(one) if minutes == size else tr(many, n=minutes // size)
    return tr("{n} min before", n=minutes)


@app.post("/event/delete", dependencies=[Depends(gui_auth)])
async def delete_event(request: Request, csrf: str = Form(""), uid: str = Form(""), month: str = Form(""),
                       embed: str = Form("")):
    """Delete an event (the bin on an event). One added here is deleted; a source's own event would
    come back with the next download, so it's hidden from every destination instead (Edit → untick
    Hide brings it back)."""
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e:
        raise HTTPException(404, "That event isn't in the current schedule any more.")
    if e.origin == "rule":
        raise HTTPException(400, "This event is made by a rule; change the rule or its event template instead.")
    if e.origin == "custom":
        store.delete_custom(uid)
        state.record("info", f"Deleted \"{e.title}\" ({e.start[:10]})")
    else:
        if not united_original(uid, e.source):
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        _hide(e)
        state.record("info", f"Hid \"{e.title}\" ({e.start[:10]}) from the destinations")
    rebuild(e.source)
    if _is_async(request):
        return {"ok": True}
    return _event_back(month, embed)


MAX_UPLOAD = 5 * 1024 * 1024


@app.post("/setup/upload", dependencies=[Depends(gui_auth)])
async def upload(csrf: str = Form(""), file: UploadFile = File(...)):
    """Publish a Calendar.ics downloaded by hand from CCS+ (United's own Google Calendar procedure)."""
    check_csrf(csrf)
    _sid("ccs")
    body = await file.read(MAX_UPLOAD + 1)
    if len(body) > MAX_UPLOAD:
        raise HTTPException(413, "That file is too large for a schedule (over 5 MB).")
    try:
        check_calendar(body)
        store.save_debug("source", body, "text/calendar; charset=utf-8")
        store.delete("http_cache")   # the next automatic download fetches the full file again
        state.last_attempt = now()
        apply_calendar(body, "uploaded by hand")
    except SourceError as e:
        state.record("error", f"Upload rejected: {e}")
        raise HTTPException(400, str(e))
    finally:
        state.save()
    return RedirectResponse("/#src-ccs", status_code=303)


# --- Public address (Settings) ---------------------------------------------------

@app.post("/settings/public-url", dependencies=[Depends(gui_auth)])
async def set_public_url(csrf: str = Form(""), url: str = Form(""), action: str = Form("save")):
    """Save the public address (Settings menu); empty removes it. It's used for the feed and subscribe
    links and Google's sign-in redirect."""
    check_csrf(csrf)
    if not url.strip():
        store.delete("public_url")
        state.record("info", "Public address removed")
    else:
        try:
            value = normalise_public_url(url)
        except ValueError:
            raise HTTPException(400, "Enter the address people use to reach this page, e.g. https://cal.example.com")
        store.set("public_url", value)
        state.record("info", f"Public address set to {value}")
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


# --- Admin e-mail (Settings) -------------------------------------------------------

EMAIL_RE = re.compile(r"^[^@\s<>\"']{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")


def admin_email() -> str:
    """The administrator's e-mail address (☰ Settings), or "". Shown in the Google setup guide as
    the support / contact e-mail and the test user. Checked again on the way out (it goes into the page)."""
    email = str(store.get("admin_email") or "")
    return email if EMAIL_RE.match(email) and len(email) <= 254 else ""


@app.post("/settings/admin-email", dependencies=[Depends(gui_auth)])
async def set_admin_email(csrf: str = Form(""), email: str = Form("")):
    check_csrf(csrf)
    email = email.strip()
    if not email:
        store.delete("admin_email")
        state.record("info", "Admin e-mail removed")
    elif not EMAIL_RE.match(email) or len(email) > 254:
        raise HTTPException(400, "That doesn't look like an e-mail address.")
    else:
        store.set("admin_email", email)
        state.record("info", f"Admin e-mail set to {email}")
    return RedirectResponse("/?menu=settings#admin", status_code=303)


# --- Google Calendar connection ---------------------------------------------------

@app.post("/google/client", dependencies=[Depends(gui_auth)])
async def google_client(request: Request, csrf: str = Form(""), client_id: str = Form(""),
                        client_secret: str = Form(""), action: str = Form("save"), back: str = Form("")):
    """Save or remove the Google OAuth client (Google Calendar Autosync box). The secret is stored encrypted and
    never shown again. It can't change while connected: the sign-in belongs to that client."""
    check_csrf(csrf)
    if google.connected:
        raise HTTPException(400, "Disconnect Google Calendar before changing the OAuth client.")
    if action == "remove":
        google.clear_client()
        state.record("info", "Google OAuth client removed")
    elif action == "check":
        if google.configured:
            await google.check_client(google_redirect_uri(request))
    else:
        try:
            google.save_client(client_id, client_secret)
        except GoogleError as e:
            raise HTTPException(400, str(e))
        google.record_error("")
        if _is_async(request):
            state.record("info", f"Google OAuth client saved ({google.client_id.split('.')[0][:12]}…)")
            return JSONResponse({"saved": True})      # the page then asks /verify
        check = await google.check_client(google_redirect_uri(request))
        state.record("info" if check["ok"] else "warn",
                     f"Google OAuth client saved ({google.client_id.split('.')[0][:12]}…): {check['message']}")
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


@app.post("/google/connect", dependencies=[Depends(gui_auth)])
async def google_connect(request: Request, csrf: str = Form("")):
    """Send the browser to Google's consent page."""
    check_csrf(csrf)
    view = google_view(request)
    if not view["configured"]:
        raise HTTPException(400, "Save the Google OAuth client ID and secret first.")
    if not view["redirect_ok"]:
        raise HTTPException(400, "Set the public address (Settings → Public address) to this page's https:// address first.")
    return RedirectResponse(google.sign_in_url(view["redirect_uri"]), status_code=303)


@app.get("/google/callback", dependencies=[Depends(gui_auth)])
async def google_callback(state_: str = Query("", alias="state"), code: str = "", error: str = ""):
    """Google sends the browser back here after the consent page, with a one-time code."""
    try:
        if error or not code:
            raise GoogleError("Google sign-in was cancelled or refused. If Google said the app is only for "
                              "testers, add your Gmail address under Audience → Test users in Google Cloud."
                              if error in ("access_denied", "") else f"Google sign-in failed: {error[:80]}.")
        async with google_job.lock:      # no sync may start while the calendars are being found or made
            info = await google.finish_sign_in(state_, code)
            found = []
            for d in destinations("google"):     # each Google destination's calendar: the one from before, or a new one
                await google.ensure_calendar(d["id"], d["name"])
                cal = google.cal_info(d["id"])
                found.append(f"calendar \"{cal.get('calendar_name', '')}\" "
                             + ("created" if cal.get("created") else "found again"))
        state.record("info", f"Google Calendar connected as {info.get('email') or 'your account'}"
                     + "".join("; " + f for f in found))
        request_google_sync(full=True)
    except GoogleError as e:
        google.record_error(str(e))
        state.record("error", f"Google: {e}")
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


@app.post("/google/disconnect", dependencies=[Depends(gui_auth)])
async def google_disconnect(csrf: str = Form(""), delete: str = Form("")):
    """Stop syncing: optionally delete CalendarStream's calendar, then remove its access in Google."""
    check_csrf(csrf)
    if not google.connected:
        return RedirectResponse(GOOGLE_SETTINGS, status_code=303)
    email = google.info().get("email") or "your account"
    async with google_job.lock:      # not in the middle of a sync
        await google.stop_watch(sorted({d["id"] for d in destinations("google")} | set(google.calendar_sids())))
        notes = await google.disconnect(delete_calendar=delete == "1")
    if delete == "1":
        store.google_forget()
    what = "and its calendar deleted" if delete == "1" and not any("calendar" in n for n in notes) else ""
    state.record("warn" if notes else "info", f"Google Calendar disconnected ({email}) {what}".strip()
                 + ("; " + "; ".join(notes) if notes else ""))
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


@app.post("/google/notify")
async def google_notify(request: Request):
    """Google's change notification for CalendarStream's calendar (no login: Google can't sign in).
    Checked by the channel ID and the secret token CalendarStream gave Google; it carries no
    details, so it just starts a check that puts back events changed or deleted in Google."""
    channel = request.headers.get("x-goog-channel-id", "")
    sid = google.notice_from(channel, request.headers.get("x-goog-channel-token", ""), [d["id"] for d in destinations("google")])
    if sid:
        if request.headers.get("x-goog-resource-state") != "sync":   # "sync" only confirms the channel
            google.noticed(sid)
            request_google_sync(full=True)
    return Response(status_code=200)   # anything else makes Google retry; unknown channels just expire


@app.post("/google/sync", dependencies=[Depends(gui_auth)])
async def google_sync_now(request: Request, csrf: str = Form("")):
    """Sync now, checking Google's copy too (repairs events changed or deleted in Google). From the
    page's script it answers at once, and the page follows it in /api/status (see /run)."""
    check_csrf(csrf)
    request_google_sync(full=True)
    await asyncio.sleep(0.5)
    if _is_async(request):
        return {"ok": True}
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


@app.get("/subscribe/{token}")
def subscribe(request: Request, token: str):
    """Shareable page (no status-page login needed); the secret token in the URL is the access control."""
    d = dest_for_token(token)
    if not d:
        raise HTTPException(404)
    # Shared with other people: shown in each visitor's browser language.
    lang = i18n.pick(None, request.headers.get("accept-language", ""))
    checked = [st(x).last_success for x in d["sources"] if st(x).last_success]
    return page(request, "subscribe.html", {
        "cfg": settings, "name": d["name"], "links": subscribe_links(request, d["token"]),
        "last_success": max(checked) if checked else None,
        "event_count": sum(1 for e in dest_events(d) if not e.hidden),
    }, lang=lang)


@app.get("/api/status", dependencies=[Depends(gui_auth)])
def api_status():
    """Machine-readable status for monitoring (status-page login)."""
    fmt = lambda d: d.isoformat() if d else None

    def one(sid: str) -> dict:
        S = st(sid)
        return {"id": sid, "name": calendar_name(sid), "type": (source(sid) or {}).get("type"), "status": S.status,
                "message": S.message, "running": S.running, "last_attempt": fmt(S.last_attempt),
                "last_success": fmt(S.last_success), "last_change": fmt(S.last_change), "next_run": fmt(S.next_run),
                "events": S.event_count}
    found = [one(sid) for sid in source_ids()]
    # The top-level fields are CCS+'s (as before 0.2), or the first source's.
    first = st("ccs") if "ccs" in source_ids() else (st(source_ids()[0]) if found else State("none"))
    return {"version": __version__, "status": first.status, "message": first.message, "running": first.running,
            "last_attempt": fmt(first.last_attempt), "last_success": fmt(first.last_success),
            "last_change": fmt(first.last_change), "last_auth": fmt(first.last_auth),
            "last_auth_ok": first.last_auth_ok, "next_run": fmt(first.next_run), "events": first.event_count,
            "sources": found,
            "destinations": [{k: d[k] for k in ("id", "type", "name", "sources")} for d in destinations()],
            # Google: a sync asked for (pending) or running, and whether the last one failed
            "google": {"connected": google.connected, "running": google_job.running, "pending": google_job.wake.is_set(),
                       "error": bool(google.info().get("last_error"))}}


def redact(text: str) -> str:
    """Take private details out of text for a problem report: the CCS+ username, feed links and
    stream names, the public address, e-mail addresses, the Google client ID and long secrets."""
    out = text or ""
    secrets_ = [logins.ccs()[0], public_url(), store.get("admin_email") or "", (google.client_id or "")]
    secrets_ += [x.get("url") or "" for x in sources()] + [d.get("token") or "" for d in destinations()]
    for value in sorted({v for v in secrets_ if v and len(v) >= 3}, key=len, reverse=True):
        out = out.replace(value, "[private]")
    out = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[e-mail]", out)
    out = re.sub(r"(?i)(password|secret|token|authorization|cookie)([\"']?\s*[:=]\s*)\S+", r"\1\2[private]", out)
    return re.sub(r"\b[A-Za-z0-9_-]{32,}\b", "[private]", out)


@app.get("/report/data", dependencies=[Depends(gui_auth)])
def report_data():
    """What Report a problem can attach, private details taken out: the recent Activities and Logs
    lines, each source's last download details, and this install's setup. The page shows it in the
    report's preview; nothing is sent anywhere from here."""
    lines = [f"{h['time'].astimezone(TZ):%Y-%m-%d %H:%M:%S} {h['level']:5} {h['msg']}" for h in store.recent_log(60)]
    found = []
    for sid in source_ids():
        S, debug = st(sid), store.get_debug(skey(sid, "response"))
        found.append({"id": sid, "name": calendar_name(sid), "type": (source(sid) or {}).get("type"),
                      "status": f"{S.status}: {S.message}",
                      "debug": redact(debug[0].decode("utf-8", "replace") if debug else "")[:6000]})
    return {"version": __version__, "image_tag": os.environ.get("IMAGE_TAG") or "latest", "channel": release_channel(),
            "server": f"Python {platform.python_version()} on {platform.system()} {platform.machine()}",
            "time_zone": settings.timezone, "sources": [{**x, "status": redact(x["status"])} for x in found],
            "destinations": [d["type"] for d in destinations()], "google_connected": bool(google.connected),
            "updater": updater.ready, "activity": redact("\n".join(lines))}


@app.get("/debug/{name}", dependencies=[Depends(gui_auth)])
def debug_file(name: str):
    """The last download's response details or calendar file, for debugging (status-page login)."""
    ok = re.fullmatch(r"(source|response)(:f[0-9a-f]{6})?", name)
    found = store.get_debug(name) if ok else None
    if not found:
        raise HTTPException(404)
    content, content_type = found
    if name.startswith("source"):   # show it in the browser rather than downloading
        content_type = "text/plain; charset=utf-8"
    return Response(content, media_type=content_type)


@app.get("/calendar/{token}.ics")
def calendar(token: str, request: Request):
    """The published .ics feed. The token in the address is the only protection (it's secret)."""
    d = dest_for_token(token)
    if not d:
        raise HTTPException(404)
    note_feed_read(request.headers.get("user-agent", ""), d["id"])
    color = calendar_color(d["sources"][0]) if len(d["sources"]) == 1 else ""
    ics = build_feed(dest_events(d), d["name"], settings.timezone, color)
    # An unchanged feed answers "304 Not Modified" (0.2.8-beta.4): calendar apps that ask with the tag
    # they were given last time don't download it all again.
    tag = '"' + hashlib.sha256(ics).hexdigest()[:32] + '"'
    headers = {"Cache-Control": "no-cache", "ETag": tag}
    if tag in [t.strip() for t in request.headers.get("if-none-match", "").split(",")]:
        return Response(status_code=304, headers=headers)
    return Response(ics, media_type="text/calendar; charset=utf-8", headers=headers)


@app.get("/healthz")
def health():
    try:
        store.event_count()
    except Exception as e:
        log.warning("Health check: database unavailable: %s", e)
        raise HTTPException(503, "database unavailable")
    return {"ok": True}
