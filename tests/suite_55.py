"""0.2.8-beta.19 tests, against the mock Google: a request Google refuses shows Google's own reason, never "no longer
accepts…", and a refusal a fresh token can't fix isn't retried (I1); a Google module's colors say the color doesn't
carry to Google (I1.1); a known browser gets past the limit for all addresses, and the one-time unlock link from the
container log makes a browser known (F6); a Google module's first Sync Now opens "Making the calendar…" in a new tab,
which then goes to Google Calendar, without ?cid= (F7); emoji older Windows may not draw get an (i) (F8)."""
import asyncio, json, os, re, sys, threading, time
from datetime import timedelta
from urllib.parse import urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
M = "http://127.0.0.1:8125"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8125, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, G = mockgoogle.S, httpx.Client()
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
log = lambda n=30: [h["msg"] for h in main.store.recent_log(n)]

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = ("t", "password1")
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    main.google.save_client(mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET)
    def connect(did):
        r = c.post("/google/account", data={"csrf": csrf, "did": did, "action": "connect"}, follow_redirects=False)
        back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
        return c.get(cb.path + "?" + cb.query, follow_redirects=False)
    def module(did):
        p = page(); box = p[p.index(f'id="dest-{did}"'):]
        return box[:box.index('class="cfgbody"')]
    with patch.object(main, "api_on", lambda: True):
        c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Flying", "sources": ["ccs"]})
    d = next(x for x in main.destinations("google") if x["name"] == "Flying")
    connect(d["id"])
    g = main.dest_google(main.destination(d["id"]))

    # --- F7: the first Sync Now after the calendar was made ---------------------------------------------------------
    main.google_job.wake.clear(); asyncio.run(main.google_sync_once(True))     # the sync that follows a sign-in
    ok(g.cal_info(d["id"]).get("shown") is False and f'data-gopen="/google/open/{d["id"]}"' in module(d["id"]),
       "F7: a module whose calendar was just made: its Sync Now opens Google Calendar (also after the sign-in's own sync)")
    c.post("/google/sync", data={"csrf": csrf})
    r = c.get(f"/google/open/{d['id']}", headers={"accept": "text/html"})
    ok(r.status_code == 200 and "Making the calendar…" in r.text and "Flying" in r.text, "F7: the tab says Making the calendar…")
    ok(c.get(f"/google/open/{d['id']}?check=1").json() == {}, "F7: …and waits while the sync runs")
    main.google_job.wake.clear()
    asyncio.run(main.google_sync_once(True))
    url = c.get(f"/google/open/{d['id']}?check=1").json().get("url", "")
    ok(url == "https://calendar.google.com/calendar/r?authuser=pilot%40example.com",
       "F7: …then Google Calendar, in the module's own Gmail")
    ok("cid=" not in url and "Add calendar" not in r.text, "F7: no ?cid= (Google's Add calendar?) and no Add calendar link")
    ok("data-gopen" not in module(d["id"]), "F7: only the first Sync Now opens it")
    feed = main.destinations("feed")[0]
    ok(c.get(f"/google/open/{feed['id']}").status_code == 404, "F7: not for a Calendar Feed")
    g._update_cal(d["id"], shown=None)
    ok("data-gopen" not in module(d["id"]), "F7: a calendar made before beta.19 (no mark) doesn't open a tab")

    # --- I1.1: the color note ---------------------------------------------------------------------------------------
    gbox = module(d["id"]); fbox = module(feed["id"])
    ok('class="palnote">Color change does not carry to Google<' in gbox, "I1.1: a Google module's colors say it doesn't carry to Google")
    ok("palnote" not in fbox, "I1.1: …a Calendar Feed's don't")

    # --- I1: Google's own reason; no retry a fresh token can't fix --------------------------------------------------
    S["refuse_color"] = True
    c.post("/destinations/update", data={"csrf": csrf, "did": d["id"], "name": "Flying", "sources": ["ccs"], "color": "#0b8043"})
    S["calls"].clear()
    ok(asyncio.run(main.google_sync_once(True)), "I1: a refused color doesn't fail the sync")
    lines = log()
    said = next((m for m in lines if "color couldn't be set" in m), "")
    ok("refused PATCH /users/me/calendarList" in said and "HTTP 401 authError" in said
       and "Request had invalid authentication credentials" in said and "Invalid Credentials" in said,
       "I1: History shows Google's own reason, word for word")
    ok(not any("no longer accepts" in m for m in lines) and not g.info().get("last_error"),
       "I1: …never \"no longer accepts CalendarStream's sign-in\", and the module stays healthy")
    ok(sum(x.startswith("PATCH /users/me/calendarList") for x in S["calls"]) <= 2,
       "I1: a 401 is tried again at most once, with a fresh token")
    g._access = None; S["calls"].clear()
    try:
        asyncio.run(g.set_color(d["id"], "#d50000")); ok(False, "refused")
    except gsync.AccessRevoked:
        ok(False, "I1: a refusal with a fresh token isn't a lost sign-in")
    except gsync.GoogleError as e:
        ok("refused" in str(e), "I1: a refusal with a fresh token is Google's refusal, not a lost sign-in")
    ok(sum(x.startswith("PATCH /users/me/calendarList") for x in S["calls"]) == 1,
       "I1: …and a fresh token isn't renewed to try again")
    S["calls"].clear()
    asyncio.run(main.google_sync_once(True))
    ok(not any(x.startswith("PATCH /users/me/calendarList") for x in S["calls"]), "I1: the same color isn't tried again")
    g._update_cal(d["id"], color_try=None)                 # tried by beta.18 (no color_try): tried once more
    S["calls"].clear()
    asyncio.run(main.google_sync_once(True))
    ok(any(x.startswith("PATCH /users/me/calendarList") for x in S["calls"]), "I1: a color beta.18 tried is tried once more")
    S["refuse_color"] = False
    for t in S["refresh"]: S["revoked"].add(t)
    g._access = None
    try:
        asyncio.run(g.api("GET", "/calendars/x")); ok(False, "revoked")
    except gsync.AccessRevoked as e:
        ok("Connect again" in str(e), "I1: a sign-in Google really dropped is still said so")
    S["revoked"].clear(); g._access = None

    # --- F6: known browsers and the unlock link ----------------------------------------------------------------------
    anon = TestClient(main.app, base_url="https://cal.example.com")
    login = lambda cl: cl.post("/login", data={"csrf": main.LOGIN_TOKEN, "user": "t", "password": "password1"}, follow_redirects=False)
    r = login(anon)
    ok(r.status_code == 303 and "cs_known" in r.headers.get("set-cookie", ""), "F6: a sign-in marks the browser as known")
    known = anon.cookies.get("cs_known")
    ok(known and main.known_browser(type("R", (), {"cookies": {"cs_known": known}})()), "F6: …with a signed cookie")
    ok(not main.known_browser(type("R", (), {"cookies": {"cs_known": known.split(".")[0] + ".00"}})()), "F6: a forged one isn't")
    warned = []
    with patch.object(main, "_own_network", lambda ip: False), patch.object(main.log, "warning", lambda *a: warned.append(a[0] % a[1:])):
        main._global_failures.clear(); main._good_ips.clear()
        for i in range(main.GLOBAL_MAX_FAILURES):
            main._count_failure(f"203.0.113.{i}")
        ok(any("/unlock/" in w and "within an hour" in w for w in warned), "F6: the limit tripping puts a one-time link in the container log")
        ok(any("container log" in m and "within an hour" in m for m in log()), "F6: …and History says where to find it")
        stranger = TestClient(main.app, base_url="https://cal.example.com")
        ok(login(stranger).status_code == 429, "F6: a new browser waits")
        mine = TestClient(main.app, base_url="https://cal.example.com"); mine.cookies.set("cs_known", known)
        ok(login(mine).status_code == 303, "F6: a known browser gets in, from anywhere")
        main._gui_failures["testclient"] = [0, main.now() + timedelta(minutes=15)]
        ok(login(mine).status_code == 429, "F6: …but the limit for its own address still applies")
        main._gui_failures.pop("testclient", None)
        link = next(w for w in warned if "/unlock/" in w).split()[-1]
        ok(link.startswith("https://cal.example.com/unlock/"), "F6: the link uses the public address")
        path = urlparse(link).path
        fresh = TestClient(main.app, base_url="https://cal.example.com")
        r = fresh.get(path, follow_redirects=False)
        ok(r.status_code == 303 and r.headers["location"] == "/login" and fresh.cookies.get("cs_known"),
           "F6: the unlock link makes that browser known and goes to the sign-in page")
        ok(login(fresh).status_code == 303, "F6: …which then gets in")
        ok(TestClient(main.app).get(path, follow_redirects=False).status_code == 404, "F6: the link works once")
        main._new_unlock(); main._unlock["until"] = main.now() - timedelta(seconds=1)
        ok(TestClient(main.app).get("/unlock/" + main._unlock["token"], follow_redirects=False).status_code == 404,
           "F6: …and only within the hour")
        main._global_failures.clear()

    # --- F8: emoji older Windows may not draw -------------------------------------------------------------------
    data = json.loads(c.get("/static/emoji.json").content)
    marks = {e[0]: len(e) > 3 for e in data["emoji"]}
    ok(marks.get("🥲") and not marks.get("😀") and not marks.get("✈️"), "F8: emoji newer than Emoji 12 are marked, older ones aren't")

    # --- In a browser: F7's tab, F8's (i) -------------------------------------------------------------------------
    from playwright.sync_api import sync_playwright
    def answer(route):
        rq = route.request; u = urlparse(rq.url)
        if u.hostname == "calendar.google.com":
            return route.fulfill(status=200, content_type="text/html", body="<title>Google Calendar</title>")
        r = c.request(rq.method, u.path + ("?" + u.query if u.query else ""), content=rq.post_data_buffer,
                      headers={k: v for k, v in rq.headers.items() if k.lower() not in ("host", "content-length")})
        route.fulfill(status=r.status_code, headers={k: v for k, v in r.headers.items() if k.lower() not in ("content-length", "content-encoding")}, body=r.content)
    g._update_cal(d["id"], shown=False)
    main.google_job.wake.clear()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1230, "height": 900}); errs = []
        ctx.route("http://cs.test/**", answer); ctx.route("https://calendar.google.com/**", answer)
        pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://cs.test/"); pg.wait_for_timeout(500)
        with ctx.expect_page() as tab:
            pg.click(f"#dest-{d['id']} .syncnow")
        t = tab.value; t.wait_for_load_state()
        ok("/google/open/" in t.url and "Making the calendar…" in t.inner_text("body"), "browser F7: Sync Now opens the tab at the click")
        ok(t.evaluate("window.opener") is None, "browser F7: …without a handle back to CalendarStream")
        main.google_job.wake.clear()
        th = threading.Thread(target=lambda: asyncio.run(main.google_sync_once(True))); th.start(); th.join()
        t.wait_for_url("https://calendar.google.com/**", timeout=8000)
        ok(t.url.startswith("https://calendar.google.com/calendar/r"), "browser F7: …then goes to Google Calendar")
        pg.goto("http://cs.test/?newrule=1&title=Test"); pg.wait_for_timeout(600)
        pg.evaluate("""() => { var s = document.querySelector('#ruledialog .act select.atype'); s.value = 'emoji';
                                s.dispatchEvent(new Event('change', { bubbles: true })); }""")
        pg.click("#ruledialog .emofind"); pg.fill("#ruledialog .emofind", "tear"); pg.wait_for_timeout(600)
        st = pg.evaluate("""() => [...document.querySelectorAll('#ruledialog .emogrid .emo')].map(b => [b.textContent, b.classList.contains('newemo'), b.title])""")
        new = [x for x in st if x[1]]; old = [x for x in st if not x[1]]
        ok(new and all("May not show on older Windows" in x[2] for x in new) and old and not any("Windows" in x[2] for x in old),
           "browser F8: in the grid, only newer emoji get the (i), \"May not show on older Windows\"")
        ok(pg.evaluate("getComputedStyle(document.querySelector('#ruledialog .emo.newemo'), '::after').content") == '"i"',
           "browser F8: …drawn as a small i")
        pick = lambda v: pg.evaluate("""v => { var f = document.querySelector('#ruledialog .aval.emoji'); f.value = v;
                                       f.dispatchEvent(new Event('input', { bubbles: true })); }""", v) or pg.wait_for_timeout(300)
        shown = lambda: pg.is_visible("#ruledialog .emowarn")
        pick("🇺🇸"); ok(shown(), "browser F8: a flag in the field gets the (i)")
        pg.click("#ruledialog .emowarn"); pg.wait_for_timeout(200)
        ok(pg.is_visible("#ruledialog .emowarn .helptip") and "May not show on older Windows" in pg.inner_text("#ruledialog .emowarn .helptip"),
           "browser F8: …the page's own (i): a tap shows \"May not show on older Windows\"")
        pick("✈️"); ok(not shown(), "browser F8: a universal emoji doesn't")
        pick("🥲"); ok(shown(), "browser F8: a newer emoji typed in does")
        pg.click(f"#ruledialog .emogrid .emo:not(.newemo)"); pg.wait_for_timeout(200)
        ok(not shown() and pg.input_value("#ruledialog .aval.emoji") != "", "browser F8: picking an older one clears it")
        ok(not errs, "browser: no script errors " + "; ".join(errs))
        b.close()
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
