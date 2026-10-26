"""0.2.8-beta.7 tests: Settings → Updates (I1): the button is Update; it keeps working after Settings is
redrawn by Check now; once the update is in, Updates goes back to Up to date and Check now, which works
again. A stand-in Watchtower and a stand-in check (no GitHub)."""
import os, re, sys, tempfile, threading, time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
tok = tempfile.NamedTemporaryFile("w", delete=False); tok.write("sekret-token\n"); tok.close()
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="",
                  UPDATER_URL="http://127.0.0.1:8113", UPDATER_TOKEN_FILE=tok.name, IMAGE_TAG="beta")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main, updates as U
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
class Fake(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def answer(self, code):
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b"{}")
    def do_GET(self): self.answer(200 if self.path == "/livez" else 404)
    def do_POST(self): self.answer(202 if self.path.startswith("/v1/update") else 404)
fake = ThreadingHTTPServer(("127.0.0.1", 8113), Fake); threading.Thread(target=fake.serve_forever, daemon=True).start()
checks = []
async def fake_check():
    checks.append(1)
    r = {"checked": datetime.now(timezone.utc).isoformat(), "channel": "beta", "newest": "0.2.7-beta.3"}
    main.store.set("update_check", r); return r
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(U, "__version__", "0.2.7-beta.2"), patch.object(main, "__version__", "0.2.7-beta.2"), patch.object(main.updates, "check", fake_check):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8099, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8099", auth=("t", "password1"))
    c.get("/")
    main.store.set("update_check", {"checked": "2026-10-22T00:00:00+00:00", "channel": "beta", "newest": "0.2.7-beta.3"})
    ok(main.updater.ready, "the stand-in updater is found")
    ud = c.get("/?menu=settings").text; ud = ud[ud.index('id="updates"'):]; ud = ud[:ud.index("</form>")]
    ok(re.search(r'<button type="button" class="upgradebtn">.*?Update now</button>', ud) is not None and "Upgrade" not in ud, "I1.1: Settings → Updates says Update now (like the top bar), not Upgrade")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1300, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8099/?menu=settings"); pg.wait_for_timeout(500)
        # Check now first: Settings is redrawn in place, Update still works afterwards
        main.store.set("update_check", {"checked": "2026-10-22T00:00:00+00:00", "channel": "beta", "newest": "0.2.7-beta.2"})
        pg.goto("http://127.0.0.1:8099/?menu=settings"); pg.wait_for_timeout(500)
        pg.click("#updates button.checknow"); pg.wait_for_timeout(4200)
        ok(len(checks) == 1 and pg.locator("#updates button.upgradebtn").count() == 1 and "Update available" in pg.inner_text("#updates"),
           "Check now finds the newer version: Update available, Update")
        pg.click("#updates button.upgradebtn"); pg.wait_for_timeout(600)
        ok(pg.get_attribute(".updslot", "data-state") == "downloading" and pg.locator("#updates button.upgradebtn").is_disabled(),
           "I1.2: Update works after the redraw (Downloading… at the top; Update waits)")
        U.__version__ = main.__version__ = "0.2.7-beta.3"          # the restarted container
        pg.wait_for_timeout(3500)
        ok(pg.inner_text(".curver") == "v0.2.7-beta.3" and pg.locator(".updslot").count() == 0, "…the new version at the top")
        ok(pg.locator("#updates button.upgradebtn").count() == 0 and pg.locator("#updates button.checknow").count() == 1 and "Up to date" in pg.inner_text("#updates"),
           "I1.2: Settings → Updates goes back to Up to date with Check now")
        pg.click("#updates button.checknow"); pg.wait_for_timeout(4200)
        ok(len(checks) == 2 and "Up to date" in pg.inner_text("#updates") and pg.locator("#updates button.checknow").count() == 1, "…and Check now works again")
        ok(not errs, f"no script errors {errs}")
        b.close()
    fake.shutdown(); srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
