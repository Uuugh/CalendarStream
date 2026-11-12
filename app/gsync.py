"""Google Calendar, as the rest of the app imports it: the facade over app/google/ (F58 checkpoint 8; checkpoint
10: GoogleSync is handed this connection instead of being mixed into it).

`Google` is one account's connection (GoogleApi: sign-in, tokens, requests); it holds a GoogleSync (its calendar
and event work), handed `self` as its `api_client`, and forwards GoogleSync's public methods so existing callers
keep calling them straight on the `Google` instance (`g.sync(...)`, `g.pull(...)`, …) with no change on their
side. Everything else here is re-exported from app/google/ so `from .gsync import ...` and the suites'
`gsync.<name>` keep working. The three endpoint URLs below stay in this module because the suites point them at
the mock Google; `Google` reads them from here each time.
"""
from __future__ import annotations

import httpx  # noqa: F401 (a suite patches gsync.httpx)

from .google.api import CLIENT_ID_RE, GoogleApi, _b64url, _error_message, _error_reason, _id_token_claims  # noqa: F401
from .google.errors import AccessRevoked, CalendarMissing, Conflict, GoogleError  # noqa: F401
from .google.sync import (CALENDAR_COLORS, COLOR_WAYS, GOOGLE_COLORS, MARKER, SyncResult, GoogleSync, event_body,  # noqa: F401
                          event_id, google_fields, in_window, nearest_calendar_color, nearest_color_id, _hash, _needs_repair,
                          _quote, _rgb, _SkipRevoke)

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
API_URL = "https://www.googleapis.com/calendar/v3"
MAX_WRITES = 1500          # Google writes in one sync at most; the rest wait for the next one (a suite lowers it here)


class Google(GoogleApi):
    """One Google account's connection, plus its calendars' sync (a GoogleSync handed this connection, not mixed
    into it: F58 checkpoint 10); the endpoints are read from this module each time (where the test suites point
    them at the mock Google)."""

    def __init__(self, store, box, tz_name, account: str = "", traffic=None):
        super().__init__(store, box, tz_name, account, traffic)
        self._sync_engine = GoogleSync(self)

    @property
    def AUTH_URL(self): return AUTH_URL

    @property
    def TOKEN_URL(self): return TOKEN_URL

    @property
    def REVOKE_URL(self): return REVOKE_URL

    @property
    def API_URL(self): return API_URL

    @property
    def MAX_WRITES(self): return MAX_WRITES

    # --- Calendar and event work, forwarded to the GoogleSync handed this connection ---------------------

    def cal_info(self, sid): return self._sync_engine.cal_info(sid)

    def _update_cal(self, sid, **changes): return self._sync_engine._update_cal(sid, **changes)

    def rekey(self, old, new): return self._sync_engine.rekey(old, new)

    def calendar_sids(self): return self._sync_engine.calendar_sids()

    def forget_calendar(self, sid): return self._sync_engine.forget_calendar(sid)

    async def ensure_calendar(self, sid, name, calendar_id=None):
        return await self._sync_engine.ensure_calendar(sid, name, calendar_id)

    async def set_color(self, sid, color): return await self._sync_engine.set_color(sid, color)

    async def delete_calendar(self, sid): return await self._sync_engine.delete_calendar(sid)

    async def disconnect(self, delete_calendar, revoke=True):
        return await self._sync_engine.disconnect(delete_calendar, revoke)

    def record_error(self, message): return self._sync_engine.record_error(message)

    def watch_info(self, sid="ccs"): return self._sync_engine.watch_info(sid)

    def _update_watch(self, sid, **changes): return self._sync_engine._update_watch(sid, **changes)

    def watch_due(self, sid, address, now_, renew_before, retry_after):
        return self._sync_engine.watch_due(sid, address, now_, renew_before, retry_after)

    async def start_watch(self, sid, address): return await self._sync_engine.start_watch(sid, address)

    async def stop_watch(self, sids): return await self._sync_engine.stop_watch(sids)

    def notice_from(self, channel, token, sids): return self._sync_engine.notice_from(channel, token, sids)

    def noticed(self, sid): return self._sync_engine.noticed(sid)

    async def pull(self, sid, first_day): return await self._sync_engine.pull(sid, first_day)

    async def delete_event(self, sid, gid): return await self._sync_engine.delete_event(sid, gid)

    async def sync(self, sid, events, name, color_for, first_day, full=False, hold=frozenset()):
        return await self._sync_engine.sync(sid, events, name, color_for, first_day, full, hold)
