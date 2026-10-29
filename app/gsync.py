"""Google Calendar connection: OAuth sign-in, the stored (encrypted) refresh token, and the
calendar CalendarStream owns in the connected Google account.

CalendarStream asks only for `calendar.app.created`, which lets it manage calendars it created and
nothing else in the account, plus `openid email` to show which account is connected.

The refresh token is encrypted with a key derived from DB_PASSWORD, which is not stored in the
database, so a copy of the database alone can't be used to reach the Google account.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import logging
import re
import secrets
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from urllib.parse import parse_qs, quote, urlencode, urlparse

import httpx

from .secretbox import SecretBox

log = logging.getLogger("calendar_stream.google")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
API_URL = "https://www.googleapis.com/calendar/v3"
SCOPE_CALENDAR = "https://www.googleapis.com/auth/calendar.app.created"
SCOPES = ("openid", "email", SCOPE_CALENDAR)

SIGN_IN_TTL = 15 * 60       # seconds a sign-in started here stays valid
MAX_PENDING = 20            # sign-ins started but not finished, kept at most
TIMEOUT = httpx.Timeout(20.0, connect=10.0)

MAX_WRITES = 1500          # Google writes in one sync at most; the rest wait for the next one
SYNC_NOTE = "Synced by CalendarStream"
MARKER = "calendarstream"   # private extended property on every event CalendarStream writes

# Google Calendar's event colors, as its apps show them: colorId -> (name, hex).
GOOGLE_COLORS = {
    "11": ("Tomato", "#d50000"), "4": ("Flamingo", "#e67c73"), "6": ("Tangerine", "#f4511e"),
    "5": ("Banana", "#f6bf26"), "2": ("Sage", "#33b679"), "10": ("Basil", "#0b8043"),
    "7": ("Peacock", "#039be5"), "9": ("Blueberry", "#3f51b5"), "1": ("Lavender", "#7986cb"),
    "3": ("Grape", "#8e24aa"), "8": ("Graphite", "#616161"),
}

WATCH_TTL = 7 * 24 * 3600   # seconds a push-notification channel lasts (Google's default and usual limit)

CALENDAR_DESCRIPTION = ("Kept up to date by CalendarStream. "
                        "Changes made here may be overwritten at the next sync.")
CAL_KEYS = ("calendar_id", "calendar_name", "synced_calendar", "created", "last_sync", "events")


class GoogleError(Exception):
    """Something went wrong talking to Google; the message is shown on the status page."""


class AccessRevoked(GoogleError):
    """Google no longer accepts the stored sign-in (revoked, expired or the password changed)."""


class Conflict(GoogleError):
    """Google already has an event with that ID."""


class CalendarMissing(GoogleError):
    """CalendarStream's calendar was deleted in Google."""


def _rgb(hex_color: str) -> tuple[int, int, int]:
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def nearest_color_id(hex_color: str) -> str:
    """The Google event color closest to a #rrggbb color."""
    r, g, b = _rgb(hex_color)
    return min(GOOGLE_COLORS, key=lambda cid: sum((x - y) ** 2 for x, y in zip((r, g, b), _rgb(GOOGLE_COLORS[cid][1]))))


def event_id(uid: str) -> str:
    """A stable Google event ID for a CalendarStream UID. Google allows only the letters a–v and
    digits (base32hex), 5–1024 long; a hash of the UID fits and never collides in practice."""
    return base64.b32hexencode(hashlib.sha256(uid.encode()).digest()).decode().rstrip("=").lower()


def event_body(e, tz_name: str, color_id: str = "") -> dict:
    """The Google event for a CalendarStream event (calsync.Event)."""
    if e.all_day:
        start, end = {"date": e.start[:10]}, {"date": e.end[:10]}
    else:
        start, end = {"dateTime": e.start, "timeZone": tz_name}, {"dateTime": e.end, "timeZone": tz_name}
    body = {
        "id": event_id(e.uid),
        "status": "confirmed",
        "summary": e.title,
        "location": e.location,
        "description": (e.description + "\n\n" if e.description else "") + SYNC_NOTE,
        "start": start, "end": end,
        "transparency": "transparent" if e.free else "opaque",
        # Only the reminders set on the status page (Google allows five); none otherwise (decision 3)
        "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": m} for m in e.alarm_minutes()[:5]]},
        "extendedProperties": {"private": {MARKER: "1", "uid": e.uid[:900]}},
    }
    if color_id:
        body["colorId"] = color_id
    return body


