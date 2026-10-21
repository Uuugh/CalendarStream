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
from urllib.parse import quote, urlencode

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

# Google Calendar's event colours, as its apps show them: colorId -> (name, hex).
GOOGLE_COLORS = {
    "11": ("Tomato", "#d50000"), "4": ("Flamingo", "#e67c73"), "6": ("Tangerine", "#f4511e"),
    "5": ("Banana", "#f6bf26"), "2": ("Sage", "#33b679"), "10": ("Basil", "#0b8043"),
    "7": ("Peacock", "#039be5"), "9": ("Blueberry", "#3f51b5"), "1": ("Lavender", "#7986cb"),
    "3": ("Grape", "#8e24aa"), "8": ("Graphite", "#616161"),
}

CALENDAR_DESCRIPTION = ("Your United CCS+ schedule, kept up to date by CalendarStream. "
                        "Changes made here may be overwritten at the next sync.")


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
    """The Google event colour closest to a #rrggbb colour."""
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
        "reminders": {"useDefault": False, "overrides": []},     # decision 3: no reminders
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
    def __init__(self, store, box: SecretBox, tz_name: str):
        self.store = store
        self.box = box
        self._client: tuple[str, str] | None = None              # (client ID, secret), read once
        self.tz_name = tz_name
        self._pending: dict[str, tuple[str, str, float]] = {}   # state -> (PKCE verifier, redirect URI, expiry)
        self._access: tuple[str, float] | None = None            # (access token, expiry)
        self._lock = asyncio.Lock()

    # --- What the status page shows ------------------------------------------------

    # --- The OAuth client (entered in the Settings menu) -------------------------------

    def client(self) -> tuple[str, str]:
        """The OAuth client ID and secret saved in the Settings menu, or ("", "")."""
        if self._client is None:
            saved = self.store.get("google_client") or {}
            secret = self._unseal(saved["secret"], "") if saved.get("secret") else ""
            self._client = (saved.get("id", ""), secret)
        return self._client

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
        """Save the OAuth client. A blank secret keeps the one already saved (the menu never shows it)."""
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
        """The last check of the saved client: {"ok": True/False/None, "message", "at"}."""
        return (self.store.get("google_client") or {}).get("check") or {}

    def _save_check(self, ok: bool | None, message: str):
        saved = self.store.get("google_client")
        if saved:
            saved["check"] = {"ok": ok, "message": message, "at": datetime.now(timezone.utc).isoformat()}
            self.store.set("google_client", saved)

    async def check_client(self, redirect_uri: str) -> dict:
        """Ask Google whether it accepts the saved client ID and secret, without signing anyone in:
        swap a made-up code. Google answers "invalid_grant" (bad code) only once the client ID and
        secret are right, and "invalid_client" when either is wrong. The redirect URI and consent
        screen are only checked when someone connects."""
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
        if error in ("invalid_grant", "redirect_uri_mismatch"):
            self._save_check(True, "Google accepted the client ID and secret")
        elif error in ("invalid_client", "unauthorized_client"):
            self._save_check(False, "Google doesn't know this client ID" if "not found" in detail
                             else "Google rejected the client secret")
        else:
            self._save_check(None, f"Google gave an unexpected answer ({error or r.status_code})")
        return self.client_check()

    def clear_client(self):
        self.store.delete("google_client")
        self._client = None
        self._access = None

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
        self.store.set("google_token", self._seal(token))

    def _refresh_token(self) -> str:
        saved = self.store.get("google_token")
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
        self._save_check(True, "Google accepted the client ID and secret")
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

    # --- Keeping the events in step -------------------------------------------------------

    async def sync(self, events: list, name: str, color_for, first_day: date, full: bool = False) -> SyncResult:
        """Write the schedule to CalendarStream's calendar in Google.

        `events` are the published events (calsync.Event); hidden ones are left out. `color_for(title)`
        gives a tag's #rrggbb colour or "". Only events ending after `first_day` are written; older
        ones are left as they are. Normally only events that changed since the last sync are sent;
        with `full`, Google's copy is also checked and anything changed or deleted there is repaired."""
        tz = ZoneInfo(self.tz_name)
        result = SyncResult()
        info = self.info()
        calendar_id = info.get("calendar_id")
        if not calendar_id or info.get("synced_calendar") != calendar_id:
            full = True                       # a new calendar: nothing in it is known yet
        if full:
            calendar_id = await self.ensure_calendar(name, calendar_id)
            if self.info().get("synced_calendar") != calendar_id:
                self.store.google_forget()
                self._update_info(synced_calendar=calendar_id)
        try:
            return await self._sync(calendar_id, events, name, color_for, first_day, tz, full, result)
        except CalendarMissing:
            # Deleted in Google since the last check: make a new one and write everything again.
            self._update_info(calendar_id=None, synced_calendar=None)
            calendar_id = await self.ensure_calendar(name)
            self.store.google_forget()
            self._update_info(synced_calendar=calendar_id)
            result = SyncResult(notes=["the calendar was missing in Google, so a new one was made"])
            return await self._sync(calendar_id, events, name, color_for, first_day, tz, True, result)

    async def _sync(self, calendar_id, events, name, color_for, first_day, tz, full, result) -> SyncResult:
        cal = f"/calendars/{_quote(calendar_id)}"
        if self.info().get("calendar_name") != name:          # F2: keep the name in step
            if await self.api("PATCH", cal, body={"summary": name}, ok_missing=True) is None:
                raise CalendarMissing()
            self._update_info(calendar_name=name)
            result.renamed = True

        wanted = {e.uid: e for e in events if not e.hidden and in_window(e, first_day, tz)}
        rows = self.store.google_rows()
        remote = await self._list_events(cal, first_day, tz) if full else None
        writes = 0

        for uid, e in wanted.items():
            color = e.color or color_for(e.title)   # a colour chosen for the event wins over tags
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
            self.store.google_saved(uid, gid, digest, e.end)
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
            self.store.google_forget(uid)       # past events: left in Google, no longer tracked

        if remote:   # events CalendarStream wrote that it no longer knows about (e.g. a lost database)
            for gid, ev in remote.items():
                if gid not in wanted_ids and ev.get("status") != "cancelled" and writes < MAX_WRITES:
                    await self.api("DELETE", f"{cal}/events/{gid}", ok_missing=True)
                    result.removed += 1
                    writes += 1

        self._update_info(last_sync=datetime.now(timezone.utc).isoformat(), last_result=result.summary(),
                          events=len(wanted), last_error=None)
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
