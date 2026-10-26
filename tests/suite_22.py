"""0.1.19 tests: Settings → Check for updates (channel-specific)."""
import asyncio, os, re, sys
from datetime import datetime, timedelta, timezone
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="https://cal.example.com")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import httpx
from fastapi.testclient import TestClient
from app import main, updates as U
A = ("t", "p"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
REMOTE = {"VERSION": "9.9.9\n", "STABLE": "0.0.6\n"}
asked = []
class FakeClient:
    def __init__(self, *a, **k): pass
    async def __aenter__(self): return self
    async def __aexit__(self, *a): pass
    async def get(self, url, headers=None):
        name = url.rsplit("/", 1)[1]; asked.append(name)
        return httpx.Response(200, text=REMOTE[name], request=httpx.Request("GET", url))
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(U.httpx, "AsyncClient", FakeClient), patch.object(U, "__version__", "0.1.19"), TestClient(main.app) as c:
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/", auth=A).text)[1]
    p = c.get("/", auth=A).text
    ok('id="updates"' in p and '<option value="weekly" selected>' in p and all(f'value="{f}"' in p for f in ("hourly", "monthly", "never")), "Settings: Check for updates, weekly by default")
    order = [m.group(1) for m in re.finditer(r'class="mgroup" id="([a-z]+)"', p)]
    ok(order == ["pagelogin", "public", "admin", "googlesync", "updates"], f"order: login, public address, admin, Google Calendar sync, updates ({order})")
    # stable install: only STABLE is consulted, a newer beta is never offered
    os.environ["IMAGE_TAG"] = "latest"
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    ok(asked[-1] == "STABLE" and not main.updates.available(), "stable install: checks STABLE; beta 9.9.9 not offered")
    p = c.get("/", auth=A).text
    ok('class="newver"' not in p and "Subscribed to stable versions" in p and "(Up to date)." in p and "Next check at" in p, "stable: no (version) in the title; 'Up to date'")
    REMOTE["STABLE"] = "9.2.0\n"
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    p = c.get("/", auth=A).text
    ok(main.updates.available() == "9.2.0" and "(v9.2.0 is available)</a>" in p and "/releases/tag/v" + main.__version__ in p and "/releases/tag/v9.2.0" in p, "a newer stable: (v9.2.0) next to the version, linked to its release")
    # beta install
    os.environ["IMAGE_TAG"] = "beta"
    ok(main.updates.info() == {}, "switching channel forgets the other channel's answer")
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    p = c.get("/", auth=A).text
    ok(asked[-1] == "VERSION" and main.updates.available() == "9.9.9" and "(v9.9.9 is available)" in p and "Subscribed to beta versions" in p and "version 9.9.9 available" in p, "beta install: checks VERSION; 9.9.9 offered")
    os.environ["IMAGE_TAG"] = "0.1.9"
    ok(U.channel() == "stable", "a pinned version follows stable")
    # frequency
    ok(c.post("/settings/updates", auth=A, data={"csrf": csrf, "frequency": "yearly"}).status_code == 400, "unknown frequency refused")
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "frequency": "never"})
    now = datetime.now(timezone.utc)
    ok(main.updates.frequency() == "never" and not main.updates.due(now + timedelta(days=400)), "never: never due")
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "frequency": "hourly"})
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    ok(not main.updates.due(now + timedelta(minutes=30)) and main.updates.due(now + timedelta(minutes=61)), "hourly: due after an hour")
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "frequency": "monthly"})
    ok(not main.updates.due(now + timedelta(days=29)) and main.updates.due(now + timedelta(days=31)), "monthly: due after 30 days")
    # failures keep the last answer
    class Broken(FakeClient):
        async def get(self, url, headers=None): raise httpx.ConnectError("no route")
    os.environ["IMAGE_TAG"] = "beta"
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    with patch.object(U.httpx, "AsyncClient", Broken):
        c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    p = c.get("/", auth=A).text
    ok(main.updates.available() == "9.9.9" and ("Couldn&#39;t check for updates" in p or "Couldn't check for updates" in p), "a failed check is shown and keeps the last answer")
    ok(c.post("/settings/updates", data={"csrf": csrf}).status_code == 401, "needs the status-page login")
    # "logged" survives a manual check, so the log announces each version once
    main.store.set("update_check", {**main.updates.info(), "logged": "9.9.9"})
    c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    ok(main.updates.info().get("logged") == "9.9.9", "Check now keeps the record of the announced version")
print("FAILED:", fails) if fails else print("ALL PASSED")
