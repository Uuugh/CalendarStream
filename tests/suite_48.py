"""0.2.8-beta.14 tests, against the mock Google: Connect in one straight line (save → check the client →
check the address → Google's sign-in), stopping with what to fix; the redirect address checked for real;
the lifecycle: disconnect → reconnect (the same calendar, no duplicate) → delete the client → a fresh
client (a new calendar, the old one named for deleting by hand) with the Google feed graceful throughout;
one look per meaning on the statuses."""
import asyncio, os, re, sys, threading, time
from urllib.parse import urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="https://cal.example.com", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
M = "http://127.0.0.1:8120"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8120, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, A = mockgoogle.S, ("t", "p"); G = httpx.Client(); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
run = asyncio.run
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
URI = "https://cal.example.com/google/callback"
A_ID, A_SECRET = mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET
B_ID, B_SECRET = "other-client.apps.googleusercontent.com", "GOCSPX-other"
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    if not main.destinations("google"):
        c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Flying"})
    step = lambda s, **f: c.post("/google/step", data={"csrf": csrf, "step": s, **f}).json()
    def connect(cid, secret):
        """Connect, as the page does it: each step in turn, stopping at the first that fails."""
        for s, extra in (("save", {"client_id": cid, "client_secret": secret}), ("client", {}), ("address", {}), ("go", {})):
            j = step(s, **extra)
            if not j["ok"]:
                return j
        # (0.2.8-beta.17) Turn on stops at Ready: the first account (an install from before) signs in here
        url = j["url"] or c.post("/google/connect", data={"csrf": csrf}, follow_redirects=False).headers["location"]
        back = G.get(url, follow_redirects=False); cb = urlparse(back.headers["location"])
        c.get(cb.path + "?" + cb.query, follow_redirects=False)
        return {"ok": main.google.connected}
    def cals():
        return [x for x in S["calendars"].values() if x["owner"] == S["email"]]
    DID = lambda: main.destinations("google")[0]["id"]

    # Connect stops at the first step that fails, saying what to fix
    j = step("save")
    ok(not j["ok"] and "Client ID and Client secret:" in j["message"], "nothing typed: Connect stops at Saving… and says what's needed")
    j = step("save", client_id="not-a-client", client_secret="x")
    ok(not j["ok"] and "doesn't look like a Google OAuth client ID" in j["message"], "a wrong-looking ID: stops at Saving…")
    j = step("save", client_id=A_ID, client_secret="GOCSPX-wrong")
    ok(j["ok"], "saved")
    j = step("client")
    ok(not j["ok"] and "rejected the client secret" in j["message"] and j["fix"].get("open"), "a wrong secret: stops at Checking…, with Open your client")
    S["redirects"] = {A_ID: []}
    j = connect(A_ID, A_SECRET)
    ok(not j["ok"] and j["step"] == "address" and URI in j["message"] and j["fix"].get("copy") == URI and j["fix"].get("open"),
       "the address not on the client: stops at Checking address…, with Copy and Open")
    p = c.get("/?menu=settings").text
    gs = p[p.index('id="googlesync"'):p.index('id="updates"')]
    ok("Address missing" in gs and 'class="statusbox gbox warn"' in gs and 'data-address="0"' in gs and "<b>Google</b>" not in gs,
       "…Settings says Address missing (amber: Google's side), guided step 6 not ticked")
    S["redirects"] = {A_ID: [URI]}
    j = connect(A_ID, A_SECRET)
    ok(j["ok"] and main.google.connected, "with the address added: Connect goes all the way to Connected")
    ok(main.google.client_check().get("redirect_ok") is True, "…and the address is recorded as confirmed by Google")
    ok(run(main.google_sync_once(True)), "first sync")
    first = main.google.cal_info(DID()).get("calendar_id")
    n_events = len([e for e in S["events"][first].values() if e.get("status") != "cancelled"])
    ok(first and len(cals()) == 1 and n_events > 5, f"one calendar in Google ({n_events} events)")

    # Disconnect (keeping the calendars), the feed graceful, reconnect: the same calendar
    c.post("/google/disconnect", data={"csrf": csrf})
    ok(not main.google.connected and main.google.cal_info(DID()).get("calendar_id") == first, "disconnected; the calendar's ID kept")
    p = c.get("/").text
    dh = p[p.index(f'id="dest-{DID()}"'):]; dh = dh[:dh.index('class="cfgline"')]
    ok("Not connected" in dh and 'class="statusbox run"' in dh, "the Google feed while disconnected: Not connected, the pressed look (waiting on you)")
    ok(run(main.google_sync_once(True)) and not main.google.info().get("last_error"), "…and the background sync carries on without errors")
    j = connect(A_ID, "")
    ok(j["ok"] and main.google.connected, "reconnect with the same client (the secret kept)")
    run(main.google_sync_once(True))
    ok(main.google.cal_info(DID()).get("calendar_id") == first and len(cals()) == 1, "…the same calendar in Google: no duplicate")
    ok(len([e for e in S["events"][first].values() if e.get("status") != "cancelled"]) == n_events, "…and no duplicate events")

    # The trash: deletes the client (disconnecting first); a fresh client: a new calendar, the old one named
    c.post("/google/client", data={"csrf": csrf, "action": "remove"})
    ok(not main.google.connected and not main.google.configured, "the trash: disconnected and the client deleted")
    p = c.get("/").text
    ok('Not set up' in p and "Traceback" not in p, "Settings starts over: Not set up")
    S["clients"][B_ID] = B_SECRET; S["redirects"][B_ID] = [URI]
    j = connect(B_ID, B_SECRET)
    ok(j["ok"] and main.google.connected and main.google.client_id == B_ID, "a fresh setup with another client: connected")
    ok(run(main.google_sync_once(True)), "…the sync works")
    second = main.google.cal_info(DID()).get("calendar_id")
    log = [h["msg"] for h in main.store.recent_log(12)]
    ok(second and second != first and len(cals()) == 2 and first in S["calendars"], "…a new calendar (Google won't show the old one to this client)")
    ok(any("made with the earlier Google client can't be reached" in m and "delete the old" in m for m in log), "…and the log names the old one to delete by hand")
    ok(not main.google.info().get("last_error"), "…without errors")
    run(main.google_sync_once(True))
    ok(len(cals()) == 2 and main.google.cal_info(DID()).get("calendar_id") == second, "a later sync keeps the new calendar (no third one)")
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
