"""0.2.8-beta.11 tests: Google calendars say "Next push instantaneous" (F1); Settings → Updates on one line,
Update now with Sync Now's states, Google credentials with a trash that asks first (F2); the event pop-up's
layout (F3); the calendar's + and search (F4); All Rules' and Event Templates' + at the bottom right,
event icons above Close when narrow (F5, I2)."""
import os, re, sys, threading, time
from datetime import datetime, timezone
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch, PropertyMock
import uvicorn, httpx, seed
from app import main, calsync, gsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, *a, **k):
    return calsync.Download(200, body=FEED, debug={"url": url})

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8115, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8115", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    wid = seed.demo(c, csrf, main)
    with patch.object(gsync.Google, "connected", new_callable=PropertyMock, return_value=True):
        p = c.get("/?menu=settings").text
        g = main.destinations("google")[0]
        head = p[p.index(f'id="dest-{g["id"]}"'):]; head = head[:head.index('class="cfgline"')]
        ok('<p class="srcnext">Next push instantaneous</p>' in head, "F1: a Google calendar's header says Next push instantaneous")
        f = [d for d in main.destinations("feed")][0]
        fh = p[p.index(f'id="dest-{f["id"]}"'):]; fh = fh[:fh.index('class="cfgline"')]
        ok("Next push" not in fh, "…a calendar feed doesn't (the app reads it when it chooses)")
        gs = p[p.index('id="googlesync"'):]; gs = gs[:gs.index('id="updates"')]
        ok('class="ghost credtrash"' in gs and 'id="gremove"' in gs and 'data-confirm="Delete the client ID and secret?' in gs,
           "F2.3: the connected credentials end with a trash that asks first")
    p = c.get("/?menu=settings").text
    ud = p[p.index('id="updates"'):]; ud = ud[:ud.index("</form>")]
    ok(re.search(r'<div class="pair inline updrow">\s*<label class="rowlabel" for="updfreq">Check for updates</label>\s*<select id="updfreq"', ud) is not None and "autoupd" in ud,
       "F2.1: Check for updates, its menu and Auto-update on one line")
    gs = p[p.index('id="googlesync"'):]; gs = gs[:gs.index('id="updates"')]
    ok('form="fgremove" class="ghost credtrash"' in gs and 'id="fgremove"' in gs, "F2.3: the credentials before connecting end with a trash too")
    r = c.post("/google/client", data={"csrf": csrf, "action": "remove"}, follow_redirects=False)
    ok(r.status_code == 303 and not main.google.configured, "…which deletes the client ID and secret")
    # F4: search
    p = c.get("/?q=union&month=2026-10").text
    ok('8 found' in p or re.search(r'\d+ found', p) is not None, "F4: a search lists what it found")
    found = re.findall(r'<details data-uid="[^"]+" class="ev[^"]*"[^>]*>\s*<summary title="([^"]+)"', p)
    ok(found and all("Union" in t for t in found), f"…only matching events ({len(found)})")
    p2 = c.get(f"/?q=union&qsrc={wid}&qfrom=2026-10-01&qto=2026-10-31").text
    n2 = len(re.findall(r'<summary title="Union meeting"', p2))
    ok(0 < n2 < len(found) and "2026-10-01" in p2, f"…filtered by calendar and dates ({n2})")
    ok("Nothing found." in c.get("/?q=zzzzqq").text, "…and says when nothing matches")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1230, "height": 950}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8115/?month=2026-10"); pg.wait_for_timeout(500)
        # F4: + in the calendar's top right corner; search left of Time Zone
        r = pg.evaluate("""() => { const c = document.getElementById('cal').getBoundingClientRect(), h = document.querySelector('#cal .calhead').getBoundingClientRect(),
                          p = document.querySelector('.calplus').getBoundingClientRect(), s = document.getElementById('searchbtn').getBoundingClientRect(),
                          t = document.querySelector('.tzlabel').getBoundingClientRect(); return [Math.round(c.right - p.right), Math.round(p.top - h.top), s.right <= t.left, Math.abs(s.top - t.top) < 20]; }""")
        ok(17 <= r[0] <= 21 and r[1] <= 2 and r[2] and r[3], f"F4: + in the calendar's top right corner; search just left of Time Zone {r}")
        pg.click("#searchbtn"); pg.fill("#calq", "union"); pg.wait_for_timeout(1300)
        ok(pg.is_visible("#calsearch") and pg.locator("#calbody details.ev").count() > 0 and all("Union" in t for t in pg.locator("#calbody details.ev summary").all_inner_texts()),
           "F4: the search line lists matches as you type")
        ok(pg.input_value("#calq") == "union" and pg.evaluate("document.activeElement.id") == "calq", "…without losing what's typed")
        pg.click("#calqclose"); pg.wait_for_timeout(900)
        ok(pg.is_hidden("#calsearch") and pg.locator(".month .day").count() > 0, "…✕ closes it and brings the calendar back")
        pg.click(".calplus"); pg.wait_for_timeout(1200)
        ok(pg.is_visible("#eventdialog") and "date=" in (pg.get_attribute("#eventdialog iframe", "src") or ""), "F4: + adds an event")
        fr = pg.frame_locator("#eventdialog iframe")
        # F3: the pop-up's layout
        q = lambda sel: fr.locator(sel).first.bounding_box()
        cal, title, loc, tools, start, end, st, et = (q(s) for s in ("label[for=source]", "#title", "#location", ".tools", "#start_date", "#end_date", "#start_time", "#end_time"))
        ok(abs(cal["y"] + 20 - title["y"]) < 22 and title["x"] > cal["x"] + 100, "F3: Calendar | Title on one line")
        ok(abs(loc["y"] - tools["y"]) < 22 and loc["x"] > tools["x"] and loc["y"] > title["y"], "F3: Location under Title, beside the color, link and duplicate")
        ok(abs(start["y"] - end["y"]) < 2 and st["y"] > start["y"] and abs(st["x"] - start["x"]) < 2 and abs(et["x"] - end["x"]) < 2, "F3: Starts | Ends, each with its Time under it")
        tick, allday = q("#end_tz_differs"), q("#all_day")
        ok(abs(tick["y"] - allday["y"]) < 4 and tick["y"] < start["y"], "F3: 'The end is in a different time zone' beside All-day, above the times")
        hs = fr.locator("input[type=text], input[type=date], select").evaluate_all("els => els.filter(e => e.offsetParent).map(e => Math.round(e.getBoundingClientRect().height))")
        ok(hs and all(h == 34 for h in hs), f"F3: every field is 34 px ({sorted(set(hs))})")
        body = fr.locator("body").inner_text()
        ok("times in" not in body and "Last day" not in body and fr.locator("#mapbtn").count() == 1, "F3: no 'times in …', Ends (not Last day), a map for the Location")
        fr.locator("#all_day").check(); pg.wait_for_timeout(100)
        ok(fr.locator("#end_label").inner_text() == "Ends", "…Ends stays Ends for an all-day event")
        fr.locator("#location").fill("EWR Terminal C")
        ok("query=EWR%20Terminal%20C" in fr.locator("#mapbtn").get_attribute("href"), "…the map opens what's in Location")
        pr = q(".pairbtns")
        ok(pr and round(pr["width"]) == 130 and round(pr["height"]) == 34, "F3: Cancel | Save is the theme's pair")
        pg.evaluate("document.getElementById('eventdialog').close()"); pg.wait_for_timeout(300)
        # F5: + at the bottom right of All Rules and Event Templates
        for sec in ("#rules", "#templates"):
            pg.click(f"{sec} > .cfgline .cfgtoggle"); pg.wait_for_timeout(200)
            r = pg.evaluate(f"""() => {{ const s = document.querySelector('{sec}').getBoundingClientRect(), p = document.querySelector('{sec} .sfoot .plus').getBoundingClientRect();
                                return [Math.round(s.right - p.right), Math.round(s.bottom - p.bottom), document.querySelectorAll('{sec} > .shead .plus').length]; }}""")
            ok(17 <= r[0] <= 21 and r[1] <= 21 and r[2] == 0, f"F5: {sec}: + at the bottom right, none in the header {r}")
        pg.click("#templates .sfoot .plus"); pg.wait_for_timeout(200)
        ok(pg.eval_on_selector("#tpladd", "d => d.open") and pg.locator("#tpladd .tagrow").count() == 1,
           "…Event Templates' + opens its pop-up (0.2.8-beta.15: every + is a centred pop-up)")
        pg.click("#tpladd .pcancel"); pg.wait_for_timeout(200)
        if pg.eval_on_selector("#tpladd", "d => d.open"): pg.evaluate("document.getElementById('tpladd').close()")
        # I2: a narrow event: icons above Close, Close in the bottom left corner
        ev = pg.locator(".month details.ev").first
        ev.locator("summary").click(); pg.wait_for_timeout(200)
        r = ev.evaluate("""d => { const t = d.querySelector('.evtools').getBoundingClientRect(), c = d.querySelector('.evclose').getBoundingClientRect(),
                          i = [...d.querySelectorAll('.evicons > *')].map(x => x.getBoundingClientRect());
                          return [Math.round(c.left - t.left), Math.round(t.bottom - c.bottom), i.every(x => x.bottom <= c.top + 1 || Math.abs(x.top - c.top) < 6),
                                  Math.round(t.right - Math.max(...i.map(x => x.right)))]; }""")
        ok(r[0] <= 1 and r[1] <= 1 and r[2] and r[3] <= 1, f"I2: Close in the bottom left corner, the icons right-aligned above it (or beside it) {r}")
        # F2.2: Update now: Sync Now's states
        main.store.set("update_check", {"checked": datetime.now(timezone.utc).isoformat(), "channel": "stable", "newest": "99.0.0"})
        with patch.object(main.updater, "ready", True), patch.object(main.updater, "pinned", lambda: False):
            pg.goto("http://127.0.0.1:8115/?menu=settings"); pg.wait_for_timeout(400)
            ok(pg.locator("#updates .syncform button.syncnow.upgradebtn .sn").count() == 4 and "Update now" in pg.inner_text("#updates .upgradebtn"),
               "F2.2: Settings → Update now is a Sync Now (Updating…, Updated, Failed)")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
