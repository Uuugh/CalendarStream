"""0.2.8-beta.16 tests: a Google module's Remove names its calendar without "the" (I2); a deleted event says where it
was deleted, not "Edited here" (I3); the release workflow scans the image with trivy before publishing (F1)."""
import os, re, sys
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main
import seed
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = ("t", "password1")
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Flying", "sources": ["ccs"]})
    seed.demo(c, csrf, main)
    p = page()
    # I2: "delete Flying", not "delete the Flying"
    asks = re.findall(r'data-yesdel="([^"]*)"', p) + re.findall(r'data-yeskeep="([^"]*)"', p)
    mods = [a for a in asks if "the module" in a]
    ok(mods and all(" the Flying" not in a for a in mods) and any("delete Flying from Google Calendar" in a for a in mods),
       f"I2: a Google module's Remove names its calendar without 'the' ({mods[:2]})")
    # I3: a deleted event says where, not "Edited here"
    ev = next(e for e in main.store.load_events("ccs") if e.origin == "united" and not e.hidden)
    c.post("/event/delete", data={"csrf": csrf, "uid": ev.uid})
    p = page(f"?date={ev.start[:10]}")
    m = re.search(r'<details data-uid="' + re.escape(ev.uid) + r'".*?</details>', p, re.S)
    block = m.group(0) if m else ""
    ok(block and 'class="delnote"' in block and "Edited here" not in block,
       "I3: a deleted event shows where it was deleted, and not 'Edited here'")
# F1: trivy runs before anything is tagged or published, pinned, blocking only on fixable High/Critical
wf = open(os.path.join(os.path.dirname(HERE), ".github", "workflows", "release.yml")).read()
beta = wf[wf.index("trivy gate"):]
ok(wf.index("trivy gate") < wf.index("Tag v<VERSION> and move beta") < wf.index("Build and push image"),
   "F1: the trivy scan comes before the tag and the published image")
ok(re.search(r"aquasecurity/trivy-action@[0-9a-f]{40}", wf) and "severity: HIGH,CRITICAL" in beta and "ignore-unfixed: true" in beta
   and "exit 1" in beta and "::error title=trivy gate" in beta, "F1: pinned to a commit; stops the beta on a fixable High or Critical only")
print("FAILED:", fails) if fails else print("ALL PASSED")
