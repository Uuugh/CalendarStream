"""0.2.8-beta.33 tests (build 9): a status word that isn't an ongoing health check vanishes entirely after
shrinking to its icon, instead of keeping the icon forever (I21/F45); Escape in the rule dialog cancels exactly
like the Cancel button, so creating a rule from the event pop-up and pressing Escape brings the event pop-up
back instead of leaving with nothing (I37). Settings > Administrator's public-address rows: trashing the
domain row with another row present used to remove the whole row - its only + button and its "main" field
gone for good - instead of just clearing it, the way it already did when it was the only row (I22, found and
fixed here with a browser repro). I25's own claim (typing not registering at all) stays not reproducible from
the code, confirming the Dashboard's own automated check - see build-costs.md and the Dashboard's notes.
Settings: Updates moves to the top (F47) and its "up to date" status shows the running version (F53); Look is
renamed Theme (F46). The calendar's view picker (Month/Week/Day/List) and the Light/Dark/System switch both
become one icon with a dropdown menu, not a native <select> or a 3-button segmented control (F52, F57). The
Calendars/Key footer's dim-and-hide click works in every mode, not just Full page (F48)."""
import os, re, sys, threading, time
from datetime import datetime, timezone
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "IMAGE_TAG", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
read = lambda *p: open(os.path.join(os.path.dirname(HERE), *p)).read()
PORT = 8167

