"""0.2.8-beta.35 (F58 checkpoint 2): app/google's shared types, tested without the app, a database or a network
(R18). The database name argument is accepted and unused."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google.errors import AccessRevoked, CalendarMissing, Conflict, GoogleError
from app.google.health_state import HealthState
from app.google.failure_kind import FailureKind
from app.google.recovery_decision import RecoveryDecision
ok(all(issubclass(e, GoogleError) for e in (AccessRevoked, CalendarMissing, Conflict)), "the three errors are Google errors")
ok(str(GoogleError("x")) == "x", "a Google error keeps its message")
ok({s.value for s in HealthState} == {"healthy", "degraded", "recovering", "reauth_required", "paused"}, "the five health states")
ok(HealthState("paused") is HealthState.PAUSED and HealthState.HEALTHY == "healthy", "a state is its saved text")
ok({k.value for k in FailureKind} == {"token_expired", "consent_revoked", "rate_limit", "transient", "permission",
                                      "calendar_missing", "event_invalid", "conflict", "unknown"}, "the nine failure kinds")
d = RecoveryDecision(True, HealthState.RECOVERING, "refreshing the access token")
ok(d.retry and d.state is HealthState.RECOVERING and d.retry_after_seconds == 0.0, "a decision's fields, retry-after defaulting to 0")
try:
    d.retry = False; ok(False, "a decision can't be changed")
except Exception:
    ok(True, "a decision can't be changed")
from app import gsync
ok(gsync.GoogleError is GoogleError and gsync.AccessRevoked is AccessRevoked and gsync.Conflict is Conflict
   and gsync.CalendarMissing is CalendarMissing, "gsync still offers the same error classes (the facade)")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
