"""0.2.8-beta.45 tests (Build E, in a browser): F65's slide-out actually opens the right pop-up and moves a
Configure section there and back; I2's auto-update toggle (and frequency) reverts to what the server actually
holds when a self-submitting change is refused, instead of keeping the rejected click on screen."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8097, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8097", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    seed.demo(c, csrf, main)
    post("/ui/calview", full="1")
    main.updater.ready = True   # so Auto-update isn't disabled

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8097/?menu=settings"); pg.wait_for_timeout(500)

        # --- F65: the slide-out, not the inline list ---
        ok(pg.is_visible(".settingsnav") and not pg.is_visible("#setting-pagelogin"), "F65: ☰ Settings opens the slide-out; the pop-ups start closed")

        # Configure → Calendars: #sources moves into the shared pop-up, and back out when it closes
        before_parent = pg.eval_on_selector("#sources", "e => e.parentElement.className")
        pg.click('.settingsnav [data-configure="sources"]'); pg.wait_for_timeout(200)
        ok(pg.eval_on_selector("#configure-popup", "d => d.open") is True, "F65: Configure → Calendars opens the shared pop-up")
        ok(pg.eval_on_selector("#configureBody #sources", "e => !!e") is True, "…with the real #sources section moved into it")
        ok(not pg.is_visible(".settingsnav"), "…and the slide-out itself closed")
        pg.click("#configure-popup .dlgback"); pg.wait_for_timeout(200)
        ok(pg.eval_on_selector("#sources", "e => e.parentElement.className") == before_parent, "F65: closing it puts #sources straight back where it was")
        ok(pg.is_visible(".settingsnav"), "…and re-opens the slide-out (Back)")

        # User → Login & password: its own pop-up, the same fields as the non-fullscreen mgroup
        pg.click('.settingsnav [data-setting="pagelogin"]'); pg.wait_for_timeout(200)
        ok(pg.eval_on_selector("#setting-pagelogin", "d => d.open") is True, "F65: User → Login & password opens its own pop-up")
        ok(pg.is_visible("#setting-pagelogin input[name=user]"), "…with the real login form inside it")
        pg.click("#setting-pagelogin .dlgback"); pg.wait_for_timeout(200)

        # --- I2: a refused auto-submit change reverts to the live server state ---
        pg.click('.settingsnav [data-setting="updates"]'); pg.wait_for_timeout(200)
        was = pg.eval_on_selector('#setting-updates input[name=auto]', "i => i.checked")
        pg.route("**/settings/updates", lambda route: route.fulfill(status=400, content_type="application/json", body='{"detail":"refused"}'))
        pg.click('#setting-updates input[name=auto]'); pg.wait_for_timeout(500)
        now = pg.eval_on_selector('#setting-updates input[name=auto]', "i => i.checked")
        ok(now == was, f"I2: Auto-update reverts to the live server state after a refused save (was {was}, now {now})")
        pg.unroute("**/settings/updates")

        # ui_ux.md §5: keyboard and visible focus - every nav item and Back button is a real <button>
        # (focusable, activates on Enter/Space with no extra JS), and reduced motion drops the slide-in
        ok(pg.eval_on_selector_all(".settingsnav .navitem, .settingspop .dlgback", "els => els.every(e => e.tagName === 'BUTTON')"),
           "ui_ux.md §5: every slide-out item and pop-up Back is a real <button> (native keyboard support)")
        pg2 = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg2.emulate_media(reduced_motion="reduce")
        pg2.goto("http://127.0.0.1:8097/?menu=settings"); pg2.wait_for_timeout(300)
        ok(pg2.evaluate("getComputedStyle(document.querySelector('.settingsnav')).animationName") == "none",
           "ui_ux.md §5: the slide-out's own slide-in is off under reduced motion")
        pg2.close()

        ok(not errs, f"no console errors ({errs})")
        b.close()
    print(f"{fails} failing")
    sys.exit(1 if fails else 0)
