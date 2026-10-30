"""Web app: status page, month view, .ics feed, and the background loops (CCS+ downloads,
Google sync, update checks)."""
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
from .calsync import (AuthError, BlockedError, Defaults, Event, SourceError, apply_changes, build_feed,
                      download, parse, parse_feed)
from .config import normalise_public_url, settings
from .gsync import GOOGLE_COLORS, Google, GoogleError, nearest_color_id
from .logins import Logins
from .secretbox import SecretBox
from .store import Store, from_iso, iso
from .updates import FREQUENCIES, RELEASES, Updater, UpdaterError, Updates, channel as release_channel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("calendar_stream")
logging.getLogger("httpx").setLevel(logging.WARNING)   # one line per Google request is too chatty


class _LogTail(logging.Handler):
    """The container's log as it's written (what `docker logs` shows for this app), kept in memory for
    History › Container log (0.2.8-beta.15): the last LOG_TAIL_LINES lines."""
    def __init__(self, keep: int):
        super().__init__()
        self.lines: deque[str] = deque(maxlen=keep)
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

    def emit(self, record):
        try:
            self.lines.append(self.format(record))
        except Exception:  # noqa: BLE001 - a line that can't be formatted is reported the logging way, never raised
            self.handleError(record)


LOG_TAIL_LINES = 3000
LOG_TAIL = _LogTail(LOG_TAIL_LINES)


def tail_logs():
    """Keep the log lines from here on (called at start-up, once uvicorn has set up its own loggers):
    the app's (the root logger) and uvicorn's, which don't pass theirs up."""
    for name in ("", "uvicorn", "uvicorn.access"):
        logger = logging.getLogger(name)
        if LOG_TAIL not in logger.handlers and (not name or not logger.propagate):
            logger.addHandler(LOG_TAIL)
TZ = ZoneInfo(settings.timezone)
store = Store(settings.dsn)
box = SecretBox(settings.db_password)
google = Google(store, box, settings.timezone)        # the first Google account (connected in Settings)
ACCOUNT_RE = re.compile(r"^(|a[0-9a-f]{6})$")
_accounts: dict[str, Google] = {"": google}


def google_for(account: str = "") -> Google:
    """A Google account's connection (0.2.8-beta.15: each Google module can use its own Gmail; they share
    the OAuth client). "" is the first one."""
    if account not in _accounts:
        _accounts[account] = Google(store, box, settings.timezone, account)
    return _accounts[account]


def dest_google(d: dict) -> Google:
    return google_for(d.get("account", ""))


def google_accounts() -> list[str]:
    """The accounts in use: the first, and any a Google module uses."""
    return list(dict.fromkeys([""] + [d.get("account", "") for d in destinations("google")]))


