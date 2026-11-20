"""0.2.7-beta.3 tests: F1 Update now through the updater container (a stand-in Watchtower here)."""
import asyncio, json, os, re, sys, tempfile, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
tok = tempfile.NamedTemporaryFile("w", delete=False); tok.write("sekret-token\n"); tok.close()
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="",
                  UPDATER_URL="http://127.0.0.1:8112", UPDATER_TOKEN_FILE=tok.name, IMAGE_TAG="beta")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main, updates as U
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
asked = []
class Fake(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def answer(self, code, body=b"{}"):
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        self.answer(200 if self.path == "/livez" else 404)
    def do_POST(self):
        u = urlparse(self.path); asked.append((u.path, parse_qs(u.query), self.headers.get("Authorization")))
        if self.headers.get("Authorization") != "Bearer sekret-token": return self.answer(401)
        self.answer(202 if u.path == "/v1/update" else 404)
fake = ThreadingHTTPServer(("127.0.0.1", 8112), Fake); threading.Thread(target=fake.serve_forever, daemon=True).start()
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(U, "__version__", "0.2.7-beta.2"), patch.object(main, "__version__", "0.2.7-beta.2"):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8098, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8098", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    main.store.set("update_check", {"checked": "2026-10-22T00:00:00+00:00", "channel": "beta", "newest": "0.2.7-beta.3"})
    ok(main.updater.ready, "F1.1: the updater is found (its /livez answers)")
    p = c.get("/").text
    ok('class="updslot" data-state="ready" data-from="0.2.7-beta.2" data-to="0.2.7-beta.3"' in p and ">Update now</button>" in p, "F1.2: Update now next to (v0.2.7-beta.3 is available)")
    ok("Updater: running" not in p and "run the installer again and answer yes to updating" not in p, "0.2.8-beta.5: with the updater, Settings doesn't need to say so")
    r = c.post("/update/now", data={"csrf": csrf}, headers={"X-CS-Async": "1"})
    path, q, auth = asked[-1]
    ok(r.status_code == 200 and r.json()["to"] == "0.2.7-beta.3" and path == "/v1/update" and q == {"image": ["ghcr.io/uuugh/calendarstream"], "async": ["true"]} and auth == "Bearer sekret-token",
       "F1.1: asks the updater to update only CalendarStream's image, with the token, in the background")
    ok("Updating to CalendarStream 0.2.7-beta.3" in c.get("/").text, "…and says so in Activities and Logs")
    ok(c.post("/update/now", data={"csrf": "wrong"}, headers={"X-CS-Async": "1"}).status_code in (400, 403), "a wrong CSRF token is refused")
    open(tok.name, "w").write("other")
    r = c.post("/update/now", data={"csrf": csrf}, headers={"X-CS-Async": "1"})
    ok(r.status_code == 502 and "refused the token" in r.json()["detail"], "a token the updater refuses: the reason comes back")
    open(tok.name, "w").write("sekret-token")
    os.environ["IMAGE_TAG"] = "0.2.7-beta.2"
    p = c.get("/").text
    ok('class="updslot"' not in p and c.post("/update/now", data={"csrf": csrf}, headers={"X-CS-Async": "1"}).status_code == 400, "an exact version in IMAGE_TAG: no Update now")
    os.environ["IMAGE_TAG"] = "beta"
    # The page follows along: while /api/status still says the old version it's Downloading…; when it
    # says the new one the pill goes and the version at the top changes.
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1300, "height": 800}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8098/"); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(tempfile.gettempdir(), "cs-upd_ready.png"), clip={"x": 0, "y": 0, "width": 700, "height": 60})
        pg.click(".updbtn"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(tempfile.gettempdir(), "cs-upd_down.png"), clip={"x": 0, "y": 0, "width": 700, "height": 60})
        ok(pg.get_attribute(".updslot", "data-state") == "downloading" and "Downloading" in pg.inner_text(".updslot") and pg.is_visible(".updbar i"), "F1.2: Downloading… with a moving bar")
        main.__version__ = U.__version__ = "0.2.7-beta.3"          # the restarted container (the page reloads, beta.9)
        pg.wait_for_timeout(3000)
        ok(pg.locator(".updslot").count() == 0 and pg.locator(".newver").count() == 0 and pg.inner_text(".curver") == "v0.2.7-beta.3"
           and pg.get_attribute(".curver", "href").endswith("/tag/v0.2.7-beta.3") and "v0.2.7-beta.3" in pg.inner_text(".foot"), "F1.2: when it's back: blank, and the version reads v0.2.7-beta.3")
        main.__version__ = U.__version__ = "0.2.7-beta.2"
        open(tok.name, "w").write("other")
        pg.goto("http://127.0.0.1:8098/"); pg.wait_for_timeout(300)
        pg.click(".updbtn"); pg.wait_for_timeout(800)
        ok(pg.get_attribute(".updslot", "data-state") == "failed" and "refused the token" in (pg.get_attribute(".updslot", "title") or ""), "F1.2: a refused update shows ✗ Update failed, with the reason")
        ok(not errs, f"no script errors {errs}")
        b.close()
    fake.shutdown()
    asyncio.run(main.updater.probe())
    p = c.get("/").text
    ok(not main.updater.ready and 'class="updslot"' not in p and "To update from here: run the installer again" in p, "no updater running: no Update now; Settings says how to add it")
    srv.should_exit = True
print("FAILS", fails)
