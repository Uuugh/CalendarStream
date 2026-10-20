"""Web app: status GUI, .ics feed, and the background scrape loop."""
from __future__ import annotations

import asyncio
import logging
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from . import __version__
from .config import settings
from .ics import build_ics
from .parser import Defaults, extract_events
from .scraper import LoginError, scrape
from .store import Store, from_iso, iso

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("ccs")
TZ = ZoneInfo(settings.timezone)
store = Store(settings.dsn)
MAX_LOGIN_FAILURES = 2  # pause auto-login after this many bad-credential failures (avoids account lockout)


def now():
    return datetime.now(TZ)


class State:
    def __init__(self):
        self.status = "starting"          # ok | login_failed | mfa | error | paused | running | starting
        self.message = ""
        self.last_attempt: datetime | None = None
        self.last_success: datetime | None = None
        self.last_login: datetime | None = None
        self.last_login_ok: bool | None = None
        self.next_run: datetime | None = None
        self.login_failures = 0
        self.event_count = 0
        self.source = ""
        self.running = False
        self.wake = asyncio.Event()

    def record(self, level: str, msg: str):
        log.log({"warn": logging.WARNING, "error": logging.ERROR}.get(level, logging.INFO), msg)
        try:
            store.add_log(level, msg)
        except Exception as e:
            log.error("Couldn't write activity log to the database: %s", e)

    # Persisted across restarts in kv "status"
    _SAVED = ("status", "message", "last_attempt", "last_success", "last_login", "last_login_ok",
              "login_failures", "event_count", "source")

    def save(self):
        data = {k: getattr(self, k) for k in self._SAVED}
        for k in ("last_attempt", "last_success", "last_login"):
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
                if k in ("last_attempt", "last_success", "last_login"):
                    v = from_iso(v)
                    v = v.astimezone(TZ) if v else None
                setattr(self, k, v)
        if self.status == "running":  # container stopped mid-run
            self.status = "starting"


state = State()


async def run_once(manual: bool = False):
    if state.running:
        return
    if not settings.configured:
        state.status, state.message = "error", "CCS_USERNAME / CCS_PASSWORD are not set in .env"
        state.record("error", state.message)
        return
    if state.login_failures >= MAX_LOGIN_FAILURES and not manual:
        state.status = "paused"
        state.message = (f"Auto-login paused after {state.login_failures} failed logins to avoid locking "
                         "your account. Fix .env and restart, or press 'Run now' to retry.")
        return

    state.running, state.status = True, "running"
    state.last_attempt = now()
    try:
        result = await scrape(settings, store)
        if result.logged_in:
            state.last_login, state.last_login_ok, state.login_failures = now(), True, 0
            state.record("info", "Login succeeded")
        elif result.used_saved_session:
            state.record("info", "Saved session still valid (no login needed)")

        events, source = extract_events(result.html, result.json_payloads,
                                        settings.timezone,
                                        Defaults(settings.default_event_type, settings.default_event_hours))
        if not events:
            state.status = "error"
            state.message = ("Reached the schedule page but found no events. Check the debug screenshot/"
                             "HTML and adjust app/parser.py. The previous feed is kept.")
            state.record("warn", state.message)
            return

        store.replace_events(events)
        state.event_count, state.source = len(events), source
        state.last_success, state.status = now(), "ok"
        state.message = f"{len(events)} events parsed from {source.upper()}"
        state.record("info", f"Scrape OK: {state.message}")

    except LoginError as e:
        state.last_login, state.last_login_ok = now(), False
        if e.kind == "failed":
            state.login_failures += 1
        state.status = "mfa" if e.kind == "mfa" else "login_failed"
        state.message = str(e)
        state.record("error", f"Login failed: {e}")
        store.delete("session")
    except Exception as e:  # network errors, timeouts, site changes
        state.status, state.message = "error", f"{type(e).__name__}: {e}"
        state.record("error", f"Scrape error: {state.message}")
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
    state.event_count = store.event_count()
    task = asyncio.create_task(loop())
    yield
    task.cancel()
    store.close()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, version=__version__)
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
basic = HTTPBasic(auto_error=False)


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
    if creds:  # a real attempt (not just the browser's first, credential-less request)
        count += 1
        locked = now() + GUI_LOCKOUT if count >= GUI_MAX_FAILURES else None
        _gui_failures[ip] = [0 if locked else count, locked]
        if locked:
            state.record("warn", f"Status page locked for {ip} after {GUI_MAX_FAILURES} failed logins")
            raise HTTPException(429, "Too many failed logins. Try again later.")
    raise HTTPException(401, headers={"WWW-Authenticate": 'Basic realm="Calendar Stream"'})


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


@app.get("/", dependencies=[Depends(gui_auth)])
def index(request: Request):
    events = [e for e in store.load_events() if e.end >= now().date().isoformat()][:25]
    history = [{**h, "time": h["time"].astimezone(TZ)} for h in store.recent_log(100)]
    return templates.TemplateResponse(request, "index.html", {
        "s": state, "cfg": settings, "feed": feed_url(request), "links": subscribe_links(request),
        "version": __version__, "events": events, "history": history, "has_shot": store.has_debug("screenshot"),
    })


@app.get("/subscribe/{token}")
def subscribe(request: Request, token: str):
    """Shareable page (no GUI login needed) — the secret token in the URL is the access control."""
    if not secrets.compare_digest(token, settings.feed_token):
        raise HTTPException(404)
    return templates.TemplateResponse(request, "subscribe.html", {
        "cfg": settings, "links": subscribe_links(request),
        "last_success": state.last_success, "event_count": state.event_count,
    })


@app.post("/run", dependencies=[Depends(gui_auth)])
async def run_now():
    if not state.running:
        asyncio.create_task(run_once(manual=True))
    return RedirectResponse("/", status_code=303)


@app.get("/api/status", dependencies=[Depends(gui_auth)])
def api_status():
    fmt = lambda d: d.isoformat() if d else None
    return {"version": __version__, "status": state.status, "message": state.message, "running": state.running,
            "last_attempt": fmt(state.last_attempt), "last_success": fmt(state.last_success),
            "last_login": fmt(state.last_login), "last_login_ok": state.last_login_ok,
            "next_run": fmt(state.next_run), "events": state.event_count}


@app.get("/debug/{name}", dependencies=[Depends(gui_auth)])
def debug_file(name: str):
    found = store.get_debug(name) if name in ("screenshot", "html", "json") else None
    if not found:
        raise HTTPException(404)
    content, content_type = found
    return Response(content, media_type=content_type)


@app.get("/calendar/{token}.ics")
def calendar(token: str):
    if not secrets.compare_digest(token, settings.feed_token):
        raise HTTPException(404)
    ics = build_ics(store.load_events(), settings.calendar_name, settings.timezone)
    return Response(ics, media_type="text/calendar; charset=utf-8", headers={"Cache-Control": "no-cache"})


@app.get("/healthz")
def health():
    try:
        store.event_count()
    except Exception as e:
        raise HTTPException(503, f"database unavailable: {e}")
    return {"ok": True}
