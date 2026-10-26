"""0.2.8-beta.4 tests: caching (the page's stylesheet and script as cached, compressed files; versioned
fonts; feeds answering 304), event tools made when an event opens, Google Calendar sync in Settings,
+ Google Calendar making a feed while it isn't set up, empty form fields after the FastAPI upgrade."""
import gzip, os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
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
V = main.__version__

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8095, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8095", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    # + Google Calendar before Google Calendar sync is set up: a feed for Google
    main.store.set("public_url", "https://cal.example.com")
    post("/destinations/add", type="google", name="Flying")
    d = main.destinations()[-1]
    ok(d["type"] == "feed" and d["for"] == "google", "+ Google Calendar without Google Calendar sync: a feed for Google")
    p0 = c.get("/").text
    ok("set up <b>Google Calendar sync</b>" in p0, "…which points to Google Calendar sync in Settings")
    wid = seed.demo(c, csrf, main)
    p = c.get("/").text
    # caching: the stylesheet and script are files
    ok(f'<link rel="stylesheet" href="/assets/app.css?v={V}">' in p and f'<script src="/assets/page-{V}-en.js"></script>' in p and "<style>\n  * { box-sizing" not in p,
       "the page links its stylesheet and script instead of holding them")
    css = c.get(f"/assets/app.css?v={V}", headers={"Accept-Encoding": "gzip"})
    ok(css.status_code == 200 and css.headers.get("content-encoding") == "gzip" and "immutable" in css.headers.get("cache-control", "") and ".checks li" in css.text,
       "app.css: compressed, kept a year")
    js = c.get(f"/assets/page-{V}-fr.js")
    ok(js.status_code == 200 and "var PAGE = JSON.parse" in js.text and "{{" not in js.text and "immutable" in js.headers.get("cache-control", ""),
       "the script: one per version and language, kept a year")
    ok(c.get("/assets/page-0.0.1-en.js").status_code == 404 and c.get(f"/assets/page-{V}-xx.js").status_code == 404, "…only for this version and known languages")
    font = c.get(f"/static/fonts/ibm-plex-sans-latin-400-normal.woff2?v={V}")
    ok(font.status_code == 200 and "immutable" in font.headers.get("cache-control", "") and f"-normal.woff2?v={V}" in p, "fonts: versioned addresses, kept a year")
    ok("immutable" not in c.get("/static/fonts/ibm-plex-sans-latin-400-normal.woff2").headers.get("cache-control", ""), "…unversioned ones a day")
    ok("content-encoding" not in c.get("/", headers={"Accept-Encoding": "gzip"}).headers, "pages (with the form token) aren't compressed")
    # feeds: 304 when unchanged
    feed = main.destinations("feed")[-1]
    r1 = c.get(f"/calendar/{feed['token']}.ics"); tag = r1.headers.get("etag")
    r2 = c.get(f"/calendar/{feed['token']}.ics", headers={"If-None-Match": tag})
    ok(tag and r2.status_code == 304 and not r2.content, "a feed that hasn't changed answers 304")
    post("/event/save", month="2026-10", title="New one", start_date="2026-10-20", start_time="09:00", end_date="2026-10-20", end_time="10:00", source=wid)
    ok(c.get(f"/calendar/{feed['token']}.ics", headers={"If-None-Match": tag}).status_code == 200, "…and sends it again once it changed")
    # event tools: one template
    ok(p.count('id="evtoolstpl"') == 1 and p.count('class="linkbtn evclose"') == 1 and re.search(r'<span class="evtools" data-origin="united" data-alarms=""></span>', p) is not None,
       "event tools: once, in a template; each event only says what it is")
    # Google Calendar sync in Settings
    ok('id="dest-google"' not in p and 'id="googlesync"' in p and p.index('id="googlesync"') < p.index("</header>") and 'action="/google/client"' in p.split('id="googlesync"')[1][:20000],
       "Google Calendar sync is in Settings, not in Feeds")
    ok("Google Calendar · feed" in p and "Add to Apple / Outlook" in p and "set up <b>Google Calendar sync</b>" not in p, "the Google feed's module; no pointer once Google Calendar sync is set up")
    sub = p[p.index(f'id="dest-{d["id"]}"'):]; sub = sub[:sub.index('class="srcfoot"')]
    ok(sub.index("Add to Google Calendar") < sub.index("Add to Apple / Outlook") < sub.index("Feed link"), "…Add to Google Calendar first, the feed link last")
    main.store.set("google_client", {"id": "123-abc.apps.googleusercontent.com", "secret": main.google._seal("s"),
                                     "check": {"ok": True, "message": "", "at": "2026-10-20T20:00:00+00:00", "redirect_ok": True}})
    main.google._client = None
    post("/destinations/add", type="google", name="Synced")
    ok(main.destinations()[-1]["type"] == "google", "with Google Calendar sync set up, + Google Calendar is a Google calendar")
    r = c.post("/google/client", data={"csrf": csrf, "client_id": "123-abc.apps.googleusercontent.com", "client_secret": "", "action": "check"}, follow_redirects=False)
    ok(r.headers.get("location") == "/?menu=settings#googlesync", "Google's forms return to Settings")
    # empty fields after the FastAPI upgrade
    post("/feed/tags", sid=wid, name="Work", note="Office")
    post("/feed/tags", sid=wid, name="Work", note="")
    ok(main.calendar_note(wid) == "" if hasattr(main, "calendar_note") else "Office" not in c.get("/").text.split(f'id="src-{wid}"')[1][:3000], "an emptied note is saved empty")
    post("/destinations/update", did=feed["id"], name=feed["name"], sources=[wid], start="2026-10-01", end="")
    ok(main.destination(feed["id"])["start"] == "2026-10-01" and main.destination(feed["id"])["end"] == "", "an empty End date is no limit")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 1000}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8095/?month=2026-10"); pg.wait_for_timeout(600)
        ev = pg.locator("details.ev").filter(has_text="New one").first
        ev.locator("summary").click(); pg.wait_for_timeout(150)
        tools = ev.locator(".evtools")
        ok(tools.locator(".evclose").count() == 1 and tools.locator(".evedit").get_attribute("href").startswith("/event?uid=")
           and tools.locator("form.evdel input[name=uid]").input_value() == ev.get_attribute("data-uid"), "an opened event gets its tools, fitted to it")
        rule_ev = pg.locator("details.ev").filter(has_text="Drive to the airport").first
        rule_ev.locator("summary").click(); pg.wait_for_timeout(150)
        ok(rule_ev.locator(".evtools .evedit").count() == 0 and rule_ev.locator(".evtools .evdel").count() == 0 and rule_ev.locator(".evtools .evcopy").count() == 1,
           "…a rule's event: no edit or delete")
        pg.click("#menubtn"); pg.wait_for_timeout(200)
        ok(pg.is_visible("#googlesync") and pg.is_visible("#googlesync .gstate .chip"), "Settings shows Google Calendar sync and its state")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
