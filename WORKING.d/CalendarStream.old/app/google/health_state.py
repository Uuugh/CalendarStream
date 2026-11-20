"""How well one Google account's connection is working.

Holds: HealthState.
Depends on: nothing (standard library only).
Used by: app/google/recovery_decision.py; later app/google/health.py (F58 checkpoints 6-7) and the status page.
Reads/writes: nothing; no database, network, files or clock.
Dart note: `enum HealthState { healthy, degraded, recovering, reauthRequired, paused }` with a `value` string for
  the saved form. Layer: domain.
"""
from __future__ import annotations

from enum import Enum


class HealthState(str, Enum):
    HEALTHY = "healthy"                  # signed in and the last sync worked
    DEGRADED = "degraded"                # a failure that is expected to pass (rate limit, network)
    RECOVERING = "recovering"            # a repair or retry is under way
    REAUTH_REQUIRED = "reauth_required"  # the person must sign in again (consent revoked, client wrong)
    PAUSED = "paused"                    # stopped on purpose until something is fixed
