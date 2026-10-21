"""Web app: status page, month view, .ics feed, and the background Calendar Sync loop."""
from __future__ import annotations

import asyncio
import calendar as pycal
import json
import logging
import re
import secrets
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone
from itertools import zip_longest
from pathlib import Path
from urllib.parse import quote, urlparse
from zoneinfo import ZoneInfo, available_timezones

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.exception_handlers import http_exception_handler as default_http_error
from fastapi.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from . import __version__, i18n
from .calsync import (AuthError, BlockedError, Defaults, Event, SourceError, check_calendar, download,
                      empty_feed, new_calendar, parse, render)
from .config import DEFAULT_CALENDAR_URL, settings
from .gsync import GOOGLE_COLORS, Google, GoogleError
from .logins import LoginError, Logins
from .secretbox import SecretBox
from .store import Store, from_iso, iso
from .updates import FREQUENCIES, RELEASES, Updates, channel as release_channel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("calendar_stream")
logging.getLogger("httpx").setLevel(logging.WARNING)   # one line per Google request is too chatty
TZ = ZoneInfo(settings.timezone)
store = Store(settings.dsn)
box = SecretBox(settings.db_password)
google = Google(store, box, settings.timezone)
logins = Logins(store, box)
updates = Updates(store)
MAX_AUTH_FAILURES = 2   # pause automatic downloads after this many rejected sign-ins (avoids account lockout)
CSRF_TOKEN = secrets.token_urlsafe(24)   # forms on the status page must carry this


def now():
    return datetime.now(TZ)


def defaults() -> Defaults:
    return Defaults(settings.default_event_type, settings.default_event_hours, settings.allday_24h)


def calendar_url() -> str:
    return store.get("calendar_url") or settings.calendar_url


def calendar_name() -> str:
    """Name set on the status page, else CALENDAR_NAME from .env."""
    return store.get("calendar_name") or settings.calendar_name


COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def calendar_color() -> str:
    """Color set on the status page (#rrggbb), or "" for none. Validated again on the way out
    because it is written into the page's CSS."""
    color = store.get("calendar_color") or ""
    return color.lower() if COLOR_RE.match(color) else ""


MAX_TAGS, MAX_TAG_LEN = 30, 40

# How a tag is matched against an event title. "word" is the default.
TAG_MODES = {
    "word": "Whole word",      # "RDO" matches "RDO" and "RDO." but not "VRDO"
    "contains": "Contains",    # "RDO" also matches "VRDO"
    "starts": "Starts with",   # "UA" matches "UA 122 EWR-LHR" but not "TRV UA"
    "exact": "Exact title",    # the whole title must be the tag
}


def calendar_tags() -> list[dict]:
    """Tag colors set on the status page, in priority order:
    [{"tag": "RDO", "color": "#rrggbb", "mode": "word", "case": False}, …].
    Validated again on the way out because the colors are written into the page's CSS."""
    tags = []
    for t in store.get("calendar_tags") or []:
        tag, color = str(t.get("tag", "")).strip(), str(t.get("color", ""))
        mode = t.get("mode") if t.get("mode") in TAG_MODES else "word"
        if tag and COLOR_RE.match(color):
            tags.append({"tag": tag[:MAX_TAG_LEN], "color": color.lower(), "mode": mode, "case": bool(t.get("case"))})
    return tags[:MAX_TAGS]


def _tag_pattern(t: dict) -> re.Pattern:
    tag = re.escape(t["tag"])
    pattern = {"word": r"(?<!\w)" + tag + r"(?!\w)", "contains": tag,
               "starts": r"^\s*" + tag, "exact": r"^\s*" + tag + r"\s*$"}[t["mode"]]
    return re.compile(pattern, 0 if t["case"] else re.IGNORECASE)


def tag_matcher(tags: list[dict]):
    """Return a function giving the color of the first tag that matches an event title
    (by each tag's mode and case setting), or "" when none match."""
    rules = [(_tag_pattern(t), t["color"]) for t in tags]

    def color_for(title: str) -> str:
        return next((color for rx, color in rules if rx.search(title)), "")
    return color_for


# Collapsible sections on the status page, and whether each starts open. The open/closed state
# is saved in the database so it's the same in every browser.
SECTIONS = {"status": True, "setup": False, "activity": False}


def section_state() -> dict:
    saved = store.get("ui_sections") or {}
    return {k: bool(saved.get(k, default)) for k, default in SECTIONS.items()}


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
                   "checked": _local_time(updates.info().get("checked"), lang)}, "version": __version__,
    }, status_code=status_code)


THEMES = ("system", "light", "dark")
CLOCKS = ("auto", "12", "24")


def ui_clock() -> str:
    """12-hour (1:00pm) or 24-hour ("military", 13:00) times on the status page, or "auto" (by language)."""
    clock = store.get("ui_clock")
    return clock if clock in CLOCKS else "auto"


