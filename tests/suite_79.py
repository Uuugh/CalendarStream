"""0.2.8-beta.41 tests (Build B): F51's new stretch-bar spec (a centered bar, dots as the drag handle, fixed
collapse/expand side arrows, a lower -300 floor) and F15.2's rework (a single hollow clock icon instead of the
12 | 24 segmented switch)."""
import os, re, sys, asyncio
from unittest.mock import patch
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"): del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
from fastapi.testclient import TestClient
from app import main
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    import seed; seed.demo(c, csrf, main)

    # --- F51: the stretch bar is centered, no longer a single left/right button ---
    p = page("?date=2026-10-14")
    ok('id="calstretchbar"' in p and 'id="calcollapse"' in p and 'id="calexpand"' in p, "F51: the stretch bar has its collapse and expand side arrows")
    ok('class="calstretch" id="calstretch"' in p and 'role="slider"' in p, "F51: the dots (the drag handle) are a slider, not a button")
    ok('class="stretchdots"' in p and p.count('<circle', p.index('stretchdots')) >= 12, "F51: twelve dots (two rows of six), the same look as a module's own handle")
    ok('class="calstretch" id="calstretch"' in p and '<button type="button" class="calstretch"' not in p, "F51: the old single stretch button is gone")
    ok('body.gripsright .calstretch' not in open(os.path.join(REPO, "app", "styles", "19-calendar.css")).read(), "F51: the stretch bar no longer follows the Reorder grips left/right setting")

    # --- F51: the floor moved from 0 to -300, so there's room to compress past the old minimum ---
    ok(post("/ui/calview", stretch="-300").status_code in (200, 204, 303) and main.store.get("ui_calview").get("stretch") == -300,
       "F51: -300 (the new floor) is accepted and saved")
    ok(post("/ui/calview", stretch="-301").status_code == 400, "F51: past the new floor is still rejected")
    ok(post("/ui/calview", stretch="-120").status_code in (200, 204, 303) and main.store.get("ui_calview").get("stretch") == -120,
       "F51: a value between the old and new floor is accepted")
    post("/ui/calview", stretch="0")   # leave it clean for later suites

    # --- F15.2: one hollow clock icon, not a segmented switch; the current number is on the icon itself ---
    ok('id="clockswitch"' not in p, "F15.2: the old segmented 12 | 24 switch is gone")
    ok('id="clockicon"' in p and 'role="switch"' in p.split('id="clockicon"', 1)[0][-200:] + p.split('id="clockicon"', 1)[1][:200],
       "F15.2: the new single clock icon control is present, still a switch")
    ok('class="clocknum"' in p and ">12<" in p.split('id="clockicon"', 1)[1][:500], "F15.2: the icon itself carries the current format (12h by default)")
    ok(post("/ui/clock", clock="24").status_code in (200, 204, 303), "F15.2: switching to 24h still saves")
    p24 = page("?date=2026-10-14")
    ok('aria-checked="true"' in p24.split('id="clockicon"', 1)[1][:200] and ">24<" in p24.split('id="clockicon"', 1)[1][:500],
       "F15.2: after switching, the icon shows 24 and aria-checked flips")
    post("/ui/clock", clock="12")   # leave it clean for later suites

print(("ALL %d PASS" if not fails else "%d FAILURES") % fails); sys.exit(1 if fails else 0)
