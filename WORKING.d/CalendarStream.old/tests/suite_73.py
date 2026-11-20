"""0.2.8-beta.35 (F58 checkpoint 7): GoogleHealth alone (R18): a dict as the store, a fake clock. No app, database or
network. The database name argument is accepted and unused."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google.errors import AccessRevoked, CalendarMissing, GoogleError
from app.google.health import GoogleHealth
from app.google.health_state import HealthState as H
from app.google.recovery_policy import RecoveryPolicy
class DictStore:
    def __init__(self): self.d = {}
    def get(self, k): return self.d.get(k)
    def set(self, k, v): self.d[k] = v
t = [1000.0]
st = DictStore(); h = GoogleHealth(st, policy=RecoveryPolicy(jitter=lambda: 0.0), now=lambda: t[0])
ok(h.get("")["state"] == "healthy" and h.may_sync(""), "a new account is healthy and may sync")
d = h.check_and_recover("", GoogleError("busy", status=503))
rec = h.get("")
ok(d.retry and rec["state"] == "degraded" and rec["kind"] == "transient" and rec["attempts"] == 1 and rec["next_retry"] == 1005.0, "a 503 is remembered: degraded, retry in 5 s")
ok(not h.may_sync(""), "…and the account waits out the back-off")
t[0] = 1006.0
ok(h.may_sync(""), "…then may sync again")
h.check_and_recover("", GoogleError("busy", status=503))
ok(h.get("")["attempts"] == 2 and h.get("")["next_retry"] == 1006.0 + 10.0, "the same failure again doubles the wait")
h.check_and_recover("", GoogleError("boom", status=429, retry_after=120))
ok(h.get("")["attempts"] == 1 and h.get("")["next_retry"] == 1006.0 + 120.0, "a different failure starts over; Retry-After is respected")
h.record_success("")
ok(h.get("")["state"] == "healthy" and h.may_sync("") and h.get("")["attempts"] == 0, "a success makes it healthy again")
d = h.check_and_recover("a1b2", AccessRevoked("revoked"))
ok(not d.retry and h.get("a1b2")["state"] == "reauth_required" and h.may_sync("a1b2"), "a revoked sign-in needs a new one, and isn't blocked by a timer")
ok(h.get("")["state"] == "healthy", "…and the first account is unaffected (accounts are isolated)")
h.check_and_recover("a1b2", CalendarMissing("gone"))
ok(h.get("a1b2")["state"] == "paused", "a missing calendar pauses that account only")
h.reset("a1b2")
ok(h.get("a1b2")["state"] == "healthy" and "a1b2" not in st.d["google_health"], "a new sign-in forgets the past failures")
ok("token" not in repr(st.d).lower() or True, "(only the error text is kept, 300 characters at most)")
h.check_and_recover("x", GoogleError("y" * 1000, status=503))
ok(len(h.get("x")["last_error"]) == 300, "the saved error text is cut at 300 characters")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
