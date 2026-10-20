"""Web app: status page, month view, .ics feed, and the background Calendar Sync loop."""
from __future__ import annotations

import asyncio
import calendar as pycal
import json
import logging
import secrets
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import quote, urlparse
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from . import __version__
from .calsync import (AuthError, BlockedError, Defaults, Event, SourceError, check_calendar, download,
                      empty_feed, process)
from .config import DEFAULT_CALENDAR_URL, settings
from .store import Store, from_iso, iso

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("calendar_stream")
TZ = ZoneInfo(settings.timezone)
store = Store(settings.dsn)
MAX_AUTH_FAILURES = 2   # pause automatic downloads after this many rejected sign-ins (avoids account lockout)
CSRF_TOKEN = secrets.token_urlsafe(24)   # forms on the status page must carry this


def now():
    return datetime.now(TZ)


def defaults() -> Defaults:
    return Defaults(settings.default_event_type, settings.default_event_hours, settings.allday_24h)


def calendar_url() -> str:
    return store.get("calendar_url") or settings.calendar_url


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


def publish(raw: bytes, sha: str | None = None) -> tuple[list[Event], list[Event]]:
    """Process a downloaded calendar and store it. Returns (new events, previous events)."""
    feed, events, digest = process(raw, settings.calendar_name, settings.timezone, defaults())
    previous = store.load_events()
    store.save_calendar("source", raw, sha or digest)
    store.save_calendar("feed", feed, sha or digest)
    store.replace_events(events)
    state.event_count = len(events)
    return events, previous


def apply_calendar(body: bytes, how: str) -> bool:
    """Publish a calendar file (downloaded or uploaded). Returns False if it was rejected."""
    old_source = store.get_calendar("source")
    changed = not old_source or old_source[0] != body
    _, preview, digest = process(body, settings.calendar_name, settings.timezone, defaults())
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
        state.message = f"{how[:1].upper()}{how[1:]}: {len(events)} events ({detail})"
        state.record("info", f"Schedule {how}: {len(events)} events ({detail})")
    else:
        state.message = f"Up to date: {len(events)} events (no changes)"
        state.record("info", f"Schedule {how}: no changes")
    return True


async def run_once(manual: bool = False):
    if state.running:
        return
    if not settings.configured:
        state.status = "error"
        state.message = ("Calendar Sync sign-in is missing: put your UID in CCS_USER.txt and the Calendar Sync "
                         "password in CCS_PASSWORD.txt (in $MNT_DOCKER/.secrets), then restart.")
        state.record("error", state.message)
        state.save()
        return
    if state.login_failures >= MAX_AUTH_FAILURES and not manual:
        state.status = "paused"
        state.message = (f"Automatic downloads paused after {state.login_failures} rejected sign-ins, to avoid "
                         "locking your account. Fix the secret files and restart, or press 'Sync now'.")
        state.save()
        return

    state.running, state.status = True, "running"
    state.last_attempt = now()
    try:
        have_source = store.get_calendar("source") is not None
        cache = (store.get("http_cache") or {}) if have_source else {}
        dl = await download(calendar_url(), settings.username, settings.password,
                            etag=cache.get("etag", ""), last_modified=cache.get("last_modified", ""))
        store.save_debug("response", json.dumps(dl.debug, indent=2).encode(), "application/json")
        state.last_auth, state.last_auth_ok, state.login_failures = now(), True, 0

        if dl.not_modified:
            state.status, state.last_success = "ok", now()
            state.message = f"Up to date: {state.event_count} events (no changes)"
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


async def loop():
    while True:
        await run_once()
        state.next_run = now() + timedelta(minutes=settings.interval_minutes)
        state.wake.clear()
        try:
            await asyncio.wait_for(state.wake.wait(), timeout=settings.interval_minutes * 60)
        except asyncio.TimeoutError:
            pass


@asynccontextmanager
async def lifespan(_app):
    await asyncio.to_thread(store.open)       # waits for the database container if needed
    settings.resolve_feed_token(store)
    state.load()
    # Re-apply current settings (calendar name, DEFAULT_EVENT_HOURS) to the last download
    source = store.get_calendar("source")
    if source:
        try:
            publish(source[0], source[1])
        except Exception as e:
            log.error("Couldn't rebuild the feed from the stored download: %s", e)
    state.event_count = store.event_count()
    task = asyncio.create_task(loop())
    yield
    task.cancel()
    store.close()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, version=__version__)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
