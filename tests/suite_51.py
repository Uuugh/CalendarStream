"""0.2.8-beta.17 tests, against the mock Google: Feeds rebuilt. Invite someone (F1: the one-time link, its page
without the login, the form token, single use, expiry, Withdraw, the sign-in making the calendar in the invited
account); a new Google module makes nothing in another account (I4); removing one doesn't sign the others out
(I5); the add flow (F7: the module picked first, then the module itself, its calendars and dates); Save checks
naming their fields (F8); Google Calendar (feed) is now a Calendar Feed (F9); the stream name edited and checked
(F5); the address drop-down and ☰ Settings' More addresses (F10, F11); Add to Outlook (F6); the Google modules
dimmed and refused while Google Calendar API Sync is off (F13). In a browser: the add flow, amber outlines, the
rule dialog's + outside the box with the ✕ column aligned (F14) and Create event on tidy groups (I6)."""
import asyncio, os, re, sys, threading, time
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
M = "http://127.0.0.1:8122"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8122, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, G = mockgoogle.S, httpx.Client()
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = ("t", "password1")
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    c.post("/sources/add", data={"csrf": csrf, "type": "ccs"})
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    c.post("/sources/add", data={"csrf": csrf, "type": "local", "name": "Local"})
    dests = lambda: main.destinations()
    by_name = lambda n: next(d for d in main.destinations() if d["name"] == n)

    # --- F13: Google Calendar API Sync off: the Google modules dimmed and refused --------------------------------
    p = page()
    ok(len(re.findall(r'class="opt pickdest" data-type="google1?" disabled', p)) == 2 and "Needs Google Calendar API Sync, which your admin turns on" in p,
       "F13: API off: Google 1-way and 2-way are dimmed in the picker, with why")
    ok(re.search(r'class="[^"]*\boff\b[^"]*">Google 2-way Sync<', p), "F13: …and dimmed in the Information & Instructions table")
    r = post("/destinations/add", type="google", name="Nope")
    ok(r.status_code == 400 and not any(d["name"] == "Nope" for d in dests()), "F13: a Google module can't be added while the API is off")
    ok("adminmail" not in p and "Admin e-mail" not in p and "/settings/admin-email" not in p, "F13: ☰ Settings has no administrator's e-mail any more")

    # --- F7, F9, F5: the add flow -------------------------------------------------------------------------------
    p = page()
    step1 = p[p.index('id="adddestpop"'):p.index('id="adddest2"')]
    ok(step1.count('class="opt pickdest"') == 3 and "Label" not in step1 and "It gets every source" not in step1,
       "F7: step 1 picks one of three modules, without a Label or the old note")
    step2 = p[p.index('id="adddest2"'):p.index('</dialog>', p.index('id="adddest2"'))]
    ok('name="name"' in step2 and 'name="note"' in step2 and 'name="stream"' in step2 and 'name="sources"' in step2 and 'name="start"' in step2
       and "statusbox" not in step2 and "cfgline" not in step2 and "Remove" not in step2, "F7: step 2 is the module itself, without status, Close line or Remove")
    r = post("/destinations/add", type="feed", name="Crew", note="for the crew room", sources=["ccs"], start="2026-01-01", end="")
    crew = by_name("Crew")
    ok(r.status_code == 303 and crew["sources"] == ["ccs"] and crew["start"] == "2026-01-01" and crew["note"] == "for the crew room",
       "F7: the add pop-up's calendars, dates and note are kept")
    post("/destinations/add", type="gfeed", name="Old kind")
    ok(by_name("Old kind")["type"] == "feed", "F9: Google Calendar (feed) is added as a Calendar Feed")
    r = post("/destinations/add", type="feed", name="Back", stream="https://cal.example.com/calendar/MyOldStreamName1234.ics")
    ok(by_name("Back")["token"] == "MyOldStreamName1234", "F5: an old link pasted as the stream name brings it back")
    r = post("/destinations/add", type="feed", name="Twin", stream="MyOldStreamName1234")
    ok(r.status_code == 400 and r.headers.get("X-CS-Fields") == "stream" and not any(d["name"] == "Twin" for d in dests()),
       "F5, F8: a stream name another feed uses is refused, naming the field")
    r = post("/destinations/update", did=crew["id"], name="Crew", stream="bad name")
    ok(r.status_code == 400 and r.headers.get("X-CS-Fields") == "stream", "F8: a stream name in the wrong form is refused, naming the field")
    r = post("/destinations/update", did=crew["id"], name="Crew", stream="CrewRoomStream12345")
    ok(r.status_code == 303 and by_name("Crew")["token"] == "CrewRoomStream12345", "F5: the stream name is edited in the module")
    r = post("/destinations/update", did=crew["id"], name="Crew", start="2026-05-01", end="2026-04-01")
    ok(r.status_code == 400 and r.headers.get("X-CS-Fields") == "end", "F8: an end before the start is refused, naming the field")

    # --- F10, F11, F6: addresses, the address drop-down, Add to Outlook ------------------------------------------
    r = post("/settings/public-extra", url=["https://calendar.example.org", "not an address"])
    ok(r.status_code == 400 and r.headers.get("X-CS-Fields") == "url1", "F11: a wrong address is refused, naming which one")
    post("/settings/public-extra", url=["https://calendar.example.org", ""])
    ok(main.store.get("public_urls_extra") == ["https://calendar.example.org"], "F11: More addresses are kept (an empty one is taken out)")
    post("/destinations/update", did=crew["id"], name="Crew", base="https://calendar.example.org")
    p = page()
    box = p[p.index(f'id="dest-{crew["id"]}"'):]
    box = box[:box.index('class="handle')] if 'class="handle' in box else box
    ok(re.search(r'<option value="https://calendar.example.org" selected>', box) and '<option value="+add">+ Add a domain</option>' in box,
       "F10: the feed link's address is a drop-down of every address, ending in + Add a domain")
    ok("https://calendar.example.org/calendar/CrewRoomStream12345.ics" in box.replace("&#34;", '"') or
       "calendar.example.org%2Fcalendar%2FCrewRoomStream12345.ics" in box, "F10: the links use the address chosen")
    ok(c.get("/calendar/CrewRoomStream12345.ics").status_code == 200, "…and the feed is there at the stream name")
    ok("outlook.live.com/calendar/0/addfromweb?url=" in box and "appgoogle" in box and "appapple" in box and "sendbtn" in box
       and "Open subscribe page" not in box, "F6: Add to Google / Apple / Outlook and Send to…; no Open subscribe page")
    ok(box.index("Feed link") < box.index("Account") < box.index("Include") < box.index("pcancel") < box.index(">Information "),
       "F4: link, account, Include, then Cancel | Save, then Information & Instructions")
    ok('class="noteinput editonly"' in box and 'placeholder="Note (optional)"' in box and box.index("noteinput") < box.index("srcright"),
       "F12: the note is in the header, placeholder Note (optional)")

    # --- Google on: the first account (as from before beta.17), then I4 -----------------------------------------
    main.google.save_client(mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET)
    def sign_in(url, client=c):
        back = G.get(url, follow_redirects=False); cb = urlparse(back.headers["location"])
        return client.get(cb.path + "?" + cb.query, follow_redirects=False)
    sign_in(main.google.sign_in_url("https://cal.example.com/google/callback"))
    ok(main.google.connected, "the first Google account is connected (from before beta.17)")
    with patch.object(main, "api_on", lambda: True):
        p = page()
        ok(not re.search(r'class="opt pickdest" data-type="google1?" disabled', p), "F13: API on: the Google modules can be picked")
        cals_before = set(S["calendars"])
        r = post("/destinations/add", type="google1", name="For Mom", sources=["ccs"])
        mom = by_name("For Mom")
        ok(r.status_code == 303 and mom["account"] and mom["oneway"] and not main.dest_google(mom).connected,
           "I4: a new Google module gets an account of its own, not connected")
        asyncio.run(main.google_sync_once(True))
        ok(set(S["calendars"]) == cals_before and not main.google.cal_info(mom["id"]).get("calendar_id"),
           "I4: …and nothing is made in the first account's Google Calendar")
        p = page()
        box = p[p.index(f'id="dest-{mom["id"]}"'):]
        ok('value="connect"' in box and "Invite someone" in box and "No Google account specified yet" in box and "pilot@example.com" not in box[:4000],
           "F2: no account filled in: Connect me or Invite someone")

        # --- F1: Invite someone ----------------------------------------------------------------------------
        r = post("/google/invite", did=mom["id"])
        p = page()
        m = re.search(r'value="(https://cal\.example\.com/invite/([A-Za-z0-9_-]+))"', p)
        ok(m and "works once, until" in p and ">Invited<" in p, "F1: Invite someone makes a one-time link, shown with its date")
        url, token = m[1], m[2]
        anon = TestClient(main.app, base_url="https://cal.example.com")
        r = anon.get(f"/invite/{token}", headers={"accept": "text/html"})
        form = re.search(r'name="form" value="([0-9a-f]+)"', r.text)
        ok(r.status_code == 200 and "For Mom" in r.text and "Continue with Google" in r.text and form, "F1: the invite page opens without the login")
        ok('id="destinations"' not in anon.get("/", headers={"accept": "text/html"}).text, "…the status page still needs the login")
        r = anon.post(f"/invite/{token}", data={"form": "0" * 32}, headers={"accept": "text/html"}, follow_redirects=False)
        ok(r.status_code == 400, "F1: Continue needs the page's form token")
        r = anon.post(f"/invite/{token}", data={"form": form[1]}, follow_redirects=False)
        ok(r.status_code == 303 and r.headers["location"].startswith(M + "/auth"), "F1: Continue goes to Google's sign-in")
        S["email"] = "mom@example.com"
        r = sign_in(r.headers["location"], anon)
        mom = by_name("For Mom"); gm = main.dest_google(mom)
        cal = main.google_for(mom["account"]).cal_info(mom["id"]).get("calendar_id")
        ok(r.status_code == 200 and "Done" in r.text and gm.connected and gm.info().get("email") == "mom@example.com",
           "F1: the invited person's sign-in connects the module")
        ok(cal and S["calendars"][cal]["owner"] == "mom@example.com", "F1: …its calendar is made in their Google Calendar")
        ok(main.google.info().get("email") == "pilot@example.com" and main.google.connected, "F1: …and the first account is unchanged")
        ok(anon.get(f"/invite/{token}", headers={"accept": "text/html"}).status_code == 404, "F1: an invite works once")
        # expiry and Withdraw
        post("/destinations/add", type="google", name="Sister")
        sis = by_name("Sister")
        post("/google/invite", did=sis["id"])
        tok2 = next(t for t, v in main.store.get("google_invites").items() if v["did"] == sis["id"])
        ok(anon.get(f"/invite/{tok2}", headers={"accept": "text/html"}).status_code == 200, "F1: a second module's invite works")
        post("/google/invite", did=sis["id"], action="withdraw")
        ok(anon.get(f"/invite/{tok2}", headers={"accept": "text/html"}).status_code == 404, "F1: Withdraw ends it")
        post("/google/invite", did=sis["id"])
        allinv = main.store.get("google_invites"); tok3 = next(t for t, v in allinv.items() if v["did"] == sis["id"])
        allinv[tok3]["expires"] = time.time() - 1; main.store.set("google_invites", allinv)
        ok(anon.get(f"/invite/{tok3}", headers={"accept": "text/html"}).status_code == 404, "F1: an invite ends after 7 days")
        ok(anon.get("/invite/not-a-real-invite-token-at-all", headers={"accept": "text/html"}).status_code == 404, "F1: a made-up link finds nothing")

        # --- I5: removing a module signed in with the same Gmail keeps the others signed in ------------------------
        S["email"] = "pilot@example.com"
        r = post("/destinations/add", type="google", name="Mine", then="connect")
        ok(r.status_code == 303 and r.headers["location"].startswith(M + "/auth"), "Connect me (while adding) goes straight to Google's sign-in")
        sign_in(r.headers["location"])
        mine = by_name("Mine"); gmine = main.dest_google(mine)
        ok(gmine.connected and gmine.info().get("email") == "pilot@example.com", "…and connects the new module")
        tok_mine = gmine._refresh_token()
        post("/destinations/remove", did=mine["id"], delete="1")
        ok(not any(d["name"] == "Mine" for d in dests()) and tok_mine not in S["revoked"] and main.google.connected,
           "I5: removing a module with the same Gmail as another doesn't revoke Google's grant: the first account stays connected")
        post("/destinations/remove", did=mom["id"], delete="")
        ok(any(t for t in S["revoked"]), "…a Gmail used by nothing else is still revoked when its module goes")

    # --- In a browser: the add flow, amber outlines, the rule dialog ---------------------------------------------
    from playwright.sync_api import sync_playwright
    def answer(route):
        rq = route.request; u = urlparse(rq.url)
        r = c.request(rq.method, u.path + ("?" + u.query if u.query else ""), content=rq.post_data_buffer,
                      headers={k: v for k, v in rq.headers.items() if k.lower() not in ("host", "content-length")})
        route.fulfill(status=r.status_code, headers={k: v for k, v in r.headers.items() if k.lower() not in ("content-length", "content-encoding")}, body=r.content)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1230, "height": 900}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.route("http://cs.test/**", answer)
        pg.goto("http://cs.test/"); pg.wait_for_timeout(500)
        pg.click("#destinations .addwrap .plus"); pg.wait_for_timeout(250)
        ok(pg.is_visible("#adddestpop .pickdest[data-type=feed]") and pg.is_enabled("#adddestpop .pickdest[data-type=google]"),
           "browser F7/F13: step 1 shows the modules, Google ones on while the API is")
        pg.click("#adddestpop .pickdest[data-type=feed]"); pg.wait_for_timeout(250)
        st = pg.evaluate("""() => ({ two: document.getElementById('adddest2').open, one: document.getElementById('adddestpop').open,
            kind: document.querySelector('#adddest2 .addkind').textContent, gacc: document.querySelector('#adddest2 .addfor[data-for=google]').hidden,
            type: document.querySelector('#adddest input[name=type]').value })""")
        ok(st["two"] and not st["one"] and st["kind"] == "Calendar Feed" and st["gacc"] and st["type"] == "feed",
           "browser F7: step 2 is the Calendar Feed module, without Google's account buttons")
        pg.fill("#adddest .nameinput", "Browser feed"); pg.fill("#adddest .fstream", "bad name")
        pg.click("#adddest .psave"); pg.wait_for_timeout(700)
        fx = pg.evaluate("""() => { const s = document.querySelector('#adddest .fstream'), cs = getComputedStyle(s);
            return { cls: s.className, oc: cs.outlineColor, warn: getComputedStyle(document.body).getPropertyValue('--warn').trim(), w: cs.outlineWidth } }""")
        ok("needsfix" in fx["cls"] and fx["w"] == "2px", f"browser F8: the refused field is outlined ({fx['oc']})")
        pg.fill("#adddest .fstream", "BrowserStream123456")
        ok("needsfix" not in pg.evaluate("document.querySelector('#adddest .fstream').className"), "browser F8: …until it's changed")
        pg.click("#adddest .psave"); pg.wait_for_timeout(1500)
        ok(any(d["name"] == "Browser feed" and d["token"] == "BrowserStream123456" for d in dests()) and not pg.evaluate("document.getElementById('adddest2').open"),
           "browser F7: Save adds it and closes the pop-up")
        # Send to… and copy inside the field
        did = by_name("Browser feed")["id"]
        pg.evaluate(f"setModule(document.getElementById('dest-{did}'), true)"); pg.wait_for_timeout(300)
        geo = pg.evaluate(f"""() => {{ const b = document.getElementById('dest-{did}');
            const fl = b.querySelector('.feedlink').getBoundingClientRect(), cp = b.querySelector('.feedcopy').getBoundingClientRect(),
                  ics = [...b.querySelectorAll('.feedlink .fmid')].pop().getBoundingClientRect();
            const hs = [...b.querySelectorAll('.addbtns .appbtn')].map(x => [Math.round(x.getBoundingClientRect().width), Math.round(x.getBoundingClientRect().height)]);
            return {{ inside: cp.left >= ics.right - 1 && cp.right <= fl.right + 1, hs }} }}""")
        ok(geo["inside"], "browser F10: the copy icon sits inside the field, after .ics")
        ok(len(geo["hs"]) == 4 and len(set(map(tuple, geo["hs"]))) == 1, f"browser F6: the four buttons are the same size ({geo['hs'][:1]})")
        pg.click(f"#dest-{did} .addbtns .sendbtn"); pg.wait_for_timeout(150)
        ok(pg.is_visible(f"#dest-{did} .sendmenu a[href^='mailto:']") and pg.is_visible(f"#dest-{did} .sendmenu a[href^='sms:']"),
           "browser F6: Send to… offers e-mail and a text message")
        pg.keyboard.press("Escape")

        # F14, I6: the rule dialog
        pg.evaluate("document.querySelector('#rules .sfoot .newrule').click()"); pg.wait_for_timeout(300)
        pg.click("#ruledialog .acts .aadd"); pg.wait_for_timeout(100)
        pg.select_option("#ruledialog .act:last-child .atype", "event"); pg.wait_for_timeout(200)
        g2 = pg.evaluate("""() => { const box = document.querySelector('#ruledialog .acts').getBoundingClientRect();
            const acts = [...document.querySelectorAll('#ruledialog .acts .act')], adds = [...document.querySelectorAll('#ruledialog .acts .aadd')].filter(x => !x.hidden);
            const xs = acts.map(a => Math.round(a.querySelector('.adel').getBoundingClientRect().right));
            const ev = acts[acts.length - 1], parts = [...ev.querySelectorAll('.evpart')];
            const tops = parts.map(p => p.getBoundingClientRect()), bad = parts.some(p => p.getBoundingClientRect().height > 40);
            const ab = adds.length ? adds[0].getBoundingClientRect() : null;
            const border = parseFloat(getComputedStyle(document.querySelector('#ruledialog .acts')).paddingRight);
            return { xs, out: ab && ab.left >= box.right - border - 1, parts: parts.length, bad } }""")
        ok(g2["out"], "browser F14: the action's + sits outside the rules box")
        ok(len(set(g2["xs"])) == 1, f"browser F14: the ✕ column stays aligned ({g2['xs']})")
        ok(g2["parts"] == 4 and not g2["bad"], "browser I6: Create event sits in four groups, none broken over lines")
        ok(not errs, f"browser: no script errors ({errs[:2]})")
        b.close()
print("FAILED:", fails) if fails else print("ALL PASSED")
