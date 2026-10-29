"""0.2.8-beta.6 tests: a module's handle sits in its section's right margin, so calendars and feeds are
as wide as the section header (I1), on a computer and on a phone."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main, calsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, *a, **k):
    return calsync.Download(200, body=FEED, debug={"url": url})

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8097, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8097", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    seed.demo(c, csrf, main)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w in (1230, 390):
            pg = b.new_page(viewport={"width": w, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("http://127.0.0.1:8097/?month=2026-10"); pg.wait_for_timeout(500)
            for sec, mod in (("#sources", "#src-ccs"), ("#destinations", ".box.dest")):
                r = pg.evaluate("""([sec, mod]) => { const q = s => document.querySelector(s).getBoundingClientRect();
                  const m = document.querySelector(mod), h = m.closest('.modrow').querySelector(':scope > .handle').getBoundingClientRect();
                  return {sec: q(sec).right, plus: q(sec + ' > .cardhead .plus').right, mod: m.getBoundingClientRect().right, h: h.right, hl: h.left} }""", [sec, mod])
                ok(abs(r["mod"] - r["plus"]) <= 1, f"I1 ({w} px): {sec}: the module's right edge lines up with the + ({r})")
                ok(r["hl"] >= r["mod"] and r["h"] <= r["sec"] - 1, f"…its handle sits in the section's right margin")
            ok(pg.evaluate("document.documentElement.scrollWidth") <= w, f"…no sideways scroll at {w} px")
            ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