# F2.2: the time zone the status page's calendar is shown in. It only changes how the calendar looks
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
    def __init__(self):
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
        self.running = False
        self.wake = asyncio.Event()

    def record(self, level: str, msg: str):
        log.log({"warn": logging.WARNING, "error": logging.ERROR}.get(level, logging.INFO), msg)
        try:
            store.add_log(level, msg)
        except Exception as e:
            log.error("Couldn't write activity log to the database: %s", e)

    _TIMES = ("last_attempt", "last_success", "last_change", "last_auth")
    _SAVED = _TIMES + ("status", "message", "last_auth_ok", "login_failures", "event_count")

    def save(self):
        data = {k: getattr(self, k) for k in self._SAVED}
        for k in self._TIMES:
            data[k] = iso(data[k])
        try:
            store.set("status", data)
        except Exception as e:
            log.error("Couldn't save status to the database: %s", e)

    def load(self):
        data = store.get("status") or {}
        for k in self._SAVED:
            if k in data:
                v = data[k]
                if k in self._TIMES:
                    v = from_iso(v)
                    v = v.astimezone(TZ) if v else None
                setattr(self, k, v)
        if self.status == "running":   # container stopped mid-run
            self.status = "starting"


state = State()


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


async def ensure_watch():
    """Keep Google's change notifications ("webhooks") running for CalendarStream's calendar: start
    them, move them to a new public address, renew them before they run out. If Google refuses,
    Autosync carries on as before (daily check) and asks again later."""
    address = notify_address()
    if not address or not google.connected or not google.watch_due(address, now(), WATCH_RENEW, WATCH_RETRY):
        return
    before = google.watch_info()
    had = bool(before.get("id"))
    try:
        await google.start_watch(address)
        if not had:
            state.record("info", "Google: instant updates turned on (changes made in Google are checked within seconds)")
    except GoogleError as e:
        if str(e) != before.get("error"):     # say so once, not at every retry
            state.record("warn", f"Google: instant updates aren't available ({e}); changes made in Google are checked daily instead")


def sync_window_start() -> date:
    """Decision 5: events from the first day of the current month onward are synced."""
    return now().date().replace(day=1)


async def google_sync_once(full: bool) -> bool:
    """Run one sync. Returns False if it failed."""
    async with google_job.lock:
        if not (google.configured and google.connected):
            return True
        google_job.running = True
        try:
            result = await google.sync(store.load_events(), calendar_name(), tag_matcher(calendar_tags()),
                                       sync_window_start(), full)
            if result.changed or result.notes:
                state.record("info", f"Google: {result.summary()}"
                             + ("; " + "; ".join(result.notes) if result.notes else ""))
            await ensure_watch()
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
        ok = await google_sync_once(full)
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


def publish(raw: bytes | None, sha: str | None = None) -> tuple[list[Event], list[Event]]:
    """Build the feed from a CCS+ calendar (or none yet) plus the edits and added events made here,
    and store it. Returns (all events now, events before)."""
    if raw is not None:
        cal, base, digest = parse(raw, settings.timezone, defaults())
    else:
        cal, base, digest = new_calendar(), [], ""
    feed, events = render(cal, base, calendar_name(), settings.timezone, store.get_edits(), store.get_customs(),
                          calendar_color())
    previous = store.load_events()
    if raw is not None:
        store.save_calendar("source", raw, sha or digest)
    store.save_calendar("feed", feed, sha or digest)
    store.replace_events(events)
    state.event_count = sum(1 for e in events if not e.hidden)
    request_google_sync()
    return events, previous


def rebuild():
    """Rebuild the feed from the last CCS+ calendar, e.g. after an edit or a rename."""
    source = store.get_calendar("source")
    publish(source[0] if source else None, source[1] if source else None)


def apply_calendar(body: bytes, how: str) -> bool:
    """Publish a calendar file (downloaded or uploaded). Returns False if it was rejected."""
    old_source = store.get_calendar("source")
    changed = not old_source or old_source[0] != body
    _, preview, digest = parse(body, settings.timezone, defaults())
    if not preview and store.event_count() > 0:
        state.status = "error"
        state.message = (f"The {how} calendar has no events. Keeping the previous feed "
                         f"({state.event_count} events) in case this is a glitch.")
        state.record("warn", state.message)
        return False
    events, previous = publish(body, digest)
    state.status, state.last_success = "ok", now()
    if changed:
        state.last_change = now()
        old_ids, new_ids = {e.uid for e in previous}, {e.uid for e in events}
        added, removed = len(new_ids - old_ids), len(old_ids - new_ids)
        detail = f"{added} new, {removed} removed" if previous else "first copy"
        state.message = f"{how[:1].upper()}{how[1:]}: {state.event_count} events in feed ({detail})"
        state.record("info", f"Schedule {how}: {state.event_count} events in feed ({detail})")
    else:
        state.message = f"Up to date: {state.event_count} events in feed (no changes)"
        state.record("info", f"Schedule {how}: no changes")
    return True


async def run_once(manual: bool = False):
    if state.running:
        return
    if not logins.ccs_configured:
        # Nothing to do until the login is entered; the page shows the boxes for it.
        state.status = "setup"
        state.message = "Enter your CCS+ UID and Calendar Sync password to start downloading the schedule."
        state.save()
        return
    if state.login_failures >= MAX_AUTH_FAILURES and not manual:
        state.status = "paused"
        state.message = (f"Automatic downloads paused after {state.login_failures} rejected sign-ins, to avoid "
                         "locking your account. Check the UID and Calendar Sync password in Setup, then press Sync now.")
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
            state.status, state.last_success = "ok", now()
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


