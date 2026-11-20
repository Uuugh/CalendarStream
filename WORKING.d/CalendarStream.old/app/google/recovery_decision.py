"""What the health check decided after a failure: retry or not, the account's new state, and why.

Holds: RecoveryDecision.
Depends on: app/google/health_state.py.
Used by: app/google/health.py (F58 checkpoint 6) and the sync's record of a failure.
Reads/writes: nothing; no database, network, files or clock.
Dart note: an immutable class (`final class RecoveryDecision` with final fields, or a `freezed` one):
  `retry`, `state`, `reason`, `retryAfterSeconds`. Layer: domain.
"""
from __future__ import annotations

from dataclasses import dataclass

from .health_state import HealthState


@dataclass(frozen=True)
class RecoveryDecision:
    retry: bool
    state: HealthState
    reason: str
    retry_after_seconds: float = 0.0
