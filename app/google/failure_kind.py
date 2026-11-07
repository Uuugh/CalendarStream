"""What kind of failure a Google call ended in, which decides the recovery.

Holds: FailureKind.
Depends on: nothing (standard library only).
Used by: app/google/health.py (F58 checkpoint 6), which maps an error to one of these.
Reads/writes: nothing; no database, network, files or clock.
Dart note: `enum FailureKind { tokenExpired, consentRevoked, rateLimit, transient, permission, calendarMissing,
  eventInvalid, conflict, unknown }`. Layer: domain.
"""
from __future__ import annotations

from enum import Enum


class FailureKind(str, Enum):
    TOKEN_EXPIRED = "token_expired"        # access token refused (401): refresh once
    CONSENT_REVOKED = "consent_revoked"    # refresh token refused (invalid_grant): sign in again
    RATE_LIMIT = "rate_limit"              # 429: wait, then retry
    TRANSIENT = "transient"                # 5xx, timeout, network: back off, then retry
    PERMISSION = "permission"              # missing scope or wrong client: not retried
    CALENDAR_MISSING = "calendar_missing"  # the calendar is gone (404/410): never recreated silently
    EVENT_INVALID = "event_invalid"        # one event was refused (400): an event problem, not a sign-in one
    CONFLICT = "conflict"                  # 409: the existing conflict policy decides
    UNKNOWN = "unknown"