def _shared_grant(g: Google) -> bool:
    """Another account here is signed in with the same Gmail (0.2.8-beta.17, I5). Google keeps one grant per
    Gmail, so revoking this sign-in would sign the other out too: it's only forgotten here."""
    email = (g.info().get("email") or "").lower()
    return bool(email) and any(x is not g and x.connected and (x.info().get("email") or "").lower() == email
                               for x in [google_for(a) for a in google_accounts()])
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
                      "for": "google" if d["type"] == "feed" and d.get("for") == "google" else "",
                      # 0.2.8-beta.15: a Google module's account ("" = the first one, connected in Settings), whether it's
                      # 1-way (written by CalendarStream only; changes made in Google are put back), and its color
                      "account": str(d.get("account") or "") if ACCOUNT_RE.match(str(d.get("account") or "")) else "",
                      "oneway": bool(d.get("oneway")) and d["type"] == "google",
                      "color": str(d.get("color") or "").lower() if COLOR_RE.match(str(d.get("color") or "")) else "",
                      # 0.2.8-beta.17: its note (in the header's (i)), and a Calendar Feed's address (one of ☰ Settings')
                      "note": " ".join(str(d.get("note") or "").split())[:300],
                      "base": str(d.get("base") or "") if d["type"] == "feed" else ""})
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
    store.set("destinations", [{k: d.get(k, "") for k in ("id", "type", "name", "sources", "token", "start", "end", "for",
                                                          "account", "oneway", "color", "note", "base")} for d in found])


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
    name in brackets ("Color ■ (Tomato)"). A rule with a title also says what it does (0.2.8-beta.10):
    "Items without an end time → Change to all-day"."""
    text = rule_label(r, lang)
    colors = [a["color"] for a in r["actions"] if a["type"] == "color"]
    if r["title"] and r["actions"]:
        tr = lambda t, **kw: str(i18n.tr(lang, t, **kw))
        text += " → " + rules_mod.actions_text(r, tr, color_name, {t["id"]: t for t in event_templates()})
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
    """There's always a CalendarStream (local) calendar, and the top calendar (the default for events added
    here) is always one (0.2.8-beta.15; before, one was made once). A missing one is made, in every feed;
    if another kind is on top, the first CalendarStream calendar moves up."""
    found = sources()
    locals_ = [x for x in found if x.get("type") == "local"]
    if not locals_:
        sid = new_local()
        store.set("sources", [{"id": sid, "type": "local"}] + found)
        store.set(f"calendar_name:{sid}", "CalendarStream" if store.get("local_made") else "Local")
        save_destinations([{**d, "sources": [sid] + d["sources"]} for d in destinations()])
        store.set("local_made", True)
    elif found[0].get("type") != "local":
        store.set("sources", [locals_[0]] + [x for x in found if x is not locals_[0]])


def is_local(sid: str) -> bool:
    return (source(sid) or {}).get("type") == "local"


def last_local(sid: str) -> bool:
    """The only CalendarStream calendar left: it can be emptied, not removed."""
    return is_local(sid) and sum(1 for x in sources() if x.get("type") == "local") == 1


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
SECTIONS = {"status": True, "activity": False, "rules": False, "templates": False, "googlesync": False}


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

    def record(self, level: str, msg: str, kind: str = "", undo: dict | None = None, stack: bool = True) -> int | None:
        """Add a line to History (a feed source's lines start with its name). `kind` is its Type (worked out
        from the words when not given); `undo` makes it a change that can be undone (0.2.8-beta.15)."""
        if self.sid != "ccs":
            msg = f"{calendar_name(self.sid)}: {msg}"
        log.log({"warn": logging.WARNING, "error": logging.ERROR}.get(level, logging.INFO), msg)
        try:
            return store.add_log(level, msg, kind or log_kind(msg, self.sid), undo, stack)
        except Exception as e:
            log.error("Couldn't write activity log to the database: %s", e)
            return None

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


# --- History, Undo & Logs (0.2.8-beta.15) -------------------------------------------------------
# Every line has a Type. A change made on the page (a calendar, feed, rule, template or event) keeps what
# was there before and after it, so it can be undone, and then redone: a stack, newest first. The newest
# changes are kept (Settings › History: how many); older ones pop off, and what they kept is forgotten.

LOG_KINDS = ("Calendar", "Feed", "Rule", "Event", "Google", "Settings", "Update", "Sync")


def log_kind(msg: str, sid: str = "ccs") -> str:
    """A line's Type, from its words, for the lines that don't say."""
    m = msg.split(": ", 1)[1] if sid != "ccs" and ": " in msg else msg
    for kind, starts in (("Rule", ("Rule ", "Event templates")),
                         ("Calendar", ("Calendar source", "Default calendar", "Calendar settings", "Calendar Sync link", "Checks every",
                                       "Imported", "Emptied", "Moved ")),
                         ("Feed", ("Destination", "Feed link", "Stream name")),
                         ("Event", ("Added \"", "Updated \"", "Deleted \"", "Hid \"", "Edited \"", "Reminders for", "Reverted",
                                    "Restored \"")),
                         ("Google", ("Google",)),
                         ("Settings", ("Public address", "Admin e", "Status page", "Status-page", "Signed ")),
                         ("Update", ("Update", "Updating", "Auto-update", "Auto"))):
        if m.startswith(starts):
            return kind
    return "Sync"


# What each kind of module is: its (i), with the person's note after it (0.2.8-beta.15)
MODULE_ABOUT = {"local": "Only the events you add here. Goes into every feed.",
                "ccs": "Your United CCS+ schedule, downloaded with your Calendar Sync password.",
                "google": "A Google calendar, read from its secret iCal address.",
                "apple": "An Apple calendar, read from its public link.",
                "feed": "A calendar read from its link (.ics).",
                "gdest": "The same as Google 1-way Sync, and changes made in Google come back here.",
                "gdest1": "CalendarStream writes into a Google calendar within seconds, with rule colors and reminders.",
                "gfeed": "A link any calendar app subscribes to: Google, Apple, Outlook, or send it to someone.",
                "ffeed": "A link any calendar app subscribes to: Google, Apple, Outlook, or send it to someone.",
                "apioff": "Needs Google Calendar API Sync, which your admin turns on in ☰ Settings."}

SOURCE_BASES = ("calendar_name", "calendar_color", "calendar_tags", "rule_subs", "defaults", "note", "sync_interval",
                "http_cache", "status", "feed_reads")
UNDO_KEYS = ("sources", "destinations", "rules", "event_templates", "event_alarms", "event_links", "rule_conflicts_ignored")
UNDO_KEEP = 20          # changes remembered for Undo, unless Settings › History says otherwise


def undo_keep() -> int:
    n = store.get("undo_keep")
    return n if isinstance(n, int) and 1 <= n <= 200 else UNDO_KEEP


class Change:
    """A change that can be undone: what it touches is kept as it was (settings, and the whole of the
    calendars in `whole`), then as it is after; done() writes its History line.

        ch = Change(sids=[sid], whole=[sid]); …change things…; ch.done("Calendar", "Calendar source removed: Work")
    """
    def __init__(self, sids=(), whole=(), uids=()):
        keys = list(UNDO_KEYS)
        for sid in dict.fromkeys(sids):      # (its settings; `whole` adds its events, without its sign-in)
            keys += [skey(sid, b) for b in SOURCE_BASES] + (["ccs_login", "calendar_url"] if sid == "ccs" else [])
        self.keys, self.whole, self.uids = keys, list(whole), list(uids)
        self.before = store.snapshot(self.keys, self.whole, self.uids)

    def done(self, kind: str, msg: str) -> int | None:
        after = store.snapshot(self.keys, self.whole, self.uids)
        entry = state.record("info", msg, kind=kind, undo={"type": "snapshot", "before": self.before, "after": after})
        pop_undo()
        return entry


def pop_undo():
    """Drop what's kept for changes beyond the ones remembered (and finish their deletions)."""
    popped = store.trim_undo(undo_keep())
    if popped:
        finish_deletions()


