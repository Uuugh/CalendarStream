"""The recovery plan for each kind of failure (per account, not global).

Holds: RecoveryPolicy (`decide(kind, attempt, retry_after) -> RecoveryDecision`).
Depends on: app/google/failure_kind.py, app/google/health_state.py, app/google/recovery_decision.py.
Used by: app/google/health.py (F58 checkpoint 7).
Reads/writes: nothing; randomness for the backoff's jitter is passed in, so this needs no clock or network.
Dart note: `final class RecoveryPolicy` taking a `double Function() jitter` (default `Random().nextDouble`). Layer: domain.
"""
from __future__ import annotations

import random
from typing import Callable

from .failure_kind import FailureKind
from .health_state import HealthState
from .recovery_decision import RecoveryDecision

MAX_ATTEMPTS = 5        # tries of a failure that may pass by itself; after these it stops until the next scheduled sync
BASE_DELAY = 5.0        # seconds: the first wait, doubled each attempt
MAX_DELAY = 15 * 60.0   # seconds: the longest wait


class RecoveryPolicy:
    def __init__(self, jitter: Callable[[], float] = random.random):
        self._jitter = jitter

    def backoff(self, attempt: int, retry_after: float | None = None) -> float:
        """Seconds to wait before attempt `attempt` (0 = the first retry): exponential, with jitter (up to +25 %),
        never less than what Google asked (`retry_after`) and never more than MAX_DELAY."""
        wait = min(MAX_DELAY, BASE_DELAY * (2 ** attempt))
        wait *= 1 + 0.25 * self._jitter()
        return min(MAX_DELAY, max(wait, retry_after or 0.0))

    def decide(self, kind: FailureKind, attempt: int = 0, retry_after: float | None = None) -> RecoveryDecision:
        """`attempt` counts the retries already made for this failure (0 = the first time it happened)."""
        K, H = FailureKind, HealthState
        if kind is K.TOKEN_EXPIRED:
            if attempt == 0:
                return RecoveryDecision(True, H.RECOVERING, "the access token was refused: refresh it once and retry")
            return RecoveryDecision(False, H.REAUTH_REQUIRED, "a fresh access token was refused too: sign in again")
        if kind is K.CONSENT_REVOKED:
            return RecoveryDecision(False, H.REAUTH_REQUIRED, "Google no longer accepts this sign-in: sign in again")
        if kind is K.PERMISSION:
            return RecoveryDecision(False, H.REAUTH_REQUIRED, "Google refused the client or a permission: fix it, then sign in again")
        if kind in (K.RATE_LIMIT, K.TRANSIENT):
            if attempt >= MAX_ATTEMPTS:
                return RecoveryDecision(False, H.DEGRADED, "still failing after several tries: waiting for the next sync")
            return RecoveryDecision(True, H.DEGRADED, "Google is busy or unreachable: retrying later",
                                    self.backoff(attempt, retry_after))
        if kind is K.CALENDAR_MISSING:
            return RecoveryDecision(False, H.PAUSED, "the calendar is gone in Google: not recreated without asking")
        if kind in (K.EVENT_INVALID, K.CONFLICT):
            return RecoveryDecision(False, H.HEALTHY, "an event-level problem, not a sign-in one: the account stays healthy")
        if attempt == 0:
            return RecoveryDecision(True, H.DEGRADED, "an unknown failure: trying once more")
        return RecoveryDecision(False, H.DEGRADED, "an unknown failure that repeated")