MIN_INTERVAL, MAX_INTERVAL = 15, 24 * 60   # minutes between automatic downloads


def interval_minutes() -> int:
    """How often to download from CCS+: set on the status page, else SYNC_INTERVAL_MINUTES."""
    saved = store.get("sync_interval")
    return saved if isinstance(saved, int) and MIN_INTERVAL <= saved <= MAX_INTERVAL else settings.interval_minutes


async def loop():
    while True:
        await run_once()
        state.next_run = now() + timedelta(minutes=interval_minutes())
        # Sleep until the next check. state.wake means the interval changed: work out the time again.
        while (remaining := (state.next_run - now()).total_seconds()) > 0:
            state.wake.clear()
            try:
                await asyncio.wait_for(state.wake.wait(), timeout=remaining)
            except asyncio.TimeoutError:
                break


async def update_loop():
    """Settings → Check for updates: look for a newer version of this install's channel when due."""
    await asyncio.sleep(30)
    while True:
        try:
            if updates.due(datetime.now(timezone.utc)):
                found = await updates.check()
                if updates.available() and found.get("newest") != found.get("logged"):
                    state.record("info", f"Update available: CalendarStream {found['newest']} "
                                         "(run the installer again to update)")
                    store.set("update_check", {**found, "logged": found["newest"]})
        except Exception as e:      # never let this stop the app
            log.warning("Update check failed: %s", e)
        await asyncio.sleep(3600)


@asynccontextmanager
async def lifespan(_app):
    await asyncio.to_thread(store.open)       # waits for the database container if needed
    settings.resolve_feed_token(store)
    state.load()
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
    tasks = [asyncio.create_task(loop()), asyncio.create_task(google_loop()), asyncio.create_task(update_loop())]
    yield
    for task in tasks:
        task.cancel()
    store.close()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, version=__version__)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    """Show form errors as a small page in the visitor's language (the API keeps JSON). Sign-in
    prompts (401) and redirects (303) pass through unchanged."""
    wants_page = "text/html" in request.headers.get("accept", "") and not request.url.path.startswith("/api/")
    if exc.status_code in (303, 401) or not wants_page:
        return await default_http_error(request, exc)
    try:
        lang = lang_for(request)
    except Exception:
        lang = "en"
    return page(request, "error.html", {"detail": exc.detail, "code": exc.status_code},
                status_code=exc.status_code, lang=lang)
basic = HTTPBasic(auto_error=False)


# --- Status-page login -------------------------------------------------------

GUI_MAX_FAILURES, GUI_LOCKOUT = 5, timedelta(minutes=15)
_gui_failures: dict[str, list] = {}   # client ip -> [failure count, locked-until]


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "?"


def _check_lockout(ip: str):
    locked_until = _gui_failures.get(ip, [0, None])[1]
    if locked_until and now() < locked_until:
        raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_failure(ip: str, what: str = "logins"):
    count = _gui_failures.get(ip, [0, None])[0] + 1
    locked = now() + GUI_LOCKOUT if count >= GUI_MAX_FAILURES else None
    _gui_failures[ip] = [0 if locked else count, locked]
    if locked:
        state.record("warn", f"Status page locked for {ip} after {GUI_MAX_FAILURES} failed {what}")
        raise HTTPException(429, "Too many failed attempts. Try again later.")


def gui_auth(request: Request, creds: HTTPBasicCredentials | None = Depends(basic)):
    """The status-page login (HTTP Basic). Before one exists, every page leads to the first-visit form."""
    if not logins.has_page_login:
        raise HTTPException(303, headers={"Location": "/welcome"})
    ip = _client_ip(request)
    _check_lockout(ip)
    if creds and logins.check_page_login(creds.username, creds.password):
        _gui_failures.pop(ip, None)
        return
    if creds:   # a real attempt (not just the browser's first, credential-less request)
        _count_failure(ip)
    raise HTTPException(401, headers={"WWW-Authenticate": 'Basic realm="CalendarStream"'})


def check_csrf(token: str):
    if not secrets.compare_digest(token or "", CSRF_TOKEN):
        raise HTTPException(400, "This form has expired. Reload the page and try again.")


# --- Who reads the feed --------------------------------------------------------------------
#
# Google Calendar fetches a subscribed feed with its own reader ("Google-Calendar-Importer"). Noting
# when it last came shows whether Google can reach the feed at all: until it has, Google shows the
# subscription under its web address and without events.

def note_feed_read(user_agent: str):
    kind = "google" if "google" in user_agent.lower() else "other"
    reads = store.get("feed_reads") or {}
    last = from_iso(reads.get(kind))
    if last is None or now() - last > timedelta(minutes=1):     # don't write on every fetch
        reads[kind] = iso(now())
        store.set("feed_reads", reads)


