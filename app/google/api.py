"""Google's OAuth and HTTP side: the OAuth client, the sign-in (PKCE), the encrypted refresh token, access tokens,
an account's saved details, and the authenticated request to Calendar's API.

Holds: GoogleApi (one Google account's connection; the calendar and event work is in app/gsync.py's Google, which
  builds on it until F58 checkpoint 8 moves that into app/google/sync.py).
Depends on: app/secretbox.py (encrypts the secrets), app/google/errors.py, app/google/traffic_entry.py,
  app/google/traffic_log.py (F59: every call to Google is recorded there, unredacted, for the Beta traffic view);
  httpx; the store it is given.
Used by: app/gsync.py (Google extends it, and re-exports it for the rest of the app).
Reads/writes: the database through the `store` it is given (keys `google_client`, `google[:account]`,
  `google_token[:account]`, `google_signins`); the network (Google's sign-in, token and Calendar endpoints); the clock.
Dart note: `class GoogleApi`, data layer. `store` becomes a `KeyValueStore` interface and the HTTP client an injected
  `http.Client` so tests can fake both. The three endpoint URLs are constructor arguments there; here they are
  attributes so the test suites can point them at the mock Google (gsync passes its own module values through,
  which is where the suites set them).
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
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlencode, urlparse

import httpx

from ..secretbox import SecretBox
from .errors import AccessRevoked, Conflict, GoogleError
from .traffic_entry import TrafficEntry
from .traffic_log import TrafficLog

log = logging.getLogger("calendar_stream.google")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API_URL = "https://www.googleapis.com/calendar/v3"
SCOPE_CALENDAR = "https://www.googleapis.com/auth/calendar.app.created"
SCOPES = ("openid", "email", SCOPE_CALENDAR)

SIGN_IN_TTL = 15 * 60       # seconds a sign-in started here stays valid
SIGNINS_KEY = "google_signins"   # database key: sign-ins started and not finished, by state (all accounts)
MAX_PENDING = 20            # sign-ins started but not finished, kept at most
TIMEOUT = httpx.Timeout(20.0, connect=10.0)
FRESH_TOKEN = 60.0         # seconds an access token counts as just issued: a 401 with it isn't fixed by another (I1)




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



class GoogleApi:
    def __init__(self, store, box: SecretBox, tz_name: str, account: str = "", traffic: TrafficLog | None = None):
        self.store = store
        self.box = box
        self.traffic = traffic or TrafficLog()   # (F59) every call is recorded here for the Beta traffic view
        # 0.2.8-beta.15: one Google account per instance (each Google module can use its own Gmail); the
        # first ("") keeps the keys it always had, so installs from before need nothing moved. The OAuth
        # client is shared by every account.
        self.account = account
        self._info_key = "google" + (f":{account}" if account else "")
        self._token_key = "google_token" + (f":{account}" if account else "")
        self._client: tuple[str, str] | None = None              # (kept for callers from before; read each time now)
        self.tz_name = tz_name
        self._access: tuple[str, float] | None = None            # (access token, expiry)
        self._access_at = 0.0     # (0.2.8-beta.21, I1) when Google issued the access token (time.monotonic())
        self._lock = asyncio.Lock()

    AUTH_URL, TOKEN_URL, API_URL = AUTH_URL, TOKEN_URL, API_URL   # endpoints (see the Dart note)

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
                r = await client.post(self.TOKEN_URL, data={
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
        url = self.AUTH_URL + "?" + urlencode({
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
        # (0.2.8-beta.35, F58 4) kept in the database, not in memory, so a restart between this page and Google's
        # answer doesn't lose it; the PKCE verifier is stored encrypted, and used once (finish_sign_in)
        now = time.time()
        pending = {k: v for k, v in (self.store.get(SIGNINS_KEY) or {}).items() if v.get("expires", 0) > now}
        while len(pending) >= MAX_PENDING:
            pending.pop(next(iter(pending)))
        state, verifier = secrets.token_urlsafe(24), secrets.token_urlsafe(48)
        pending[state] = {"account": self.account, "verifier": self._seal(verifier), "redirect": redirect_uri,
                          "expires": now + SIGN_IN_TTL}
        self.store.set(SIGNINS_KEY, pending)
        return self.AUTH_URL + "?" + urlencode({
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

    def owns_sign_in(self, state: str) -> bool:
        """Was this sign-in `state` started for this account, and is it still valid?"""
        rec = (self.store.get(SIGNINS_KEY) or {}).get(state or "")
        return bool(rec) and rec.get("account") == self.account and rec.get("expires", 0) > time.time()

    def _take_sign_in(self, state: str) -> dict | None:
        """Use a started sign-in up: returned once, then gone (a second answer for the same state finds nothing)."""
        pending = self.store.get(SIGNINS_KEY) or {}
        rec = pending.pop(state or "", None)
        self.store.set(SIGNINS_KEY, pending)
        if not rec or rec.get("account") != self.account or rec.get("expires", 0) < time.time():
            return None
        return rec

    async def finish_sign_in(self, state: str, code: str) -> dict:
        """Handle Google's answer: swap the code for tokens, check the permission was granted and
        save the refresh token. The calendars are made (or found again) by the next sync. Returns the info."""
        pending = self._take_sign_in(state)
        if not pending:
            raise GoogleError("This Google sign-in has expired or was already used. Try Connect again.")
        verifier, redirect_uri = self._unseal(pending["verifier"]), pending["redirect"]
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
        email = claims.get("email", "") if claims.get("aud") == self.client_id else ""   # (REVIEW 2, #11 #4) a missing audience is not trusted

        previous = self.info()
        if previous.get("email") and email and previous["email"] != email:
            # A different account: its calendar is a different one.
            previous = {}
            self.store.set(self._info_key, {})
        self._save_refresh_token(refresh)
        self._save_check(True, "Google accepted the client ID and secret", redirect_uri, True)   # signed in: both proven
        self._access = (tokens["access_token"], time.monotonic() + int(tokens.get("expires_in", 3600)) - 60)
        self._access_at = time.monotonic()
        self._update_info(email=email, connected_at=datetime.now(timezone.utc).isoformat(), last_error=None)
        return self.info()

    async def _token_request(self, form: dict) -> dict:
        form = {**form, "client_id": self.client_id, "client_secret": self.client_secret}
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.post(self.TOKEN_URL, data=form)
        except httpx.HTTPError as e:
            self._record_traffic("POST", self.TOKEN_URL, form, time.monotonic() - start, status="error",
                                 response_body=f"{type(e).__name__}: {e}")
            raise GoogleError(f"Couldn't reach Google ({type(e).__name__}).", transient=True)
        try:
            body = r.json()
        except ValueError:
            body = {}
        self._record_traffic("POST", self.TOKEN_URL, form, time.monotonic() - start, response=r)
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
            self._access_at = time.monotonic()
            return self._access[0]

    def _record_traffic(self, method: str, url: str, request_body, seconds: float, *, response: httpx.Response | None = None,
                        status=None, response_body: str = "", request_headers: dict | None = None):
        """(F59) One exchange, kept for the Beta traffic view. Nothing is redacted (not the access or
        refresh token, not the client secret): the Developer asked to see everything, it's their own
        account, and this never leaves memory (no database, report, log file or screenshot)."""
        try:
            req_body = request_body if isinstance(request_body, str) else json.dumps(request_body, default=str)
        except TypeError:
            req_body = str(request_body)
        if response is not None:
            status = response.status_code
            response_body = response.text
            response_headers = dict(response.headers)
        else:
            response_headers = {}
        self.traffic.record(TrafficEntry(at=time.time(), account=self.account, method=method, url=url,
                                         request_headers=dict(request_headers or {}), request_body=req_body,
                                         status=status, response_headers=response_headers,
                                         response_body=response_body[:20000], ms=seconds * 1000))

    # --- Calendar API -------------------------------------------------------------------------

    async def api(self, method: str, path: str, *, body: dict | None = None, params: dict | None = None,
                  ok_missing: bool = False) -> dict | None:
        """Call the Calendar API. Retries once with a fresh access token on 401 and backs off on
        rate limits and server errors. With ok_missing, a 404/410 returns None instead of failing."""
        delay = 1.0
        renewed = False                # (0.2.8-beta.19, I1) a fresh access token was already tried for this call
        for attempt in range(5):
            fresh = not (self._access and self._access[1] > time.monotonic())
            token = await self._access_token()
            # (0.2.8-beta.21, I1) a token Google issued in the last minute is fresh for every call, not only the one
            # that got it: the next ways of setting a color aren't each retried with yet another token
            fresh = fresh or time.monotonic() - self._access_at < FRESH_TOKEN
            renewed = renewed or fresh
            headers = {"Authorization": f"Bearer {token}"}
            start = time.monotonic()
            try:
                async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                    r = await client.request(method, self.API_URL + path, json=body, params=params,
                                             headers=headers)
            except httpx.HTTPError as e:
                self._record_traffic(method, self.API_URL + path, body or params, time.monotonic() - start,
                                     status="error", response_body=f"{type(e).__name__}: {e}", request_headers=headers)
                if attempt == 4:
                    raise GoogleError(f"Couldn't reach Google Calendar ({type(e).__name__}).", transient=True)
                await asyncio.sleep(delay)
                delay *= 2
                continue
            self._record_traffic(method, self.API_URL + path, body or params, time.monotonic() - start,
                                 response=r, request_headers=headers)
            if r.status_code in (200, 201):
                return r.json() if r.content else {}
            if r.status_code == 204:
                return {}
            if r.status_code in (404, 410) and ok_missing:
                return None
            reason = _error_reason(r)
            if r.status_code == 409:
                raise Conflict(f"Google Calendar: {reason or 'conflict'}")
            if r.status_code == 401 and not renewed:
                self._access = None              # expired early: get a new access token once
                continue
            if r.status_code == 429 or r.status_code >= 500 or reason in ("rateLimitExceeded", "userRateLimitExceeded"):
                if attempt < 4:
                    await asyncio.sleep(delay)
                    delay *= 2
                    continue
            # (0.2.8-beta.19, I1) Google's own words, never a guess: a 401 here came with an access token Google had
            # just issued for this sign-in, so the sign-in itself works (a sign-in Google no longer accepts fails at
            # the token request, as AccessRevoked) and signing in again can't fix it.
            said = _error_message(r)
            log.warning("Google Calendar refused %s %s: HTTP %s %s", method, path.split("?")[0], r.status_code,
                        r.text[:2000])
            raise GoogleError(f"Google Calendar refused {method} {path.split('?')[0]}: HTTP {r.status_code}"
                              + (f" {reason}" if reason else "") + (f", “{said}”" if said else ""), status=r.status_code)
        raise GoogleError("Google Calendar is busy; CalendarStream will try again later.", transient=True)


def _error_reason(r: httpx.Response) -> str:
    try:
        errors = r.json().get("error", {}).get("errors") or [{}]
        return errors[0].get("reason", "")
    except (ValueError, AttributeError):
        return ""


def _error_message(r: httpx.Response) -> str:
    """Google's own explanation of a refused request (0.2.8-beta.19, I1): its message, and the detail's when it
    says more; one line, at most 300 characters."""
    try:
        err = r.json().get("error", {})
        if not isinstance(err, dict):
            return str(err)[:300]
        said = [err.get("message") or ""]
        for e in err.get("errors") or []:
            m = (e or {}).get("message") or ""
            if m and m not in said[0]:
                said.append(m)
        return " · ".join(s for s in said if s).replace("\n", " ")[:300]
    except (ValueError, AttributeError):
        return ""
