"""0.1.0 tests: check interval, upload placement, theme order, client check."""
import os, re, sys, threading, time
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="http://localhost",
                  CCS_USERNAME="", CCS_PASSWORD="", SYNC_INTERVAL_MINUTES="60")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
import uvicorn, mockgoogle
from datetime import timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
M = "http://127.0.0.1:8099"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8099, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
A = ("t", "p"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), TestClient(main.app) as c:
    p = c.get("/", auth=A).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    order = re.findall(r'data-theme-choice="(\w+)"', p)
    ok(order == ["light", "dark", "system"], f"theme order {order}")
    body = p[p.index('id="src-ccs"'):]
    ok(body.index('class="srcstatus"') < body.index('action="/setup/interval"') < body.index('action="/setup/upload"') < body.index('id="destinations"'),
       "0.2.2: last download, interval (header) → upload (Configure) → destinations")
    ok(p.count('action="/setup/upload"') == 1 and 'class="sub"' not in p.split("</header>")[1][:300], "upload only once; old line under the title gone")
    ok('name="minutes" value="60"' in p, "interval box shows 60")
    main.state.last_attempt = main.now() - timedelta(minutes=10)
    r = c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "30"}, follow_redirects=False)
    ok(r.status_code == 303 and main.interval_minutes() == 30 and main.state.wake.is_set(), "interval saved, loop woken")
    ok(abs((main.state.next_run - (main.state.last_attempt + timedelta(minutes=30))).total_seconds()) < 2, "next check = last check + 30 min")
    main.state.last_attempt = main.now() - timedelta(minutes=100)
    c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "45"})
    ok((main.state.next_run - main.now()).total_seconds() < 5, "overdue → checks right away")
    ok(c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "5"}).status_code == 400, "below 15 refused")
    ok(c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "abc"}).status_code == 400, "not a number refused")
    ok(c.post("/setup/interval", auth=A, data={"csrf": "x", "minutes": "30"}).status_code == 400, "needs CSRF")
    c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "60"})
    ok(main.store.get("sync_interval") is None and main.interval_minutes() == 60, "back to the .env value clears the override")
    ok('name="minutes" value="60"' in c.get("/", auth=A).text, "page shows it")

    # Client check
    save = lambda cid, sec: c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": cid, "client_secret": sec, "action": "save"})
    save("test-client.apps.googleusercontent.com", "test-secret")
    ck = main.google.client_check(); p = c.get("/", auth=A).text
    ok(ck.get("ok") is True and "✓" in p and "Google accepted the client ID and secret" in p, "right ID + secret → accepted")
    ok(p.index('action="/google/client"') < p.index('Guided setup: a client ID and secret') and '<details class="guide gsteps" open' not in p, "form above the guide; guide closed")
    save("test-client.apps.googleusercontent.com", "wrong")
    p = c.get("/", auth=A).text
    ok(main.google.client_check().get("ok") is False and "Google rejected the client secret" in p and "Client rejected" in p and '<div class="gstepmsg check bad">' in p, "wrong secret → rejected, said under the row (beta.14: Connect stops there)")
    save("999999999999-nope.apps.googleusercontent.com", "test-secret")
    ok("doesn't know this client ID" in main.google.client_check().get("message", ""), "unknown ID reported")
    save("test-client.apps.googleusercontent.com", "test-secret")
    srv.should_exit = True; time.sleep(1.5)
    c.post("/google/client", auth=A, data={"csrf": csrf, "action": "check"})
    ck = main.google.client_check()
    ok(ck.get("ok") is None and "couldn't reach Google" in ck.get("message", ""), "Google unreachable → unknown, not failed")
    ok("test-secret" not in " ".join(h["msg"] for h in main.store.recent_log(20)), "secret never logged")
print("FAILED:", fails) if fails else print("ALL PASSED")