def feed_reads(lang: str) -> dict:
    reads = store.get("feed_reads") or {}
    return {k: _local_time(reads.get(k), lang) for k in ("google", "other")}


# --- Links ---------------------------------------------------------------------

def public_url() -> str:
    """The public address: set in Settings (wins), else PUBLIC_URL in .env, else ""."""
    return store.get("public_url") or settings.public_base_url


def normalise_public_url(value: str) -> str:
    """Tidy an address typed in Settings: add https:// when there's no scheme, drop a trailing
    slash. Raises ValueError for anything that isn't a plain http(s) address."""
    value = value.strip().rstrip("/")
    if value and "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    if (parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.query or parsed.fragment
            or parsed.username or parsed.password or any(c.isspace() for c in value) or len(value) > 300):
        raise ValueError(value)
    return value


def base_url(request: Request) -> str:
    return public_url() or str(request.base_url).rstrip("/")


def feed_url(request: Request) -> str:
    return f"{base_url(request)}/calendar/{settings.feed_token}.ics"


def subscribe_links(request: Request) -> dict:
    feed = feed_url(request)
    return {
        "feed": feed,
        # Opens Google Calendar's "add this calendar?" prompt. Google expects the feed as webcal://.
        "google": "https://calendar.google.com/calendar/r?cid=" + quote("webcal://" + feed.split("://", 1)[1], safe=""),
        # webcal:// hands the feed to Apple Calendar / Outlook / the phone's default calendar app.
        "webcal": "webcal://" + feed.split("://", 1)[1],
        "page": f"{base_url(request)}/subscribe/{settings.feed_token}",
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
    """Instant updates from Google, for the page: on (until when, last notice) or why not."""
    w = google.watch_info()
    if not notify_address():
        return {"on": False, "why": "needs a public https:// address (☰ → Public address)"}
    if w.get("error") and w.get("address") == notify_address():
        return {"on": False, "why": w["error"]}
    if w.get("id"):
        return {"on": True, "until": _local_time(w.get("expires"), lang), "last": _local_time(w.get("last_notice"), lang)}
    return {"on": False, "why": "starts with the next sync"}


def google_view(request: Request, lang: str = "en") -> dict:
    uri = google_redirect_uri(request)
    host = urlparse(uri).hostname or ""
    info = google.info()
    return {"configured": google.configured, "connected": google.connected, "info": info,
            "client_id": google.client_id, "has_secret": bool(google.client_secret),
            "check": google.client_check(), "checked_at": _local_time(google.client_check().get("at"), lang),
            "running": google_job.running, "last_sync": _local_time(info.get("last_sync"), lang),
            "redirect_uri": uri, "watch": _watch_view(lang),
            # Google only sends sign-ins back to https:// addresses, or http:// on this computer.
            "redirect_ok": uri.startswith("https://") or host in ("localhost", "127.0.0.1")}


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


def month_view(events: list[Event], year: int, month: int, tags: list[dict] | None = None,
               lang: str = "en") -> dict:
    tz = display_tz()
    dates = dates_for(lang)
    hm = dates.clock
    cont = str(i18n.tr(lang, "cont."))
    weeks = pycal.Calendar(firstweekday=6).monthdatescalendar(year, month)
    color_for = tag_matcher(tags or [])   # Sunday first, like CCS+
    first_day, last_day = weeks[0][0], weeks[-1][-1]
    by_day: dict[date, list] = {}
    in_month = 0
    for e in events:
        d0, d1, s, t = _span(e, tz)
        if d1 < first_day or d0 > last_day:
            continue
        if d1 >= date(year, month, 1) and d0 <= date(year, month, pycal.monthrange(year, month)[1]):
            in_month += 1
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
            by_day.setdefault(d, []).append({"e": e, "when": when, "first": d == d0, "tag_color": e.color or color_for(e.title),
                                             "multi": d0 != d1, "range": _range_text(e, s, t, lang)})
            d += timedelta(days=1)
    prev_m = date(year, month, 1) - timedelta(days=1)
    next_m = date(year, month, 28) + timedelta(days=5)
    return {
        "title": dates.title(date(year, month, 1)), "dow": dates.dow,
        "weeks": [[{"date": d, "in_month": d.month == month, "items": by_day.get(d, [])} for d in w] for w in weeks],
        "prev": f"{prev_m:%Y-%m}", "next": f"{next_m.replace(day=1):%Y-%m}", "month": f"{year}-{month:02d}",
        "today": now().astimezone(tz).date(), "count": in_month,
    }


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

@app.get("/", dependencies=[Depends(gui_auth)])
def index(request: Request, month: str | None = None):
    events = store.load_events()
    year, mon = _parse_month(month)
    history = [{**h, "time": h["time"].astimezone(TZ)} for h in store.recent_log(100)]
    url = calendar_url()
    lang = lang_for(request)
    return page(request, "index.html", {
        "s": state, "cfg": settings, "feed": feed_url(request), "links": subscribe_links(request),
        "history": history, "cal": month_view(events, year, mon, calendar_tags(), lang),
        "csrf": CSRF_TOKEN, "name": calendar_name(), "name_from_gui": bool(store.get("calendar_name")),
        "color": calendar_color(), "tags": calendar_tags(), "tag_modes": TAG_MODES,
        "sections": section_state(), "interval": interval_minutes(),
        "zone": display_zone(), "zones": ALL_ZONES, "common_zones": COMMON_ZONES, "reads": feed_reads(lang),
        "google": google_view(request, lang), "open_menu": request.query_params.get("menu") == "settings",
        "public": {"url": public_url(), "from_settings": bool(store.get("public_url")),
                   "env": settings.public_base_url},
        "page_user": logins.page_user,
        "setup": {
            "uid": logins.ccs()[0], "has_password": bool(logins.ccs()[1]), "configured": logins.ccs_configured,
            "url": url, "url_is_default": url == DEFAULT_CALENDAR_URL,
            "url_from_gui": bool(store.get("calendar_url")),
            "downloaded": store.get_calendar("source") is not None,
        },
        "has_source": store.has_debug("source"), "has_response": store.has_debug("response"),
    }, lang=lang)


@app.post("/run", dependencies=[Depends(gui_auth)])
async def run_now(csrf: str = Form("")):
    check_csrf(csrf)
    if not state.running:
        asyncio.create_task(run_once(manual=True))
    return RedirectResponse("/", status_code=303)


# --- Logins -----------------------------------------------------------------------

@app.get("/welcome")
def welcome(request: Request):
    """First visit: create the status-page login (needs the setup code from the container log)."""
    if logins.has_page_login:
        return RedirectResponse("/", status_code=303)
    return page(request, "welcome.html", {"csrf": CSRF_TOKEN, "error": ""})


@app.post("/welcome")
def create_login(request: Request, csrf: str = Form(""), code: str = Form(""), user: str = Form(""),
                 password: str = Form(""), confirm: str = Form("")):
    check_csrf(csrf)
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
        return page(request, "welcome.html", {"csrf": CSRF_TOKEN, "error": error, "user": user}, status_code=400)
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
    state.record("info", f"Status-page login changed (user \"{logins.page_user}\")")
    # The browser still holds the old login; it will ask for the new one.
    return RedirectResponse("/", status_code=303)


def _back_to(back: str, anchor: str) -> str:
    """Where a dashboard form returns to: its own box. (`back` is accepted from older pages and ignored:
    the logins no longer appear in Settings.)"""
    return f"/#{anchor}"


@app.post("/setup/ccs", dependencies=[Depends(gui_auth)])
async def set_ccs_login(csrf: str = Form(""), uid: str = Form(""), password: str = Form(""), back: str = Form("")):
    """Save the CCS+ UID and Calendar Sync password (Setup), then download straight away."""
    check_csrf(csrf)
    try:
        logins.save_ccs(uid, password)
    except LoginError as e:
        raise HTTPException(400, str(e))
    state.login_failures = 0
    store.delete("http_cache")
    state.record("info", "CCS+ UID and Calendar Sync password saved")
    if not state.running:
        asyncio.create_task(run_once(manual=True))
        await asyncio.sleep(1.5)   # usually long enough to show whether CCS+ accepted it
    return RedirectResponse(_back_to(back, "setup"), status_code=303)


@app.post("/setup/interval", dependencies=[Depends(gui_auth)])
async def set_interval(csrf: str = Form(""), minutes: str = Form("")):
    """Change how often the schedule is downloaded from CCS+ (saved in the database)."""
    check_csrf(csrf)
    try:
        value = int(minutes)
    except ValueError:
        raise HTTPException(400, "Enter a number of minutes.")
    if not MIN_INTERVAL <= value <= MAX_INTERVAL:
        raise HTTPException(400, f"Choose between {MIN_INTERVAL} and {MAX_INTERVAL} minutes.")
    if value == settings.interval_minutes:
        store.delete("sync_interval")
    else:
        store.set("sync_interval", value)
    # The next check counts from the last one (or now, if that time has already passed).
    state.next_run = max(now(), (state.last_attempt or now()) + timedelta(minutes=value))
    state.wake.set()
    state.record("info", f"Checks every {value} min from now on")
    return RedirectResponse("/", status_code=303)


@app.post("/setup/link", dependencies=[Depends(gui_auth)])
async def set_link(csrf: str = Form(""), url: str = Form(""), action: str = Form("save")):
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
        asyncio.create_task(run_once(manual=True))
    return RedirectResponse("/#setup", status_code=303)


@app.post("/feed/name", dependencies=[Depends(gui_auth)])
async def set_name(csrf: str = Form(""), name: str = Form(""), color: str = Form(""),
                   color_default: str = Form(""), tag: list[str] = Form([]), tag_color: list[str] = Form([]),
                   tag_mode: list[str] = Form([]), tag_case: list[str] = Form([])):
    """Save the calendar's name and color (the title editor of Status & setup).
    A blank name goes back to CALENDAR_NAME from .env. `color` is only sent when it was changed on
    the page; `color_default` clears it. Tags are saved by /feed/tags."""
    check_csrf(csrf)
    name = " ".join(name.split())[:100]
    if name and name != settings.calendar_name:
        store.set("calendar_name", name)
    else:
        store.delete("calendar_name")
    notes = [f"name \"{calendar_name()}\""]
    if color_default:
        store.delete("calendar_color")
        notes.append("default color")
    elif color:
        if not COLOR_RE.match(color):
            raise HTTPException(400, "Choose the color with the color picker.")
        store.set("calendar_color", color.lower())
        notes.append(f"color {color.lower()}")
    if tag:   # older pages sent the tags with the name; they now have their own form (/feed/tags)
        notes += _save_tags(tag, tag_color, tag_mode, tag_case)
    rebuild()
    state.record("info", "Calendar settings saved: " + ", ".join(notes))
    return RedirectResponse("/", status_code=303)


def _save_tags(tag: list[str], tag_color: list[str], tag_mode: list[str], tag_case: list[str]) -> list[str]:
    """Check and store the tag rows; returns a note for the activity log if they changed."""
    tags = []
    # Each row sends one value per field (the case toggle is a hidden "1"/"" input), so they line up.
    for t, c, m, cs in zip_longest(tag, tag_color, tag_mode, tag_case, fillvalue=""):
        t = " ".join(t.split())[:MAX_TAG_LEN]
        if not t:
            continue
        if not COLOR_RE.match(c):
            raise HTTPException(400, f"Choose a color for the tag \"{t}\" with the color picker.")
        tags.append({"tag": t, "color": c.lower(), "mode": m if m in TAG_MODES else "word", "case": cs == "1"})
    if len(tags) > MAX_TAGS:
        raise HTTPException(400, f"Up to {MAX_TAGS} tags can be used.")
    if tags != calendar_tags():
        store.set("calendar_tags", tags)
        return [f"{len(tags)} tag color{'' if len(tags) == 1 else 's'}"]
    return []


@app.post("/feed/tags", dependencies=[Depends(gui_auth)])
async def set_tags(csrf: str = Form(""), tag: list[str] = Form([]), tag_color: list[str] = Form([]),
                   tag_mode: list[str] = Form([]), tag_case: list[str] = Form([])):
    """Save the tag colors (the Tag Colors block under the health bar). Rows with no text are dropped."""
    check_csrf(csrf)
    notes = _save_tags(tag, tag_color, tag_mode, tag_case)
    if notes:
        rebuild()
        state.record("info", "Calendar settings saved: " + ", ".join(notes))
    return RedirectResponse("/#tags", status_code=303)


@app.post("/ui/section", dependencies=[Depends(gui_auth)])
async def set_section(csrf: str = Form(""), section: str = Form(""), open_: str = Form("", alias="open")):
    """Remember whether a status-page section is open (the page sends this when it's toggled)."""
    check_csrf(csrf)
    if section not in SECTIONS:
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
    """Remember 12-hour / 24-hour times (Settings → Time format); "auto" follows the language."""
    check_csrf(csrf)
    if clock not in CLOCKS:
        raise HTTPException(400, "Unknown time format.")
    if clock == "auto":
        store.delete("ui_clock")
    else:
        store.set("ui_clock", clock)
    return Response(status_code=204)


@app.post("/ui/tz", dependencies=[Depends(gui_auth)])
async def set_display_tz(csrf: str = Form(""), tz: str = Form("")):
    """F2.2: the time zone the calendar is shown in here; "" goes back to TZ from .env."""
    check_csrf(csrf)
    if not tz or tz == settings.timezone:
        store.delete("ui_tz")
    elif valid_zone(tz):
        store.set("ui_tz", tz)
    else:
        raise HTTPException(400, "Unknown time zone.")
    return Response(status_code=204)


@app.post("/settings/updates", dependencies=[Depends(gui_auth)])
async def update_settings(csrf: str = Form(""), frequency: str = Form(""), action: str = Form("save")):
    """Settings → Check for updates: how often, or check now."""
    check_csrf(csrf)
    if frequency:
        try:
            updates.set_frequency(frequency)
        except ValueError:
            raise HTTPException(400, "Unknown update frequency.")
    if action == "check":
        await updates.check()
    return RedirectResponse("/?menu=settings#updates", status_code=303)


@app.post("/ui/theme", dependencies=[Depends(gui_auth)])
async def set_theme(csrf: str = Form(""), theme: str = Form("")):
    """Remember the light / dark / system choice (the page sends this when it's changed)."""
    check_csrf(csrf)
    if theme not in THEMES:
        raise HTTPException(400, "Unknown theme.")
    store.set("ui_theme", theme)
    return Response(status_code=204)


# --- F3: edit and add events --------------------------------------------------

def _back(month: str | None) -> str:
    y, m = _parse_month(month)
    return f"/?month={y}-{m:02d}#cal"


def united_original(uid: str) -> Event | None:
    """United's own version of an event, from the last CCS+ calendar."""
    source = store.get_calendar("source")
    if not source:
        return None
    _, base, _ = parse(source[0], settings.timezone, defaults())
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
def edit_event(request: Request, uid: str = "", date_: str = Query("", alias="date"), month: str | None = None):
    if uid:
        e = store.get_event(uid)
        if not e:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
    else:   # new event on a given day
        try:
            day = date.fromisoformat(date_)
        except ValueError:
            day = now().date()
        e = Event(title="", start=day.isoformat(), end=(day + timedelta(days=1)).isoformat(), all_day=False,
                  origin="custom")
        e.start = datetime.combine(day, datetime.min.time().replace(hour=9), display_tz()).isoformat()
        e.end = datetime.combine(day, datetime.min.time().replace(hour=10), display_tz()).isoformat()
    original = united_original(uid) if e.origin == "united" and uid else None
    lang = lang_for(request)
    tag_color = tag_matcher(calendar_tags())(e.title) if e.title else ""
    start_zone, end_zone = _saved_zones(uid) if uid else ("", "")
    start_zone, end_zone = start_zone or display_zone(), end_zone or start_zone or display_zone()
    return page(request, "event.html", {
        "e": e, "f": _form_values(e, ZoneInfo(start_zone), ZoneInfo(end_zone), dates_for(lang).clock),
        "start_zone": start_zone, "end_zone": end_zone, "zones": ALL_ZONES, "common_zones": COMMON_ZONES,
        "is_new": not uid, "original": original,
        "colors": GOOGLE_COLORS.values(), "auto_color": tag_color or calendar_color() or "",
        "original_range": _range_text(original, *_span(original)[2:], lang) if original else "",
        "csrf": CSRF_TOKEN, "month": month or (e.start[:7]), "tz": display_zone(),
    }, lang=lang)


EVENT_COLORS = {hex_ for _, hex_ in GOOGLE_COLORS.values()}   # Google's 11 event colors


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
                     start_tz: str = Form(""), end_tz: str = Form(""), end_tz_differs: str = Form("")):
    check_csrf(csrf)
    end_tz = end_tz if end_tz_differs else start_tz      # one time zone for both unless asked otherwise
    data = _event_from_form(title, all_day, start_date, start_time, end_date, end_time, location, description,
                            color, start_tz, end_tz)
    current = store.get_event(uid) if uid else None
    if current and current.origin == "united":
        original = united_original(uid)
        if not original:
            raise HTTPException(404, "That event isn't in the current schedule any more.")
        store.set_edit(uid, {**data, "hidden": bool(hidden), "base": original.fingerprint()})
        state.record("info", f"Edited \"{original.title}\" ({original.start[:10]})"
                     + (" and hid it from Google" if hidden else ""))
    else:
        new_uid = uid if current else f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(new_uid, data)
        state.record("info", f"{'Updated' if current else 'Added'} \"{data['title']}\" ({data['start'][:10]})")
    rebuild()
    state.save()
    return RedirectResponse(_back(month or data["start"][:7]), status_code=303)


