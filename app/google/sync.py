"""Google Calendar's calendars and events: making and deleting a module's calendar, its color, push notices, pulling
Google's changes, and the 1-way / 2-way reconciliation of events (checkpoints, conflicts), plus the pure event
helpers they use.

Holds: GoogleSync (the calendar/event/watch methods a Google account's connection has; it is a mixin, so it uses
  `self.api(...)`, `self.store`, `self.info()` and `self._update_info()` of GoogleApi, and `self.REVOKE_URL`),
  SyncResult, event_body, event_id, in_window, google_fields, nearest_color_id and the colour tables.
Depends on: app/calsync.py (meeting links), app/google/errors.py, app/google/api.py (what a host provides);
  httpx, the standard library.
Used by: app/gsync.py (`Google(GoogleApi, GoogleSync)`, and re-exports these names for the rest of the app and
  the suites); app/main.py and the routes through gsync.
Reads/writes: the database through `self.store` (per-account details: calendars, checkpoints, watch channels); the
  network through `self.api`; the clock.
Dart note: this becomes a `SyncEngine` (domain) that is handed a `GoogleApi` client (data) instead of being mixed in:
  the pure helpers (`eventBody`, `inWindow`, `SyncResult`...) are separate classes/files there. The mixin is the
  interim step here; the calls through `self.api` are the seam to cut.
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import secrets
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from urllib.parse import quote

import httpx

from ..calsync import meeting_link, notes_with_meeting
from .api import TIMEOUT
from .errors import AccessRevoked, CalendarMissing, Conflict, GoogleError

log = logging.getLogger("calendar_stream.google")

MAX_WRITES = 1500          # Google writes in one sync at most; the rest wait for the next one
SYNC_NOTE = "Synced by CalendarStream"
MARKER = "calendarstream"   # private extended property on every event CalendarStream writes

GOOGLE_COLORS = {
    "11": ("Tomato", "#d50000"), "4": ("Flamingo", "#e67c73"), "6": ("Tangerine", "#f4511e"),
    "5": ("Banana", "#f6bf26"), "2": ("Sage", "#33b679"), "10": ("Basil", "#0b8043"),
    "7": ("Peacock", "#039be5"), "9": ("Blueberry", "#3f51b5"), "1": ("Lavender", "#7986cb"),
    "3": ("Grape", "#8e24aa"), "8": ("Graphite", "#616161"),
}

# (0.2.8-beta.21, I1) Google's calendar colors (its calendar palette, not the event colors above): colorId -> hex.
CALENDAR_COLORS = {
    "1": "#ac725e", "2": "#d06b64", "3": "#f83a22", "4": "#fa573c", "5": "#ff7537", "6": "#ffad46",
    "7": "#42d692", "8": "#16a765", "9": "#7bd148", "10": "#b3dc6c", "11": "#fbe983", "12": "#fad165",
    "13": "#92e1c0", "14": "#9fe1e7", "15": "#9fc6e7", "16": "#4986e7", "17": "#9a9cff", "18": "#b99aff",
    "19": "#c2c2c2", "20": "#cabdbf", "21": "#cca6ac", "22": "#f691b2", "23": "#cd74e6", "24": "#a47ae2",
}
# (0.2.8-beta.21, I1) the ways a calendar's color is sent to Google, in the order they're tried: its RGB color; the
# nearest of Google's calendar colors (colorId); a full update of the calendar's entry (PUT). The one Google takes is kept.
COLOR_WAYS = ("rgb", "colorId", "put")

WATCH_TTL = 7 * 24 * 3600   # seconds a push-notification channel lasts (Google's default and usual limit)

CALENDAR_DESCRIPTION = ("Kept up to date by CalendarStream. "
                        "Changes made here may be overwritten at the next sync.")
CAL_KEYS = ("calendar_id", "calendar_name", "synced_calendar", "created", "last_sync", "events")


class _SkipRevoke(Exception):
    """Internal: disconnect without revoking the grant in Google."""

def _rgb(hex_color: str) -> tuple[int, int, int]:
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def nearest_color_id(hex_color: str) -> str:
    """The Google event color closest to a #rrggbb color."""
    r, g, b = _rgb(hex_color)
    return min(GOOGLE_COLORS, key=lambda cid: sum((x - y) ** 2 for x, y in zip((r, g, b), _rgb(GOOGLE_COLORS[cid][1]))))


