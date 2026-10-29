"""0.1.9 tests: CCS+ login placement, Google sections, footer, copy icons, month-view clicks."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
    os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn
from app import main
from app.calsync import AuthError
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
async def fake_download(url, user, password, **kw):
    raise AuthError("rejected")
REAL = os.path.join(HERE, "data", "Demo.ics")

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8097, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2)
    import httpx
    c = httpx.Client(base_url="http://127.0.0.1:8097", auth=A, follow_redirects=False)
    asyncio_run = __import__("asyncio").run
    asyncio_run(main.run_once())
    p = c.get("/").text
    csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    ok(main.state.status == "setup" and "Setup needed" in p and "Enter your CCS+ Username and Calendar Sync password to start" in p, "no CCS+ login: 'Setup needed', not an error")
    ok(not any("CCS+" in h["msg"] for h in main.store.recent_log(5)), "no error logged for a missing login")
    body = p[p.index('id="src-ccs"'):]
    ok('id="cfg-ccs" hidden' not in p and body.index('action="/setup/ccs"') < body.index('action="/setup/interval"'), "0.2: the CCS+ source box is open, with its login")
    ok(p.count('action="/setup/ccs"') == 1 and 'id="ccsmenu"' not in p, "CCS+ login only on the dashboard (not in Settings)")
    ok("(not your CCS login):" in p, "setup note above the boxes")
    ok(re.search(r'<button class="syncnow" data-state="idle" disabled><span class="sn idle">Sync Now', p) is not None, "Sync now disabled until the login is entered")
    r = c.post("/setup/ccs", data={"csrf": csrf, "uid": "U123456", "password": "pw12345", "back": "menu"})
    ok(r.status_code == 303 and r.headers["location"] == "/#src-ccs", "saving returns to the CCS+ box")
    time.sleep(0.5); p = c.get("/").text
    ok(re.search(r'<p class="check bad"><svg[^>]*>.*?</svg> CCS\+ rejected the Username or Calendar Sync password', p) is not None, "rejection shown next to the boxes")
    main.state.last_auth_ok = True; p = c.get("/").text
    ok(re.search(r'<span class="okslot" data-state="ok">\s*<span class="okmark" title="Validated: CCS\+ sign-in"><svg[^>]*>.*?</svg>Validated</span>', p) is not None, "✓ Validated when CCS+ accepts (Save and Cancel appear when typing)")
    ok("Google Calendar API Sync" in p and 'id="fcid"' in p and 'id="scid"' not in p and "Guided setup: a client ID and secret" in p, "Autosync client form on the dashboard only, with its guide")
    feed = p[p.index('id="destinations"'):]
    mod = feed[feed.index('class="box module cfgbox dest'):]
    ok('id="dest-google"' not in feed and mod.index("Feed link") < mod.index("Add to Apple Calendar") and "Open subscribe page" not in feed,
       "Feeds (beta.17): the feed link, then Add to Google / Apple / Outlook beside it; Google Calendar sync is in Settings")
    ok("<b>Add to Google, Apple or Outlook</b>: one click opens that app" in p and "<b>Send to…</b>" in p, "the buttons are explained (Information & Instructions)")
    ok(p.count('class="copybtn"') >= 3 and ">Copy<" not in p, f"copy buttons are icons ({p.count('class=\"copybtn\"')})")
    ok('class="linkbtn reportbtn" data-kind="bug"' in p and 'data-kind="idea"' in p and 'id="reportdialog"' in p, "footer: report a problem / suggest a feature")
    ok('<h3 class="cfghead">Manual Upload</h3>' in p and 'class="filefield"' in p and "Upload Calendar.ics by hand" not in p,
       "0.2.8-beta.15: CCS+'s Manual Upload row, laid out like Import (the file field fills the line)")
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(REAL, "rb").read())})
    c.post("/feed/name", data={"csrf": csrf, "name": "United Airlines Schedule"})
    import seed
    seed.rule(c, csrf, "", [seed.text("RDO")], [{"type": "color", "color": "#d50000"}], ["ccs"])
    seed.rule(c, csrf, "", [seed.text("LSR")], [{"type": "color", "color": "#0b8043"}], ["ccs"])
    p = c.get("/?month=2026-10").text
    ok("“RDO” → Color <span class=\"swatch\" style=\"--c:#d50000\" aria-hidden=\"true\"></span> (Tomato)" in p and "“LSR” → Color <span class=\"swatch\" style=\"--c:#0b8043\" aria-hidden=\"true\"></span> (Basil)" in p and "--sw:color-mix(in srgb, #d50000" in p, "i3: rules saved, shown in Rules, the source and the key")
    ok("United Airlines Schedule" in p, "i2: name saved")
    ok('class="pin"' not in p and 'class="linkbtn evclose"' in p and 'evalarm' in p and 'data-add="/event?date=2026-10-' in p, "0.2.8: Close and the bell instead of the pin; add-on-click days")

    # Real clicks in a browser
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); ctx = b.new_context(extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="}, viewport={"width": 1100, "height": 900})
        pg = ctx.new_page(); pg.goto("http://127.0.0.1:8097/?month=2026-10"); pg.wait_for_timeout(300)
        evs = pg.locator("details.ev")
        evs.nth(3).locator("summary").click(); pg.wait_for_timeout(100)
        ok(evs.nth(3).evaluate("d => d.open"), "click an event: it opens")
        pg.locator(".legend").click(position={"x": 3, "y": 3}); pg.wait_for_timeout(100)
        ok(evs.nth(3).evaluate("d => d.open"), "F2.2.1 (0.2.8): click elsewhere: it stays open")
        evs.nth(3).locator(".evclose").click(); pg.wait_for_timeout(100)
        ok(not evs.nth(3).evaluate("d => d.open"), "…until its Close")
        pg.locator(".day[data-add]").nth(10).dispatch_event("click"); pg.wait_for_timeout(800)     # (on the day itself, not an event: every demo day has events)
        ok(pg.locator("#eventdialog[open]").count() == 1 and "/event?date=" in pg.locator("#eventdialog iframe").get_attribute("src"),
           "6.3 / F1.3: click an empty day: Add event in a pop-up")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        pg.goto("http://127.0.0.1:8097/"); pg.wait_for_timeout(300)
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        pg.evaluate("var b = document.querySelector('.box.dest .copybtn').closest('.box'); if (b.querySelector('.cfgbody').hidden) b.querySelector('.cfgtoggle').click()")   # 0.2.7: under Configure
        pg.evaluate("document.querySelector('.box.dest .copybtn').scrollIntoView()")
        btn = pg.locator(".box.dest .copybtn:visible").first
        btn.click(); pg.wait_for_timeout(200)
        ok("Copied" in btn.inner_text(), "copy icon shows 'Copied'")
        pg.wait_for_timeout(2000)
        ok(btn.locator("svg").count() == 1, "…then the icon again")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
