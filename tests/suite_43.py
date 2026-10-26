"""0.2.8-beta.8 tests: Settings → Check now works like Sync Now (I1): Checking… growing over the status
box, then Up to date (green), Update found (yellow) or Couldn't check (yellow), then back to rest with
Updates redrawn; it works every time. A stand-in check (no GitHub)."""
import os, re, sys, tempfile, threading, time
from datetime import datetime, timezone
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="", IMAGE_TAG="beta")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main, updates as U
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
answer = {"newest": "0.2.7-beta.2"}; checks = []
async def fake_check():
    checks.append(1)
    r = {"checked": datetime.now(timezone.utc).isoformat(), "channel": "beta", **answer}
    main.store.set("update_check", r); return r
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(U, "__version__", "0.2.7-beta.2"), patch.object(main, "__version__", "0.2.7-beta.2"), patch.object(main.updates, "check", fake_check):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8102, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8102", auth=("t", "password1")); c.get("/")
    ud = c.get("/?menu=settings").text; ud = ud[ud.index('id="updates"'):]; ud = ud[:ud.index("</form>")]
    ok('class="syncnow checknow" name="action" value="check" data-state="idle"' in ud and "Checking…" in ud and "Couldn’t check" in ud,
       "I1: Check now is a Sync Now button (Checking…, Up to date, Update found, Couldn't check)")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1300, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8102/?menu=settings"); pg.wait_for_timeout(600)
        btn = "#updates button.checknow"; box = "#updates .statusbox"
        rest = pg.locator(btn).bounding_box()
        ok(rest["height"] < 26, f"at rest: Check now at the bottom of the box ({rest['height']:.0f} px)")
        for n in (1, 2):                     # the same answer twice: each click shows it
            pg.click(btn); pg.wait_for_timeout(350)
            grown = pg.locator(btn).bounding_box(); sb = pg.locator(box).bounding_box()
            ok(pg.get_attribute(btn, "data-state") == "syncing" and "Checking" in pg.inner_text(btn) and grown["height"] > sb["height"] - 10,
               f"click {n}: Checking…, over the whole status box ({grown['height']:.0f} of {sb['height']:.0f} px)")
            pg.wait_for_timeout(800)
            ok(pg.get_attribute(btn, "data-state") == "done" and "Up to date" in pg.inner_text(btn), f"click {n}: then Up to date (green)")
            pg.wait_for_timeout(3000)
            ok(len(checks) == n and pg.get_attribute(btn, "data-state") == "idle" and "Up to date" in pg.inner_text(box) and "Last checked" in pg.inner_text("#updates"),
               f"click {n}: back to Check now, Updates redrawn (Up to date, Checked …)")
        answer["newest"] = "0.2.7-beta.3"
        pg.click(btn); pg.wait_for_timeout(1100)
        pg.locator(box).screenshot(path=os.path.join(tempfile.gettempdir(), "cs-found.png"))
        ok(pg.get_attribute(btn, "data-state") == "found" and "Update found" == " ".join(pg.inner_text(btn).split()), "a newer version: Update found (yellow)")
        pg.wait_for_timeout(3000)
        ok("Update available" in pg.inner_text(box) and pg.locator("#updates .upgradebtn").count() == 1 and pg.locator(".topbar .newver").count() == 1,
           "…then Update available, Update, and the version at the top")
        answer.clear(); answer.update({"newest": "0.2.7-beta.2", "error": "Couldn't check for updates (ConnectError: no route)"})
        main.store.set("update_check", {"checked": "2026-10-22T00:00:00+00:00", "channel": "beta", "newest": "0.2.7-beta.2"})
        pg.goto("http://127.0.0.1:8102/?menu=settings"); pg.wait_for_timeout(500)
        pg.click(btn); pg.wait_for_timeout(1100)
        ok(pg.get_attribute(btn, "data-state") == "fail" and "Couldn’t check" in pg.inner_text(btn), "a failed check: Couldn't check (yellow)")
        pg.wait_for_timeout(3000)
        ok("ConnectError" in pg.inner_text("#updates") and pg.get_attribute(btn, "data-state") == "idle", "…then the reason under Updates, and Check now again")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