def nearest_calendar_color(hex_color: str) -> str:
    """(0.2.8-beta.21, I1) The colorId of Google's calendar color closest to a #rrggbb color."""
    r, g, b = _rgb(hex_color)
    return min(CALENDAR_COLORS, key=lambda cid: sum((x - y) ** 2 for x, y in zip((r, g, b), _rgb(CALENDAR_COLORS[cid]))))


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
        "description": (notes_with_meeting(e) + "\n\n" if notes_with_meeting(e) else "") + SYNC_NOTE,
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


class GoogleSync:
    """The calendar and event side of a Google account (see this file's header)."""

    MAX_WRITES = MAX_WRITES    # (an attribute so a host or a suite can change it: gsync.Google reads gsync.MAX_WRITES)

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


    async def ensure_calendar(self, sid: str, name: str, calendar_id: str | None = None) -> str:
        """Use a source's calendar if it still exists in Google, otherwise create it."""
        info = self.cal_info(sid)
        # its own calendar first; `calendar_id` is one remembered for the module from an earlier sign-in (0.2.8-beta.18, I5)
        remembered = calendar_id if not info.get("calendar_id") else None
        calendar_id = info.get("calendar_id") or calendar_id
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
            if not remembered and (unreachable or (info.get("client") and info.get("client") != self.client_id)):
                self._update_cal(sid, replaced=info.get("calendar_name") or name)
        made = await self.api("POST", "/calendars", body={
            "summary": name, "timeZone": self.tz_name,
            "description": CALENDAR_DESCRIPTION})
        self._update_cal(sid, calendar_id=made["id"], calendar_name=made.get("summary", name), created=True, client=self.client_id,
                         shown=False)   # (0.2.8-beta.19, F7) not shown yet: the next Sync Now shows it in Google Calendar
        return made["id"]

    async def set_color(self, sid: str, color: str) -> str:
        """The calendar's color in the person's Google Calendar (0.2.8-beta.15: a Google module's color box). Returns the
        way Google took it (COLOR_WAYS), "" without a calendar. (0.2.8-beta.21, I1) Google may refuse the RGB color
        (HTTP 401 on the calendar list, with a sign-in that works everywhere else), so a refusal tries the next way;
        the way Google took last time is tried first. Refused every way: GoogleError with Google's own reasons."""
        info = self.cal_info(sid)
        calendar_id = info.get("calendar_id")
        if not calendar_id:
            return ""
        kept = info.get("color_way")
        ways = ([kept] if kept in COLOR_WAYS else []) + [w for w in COLOR_WAYS if w != kept]
        refused: list[str] = []
        for way in ways:
            try:
                await self._send_color(calendar_id, way, color)
            except AccessRevoked:
                raise
            except GoogleError as e:
                if not str(e).startswith("Google Calendar refused"):
                    raise                     # Google out of reach or busy: no other way would fare better now
                if str(e) not in refused:
                    refused.append(str(e))
                continue
            self._update_cal(sid, color=color, color_way=way)
            return way
        raise GoogleError("; ".join(refused))

    async def _send_color(self, calendar_id: str, way: str, color: str):
        path = f"/users/me/calendarList/{_quote(calendar_id)}"
        if way == "rgb":
            await self.api("PATCH", path, params={"colorRgbFormat": "true"},
                           body={"backgroundColor": color, "foregroundColor": "#ffffff"})
        elif way == "colorId":
            await self.api("PATCH", path, body={"colorId": nearest_calendar_color(color)})
        else:
            # a PUT replaces the whole entry: start from Google's own copy so nothing else in it changes
            try:
                entry = await self.api("GET", path, ok_missing=True) or {}
            except GoogleError as e:
                if not str(e).startswith("Google Calendar refused"):
                    raise
                entry = {}
            body = {k: v for k, v in entry.items() if k not in ("colorId", "etag", "kind")}
            body.setdefault("selected", True)
            body.setdefault("hidden", False)
            body.update(id=calendar_id, backgroundColor=color, foregroundColor="#ffffff")
            await self.api("PUT", path, params={"colorRgbFormat": "true"}, body=body)

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

    async def disconnect(self, delete_calendar: bool, revoke: bool = True) -> list[str]:
        """Optionally delete CalendarStream's calendar, revoke the sign-in in Google and forget it.
        The local sign-in is always forgotten; returns notes on anything Google didn't confirm. revoke=False
        (0.2.8-beta.17, I5): only forget it here. Google revokes a whole grant, so revoking one sign-in of a
        Gmail also signs out every other module using the same Gmail."""
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
            if not revoke:
                raise _SkipRevoke
            token = self._refresh_token()
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.post(self.REVOKE_URL, data={"token": token})
            if r.status_code not in (200, 400):   # 400: Google had already dropped it
                notes.append(f"Google didn't confirm removing access (HTTP {r.status_code}); "
                             "remove CalendarStream at myaccount.google.com/permissions")
        except (GoogleError, httpx.HTTPError):
            notes.append("couldn't reach Google to remove access; remove CalendarStream at "
                         "myaccount.google.com/permissions")
        except _SkipRevoke:
            pass
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
                elif _needs_repair(ev, row):
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
            if same and (remote is None or not _needs_repair(remote.get(gid), row)):
                result.unchanged += 1
                continue
            if writes >= self.MAX_WRITES:
                result.more = True
                continue
            stamp = await self._put_event(cal, gid, body, known=bool(row) or bool(remote and gid in remote))
            if same:
                result.repaired += 1
            elif row:
                result.updated += 1
            else:
                result.added += 1
            self.store.google_saved(uid, gid, digest, e.end, sid, stamp)
            writes += 1

        wanted_ids = {event_id(uid) for uid in wanted}
        for uid, row in rows.items():
            if uid in wanted:
                continue
            if _ends_in_window(row["ends"], first_day, tz) and writes < self.MAX_WRITES:
                await self.api("DELETE", f"{cal}/events/{row['google_id']}", ok_missing=True)
                result.removed += 1
                writes += 1
            elif writes >= self.MAX_WRITES:
                result.more = True
                continue
            self.store.google_forget(uid, sid)  # past events: left in Google, no longer tracked

        if remote:   # events CalendarStream wrote that it no longer knows about (e.g. a lost database)
            for gid, ev in remote.items():
                if gid in wanted_ids or ev.get("status") == "cancelled":
                    continue
                if writes >= self.MAX_WRITES:      # (review #3.2) the rest waits for the next sync, and says so
                    result.more = True
                    break
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

    async def _put_event(self, cal: str, gid: str, body: dict, known: bool) -> str:
        """Create or replace one event; returns Google's "updated" time on the copy written. Its ID is fixed, so
        this never makes duplicates: Google answers 409 to a second insert (including for a deleted event,
        which a replace brings back)."""
        if known:
            done = await self.api("PUT", f"{cal}/events/{gid}", body=body, ok_missing=True)
            if done is not None:
                return str(done.get("updated") or "")
        try:
            done = await self.api("POST", f"{cal}/events", body=body, ok_missing=True)
            if done is None:
                raise CalendarMissing()
        except Conflict:
            done = await self.api("PUT", f"{cal}/events/{gid}", body=body)
        return str((done or {}).get("updated") or "")