def after_restore():
    """After an undo or redo: checks started or stopped for calendars that came or went, statuses read
    again, every calendar rebuilt."""
    ensure_local()
    ids = source_ids()
    for sid in list(source_tasks):
        if sid not in ids:
            stop_source(sid)
    for sid in store.event_sources():      # a calendar that's gone again (its adding undone): nothing of it is kept
        if sid not in ids:
            store.forget_source(sid)
    for sid in ids:
        states.pop(sid, None) if sid != "ccs" else state.load()
        start_source(sid)
    rebuild()


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
    d = destination(sid)
    g = dest_google(d) if d else google
    if not address or not g.connected or not g.watch_due(sid, address, now(), WATCH_RENEW, WATCH_RETRY):
        return
    before = g.watch_info(sid)
    had = bool(before.get("id")) or any(g.watch_info(x["id"]).get("id") for x in destinations("google") if x["id"] != sid)
    try:
        await g.start_watch(sid, address)
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


# --- Two-way sync (0.2.8-beta.10) -------------------------------------------------------
# Only the calendars CalendarStream makes in Google. A change made there becomes a change here, exactly
# like making it on the status page (CCS+ itself is never touched): an edit of a source's event is an
# edit, one of an added event changes it; an event added in Google goes into a CalendarStream (local)
# calendar; a deletion strikes the event through here (0.2.8-beta.15: Undo in History restores it). A
# rule's events stay read-only (put back). When both sides changed, the newest change wins.

_FIELDS = ("title", "start", "end", "all_day", "location", "description")


def google_held() -> dict:
    """{uid: {dest, title, start}}: events deleted in Google that waited for the person's choice (0.2.8-beta.10
    to beta.14; taken as deletions at the next sync since beta.15)."""
    found = store.get("google_pending_deletes")
    return found if isinstance(found, dict) else {}


def _same_time(a: str, b: str) -> bool:
    if a == b:
        return True
    try:
        return datetime.fromisoformat(a) == datetime.fromisoformat(b)
    except ValueError:
        return False


async def apply_google_changes(d: dict, changes: list[dict]) -> list[str]:
    """Make the changes found in a destination's Google calendar here. Returns the log lines."""
    lines, touched = [], set()
    customs = {c["uid"]: c for c in store.get_customs()}
    edits = store.get_edits()
    held = google_held()
    restoring = set(store.get("google_restoring") or [])       # "Put them back": not deletions any more
    def still_here(uid):
        e = store.get_event(uid)
        return e is not None and not e.hidden
    # Deleted in Google (0.2.8-beta.15): struck through here, in no other feed, with Undo (Restore) in History;
    # any held by an earlier version ("more than 3 at once wait for you") are taken the same way now
    deleted = [c for c in changes if c["kind"] == "deleted" and c["uid"] not in restoring and still_here(c["uid"])]
    deleted += [{"kind": "deleted", "uid": uid} for uid in held if still_here(uid) and uid not in {c["uid"] for c in deleted}]
    if held:
        store.delete("google_pending_deletes")
    gone = []
    for c in deleted:
        e = store.get_event(c["uid"])
        if e is None:
            continue
        if e.origin == "rule":
            lines.append(f"\"{e.title}\" is made by a rule, so it was put back")
            continue
        gone.append(e)
        touched.add(e.source)
    if gone:
        names = ", ".join(f"\"{e.title}\" ({e.start[:10]})" for e in gone[:5]) + (" …" if len(gone) > 5 else "")
        delete_events(gone, "google", f"Deleted in Google Calendar: {names}")
    for c in (c for c in changes if c["kind"] == "edited"):
        e = store.get_event(c["uid"])
        if e is None or c["uid"] in held:
            continue
        new = {k: c[k] for k in _FIELDS}
        if all((_same_time(new[k], getattr(e, k)) if k in ("start", "end") else new[k] == getattr(e, k)) for k in _FIELDS):
            continue                      # only its color or reminders changed there: put back
        if e.origin == "rule":
            lines.append(f"\"{e.title}\" is made by a rule, so Google's change was undone")
            continue
        local_at = store.changed_at(e.uid)
        try:
            remote_at = datetime.fromisoformat(c["at"].replace("Z", "+00:00"))
        except ValueError:
            remote_at = None
        if local_at and local_at > c["synced_at"] and (remote_at is None or local_at > remote_at):
            lines.append(f"\"{e.title}\" was changed here and in Google; the newer change, here, was kept")
            continue
        if e.origin == "custom" and e.uid in customs:
            store.set_custom(e.uid, {**customs[e.uid], **new})
        else:
            original = united_original(e.uid, e.source)
            if not original:
                continue
            base = edits.get(e.uid) or {"title": e.title, "start": e.start, "end": e.end, "all_day": e.all_day,
                                        "location": e.location, "description": e.description, "color": e.color,
                                        "base": original.fingerprint()}
            store.set_edit(e.uid, {**base, **new})
        lines.append(f"\"{new['title']}\" ({new['start'][:10]}) was changed in Google; the change is saved here")
        touched.add(e.source)
    locals_ = [sid for sid in d["sources"] if (source(sid) or {}).get("type") == "local"]
    told = set(store.get("google_left_alone") or [])        # events added in Google that can't come here: said once
    for c in (c for c in changes if c["kind"] == "created"):
        if c["repeats"] or not locals_:
            if c["gid"] not in told:
                lines.append(f"\"{c['title']}\" was added in Google, but " + ("repeating events can't be copied here yet" if c["repeats"]
                             else "this calendar gets no CalendarStream calendar to put it in") + "; it's left as it is in Google")
                told.add(c["gid"])
                store.set("google_left_alone", sorted(told)[-500:])
            continue
        uid = f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(uid, {**{k: c[k] for k in _FIELDS}, "color": "", "source": locals_[0]})
        await dest_google(d).delete_event(d["id"], c["gid"])    # it comes back as CalendarStream's own copy
        lines.append(f"\"{c['title']}\" ({c['start'][:10]}) was added in Google; it's now in {calendar_name(locals_[0])}")
        touched.add(locals_[0])
    for sid in touched:
        rebuild(sid)
    if touched:
        state.save()
    return lines


