"""0.2.7-beta.1 tests: semver versions with -beta.N (F1)."""
import os, re, sys
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="")
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
# Order: every beta of a version comes before it; beta.10 after beta.2.
order = ["0.2.6", "0.2.7-beta.1", "0.2.7-beta.2", "0.2.7-beta.10", "0.2.7", "0.2.8-beta.1", "0.3.0-beta.1", "0.3.0", "1.0.0-beta.1"]
ok(all(U.is_newer(b, a) and not U.is_newer(a, b) for a, b in zip(order, order[1:])), "F1.2: semver order, betas before their release")
ok(not U.is_newer("0.2.7-beta", "0.2.6") and not U.is_newer("0.2.7.1", "0.2.6") and not U.is_newer("0.2.7", "unknown"), "F1.2: anything else isn't a version")
ok(U.is_stable("0.2.7") and not U.is_stable("0.2.7-beta.1") and not U.is_stable("x"), "is_stable")
for tag, want in (("beta", "beta"), ("0.2.7-beta.1", "beta"), ("latest", "stable"), ("0.2.7", "stable"), ("", "stable")):
    os.environ["IMAGE_TAG"] = tag
    ok(U.channel() == want, f"F1.2: IMAGE_TAG {tag or '(unset)'} follows {want}")
REMOTE = {}
class FakeClient:
    def __init__(self, *a, **k): pass
    async def __aenter__(self): return self
    async def __aexit__(self, *a): pass
    async def get(self, url, headers=None):
        return httpx.Response(200, text=REMOTE[url.rsplit("/", 1)[1]], request=httpx.Request("GET", url))
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(U.httpx, "AsyncClient", FakeClient), patch.object(U, "__version__", "0.2.7-beta.1"), \
     patch.object(main, "__version__", "0.2.7-beta.1"), TestClient(main.app) as c:
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/", auth=A).text)[1]
    check = lambda: c.post("/settings/updates", auth=A, data={"csrf": csrf, "action": "check"})
    os.environ["IMAGE_TAG"] = "beta"
    REMOTE.update(VERSION="0.2.7-beta.2\n", STABLE="0.2.6\n")
    check(); p = c.get("/", auth=A).text
    ok('/releases/tag/v0.2.7-beta.1"' in p and ">v0.2.7-beta.1</a>" in p and "CalendarStream v0.2.7-beta.1 ·" in p, "F1.1: the full version at the top (linked) and in the footer")
    ok(main.updates.available() == "0.2.7-beta.2" and "(v0.2.7-beta.2 is available)" in p, "F1.2: a beta install is offered the next beta")
    REMOTE["VERSION"] = "0.2.7\n"; check()
    ok(main.updates.available() == "0.2.7", "F1.2: …and the release it leads to")
    os.environ["IMAGE_TAG"] = "latest"
    REMOTE.update(VERSION="0.2.8-beta.1\n", STABLE="0.2.7\n"); check()
    ok(main.updates.available() == "0.2.7", "F1.2: a stable install is offered the stable release only")
    REMOTE["STABLE"] = "0.2.9-beta.1\n"; r = check()
    ok(main.updates.info().get("error") and main.updates.available() == "0.2.7", "F1.2: a beta named in STABLE is refused (the last answer is kept)")
print("FAILS", fails)
