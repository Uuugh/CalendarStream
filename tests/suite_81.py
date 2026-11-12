"""Build D: I22 combined normal Settings, F65 independent Full-mode popups and accessibility.
Depends on: app routes and tests/seed.py; appearance_settings_test.py is independently runnable.
Used by: tests/run.sh. Reads/writes: dedicated demo test database and browser only.
Dart note: UI/controller acceptance contracts for the settings navigation.
"""
import os, re, sys, asyncio, threading, time, subprocess
import uvicorn
from playwright.sync_api import sync_playwright
from unittest.mock import patch
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"): del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
from fastapi.testclient import TestClient
from app import main
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main.updates, "check", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    import seed; seed.demo(c, csrf, main)

    result = subprocess.run([sys.executable, os.path.join(HERE, "appearance_settings_test.py")])
    ok(result.returncode == 0, "Appearance: standalone validation tests")
    before = (main.store.get("public_url"), main.store.get("public_urls_extra"))
    values = dict(user="t", password="", current="", confirm="", frequency="monthly", intensity="125", duration="75", grips="right")
    ok(post("/settings/user", **values).status_code == 303, "I22: one Save accepts all user preferences")
    ok(main.updates.frequency() == "monthly" and main.store.get("ui_anim") == {"i": 125, "d": 75}
       and main.store.get("ui_grips") == "right", "I22: Updates and Theme saved together")
    ok(before == (main.store.get("public_url"), main.store.get("public_urls_extra")), "I22: user Save leaves Domains intact")
    old = main.store.get("ui_anim")
    ok(post("/settings/user", **{**values, "frequency": "never", "duration": "500"}).status_code == 400
       and main.updates.frequency() == "monthly" and main.store.get("ui_anim") == old,
       "I22: invalid Theme leaves all preferences intact")
    ok(post("/settings/user", **{**values, "user": "new", "current": "wrong", "frequency": "never"}).status_code == 400
       and main.updates.frequency() == "monthly", "I22: refused login leaves preference edits unapplied")
    ok(post("/settings/user", scope="updates", frequency="weekly").status_code == 303
       and main.store.get("ui_anim") == old, "F65: Updates popup only saves Updates")
    ok(post("/settings/user", scope="look", intensity="100", duration="100", grips="left").status_code == 303
       and main.updates.frequency() == "weekly", "F65: Theme popup only saves Theme")

    server = uvicorn.Server(uvicorn.Config(main.app, host="127.0.0.1", port=8181, lifespan="off", log_level="error"))
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(100):
        if server.started: break
        time.sleep(.05)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width in (1230, 390):
            for palette in ("light", "dark"):
                tag = f"{width}/{palette}"
                post("/ui/calview", full="0")
                post("/settings/user", scope="updates", frequency="weekly")
                post("/settings/user", scope="look", intensity="100", duration="100", grips="left")
                pg = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=palette,
                                      reduced_motion="reduce", extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
                errors = []
                pg.on("pageerror", lambda e: errors.append(str(e)))
                pg.goto("http://127.0.0.1:8181/?menu=settings"); pg.wait_for_load_state("networkidle")
                ok(pg.locator('#pagelogin .pairbtns').count() == 1 and pg.locator('#adminform hr').count() == 2,
                   f"I22 [{tag}]: one Save pair, two dividers")
                ok(pg.locator('#adminform .login-status .pairbtns').count() == 0 and
                   pg.locator('#adminform .pair > .login-status').count() == 1,
                   f"I22 [{tag}]: Signed in/Sign out belongs beside login fields")
                pg.select_option('#updfreq', 'never')
                pg.locator('#animI').evaluate("e => { e.value = '150'; e.dispatchEvent(new Event('input', {bubbles:true})); }")
                ok(main.updates.frequency() == 'weekly', f"I22 [{tag}]: Updates waits for Save")
                pg.click('#updates .checknow'); pg.wait_for_timeout(4200)
                ok(pg.input_value('#updfreq') == 'never' and pg.input_value('#animI') == '150',
                   f"I22 [{tag}]: Check now preserves staged user preferences")
                pg.click('#adminform .pcancel'); pg.wait_for_timeout(3200)
                ok(pg.input_value('#updfreq') == 'weekly' and pg.input_value('#animI') == '100',
                   f"I22 [{tag}]: Cancel resets every subsection and animation preview")
                pg.select_option('#updfreq', 'monthly')
                pg.locator('#animI').evaluate("e => { e.value = '125'; e.dispatchEvent(new Event('input', {bubbles:true})); }")
                with pg.expect_response(lambda r: '/settings/user' in r.url) as saved:
                    pg.click('#adminform .psave')
                ok(saved.value.status in (200, 303) and main.updates.frequency() == 'monthly' and main.store.get('ui_anim')['i'] == 125,
                   f"I22 [{tag}]: one browser Save applies both subsections")
                pg.wait_for_timeout(1400); pg.wait_for_load_state('networkidle')
                if pg.locator('#menu').is_visible(): pg.click('#menubtn')
                pg.click('#fullbtn')
                pg.wait_for_function("document.querySelector('#settingswrap').dataset.full === '1'")
                pg.click('#menubtn')
                ok(pg.locator('[data-configure]').count() == 6 and pg.locator('[data-setting]').count() == 5,
                   f"F65 [{tag}]: Configure, User and Site Admin items")
                ok(pg.locator('.sections').is_hidden(), f"F65 [{tag}]: page modules hidden outside Configure")
                for _ in range(25):
                    pg.keyboard.press('Tab')
                    ok(pg.evaluate("document.activeElement.closest('#menu') !== null && getComputedStyle(document.activeElement).visibility !== 'hidden'"),
                       f"F65 [{tag}]: keyboard navigation stays on visible slide-out controls")
                animation = pg.locator('#menu').evaluate("e => getComputedStyle(e).animationName")
                ok(animation == 'none', f"F65 [{tag}]: reduced motion")
                for key in ('pagelogin', 'updates', 'look', 'domains', 'googlesync'):
                    link = pg.locator(f'[data-setting="{key}"]')
                    link.focus(); pg.keyboard.press('Enter')
                    dialog = pg.locator(f'#setting-{key}')
                    ok(dialog.is_visible(), f"F65 [{tag}]: {key} opens its own popup")
                    if key != 'googlesync':
                        size = dialog.locator('.pairbtns').bounding_box()
                        ok(round(size['width']) == 130 and round(size['height']) == 34,
                           f"F65 [{tag}]: standard Cancel | Save dimensions in {key}")
                    pg.keyboard.press('Escape'); pg.wait_for_timeout(800)
                    ok(not dialog.is_visible() and link.evaluate('e => e === document.activeElement'),
                       f"F65 [{tag}]: Escape restores focus from {key}")
                for key in ('calendar', 'sources', 'destinations', 'rules', 'templates', 'activity'):
                    pg.click(f'[data-configure="{key}"]')
                    ok(pg.locator('#configure-popup').is_visible() and pg.locator('#configure-popup .configure-content > *').count() == 1,
                       f"F65 [{tag}]: Configure opens {key}")
                    pg.keyboard.press('Escape')
                pg.keyboard.press('Escape')
                pg.click('#fullbtn')
                pg.wait_for_function("document.querySelector('#settingswrap').dataset.full === '0'")
                ok(pg.locator('.sections').is_visible() and pg.locator('#sources').count() == 1,
                   f"F65 [{tag}]: leaving Full restores original modules without duplicates")
                ok(pg.evaluate('document.documentElement.scrollWidth <= innerWidth'), f"F65 [{tag}]: no horizontal overflow")
                ok(not errors, f"F65 [{tag}]: no script errors {errors}")
                pg.close()
        browser.close()
    response = post("/settings/user", scope="login", user="builder", current="password1",
                    password="BuilderTest9!", confirm="BuilderTest9!")
    ok(response.status_code == 200 and response.json().get("redirect") == "/login" and
       main.logins.check_page_login("builder", "BuilderTest9!") and not main.logins.check_page_login("t", "password1"),
       "I22/F65: changed login ends the old credentials and redirects to sign-in")
    server.should_exit = True

print(("ALL PASS" if not fails else "%d FAILURES" % fails)); sys.exit(1 if fails else 0)