async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "updater_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    seed.demo(c, csrf, main)

    # --- I21/F45: the fold's general rule, and the macro/markup that opts History's "Saved" out of keeping ---
    fold = read("app", "templates", "js", "14-status-fold.js")
    ok("vanish" in fold and "data-fold-vanish" in fold, "I21/F45: a shrunk status can go on to vanish entirely, flagged by data-fold-vanish")
    ok("classList.add('gone')" in fold, "I21/F45: vanishing adds a .gone class before hiding the element")
    macros = read("app", "templates", "_macros.html")
    ok('keep=True' in macros and 'data-fold-vanish="1"' in macros, "I21/F45: okbutton's keep=True default marks data-fold-vanish only when keep is False")
    hist = read("app", "templates", "index", "history.html")
    ok("keep=False" in hist, "F45: History's \"Remember the last\" Saved confirmation opts out of keeping (it can never become unhealthy)")
    css = read("app", "styles", "15-features.css")
    ok(".chip.gone, .okmark.gone" in css and "prefers-reduced-motion:reduce" in css.split(".chip.gone, .okmark.gone")[1][:300], "I21/F45: the vanish fade respects reduced motion")

    # --- I35: a rule's calendar badge keeps naming a calendar that's since been removed (its own name if that
    # still resolves, else a generic one), instead of falling back to "No calendar yet" the way a rule whose
    # apply list is genuinely empty (never had one chosen) correctly does ---
    pyp = read("app", "routes", "page.py")
    ok('"used": [] if r["apply"] == "all" else rule_used(r["id"])' in pyp,
       "I35: a rule's used calendars come from rule_used(), reading the raw apply list directly, not filtered through today's live sources")
    rid = seed.rule(c, csrf, "I35 stale-calendar rule", [seed.text("I35TEST")], [{"type": "color", "color": "#8e24aa"}], ["ccs"])
    main.store.set("calendar_name:i35gone", "I35 Gone Calendar")
    # simulate what's left after its one calendar is gone by some path that doesn't prune the dead id from apply
    # (e.g. a destination/Google removal, distinct from /sources/remove's own cleanup): the id stays in apply.
    main.save_rules([{**r, "apply": ["i35gone"]} if r["id"] == rid else r for r in main.all_rules()])
    rp = c.get("/", headers={"accept": "text/html"}).text
    seg = rp[rp.index(f'data-rule-id="{rid}"'):]; seg = seg[:seg.index("</div>", seg.index("ruleused"))]
    ok("No calendar yet" not in seg, f"I35: the badge for a rule whose calendar was removed never says No calendar yet ({seg!r})")
    ok("I35 Gone Calendar" in seg, f"I35: it still shows the gone calendar's own name ({seg!r})")
    rid0 = seed.rule(c, csrf, "I35 never configured", [seed.text("I35NONE")], [{"type": "color", "color": "#8e24aa"}], [])
    rp0 = c.get("/", headers={"accept": "text/html"}).text
    seg0 = rp0[rp0.index(f'data-rule-id="{rid0}"'):]; seg0 = seg0[:seg0.index("</div>", seg0.index("ruleused"))]
    ok("No calendar yet" in seg0, f"I35: a rule that was genuinely never given a calendar still says so ({seg0!r})")

    # --- Playwright: the actual vanish, end to end, on History's Remember-the-last field ---
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg.goto(f"http://127.0.0.1:{PORT}/?menu=settings")
        pg.wait_for_selector("#activity")
        if pg.locator("#activity-body[hidden]").count(): pg.click("#activity > .cfgline .cfgtoggle")
        pg.wait_for_timeout(300)
        pg.fill('input[name="keep"]', "77")
        pg.click('.keepform .slotsave')
        pg.wait_for_timeout(600)
        shown = pg.evaluate("""() => { const m = document.querySelector('.keepform .okmark'); return m ? { hidden: m.hidden, cls: m.className } : null }""")
        ok(shown is not None and not shown["hidden"], f"I21/F45: right after Saved, the check mark is visible ({shown})")
        pg.wait_for_timeout(3200)   # past the first hold (icon-only)
        shrunk = pg.evaluate("""() => { const m = document.querySelector('.keepform .okmark'); return m ? m.className : null }""")
        ok(shrunk is not None and "shrunk" in shrunk, f"I21/F45: it shrinks to its icon after the hold ({shrunk})")
        pg.wait_for_timeout(3200)   # past the second hold (vanish)
        gone = pg.evaluate("""() => { const m = document.querySelector('.keepform .okmark'); return m ? { hidden: m.hidden, cls: m.className } : 'removed' }""")
        ok(gone == "removed" or (gone.get("hidden") and "gone" in gone.get("cls", "")), f"I21/F45: it then vanishes entirely, unlike an ongoing health check ({gone})")

        # --- Playwright: I37, Escape while writing a rule from the event pop-up brings the event back ---
        pg2 = b.new_page(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg2.goto(f"http://127.0.0.1:{PORT}/?month=2026-10")
        pg2.wait_for_selector(".day[data-add]")
        pg2.locator(".day[data-add]").first.click(position={"x": 5, "y": 5})
        pg2.wait_for_timeout(500)
        ok(pg2.eval_on_selector("#eventdialog", "el => el.open"), "I37: the event pop-up opens for a new event")
        frame = pg2.frame_locator("#eventdialog iframe")
        frame.locator('button[data-kind="rule"]').click(timeout=5000)
        pg2.wait_for_timeout(300)
        frame.locator(".newrulefor").click(timeout=5000)
        pg2.wait_for_timeout(500)
        ok(pg2.eval_on_selector("#eventdialog", "el => el.open") is False, "I37: writing the rule closes the event pop-up (suspended, not wiped)")
        ok(pg2.eval_on_selector("#ruledialog", "el => el.open"), "I37: the rule dialog opens for the new rule")
        pg2.keyboard.press("Escape")
        pg2.wait_for_timeout(1000)
        ok(pg2.eval_on_selector("#ruledialog", "el => el.open") is False, "I37: Escape closes the rule dialog")
        ok(pg2.eval_on_selector("#eventdialog", "el => el.open"), "I37: Escape, like Cancel, brings the event pop-up back - it doesn't close with the rule dialog")
        pg2.close()

        # --- Playwright: I22, trashing the domain row with another row present clears it, never removes it ---
        pg3 = b.new_page(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg3.goto(f"http://127.0.0.1:{PORT}/?menu=settings")
        pg3.wait_for_selector("#publicurl")
        pg3.click("#publicrows .domainrow .extraadd")
        pg3.wait_for_timeout(150)
        pg3.click("#publicrows .domainrow .extradel")
        pg3.wait_for_timeout(150)
        ok(pg3.eval_on_selector_all("#publicrows input[name=main]", "els => els.length") == 1,
           "I22: the domain row (and its only main field) is still there after trashing it with another row present")
        ok(pg3.eval_on_selector_all("#publicrows .extraadd", "els => els.filter(e => getComputedStyle(e).display !== 'none').length") == 1,
           "I22: its + button is still there too (now on the row that's last), so another address can still be added")
        ok(pg3.eval_on_selector("#publicurl", "el => el.value") == "",
           "I22: trashing the domain row clears it, same as when it was the only row")

        # --- I22: the + follows whichever row is last, not fixed to the domain row ---
        visible_add_parent = pg3.eval_on_selector_all(
            "#publicrows .extraadd",
            "els => { var v = els.find(e => getComputedStyle(e).display !== 'none'); return v && v.closest('.extrarow').className; }")
        ok(visible_add_parent is not None and "domainrow" not in visible_add_parent,
           f"I22: with an extra row present, the + sits on that last row, not the domain row ({visible_add_parent})")
        pg3.click("#publicrows .extrarow:last-child .extradel")
        pg3.wait_for_timeout(150)
        ok(pg3.eval_on_selector_all("#publicrows .extrarow", "els => els.length") == 1,
           "I22: removing the extra row takes it out entirely (unlike the domain row)")
        ok(pg3.eval_on_selector("#publicrows .domainrow .extraadd", "el => getComputedStyle(el).display") != "none",
           "I22: …and the + moves back onto the domain row, now that it's last again")

        # --- F56: changing the public address with Google already set up pops up a fix-it notice ---
        # (an https address, not this test server's own http://127.0.0.1 one, so redirect_ok reads true)
        main.store.set("public_url", "https://cal.example.com")
        redirect0 = "https://cal.example.com/google/callback"
        main.google.save_client("f56-test-client.apps.googleusercontent.com", "GOCSPX-f56testsecretvalue00")
        main.google._save_check(True, "Google accepted the client ID and secret", redirect0, True)
        before_gs = c.get("/?menu=settings", headers={"accept": "text/html"}).text
        before_gs = before_gs[before_gs.index('id="googlesync"'):before_gs.index('id="cal"')]
        ok('class="gassist"' not in before_gs, "F56 setup: Google Calendar API Sync reads as healthy before the address changes")
        pg3.fill("#publicurl", "https://cal.example.org")
        pg3.dispatch_event("#publicurl", "input")
        pg3.click('#pagelogin .psave')
        pg3.wait_for_timeout(1200)
        ok(pg3.eval_on_selector("#askdialog", "el => el.open") is True, "F56: saving a changed public address pops up a notice")
        text = pg3.eval_on_selector("#askdialog .asktext", "el => el.textContent")
        ok("redirect URI" in text and "Google Calendar API Sync" in text, f"F56: it says Google Calendar API Sync's redirect URI needs fixing ({text!r})")
        ok(pg3.locator("#googlesync .gassist").count() == 1,
           "F56: Google Calendar API Sync's own assist box is already drawn, redrawn by the save's own swap (no reload needed)")
        pg3.click("#askdialog button")
        pg3.wait_for_timeout(300)
        ok(pg3.eval_on_selector("#askdialog", "el => el.open") is False, "F56: OK closes the notice")
        main.store.set("public_url", "")    # leave it as it was found
        main.store.delete("google_client")
        pg3.close()
        b.close()

    # --- F46/F47/F53: Settings menu order and labels ---
    from app import updates as updatesmod
    main.store.set("update_check", {"checked": datetime.now(timezone.utc).isoformat(), "channel": updatesmod.channel(), "newest": main.__version__})
    sp = c.get("/?menu=settings", headers={"accept": "text/html"}).text
    first_group = re.search(r'<div class="mgroup" id="(\w+)"', sp)
    ok(first_group is not None and first_group[1] == "pagelogin", f"F47: Administrator is the first Settings section ({first_group})")
    ok(sp.index('id="pagelogin"') < sp.index('id="updates"') < sp.index('id="look"') < sp.index('id="googlesync"'),
       "F47: default order is Administrator, Updates, Theme, then any other modules (Google Calendar API Sync)")
    look_mhead = sp[sp.index('id="look"'):][:400]
    ok(">Theme<" in look_mhead, f"F46: the former Look/Appearance section is now called Theme ({look_mhead[:120]!r})")
    ok(">Appearance<" not in sp, "F46: the old 'Appearance' label is gone from the page")
    ok(re.search(rf'class="chip good"[^>]*title="v{re.escape(main.__version__)}"', sp),
       f"F53: Updates' up-to-date status shows the running version (v{main.__version__}), not \"Up to date\"")

    # --- F52: the view picker is a button + menu of icons, not a native <select> ---
    cp = c.get("/?date=2026-10-14", headers={"accept": "text/html"}).text
    ok('id="viewbtn"' in cp and 'id="viewmenu"' in cp and 'id="viewpick"' not in cp,
       "F52: the view picker is a button + menu (#viewbtn/#viewmenu), not the old <select id=viewpick>")
    ok(all(f'role="menuitemradio" data-view="{v}"' in cp for v in ("month", "week", "day", "list")),
       "F52: the menu has one choice per view")
    from playwright.sync_api import sync_playwright as _spw
    with _spw() as pw4:
        b4 = pw4.chromium.launch()
        pg4 = b4.new_page(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg4.goto(f"http://127.0.0.1:{PORT}/?date=2026-10-14")
        pg4.wait_for_selector("#viewbtn")
        ok(pg4.eval_on_selector("#viewmenu", "el => el.hidden"), "F52: the view menu starts closed")
        pg4.click("#viewbtn")
        ok(not pg4.eval_on_selector("#viewmenu", "el => el.hidden"), "F52: clicking the button opens the menu")
        pg4.click("#viewmenu [data-view='week']")
        pg4.wait_for_timeout(800)
        ok(pg4.eval_on_selector("#viewmenu", "el => el.hidden"), "F52: picking a view closes the menu again")
        ok(pg4.locator(".hourview").count() == 1, "F52: picking Week from the new menu actually switches the view")

        # --- F48: the key/calendar dim-and-hide click works outside Full page too (just the Month view here) ---
        pg4.goto(f"http://127.0.0.1:{PORT}/?date=2026-10-14")
        pg4.wait_for_selector("#cal .legitem[data-hide='src:ccs']")
        ok(pg4.eval_on_selector("#fullbtn", "el => el.getAttribute('aria-pressed')") == "false", "F48: not in Full page")
        pg4.click("#cal .legitem[data-hide='src:ccs']"); pg4.wait_for_timeout(1000)
        off = pg4.eval_on_selector("#cal .legitem[data-hide='src:ccs']", "el => el.getAttribute('aria-pressed')")
        ok(off == "false", f"F48: clicking a Calendars key item in plain Month view dims/hides it too ({off})")
        pg4.click("#cal .legitem[data-hide='src:ccs']"); pg4.wait_for_timeout(1000)   # leave it as it was found

        # --- F57: Light/Dark/System is one icon, a button + menu like the view picker ---
        ok(pg4.eval_on_selector("#thememenu", "el => el.hidden"), "F57: the theme menu starts closed")
        before = pg4.eval_on_selector("#themebtn", "el => el.innerHTML")
        pg4.click("#themebtn")
        ok(not pg4.eval_on_selector("#thememenu", "el => el.hidden"), "F57: clicking the theme button opens its menu")
        pg4.click("#thememenu [data-theme-choice='dark']")
        pg4.wait_for_timeout(200)
        ok(pg4.eval_on_selector("#thememenu", "el => el.hidden"), "F57: picking a theme closes the menu again")
        ok(pg4.eval_on_selector("html", "el => el.getAttribute('data-theme')") == "dark", "F57: picking Dark actually applies it")
        after = pg4.eval_on_selector("#themebtn", "el => el.innerHTML")
        ok(after != before, "F57: the closed button's icon changes to match the new choice")
        ok(pg4.eval_on_selector("#thememenu [data-theme-choice='dark']", "el => el.getAttribute('aria-checked')") == "true",
           "F57: the menu marks the current choice")

        # --- F51: the stretch handle lives inside #calbody now (bottom of the calendar, not the whole section) ---
        inside = pg4.eval_on_selector("#calbody", "el => el.contains(document.getElementById('calstretch'))")
        ok(inside, "F51: #calstretch is inside #calbody (the calendar itself), not below the key/footer")

        # --- F49/F50: the vertical rule sits right after the Calendars list (not stretched out), and View All ---
        pg4.goto(f"http://127.0.0.1:{PORT}/?date=2026-10-14")
        pg4.wait_for_selector(".legvr")
        gap = pg4.eval_on_selector_all(".legcals, .legvr", """els => els[1].getBoundingClientRect().left - els[0].getBoundingClientRect().right""")
        ok(gap < 20, f"F49: the vertical rule sits close to the Calendars list, not stretched to the middle ({gap:.0f}px gap)")
        ok(pg4.locator("#legviewall").count() == 0, "F50: View All is hidden when nothing is dimmed")
        pg4.click("#cal .legitem[data-hide='src:ccs']"); pg4.wait_for_timeout(1000)
        ok(pg4.locator("#legviewall").count() == 1, "F50: View All appears once something is dimmed")
        pg4.click("#legviewall"); pg4.wait_for_timeout(1000)
        restored = pg4.eval_on_selector("#cal .legitem[data-hide='src:ccs']", "el => el.getAttribute('aria-pressed')")
        ok(restored == "true", f"F50: View All clears the dimmed item ({restored})")
        ok(pg4.locator("#legviewall").count() == 0, "F50: View All hides itself again once nothing is dimmed")
        pg4.close(); b4.close()

# --- F55: the 8 master logo files moved from build_rules/ to app/static/logo/source/ ---
REPO = os.path.dirname(HERE)
LOGO_FILES = ["CalendarStream_Logo.png", "CalendarStream_Logo_Dark.png", "CalendarStream_Logo_Dark.svg",
              "CalendarStream_Logo_Light.png", "CalendarStream_Logo_Light.svg", "CalendarStream_Logo w Text.png",
              "CalendarStream_Mark_Dark.png", "CalendarStream_Mark_Light.png"]
for fn in LOGO_FILES:
    ok(os.path.exists(os.path.join(REPO, "app", "static", "logo", "source", fn)), f"F55: {fn} lives in app/static/logo/source/ now")
    ok(not os.path.exists(os.path.join(REPO, "build_rules", fn)), f"F55: {fn} is gone from build_rules/")
readme = read("README.md"); readme2 = read("README2.md")
ok("app/static/logo/source/CalendarStream_Mark_Light.png" in readme and "build_rules/CalendarStream_Mark" not in readme,
   "F55: README.md's logo link follows the move")
ok("app/static/logo/source/CalendarStream_Logo.png" in readme2 and "build_rules/CalendarStream_Logo" not in readme2,
   "F55: README2.md's logo link follows the move")
# the Theme Rules pictures (diagrams, not logos) stay put in build_rules/
ok(os.path.exists(os.path.join(REPO, "build_rules", "CalendarStream_Theme_Rules_Light.png")) and
   os.path.exists(os.path.join(REPO, "build_rules", "CalendarStream_Theme_Rules_Dark.png")),
   "F55: the Theme Rules pictures are not logos and stay in build_rules/")

print(f"\n{fails} failure(s)" if fails else "\nAll passed")
sys.exit(1 if fails else 0)