async def google_sync_once(full: bool) -> bool:
    """Run one sync of every Google module, account by account (0.2.8-beta.15). Returns False if one failed."""
    async with google_job.lock:
        dests = destinations("google")
        if not (google.configured and dests):
            return True
        google_job.running = True
        ok = True
        try:
            color_for = event_colorer()
            for account in google_accounts():
                mine = [d for d in dests if d["account"] == account]
                g = google_for(account)
                if mine and g.connected:
                    ok = await _sync_account(g, mine, len(dests), color_for, full) and ok
        finally:
            google_job.running = False
        return ok


COLOR_TRY = 2    # (0.2.8-beta.19) a refused color is tried once per color and per COLOR_TRY


async def _sync_account(g: Google, dests: list[dict], total: int, color_for, full: bool) -> bool:
    try:
        for d in dests:
            first = date.fromisoformat(d["start"]) if d.get("start") else EARLIEST
            who = "Google" if total == 1 else f"Google, {d['name']}"
            if full and not d["oneway"]:    # two-way: what changed in Google comes here first (0.2.8-beta.10)
                for line in await apply_google_changes(d, await g.pull(d["id"], first)):
                    state.record("info", f"{who}: {line}")
            result = await g.sync(d["id"], dest_events(d), d["name"], color_for, first, full,
                                  hold=frozenset(google_held()))
            if full and store.get("google_restoring"):
                store.set("google_restoring", [])      # put back in Google by this sync
            if result.changed or result.notes:
                state.record("info", f"{who}: {result.summary()}" + ("; " + "; ".join(result.notes) if result.notes else ""))
            info = g.cal_info(d["id"])
            # (0.2.8-beta.19, I1) tried again once after updating, so History gets Google's own reason for a refusal
            tried = info.get("color_tried") == d["color"] and info.get("color_try") == COLOR_TRY
            if d["color"] and info.get("color") != d["color"] and not tried:   # its color box (0.2.8-beta.15)
                # (0.2.8-beta.18, I4) tried once per color: Google refusing it is said once and never makes the
                # module's sync a "Sync problem" (before, it failed after every successful sync)
                try:
                    await g.set_color(d["id"], d["color"])
                    state.record("info", f"{who}: color set in Google Calendar", kind="Google")
                except GoogleError as e:
                    g._update_cal(d["id"], color_tried=d["color"], color_try=COLOR_TRY)
                    state.record("warn", f"{who}: the calendar's color couldn't be set in Google Calendar ({e}); "
                                 "set it there by hand if you like", kind="Google")
            _remember_calendar(d["id"], g)
            await ensure_watch(d["id"])
        return True
    except GoogleError as e:
        message = str(e)
    except Exception as e:      # keep the loop alive whatever happens
        message = f"Google sync failed: {type(e).__name__}: {e}"
    if message != g.info().get("last_error"):   # log each new problem once
        state.record("error", f"Google: {message}")
    g.record_error(message)
    return False


def _remember_calendar(did: str, g: Google):
    """(0.2.8-beta.18, I5) The Google calendar a module writes to, kept apart from its sign-in: a module that
    connects again (a new sign-in, the same Gmail) finds it and uses it again, instead of making a second one."""
    cid = g.cal_info(did).get("calendar_id")
    found = store.get("google_calendar_ids") or {}
    if cid and found.get(did) != cid:
        store.set("google_calendar_ids", {**found, did: cid})


