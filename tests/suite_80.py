"""Build D: persisted Settings order (F47/I45), with isolated normalization and HTTP contracts.
Depends on: app/services/page_settings.py and app routes, tests/seed.py.
Used by: tests/run.sh. Reads/writes: dedicated demo test database only.
Dart note: preference service and controller contracts.
"""
import os, re, sys, asyncio, threading, time
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

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    import seed; seed.demo(c, csrf, main)

    from app.services.page_settings import settings_order, SETTINGS_MODULES
    from types import SimpleNamespace
    fake = lambda saved: SimpleNamespace(get=lambda key: saved)
    ok(settings_order(store=fake(None)) == list(SETTINGS_MODULES), "Settings: default order")
    ok(settings_order(store=fake(["look", "look", "retired", {}, "pagelogin"])) ==
       ["look", "pagelogin", "updates", "domains", "googlesync"], "Settings: deduplicate saved order and append new modules")
    ok(settings_order(store=fake("look")) == list(SETTINGS_MODULES), "Settings: malformed saved state falls back")
    ok(settings_order(store=fake(["look"]), modules=(*SETTINGS_MODULES, "future"))[-1] == "future",
       "Settings: newly installed modules appear automatically")
    ok(post("/settings/move", id="look", before="pagelogin").status_code == 200,
       "Settings: move above Administrator")
    ok(main.store.get("ui_settings_order") == ["look", "pagelogin", "updates", "domains", "googlesync"],
       "Settings: chosen order persisted")
    p = page("?menu=settings")
    user_part = p.split('class="sortable settings-list user-settings"', 1)[1].split('class="settings-foot"', 1)[0]
    ok(re.findall(r'<div class="settingrow" data-id="([^"]+)"', user_part) == ["look", "pagelogin", "updates"],
       "Settings: rendered order matches stored order")
    ok(p.count('data-kind="setting"') >= 5, "Settings: modules expose existing reorder controls")
    ok(post("/settings/move", id="gone", before="pagelogin").status_code == 400,
       "Settings: nonexistent module rejected")
    old = main.store.get("ui_settings_order")
    ok(c.post("/settings/move", data={"csrf": "bad", "id": "look", "after": "updates"}).status_code == 400
       and main.store.get("ui_settings_order") == old, "Settings: CSRF refusal leaves order intact")
    ok(post("/settings/move", id="look", after="updates").status_code == 200,
       "Settings: arrow move below Updates")
    main.store.delete("ui_settings_order")
    server = uvicorn.Server(uvicorn.Config(main.app, host="127.0.0.1", port=8180, lifespan="off", log_level="error"))
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(100):
        if server.started: break
        time.sleep(.05)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width, palette in ((1230, "light"), (390, "dark")):
            pg = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=palette,
                                  extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
            pg.goto("http://127.0.0.1:8180/?menu=settings")
            pg.wait_for_load_state("networkidle")
            arrow = pg.locator('.settingrow[data-id="updates"] > .handle [data-dir="up"]')
            arrow.focus()
            with pg.expect_response(lambda r: "/settings/move" in r.url) as answer:
                pg.keyboard.press("Enter")
            ok(answer.value.ok, f"Settings: keyboard reorder at {width}px")
            ok(pg.locator('.user-settings > hr').count() == 2 and
               pg.locator('.user-settings > .settingrow + .settingrow').count() == 0,
               f"Settings: dividers remain between reordered user subsections at {width}px")
            pg.reload(); pg.wait_for_load_state("networkidle")
            if not pg.locator("#menu").is_visible(): pg.click("#menubtn")
            ok(pg.locator('.user-settings > .settingrow').first.get_attribute('data-id') == 'updates',
               f"Settings: browser reload retains order at {width}px")
            pg.locator('.user-settings > .settingrow[data-id="pagelogin"] > .handle .hgrip').drag_to(
                pg.locator('.settingrow[data-id="updates"] .mhead, .settingrow[data-id="updates"] .srcname').first)
            pg.wait_for_timeout(300)
            pg.reload(); pg.wait_for_load_state("networkidle")
            if not pg.locator("#menu").is_visible(): pg.click("#menubtn")
            ok(pg.locator('.user-settings > .settingrow').first.get_attribute('data-id') == 'pagelogin',
               f"Settings: drag reorder survives reload at {width}px")
            original = pg.locator('.user-settings > .settingrow').evaluate_all('(rows) => rows.map(r => r.dataset.id)')
            pg.fill('#luser', 'draft')
            pg.route('**/settings/move', lambda route: route.fulfill(status=503, body='{}', content_type='application/json'))
            pg.locator('.user-settings .settingrow[data-id="updates"] > .handle [data-dir="up"]').click()
            pg.wait_for_timeout(200)
            ok(pg.locator('.user-settings > .settingrow').evaluate_all('(rows) => rows.map(r => r.dataset.id)') == original
               and pg.input_value('#luser') == 'draft', f"Settings: failed reorder preserves order and typed fields at {width}px")
            pg.locator('#askdialog .askchoices button').click()
            pg.unroute('**/settings/move')
            pg.fill('#luser', 't')
            for _ in range(2):
                with pg.expect_response(lambda r: '/settings/move' in r.url):
                    pg.locator('.settings-modules > .settingrow[data-id="googlesync"] > .handle [data-dir="up"]').click()
            pg.reload(); pg.wait_for_load_state('networkidle')
            if not pg.locator('#menu').is_visible(): pg.click('#menubtn')
            ok(pg.locator('.settings-modules > .settingrow').first.get_attribute('data-id') == 'googlesync',
               f"Settings: outer modules can move ahead of Administrator at {width}px")
            pg.close()
            main.store.delete("ui_settings_order")
        browser.close()
    server.should_exit = True


print(("ALL PASS" if not fails else "%d FAILURES" % fails)); sys.exit(1 if fails else 0)