@app.post("/event/revert", dependencies=[Depends(gui_auth)])
async def revert_event(csrf: str = Form(""), uid: str = Form(""), month: str = Form("")):
    check_csrf(csrf)
    store.delete_edit(uid)
    rebuild()
    state.record("info", "Reverted an event to United's version")
    return RedirectResponse(_back(month), status_code=303)


@app.post("/event/delete", dependencies=[Depends(gui_auth)])
async def delete_event(csrf: str = Form(""), uid: str = Form(""), month: str = Form("")):
    check_csrf(csrf)
    e = store.get_event(uid)
    if not e or e.origin != "custom":
        raise HTTPException(400, "Only events added here can be deleted. Hide United's events instead.")
    store.delete_custom(uid)
    rebuild()
    state.record("info", f"Deleted \"{e.title}\" ({e.start[:10]})")
    return RedirectResponse(_back(month), status_code=303)


MAX_UPLOAD = 5 * 1024 * 1024


@app.post("/setup/upload", dependencies=[Depends(gui_auth)])
async def upload(csrf: str = Form(""), file: UploadFile = File(...)):
    """Publish a Calendar.ics downloaded by hand from CCS+ (United's own Google Calendar procedure)."""
    check_csrf(csrf)
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
    return RedirectResponse("/#setup", status_code=303)