def _remembered_calendar(did: str) -> str | None:
    return (store.get("google_calendar_ids") or {}).get(did)


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


# --- Deleted events (0.2.8-beta.15) -------------------------------------------------------------------
# A deleted event stays on the page, struck through and greyed, saying where it was deleted, until its
# Undo pops off History; it's in no feed meanwhile. Undo (Restore) brings it back. After that it's gone:
# an added event for good, a source's event hidden (its source would only send it again).

DELETED_WHERE = {"calendarstream": "Deleted in CalendarStream", "google": "Deleted in Google Calendar",
                 "united": "Removed by United (CCS+)", "feed": "Gone from the feed"}


def mark_deleted(e: Event, where: str):
    """Delete an event, keeping it struck through (see above)."""
    stamp = f"{where}|{now().isoformat(timespec='seconds')}"
    if e.origin == "custom":
        c = next((x for x in store.get_customs() if x["uid"] == e.uid), None)
        if c:
            store.set_custom(e.uid, {k: v for k, v in c.items() if k != "uid"} | {"deleted": stamp})
        return
    had_edit = e.uid in store.get_edits()
    _hide(e)
    ed = store.get_edits().get(e.uid)
    if ed:
        store.set_edit(e.uid, {**ed, "hidden": True, "deleted": stamp, **({} if had_edit else {"for_delete": True})})


def unmark_deleted(uid: str):
    """Undo a delete: the event is back, as it was."""
    c = next((x for x in store.get_customs() if x["uid"] == uid), None)
    if c:
        store.set_custom(uid, {k: v for k, v in c.items() if k not in ("uid", "deleted")})
        return
    ed = store.get_edits().get(uid)
    if ed and ed.get("for_delete"):
        store.delete_edit(uid)
    elif ed:
        store.set_edit(uid, {k: v for k, v in ed.items() if k not in ("deleted",)} | {"hidden": False})
    store.google_forget(uid)        # it's written to Google again


def delete_events(found: list[Event], where: str, msg: str) -> int | None:
    """Delete events (kept struck through) as one change that can be undone. Deleted outside CalendarStream
    (in Google), it's Restore on each event instead: no Undo on the stack, which is for changes made here."""
    for e in found:
        mark_deleted(e, where)
    entry = state.record("info", msg, kind="Google" if where == "google" else "Event",
                         undo={"type": "deleted", "where": where, "uids": [e.uid for e in found]}, stack=where == "calendarstream")
    pop_undo()
    return entry


def finish_deletions():
    """Deleted events whose Undo has popped off: an added one goes for good; a source's stays hidden
    and is no longer shown ("gone")."""
    live = {uid for undo in store.undo_payloads("deleted") for uid in undo["uids"]}
    touched = set()
    for c in store.get_customs():
        if c.get("deleted") and c["uid"] not in live:
            store.delete_custom(c["uid"])
            touched.add(c.get("source", "ccs"))
    for uid, ed in store.get_edits().items():
        if ed.get("deleted") and ed["deleted"] != "gone" and uid not in live:
            store.set_edit(uid, {**ed, "deleted": "gone"})
            e = store.get_event(uid)
            touched.add(e.source if e else "ccs")
    for sid in touched & set(source_ids()):
        rebuild(sid)


def keep_removed(sid: str, previous: list[Event], events: list[Event]):
    """Events the source no longer has (United removed them, or they're gone from the feed): kept here
    struck through, as added events of this calendar, so Undo (Restore) can keep them. Past events that
    simply drop off the schedule aren't kept."""
    today = now().astimezone(TZ).date().isoformat()
    still = {e.uid for e in events}
    gone = [e for e in previous if e.origin == "united" and not e.hidden and e.uid not in still and e.end[:10] >= today]
    if not gone:
        return
    where = "united" if sid == "ccs" else "feed"
    kept = []
    for e in gone[:200]:
        uid = f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(uid, {"title": e.title, "start": e.start, "end": e.end, "all_day": e.all_day, "location": e.location,
                               "description": e.description, "color": e.color, "source": sid,
                               "deleted": f"{where}|{now().isoformat(timespec='seconds')}"})
        kept.append(uid)
    names = ", ".join(f"\"{e.title}\" ({e.start[:10]})" for e in gone[:5]) + (" …" if len(gone) > 5 else "")
    who = "United removed" if sid == "ccs" else f"{calendar_name(sid)}: gone from the feed:"
    state.record("info", f"{who} {len(gone)} event{'s' if len(gone) != 1 else ''}: {names}", kind="Event",
                 undo={"type": "deleted", "where": where, "uids": kept}, stack=False)   # Restore on each event
    pop_undo()
    publish_again = store.get_calendar(skey(sid, "source"))
    if publish_again:
        publish(publish_again[0], publish_again[1], sid)


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
    kept in kv change_notes:<source> and shown in its description, and a line goes in History and
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
    if changed and previous:
        keep_removed(sid, previous, events)
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
        state.status, state.message = "internal", f"{type(e).__name__}: {e}"     # CalendarStream itself failed: red (beta.14)
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
        S.status, S.message = "internal", f"{type(e).__name__}: {e}"
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
    tail_logs()
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
        return JSONResponse({"detail": str(i18n.message(lang, str(exc.detail)))}, status_code=exc.status_code,
                            headers=getattr(exc, "headers", None))      # (X-CS-Fields: the fields to outline)
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


