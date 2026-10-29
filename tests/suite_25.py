"""0.1.24 tests: admin e-mail (F1), password boxes (F2), public address out of .env (F6.1), Updates line (F6.3)."""
import os, re, sys
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main
A = ("t", "p"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    main.google.save_client("123456789012-abcdefghijklmnopqrstuvwxyz012345.apps.googleusercontent.com", "GOCSPX-test")
    p = c.get("/", auth=A).text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    ok('id="adminemail" name="email" value=""' in p and p.index('id="googlesync"') < p.index('id="admin"'), "F1: Admin e-mail in the Google Calendar API Sync block (0.2.8-beta.15), not set")
    ok("set ☰ Settings → <b>Admin e-mail</b>" in p, "F1: the guide points to it while it isn't set")
    post = lambda e: c.post("/settings/admin-email", auth=A, data={"csrf": csrf, "email": e}, follow_redirects=False)
    for bad in ("nope", "a@b", "<x>@y.com", "a b@c.com"):
        ok(post(bad).status_code == 400, f"F1: refused {bad!r}")
    ok(post(" pilot@gmail.com ").status_code == 303 and main.admin_email() == "pilot@gmail.com", "F1: saved, trimmed")
    p = c.get("/", auth=A).text
    g = p[p.index("Guided setup: a client ID and secret"):]
    ok(g.count("<code>pilot@gmail.com</code>") >= 3, "F1: guide uses it (support, contact e-mail, test user)")
    ok("&lt;code&gt;" not in g, "F1: not escaped twice")
    post("")
    ok(main.admin_email() == "", "F1: empty removes it")
    ok(len(re.findall(r'<input[^>]*data-strength', p)) == 2 and "_pwfield" not in p and "function level(pw, min)" in p, "F2: strength bar on the chosen passwords (page login, CCS+)")
    ok("Show password" in p, "F2: eye button script")
    ok(">Stable versions<" in p and ">Not checked<" in p and "Next check @" in p, "F6.3 (beta.5: as a module header): channel, state, next check")
    main.updates.set_frequency("never")
    p = c.get("/", auth=A).text
    ok("Automatic checks are off" in p, "F6.3: never → off")
    ok(main.store.get("public_url_imported") is True and main.public_url() == "", "F6.1: nothing to import from an empty PUBLIC_URL")
print("FAILS", fails)