# --- Google Calendar connection ---------------------------------------------------

@app.post("/settings/public-url", dependencies=[Depends(gui_auth)])
async def set_public_url(csrf: str = Form(""), url: str = Form(""), action: str = Form("save")):
    """Save the public address (Settings menu). It wins over PUBLIC_URL in .env; Reset goes back
    to .env. It's used for the feed and subscribe links and Google's sign-in redirect."""
    check_csrf(csrf)
    if action == "reset" or not url.strip():
        store.delete("public_url")
        state.record("info", f"Public address reset to .env ({settings.public_base_url or 'not set'})")
    else:
        try:
            value = normalise_public_url(url)
        except ValueError:
            raise HTTPException(400, "Enter the address people use to reach this page, e.g. https://cal.example.com")
        if value == settings.public_base_url:
            store.delete("public_url")
        else:
            store.set("public_url", value)
        state.record("info", f"Public address set to {value}")
    return RedirectResponse("/#feedcard", status_code=303)


@app.post("/google/client", dependencies=[Depends(gui_auth)])
async def google_client(request: Request, csrf: str = Form(""), client_id: str = Form(""),
                        client_secret: str = Form(""), action: str = Form("save"), back: str = Form("")):
    """Save or remove the Google OAuth client (Settings menu). The secret is stored encrypted and
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
        check = await google.check_client(google_redirect_uri(request))
        state.record("info" if check["ok"] else "warn",
                     f"Google OAuth client saved ({google.client_id.split('.')[0][:12]}…): {check['message']}")
    return RedirectResponse(_back_to(back, "feedcard"), status_code=303)


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
            raise GoogleError("Google sign-in was cancelled." if error in ("access_denied", "")
                              else f"Google sign-in failed: {error[:80]}.")
        info = await google.finish_sign_in(state_, code, calendar_name())
        how = "created" if info.get("created") else "found again"
        state.record("info", f"Google Calendar connected as {info.get('email') or 'your account'}; "
                             f"calendar \"{info.get('calendar_name', '')}\" {how}")
        request_google_sync(full=True)
    except GoogleError as e:
        google.record_error(str(e))
        state.record("error", f"Google: {e}")
    return RedirectResponse("/#feedcard", status_code=303)


@app.post("/google/disconnect", dependencies=[Depends(gui_auth)])
async def google_disconnect(csrf: str = Form(""), delete: str = Form("")):
    """Stop syncing: optionally delete CalendarStream's calendar, then remove its access in Google."""
    check_csrf(csrf)
    if not google.connected:
        return RedirectResponse("/#feedcard", status_code=303)
    email = google.info().get("email") or "your account"
    async with google_job.lock:      # not in the middle of a sync
        await google.stop_watch()
        notes = await google.disconnect(delete_calendar=delete == "1")
    if delete == "1":
        store.google_forget()
    what = "and its calendar deleted" if delete == "1" and not any("calendar" in n for n in notes) else ""
    state.record("warn" if notes else "info", f"Google Calendar disconnected ({email}) {what}".strip()
                 + ("; " + "; ".join(notes) if notes else ""))
    return RedirectResponse("/#feedcard", status_code=303)