_LOCAL_NETS = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8",
                                                  "169.254.0.0/16", "::1/128", "fc00::/7", "fe80::/10")]
_domain_ips: dict = {"at": None, "ips": set()}    # the public addresses' own IPs, looked up at most every 10 minutes


def _own_network(ip: str) -> bool:
    """An address the limit for all addresses together never shuts out (review #6.1, the Developer's decision): a
    local one (192.168.x.x, 10.x, 172.16–31.x, this machine, IPv6 local) or the IP a public address's domain
    points at (the owner's own connection, when CalendarStream is reached at home through it)."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    if any(addr in net for net in _LOCAL_NETS if net.version == addr.version):
        return True
    if _domain_ips["at"] is None or now() - _domain_ips["at"] > timedelta(minutes=10):
        found = set()
        for url in public_addresses():
            host = urlparse(url).hostname
            if not host:
                continue
            try:
                found |= {i[4][0] for i in socket.getaddrinfo(host, None)}
            except OSError:
                pass
        _domain_ips.update(at=now(), ips=found)
    return ip in _domain_ips["ips"]


# (0.2.8-beta.19, F6) Two ways back in when the limit for all addresses trips, so it can't lock the owner out of a
# remote server: (a) a browser that has signed in here before carries a signed "known browser" cookie, which gets
# past that limit from anywhere (the limit for its own address still applies, and it still needs the password);
# (b) the moment the limit trips, the container log gets a one-time link, good for an hour, that makes the
# browser opening it a known browser.
KNOWN_COOKIE = "cs_known"
KNOWN_DAYS = 400                        # the longest browsers keep a cookie
UNLOCK_FOR = timedelta(hours=1)
_unlock: dict = {"token": None, "until": None}


def _known_sig(issued: int) -> str:
    return hmac.new(_session_key(), f"known\0{issued}".encode(), hashlib.sha256).hexdigest()


def known_browser(request: Request) -> bool:
    """The browser has signed in here before (its signed cookie, within KNOWN_DAYS)."""
    try:
        issued, sig = request.cookies.get(KNOWN_COOKIE, "").split(".")
        issued_n = int(issued)
    except ValueError:
        return False
    if now().timestamp() - issued_n > KNOWN_DAYS * 86400:
        return False
    return hmac.compare_digest(sig, _known_sig(issued_n))


def _new_unlock() -> str:
    """A one-time unlock link for the container log, replacing any earlier one."""
    token = secrets.token_urlsafe(24)
    _unlock.update(token=token, until=now() + UNLOCK_FOR)
    base = (public_addresses() or [""])[0].rstrip("/")
    return f"{base}/unlock/{token}"


def _check_lockout(ip: str, known: bool = False):
    own = _own_network(ip)       # (looked up before the lock: it may ask DNS)
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
        if (len(_global_failures) >= GLOBAL_MAX_FAILURES and not own and not known
                and not (trusted and now() - trusted < GOOD_IP_FOR)):
            raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_failure(ip: str, what: str = "logins"):
    with _failures_lock:
        if len(_gui_failures) > 10_000:      # bounded: forget addresses that aren't locked out first
            for key in [k for k, (_, until) in list(_gui_failures.items()) if not until or until < now()][:5_000]:
                _gui_failures.pop(key, None)
        _global_failures.append(now())
        everyone = len(_global_failures) == GLOBAL_MAX_FAILURES     # the moment the limit for all addresses is reached
        count = _gui_failures.get(ip, [0, None])[0] + 1
        locked = now() + GUI_LOCKOUT if count >= GUI_MAX_FAILURES else None
        _gui_failures[ip] = [0 if locked else count, locked]
    if everyone:     # (review #6.1) said once, with the ways back in
        link = _new_unlock()
        log.warning("Sign-ins paused for new browsers after %s failed attempts. To let your browser in, open this "
                    "link in it within an hour (it works once): %s", GLOBAL_MAX_FAILURES, link)
        state.record("warn", f"{GLOBAL_MAX_FAILURES} failed sign-ins from many addresses in {int(GUI_LOCKOUT.total_seconds() // 60)} min: "
                     "new browsers wait 15 minutes, except browsers that have signed in here before, your own network (a local "
                     "address, or the IP your domain points at) and addresses signed in here in the last 7 days. Locked out "
                     "yourself? Open the one-time link in the container log (docker compose logs) within an hour, or restart "
                     "CalendarStream (docker compose restart).", kind="Settings")
    if locked:
        state.record("warn", f"Status page locked for {ip} after {GUI_MAX_FAILURES} failed {what}")
        raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_success(ip: str):
    with _failures_lock:
        _gui_failures.pop(ip, None)
        if len(_good_ips) > 1_000:
            _good_ips.clear()
        _good_ips[ip] = now()


# --- Signing in (0.2.8-beta.15: the page's own sign-in page, not the browser's pop-up) ------------------
# A signed session cookie: the user, when it ends, and a signature that also covers the password's hash,
# so changing the login signs every browser out. HTTP Basic is still accepted from scripts and tools
# that send it; a page asked for without either goes to /login.

SESSION_COOKIE = "cs_session"


def _session_key() -> bytes:
    key = store.get("session_key")
    if not isinstance(key, str) or len(key) < 64:
        key = secrets.token_hex(32)
        store.set("session_key", key)
    return bytes.fromhex(key)


def _session_sig(user: str, until: int) -> str:
    saved = logins.page_login() or {}
    stamp = (saved.get("password") or {}).get("hash", "")
    return hmac.new(_session_key(), f"{user}\0{until}\0{stamp}".encode(), hashlib.sha256).hexdigest()


def session_user(request: Request) -> str:
    """The signed-in user from the session cookie, or ""."""
    raw = request.cookies.get(SESSION_COOKIE, "")
    try:
        user_q, until, sig = raw.split(".")
        user, until_n = unquote(user_q), int(until)
    except ValueError:
        return ""
    if until_n < now().timestamp() or user != logins.page_user:
        return ""
    return user if hmac.compare_digest(sig, _session_sig(user, until_n)) else ""


def gui_auth(request: Request, creds: HTTPBasicCredentials | None = Depends(basic)):
    """The status-page login. Before one exists, every page leads to the first-visit form; then the sign-in
    page (a session cookie), or HTTP Basic sent by a script."""
    if not logins.has_page_login:
        raise HTTPException(303, headers={"Location": "/welcome"})
    if session_user(request):
        return
    ip = _client_ip(request)
    _check_lockout(ip, known_browser(request))
    if creds and logins.check_page_login(creds.username, creds.password):
        _count_success(ip)
        return
    if creds:   # a real attempt
        _count_failure(ip)
    if request.method == "GET" and not _is_async(request) and "text/html" in request.headers.get("accept", ""):
        target = request.url.path + (f"?{request.url.query}" if request.url.query else "")
        raise HTTPException(303, headers={"Location": "/login?" + urlencode({"next": target})})
    raise HTTPException(401, "Sign in again (reload the page).")


def check_csrf(token: str, expected: str | None = None):
    if not secrets.compare_digest((token or "").encode(), (expected or CSRF_TOKEN).encode()):
        raise HTTPException(400, "This form has expired. Reload the page and try again.")


def renew_csrf():
    """A new form token, e.g. after the login changed, so a token seen before (such as on the
    first-visit page) can't be used against the new login."""
    global CSRF_TOKEN
    CSRF_TOKEN = secrets.token_urlsafe(24)


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


