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
ok(q["code_challenge_method"] == ["S256"] and q["access_type"] == ["offline"] and q["client_id"] == [g.client_id] and len(store.d['google_signins']) == 1,
   "a sign-in URL carries PKCE, asks for offline access and remembers its state")
for _ in range(MAX_PENDING + 5): g.sign_in_url("https://cal.example.com/google/callback")
ok(len(store.d['google_signins']) <= MAX_PENDING, "unfinished sign-ins are capped")
import asyncio, time
url = g.sign_in_url("https://cal.example.com/google/callback")
state = parse_qs(urlparse(url).query)["state"][0]
ok(g.owns_sign_in(state) and not other.owns_sign_in(state) and "verifier" in str(store.d["google_signins"][state]), "a started sign-in is saved for its own account")
ok("calendarstream" not in repr(store.d["google_signins"]) and parse_qs(urlparse(url).query)["code_challenge"][0] not in repr(store.d["google_signins"][state]["verifier"]), "the PKCE verifier is saved encrypted")
# a restart: a fresh object on the same store still knows the sign-in
again = GoogleApi(store, box, "America/New_York")
ok(again.owns_sign_in(state), "after a restart (a new object, the same database) the sign-in is still known")
ok(again._take_sign_in(state) is not None and again._take_sign_in(state) is None and not again.owns_sign_in(state), "a sign-in is used once")
s2 = parse_qs(urlparse(g.sign_in_url("https://cal.example.com/google/callback")).query)["state"][0]
rec = store.d["google_signins"][s2]; rec["expires"] = time.time() - 1; store.set("google_signins", {**store.d["google_signins"], s2: rec})
ok(not g.owns_sign_in(s2) and g._take_sign_in(s2) is None, "an expired sign-in is refused")
s3 = parse_qs(urlparse(other.sign_in_url("https://cal.example.com/google/callback")).query)["state"][0]
ok(g._take_sign_in(s3) is None, "another account's sign-in can't be used")
try:
    asyncio.run(g.finish_sign_in("not-a-state", "code")); ok(False, "an unknown state is refused")
except Exception as e:
    ok("expired or was already used" in str(e), "an unknown state is refused")
ok(gsync.Google.__mro__[1] is GoogleApi, "gsync's Google builds on GoogleApi (the facade)")
gsync.AUTH_URL = "http://mock/auth"
ok(gsync.Google(store, box, "UTC").AUTH_URL == "http://mock/auth", "the endpoint a suite sets on gsync is the one used")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
