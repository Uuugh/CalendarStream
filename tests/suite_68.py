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
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
