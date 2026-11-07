"""One Google account's health: what the last failure was, what to do about it, and when to try again.

Holds: GoogleHealth (`check_and_recover(account, error)`, `record_success`, `may_sync`, `reset`, `get`).
Depends on: app/google/failure_classifier.py, recovery_policy.py, recovery_decision.py, health_state.py (and the
  errors they use); the store it is given.
Used by: app/main.py (`_sync_account` records each sync's result and skips an account that is waiting to retry) and
  app/routes/google.py (a new sign-in resets the account).
Reads/writes: the database through the store it is given (key `google_health`, one entry per account); the clock it is
  given. It never touches tokens, mappings or a module's 1-way/2-way setting: only its own record.
Dart note: `class GoogleHealth` (domain) with a `KeyValueStore` and a `DateTime Function() now`. Layer: domain.
"""
from __future__ import annotations

import time
from typing import Callable

from .failure_classifier import FailureClassifier
from .health_state import HealthState
from .recovery_decision import RecoveryDecision
from .recovery_policy import RecoveryPolicy

HEALTH_KEY = "google_health"


class GoogleHealth:
    def __init__(self, store, classifier: FailureClassifier | None = None, policy: RecoveryPolicy | None = None,
                 now: Callable[[], float] = time.time):
        self.store = store
        self.classifier = classifier or FailureClassifier()
        self.policy = policy or RecoveryPolicy()
        self.now = now

    def get(self, account: str = "") -> dict:
        """The account's record: state, kind, reason, attempts, next_retry (epoch seconds or None), last_error, at."""
        rec = (self.store.get(HEALTH_KEY) or {}).get(account)
        return dict(rec) if rec else {"state": HealthState.HEALTHY.value, "attempts": 0, "next_retry": None}

    def _save(self, account: str, rec: dict):
        everything = dict(self.store.get(HEALTH_KEY) or {})
        everything[account] = rec
        self.store.set(HEALTH_KEY, everything)

    def check_and_recover(self, account: str, error: BaseException) -> RecoveryDecision:
        """A sync of this account failed: classify it, decide, remember. The caller retries once at most (the
        decision's `retry`), and later attempts wait for `next_retry`."""
        kind = self.classifier.classify(error)
        before = self.get(account)
        attempt = before.get("attempts", 0) if before.get("kind") == kind.value else 0
        decision = self.policy.decide(kind, attempt, getattr(error, "retry_after", None))
        now = self.now()
        self._save(account, {
            "state": decision.state.value, "kind": kind.value, "reason": decision.reason,
            "attempts": attempt + 1 if decision.retry else attempt,
            "next_retry": now + decision.retry_after_seconds if decision.retry and decision.retry_after_seconds else None,
            "last_error": str(error)[:300], "at": now})
        return decision

    def record_success(self, account: str):
        """A sync worked: the account is healthy again (nothing is written when it never had a problem)."""
        if (self.store.get(HEALTH_KEY) or {}).get(account):
            self._save(account, {"state": HealthState.HEALTHY.value, "attempts": 0, "next_retry": None, "at": self.now()})

    def may_sync(self, account: str) -> bool:
        """False only while the account is waiting out a back-off (so a failing Google isn't hammered)."""
        nxt = self.get(account).get("next_retry")
        return not (nxt and self.now() < nxt)

    def reset(self, account: str):
        """A new sign-in: forget the past failures."""
        everything = dict(self.store.get(HEALTH_KEY) or {})
        if everything.pop(account, None) is not None:
            self.store.set(HEALTH_KEY, everything)
