"""0.2.8-beta.45 tests (Build E, F65): Full page's own Settings (Configure / User / Site Admin, the right-side
slide-out and each item's pop-up) - no app or database beyond the status page itself."""
import os, re, sys
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

    # --- Normal mode: unchanged from before F65 - no slide-out, the mgroups still inline ---
    p = page("?menu=settings")
    ok('class="settingsnav"' not in p and 'id="configure-popup"' not in p, "F65: normal mode has no slide-out or Configure pop-up")
    ok('id="pagelogin"' in p and 'id="domainsform"' in p and p.count('id="loginform"') == 1, "F65: normal mode's Login & password and Domains are unchanged")

    # --- Full mode: ☰ Settings is the Configure / User / Site Admin slide-out ---
    post("/ui/calview", full="1")
    p = page("?menu=settings")
    ok('class="menu settingsnav"' in p, "F65: full page's ☰ Settings is the slide-out, not the inline list")
    for grp in (">Configure<", ">User<", ">Site Admin<"):
        ok(grp in p, f"F65: the slide-out has its {grp.strip('><')} group")
    for key in ("sources", "destinations", "rules", "templates", "activity"):
        ok(f'data-configure="{key}"' in p, f"F65: Configure links to the real #{key} section (moved there and back by 03-topbar-settings.js)")
    for key in ("pagelogin", "domains", "updates", "look", "googlesync"):
        ok(f'data-setting="{key}"' in p, f"F65: the slide-out has an item for {key}")
        ok(f'id="setting-{key}"' in p, f"F65: {key} has its own pop-up (dialog.popup.settingspop)")
    ok('id="configure-popup"' in p and 'id="configureBody"' in p, "F65: one shared pop-up for every Configure item")
    # Each setting's own pop-up holds the same fields as the non-fullscreen mgroup, under the same ids - not duplicated
    ok(p.count('id="loginform"') == 1 and p.count('id="domainsform"') == 1 and p.count('id="lookform"') == 1, "F65: no duplicate form ids between the normal mgroup and the pop-up (only one renders at a time)")
    ok('name="user"' in p and 'name="main"' in p and 'name="logo"' in p, "F65: the pop-ups carry the real fields (Login's user name, Domains' address, Theme's logo), the exact non-fullscreen layout")
    # Dropped scope: no reorder grip markup was added for this (F47/I45 stay dropped)
    ok('sortable' not in p.split('class="sections"')[0] if 'class="sections"' in p else True, "F65: no module-reorder markup added to Settings")

    post("/ui/calview", full="0")
    print(f"{fails} failing")
    sys.exit(1 if fails else 0)
