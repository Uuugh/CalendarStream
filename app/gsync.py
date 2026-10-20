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
import secrets
import time
from datetime import datetime, timezone
from urllib.parse import quote, urlencode

import httpx
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

log = logging.getLogger("calendar_stream.google")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
API_URL = "https://www.googleapis.com/calendar/v3"
SCOPE_CALENDAR = "https://www.googleapis.com/auth/calendar.app.created"
SCOPES = ("openid", "email", SCOPE_CALENDAR)

SIGN_IN_TTL = 15 * 60       # seconds a sign-in started here stays valid
MAX_PENDING = 20            # sign-ins started but not finished, kept at most
KDF_ROUNDS = 390_000        # PBKDF2-SHA256 rounds for the token key
TIMEOUT = httpx.Timeout(20.0, connect=10.0)

CALENDAR_DESCRIPTION = ("Your United CCS+ schedule, kept up to date by CalendarStream. "
                        "Changes made here may be overwritten at the next sync.")


class GoogleError(Exception):
    """Something went wrong talking to Google; the message is shown on the status page."""


class AccessRevoked(GoogleError):
    """Google no longer accepts the stored sign-in (revoked, expired or the password changed)."""


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


class Google:
    def __init__(self, store, client_id: str, client_secret: str, key_secret: str, tz_name: str):
        self.store = store
        self.client_id, self.client_secret = client_id, client_secret
        self._key_secret = key_secret
        self.tz_name = tz_name
        self._pending: dict[str, tuple[str, str, float]] = {}   # state -> (PKCE verifier, redirect URI, expiry)
        self._access: tuple[str, float] | None = None            # (access token, expiry)
        self._keys: dict[bytes, Fernet] = {}                     # salt -> key (deriving one is slow on purpose)
        self._lock = asyncio.Lock()

    # --- What the status page shows ------------------------------------------------

    @property
    def configured(self) -> bool:
        """The OAuth client ID and secret are present (Docker secrets)."""
        return bool(self.client_id and self.client_secret)

    def info(self) -> dict:
        """Saved connection details: email, calendar_id, calendar_name, connected_at, last_error."""
        return self.store.get("google") or {}

    def _update_info(self, **changes):
        info = self.info()
        info.update(changes)
        self.store.set("google", {k: v for k, v in info.items() if v not in (None, "")})

    @property
    def connected(self) -> bool:
        return self.store.get("google_token") is not None

    # --- The encrypted refresh token ---------------------------------------------------

    def _fernet(self, salt: bytes) -> Fernet:
        if not self._key_secret:
            raise GoogleError("DB_PASSWORD is needed to store the Google sign-in securely.")
        if salt not in self._keys:
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=KDF_ROUNDS)
            self._keys = {salt: Fernet(base64.urlsafe_b64encode(kdf.derive(self._key_secret.encode())))}
        return self._keys[salt]

    def _save_refresh_token(self, token: str):
        salt = secrets.token_bytes(16)
        sealed = self._fernet(salt).encrypt(token.encode()).decode()
        self.store.set("google_token", {"v": 1, "salt": _b64url(salt), "token": sealed})

    def _refresh_token(self) -> str:
        saved = self.store.get("google_token")
        if not saved:
            raise GoogleError("Google Calendar isn't connected.")
        try:
            salt = base64.urlsafe_b64decode(saved["salt"] + "=" * (-len(saved["salt"]) % 4))
            return self._fernet(salt).decrypt(saved["token"].encode()).decode()
        except (InvalidToken, KeyError, ValueError):
            raise AccessRevoked("The saved Google sign-in can't be read (was DB_PASSWORD changed?). "
                                "Disconnect and connect again.")

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

    async def finish_sign_in(self, state: str, code: str, calendar_name: str) -> dict:
        """Handle Google's answer: swap the code for tokens, check the permission was granted,
        save the refresh token and make sure CalendarStream's calendar exists. Returns the info."""
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
            self.store.set("google", {})
        self._save_refresh_token(refresh)
        self._access = (tokens["access_token"], time.monotonic() + int(tokens.get("expires_in", 3600)) - 60)
        self._update_info(email=email, connected_at=datetime.now(timezone.utc).isoformat(), last_error=None)
        await self.ensure_calendar(calendar_name, previous.get("calendar_id"))
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
            raise GoogleError("Google rejected the OAuth client: check GOOGLE_CLIENT_ID.txt and "
                              "GOOGLE_CLIENT_SECRET.txt.")
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

    async def ensure_calendar(self, name: str, calendar_id: str | None = None) -> str:
        """Use CalendarStream's calendar if it still exists in Google, otherwise create it."""
        calendar_id = calendar_id or self.info().get("calendar_id")
        if calendar_id:
            found = await self.api("GET", f"/calendars/{_quote(calendar_id)}", ok_missing=True)
            if found is not None:
                self._update_info(calendar_id=calendar_id, calendar_name=found.get("summary", name), created=False)
                return calendar_id
        made = await self.api("POST", "/calendars", body={
            "summary": name, "timeZone": self.tz_name, "description": CALENDAR_DESCRIPTION})
        self._update_info(calendar_id=made["id"], calendar_name=made.get("summary", name), created=True)
        return made["id"]

    # --- Disconnecting ------------------------------------------------------------------------

    async def disconnect(self, delete_calendar: bool) -> list[str]:
        """Optionally delete CalendarStream's calendar, revoke the sign-in in Google and forget it.
        The local sign-in is always forgotten; returns notes on anything Google didn't confirm."""
        notes = []
        info = self.info()
        try:
            if delete_calendar and info.get("calendar_id"):
                await self.api("DELETE", f"/calendars/{_quote(info['calendar_id'])}", ok_missing=True)
                info.pop("calendar_id", None)
                info.pop("calendar_name", None)
        except GoogleError as e:
            notes.append(f"the calendar wasn't deleted ({e})")
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
        self.store.delete("google_token")
        self._access = None
        # Keep the calendar ID (unless deleted) so reconnecting the same account reuses that calendar.
        info.pop("connected_at", None)
        info.pop("last_error", None)
        info.pop("created", None)
        self.store.set("google", info)
        return notes

    def record_error(self, message: str):
        self._update_info(last_error=message)


def _error_reason(r: httpx.Response) -> str:
    try:
        errors = r.json().get("error", {}).get("errors") or [{}]
        return errors[0].get("reason", "")
    except (ValueError, AttributeError):
        return ""


def _quote(calendar_id: str) -> str:
    return quote(calendar_id, safe="")
