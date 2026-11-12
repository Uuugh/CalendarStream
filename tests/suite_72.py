"""0.2.8-beta.35 (F58 checkpoint 6): the failure classifier and the recovery policy alone (R18): no app, database or
network. The database name argument is accepted and unused."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google.errors import AccessRevoked, CalendarMissing, Conflict, GoogleError
from app.google.failure_kind import FailureKind as K
from app.google.failure_classifier import FailureClassifier
from app.google.health_state import HealthState as H
from app.google.recovery_policy import RecoveryPolicy, MAX_DELAY, MAX_ATTEMPTS
c = FailureClassifier().classify
ok(c(AccessRevoked("x")) is K.CONSENT_REVOKED and c(CalendarMissing("x")) is K.CALENDAR_MISSING and c(Conflict("x")) is K.CONFLICT, "the error classes decide first")
ok(c(GoogleError("x", status=401)) is K.TOKEN_EXPIRED and c(GoogleError("x", status=403)) is K.PERMISSION, "401 is an expired token; 403 a permission")
ok(c(GoogleError("x", status=429)) is K.RATE_LIMIT and c(GoogleError("x", status=503)) is K.TRANSIENT, "429 is a rate limit; 5xx is transient")
ok(c(GoogleError("x", transient=True)) is K.TRANSIENT, "a network failure is transient")
ok(c(GoogleError("x", status=404)) is K.CALENDAR_MISSING and c(GoogleError("x", status=409)) is K.CONFLICT and c(GoogleError("x", status=400)) is K.EVENT_INVALID, "404/410, 409, 400")
ok(c(GoogleError("Google rejected the OAuth client: check")) is K.PERMISSION, "a refused client is a permission failure")
ok(c(ValueError("x")) is K.UNKNOWN and c(GoogleError("plain")) is K.UNKNOWN, "anything else is unknown")
p = RecoveryPolicy(jitter=lambda: 0.0)
d = p.decide(K.TOKEN_EXPIRED, 0)
ok(d.retry and d.state is H.RECOVERING, "an expired token: the next scheduled sync retries with a fresh one")
d = p.decide(K.TOKEN_EXPIRED, 1)
ok(not d.retry and d.state is H.REAUTH_REQUIRED, "…and if the fresh one is refused too, sign in again")
ok(not p.decide(K.CONSENT_REVOKED).retry and p.decide(K.CONSENT_REVOKED).state is H.REAUTH_REQUIRED, "a revoked grant needs a new sign-in, no retry")
ok(not p.decide(K.PERMISSION).retry and p.decide(K.PERMISSION).state is H.REAUTH_REQUIRED, "a refused client or permission isn't retried")
ok(p.decide(K.TRANSIENT, 0).retry and p.decide(K.TRANSIENT, 0).retry_after_seconds == 5.0 and p.decide(K.TRANSIENT, 1).retry_after_seconds == 10.0, "waits double: 5 s, 10 s…")
ok(p.decide(K.RATE_LIMIT, 0, retry_after=120).retry_after_seconds == 120.0, "Retry-After is respected when it is longer")
ok(p.decide(K.TRANSIENT, MAX_ATTEMPTS - 1).retry_after_seconds <= MAX_DELAY, "no wait is longer than the limit")
ok(not p.decide(K.TRANSIENT, MAX_ATTEMPTS).retry and p.decide(K.TRANSIENT, MAX_ATTEMPTS).state is H.DEGRADED, "retries are bounded")
ok(RecoveryPolicy(jitter=lambda: 1.0).backoff(0) == 5.0 * 1.25, "jitter adds up to 25 %")
d = p.decide(K.CALENDAR_MISSING)
ok(not d.retry and d.state is H.PAUSED, "a missing calendar pauses; it is not recreated")
ok(all(not p.decide(k).retry and p.decide(k).state is H.HEALTHY for k in (K.EVENT_INVALID, K.CONFLICT)), "event-level problems don't touch the account's health")
ok(p.decide(K.UNKNOWN, 0).retry and not p.decide(K.UNKNOWN, 1).retry, "an unknown failure gets one more try")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
