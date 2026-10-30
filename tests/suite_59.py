"""0.2.8-beta.24 tests: Add event's Default color follows the Calendar chosen, unless a color is picked (I1); updates
started elsewhere (Auto-update, at the frequency chosen in Settings, or another tab) shown on every open page, which
refreshes 15 seconds after Restarting… (F1); Remove a feed's question with its note on the line under it (F2); the event
pop-up's All-day Event on the end's Time label line and Different end time zone beside Time zone (F5); sections and
modules told apart by their border colors and tints (F7)."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "IMAGE_TAG", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main, calsync
from app.updates import channel
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", **k):
    return calsync.Download(200, body=FEED, debug={"url": url})
PORT = 8159

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(main, "updater_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    seed.demo(c, csrf, main)
    sids = main.source_ids()

    # --- F1: an update asked of the updater is seen by every open page, for 15 minutes, until the restart --------------
    ok(c.get("/api/status").json().get("updating") == "", "F1: /api/status says no update is running")
    main.mark_updating("9.9.9")
    ok(c.get("/api/status").json().get("updating") == "9.9.9", "F1: …then the version an update is going to")
    main.store.set("update_running", {**main.store.get("update_running"), "at": (datetime.now(timezone.utc) - timedelta(minutes=16)).isoformat()})
    ok(main.updating_to() == "", "F1: …not after 15 minutes (an update that never restarted)")
    main.store.set("update_running", {"from": "0.0.1", "to": "9.9.9", "at": datetime.now(timezone.utc).isoformat()})
    ok(main.updating_to() == "", "F1: …nor once the new version runs")
    main.updates.set_frequency("hourly")
    main.updates.store.set("update_check", {"checked": (datetime.now(timezone.utc) - timedelta(minutes=50)).isoformat(), "channel": channel()})
    nxt = main.updates.next_check(datetime.now(timezone.utc))
    ok(nxt and timedelta(minutes=9) < nxt - datetime.now(timezone.utc) < timedelta(minutes=11), "F1: the next automatic check is due at the frequency chosen (hourly: 10 min after 50)")
    src = open(os.path.join(os.path.dirname(HERE), "app", "main.py")).read()
    ok("await asyncio.sleep(min(3600, max(60, wait)))" in src, "F1: the update loop wakes when the next check is due")

    # --- F2: Remove a feed: the note on the line under the question -------------------------------------------------
    page = c.get("/").text
    ok(re.search(r'data-confirm="Remove the feed [^"]*\?&#10;Its links and subscribe page stop working\.">', page) is not None,
       "F2: Remove the feed …? with \"Its links and subscribe page stop working.\" on the next line")

    # --- F5: the event pop-up's markup ---------------------------------------------------------------------------------
    p = c.get("/event?date=2026-10-21&month=2026-10&embed=1").text
    ok('grid2 ticks' not in p and "The end is in a different time zone" not in p, "F5: the All-day line is gone")
    et = p[p.index('class="endtime"'):p.index('id="end_time"')]
    ok(et.index('for="end_time"') < et.index('id="all_day"') and "All-day Event" in et, "F5: All-day Event on the end's Time label line, after Time")
    ok('class="timed tzdiff"' in p and "Different end time zone" in p and p.index('id="start_tz"') < p.index('id="end_tz_differs"') < p.index('name="end_tz"'),
       "F5: Different end time zone after Time zone, End time zone under it")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []
        pg.on("pageerror", lambda x: errs.append(str(x))); pg.on("console", lambda m: m.type == "error" and "Failed to load resource" not in m.text and errs.append(m.text))

        # --- I1 --------------------------------------------------------------------------------------------------------
        pg.goto(f"http://127.0.0.1:{PORT}/event?date=2026-10-21&month=2026-10&embed=1"); pg.wait_for_timeout(400)
        shown = lambda: pg.evaluate("() => getComputedStyle(document.getElementById('colorshow')).getPropertyValue('--c').trim()")
        other = [s for s in sids if s != sids[0] and main.calendar_color(s)][0]
        pg.select_option("select#source", other); pg.wait_for_timeout(100)
        ok(shown().lower() == main.calendar_color(other).lower(), f"I1: Default color shows the calendar chosen's color ({shown()})")
        auto = pg.evaluate("() => document.querySelector('#colorpick input[value=\"\"]').dataset.c")
        ok(auto.lower() == main.calendar_color(other).lower(), "I1: …and so does the palette's Default color")
        pg.click("#colorpick summary"); pg.locator("#colorpick .palette label").nth(3).click(); pg.wait_for_timeout(100)
        picked = shown()
        pg.select_option("select#source", sids[0]); pg.wait_for_timeout(100)
        ok(shown() == picked and picked.lower() != (main.calendar_color(sids[0]) or "").lower(), "I1: a color picked stays when the calendar changes")

        # --- F5: where they sit, and All-day stays put as the Time fields hide ----------------------------------------
        bb = lambda sel: pg.locator(sel).bounding_box()
        ad, tl, ef = bb("label.allday"), bb("label[for=end_time]"), bb("#end_time")
        ok(abs((ad["y"] + ad["height"] / 2) - (tl["y"] + tl["height"] / 2)) <= 3 and ad["x"] > tl["x"] + tl["width"] and ad["y"] + ad["height"] <= ef["y"] + 1,
           "F5: All-day Event on the end's Time label line, right of Time *")
        zd, sz = bb(".tzdiff label"), bb("#start_tz")
        ok(zd["x"] >= sz["x"] + sz["width"] and abs((zd["y"] + zd["height"] / 2) - (sz["y"] + sz["height"] / 2)) <= 4, "F5: Different end time zone beside Time zone's field")
        pg.check("#end_tz_differs"); pg.wait_for_timeout(100)
        ez = bb(".endzone")
        ok(ez and ez["y"] >= zd["y"] + zd["height"] - 1 and abs(ez["x"] - ef["x"]) <= 1, "F5: ticked, End time zone shows under it, in the end's column")
        pg.check("#all_day"); pg.wait_for_timeout(100)
        ad2 = bb("label.allday")
        ok(abs(ad2["x"] - ad["x"]) <= 1 and abs(ad2["y"] - ad["y"]) <= 1 and not pg.is_visible("#end_time") and not pg.is_visible("#start_time")
           and not pg.is_visible(".tzdiff"), "F5: ticked, All-day Event stays in its spot while the Time fields hide")

        # --- F7: sections and modules, light and dark --------------------------------------------------------------
        for scheme in ("light", "dark"):
            pg.emulate_media(color_scheme=scheme)
            pg.goto(f"http://127.0.0.1:{PORT}/?month=2026-10"); pg.wait_for_timeout(500)
            r = pg.evaluate("""() => {
              const cs = e => getComputedStyle(e);
              const line = cs(document.body).getPropertyValue('--line').trim();
              const secs = ['#cal', '#sources', '#destinations', '#rules', '#templates', '#activity'].map(s => {
                const x = cs(document.querySelector(s));
                return [x.borderTopColor, x.borderTopWidth, x.boxShadow.includes('inset'), x.backgroundColor]; });
              const card = cs(document.querySelector('#sources')).getPropertyValue('--card').trim();
              const mods = [...document.querySelectorAll('.box.module.src, .box.module.dest')].map(m => {
                const x = cs(m); return [x.getPropertyValue('--mc').trim(), x.borderTopColor, x.backgroundImage]; });
              return {secs, mods, line, card}; }""")
            colors = [s[0] for s in r["secs"]]
            ok(len(set(colors)) == 6 and all(s[1] == "1px" and s[2] for s in r["secs"]), f"F7 ({scheme}): six sections, six border colors, 2 px (1 px and an inset line) {colors}")
            ok(len({s[3] for s in r["secs"]}) == 1, f"F7 ({scheme}): every section on the same --card background")
            ok(r["mods"] and all(m[0] and "linear-gradient" in m[2] and m[1] not in colors for m in r["mods"]),
               f"F7 ({scheme}): each module bordered in its own color, a tinted header over a tinted body")
        pg.emulate_media(color_scheme="light")
        sid = sids[1]
        pg.evaluate(f"() => {{ const m = document.getElementById('src-{sid}'); m.classList.add('cfgopen'); }}")
        pg.click(f"#src-{sid} .colorpick"); pg.wait_for_timeout(100)
        pick = pg.locator(f"#src-{sid} .palpop .pal").nth(4)
        want = pick.get_attribute("data-c"); pick.click(); pg.wait_for_timeout(100)
        got = pg.evaluate(f"() => document.getElementById('src-{sid}').style.getPropertyValue('--mc')")
        ok(got == want, f"F7: a module's border and tints follow a color picked ({got})")

        # --- F1: an update started elsewhere: the page follows it and refreshes 15 s after Restarting… ---------------
        pg.goto(f"http://127.0.0.1:{PORT}/?month=2026-10"); pg.wait_for_timeout(400)
        main.updater.ready = True
        pg.reload(); pg.wait_for_timeout(400)
        ok(pg.locator(".topbar[data-canupdate]").count() == 1, "F1: with the updater, the page watches for updates")
        state = {"n": 0}
        def status(route):
            state["n"] += 1
            if state["mode"] == "down": route.abort()
            else: route.fulfill(json={"version": state["mode"], "updating": "9.9.9"})
        state["mode"] = main.__version__
        pg.route("**/api/status", status)
        pg.evaluate("() => { RESTART_WAIT = 4000; updateNow(true); }"); pg.wait_for_timeout(600)
        ok(pg.locator(".updslot .updtext").inner_text() == "Downloading…", "F1: …an update started elsewhere shows Downloading… in the top bar")
        state["mode"] = "down"; pg.wait_for_timeout(2600)
        ok(pg.locator(".updslot .updtext").inner_text() == "Restarting…", "F1: …then Restarting…")
        t0 = time.time(); pg.evaluate("() => { window.__notReloaded = 1; }")
        state["mode"] = "9.9.9"; pg.wait_for_timeout(1500)
        ok(pg.evaluate("() => window.__notReloaded") == 1, "F1: …and doesn't refresh as soon as it answers")
        pg.wait_for_function("() => !window.__notReloaded", timeout=10000)
        ok(time.time() - t0 >= 1.2, "F1: …but after the wait following Restarting… (15 s; 4 s here)")
        pg.unroute("**/api/status")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
