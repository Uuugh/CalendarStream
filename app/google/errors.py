"""The errors Google's side can raise, one small family.

Holds: GoogleError and its subtypes AccessRevoked, Conflict, CalendarMissing.
Depends on: nothing (standard library only).
Used by: app/gsync.py (re-exports them, so `from .gsync import GoogleError` keeps working), app/main.py and
  app/routes/google.py (through gsync), app/google/health.py (to classify a failure, F58 checkpoint 6).
Reads/writes: nothing; no database, network, files or clock.
Dart note: one `sealed class GoogleError implements Exception` with `AccessRevoked`, `Conflict` and
  `CalendarMissing` as its subclasses in this same file (Dart requires a sealed family in one library). Layer: domain.
"""
from __future__ import annotations


class GoogleError(Exception):
    """Something went wrong talking to Google; the message is shown on the status page.

    `status` is Google's HTTP status when there was one; `transient` marks a failure of the network or of Google's
    side (not of the request); `retry_after` is the seconds Google asked us to wait (Retry-After), when it did.
    They are optional and only read by the failure classifier (app/google/failure_classifier.py)."""

    def __init__(self, message: str = "", *, status: int | None = None, transient: bool = False,
                 retry_after: float | None = None):
        super().__init__(message)
        self.status, self.transient, self.retry_after = status, transient, retry_after


class AccessRevoked(GoogleError):
    """Google no longer accepts the stored sign-in (revoked, expired or the password changed)."""


class Conflict(GoogleError):
    """Google already has an event with that ID."""


class CalendarMissing(GoogleError):
    """CalendarStream's calendar was deleted in Google."""
