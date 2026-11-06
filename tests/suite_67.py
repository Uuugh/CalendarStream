"""0.2.8-beta.33 tests (build 9): a status word that isn't an ongoing health check vanishes entirely after
shrinking to its icon, instead of keeping the icon forever (I21/F45); Escape in the rule dialog cancels exactly
like the Cancel button, so creating a rule from the event pop-up and pressing Escape brings the event pop-up
back instead of leaving with nothing (I37). Settings > Administrator's public-address rows: trashing the
domain row with another row present used to remove the whole row - its only + button and its "main" field
gone for good - instead of just clearing it, the way it already did when it was the only row (I22, found and
fixed here with a browser repro). I25's own claim (typing not registering at all) stays not reproducible from
the code, confirming the Dashboard's own automated check - see build-costs.md and the Dashboard's notes."""
import os, re, sys, threading, time
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
        ok(pg3.eval_on_selector_all("#publicrows .extraadd", "els => els.length") == 1,
           "I22: its + button is still there too, so another address can still be added")
        ok(pg3.eval_on_selector("#publicurl", "el => el.value") == "",
           "I22: trashing the domain row clears it, same as when it was the only row")
        pg3.close()
        b.close()

print(f"\n{fails} failure(s)" if fails else "\nAll passed")
sys.exit(1 if fails else 0)
