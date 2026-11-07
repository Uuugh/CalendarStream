"""Decides what kind of failure a Google error is.

Holds: FailureClassifier (`classify(error) -> FailureKind`).
Depends on: app/google/errors.py, app/google/failure_kind.py.
Used by: app/google/health.py (F58 checkpoint 7).
Reads/writes: nothing; no database, network, files or clock.
Dart note: `final class FailureClassifier` with a `FailureKind classify(GoogleError e)`; in Dart the kind can come
  from a `switch` over the sealed GoogleError family plus its `status`. Layer: domain.
"""
from __future__ import annotations

from .errors import AccessRevoked, CalendarMissing, Conflict, GoogleError
from .failure_kind import FailureKind


class FailureClassifier:
    def classify(self, error: BaseException) -> FailureKind:
        """The structure on the error decides (its class, then `status`, then `transient`); a message is only read
        for the one case an older raise site can't say otherwise: Google refusing the OAuth client."""
        K = FailureKind
        if isinstance(error, AccessRevoked):
            return K.CONSENT_REVOKED
        if isinstance(error, CalendarMissing):
            return K.CALENDAR_MISSING
        if isinstance(error, Conflict):
            return K.CONFLICT
        if not isinstance(error, GoogleError):
            return K.UNKNOWN
        status = error.status
        if status == 401:
            return K.TOKEN_EXPIRED
        if status == 403 or "rejected the OAuth client" in str(error):
            return K.PERMISSION
        if status == 429:
            return K.RATE_LIMIT
        if status in (404, 410):
            return K.CALENDAR_MISSING
        if status == 409:
            return K.CONFLICT
        if status is not None and 500 <= status <= 599 or error.transient:
            return K.TRANSIENT
        if status == 400:
            return K.EVENT_INVALID
        return K.UNKNOWN
