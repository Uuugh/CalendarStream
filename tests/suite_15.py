import os, re, sys
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL=sys.argv[2], CCS_USERNAME="", CCS_PASSWORD="")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main
A = ("t", "p"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), TestClient(main.app) as c:
    p = c.get("/", auth=A).text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    env = sys.argv[2]
    if env:
        ok(f'value="{env}"' in p and main.store.get("public_url") == env and "PUBLIC_URL" not in p.split('id="menu"')[1].split("</header>")[0], "F6.1: PUBLIC_URL from .env moved into Settings once")
    else:
        ok("Not set yet." in p and "Set the <b>Public address</b> in Settings" in p, "unset: warnings point to Settings")
    post = lambda **d: c.post("/settings/public-url", auth=A, data={"csrf": csrf, **d}, follow_redirects=False)
    r = post(url="cal.example.org/")
    ok(r.status_code == 303 and main.public_url() == "https://cal.example.org", "bare host → https://, slash dropped")
    p = c.get("/", auth=A).text
    ok("https://cal.example.org/calendar/" in p and "https://cal.example.org/google/callback" in p, "links and redirect URI use it")
    ok("PUBLIC_URL" not in p.split('id="menu"')[1].split("</header>")[0] and "Not set yet." not in p.split('id="public"')[1].split('id="admin"')[0], "F6.1: no mention of .env")
    for bad in ("ftp://x.com", "https://x.com/?a=1", "https://user:pw@x.com", "not a url"):
        ok(post(url=bad).status_code == 400, f"refused: {bad}")
    ok(c.post("/settings/public-url", auth=A, data={"csrf": "x", "url": "https://a.com"}).status_code == 400, "needs CSRF")
    post(url="")
    ok(main.public_url() == "" and main.store.get("public_url") is None, "an empty address removes it")
    main.import_public_url()
    ok(main.public_url() == "", "F6.1: .env isn't imported again after it was removed")
    s = c.get(f"/subscribe/{main.settings.feed_token}").text
    ok("Set the public address in CalendarStream" in s, "subscribe page warning")
print("FAILED:", fails) if fails else print("ALL PASSED")