@app.post("/google/notify")
async def google_notify(request: Request):
    """Google's change notification for CalendarStream's calendar (no login: Google can't sign in).
    Checked by the channel ID and the secret token CalendarStream gave Google; it carries no
    details, so it just starts a check that puts back events changed or deleted in Google."""
    channel = request.headers.get("x-goog-channel-id", "")
    if google.notice_ok(channel, request.headers.get("x-goog-channel-token", "")):
        if request.headers.get("x-goog-resource-state") != "sync":   # "sync" only confirms the channel
            google.noticed()
            request_google_sync(full=True)
    return Response(status_code=200)   # anything else makes Google retry; unknown channels just expire


@app.post("/google/sync", dependencies=[Depends(gui_auth)])
async def google_sync_now(csrf: str = Form("")):
    """Sync now, checking Google's copy too (repairs events changed or deleted in Google)."""
    check_csrf(csrf)
    request_google_sync(full=True)
    await asyncio.sleep(0.5)
    return RedirectResponse("/#feedcard", status_code=303)


@app.get("/subscribe/{token}")
def subscribe(request: Request, token: str):
    """Shareable page (no status-page login needed); the secret token in the URL is the access control."""
    if not secrets.compare_digest(token, settings.feed_token):
        raise HTTPException(404)
    # Shared with other people: shown in each visitor's browser language.
    lang = i18n.pick(None, request.headers.get("accept-language", ""))
    return page(request, "subscribe.html", {
        "cfg": settings, "name": calendar_name(), "links": subscribe_links(request),
        "last_success": state.last_success, "event_count": state.event_count,
    }, lang=lang)


