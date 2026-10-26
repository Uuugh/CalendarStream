"""0.2.8-beta.5 tests: a rule's Color from Google's 11 colors (I1), rule lines "Color ■ (Name)" (F2), + in the
top right of All Rules and Event Templates (F3, F4), "Last synced" headers for calendars and feeds (F5, F6),
Settings: Copy for the Client ID and Updates as a module header (F1), the Soft light palette (F7)."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main, calsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    return calsync.Download(200, body=FEED, debug={"url": url})

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8096, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8096", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    wid = seed.demo(c, csrf, main)
    p = c.get("/?menu=settings").text
    # F2: rule lines
    ok('“RDO” → Color <span class="swatch" style="--c:#d50000" aria-hidden="true"></span> (Tomato)' in p, "F2: a rule line reads Color ■ (Tomato)")
    ok(re.search(r'<span class="rulelabel" title="Drive to the airport">Drive to the airport</span>', p) is not None, "…a rule with a title shows its title")
    # F3/F4: + after the count box
    for sec, box in (("rules", "rulecount"), ("templates", "tplcount")):
        head = p[p.index(f'id="{sec}" '):]; head = head[:head.index('class="cfgline"')]
        ok(head.index(f'id="{box}"') < head.index("headplus"), f"F3/F4: {sec}: + after the count box, in the corner")
    # F5/F6: headers
    ccs = p[p.index('id="src-ccs"'):]; ccs = ccs[:ccs.index('class="cfgline"')]
    ok(re.search(r'<p class="srcstatus">Last synced <b>[^<]+</b></p>', ccs) is not None and "Last check was" not in p, "F5: a calendar's header: Last synced (time)")
    feed = main.destinations("feed")[-1]
    c.get(f"/calendar/{feed['token']}.ics", headers={"User-Agent": "Google-Calendar-Importer"})
    p = c.get("/?menu=settings").text
    fh = p[p.index(f'id="dest-{feed["id"]}"'):]; fh = fh[:fh.index('class="cfgline"')]
    ok("Last read by Google <b>" in fh and "All dates" not in fh, "F6: a feed's header: Last read by Google (time) on the right, the same layout")
    # F1: Settings
    ok('onclick="copyField(\'fcid\', this)"' in p, "F1.1: Copy in the Client ID box")
    ud = p[p.index('id="updates"'):]; ud = ud[:ud.index("</form>")]
    ok('class="module bare"' in ud and ">Updates<" in ud and 'namebox srcnote">' in ud and 'class="statusbox' in ud and "Check now" in ud and "Updater: running" not in p,
       "F1.2/F1.3: Updates as a module header (title, channel, state, status box with Check now); no updater note")
    # F7: Light is the Soft palette
    ok("--bg:#f7f6f3" in p and "--accent:#40609c" in p, "F7: Light uses the Soft palette")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 1000}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8096/?month=2026-10"); pg.wait_for_timeout(500)
        # I1: the rule dialog's Color is one of Google's 11
        pg.click("#rules > .cfgline .cfgtoggle"); pg.click("#rules .newrule.headplus"); pg.wait_for_timeout(200)
        pal = pg.locator("#ruledialog .act .pal")
        ok(pal.count() == 11 and pg.locator("#ruledialog .act input[type=color]").count() == 0, "I1: Color offers Google's 11 colors, no free color picker")
        pg.fill("#ruledialog .cond .cval", "SIM")
        pg.locator('#ruledialog .act .pal[title="Peacock"]').click()
        ok(pg.locator('#ruledialog .act .pal[aria-checked="true"]').get_attribute("title") == "Peacock", "…the chosen one is marked")
        pg.click("#ruledialog .psave"); pg.wait_for_timeout(1500)
        new = main.all_rules()[-1]
        ok(new["actions"][0] == {"type": "color", "color": "#039be5"}, f"…and saved ({new['actions']})")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
