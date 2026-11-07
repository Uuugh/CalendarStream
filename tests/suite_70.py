"""0.2.8-beta.35 (F58 checkpoint 3): app/google/api.py's GoogleApi, tested alone (R18): a plain dict as its store, no
app, database, browser or network. The database name argument is accepted and unused."""
import os, sys
from urllib.parse import parse_qs, urlparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google.api import GoogleApi, MAX_PENDING
from app.secretbox import SecretBox
from app import gsync

class DictStore:
    def __init__(self): self.d = {}
    def get(self, k): return self.d.get(k)
    def set(self, k, v): self.d[k] = v

store = DictStore(); box = SecretBox("unit-test-password")
g = GoogleApi(store, box, "America/New_York")
ok(not g.configured and g.client() == ("", ""), "no client saved: not configured")
g.save_client("1234567890-abc.apps.googleusercontent.com", "s3cret")
ok(g.configured and g.client_id.startswith("1234567890") and g.client_secret == "s3cret", "the client is saved and read back")
ok("s3cret" not in repr(store.d), "the client secret is stored encrypted, not as text")
g.save_client("1234567890-abc.apps.googleusercontent.com", "")
ok(g.client_secret == "s3cret", "a blank secret keeps the saved one")
try:
    g.save_client("not a client id", "x"); ok(False, "a malformed client ID is refused")
except Exception:
    ok(True, "a malformed client ID is refused")
ok(not g.connected and g.info() == {}, "a new account is not connected and has no details")
other = GoogleApi(store, box, "America/New_York", "a1b2c3")
ok(other.configured and other._info_key != g._info_key and other._token_key != g._token_key, "accounts share the client but keep their own keys")
q = parse_qs(urlparse(g.sign_in_url("https://cal.example.com/google/callback")).query)
ok(q["code_challenge_method"] == ["S256"] and q["access_type"] == ["offline"] and q["client_id"] == [g.client_id] and len(g._pending) == 1,
   "a sign-in URL carries PKCE, asks for offline access and remembers its state")
for _ in range(MAX_PENDING + 5): g.sign_in_url("https://cal.example.com/google/callback")
ok(len(g._pending) <= MAX_PENDING, "unfinished sign-ins are capped")
ok(gsync.Google.__mro__[1] is GoogleApi, "gsync's Google builds on GoogleApi (the facade)")
gsync.AUTH_URL = "http://mock/auth"
ok(gsync.Google(store, box, "UTC").AUTH_URL == "http://mock/auth", "the endpoint a suite sets on gsync is the one used")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
