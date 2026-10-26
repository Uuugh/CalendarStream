"""0.2.7-beta.6 tests: (?) help, Expand line, section icons, Cancel | Save pairs, saving without
reloading the page, spacing, 34 px fields and rule lines, one shade per calendar, Print, Calendars / Feeds."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8095, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8095", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    main.logins.save_ccs("U123456", "pw12345"); main.state.last_auth_ok = True
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    main.store.set("public_url", "https://cal.example.com")
    c.post("/destinations/add", data={"csrf": csrf, "type": "feed", "name": "Everything"})
    p = c.get("/").text
    ok('id="sourcestitle"><svg class="mi secicon"' in p and ">Calendars<" in p and "Feeds" in p and p.count('class="mi secicon"') == 5, f"({p.count('class=\"mi secicon\"')}) F1.3/F3.1/F4: section icons; Calendars and Feeds")
    ok("Expand for Details or to Edit Configuration" in p and '<span class="short">Expand</span>' in p and "Configure" not in re.sub(r"<[^>]+>", "", p.split('id="sources"')[1]).split("All Rules")[0], "F1.2: Expand for Details or to Edit Configuration")
    ok('class="helpdot' in p and "What other apps can subscribe to" in p and 'class=&#34;' not in p, "F1.1: explanations behind (?)")
    key = p.split('class="legend"')[1].split("</div>")[0]
    ok(">Timed<" not in key and ">All-day<" not in key, "I1: no Timed / All-day in the key")
    ok('class="iconbtn printbtn"' in p and "@media print" in c.get("/assets/app.css").text, "F2.1: Print")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        loads = []; pg.on("load", lambda: loads.append(1))
        pg.goto("http://127.0.0.1:8095/?view=month"); pg.wait_for_timeout(400); loads.clear()
        # I1: one shade per calendar
        bg = pg.evaluate("""() => { const t = document.querySelector('.ev:not(.allday):not(.custom)'), a = document.querySelector('.ev.allday:not(.custom)');
                                   return [getComputedStyle(t).backgroundColor, getComputedStyle(a).backgroundColor]; }""")
        ok(bg[0] == bg[1], f"I1: timed and all-day events in one shade ({bg})")
        # F1.1: (?) opens on click and closes with Escape
        dot = pg.locator("#destinations .cardhead .helpdot")
        dot.click(); pg.wait_for_timeout(100)
        ok(pg.is_visible("#destinations .cardhead .helptip"), "F1.1: (?) opens on click")
        pg.mouse.move(5, 5); pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        ok(not pg.is_visible("#destinations .cardhead .helptip"), "…and closes with Escape")
        # F1.4/F1.5: the source box's Cancel | Save
        if pg.locator("#cfg-ccs[hidden]").count(): pg.click("#src-ccs .cfgtoggle")
        pair = pg.locator("#src-ccs .pairbtns"); bb = pair.bounding_box()
        ok(round(bb["width"]) == 130 and round(bb["height"]) == 34 and [round(pair.locator(x).bounding_box()["width"]) for x in (".pcancel", ".psave")] == [65, 65],
           f"F1.4: Cancel | Save: one 130 × 34 px pair, 65 px each ({bb['width']:.0f}×{bb['height']:.0f})")
        pg.fill("#src-ccs .nameinput", "Changed name"); pair.locator(".pcancel").click(); pg.wait_for_timeout(300)
        ok(pg.input_value("#src-ccs .nameinput") == "United CCS Schedule" and pair.locator(".pcancel").inner_text() == "Cancelled" and round(pair.locator(".pcancel").bounding_box()["width"]) == 130,
           "F1.4: Cancel fills the pair, says Cancelled and undoes the typing")
        pg.wait_for_timeout(900)
        ok(pg.locator("#cfg-ccs[hidden]").count() == 1, "F1.1 (0.2.8): …then closes the module")
        pg.wait_for_timeout(2400)
        ok(pg.get_attribute("#src-ccs .pairbtns", "data-state") == "idle" and "Cancel" in pg.inner_text("#src-ccs .pairbtns"), "…and the pair is back after 3 s")
        pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(150)
        pg.fill("#src-dest-typing", "x") if pg.locator("#src-dest-typing").count() else None
        pg.click("#destinations .box.dest .cfgtoggle"); pg.wait_for_timeout(150)
        pg.fill("#destinations .box.dest .nameinput", "Typed elsewhere")
        pg.fill("#src-ccs .nameinput", "My Schedule"); pg.click("#src-ccs .pairbtns .psave"); pg.wait_for_timeout(1500)
        ok(main.calendar_name() == "My Schedule" and not loads, "F1.5: Save saves without reloading the page")
        ok(pg.get_attribute("#src-ccs .pairbtns", "data-state") == "saved" and pg.inner_text("#src-ccs .pairbtns .psave") == "Saved", "F1.4: …and says Saved")
        ok(pg.input_value("#destinations .box.dest .nameinput") == "Typed elsewhere", "F1.5: only that calendar's part of the page is refreshed (typing in Feeds kept)")
        ok("My Schedule" in pg.inner_text(".legend"), "…the calendar's key shows the new name")
        # after the swap the box still works: Expand and the rule lines
        pg.wait_for_timeout(3200)
        # F1.2 (0.2.8): every module and rule line has a handle: ▲, the drag grip, ▼
        lines = pg.locator("#src-ccs .ruleline")
        first, second = lines.nth(0).get_attribute("data-rule-id"), lines.nth(1).get_attribute("data-rule-id")
        h = lines.nth(0).locator(".handle")
        ok(h.locator(".hmove[data-dir=up]").count() == 1 and h.locator(".hgrip").count() == 1 and h.locator(".hmove[data-dir=down]").count() == 1, "a rule line's handle: ▲ ☰ ▼")
        h.locator(".hmove[data-dir=down]").click(); pg.wait_for_timeout(1500)
        ok([r["id"] for r in main.all_rules()][:2] == [second, first] and pg.locator("#src-ccs .ruleline").nth(0).get_attribute("data-rule-id") == second and not loads,
           "▼ lowers the rule's priority, in place")
        ok(pg.locator("#sources > .sortable > .modrow > .handle").count() == len(main.sources()), "each calendar module has a handle beside it")
        # F1.9: text boxes and rule lines 34 px, rounded rectangles
        hs = pg.evaluate("""() => Array.from(document.querySelectorAll('#cfg-ccs input[type=text], #cfg-ccs input[type=url], #cfg-ccs input[type=password], #cfg-ccs input[type=number]'))
                              .filter(e => e.offsetParent).map(e => Math.round(e.getBoundingClientRect().height))""")
        rl = pg.evaluate("() => Array.from(document.querySelectorAll('#src-ccs .srule')).map(e => [Math.round(e.getBoundingClientRect().height), getComputedStyle(e).borderTopLeftRadius])")
        ok(set(hs) == {34} and all(h == 34 and r == "8px" for h, r in rl), f"F1.9: 34 px text boxes {set(hs)} and rule lines {rl[:1]}")
        # F1.6–F1.8 spacing
        sp = pg.evaluate("""() => { const g = s => getComputedStyle(document.querySelector(s));
            return [g('#sources .cardhead').columnGap, g('#src-ccs .cfgline').marginTop, g('#cfg-ccs > h3.cfghead').marginTop, g('#cfg-ccs > h3.cfghead').marginBottom,
                    g('#cfg-ccs .cfggrid').rowGap, g('#cfg-ccs details.guide').marginTop, Math.round(document.querySelector('#cfg-ccs details.guide').getBoundingClientRect().height)]; }""")
        ok(sp == ["5px", "5px", "5px", "5px", "2px", "12px", 38], f"F1.6–F1.8/F1.10: spacing {sp}")
        # F3.2/F3.3
        ok(pg.evaluate("getComputedStyle(document.querySelector('#src-ccs .srcfoot')).borderTopStyle") == "solid", "F3.2: a line above Remove / Cancel / Save")
        # the rule dialog: Cancel | Apply, saving in the background
        pg.click("#rules .toggle"); pg.click("#rules .sfoot .newrule"); pg.wait_for_timeout(200)
        pg.fill("#ruledialog .cond .cval", "SIM"); pg.click("#ruledialog .psave"); pg.wait_for_timeout(1500)
        ok(any(c.get("value") == "SIM" for r in main.all_rules() for c in r["conds"]) and not loads and "SIM" in pg.inner_text("#rules .rulelist"), "F1.5: the rule dialog saves without reloading; All Rules shows it")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILS", fails)
