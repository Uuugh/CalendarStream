"""0.2.8-beta.13 tests: one action, one state (I1): the top bar's Update now and Settings → Update now show
the same words at the same moment (Downloading…, then Updated, or Update failed) and end together, whichever
is pressed. Also: the working Google Calendar API Sync group shows everything (beta.12). A stand-in Watchtower."""
import os, re, sys, tempfile, threading, time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
tok = tempfile.NamedTemporaryFile("w", delete=False); tok.write("sekret-token\n"); tok.close()
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="",
                  UPDATER_URL="http://127.0.0.1:8118", UPDATER_TOKEN_FILE=tok.name, IMAGE_TAG="beta")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch, PropertyMock
import uvicorn, httpx, seed
from app import main, updates as U, gsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
class Fake(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def answer(self, code):
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b"{}")
    def do_GET(self): self.answer(200 if self.path == "/livez" else 404)
    def do_POST(self): self.answer(202 if self.headers.get("Authorization") == "Bearer sekret-token" else 401)
fake = ThreadingHTTPServer(("127.0.0.1", 8118), Fake); threading.Thread(target=fake.serve_forever, daemon=True).start()
WORDS = """() => { const top = document.querySelector('.updslot'), b = document.querySelector('#updates button.upgradebtn');
  const st = b ? b.dataset.state : '', sn = b ? b.querySelector('.sn.' + (st === 'syncing' ? 'syncing' : st)) : null;
  return [top ? top.dataset.state : '', top ? top.querySelector('.updtext').textContent.trim() : '', st, sn ? sn.textContent.trim() : '']; }"""
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(U, "__version__", "0.2.7-beta.2"), patch.object(main, "__version__", "0.2.7-beta.2"):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8119, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8119", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    main.store.set("update_check", {"checked": datetime.now(timezone.utc).isoformat(), "channel": "beta", "newest": "0.2.7-beta.3"})
    ok(main.updater.ready, "the stand-in updater is found")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1230, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        for which in ("#updates .upgradebtn", ".updslot .updbtn"):
            open(tok.name, "w").write("sekret-token")
            pg.goto("http://127.0.0.1:8119/?menu=settings"); pg.wait_for_timeout(500)
            pg.click(which); pg.wait_for_timeout(300)
            w = pg.evaluate(WORDS)
            ok(w[0] == "downloading" and w[2] == "syncing" and w[1] == w[3] == "Downloading…", f"I1 ({which}): both copies say Downloading… {w}")
            U.__version__ = main.__version__ = "0.2.7-beta.3"          # the restarted container
            seen = None
            for _ in range(40):
                pg.wait_for_timeout(100)
                try:
                    w = pg.evaluate(WORDS)
                except Exception:
                    break
                if w[0] == "done":
                    seen = w; break
            ok(seen and seen[2] == "done" and seen[1] == seen[3] == "Updated", f"I1 ({which}): both say Updated together {seen}")
            pg.wait_for_timeout(1500)
            ok("v0.2.7-beta.3" in pg.inner_text(".topbar") and pg.locator("#updates .upgradebtn").count() == 0, "…then the page reloads with the new version")
            U.__version__ = main.__version__ = "0.2.7-beta.2"
        # a refused update: both say Update failed, and both go back together
        open(tok.name, "w").write("other")
        pg.goto("http://127.0.0.1:8119/?menu=settings"); pg.wait_for_timeout(500)
        pg.click("#updates .upgradebtn"); pg.wait_for_timeout(700)
        w = pg.evaluate(WORDS)
        ok(w[0] == "failed" and w[2] == "fail" and w[1] == w[3] == "Update failed", f"I1: refused: both say Update failed {w}")
        pg.wait_for_timeout(2600)
        w = pg.evaluate(WORDS)
        ok(w[0] == "ready" and w[2] == "idle", f"…and both go back together {w}")
        # beta.12: the working Google group shows everything
        with patch.object(gsync.Google, "connected", new_callable=PropertyMock, return_value=True):
            main.store.set("google_client", {"id": "123-abc.apps.googleusercontent.com", "secret": main.google._seal("s"),
                                             "check": {"ok": True, "message": "", "at": "2026-10-20T20:00:00+00:00", "redirect_ok": True}})
            main.google._client = None
            pg.goto("http://127.0.0.1:8119/?menu=settings"); pg.wait_for_timeout(500)
            ok(pg.locator("#googlesync .cfgline").count() == 0 and pg.is_visible("#googlesync .credtrash") and pg.is_visible("#googlesync .gremoverow button.danger")
               and pg.is_visible("#googlesync .gremoverow input[name=delete]"), "beta.12: the working Google group: no Expand; the trash, Remove and Also delete all showing")
            r = pg.evaluate("""() => { const g = document.querySelector('#googlesync .gremoverow').getBoundingClientRect(), b = document.querySelector('#googlesync .gremoverow button').getBoundingClientRect(),
                               m = document.getElementById('googlesync').getBoundingClientRect(); return [Math.round(b.left - m.left), Math.round(m.bottom - g.bottom)]; }""")
            ok(r[0] <= 14 and r[1] <= 14, f"…Remove in the lower left {r}")
        ok(not errs, f"no script errors {errs}")
        b.close()
    fake.shutdown(); srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