def public_addresses() -> list[str]:
    """Every public address (0.2.8-beta.17, F11): the main one (☰ Settings › Public addresses, first; Google's
    sign-in and notices use it), then any others a feed's link can use instead."""
    extra = [x for x in (store.get("public_urls_extra") or []) if isinstance(x, str)]
    return list(dict.fromkeys([x for x in [public_url(), *extra] if x]))


def feed_url(request: Request, token: str, base: str = "") -> str:
    return f"{base or base_url(request)}/calendar/{token}.ics"


def subscribe_links(request: Request, token: str, base: str = "", name: str = "") -> dict:
    base = base or base_url(request)
    feed = feed_url(request, token, base)
    return {
        "feed": feed,
        # Opens Google Calendar's "add this calendar?" prompt. Google expects the feed as webcal://.
        "google": "https://calendar.google.com/calendar/r?cid=" + quote("webcal://" + feed.split("://", 1)[1], safe=""),
        # webcal:// hands the feed to Apple Calendar (and the phone's own calendar app).
        "webcal": "webcal://" + feed.split("://", 1)[1],
        # Outlook on the web's "Subscribe from web" (0.2.8-beta.17)
        "outlook": "https://outlook.live.com/calendar/0/addfromweb?" + urlencode({"url": feed, "name": name or "CalendarStream"}),
        "page": f"{base}/subscribe/{token}",
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
            "calendars": [{"did": d["id"], "name": d["name"], **dest_google(d).cal_info(d["id"])} for d in destinations("google")],
            "events": sum(int(dest_google(d).cal_info(d["id"]).get("events") or 0) for d in destinations("google")),
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


def _opt_day(value: str) -> date | None:
    try:
        d = date.fromisoformat(value)
        return d if 2000 <= d.year <= 2100 else None
    except ValueError:
        return None


# --- Helpers the routes of more than one area use (app/routes/) ------------------------------------

def _sid(sid: str) -> str:
    """A source ID from a form, which must be one of the sources."""
    if sid not in source_ids():
        raise HTTPException(400, "That calendar source doesn't exist (any more).")
    return sid


# Calendar Sources → + offers these presets. Google and Apple calendars are calendar feeds (their
# private iCal links), with their own step-by-step help; "other" is any .ics / webcal:// link.
SOURCE_PRESETS = {"google": "Google Calendar", "apple": "Apple Calendar", "other": "Calendar feed"}


def _moved(items: list[dict], key: str, before: str, after: str) -> list[dict]:
    """`items` with the one whose id is `key` put just above `before` (or just below `after`)."""
    ids = [x["id"] for x in items]
    if key not in ids:
        raise HTTPException(400, "That isn't there (any more).")
    as_rules = rules_mod.move([{"id": x["id"]} for x in items], key, before, after)
    by_id = {x["id"]: x for x in items}
    return [by_id[x["id"]] for x in as_rules]


class FieldError(HTTPException):
    """A refused Save that names the fields to fix (0.2.8-beta.17, F8): the page outlines them in amber."""
    def __init__(self, message: str, *fields: str):
        super().__init__(400, message, headers={"X-CS-Fields": ",".join(fields)})


def api_on() -> bool:
    """Google Calendar API Sync is set up (☰ Settings): the Google feed modules can be added and connected."""
    return google.configured and google.client_check().get("ok") is not False


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


GOOGLE_SETTINGS = "/?menu=settings#googlesync"      # Google Calendar sync is in ☰ Settings (0.2.8-beta.4)


def show_duration(minutes: int) -> str:
    return f"{minutes // 60}:{minutes % 60:02d}"


def ignored_conflicts() -> list[str]:
    return [x for x in store.get("rule_conflicts_ignored") or [] if isinstance(x, str)]


def united_original(uid: str, sid: str = "ccs") -> Event | None:
    """The source's own version of an event, from its last download (United's, for CCS+)."""
    found = store.get_calendar(skey(sid, "source"))
    if not found:
        return None
    base, _ = preview(sid, found[0])
    return next((e for e in base if e.uid == uid), None)


EVENT_COLORS = {hex_ for _, hex_ in GOOGLE_COLORS.values()}   # Google's 11 event colors

# Icons for the event tools (Material Symbols): a bin to delete, two sheets to duplicate.
TRASH_ICON = icons.svg("delete", 17)
COPY_ICON = icons.svg("content_copy", 17)


ALARM_CHOICES = (0, 5, 10, 15, 30, 60, 120, 1440, 2880, 10080)    # minutes before the start


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


# --- Admin e-mail (Settings) -------------------------------------------------------

EMAIL_RE = re.compile(r"^[^@\s<>\"']{1,64}@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")


def admin_email() -> str:
    """The administrator's e-mail address (☰ Settings), or "". Shown in the Google setup guide as
    the support / contact e-mail and the test user. Checked again on the way out (it goes into the page)."""
    email = str(store.get("admin_email") or "")
    return email if EMAIL_RE.match(email) and len(email) <= 254 else ""


# --- Invite someone (0.2.8-beta.17, F1) -------------------------------------------------------
# A Google module can go to someone else's Google Calendar without their password: an invite is a one-time
# link (7 days) to a page where they sign in to Google themselves; the module's calendar is then made in
# their account. The page needs no login: the unguessable, single-use link is the permission, and the only
# thing it can do is sign that one module's account in. kv "google_invites": token -> {did, account, expires}.
# Its pages: app/routes/google.py.

INVITE_DAYS = 7


def _invites() -> dict:
    now_ = now().timestamp()
    found = {t: v for t, v in (store.get("google_invites") or {}).items() if v.get("expires", 0) > now_}
    return found


def make_invite(d: dict) -> str:
    found = _invites()
    found = {t: v for t, v in found.items() if v["did"] != d["id"]}       # one live invite per module
    token = secrets.token_urlsafe(24)
    found[token] = {"did": d["id"], "account": d["account"], "expires": now().timestamp() + INVITE_DAYS * 86400}
    store.set("google_invites", found)
    state.record("info", f"Google, {d['name']}: invite made (works once, for {INVITE_DAYS} days)", kind="Google")
    return token


def forget_invites(did: str):
    store.set("google_invites", {t: v for t, v in _invites().items() if v["did"] != did})


# --- The routes, by area (0.2.8-beta.20, F12): app/routes/<area>.py ---------------------------------
# Imported last, in this order (the order they're matched in): each one adds its routes to `app` and takes what
# it needs from this module, which is complete by now. AGENTS.md has the map.

import importlib  # noqa: E402

for _area in ("page", "sources", "destinations", "rules", "events", "history", "account", "settings", "google", "status"):
    importlib.import_module(f".routes.{_area}", __package__)

# Read from main by the tests (and anything written before the split).
from .routes.account import LOGIN_TOKEN, _safe_next  # noqa: E402,F401
from .routes.events import _form_values  # noqa: E402,F401
from .routes.page import print_prefs, ui_view  # noqa: E402,F401
from .routes.rules import parse_duration  # noqa: E402,F401