def _hash(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def in_window(e, first_day: date, tz: ZoneInfo) -> bool:
    """Whether an event ends after the start of the sync window (decision 5: from the first day of
    the current month). Older events are left alone in Google."""
    if e.all_day:
        return e.end[:10] > first_day.isoformat()
    return datetime.fromisoformat(e.end) > datetime.combine(first_day, datetime.min.time(), tz)


def _ends_in_window(ends: str, first_day: date, tz: ZoneInfo) -> bool:
    if len(ends) == 10:
        return ends > first_day.isoformat()
    return datetime.fromisoformat(ends) > datetime.combine(first_day, datetime.min.time(), tz)


@dataclass
class SyncResult:
    added: int = 0
    updated: int = 0
    removed: int = 0
    repaired: int = 0
    unchanged: int = 0
    renamed: bool = False
    more: bool = False            # stopped at MAX_WRITES; the rest goes in the next sync
    notes: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.added or self.updated or self.removed or self.repaired or self.renamed)

    def summary(self) -> str:
        parts = [f"{n} {w}" for n, w in ((self.added, "added"), (self.updated, "updated"),
                                       (self.removed, "removed"), (self.repaired, "repaired")) if n]
        if self.renamed:
            parts.append("calendar renamed")
        text = ", ".join(parts) or "no changes"
        return text + (" (more at the next sync)" if self.more else "")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _id_token_claims(id_token: str) -> dict:
    """The claims of an ID token received directly from Google's token endpoint over HTTPS.
    OpenID Connect allows skipping the signature check in that case (Core 1.0, section 3.1.3.7)."""
    try:
        payload = id_token.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (IndexError, ValueError):
        return {}


CLIENT_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{10,200}\.apps\.googleusercontent\.com$")


