"""0.2.8-beta.18 tests, against the mock Google: a color Google refuses never makes a working sync a "Sync problem"
(I4); a module that connects again reuses its calendar instead of making a second (I5); Connect me comes back to
the module (F1); a sign-in Google no longer accepts shows Fix (F1.1); no stale "Last synced" on a module that
isn't connected (I1.1); ☰ Settings › Google Calendar API Sync: the Client ID and secret editable at any time (I2),
its Status/Action box (health over Connect / Reconnect / Fix), no Sync Now, one Remove (F2, F3)."""
import asyncio, os, re, sys, threading, time
from urllib.parse import urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
M = "http://127.0.0.1:8124"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8124, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, G = mockgoogle.S, httpx.Client()
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
log = lambda n=20: [h["msg"] for h in main.store.recent_log(n)]

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = ("t", "password1")
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    main.google.save_client(mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET)
    def connect(did):
        r = c.post("/google/account", data={"csrf": csrf, "did": did, "action": "connect"}, follow_redirects=False)
        back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
        return c.get(cb.path + "?" + cb.query, follow_redirects=False)
    with patch.object(main, "api_on", lambda: True):
        c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Flying", "sources": ["ccs"]})
    d = next(x for x in main.destinations("google") if x["name"] == "Flying")
    p = page()
    box = p[p.index(f'id="dest-{d["id"]}"'):]; box = box[:box.index('class="cfgline"')]
    ok("Last synced" not in box, "I1.1: a module that isn't connected shows no Last synced")

    # F1: Connect me comes back to the module, open, Connected
    r = connect(d["id"])
    ok(r.status_code == 303 and r.headers["location"] == f"/#dest-{d['id']}", "F1: Connect me comes back to its module, not ☰ Settings")
    ok((main.store.get("ui_sections") or {}).get(f"dest:{d['id']}") is True, "F1: …opened, to show it")
    g = main.dest_google(main.destination(d["id"]))
    asyncio.run(main.google_sync_once(True))
    cal1 = g.cal_info(d["id"])["calendar_id"]
    ok(cal1 in S["calendars"] and ">Connected<" in page(), "F1: …and it says Connected")

    # I4: a color Google refuses: said once, the sync stays fine
    c.post("/destinations/update", data={"csrf": csrf, "did": d["id"], "name": "Flying", "sources": ["ccs"], "color": "#0b8043"})
    async def refuse(*a, **k):
        raise gsync.AccessRevoked("Google no longer accepts CalendarStream's sign-in. Connect again.")
    with patch.object(gsync.Google, "set_color", refuse):
        ok(asyncio.run(main.google_sync_once(True)) and asyncio.run(main.google_sync_once(True)), "I4: a refused color doesn't fail the sync")
    lines = log()
    ok(sum("color couldn't be set" in m for m in lines) == 1 and not g.info().get("last_error"),
       "I4: …it's said once, and the module isn't a Sync problem")

    # I5: connecting again (a new sign-in, same Gmail) reuses the calendar
    c.post("/google/account", data={"csrf": csrf, "did": d["id"], "action": "disconnect"})
    ok(not main.dest_google(main.destination(d["id"])).connected, "I5: disconnected")
    n_before = len(S["calendars"])
    connect(d["id"])
    asyncio.run(main.google_sync_once(True))
    g = main.dest_google(main.destination(d["id"]))
    ok(g.cal_info(d["id"])["calendar_id"] == cal1 and len(S["calendars"]) == n_before,
       "I5: connecting again uses the same Google calendar, not a second one")

    # F1.1: a sign-in Google no longer accepts: the fault over Fix
    g.record_error("Google no longer accepts CalendarStream's sign-in. Connect again.")
    p = page()
    box = p[p.index(f'id="dest-{d["id"]}"'):]; box = box[:box.index('class="cfgline"')]
    ok("Sign-in failed" in box and 'class="syncnow gfixbtn"' in box and f'form="gacct-{d["id"]}"' in box and 'value="connect"' in box,
       "F1.1: a broken sign-in shows Sign-in failed over Fix, which signs in again")
    g.record_error("")

    # F2, F3, I2: ☰ Settings › Google Calendar API Sync
    main.google.store.set("google_client", {**main.store.get("google_client"),
                                            "check": {"ok": True, "at": "2026-10-29T20:00:00+00:00", "redirect_ok": True,
                                                      "redirect_uri": "https://cal.example.com/google/callback"}})
    main.google._client = None
    p = page("?menu=settings")
    gs = p[p.index('id="googlesync"'):p.index('id="updates"')]
    ok(">Healthy<" in gs and ">Reconnect<" in gs and "Sync Now" not in gs and "Last synced" not in gs and "Instant updates" not in gs,
       "F3: healthy: Healthy over Reconnect; no Sync Now, Last synced or Instant updates")
    ok('id="fcid"' in gs and 'name="client_id"' in gs and "readonly" not in gs[gs.index('id="fcid"') - 200:gs.index('id="fcid"') + 200],
       "I2: the Client ID and secret can be changed while it's healthy")
    ok(gs.count(" Remove</button>") == 1 and "credtrash" not in gs and "each module connects again" in gs, "F3: one Remove, saying what stops")
    main.google.store.set("google_client", {**main.store.get("google_client"), "check": {"ok": False, "message": "Google rejected the client secret"}})
    main.google._client = None
    gs = page("?menu=settings"); gs = gs[gs.index('id="googlesync"'):gs.index('id="updates"')]
    ok("Client rejected" in gs and ">Fix<" in gs, "F3: a fault: the fault over Fix")
    main.google.store.delete("google_client"); main.google._client = None
    gs = page("?menu=settings"); gs = gs[gs.index('id="googlesync"'):gs.index('id="updates"')]
    ok("Not set up" in gs and ">Connect<" in gs and "Turn on" not in gs, "F2: not set up: Not set up over Connect")
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