basic = HTTPBasic(auto_error=False)


# --- Status-page login -------------------------------------------------------

GUI_MAX_FAILURES, GUI_LOCKOUT = 5, timedelta(minutes=15)
_gui_failures: dict[str, list] = {}   # client ip -> [failure count, locked-until]


def gui_auth(request: Request, creds: HTTPBasicCredentials | None = Depends(basic)):
    if not settings.gui_password:
        return
    ip = request.client.host if request.client else "?"
    count, locked_until = _gui_failures.get(ip, [0, None])
    if locked_until and now() < locked_until:
        raise HTTPException(429, "Too many failed logins. Try again later.")

    def same(a: str, b: str) -> bool:
        return secrets.compare_digest(a.encode(), b.encode())

    if creds and same(creds.username, settings.gui_user) and same(creds.password, settings.gui_password):
        _gui_failures.pop(ip, None)
        return
    if creds:   # a real attempt (not just the browser's first, credential-less request)
        count += 1
        locked = now() + GUI_LOCKOUT if count >= GUI_MAX_FAILURES else None
        _gui_failures[ip] = [0 if locked else count, locked]
        if locked:
            state.record("warn", f"Status page locked for {ip} after {GUI_MAX_FAILURES} failed logins")
            raise HTTPException(429, "Too many failed logins. Try again later.")
    raise HTTPException(401, headers={"WWW-Authenticate": 'Basic realm="Calendar Stream"'})


def check_csrf(token: str):
    if not secrets.compare_digest(token or "", CSRF_TOKEN):
        raise HTTPException(400, "This form has expired. Reload the page and try again.")


# --- Links ---------------------------------------------------------------------

def base_url(request: Request) -> str:
    return settings.public_base_url or str(request.base_url).rstrip("/")


def feed_url(request: Request) -> str:
    return f"{base_url(request)}/calendar/{settings.feed_token}.ics"


def subscribe_links(request: Request) -> dict:
    feed = feed_url(request)
    return {
        "feed": feed,
        # Opens Google Calendar's "add this calendar?" prompt with the feed pre-filled.
        "google": "https://calendar.google.com/calendar/r?cid=" + quote(feed, safe=""),
        # webcal:// hands the feed to Apple Calendar / Outlook / the phone's default calendar app.
        "webcal": "webcal://" + feed.split("://", 1)[1],
        "page": f"{base_url(request)}/subscribe/{settings.feed_token}",
        "is_public": feed.startswith("https://") and not any(
            h in feed for h in ("localhost", "127.0.0.1", "testserver")),
    }


# --- Month view ----------------------------------------------------------------

def _span(e: Event) -> tuple[date, date, datetime | None, datetime | None]:
    """First and last calendar day an event covers (in the display time zone)."""
    if e.all_day:
        first, end = date.fromisoformat(e.start[:10]), date.fromisoformat(e.end[:10])
        return first, max(first, end - timedelta(days=1)), None, None
    s = datetime.fromisoformat(e.start).astimezone(TZ)
    t = datetime.fromisoformat(e.end).astimezone(TZ)
    last = (t - timedelta(microseconds=1)).date() if t > s else s.date()
    return s.date(), last, s, t


