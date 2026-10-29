"""0.2.8-beta.3 (second list): All Rules / Event Templates / Activities as module-like sections (count
boxes, Expand lines, no opening from the header), How rules work in the rule dialog, rule badges in their
calendars' colors, color changes that stick (and update the keys), Settings saved in place, Auto-update."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
from unittest.mock import patch
import asyncio, uvicorn, httpx, seed
from app import main, calsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    return calsync.Download(200, body=FEED, debug={"url": url})

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8094, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8094", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    wid = seed.demo(c, csrf, main)
    L = main.source_ids()[0]
    p = c.get("/").text
    n = len(main.all_rules())
    ok(re.search(r'<div class="statusbox countbox good" id="rulecount">.*?%d Rules' % n, p, re.S) is not None
       and re.search(r'<div class="statusbox countbox good" id="tplcount">.*?2 Templates', p, re.S) is not None, f"F: All Rules and Event Templates: a green box with {n} Rules / 2 Templates")
    ok(p.count('<span class="expandword"><span class="long">Expand for Details</span>') == 3, "…and an Expand for Details line, like Activities and Logs")
    hd = p[p.index('id="rules"'):p.index('id="rules-body"')]
    ok('class="toggle"' not in hd and 'class="peek"' not in hd and re.search(r'All Rules<span class="helpdot', hd) is not None, "no ▸ toggle or grey count; (?) right after the title")
    ok('class="guide rulesguide"' not in p.split('id="rules-body"')[1].split("</section>")[0] and p.index('class="eactions rdfoot"') < p.index('class="guide rulesguide"', p.index('id="ruledialog"')),
       "How rules work: not under All Rules; at the bottom of the rule dialog")
    # rule badges in their calendars' colors
    ok('data-cal="all"' in p and 'data-cal="one" style="--c1:#1d4ed8"' in p and 'data-cal="none"' not in p, "rule badges: white for All calendars, the calendar's color for one")
    seed.rule(c, csrf, "Two", [seed.text("XYZ")], [{"type": "color", "color": "#d50000"}], ["ccs", wid])
    p = c.get("/").text
    ok("repeating-linear-gradient(135deg, color-mix(in srgb, #1d4ed8 28%, var(--card)) 0px 8px, color-mix(in srgb, #8e24aa 28%, var(--card)) 8px 16px)" in p,
       "…stripes of each calendar's color for several")
    # a conflict turns the box yellow
    seed.rule(c, csrf, "Two again", [seed.text("XYZ")], [{"type": "color", "color": "#d50000"}], ["ccs", wid])
    p = c.get("/").text
    ok(re.search(r'<div class="statusbox countbox run" id="rulecount" title="\d to check">', p) is not None, "…the pressed look (waiting on you, beta.14) with “n to check” while a rule needs checking")
    # Auto-update
    ok('name="auto" value="1" disabled' in p, "Auto-update: off and greyed without the updater")
    main.updater.ready = True
    p = c.get("/?menu=settings").text
    ud = p[p.index('id="updates"'):]; ud = ud[:ud.index("</form>")]
    ok('name="auto" value="1" onchange' in ud and ud.index("Check now") < ud.index('class="autoupd"'), "…a tick box under the header (Check now in its status box, beta.5) with the updater")
    post("/settings/updates", frequency="weekly", autoform="1", auto="1")
    ok(main.auto_update() and "Auto-update on" in c.get("/").text, "ticking it turns Auto-update on (logged)")
    post("/settings/updates", frequency="weekly", autoform="1")
    ok(not main.auto_update(), "…unticking turns it off")
    post("/settings/updates", frequency="weekly", autoform="1", auto="1")
    calls = []
    async def fake_update(): calls.append(1)
    main.store.set("update_check", {"checked": "2026-10-25T00:00:00+00:00", "channel": main.release_channel(), "newest": "9.9.9"})
    with patch.object(main.updater, "update", fake_update), patch.object(main.updater, "pinned", lambda: False):
        asyncio.run(main.auto_install()); asyncio.run(main.auto_install())
    ok(calls == [1] and "Auto-update: updating to CalendarStream 9.9.9" in c.get("/").text, "a newer version is installed by itself, once")
    main.store.delete("update_check"); main.updater.ready = False

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 1000}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        loads = []; pg.on("load", lambda: loads.append(1))
        pg.goto("http://127.0.0.1:8094/?month=2026-10"); pg.wait_for_timeout(500); loads.clear()
        # header clicks don't open these sections; their Expand line does
        for sec in ("rules", "templates", "activity"):
            pg.locator(f"#{sec} > .shead .bigtitle").click(); pg.wait_for_timeout(150)
            shut = pg.locator(f"#{sec}-body[hidden]").count() == 1
            pg.click(f"#{sec} > .cfgline .cfgtoggle"); pg.wait_for_timeout(150)
            ok(shut and pg.locator(f"#{sec}-body[hidden]").count() == 0, f"{sec}: the header doesn't open it; Expand does")
            pg.click(f"#{sec} > .cfgline .cfgtoggle"); pg.wait_for_timeout(150)
        lt, sb = pg.locator("#activity .peek.latest").bounding_box(), pg.locator("#activity > .shead .statusbox").bounding_box()
        right = pg.evaluate("(() => { const e = document.querySelector('#activity .peek.latest'); return getComputedStyle(e).textAlign; })()")
        ok(right == "right" and sb["x"] - (lt["x"] + lt["width"]) < 16, "Activities: Latest on the right, by Healthy")
        # I4: a second color change sticks; I3: the keys follow
        box = f"#src-{wid}"
        pg.click(f"{box} .cfgtoggle"); pg.wait_for_timeout(150)
        for color in ("#0b8043", "#f4511e"):
            pg.click(f"{box} .colorpick"); pg.click(f'{box} .palpop .pal[data-c="{color}"]')   # the color box (0.2.8-beta.15)
            pg.click(f"{box} .pairbtns .psave"); pg.wait_for_timeout(1500)
            ok(main.calendar_color(wid) == color, f"I4: color change to {color} saved")
        ok("#f4511e" in pg.inner_html(".legend") and "#f4511e" in pg.inner_html("#destinations .srcpicks") and not loads,
           "I3: the calendar key, the feeds' calendar colors and the rule badges follow, in place")
        # Settings saved in place
        pg.click("#menubtn"); pg.wait_for_timeout(150)
        pg.fill("#publicurl", "https://cal2.example.com"); pg.click("#public .slotsave"); pg.wait_for_timeout(1500)
        ok(main.public_url() == "https://cal2.example.com" and not loads and pg.is_visible("#menu") and "cal2.example.com" in pg.inner_html("#destinations"),
           "Settings: Public address saved in place (menu still open, no reload; the feeds' links follow)")
        pg.select_option("#updfreq", "monthly"); pg.wait_for_timeout(1200)
        ok(main.updates.frequency() == "monthly" and not loads and pg.is_visible("#menu"), f"…and Check for updates ({main.updates.frequency()} {loads} {pg.is_visible('#menu')} {errs})")
        u, a = pg.locator("#updfreq").bounding_box(), pg.locator("#updates button.checknow").bounding_box()
        m = pg.locator("#menu .mgroup#updates").bounding_box()
        sb = pg.locator("#updates .statusbox").bounding_box()
        ok(abs(u["height"] - 34) < 1 and abs(sb["height"] - 50) < 1 and abs(sb["width"] - 132) < 1 and a["x"] + a["width"] <= m["x"] + m["width"] - 10,
           "Settings → Updates: a module header (132 × 50 status box with Check now), a 34 px menu, all inside")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
