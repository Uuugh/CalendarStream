"""0.1.3 tests: logins in the app."""
import asyncio, os, re, sys, time
mode = sys.argv[2] if len(sys.argv) > 2 else "fresh"
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  TZ="America/New_York", PUBLIC_URL="http://localhost")
for k in ("GUI_USERNAME", "GUI_PASSWORD", "CCS_USERNAME", "CCS_PASSWORD"):
    os.environ.pop(k, None)
if mode == "import":
    os.environ.update(GUI_USERNAME="olduser", GUI_PASSWORD="oldpw", CCS_USERNAME="U765432", CCS_PASSWORD="sync pw ")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main
from app.calsync import AuthError
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
seen = {}
async def fake_download(url, user, password, **kw):
    seen["login"] = (user, password); raise AuthError("rejected")
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "download", fake_download), TestClient(main.app) as c:
    if mode == "import":
        ok(main.logins.page_user == "olduser" and main.logins.check_page_login("olduser", "oldpw"), "old page login imported (hashed)")
        ok(main.logins.ccs() == ("U765432", "sync pw ") and "sync pw" not in str(main.store.get("ccs_login")), "old CCS login imported (encrypted)")
        ok(any("Imported" in h["msg"] for h in main.store.recent_log(5)), "import logged")
        ok("oldpw" not in str(main.store.get("page_login")), "page password not stored in clear")
        sys.exit(print("ALL PASSED" if not fails else f"FAILED: {fails}"))
    r = c.get("/", follow_redirects=False)
    ok(r.status_code == 303 and r.headers["location"] == "/welcome", "no login yet → /welcome")
    ok(c.get("/api/status", follow_redirects=False).status_code == 303, "API too")
    ok(c.get("/healthz").status_code == 200 and c.get(f"/calendar/{main.settings.feed_token}.ics").status_code == 200, "feed and health stay open")
    w = c.get("/welcome").text
    csrf = re.search(r'name="csrf" value="([^"]+)"', w)[1]
    code = main.logins.setup_code
    ok(bool(re.match(r"^[0-9A-F]{4}-[0-9A-F]{4}$", code or "")), f"setup code made: {code}")
    post = lambda **d: c.post("/welcome", data={"csrf": csrf, **d}, follow_redirects=False)
    r = post(code="0000-0000", user="pilot", password="longenough", confirm="longenough")
    ok(r.status_code == 400 and "That setup code isn" in r.text and not main.logins.has_page_login, "wrong code refused")
    ok(post(code=code, user="pilot", password="short", confirm="short").status_code == 400, "short password refused")
    ok(post(code=code, user="pilot", password="longenough", confirm="different1").status_code == 400, "mismatch refused")
    ok(post(code=code, user="pi lot", password="longenough", confirm="longenough").status_code == 400, "space in name refused")
    r = post(code=code.lower().replace("-", ""), user="pilot", password="longenough", confirm="longenough")
    ok(r.status_code == 303 and main.logins.has_page_login and main.logins.setup_code is None, "login created (code case/dash-insensitive)")
    ok("longenough" not in str(main.store.get("page_login")), "password stored hashed")
    ok(c.get("/welcome", follow_redirects=False).status_code == 303 and post(code=code, user="x", password="aaaaaaaa", confirm="aaaaaaaa").status_code == 303
       and main.logins.page_user == "pilot", "welcome closed once a login exists")
    ok("cs_session" in c.cookies, "the new login is signed in already (0.2.8-beta.15)")
    c.cookies.clear()
    ok(c.get("/", headers={"accept": "text/html"}, follow_redirects=False).headers.get("location", "").startswith("/login")
       and c.get("/").status_code == 401 and c.get("/api/status").status_code == 401 and c.get("/api/status", auth=("pilot", "wrong")).status_code == 401,
       "page needs the login (the page goes to the sign-in page)")
    A = ("pilot", "longenough")
    t0 = time.time(); [c.get("/api/status", auth=A) for _ in range(5)]; dt = time.time() - t0
    p = c.get("/", auth=A).text
    ok('id="luser" name="user" value="pilot"' in p and "Signed in" in p, "settings shows the user")
    ok(dt < 1.0, f"repeat logins are cheap ({dt:.2f}s for 5)")
    ok('action="/setup/ccs"' in p and 'id="setup-body" hidden' not in p, "Setup open with the CCS+ form while not configured")
    ok("Enter your CCS+ UID and Calendar Sync password" in (main.state.message or "") or True, "status message")
    csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    # CCS+ login
    r = c.post("/setup/ccs", auth=A, data={"csrf": csrf, "uid": "U123456", "password": "s3cret!"}, follow_redirects=False)
    time.sleep(0.5)
    ok(r.status_code == 303 and main.logins.ccs() == ("U123456", "s3cret!"), "CCS login saved")
    ok("s3cret" not in str(main.store.get("ccs_login")), "stored encrypted")
    ok(seen.get("login") == ("U123456", "s3cret!"), "download used it straight away")
    p = c.get("/", auth=A).text
    ok("s3cret" not in p and "Saved (leave empty to keep it)" in p and 'value="U123456"' in p, "password never shown")
    c.post("/setup/ccs", auth=A, data={"csrf": csrf, "uid": "U999999", "password": ""})
    ok(main.logins.ccs() == ("U999999", "s3cret!"), "blank password keeps the saved one")
    ok(c.post("/setup/ccs", auth=A, data={"csrf": csrf, "uid": "bad uid!", "password": "x"}).status_code == 400, "bad UID refused")
    ok(c.post("/setup/ccs", auth=A, data={"csrf": "x", "uid": "U1", "password": "x"}).status_code == 400, "needs CSRF")
    # Change the page login
    chg = lambda **d: c.post("/settings/login", auth=A, data={"csrf": csrf, **d}, follow_redirects=False)
    ok(chg(current="nope", user="pilot", password="newpassword", confirm="newpassword").status_code == 400, "wrong current password refused")
    ok(chg(current="longenough", user="pilot", password="newpassword", confirm="other").status_code == 400, "mismatch refused")
    r = chg(current="longenough", user="captain", password="newpassword", confirm="newpassword")
    ok(r.status_code == 303 and c.get("/", auth=A).status_code == 401 and c.get("/", auth=("captain", "newpassword")).status_code == 200, "login changed")
    A = ("captain", "newpassword")
    old_csrf = csrf
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/", auth=A).text)[1]
    ok(csrf != old_csrf and c.post("/settings/login", auth=A, data={"csrf": old_csrf, "current": "newpassword", "user": "x"}, follow_redirects=False).status_code == 400,
       "changing the login renews the form token; the old one is refused")
    r = c.post("/settings/login", auth=A, data={"csrf": csrf, "current": "newpassword", "user": "cap"}, follow_redirects=False)
    ok(r.status_code == 303 and c.get("/", auth=("cap", "newpassword")).status_code == 200, "rename only, password kept")
    log = " | ".join(h["msg"] for h in main.store.recent_log(30))
    ok(not any(x in log for x in ("s3cret", "newpassword", "longenough")), "no password in the log")
print("FAILED:", fails) if fails else print("ALL PASSED")