@app.get("/api/status", dependencies=[Depends(gui_auth)])
def api_status():
    fmt = lambda d: d.isoformat() if d else None
    return {"version": __version__, "status": state.status, "message": state.message, "running": state.running,
            "last_attempt": fmt(state.last_attempt), "last_success": fmt(state.last_success),
            "last_change": fmt(state.last_change), "last_auth": fmt(state.last_auth),
            "last_auth_ok": state.last_auth_ok, "next_run": fmt(state.next_run), "events": state.event_count}


@app.get("/debug/{name}", dependencies=[Depends(gui_auth)])
def debug_file(name: str):
    found = store.get_debug(name) if name in ("source", "response") else None
    if not found:
        raise HTTPException(404)
    content, content_type = found
    if name == "source":   # show it in the browser rather than downloading
        content_type = "text/plain; charset=utf-8"
    return Response(content, media_type=content_type)


@app.get("/calendar/{token}.ics")
def calendar(token: str, request: Request):
    if not secrets.compare_digest(token, settings.feed_token):
        raise HTTPException(404)
    note_feed_read(request.headers.get("user-agent", ""))
    found = store.get_calendar("feed")
    ics = found[0] if found else empty_feed(calendar_name(), settings.timezone)
    return Response(ics, media_type="text/calendar; charset=utf-8", headers={"Cache-Control": "no-cache"})


@app.get("/healthz")
def health():
    try:
        store.event_count()
    except Exception as e:
        raise HTTPException(503, f"database unavailable: {e}")
    return {"ok": True}
