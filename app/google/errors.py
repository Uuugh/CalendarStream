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
    """Something went wrong talking to Google; the message is shown on the status page."""


class AccessRevoked(GoogleError):
    """Google no longer accepts the stored sign-in (revoked, expired or the password changed)."""


class Conflict(GoogleError):
    """Google already has an event with that ID."""


class CalendarMissing(GoogleError):
    """CalendarStream's calendar was deleted in Google."""