def month_view(events: list[Event], year: int, month: int) -> dict:
    weeks = pycal.Calendar(firstweekday=6).monthdatescalendar(year, month)   # Sunday first, like CCS+
    first_day, last_day = weeks[0][0], weeks[-1][-1]
    by_day: dict[date, list] = {}
    in_month = 0
    for e in events:
        d0, d1, s, t = _span(e)
        if d1 < first_day or d0 > last_day:
            continue
        if d1 >= date(year, month, 1) and d0 <= date(year, month, pycal.monthrange(year, month)[1]):
            in_month += 1
        d = max(d0, first_day)
        while d <= min(d1, last_day):
            if s is None:
                when = "" if d == d0 else "cont."
            elif d0 == d1:
                when = f"{s:%H:%M}–{t:%H:%M}"
            elif d == d0:
                when = f"{s:%H:%M} →"
            elif d == d1:
                when = f"→ {t:%H:%M}"
            else:
                when = "cont."
            by_day.setdefault(d, []).append({"e": e, "when": when, "first": d == d0,
                                             "multi": d0 != d1, "range": _range_text(e, s, t)})
            d += timedelta(days=1)
    prev_m = date(year, month, 1) - timedelta(days=1)
    next_m = date(year, month, 28) + timedelta(days=5)
    return {
        "title": date(year, month, 1).strftime("%B %Y"),
        "weeks": [[{"date": d, "in_month": d.month == month, "items": by_day.get(d, [])} for d in w] for w in weeks],
        "prev": f"{prev_m:%Y-%m}", "next": f"{next_m.replace(day=1):%Y-%m}",
        "today": now().date(), "count": in_month,
    }


def _range_text(e: Event, s, t) -> str:
    if s is None:
        a, b = date.fromisoformat(e.start[:10]), date.fromisoformat(e.end[:10]) - timedelta(days=1)
        return f"{a:%a %b %-d}" + ("" if a == b else f" – {b:%a %b %-d}") + " (all day)"
    if s.date() == t.date():
        return f"{s:%a %b %-d}, {s:%H:%M}–{t:%H:%M}"
    return f"{s:%a %b %-d %H:%M} – {t:%a %b %-d %H:%M}"


def _parse_month(value: str | None) -> tuple[int, int]:
    try:
        y, m = map(int, (value or "").split("-"))
        if 2000 <= y <= 2100 and 1 <= m <= 12:
            return y, m
    except ValueError:
        pass
    today = now().date()
    return today.year, today.month


def _mask(uid: str) -> str:
    return uid[:2] + "•" * max(0, len(uid) - 4) + uid[-2:] if len(uid) > 4 else "•" * len(uid)


# --- Routes ----------------------------------------------------------------------

@app.get("/", dependencies=[Depends(gui_auth)])
def index(request: Request, month: str | None = None):
    events = store.load_events()
    year, mon = _parse_month(month)
    history = [{**h, "time": h["time"].astimezone(TZ)} for h in store.recent_log(100)]
    url = calendar_url()
    return templates.TemplateResponse(request, "index.html", {
        "s": state, "cfg": settings, "feed": feed_url(request), "links": subscribe_links(request),
        "version": __version__, "history": history, "cal": month_view(events, year, mon),
        "csrf": CSRF_TOKEN,
        "setup": {
            "uid": _mask(settings.username) if settings.username else "",
            "has_password": bool(settings.password),
            "url": url, "url_is_default": url == DEFAULT_CALENDAR_URL,
            "url_from_gui": bool(store.get("calendar_url")),
            "downloaded": store.get_calendar("source") is not None,
        },
        "has_source": store.has_debug("source"), "has_response": store.has_debug("response"),
    })


@app.post("/run", dependencies=[Depends(gui_auth)])
async def run_now(csrf: str = Form("")):
    check_csrf(csrf)
    if not state.running:
        asyncio.create_task(run_once(manual=True))
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


@app.get("/subscribe/{token}")
def subscribe(request: Request, token: str):
    """Shareable page (no status-page login needed); the secret token in the URL is the access control."""
    if not secrets.compare_digest(token, settings.feed_token):
        raise HTTPException(404)
    return templates.TemplateResponse(request, "subscribe.html", {
        "cfg": settings, "links": subscribe_links(request),
        "last_success": state.last_success, "event_count": state.event_count,
    })


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
def calendar(token: str):
    if not secrets.compare_digest(token, settings.feed_token):
        raise HTTPException(404)
    found = store.get_calendar("feed")
    ics = found[0] if found else empty_feed(settings.calendar_name, settings.timezone)
    return Response(ics, media_type="text/calendar; charset=utf-8", headers={"Cache-Control": "no-cache"})


@app.get("/healthz")
def health():
    try:
        store.event_count()
    except Exception as e:
        raise HTTPException(503, f"database unavailable: {e}")
    return {"ok": True}