class Google:
    def __init__(self, store, box: SecretBox, tz_name: str, account: str = ""):
        self.store = store
        self.box = box
        # 0.2.8-beta.15: one Google account per instance (each Google module can use its own Gmail); the
        # first ("") keeps the keys it always had, so installs from before need nothing moved. The OAuth
        # client is shared by every account.
        self.account = account
        self._info_key = "google" + (f":{account}" if account else "")
        self._token_key = "google_token" + (f":{account}" if account else "")
        self._client: tuple[str, str] | None = None              # (kept for callers from before; read each time now)
        self.tz_name = tz_name
        self._pending: dict[str, tuple[str, str, float]] = {}   # state -> (PKCE verifier, redirect URI, expiry)
        self._access: tuple[str, float] | None = None            # (access token, expiry)
        self._lock = asyncio.Lock()

    # --- The OAuth client (entered in the Google Calendar Autosync box) ----------------

    def client(self) -> tuple[str, str]:
        """The OAuth client ID and secret saved in the Google Calendar Autosync box, or ("", "")."""
        saved = self.store.get("google_client") or {}      # (read each time: every account shares it)
        secret = self._unseal(saved["secret"], "") if saved.get("secret") else ""
        return (saved.get("id", ""), secret)

    @property
    def client_id(self) -> str:
        return self.client()[0]

    @property
    def client_secret(self) -> str:
        return self.client()[1]

    @property
    def configured(self) -> bool:
        return all(self.client())

    def save_client(self, client_id: str, client_secret: str):
        """Save the OAuth client. A blank secret keeps the one already saved (the page never shows it)."""
        client_id, client_secret = client_id.strip(), client_secret.strip()
        if not CLIENT_ID_RE.match(client_id):
            raise GoogleError("That doesn't look like a Google OAuth client ID "
                              "(it ends in .apps.googleusercontent.com).")
        if not client_secret:
            client_secret = self.client_secret
            if not client_secret:
                raise GoogleError("Enter the client secret too.")
        if len(client_secret) > 200 or any(ch.isspace() for ch in client_secret):
            raise GoogleError("That doesn't look like a client secret.")
        self.store.set("google_client", {"id": client_id, "secret": self._seal(client_secret)})
        self._client = None
        self._access = None

    def client_check(self) -> dict:
        """The last check of the saved client: {"ok": True/False/None, "message", "at", "redirect_uri",
        "redirect_ok"}."""
        check = (self.store.get("google_client") or {}).get("check") or {}
        message = str(check.get("message") or "")
        if check.get("ok") is False and message.startswith("Google doesn't list "):
            # Saved by 0.1.20: the ID and secret were fine, only the redirect URI was missing.
            uri = message[len("Google doesn't list "):].split(" under ", 1)[0]
            check = {**check, "ok": True, "message": "Google accepted the client ID and secret",
                     "redirect_uri": uri, "redirect_ok": False}
        return check

    def _save_check(self, ok: bool | None, message: str, redirect_uri: str = "", redirect_ok: bool | None = None):
        """Remember a check: `ok` is about the ID and secret; `redirect_ok` about `redirect_uri` (the
        address the check used), False when Google doesn't list it."""
        saved = self.store.get("google_client")
        if saved:
            saved["check"] = {"ok": ok, "message": message, "at": datetime.now(timezone.utc).isoformat(),
                              "redirect_uri": redirect_uri, "redirect_ok": redirect_ok}
            self.store.set("google_client", saved)

    async def check_client(self, redirect_uri: str) -> dict:
        """Ask Google whether it accepts the saved client ID and secret, without signing anyone in:
        swap a made-up code. Google answers "invalid_grant" (bad code) only once the client ID and
        secret are right, "invalid_client" when either is wrong, and "redirect_uri_mismatch" when the
        redirect URI isn't listed on the client. The consent screen is only checked when someone connects."""
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.post(TOKEN_URL, data={
                    "grant_type": "authorization_code", "code": "calendarstream-check",
                    "redirect_uri": redirect_uri, "client_id": self.client_id, "client_secret": self.client_secret})
            body = r.json() if r.content else {}
        except (httpx.HTTPError, ValueError) as e:
            self._save_check(None, f"couldn't reach Google to check it ({type(e).__name__})")
            return self.client_check()
        error, detail = body.get("error", ""), str(body.get("error_description", "")).lower()
        if error == "redirect_uri_mismatch":
            # The ID and secret are right, but Connect would fail: the redirect URI isn't listed.
            self._save_check(True, "Google accepted the client ID and secret", redirect_uri, False)
        elif error == "invalid_grant":
            self._save_check(True, "Google accepted the client ID and secret", redirect_uri, True)
        elif error in ("invalid_client", "unauthorized_client"):
            self._save_check(False, "Google doesn't know this client ID" if "not found" in detail
                             else "Google rejected the client secret")
        else:
            self._save_check(None, f"Google gave an unexpected answer ({error or r.status_code})")
        return self.client_check()

    async def check_redirect(self, redirect_uri: str) -> bool | None:
        """Does Google accept `redirect_uri` for the saved client (0.2.8-beta.14)? Asks for Google's sign-in
        page the way Connect does, without following it: Google answers with its sign-in page (a
        redirect) when the address is on the client's list, and with its "Error 400:
        redirect_uri_mismatch" page (or a redirect to its error page saying so) when it isn't. True,
        False, or None when Google's answer doesn't say. Saved with the client's check."""
        url = AUTH_URL + "?" + urlencode({
            "client_id": self.client_id, "redirect_uri": redirect_uri, "response_type": "code",
            "scope": " ".join(SCOPES), "access_type": "offline", "prompt": "consent", "state": "calendarstream-check",
            "code_challenge": _b64url(hashlib.sha256(b"calendarstream-check").digest()), "code_challenge_method": "S256"})
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=False) as client:
                r = await client.get(url)
        except httpx.HTTPError:
            return None
        where = r.headers.get("location", "")
        said = r.text[:200000] + " " + where
        for value in parse_qs(urlparse(where).query).get("authError", []):     # Google's error page: base64
            try:
                said += " " + base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)).decode("latin-1")
            except ValueError:
                pass
        if "redirect_uri_mismatch" in said:
            ok = False
        elif any(word in said for word in ("invalid_client", "deleted_client", "unauthorized_client")):
            ok = None                # the client itself: check_client says what's wrong
        elif r.status_code in (200, 302, 303) and "/signin/oauth/error" not in where:
            ok = True
        else:
            ok = None
        check = self.client_check()
        self._save_check(check.get("ok"), check.get("message", ""), redirect_uri, ok)
        return ok

    def clear_client(self):
        self.store.delete("google_client")
        self._client = None
        self._access = None

    def info(self) -> dict:
        """Saved connection details: email, connected_at, last_sync, last_result, last_error, and each
        source's calendar (see cal_info)."""
        return self.store.get(self._info_key) or {}

    # Each Google destination has a calendar of its own in Google: {calendar_id, calendar_name,
    # synced_calendar, created, last_sync, events}, under "calendars" by the destination's ID. (Before
    # 0.2 the one calendar's details were at the top level of "google", under the key "ccs" here;
    # rekey() moves them.)

    def cal_info(self, sid: str) -> dict:
        info = self.info()
        if sid == "ccs":
            return {k: info[k] for k in CAL_KEYS if k in info}
        return dict((info.get("calendars") or {}).get(sid) or {})

    def _update_cal(self, sid: str, **changes):
        if sid == "ccs":
            self._update_info(**changes)
            return
        info = self.info()
        cals = dict(info.get("calendars") or {})
        cal = {**(cals.get(sid) or {}), **changes}
        cals[sid] = {k: v for k, v in cal.items() if v not in (None, "")}
        info["calendars"] = cals
        self.store.set(self._info_key, info)

    def rekey(self, old: str, new: str):
        """Give a calendar (its details, tracked events and notifications) a new key: used when the
        calendars of 0.2.0 (one per source) and before become destinations."""
        info = self.cal_info(old)
        if not info:
            return
        self._update_cal(new, **info)
        if old == "ccs":
            whole = self.info()
            for k in CAL_KEYS:
                if k not in ("last_sync",):
                    whole.pop(k, None)
            self.store.set(self._info_key, whole)
        else:
            whole = self.info()
            (whole.get("calendars") or {}).pop(old, None)
            self.store.set(self._info_key, whole)
        self.store.google_rekey(old, new)
        watch = self.store.get(self._watch_key(old))
        if watch:
            self.store.set(self._watch_key(new), watch)
            self.store.delete(self._watch_key(old))

    def calendar_sids(self) -> list[str]:
        """Calendars CalendarStream has (or had) in Google, by key."""
        info = self.info()
        return (["ccs"] if info.get("calendar_id") else []) + list((info.get("calendars") or {}).keys())

    def forget_calendar(self, sid: str):
        """Stop managing a calendar (its destination was removed); it stays in Google."""
        self._forget_cal(sid)

    def _forget_cal(self, sid: str):
        if sid == "ccs":
            info = self.info()
            for k in CAL_KEYS:
                info.pop(k, None)
            self.store.set(self._info_key, info)
        else:
            info = self.info()
            (info.get("calendars") or {}).pop(sid, None)
            self.store.set(self._info_key, info)
        self.store.google_forget(source=sid)

    def _update_info(self, **changes):
        info = self.info()
        info.update(changes)
        self.store.set(self._info_key, {k: v for k, v in info.items() if v not in (None, "")})

    @property
    def connected(self) -> bool:
        return self.store.get(self._token_key) is not None

    # --- Encrypted values (the client secret and the refresh token) --------------------

    def _seal(self, text: str) -> dict:
        return self.box.seal(text)

    def _unseal(self, sealed: dict, default: str | None = None) -> str:
        """Decrypt a value from _seal. If it can't be read (DB_PASSWORD changed), return `default`,
        or raise AccessRevoked when there is none."""
        try:
            return self.box.unseal(sealed)
        except ValueError:
            if default is not None:
                return default
            raise AccessRevoked("The saved Google sign-in can't be read (was DB_PASSWORD changed?). "
                                "Disconnect and connect again.")

    def _save_refresh_token(self, token: str):
        self.store.set(self._token_key, self._seal(token))

    def _refresh_token(self) -> str:
        saved = self.store.get(self._token_key)
        if not saved:
            raise GoogleError("Google Calendar isn't connected.")
        return self._unseal(saved)

    # --- Signing in ------------------------------------------------------------------------

    def sign_in_url(self, redirect_uri: str) -> str:
        """Start a sign-in: the Google consent page to send the browser to. A one-time `state` value
        ties Google's answer to this request, and PKCE ties the code to this server."""
        now = time.monotonic()
        self._pending = {s: p for s, p in self._pending.items() if p[2] > now}
        while len(self._pending) >= MAX_PENDING:
            self._pending.pop(next(iter(self._pending)))
        state, verifier = secrets.token_urlsafe(24), secrets.token_urlsafe(48)
        self._pending[state] = (verifier, redirect_uri, now + SIGN_IN_TTL)
        return AUTH_URL + "?" + urlencode({
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline",     # ask for a refresh token…
            "prompt": "consent",          # …every time, so reconnecting always gets a new one
            "state": state,
            "code_challenge": _b64url(hashlib.sha256(verifier.encode()).digest()),
            "code_challenge_method": "S256",
        })

    async def finish_sign_in(self, state: str, code: str) -> dict:
        """Handle Google's answer: swap the code for tokens, check the permission was granted and
        save the refresh token. The calendars are made (or found again) by the next sync. Returns the info."""
        pending = self._pending.pop(state or "", None)
        if not pending or pending[2] < time.monotonic():
            raise GoogleError("This Google sign-in has expired or was already used. Try Connect again.")
        verifier, redirect_uri, _ = pending
        tokens = await self._token_request({
            "grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        })
        granted = set(tokens.get("scope", "").split())
        if SCOPE_CALENDAR not in granted:
            raise GoogleError("Google didn't grant access to calendars made by CalendarStream. Connect again "
                              "and leave the calendar permission ticked.")
        refresh = tokens.get("refresh_token")
        if not refresh:
            raise GoogleError("Google didn't send a lasting sign-in (refresh token). Try Connect again.")
        claims = _id_token_claims(tokens.get("id_token", ""))
        email = claims.get("email", "") if claims.get("aud") in (self.client_id, None) else ""

        previous = self.info()
        if previous.get("email") and email and previous["email"] != email:
            # A different account: its calendar is a different one.
            previous = {}
            self.store.set(self._info_key, {})
        self._save_refresh_token(refresh)
        self._save_check(True, "Google accepted the client ID and secret", redirect_uri, True)   # signed in: both proven
        self._access = (tokens["access_token"], time.monotonic() + int(tokens.get("expires_in", 3600)) - 60)
        self._update_info(email=email, connected_at=datetime.now(timezone.utc).isoformat(), last_error=None)
        return self.info()

    async def _token_request(self, form: dict) -> dict:
        form = {**form, "client_id": self.client_id, "client_secret": self.client_secret}
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.post(TOKEN_URL, data=form)
        except httpx.HTTPError as e:
            raise GoogleError(f"Couldn't reach Google ({type(e).__name__}).")
        try:
            body = r.json()
        except ValueError:
            body = {}
        if r.status_code == 200 and body.get("access_token"):
            return body
        error = body.get("error", f"HTTP {r.status_code}")
        if error == "invalid_grant":
            raise AccessRevoked("Google no longer accepts CalendarStream's sign-in (access removed, or the app "
                                "is still in Testing mode, which expires it after 7 days). Connect again.")
        if error in ("invalid_client", "unauthorized_client"):
            raise GoogleError("Google rejected the OAuth client: check the client ID and secret in "
                              "Settings → Google Calendar.")
        if error == "redirect_uri_mismatch":
            raise GoogleError("Google says the redirect URI isn't one of the client's authorised redirect URIs.")
        raise GoogleError(f"Google sign-in failed: {error}.")

    async def _access_token(self) -> str:
        async with self._lock:
            if self._access and self._access[1] > time.monotonic():
                return self._access[0]
            tokens = await self._token_request({"grant_type": "refresh_token", "refresh_token": self._refresh_token()})
            self._access = (tokens["access_token"], time.monotonic() + int(tokens.get("expires_in", 3600)) - 60)
            return self._access[0]

    # --- Calendar API -------------------------------------------------------------------------

    async def api(self, method: str, path: str, *, body: dict | None = None, params: dict | None = None,
                  ok_missing: bool = False) -> dict | None:
        """Call the Calendar API. Retries once with a fresh access token on 401 and backs off on
        rate limits and server errors. With ok_missing, a 404/410 returns None instead of failing."""
        delay = 1.0
        for attempt in range(5):
            token = await self._access_token()
            try:
                async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                    r = await client.request(method, API_URL + path, json=body, params=params,
                                             headers={"Authorization": f"Bearer {token}"})
            except httpx.HTTPError as e:
                if attempt == 4:
                    raise GoogleError(f"Couldn't reach Google Calendar ({type(e).__name__}).")
                await asyncio.sleep(delay)
                delay *= 2
                continue
            if r.status_code in (200, 201):
                return r.json() if r.content else {}
            if r.status_code == 204:
                return {}
            if r.status_code in (404, 410) and ok_missing:
                return None
            reason = _error_reason(r)
            if r.status_code == 409:
                raise Conflict(f"Google Calendar: {reason or 'conflict'}")
            if r.status_code == 401 and attempt == 0:
                self._access = None              # expired early: get a new access token once
                continue
            if r.status_code == 429 or r.status_code >= 500 or reason in ("rateLimitExceeded", "userRateLimitExceeded"):
                if attempt < 4:
                    await asyncio.sleep(delay)
                    delay *= 2
                    continue
            if r.status_code == 401:
                raise AccessRevoked("Google no longer accepts CalendarStream's sign-in. Connect again.")
            raise GoogleError(f"Google Calendar answered {r.status_code}"
                              + (f" ({reason})" if reason else "") + f" to {method} {path.split('?')[0]}.")
        raise GoogleError("Google Calendar is busy; CalendarStream will try again later.")

    async def ensure_calendar(self, sid: str, name: str, calendar_id: str | None = None) -> str:
        """Use a source's calendar if it still exists in Google, otherwise create it."""
        info = self.cal_info(sid)
        calendar_id = calendar_id or info.get("calendar_id")
        unreachable = False
        if calendar_id:
            try:
                found = await self.api("GET", f"/calendars/{_quote(calendar_id)}", ok_missing=True)
            except GoogleError as e:
                if "403" not in str(e):
                    raise
                found, unreachable = None, True    # made with another client: Google won't show it to this one
            if found is not None:
                self._update_cal(sid, calendar_id=calendar_id, calendar_name=found.get("summary", name), created=False,
                                 client=info.get("client") or self.client_id)
                return calendar_id
            # (0.2.8-beta.14) a calendar made with an earlier client can't be reached with this one: Google
            # only shows an app the calendars it made. A new one is made; the old one is named in the log.
            if unreachable or (info.get("client") and info.get("client") != self.client_id):
                self._update_cal(sid, replaced=info.get("calendar_name") or name)
        made = await self.api("POST", "/calendars", body={
            "summary": name, "timeZone": self.tz_name,
            "description": CALENDAR_DESCRIPTION})
        self._update_cal(sid, calendar_id=made["id"], calendar_name=made.get("summary", name), created=True, client=self.client_id)
        return made["id"]

    async def set_color(self, sid: str, color: str):
        """The calendar's color in the person's Google Calendar (0.2.8-beta.15: a Google module's color box)."""
        calendar_id = self.cal_info(sid).get("calendar_id")
        if not calendar_id:
            return
        await self.api("PATCH", f"/users/me/calendarList/{_quote(calendar_id)}", params={"colorRgbFormat": "true"},
                       body={"backgroundColor": color, "foregroundColor": "#ffffff"})
        self._update_cal(sid, color=color)

    async def delete_calendar(self, sid: str) -> str:
        """Delete a destination's calendar in Google (if connected) and forget it. Returns a note
        when Google couldn't be reached ("" otherwise)."""
        note = ""
        calendar_id = self.cal_info(sid).get("calendar_id")
        if calendar_id and self.connected:
            try:
                await self.stop_watch([sid])
                await self.api("DELETE", f"/calendars/{_quote(calendar_id)}", ok_missing=True)
            except GoogleError as e:
                note = f"its calendar in Google wasn't deleted ({e}); delete it there by hand"
        self._forget_cal(sid)
        return note

    # --- Disconnecting ------------------------------------------------------------------------

    async def disconnect(self, delete_calendar: bool) -> list[str]:
        """Optionally delete CalendarStream's calendar, revoke the sign-in in Google and forget it.
        The local sign-in is always forgotten; returns notes on anything Google didn't confirm."""
        notes = []
        if delete_calendar:
            for sid in self.calendar_sids():
                calendar_id = self.cal_info(sid).get("calendar_id")
                try:
                    if calendar_id:
                        await self.api("DELETE", f"/calendars/{_quote(calendar_id)}", ok_missing=True)
                    self._forget_cal(sid)
                except GoogleError as e:
                    notes.append(f"a calendar wasn't deleted ({e})")
        info = self.info()
        try:
            token = self._refresh_token()
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.post(REVOKE_URL, data={"token": token})
            if r.status_code not in (200, 400):   # 400: Google had already dropped it
                notes.append(f"Google didn't confirm removing access (HTTP {r.status_code}); "
                             "remove CalendarStream at myaccount.google.com/permissions")
        except (GoogleError, httpx.HTTPError):
            notes.append("couldn't reach Google to remove access; remove CalendarStream at "
                         "myaccount.google.com/permissions")
        self.store.delete(self._token_key)
        self._access = None
        # Keep the calendar IDs (unless deleted) so reconnecting the same account reuses those calendars.
        info.pop("connected_at", None)
        info.pop("last_error", None)
        info.pop("created", None)
        self.store.set(self._info_key, info)
        return notes

    def record_error(self, message: str):
        self._update_info(last_error=message)

    # --- Instant updates from Google (push notifications, "webhooks") -------------------------
    #
    # Google calls /google/notify whenever an event in CalendarStream's calendar changes there, so a
    # change made by hand in Google is repaired within seconds instead of at the daily check. The
    # notification carries no details; it only triggers a check. Channels last about a week and
    # must be renewed (a new channel, then the old one stopped). Saved in kv "google_watch":
    # {id, resource, token (sealed), address, calendar_id, expires, error, tried, last_notice}.

    @staticmethod
    def _watch_key(sid: str) -> str:
        return "google_watch" if sid == "ccs" else f"google_watch:{sid}"

    def watch_info(self, sid: str = "ccs") -> dict:
        return self.store.get(self._watch_key(sid)) or {}

    def _update_watch(self, sid: str, **changes):
        info = self.watch_info(sid)
        info.update(changes)
        self.store.set(self._watch_key(sid), info)

    def watch_due(self, sid: str, address: str, now_: datetime, renew_before: timedelta, retry_after: timedelta) -> bool:
        """Whether a channel should be started now: none yet, a new address or calendar, close to
        expiring; after a failure, only once `retry_after` has passed (or the address changed)."""
        w = self.watch_info(sid)
        calendar_id = self.cal_info(sid).get("calendar_id")
        if w.get("error") and w.get("address") == address:
            tried = datetime.fromisoformat(w["tried"]) if w.get("tried") else None
            return not tried or now_ - tried >= retry_after
        if not w.get("id") or w.get("address") != address or w.get("calendar_id") != calendar_id:
            return True
        expires = datetime.fromisoformat(w["expires"]) if w.get("expires") else now_
        return expires - now_ <= renew_before

    async def start_watch(self, sid: str, address: str):
        """Ask Google to notify `address` of changes to a source's calendar; stop the old channel."""
        calendar_id = self.cal_info(sid).get("calendar_id")
        old = self.watch_info(sid)
        self._update_watch(sid, address=address, tried=datetime.now(timezone.utc).isoformat())
        if not calendar_id:
            return
        channel, token = secrets.token_hex(16), secrets.token_urlsafe(32)
        try:
            made = await self.api("POST", f"/calendars/{_quote(calendar_id)}/events/watch", body={
                "id": channel, "type": "web_hook", "address": address, "token": token,
                "params": {"ttl": str(WATCH_TTL)}})
        except GoogleError as e:
            self._update_watch(sid, error=str(e))
            raise
        expires = datetime.fromtimestamp(int(made.get("expiration") or 0) / 1000, timezone.utc) \
            if made.get("expiration") else datetime.now(timezone.utc) + timedelta(seconds=WATCH_TTL)
        self.store.set(self._watch_key(sid), {
            "id": channel, "resource": made.get("resourceId", ""), "token": self._seal(token),
            "address": address, "calendar_id": calendar_id, "expires": expires.isoformat(),
            "tried": datetime.now(timezone.utc).isoformat(), "last_notice": old.get("last_notice")})
        if old.get("id") and old.get("resource"):
            await self._stop_channel(old["id"], old["resource"])

    async def _stop_channel(self, channel: str, resource: str):
        try:
            await self.api("POST", "/channels/stop", body={"id": channel, "resourceId": resource}, ok_missing=True)
        except GoogleError:
            pass    # it runs out by itself within a week

    async def stop_watch(self, sids: list[str]):
        """Stop notifications for these sources' calendars (when disconnecting or removing a source)."""
        for sid in sids:
            w = self.watch_info(sid)
            if w.get("id") and w.get("resource"):
                await self._stop_channel(w["id"], w["resource"])
            self.store.delete(self._watch_key(sid))

    def notice_from(self, channel: str, token: str, sids: list[str]) -> str | None:
        """The source whose current channel sent a notification (its ID and secret token match), or None."""
        for sid in sids:
            w = self.watch_info(sid)
            if not w.get("id") or not w.get("token"):
                continue
            if secrets.compare_digest((channel or "").encode(), w["id"].encode()) and \
                    secrets.compare_digest((token or "").encode(), self._unseal(w["token"], "").encode()):
                return sid
        return None

    def noticed(self, sid: str):
        self._update_watch(sid, last_notice=datetime.now(timezone.utc).isoformat())

    # --- Keeping the events in step -------------------------------------------------------

    # --- Two-way (0.2.8-beta.10): what changed in Google ------------------------------------

    async def pull(self, sid: str, first_day: date) -> list[dict]:
        """What was changed in the Google calendar CalendarStream made for a destination since it was
        last written: CalendarStream's events edited or deleted there, and events added there. Only
        CalendarStream's own calendar is read; nothing is changed here (main.apply_google_changes does)."""
        info = self.cal_info(sid)
        calendar_id = info.get("calendar_id")
        if not calendar_id or info.get("synced_calendar") != calendar_id:
            return []
        tz = ZoneInfo(self.tz_name)
        cal = f"/calendars/{_quote(calendar_id)}"
        rows = self.store.google_rows(sid)
        by_gid = {row["google_id"]: (uid, row) for uid, row in rows.items()}
        found, page = {}, None
        start = datetime.combine(first_day, datetime.min.time(), tz).isoformat()
        while True:
            params = {"timeMin": start, "showDeleted": "true", "maxResults": "2500"}
            if page:
                params["pageToken"] = page
            try:
                data = await self.api("GET", f"{cal}/events", params=params, ok_missing=True)
            except GoogleError as e:
                if "403" in str(e):      # made with another client: nothing to bring from it
                    return []
                raise
            if data is None:
                return []
            for ev in data.get("items", []):
                found[ev["id"]] = ev
            page = data.get("nextPageToken")
            if not page:
                break
        out = []
        for gid, ev in found.items():
            mine = (ev.get("extendedProperties") or {}).get("private", {}).get(MARKER) == "1"
            if mine:
                if gid not in by_gid:
                    continue
                uid, row = by_gid[gid]
                if ev.get("status") == "cancelled":
                    out.append({"kind": "deleted", "uid": uid, "gid": gid})
                elif _needs_repair(ev, row["synced_at"]):
                    out.append({"kind": "edited", "uid": uid, "gid": gid, "synced_at": row["synced_at"], **google_fields(ev)})
            elif ev.get("status") != "cancelled" and not ev.get("recurringEventId"):
                out.append({"kind": "created", "gid": gid, "repeats": bool(ev.get("recurrence")), **google_fields(ev)})
        return out

    async def delete_event(self, sid: str, gid: str):
        """Delete one event from a destination's Google calendar (one added there, once it's copied in)."""
        calendar_id = self.cal_info(sid).get("calendar_id")
        if calendar_id:
            await self.api("DELETE", f"/calendars/{_quote(calendar_id)}/events/{gid}", ok_missing=True)

    async def sync(self, sid: str, events: list, name: str, color_for, first_day: date, full: bool = False,
                   hold: set | frozenset = frozenset()) -> SyncResult:
        """Write a destination's events (from its sources) to its calendar in Google.

        `events` are the published events (calsync.Event); hidden ones are left out. `color_for(event)`
        gives its #rrggbb color (its own, a rule's or its source's) or "". Only events ending after `first_day` are written; older
        ones are left as they are. Normally only events that changed since the last sync are sent;
        with `full`, Google's copy is also checked and anything changed or deleted there is repaired."""
        tz = ZoneInfo(self.tz_name)
        result = SyncResult()
        info = self.cal_info(sid)
        calendar_id = info.get("calendar_id")
        if not calendar_id or info.get("synced_calendar") != calendar_id:
            full = True                       # a new calendar: nothing in it is known yet
        if full:
            calendar_id = await self.ensure_calendar(sid, name, calendar_id)
            if self.cal_info(sid).get("synced_calendar") != calendar_id:
                self.store.google_forget(source=sid)
                self._update_cal(sid, synced_calendar=calendar_id)
            old = self.cal_info(sid).get("replaced")
            if old:
                self._update_cal(sid, replaced=None)
                result.notes.append(f"the calendar \"{old}\" made with the earlier Google client can't be reached with this "
                                    "one (Google only lets an app see the calendars it made), so a new one was made; "
                                    f"delete the old \"{old}\" in Google Calendar by hand")
        try:
            return await self._sync(sid, calendar_id, events, name, color_for, first_day, tz, full, result, hold)
        except CalendarMissing:
            # Deleted in Google since the last check: make a new one and write everything again.
            self._update_cal(sid, calendar_id=None, synced_calendar=None)
            calendar_id = await self.ensure_calendar(sid, name)
            self.store.google_forget(source=sid)
            self._update_cal(sid, synced_calendar=calendar_id)
            result = SyncResult(notes=[f"the calendar {name} was missing in Google, so a new one was made"])
            return await self._sync(sid, calendar_id, events, name, color_for, first_day, tz, True, result, hold)

    async def _sync(self, sid, calendar_id, events, name, color_for, first_day, tz, full, result, hold=frozenset()) -> SyncResult:
        cal = f"/calendars/{_quote(calendar_id)}"
        if self.cal_info(sid).get("calendar_name") != name:          # keep the name in step
            if await self.api("PATCH", cal, body={"summary": name}, ok_missing=True) is None:
                raise CalendarMissing()
            self._update_cal(sid, calendar_name=name)
            result.renamed = True

        wanted = {e.uid: e for e in events if not e.hidden and in_window(e, first_day, tz)}
        rows = self.store.google_rows(sid)
        remote = await self._list_events(cal, first_day, tz) if full else None
        writes = 0

        for uid, e in wanted.items():
            if uid in hold:              # deleted in Google, waiting for the person to choose: left as it is
                result.unchanged += 1
                continue
            color = color_for(e)
            body = event_body(e, self.tz_name, nearest_color_id(color) if color else "")
            digest, gid, row = _hash(body), body["id"], rows.get(uid)
            same = row and row["hash"] == digest
            if same and (remote is None or not _needs_repair(remote.get(gid), row["synced_at"])):
                result.unchanged += 1
                continue
            if writes >= MAX_WRITES:
                result.more = True
                continue
            await self._put_event(cal, gid, body, known=bool(row) or bool(remote and gid in remote))
            if same:
                result.repaired += 1
            elif row:
                result.updated += 1
            else:
                result.added += 1
            self.store.google_saved(uid, gid, digest, e.end, sid)
            writes += 1

        wanted_ids = {event_id(uid) for uid in wanted}
        for uid, row in rows.items():
            if uid in wanted:
                continue
            if _ends_in_window(row["ends"], first_day, tz) and writes < MAX_WRITES:
                await self.api("DELETE", f"{cal}/events/{row['google_id']}", ok_missing=True)
                result.removed += 1
                writes += 1
            elif writes >= MAX_WRITES:
                result.more = True
                continue
            self.store.google_forget(uid, sid)  # past events: left in Google, no longer tracked

        if remote:   # events CalendarStream wrote that it no longer knows about (e.g. a lost database)
            for gid, ev in remote.items():
                if gid not in wanted_ids and ev.get("status") != "cancelled" and writes < MAX_WRITES:
                    await self.api("DELETE", f"{cal}/events/{gid}", ok_missing=True)
                    result.removed += 1
                    writes += 1

        when = datetime.now(timezone.utc).isoformat()
        self._update_cal(sid, last_sync=when, events=len(wanted))
        self._update_info(last_sync=when, last_result=result.summary(), last_error=None)
        return result

    async def _list_events(self, cal: str, first_day: date, tz: ZoneInfo) -> dict[str, dict]:
        """CalendarStream's events in Google that end after first_day (deleted ones included)."""
        found, page = {}, None
        start = datetime.combine(first_day, datetime.min.time(), tz).isoformat()
        while True:
            params = {"timeMin": start, "showDeleted": "true", "maxResults": "2500",
                      "privateExtendedProperty": f"{MARKER}=1"}
            if page:
                params["pageToken"] = page
            data = await self.api("GET", f"{cal}/events", params=params, ok_missing=True)
            if data is None:
                raise CalendarMissing()
            for ev in data.get("items", []):
                found[ev["id"]] = ev
            page = data.get("nextPageToken")
            if not page:
                return found

    async def _put_event(self, cal: str, gid: str, body: dict, known: bool):
        """Create or replace one event. Its ID is fixed, so this never makes duplicates: Google answers
        409 to a second insert (including for a deleted event, which a replace brings back)."""
        if known:
            if await self.api("PUT", f"{cal}/events/{gid}", body=body, ok_missing=True) is not None:
                return
        try:
            if await self.api("POST", f"{cal}/events", body=body, ok_missing=True) is None:
                raise CalendarMissing()
        except Conflict:
            await self.api("PUT", f"{cal}/events/{gid}", body=body)


def google_fields(ev: dict) -> dict:
    """A Google event's title, times, place and notes, as CalendarStream keeps them."""
    start, end = ev.get("start") or {}, ev.get("end") or {}
    all_day = "date" in start
    notes = (ev.get("description") or "")
    if notes.endswith(SYNC_NOTE):
        notes = notes[: -len(SYNC_NOTE)]
    return {"title": (ev.get("summary") or "")[:200], "all_day": all_day,
            "start": start.get("date") if all_day else start.get("dateTime", ""),
            "end": end.get("date") if all_day else end.get("dateTime", ""),
            "location": (ev.get("location") or "").strip()[:200], "description": notes.strip()[:4000],
            "at": ev.get("updated", "")}


def _needs_repair(remote: dict | None, synced_at) -> bool:
    """Whether Google's copy was deleted or changed by hand after CalendarStream last wrote it."""
    if remote is None or remote.get("status") == "cancelled":
        return True
    try:
        updated = datetime.fromisoformat(remote["updated"].replace("Z", "+00:00"))
    except (KeyError, ValueError):
        return False
    return updated > synced_at + timedelta(seconds=30)


def _error_reason(r: httpx.Response) -> str:
    try:
        errors = r.json().get("error", {}).get("errors") or [{}]
        return errors[0].get("reason", "")
    except (ValueError, AttributeError):
        return ""


def _quote(calendar_id: str) -> str:
    return quote(calendar_id, safe="")
