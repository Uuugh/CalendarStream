"""0.1.15 browser tests: month picker, 12h/24h switch, Settings blocks."""
import os, re, sys, tempfile, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com")
for k in ("CCS_USERNAME","CCS_PASSWORD","http_proxy","https_proxy","HTTP_PROXY","HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
OUT = tempfile.mkdtemp(prefix="cs-shots-")      # screenshots taken along the way (not kept)
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8090, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2)
    main.logins.save_ccs("U123456", "pw12345"); main.state.last_auth_ok = True; main.state.status = "ok"
    c = httpx.Client(base_url="http://127.0.0.1:8090", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    # an event at 9:45–4:15 (the made-up schedule has none; the real one did)
    c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "title": "Ground school", "start_date": "2026-10-14", "start_time": "09:45",
                                "end_date": "2026-10-14", "end_time": "16:15"})
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(http_credentials={"username": "t", "password": "password1"}, viewport={"width": 1100, "height": 900})
        pg = ctx.new_page(); pg.goto("http://127.0.0.1:8090/?month=2026-10"); pg.wait_for_timeout(300)
        pg.click("#monthbtn"); pg.wait_for_timeout(100)
        ok(pg.is_visible("#monthpick") and pg.locator("#monthpick .months button.on").inner_text() == "Oct", "month picker opens with October marked")
        pg.screenshot(path=f"{OUT}/pick.png", clip={"x": 40, "y": 40, "width": 1020, "height": 330})
        pg.click('#monthpick [data-year="1"]'); pg.click('#monthpick [data-year="1"]')
        ok(pg.inner_text("#pickyear") == "2028" and pg.locator("#monthpick .months button.on").count() == 0, "› › goes to 2028")
        pg.click('#monthpick [data-m="03"]'); pg.wait_for_load_state(); pg.wait_for_timeout(200)
        ok("date=2028-03-01" in pg.url and "March 2028" in pg.inner_text("#monthbtn"), "picking Mar jumps to March 2028")
        pg.click("#monthbtn"); pg.click(".calhead .navbtn.wide", position={"x": 2, "y": 2}, trial=True); pg.mouse.click(5, 5); pg.wait_for_timeout(100)
        ok(not pg.is_visible("#monthpick"), "clicking elsewhere closes the picker")
        pg.goto("http://127.0.0.1:8090/?month=2026-10"); pg.wait_for_timeout(200)
        sw = pg.locator("#clockswitch"); box = sw.bounding_box(); cal = pg.locator("#cal").bounding_box()
        knob = pg.locator("#clockswitch span").bounding_box()
        ok(round(box["height"]) == 22 and round(box["width"]) == 38 and box["y"] <= knob["y"] and knob["y"] + knob["height"] <= box["y"] + box["height"] + 0.5,
           f"12h/24h slider keeps its size, knob inside the track ({box['width']:.0f}x{box['height']:.0f})")
        dot = pg.locator(".legend .helpdot").bounding_box()
        ok(round(dot["height"]) == 15, "legend help dot: one 15 px help icon (F1.2, 0.2.8)")
        ok(sw.get_attribute("aria-checked") == "false" and "9:45am" in pg.content() and cal["x"] + cal["width"] - (box["x"] + box["width"]) < 180, "12h/24h switch at the top right (Print and + beside it), 12-hour by default (English)")
        sw.click(); pg.wait_for_load_state(); pg.wait_for_timeout(600)
        ok(main.ui_clock() == "24" and pg.locator("#clockswitch").get_attribute("aria-checked") == "true" and "09:45–16:15" in pg.content(), "switch → 24-hour, saved, calendar redrawn")
        pg.locator("#clockswitch").click(); pg.wait_for_timeout(600)
        ok(main.ui_clock() == "12", "switch back → 12-hour")
        pg.goto("http://127.0.0.1:8090/?menu=settings"); pg.wait_for_timeout(300)
        groups = pg.locator("#menu .mgroup")
        ok(groups.count() == 5 and all(groups.nth(i).evaluate("e => getComputedStyle(e).borderLeftStyle") == "solid" for i in range(groups.count())), "every Settings section is outlined")
        u, pw_ = pg.locator("#luser").bounding_box(), pg.locator("#lnew").bounding_box()
        ok(abs(u["y"] - pw_["y"]) < 3 and pg.locator("label[for=luser] span").inner_text() == "User name", "login form: labels above, boxes side by side")
        pg.locator("#menu").screenshot(path=f"{OUT}/menu3.png")
        pg.goto("http://127.0.0.1:8090/?month=2026-10"); pg.wait_for_timeout(300)
        ok(pg.is_visible("#src-ccs .statusbox .chip") and pg.is_visible("#src-ccs .statusbox button:has-text('Sync Now')"), "0.2.2: the source's header shows its status and Sync Now")
        # 0.2.8 (F4): + Add a rule → New rule… opens the If/Then dialog; Apply saves it for every calendar
        if pg.locator("#cfg-ccs[hidden]").count(): pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(100)
        picks = pg.locator("#rules-ccs .srcrules .rulebox")
        ok(picks.count() == 2 and "Items without an end time" in picks.nth(0).inner_text(), "a source starts with the two predefined rules")
        pg.click("#rules-ccs .addrule"); pg.wait_for_timeout(50)
        ok(pg.is_visible("#rules-ccs .rulemenu .newrule"), "+ Add a rule opens its menu")
        pg.click("#rules-ccs .rulemenu .newrule"); pg.wait_for_timeout(150)
        ok(pg.eval_on_selector("#ruledialog", "d => d.open") and pg.eval_on_selector_all("#ruledialog .rdapply input:checked", "o => o.map(x => x.value)") == ["ccs"],
           "New rule… in a calendar opens the rule dialog, applying to that calendar (0.2.8-beta.3)")
        pg.fill("#ruledialog .cond .cval", "RDO"); pg.select_option("#ruledialog .cond .cjoin", "or"); pg.wait_for_timeout(50)
        pg.locator("#ruledialog .cond").nth(1).locator(".cval").fill("LSR")
        pg.click("#ruledialog .psave"); pg.wait_for_timeout(1500)
        made = [r for r in main.all_rules() if [c.get("value") for c in r["conds"]] == ["RDO", "LSR"]]
        ok(len(made) == 1 and made[0]["conds"][1]["join"] == "or" and made[0]["apply"] == ["ccs"], "the new rule is saved: RDO or LSR, for CCS+")
        if pg.locator("#cfg-ccs[hidden]").count(): pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(100)
        ok(pg.locator("#rules-ccs .srcrules .rulebox").count() == 3 and pg.locator("#rules .rulelist .rulebox").count() == len(main.all_rules()) == 3, "3 rules on the source, and in All Rules")
        rid = made[0]["id"]
        pg.locator(f'#rules-ccs .ruleline[data-rule-id="{rid}"] .unapply').click(); pg.wait_for_timeout(1500)
        ok(all(r["id"] != rid for r in main.source_rules("ccs")) and any(r["id"] == rid for r in main.all_rules()), "the bin takes it off the source; it stays in All Rules")
        # I2: all-day only by its box or its words
        pg.goto("http://127.0.0.1:8090/event?date=2026-10-12&month=2026-10"); pg.wait_for_timeout(200)
        lab = pg.locator("label:has(#all_day)").bounding_box(); form = pg.locator("form.card").bounding_box()
        pg.mouse.click(form["x"] + form["width"] - 40, lab["y"] + lab["height"] / 2); pg.wait_for_timeout(50)
        ok(not pg.is_checked("#all_day"), "I2: clicking empty space to the right of All-day doesn't tick it")
        pg.click("text=All-day"); pg.wait_for_timeout(50)
        ok(pg.is_checked("#all_day"), "clicking the words ticks it")
        pg.goto("http://127.0.0.1:8090/?month=2026-10"); pg.wait_for_timeout(300)
        ok(pg.locator("#dest-google").count() == 0 and pg.locator("#googlesync").count() == 1 and pg.locator(".box.dest").count() == 2, "0.2.8-beta.4: two destinations; the Google sign-in is in Settings")
        ok(pg.locator(".legend .helpdot").count() == 1 and pg.locator("#cal > p.muted").count() == 0, "#10: one legend row with a help dot")
        ok(pg.locator("#rules details.guide").count() == 0 and pg.locator("#ruledialog details.guide").count() == 1, "beta.3 (F5.1): How rules work is in the rule dialog, not under All Rules")
        pg.set_input_files("#src-ccs .filebtn input", files=[{"name": "Calendar.ics", "mimeType": "text/calendar", "buffer": b"BEGIN:VCALENDAR\r\nEND:VCALENDAR\r\n"}])
        ok(pg.inner_text("#src-ccs .filebtn span") == "Calendar.ics", "#9: the file button shows the chosen file")
        heights = pg.evaluate("Array.from(document.querySelectorAll('#sources button:not(.plus):not(.hmove):not(.linkbtn):not(.syncnow):not(.cfgtoggle):not(.okslot button):not(.rulebox button):not(.addrule):not(.casebtn):not(.addtag):not(.deltag):not(.copybtn):not(.eye):not(.inboxbtn):not([hidden]), #destinations button:not(.plus):not(.hmove):not(.linkbtn):not(.syncnow):not(.cfgtoggle):not(.okslot button):not(.rulebox button):not(.addrule):not(.casebtn):not(.addtag):not(.deltag):not(.copybtn):not(.eye):not(.inboxbtn):not([hidden]), #destinations a.btn, #destinations a.btn2, #sources .filebtn')).filter(e => e.offsetParent).map(e => Math.round(e.getBoundingClientRect().height))")
        ok(set(heights) <= {34}, f"#9: every visible button is one height ({sorted(set(heights))})")
        ctx.close()
        ctx = b.new_context(http_credentials={"username": "t", "password": "password1"}, viewport={"width": 390, "height": 900}, color_scheme="dark")
        pg = ctx.new_page(); pg.goto("http://127.0.0.1:8090/?month=2026-10"); pg.wait_for_timeout(300)
        pg.click("#monthbtn"); pg.wait_for_timeout(100)
        pg.screenshot(path=f"{OUT}/pick_phone.png", clip={"x": 0, "y": 40, "width": 390, "height": 420})
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
