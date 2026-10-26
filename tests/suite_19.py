"""0.1.11 tests: time format, event form (menus, color, buttons, length kept), Google client fold."""
import tempfile
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
    os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main, gsync
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
REAL = os.path.join(HERE, "data", "Demo.ics")
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8094, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2)
    c = httpx.Client(base_url="http://127.0.0.1:8094", auth=A, follow_redirects=False)
    p = c.get("/").text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(REAL, "rb").read())})
    # an event at 9:45–4:15 (the made-up schedule has none; the real one did)
    c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "title": "Ground school", "start_date": "2026-10-14", "start_time": "09:45",
                                "end_date": "2026-10-14", "end_time": "16:15"})
    ok('data-clock=' not in p and 'id="clockswitch"' in p, "F1.5: no Time format in Settings; the switch above the calendar")
    p = c.get("/?month=2026-10").text
    ok("9:45am–4:15pm" in p and "09:45–16:15" not in p, "Automatic in English: 12-hour in the calendar")
    ok(c.post("/ui/clock", data={"csrf": csrf, "clock": "24"}).status_code == 204, "choose 24-hour")
    p = c.get("/?month=2026-10").text
    ok("09:45–16:15" in p and 'id="clockswitch" aria-checked="true"' in p, "24-hour in the calendar")
    e = c.get("/event?date=2026-10-08&month=2026-10").text
    ok('id="start_time" name="start_time" value="09:00"' in e and 'start_hour' not in e, "24-hour: one time box, 09:00")
    c.post("/ui/clock", data={"csrf": csrf, "clock": "12"})
    e = c.get("/event?date=2026-10-08&month=2026-10").text
    ok('id="start_time" name="start_time" value="9:00am"' in e and 'value="10:00am"' in e, "12-hour: one time box, 9:00am–10:00am")
    ok('name="start_tz"' in e and '<option value="America/New_York" selected>' in e and 'id="end_tz_differs"' in e, "time zone menu (the calendar's zone) and the different-end option")
    ok(e.count('name="color"') == 12 and 'value="#d50000"' in e, "color palette: default + Google's 11")
    ok(c.post("/ui/clock", data={"csrf": csrf, "clock": "x"}).status_code == 400, "unknown time format refused")
    # Save with typed times and a color
    r = c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "title": "Sim check", "start_date": "2026-10-08",
               "start_time": "1:30 pm", "end_date": "2026-10-08", "end_time": "1505", "start_tz": "America/New_York", "color": "#8E24AA"})
    ok(r.status_code == 303, "save with typed times")
    ev = [x for x in main.store.load_events() if x.title == "Sim check"][0]
    ok(ev.start.startswith("2026-10-08T13:30") and ev.end.startswith("2026-10-08T15:05") and ev.color == "#8e24aa", f"1:30 pm–1505 stored as 13:30–15:05, color kept ({ev.start[11:16]}–{ev.end[11:16]}, {ev.color})")
    r = c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "title": "x", "start_date": "2026-10-08",
               "start_time": "13pm", "end_date": "2026-10-08", "end_time": "2pm"})
    ok(r.status_code == 400, "13pm refused")
    r = c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "title": "x", "start_date": "2026-10-08", "start_time": "09:00",
               "end_date": "2026-10-08", "end_time": "10:00", "color": "#123456"})
    ok(r.status_code == 400, "colors outside Google's palette refused")
    r = c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "title": "Old form", "start_date": "2026-10-09", "start_time": "09:00",
               "end_date": "2026-10-09", "end_time": "10:00"})
    ok(r.status_code == 303, "plain HH:MM still accepted")
    p = c.get("/?month=2026-10").text
    ok("--sw:color-mix(in srgb, #8e24aa" in p or "#8e24aa" in p, "event color shows in the calendar")
    # color overrides tags in Google too
    import seed
    seed.rule(c, csrf, "", [seed.text("Sim")], [{"type": "color", "color": "#0b8043"}])
    ev = [x for x in main.store.load_events() if x.title == "Sim check"][0]
    ok(main.event_colorer()(ev) == "#8e24aa" and gsync.nearest_color_id(ev.color) == "3", "event color beats the tag (Google color Grape)")
    uid = ev.uid
    e = c.get(f"/event?uid={uid}&month=2026-10").text
    ok('value="#8e24aa" data-c="#8e24aa" data-name="Grape" checked' in e and ">Grape</span>" in e, "edit page shows the chosen color")
    # United event color edit
    u = [x for x in main.store.load_events() if x.origin == "united" and not x.all_day][0]
    f = main._form_values(u)
    c.post("/event/save", data={"csrf": csrf, "uid": u.uid, "month": "2026-10", "title": u.title, "start_date": f["start_date"],
           "start_time": f["start_time"], "end_date": f["end_date"], "end_time": f["end_time"], "color": "#f6bf26"})
    u2 = main.store.get_event(u.uid)
    ok(u2.color == "#f6bf26" and u2.edited and not u2.stale, "United event: color kept as an edit, not stale")
    # CCS+ wording and Google client fold
    main.logins.save_ccs("U123456", "pw12345"); main.state.last_auth_ok = True
    p = c.get("/").text
    ok(len(re.findall(r'title="Validated: CCS\+ sign-in"><svg[^>]*>.*?</svg>Validated</span>', p)) == 1, "✓ Validated right of the CCS+ boxes")
    main.store.set("google_client", {"id": "123-abc.apps.googleusercontent.com", "secret": main.google._seal("s3cret"),
                                     "check": {"ok": True, "message": "Google accepted the client ID and secret", "at": "2026-10-20T20:00:00+00:00"}})
    main.google._client = None
    p = c.get("/").text
    ok(len(re.findall(r'title="Validated: Client ID & Client secret"><svg[^>]*>.*?</svg>Validated</span>', p)) == 1 and 'value="123-abc.apps.googleusercontent.com"' in p, "valid Google client: boxes shown, ✓ Validated to their right")
    ok('action="/google/connect"' in p, "Connect stays outside the fold")
    main.store.set("google_client", {**main.store.get("google_client"), "check": {"ok": False, "message": "Google rejected the client ID", "at": "2026-10-20T20:00:00+00:00"}})
    p = c.get("/").text
    ok("Check both values and save again" in p and re.search(r'<span class="okslot" data-state="needs">\s*<span class="okmark" title="Validated: Client ID & Client secret">', p) is not None, "F1.2: rejected client: Save instead of ✓, with the error")
    main.store.delete("google_client")

    # Tag Colors: own block under the health bar, own save route
    p = c.get("/").text
    body = p[p.index('id="src-ccs"'):]
    ok("Rules" in p and body.index('action="/setup/ccs"') < body.index('id="rules-ccs"'), "0.2: Rules (were Tag Colors) inside the source box")
    ok('id="ed-ccs"' not in p and 'class="namebox nameinput editonly"' in p, "0.2.6: no (edit); the title is a field while Configure is open")
    rid = seed.rule(c, csrf, "", [seed.text("RDO")], [{"type": "color", "color": "#d50000"}], ["ccs"])
    ok(main.source_rules("ccs")[0]["id"] == rid, "0.2.8: /rules/save adds a calendar's own rule above the shared ones")
    c.post("/feed/name", data={"csrf": csrf, "name": "United Flying Schedule"})
    ok(any(r["id"] == rid for r in main.source_rules("ccs")), "renaming keeps the rules")
    c.post("/rules/delete", data={"csrf": csrf, "id": rid})
    ok(all(r["id"] != rid for r in main.all_rules()), "Remove deletes the rule")

    # Who reads the feed
    p = c.get("/").text
    ok("hasn’t read this feed yet" in p, "Google hasn't read the feed yet")
    c.get(f"/calendar/{main.settings.feed_token}.ics", headers={"User-Agent": "Google-Calendar-Importer"})
    p = c.get("/").text
    ok("Read by Google</span>" in p and "Google Calendar last read this feed" in p, "after Google's reader fetched it: last read shown")
    # Display time zone
    ok(c.post("/ui/tz", data={"csrf": csrf, "tz": "Mars/Base"}).status_code == 400, "unknown time zone refused")
    c.post("/ui/clock", data={"csrf": csrf, "clock": "24"})
    c.post("/ui/tz", data={"csrf": csrf, "tz": "America/Los_Angeles"})
    p = c.get("/?month=2026-10").text
    ok("06:45–13:15" in p and '<option value="America/Los_Angeles" selected>' in p, "calendar shown in Los Angeles time (09:45 New York → 06:45)")
    feed = c.get(f"/calendar/{main.settings.feed_token}.ics").text
    ok("X-WR-TIMEZONE:America/New_York" in feed, "the feed keeps TZ from .env")
    e = c.get("/event?date=2026-10-08&month=2026-10").text
    ok('<option value="America/Los_Angeles" selected>' in e, "new events start in the calendar's time zone")
    c.post("/ui/tz", data={"csrf": csrf, "tz": ""}); c.post("/ui/clock", data={"csrf": csrf, "clock": "12"})

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(); ctx = b.new_context(http_credentials={"username": "t", "password": "password1"}, viewport={"width": 800, "height": 900})
        pg = ctx.new_page(); pg.goto("http://127.0.0.1:8094/event?date=2026-10-08&month=2026-10"); pg.wait_for_timeout(200)
        val = lambda sel: pg.input_value(sel)
        def type_time(sel, text):
            pg.fill(sel, text); pg.dispatch_event(sel, "change"); pg.wait_for_timeout(50)
        type_time("#start_time", "11am")
        ok(val("#start_time") == "11:00am" and val("#end_time") == "12:00pm", f"typed 11am: end moves 10→12pm ({val('#end_time')})")
        pg.click("#end_time"); pg.wait_for_timeout(100)
        ok(pg.is_visible("#timelist") and pg.locator("#timelist [data-min='750']").inner_text().startswith("12:30pm (1 h 30 min)"), "end list shows times with lengths")
        pg.locator("#timelist [data-min='750']").dispatch_event("mousedown"); pg.wait_for_timeout(50)
        ok(val("#end_time") == "12:30pm" and not pg.is_visible("#timelist"), "picked 12:30pm from the list")
        type_time("#start_time", "2300")
        ok(val("#start_time") == "11:00pm" and val("#end_time") == "12:30am" and val("#end_date") == "2026-10-09", f"11am→2300 keeps 1 h 30: ends 12:30am the next day ({val('#end_date')} {val('#end_time')})")
        pg.fill("#start_date", "2026-10-12"); pg.dispatch_event("#start_date", "focus"); pg.dispatch_event("#start_date", "change")
        ok(val("#end_date") == "2026-10-13", "moving the start date moves the end date too")
        type_time("#start_time", "25:00")
        ok("bad" in pg.get_attribute("#start_time", "class") and not pg.eval_on_selector("form.card", "f => f.checkValidity()"), "25:00 is marked and blocks saving")
        type_time("#start_time", "23:00")
        # layout: color bottom-left, Cancel/Save bottom-right
        form = pg.locator("form.card").bounding_box(); cp = pg.locator("#colorpick summary").bounding_box()
        save = pg.locator(".actions.bottom .pairbtns .psave").bounding_box(); cancel = pg.locator(".actions.bottom .pairbtns .pcancel").bounding_box()
        ok(cp["x"] - form["x"] < 30 and form["x"] + form["width"] - (save["x"] + save["width"]) < 30 and cancel["x"] < save["x"] and abs(cp["y"] - save["y"]) < 10,
           "color at bottom left; Cancel, Save at bottom right")
        pg.click("#colorpick summary"); pg.click(".palette label[title=Tomato]"); pg.wait_for_timeout(50)
        ok(pg.inner_text("#colorname") == "Tomato" and not pg.eval_on_selector("#colorpick", "d => d.open"), "picking a color shows it and closes the palette")
        # a different end time zone: 9:00am New York → 10:00am Los Angeles (4 h)
        pg.goto("http://127.0.0.1:8094/event?date=2026-10-12&month=2026-10"); pg.wait_for_timeout(200)
        ok(not pg.is_visible(".endzone"), "one time zone by default")
        pg.check("#end_tz_differs"); pg.select_option("select[name=end_tz]", "America/Los_Angeles"); pg.wait_for_timeout(50)
        type_time("#start_time", "10am")
        ok(val("#end_time") == "11:00am", f"length kept in real hours across zones (end {val('#end_time')} LA)")
        pg.click("#colorpick summary"); pg.click(".palette label[title=Tomato]"); pg.wait_for_timeout(50)
        ok(pg.inner_text("#colorname") == "Tomato" and not pg.eval_on_selector("#colorpick", "d => d.open"), "picking a color shows it and closes the palette")
        pg.fill("#title", "Browser add"); pg.click(".actions.bottom button:not(.linkbtn)"); pg.wait_for_load_state(); pg.wait_for_timeout(200)
        ev = [x for x in main.store.load_events() if x.title == "Browser add"]
        ok(ev and ev[0].start == "2026-10-12T10:00:00-04:00" and ev[0].end == "2026-10-12T11:00:00-07:00" and ev[0].color == "#d50000", f"saved: 10am New York → 11am Los Angeles, Tomato ({ev[0].start if ev else ''} → {ev[0].end if ev else ''})")
        pg.goto(f"http://127.0.0.1:8094/event?uid={ev[0].uid}&month=2026-10"); pg.wait_for_timeout(200)
        ok(pg.is_visible(".endzone") and pg.input_value("select[name=end_tz]") == "America/Los_Angeles" and val("#end_time") == "11:00am", "reopens with both time zones")
        pg.goto("http://127.0.0.1:8094/"); pg.wait_for_timeout(200)
        if pg.locator("#cfg-ccs[hidden]").count(): pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(100)
        ok(pg.is_visible("#src-ccs .okmark") and not pg.is_visible("#src-ccs [data-save]"), "dashboard: ✓ Validated, no button")
        pg.fill("#src-ccs input[name=uid]", "U654321"); pg.wait_for_timeout(50)
        ok(not pg.is_visible("#src-ccs .okmark") and pg.is_visible("#src-ccs [data-save]"), "editing swaps ✓ for Save & sync")
        pg.goto("http://127.0.0.1:8094/?menu=settings"); pg.wait_for_timeout(200)
        ok(pg.locator("#ccsmenu").count() == 0 and pg.locator("#menu #google").count() == 0, "Settings has no CCS+ or Google logins")
        ok(pg.is_visible("#pagelogin .okmark") and not pg.is_visible("#lcur"), "page login: ✓ Signed in, current password hidden")
        pg.fill("#lnew", "newpassword1"); pg.wait_for_timeout(50)
        ok(pg.is_visible("#lcur") and pg.is_visible("#lconf") and pg.is_visible("#pagelogin [data-save]") and pg.eval_on_selector("#lcur", "e => e.required"), "typing a new password asks for the current one and shows Save")
        groups = [pg.locator("#menu .mgroup").nth(i).get_attribute("id") for i in range(pg.locator("#menu .mgroup").count())]
        ok(groups == ["pagelogin", "public", "admin", "googlesync", "updates"], f"Settings: site settings only, Google Calendar sync among them ({groups})")
        box = pg.locator("#publicurl").bounding_box(); btn = pg.locator("#usethis").bounding_box(); save = pg.locator("#public .okslot").bounding_box()
        ok(btn["x"] > box["x"] and btn["x"] + btn["width"] <= box["x"] + box["width"] and abs(save["y"] + save["height"] / 2 - (box["y"] + box["height"] / 2)) < 6, "This page inside the box; its ✓ / Save slot on the same line (0.2.8-beta.3)")
        pg.locator("#menu").screenshot(path=os.path.join(tempfile.gettempdir(), "cs-menu4.png"))
        pg.goto("http://127.0.0.1:8094/event?date=2026-10-12&month=2026-10"); pg.wait_for_timeout(200)
        pg.check("#end_tz_differs"); pg.click("#end_time"); pg.wait_for_timeout(100)
        pg.screenshot(path=os.path.join(tempfile.gettempdir(), "cs-event2.png"), full_page=True)
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
