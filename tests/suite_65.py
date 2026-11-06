"""0.2.8-beta.31 tests (build 7: the Calendar carryover): the event page's rows (I19), its icons (I17), Rule in Add event (I18),
Full page fits the window and its button (I14, F34, F35), the key's last item switched back on (I15), the calendar's top line (I16), the hour
height handle (I20), an added event deleted here is gone (I3), Print's orientation (I11), the Administrator row (I22) and the grips' side (F36.1)."""
import os, re, sys, io, base64
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
read = lambda *p: open(os.path.join(REPO, *p)).read()

from pypdf import PdfReader
from playwright.sync_api import sync_playwright
import threading, time, httpx, uvicorn
PORT = 8165
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "updater_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=A, timeout=60)
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    import seed; seed.demo(c, csrf, main)

    # --- I19, I18: the event page ---
    e = c.get("/event?date=2026-10-14").text
    i = lambda s: e.index(s)
    ok(i('id="start_date"') < i('id="all_day"') < i('id="start_time"') < i('id="end_tz_differs"') < i('id="end_time"') < i('id="start_tz"') < i('name="end_tz"'),
       "I19: All-day Event is on the Ends line and Different end time zone on the end's Time line, both a line higher")
    ok('class="enddate"' in e and re.search(r'class="enddate">.*?id="end_label".*?id="all_day"', e, re.S), "I19: All-day Event follows Ends in its label line")
    ok(not re.search(r'data-kind="rule"[^>]*disabled', e), "I18: in Add event, Rule is not disabled")

    # --- I3: an event added here and deleted here is gone from the calendar at once ---
    post("/event/save", title="Gone at once", start_date="2026-10-14", start_time="9:00am", end_date="2026-10-14", end_time="10:00am",
         start_tz="America/New_York", month="2026-10")
    mine = next(x for x in main.store.load_events() if x.title == "Gone at once")
    ok(mine.uid in page("?date=2026-10-14"), "I3: the added event shows")
    post("/event/delete", uid=mine.uid, month="2026-10")
    ok(mine.uid not in page("?date=2026-10-14"), "I3: deleted here, an event added here is not drawn (not struck through)")
    ok(any(x.uid == mine.uid and x.deleted for x in main.store.load_events()), "I3: it is still there for History › Undo")
    src = next(x for x in main.store.load_events("ccs") if x.origin == "united" and not x.hidden)
    post("/event/delete", uid=src.uid, month="2026-10")
    ok(src.title in page(f"?date={src.start[:10]}"), "I3: a source's own event deleted here stays struck through, with its Restore")

    # --- I15: the last key item switched on again is saved ---
    post("/ui/calview", full="1"); post("/ui/calview", hide="src:ccs")
    ok(main.store.get("ui_calview").get("hide") == ["src:ccs"], "I15: a hidden calendar is saved")
    ok(post("/ui/calview", hide="-").status_code in (200, 204, 303) and main.store.get("ui_calview").get("hide") == [], "I15: switching the last one on again empties the list")

    # --- F34, F35, I14: Full page (its button in the title bar, left of ☰; fits the window) ---
    p = page()
    top = p[p.index('<header class="topbar"'):p.index("</header>")]
    ok('id="fullbtn"' in top and top.index('id="fullbtn"') < top.index('id="menubtn"'), "F34: Full page is in the title bar, left of ☰")
    ok('id="fullbtn"' not in p[p.index('id="cal"'):p.index('<footer')], "F34: and no longer in the calendar's top line")
    ok('#mi-filter_none' in top and 'aria-pressed="true"' in top, "F35: in Full page its icon is Windows' restore down (two squares)")
    post("/ui/calview", full="0")
    ok('#mi-fullscreen' in page()[:page().index("</header>")], "F35: otherwise it is the Full page icon")

    # --- I20: the hour height handle; I16: tighter top line ---
    ok(post("/ui/calview", hour="64").status_code in (200, 204, 303) and main.store.get("ui_calview").get("hour") == 64, "I20: the hour height is saved")
    ok(post("/ui/calview", hour="500").status_code == 400 and post("/ui/calview", hour="10").status_code == 400, "I20: and kept between 20 and 120 px")
    post("/ui/view", view="week")
    w = page("?date=2026-10-14")
    ok('id="hourgrip"' in w and "--hhu:64px" in w and 'role="slider"' in w, "I20: Week has the handle left of the times, at the saved height")
    post("/ui/view", view="month")
    css = read("app", "styles", "19-calendar.css")
    ok("gap:5px; flex:0 0 auto" in css.replace("\n", " ") and ".calhead { display:flex; align-items:center; gap:8px" in css, "I16: the top line's gaps are tighter")

    # --- I11: Print's orientation ---
    for orient, want in (("", "land"), ("auto", "land"), ("port", "port"), ("land", "land")):
        h = c.get(f"/print?view=month&start=2026-10-01&end=2026-10-31&orient={orient}").text
        ok(f'data-paper="{want}"' in h, f"I11: month, orientation '{orient or 'not sent'}' → {want}")
    ok('data-paper="land"' in c.get("/print?view=day&orient=land&start=2026-10-14&end=2026-10-14").text, "I11: Landscape sets a day too")
    ok(post("/ui/print", view="month", theme="light", weekends="1", orient="port").status_code in (200, 204) and main.store.get("ui_print").get("orient") == "port", "I11: the choice is remembered")
    ok('data-paper="port"' in c.get("/print?view=month&start=2026-10-01&end=2026-10-31").text, "I11: and used when none is sent")
    post("/ui/print", view="month", theme="light", weekends="1", orient="auto")
    ok('class="seg orientpick"' in page() and "@page land { size:landscape; margin:5mm }" in c.get("/print?view=month").text, "I11: Print Preview has the toggle; the margins are 5 mm")
    html = c.get("/print?view=month&start=2026-10-01&end=2026-10-31&orient=port").text
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.set_content(html); pg.wait_for_timeout(300)
        data = pg.pdf(format="Letter", prefer_css_page_size=True, print_background=True)
        cut = pg.evaluate("[...document.querySelectorAll('.cell')].filter(c => c.scrollHeight > c.clientHeight + 1).length")
        b.close()
    r = PdfReader(io.BytesIO(data)); wd, ht = float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height)
    ok(len(r.pages) == 1 and ht > wd and cut == 0, f"I11: a month set to Portrait is one portrait page, nothing cut ({len(r.pages)} pages, cut {cut})")

    # --- I22: the Administrator row ---
    p = page()
    ok("--ic-x:" in p and "--ic-ok:" in p, "I22: the Administrator box carries the ✕ and ✓ icons")
    ok("#pagelogin > .mhead" in css and ".adminhead { position:absolute" in css, "I22: its Status/Action box sits on the heading's line")

    # --- F36.1: the grips' side ---
    ok('gripsright' not in page(), "F36.1: the grips are on the left by default")
    c.post("/settings/look", data={"csrf": csrf, "grips": "right", "intensity": "100", "duration": "100"}, follow_redirects=False)
    ok(main.store.get("ui_grips") == "right" and "gripsright" in page(), "F36.1: Right is saved and put on the page")
    ok("body.gripsright .modrow > .handle" in read("app", "styles", "12-handles.css"), "F36.1: its stylesheet puts the handle in the right margin")
    c.post("/settings/look", data={"csrf": csrf, "grips": "left", "intensity": "100", "duration": "100"}, follow_redirects=False)
    ok(main.store.get("ui_grips") is None and "gripsright" not in page(), "F36.1: Left puts it back")

    # --- the browser: Full page fits each view; the event icons stay together ---
    port = PORT
    with sync_playwright() as pw:
        b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic " + base64.b64encode(b"t:password1").decode()})
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"http://127.0.0.1:{port}/?month=2026-10&date=2026-10-14"); pg.wait_for_timeout(800)
        pg.evaluate("document.getElementById('fullbtn').click()"); pg.wait_for_timeout(900)
        for v in ("month", "week", "day", "list"):
            pg.evaluate(f"(function(){{var s=document.getElementById('viewpick');s.value='{v}';s.dispatchEvent(new Event('change'))}})()"); pg.wait_for_timeout(1200)
            h, w = pg.evaluate("[document.documentElement.scrollHeight, innerHeight]"), pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
            ok(h[0] <= h[1] and w[0] <= w[1], f"I14: Full page, {v}: no scrollbar ({h[0]} of {h[1]} px high)")
        calw = pg.evaluate("document.getElementById('cal').getBoundingClientRect().width")
        ok(calw >= 1200, f"I14: Full page fills the width ({calw:.0f} of 1230 px)")
        pg.evaluate("(function(){var s=document.getElementById('viewpick');s.value='month';s.dispatchEvent(new Event('change'))})()"); pg.wait_for_timeout(1200)
        # I15 in the browser: hide United, then show it again
        pg.click("#cal .legitem[data-hide='src:ccs']"); pg.wait_for_timeout(1000)
        off = pg.evaluate("document.querySelector(\"#cal .legitem[data-hide='src:ccs']\").getAttribute('aria-pressed')")
        pg.click("#cal .legitem[data-hide='src:ccs']"); pg.wait_for_timeout(1000)
        on = pg.evaluate("document.querySelector(\"#cal .legitem[data-hide='src:ccs']\").getAttribute('aria-pressed')")
        ok(off == "false" and on == "true", "I15: in the browser United hides and shows again")
        pg.evaluate("document.getElementById('fullbtn').click()"); pg.wait_for_timeout(900)
        ok(pg.evaluate("document.getElementById('fullbtn').getAttribute('aria-pressed')") == "false" and "fullscreen" in pg.evaluate("document.querySelector('#fullbtn use').getAttribute('href')"),
           "F35: leaving Full page puts the Full page icon back")
        # I19 in the browser: the lines
        pg.goto(f"http://127.0.0.1:{port}/event?date=2026-10-14"); pg.wait_for_timeout(600)
        y = lambda sel: pg.evaluate(f"document.querySelector({sel!r}).getBoundingClientRect().top")
        ok(abs(y("#end_label") - y("label:has(#all_day)")) < 4, "I19: All-day Event is on Ends' line")
        ok(abs(y("label[for=end_time]") - y("label:has(#end_tz_differs)")) < 4, "I19: Different end time zone is on the end Time's line")
        ok(y("#end_date") < y("#end_time") < y("#start_tz"), "I19: the rows run Ends, Time, Time zone")
        pg.click("#all_day"); pg.wait_for_timeout(300)
        ok(pg.is_visible("label:has(#all_day)") and not pg.is_visible("#end_time"), "I19: ticked, All-day Event stays and the Time fields hide")
        # I17: the event's icons are one line
        pg.goto(f"http://127.0.0.1:{port}/?month=2026-10&date=2026-10-14"); pg.wait_for_timeout(800)
        pg.click("#cal details.ev:not(.deleted):not(.hidden) summary >> nth=0"); pg.wait_for_timeout(900)
        tops = pg.evaluate("Array.from(document.querySelectorAll('#cal details.ev[open] .evicons .evicon')).map(e => Math.round(e.getBoundingClientRect().top))")
        ok(len(tops) >= 4 and max(tops) - min(tops) <= 2, f"I17: the event's icons are on one line ({tops})")
        ok(not errs, f"no page errors {errs[:2]}")
        b.close()
    srv.should_exit = True
print("FAILS", fails); sys.exit(1 if fails else 0)
