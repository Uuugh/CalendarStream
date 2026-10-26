"""0.1.15 tests: Google change notifications (webhooks) against the mock Google."""
import asyncio, os, re, sys, threading, time
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
M = "http://127.0.0.1:8099"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8099, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
DID = lambda: main.destinations('google')[0]['id']
GI = lambda: {**main.google.info(), **(main.google.cal_info(main.destinations('google')[0]['id']) if main.destinations('google') else {})}
S, A = mockgoogle.S, ("t", "p"); G = httpx.Client(); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
run = lambda coro: asyncio.get_event_loop().run_until_complete(coro) if False else asyncio.run(coro)
REAL = os.path.join(HERE, "data", "Demo.ics")
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), TestClient(main.app) as c:
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/", auth=A).text)[1]
    c.post("/setup/upload", auth=A, data={"csrf": csrf}, files={"file": ("Calendar.ics", open(REAL, "rb").read())})
    c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "test-client.apps.googleusercontent.com", "client_secret": "test-secret", "action": "save"})
    r = c.post("/google/connect", auth=A, data={"csrf": csrf}, follow_redirects=False)
    back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
    c.get(cb.path + "?" + cb.query, auth=A, follow_redirects=False)
    ok(main.google.connected, "connected")
    p = c.get("/", auth=A).text
    ok("Instant updates off" in p and "starts with the next sync" in p, "before the first sync: off, starts with the next sync (in the tooltip)")
    ok(run(main.google_sync_once(True)), "first sync")
    w = main.google.watch_info(DID()); cid = GI()["calendar_id"]
    ch = S["channels"].get(w.get("id"), {})
    ok(ch.get("address") == "https://cal.example.com/google/notify" and ch.get("cid") == cid and ch.get("ttl") == "604800", "channel started for CalendarStream's calendar")
    ok(w.get("token") and ch["token"] not in str(w), "secret token stored encrypted")
    ok(any("instant updates turned on" in h["msg"] for h in main.store.recent_log(10)), "logged: instant updates turned on")
    p = c.get("/", auth=A).text
    ok("Instant updates on" in p, "page: instant updates on")
    # a hand edit in Google, then the notification
    gid = next(k for k, v in S["events"][cid].items() if v.get("status") != "cancelled")
    S["events"][cid][gid]["summary"] = "changed by hand"; S["events"][cid][gid]["updated"] = "2099-01-01T00:00:00Z"
    main.google_job.full = False; main.google_job.wake.clear()
    hdr = {"X-Goog-Channel-ID": w["id"], "X-Goog-Channel-Token": ch["token"], "X-Goog-Resource-State": "exists", "X-Goog-Resource-ID": ch["resource"]}
    ok(c.post("/google/notify", headers={**hdr, "X-Goog-Channel-Token": "wrong"}).status_code == 200 and not main.google_job.wake.is_set(), "wrong token: answered, ignored")
    ok(c.post("/google/notify", headers={**hdr, "X-Goog-Channel-ID": "other"}).status_code == 200 and not main.google_job.wake.is_set(), "unknown channel: answered, ignored")
    ok(c.post("/google/notify", headers={**hdr, "X-Goog-Resource-State": "sync"}).status_code == 200 and not main.google_job.wake.is_set(), "'sync' message: no check")
    ok(c.post("/google/notify", headers=hdr).status_code == 200 and main.google_job.wake.is_set() and main.google_job.full, "change notice: full check requested (no login needed)")
    full = main.google_job.full; main.google_job.full = False
    run(main.google_sync_once(full))
    uid = next(r for r, row in main.store.google_rows(DID()).items() if row["google_id"] == gid)
    ok(S["events"][cid][gid]["summary"] == "changed by hand" and main.store.get_event(uid).title == "changed by hand",
       "two-way (0.2.8-beta.10): the hand edit comes here (an edit; CCS+ untouched)")
    ok(main.google.watch_info(DID()).get("last_notice") and "Last notice from Google" in c.get("/", auth=A).text, "last notice shown")
    # renewal
    old = main.google.watch_info(DID())["id"]
    main.google._update_watch(DID(), expires=(datetime.now(timezone.utc) + timedelta(hours=2)).isoformat())
    run(main.ensure_watch(DID()))
    new = main.google.watch_info(DID())["id"]
    ok(new != old and old not in S["channels"] and new in S["channels"], "renewed a day before it ends; old channel stopped")
    run(main.ensure_watch(DID()))
    ok(main.google.watch_info(DID())["id"] == new, "not renewed again while fresh")
    # new public address
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://new.example.com", "action": "save"})
    run(main.ensure_watch(DID()))
    ok(S["channels"][main.google.watch_info(DID())["id"]]["address"] == "https://new.example.com/google/notify" and len(S["channels"]) == 1, "moved to the new public address")
    # Google refuses
    S["refuse_watch"] = True
    main.google._update_watch(DID(), expires=datetime.now(timezone.utc).isoformat())
    run(main.ensure_watch(DID())); run(main.ensure_watch(DID()))
    warns = [h for h in main.store.recent_log(20) if "aren't available" in h["msg"]]
    ok(len(warns) == 1, "refused: logged once")
    p = c.get("/", auth=A).text
    ok("Instant updates off" in p and "daily check" in p, "page: off, with the reason (in the tooltip)")
    ok(run(main.google_sync_once(False)), "Autosync still works when refused")
    S["refuse_watch"] = False
    main.google._update_watch(DID(), tried=(datetime.now(timezone.utc) - timedelta(hours=7)).isoformat())
    run(main.ensure_watch(DID()))
    ok(main.google.watch_info(DID()).get("id") and not main.google.watch_info(DID()).get("error"), "asked again 6 h later: on")
    # http address: no notifications
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "http://192.168.1.5:8080", "action": "save"})
    ok("needs a public https:// address" in c.get("/", auth=A).text, "http:// address: off, needs https")
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://new.example.com", "action": "save"})
    # disconnect stops it
    cur = main.google.watch_info(DID())["id"]
    c.post("/google/disconnect", auth=A, data={"csrf": csrf}, follow_redirects=False)
    ok(cur not in S["channels"] and not main.google.watch_info(DID()), "disconnect stops the channel")
    ok(c.post("/google/notify", headers=hdr).status_code == 200, "late notices after disconnect: answered")
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
