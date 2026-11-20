"""How far one Google module is from working: the four things that are easy to mix up, told apart.

Holds: ReadinessStage and Readiness. The stages, in order: the OAuth client is set up (admin, once); the account is
  signed in; Google's Calendar API answers; the module has synced. "Ready" in the log used to mean only the first.
Depends on: nothing (standard library only).
Used by: app/routes/google.py (the Google Calendar API Sync "go" step's log lines); later the status page (F58 9).
Reads/writes: nothing; the caller passes in what it knows, so this needs no database, network or clock.
Dart note: `enum ReadinessStage` and an immutable `Readiness` with `factory Readiness.of(...)`, both in this one file
  (a closed family). Layer: domain.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReadinessStage(str, Enum):
    NO_CLIENT = "no_client"              # the OAuth client isn't set up
    NOT_SIGNED_IN = "not_signed_in"      # the client is set up; this module's account isn't signed in
    API_ERROR = "api_error"              # signed in, but the last call to Google failed
    NOT_SYNCED = "not_synced"            # signed in and no error, but it hasn't synced yet
    SYNCED = "synced"                    # it has synced


@dataclass(frozen=True)
class Readiness:
    stage: ReadinessStage
    text: str

    @property
    def working(self) -> bool:
        return self.stage is ReadinessStage.SYNCED

    @classmethod
    def of(cls, *, configured: bool, authorized: bool, last_error: str | None, last_sync: str | None) -> "Readiness":
        """`last_error` is Google's last complaint for the account ("" or None: none); `last_sync` is when the module
        last synced (None: never)."""
        S = ReadinessStage
        if not configured:
            return cls(S.NO_CLIENT, "the OAuth client isn't set up yet")
        if not authorized:
            return cls(S.NOT_SIGNED_IN, "not signed in to a Google account yet, so it isn't synced: open it and Connect me")
        if last_error:
            return cls(S.API_ERROR, f"signed in, but Google's last answer was a problem: {last_error}")
        if not last_sync:
            return cls(S.NOT_SYNCED, "signed in; it hasn't synced yet")
        return cls(S.SYNCED, "signed in and synced")