def google_fields(ev: dict) -> dict:
    """A Google event's title, times, place and notes, as CalendarStream keeps them."""
    start, end = ev.get("start") or {}, ev.get("end") or {}
    all_day = "date" in start
    notes = (ev.get("description") or "")
    if notes.endswith(SYNC_NOTE):
        notes = notes[: -len(SYNC_NOTE)]
    # (0.2.8-beta.28, F6) the online meeting link CalendarStream puts first isn't part of the notes
    first, _, rest = notes.strip().partition("\n")
    if first.strip() and first.strip() == meeting_link(first.strip()) and (not rest.strip() or rest.startswith("\n")):
        notes = rest
    return {"title": (ev.get("summary") or "")[:200], "all_day": all_day,
            "start": start.get("date") if all_day else start.get("dateTime", ""),
            "end": end.get("date") if all_day else end.get("dateTime", ""),
            "location": (ev.get("location") or "").strip()[:200], "description": notes.strip()[:4000],
            "at": ev.get("updated", "")}


def _needs_repair(remote: dict | None, row: dict) -> bool:
    """Whether Google's copy was deleted or changed by hand after CalendarStream last wrote it. Google changes
    an event's "updated" time on every change, so a copy whose time isn't the one our write got was changed
    there, however soon after (review #3.1). A row from before 0.2.8-beta.18 has no time kept: then by the
    clock, allowing 30 s between the two clocks."""
    if remote is None or remote.get("status") == "cancelled":
        return True
    if row.get("remote_updated"):
        return str(remote.get("updated") or "") != row["remote_updated"]
    try:
        updated = datetime.fromisoformat(remote["updated"].replace("Z", "+00:00"))
    except (KeyError, ValueError):
        return False
    return updated > row["synced_at"] + timedelta(seconds=30)




def _quote(calendar_id: str) -> str:
    return quote(calendar_id, safe="")
