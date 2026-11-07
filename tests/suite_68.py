"""0.2.8-beta.35 (F58 checkpoint 1, I5): a Google module whose account has no sign-in is skipped by every sync;
the sync now says so once in History instead of silently doing nothing, and says it again only after the module
has been signed in and lost it. Uses the mock Google; own port 8168."""
import asyncio, os, re, sys, threading
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import uvicorn, mockgoogle
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
from serve import wait_up
M = "http://127.0.0.1:8168"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8168, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); wait_up(srv, 8168)
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
log = lambda n=30: [h["msg"] for h in main.store.recent_log(n)]
said = lambda: [m for m in log() if "Sister: not signed in to a Google account yet, so it isn't synced" in m]

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        patch.object(main, "api_on", lambda: True), TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = ("t", "password1")
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/", headers={"accept": "text/html"}).text)[1]
    main.google.save_client(mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET)
    c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Sister"}, follow_redirects=False)
    sis = next(d for d in main.destinations() if d["name"] == "Sister")
    ok(not main.dest_google(sis).connected, "the new module has an account with no sign-in")
    ok(asyncio.run(main.google_sync_once(True)) is True, "syncing with it signed out isn't a failure")
    ok(len(said()) == 1, "…but History says once that it isn't synced, and why")
    asyncio.run(main.google_sync_once(True)); asyncio.run(main.google_sync_once(True))
    ok(len(said()) == 1, "…and not again at the next syncs")
    main._unsigned_said.discard(sis["id"])
    asyncio.run(main.google_sync_once(True))
    ok(len(said()) == 2, "…until it is forgotten (after a sign-in, say) and it is signed out again")
    # --- F58 5 (review #9 finding 2): the API Sync's last step no longer says "ready" ---------------------------
    r = c.post("/google/step", data={"csrf": csrf, "step": "go"})
    ok(r.status_code == 200 and r.json().get("ok") is True, "the last connect step succeeds")
    lines = log(10)
    ok(any("Google Calendar API Sync is set up" in m and "needs its own sign-in" in m for m in lines) and not any("is ready" in m for m in lines),
       "…and says the client is set up, not that it is ready")
    ok(any("Google, Sister: not signed in" in m for m in lines), "…and names the module that isn't signed in, and why")
    # --- F58 7: a failing Google is remembered per account, waited out, and forgiven by a success ------------------
    import time as _t
    from app.google.errors import GoogleError as _GE
    h = main.google_health
    h.check_and_recover("", _GE("busy", status=503))
    ok(h.get("")["state"] == "degraded" and not h.may_sync(""), "a failing sync marks the account degraded and waiting")
    ok(asyncio.run(main.google_sync_once(True)) is True, "…and the next sync skips it quietly, not hammering Google")
    h.reset("")
    ok(h.may_sync("") and h.get("")["state"] == "healthy", "a new sign-in clears it")
    # --- REVIEW 2 (#11 #1): an unexpected failure (not a GoogleError) is classified and remembered too ---------------
    class _Boom:
        account = "boom"
        def info(self): return {}
        def record_error(self, m): self.m = m
        async def pull(self, *a, **k): return []
        async def sync(self, *a, **k): raise ValueError("malformed event")
    b = _Boom()
    ok(asyncio.run(main._sync_account(b, [{"id": "x", "name": "X", "start": "", "oneway": True, "color": ""}], 1, None, True)) is False,
       "a sync that raises a ValueError fails the sync")
    rec = main.google_health.get("boom")
    ok(rec["kind"] == "unknown" and rec["state"] == "degraded", "…and the account's health records an unknown failure")
    main.google_health.reset("boom")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
