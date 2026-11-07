"""Google Calendar, as the rest of the app imports it: the facade over app/google/ (F58 checkpoint 8).

`Google` is one account's connection (GoogleApi: sign-in, tokens, requests) plus its calendar and event work
(GoogleSync). Everything else here is re-exported from app/google/ so `from .gsync import ...` and the suites'
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


class Google(GoogleApi, GoogleSync):
    """One Google account's connection plus its calendars' sync; the endpoints are read from this module each time
    (where the test suites point them at the mock Google)."""

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
