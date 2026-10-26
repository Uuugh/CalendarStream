"""0.1.23 tests: first-time Autosync guide (order, checkpoints, errors) and the public-address mismatch warning."""
import os, re, sys
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="https://ccs.example.com")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main
A = ("t", "p"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop):
    with TestClient(main.app, base_url="https://css.example.com") as c:
        main.google.save_client("123456789012-abcdefghijklmnopqrstuvwxyz012345.apps.googleusercontent.com", "GOCSPX-test")
        p = c.get("/", auth=A).text
        ok("but this page is open at <b>css.example.com</b>" in p and "<b>ccs.example.com</b>" in p, "a misspelled public address is pointed out")
        ok("back to <code>https://ccs.example.com/google/callback</code>" in p, "Connect names the redirect URI Google will use")
        g = p[p.index("How to get a client ID and secret"):]
        order = [g.find(s) for s in ("Before you start", "Create a project", "Turn on the Calendar API", "Set up the sign-in screen",
                                    "Allow calendar access", "Let yourself sign in", "Create the client", "Copy both keys now", "Connect.</b>")]
        ok(all(i >= 0 for i in order) and order == sorted(order), f"guide steps in order, test users before the client {order}")
        ok(g.count("✓ ") >= 5, "the guide has checkpoints")
        ok("If Google shows an error" in g and "redirect_uri_mismatch" in g and "access_denied" in g and "invalid_client" in g, "the guide lists Google's errors")
        r = c.get("/google/callback?error=access_denied&state=x", auth=A, follow_redirects=False)
        ok(r.status_code in (302, 303, 307), "access_denied returns to the page")
        log = c.get("/", auth=A).text
        ok("Test users" in log, "access_denied explains test users")
        ok("but this page is open at" not in c.get("https://ccs.example.com/", auth=A).text, "no warning when the addresses match")
        ok("but this page is open at" not in c.get("http://192.168.1.5:8080/", auth=A).text, "no warning when opened by IP on the LAN")
        es = c.get("/", auth=A, headers={"Accept-Language": "es"}).text
        ok("Antes de empezar" in es and "Si Google muestra un error" in es, "guide translated (es)")
print("FAILS", fails)
