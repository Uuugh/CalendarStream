"""0.2.8-beta.15 tests, against the mock Google: rules (Title / Any text, matches pattern, contains regex and its
errors, the regex test box, two emojis); the calendar lifecycle (a CalendarStream calendar always on top, the
last one emptied, Remove with Merge or Delete and its rules, Download a copy, Import with dates and
Merge | Delete); History (Undo / Redo as a stack, how many are kept, deleted events struck through with
Restore, events removed by United kept struck through); Google modules (Google 1-way Sync, a Gmail of their
own, their color in Google, a deletion in Google struck through); the sign-in page; the container log;
All in a date range (the search)."""
import asyncio, json, os, re, sys, threading, time
from datetime import date, timedelta
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
from app import gsync, main, rules as rules_mod
M = "http://127.0.0.1:8121"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8121, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, A = mockgoogle.S, ("t", "password1"); G = httpx.Client(); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
run = asyncio.run
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
TODAY = date.today()

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    page = lambda: c.get("/", headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"})
    c.post("/sources/add", data={"csrf": csrf, "type": "ccs"})
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    locals_ = lambda: [x["id"] for x in main.sources() if x["type"] == "local"]

    # --- A CalendarStream calendar is always there, on top -----------------------------------------
    ok(main.sources()[0]["type"] == "local" and len(locals_()) == 1, "a CalendarStream calendar is there, on top (the default)")
    lid = locals_()[0]
    r = post("/sources/move", sid="ccs", before=lid)
    ok(r.status_code == 400 and "always a CalendarStream calendar" in r.json()["detail"], "another kind can't go on top (400, said why)")
    p = page()
    ok(re.search(rf'data-sid="{lid}" data-name="[^"]*" data-empty="1"', p) is not None and "Empty this calendar" in p,
       "the last CalendarStream calendar's trash says Empty")

    # --- Rules: Title / Any text, matches pattern, contains regex ------------------------------------
    c.post("/event/save", data={"csrf": csrf, "title": "Trip E1234", "start_date": (TODAY + timedelta(days=3)).isoformat(),
                                "start_time": "9:00", "end_date": (TODAY + timedelta(days=3)).isoformat(), "end_time": "10:00",
                                "location": "EWR gate C71", "source": lid})
    t = rules_mod.test_text("*E####", "pattern", False, ["Trip E1234", "E12345", "e9999"])
    ok([x["match"] for x in t["results"]] == [True, False, True], "matches pattern: * any text, # a digit (the whole title)")
    r = post("/rules/test", value="*E####", op="regex", samples="Trip E1234")
    ok(r.json()["error"].startswith("Not a valid regex: nothing to repeat"), "the test box says why a regex is broken")
    r = post("/rules/test", value=r"E\d{4}", op="regex", samples="Trip E1234\nRDO")
    ok([x["match"] for x in r.json()["results"]] == [True, False] and r.json()["results"][0]["span"] == [5, 10],
       "…and which titles a regex matches, with the matched part")
    r = post("/rules/save", rule=json.dumps({"conds": [{"type": "text", "op": "regex", "value": "*E####"}], "actions": [{"type": "emoji", "emoji": "✈️"}], "apply": "all"}))
    ok(r.status_code == 400 and "Not a valid regex" in r.json()["detail"], "saving a broken regex: refused with why (not 'fill in every condition')")
    rid = post("/rules/save", rule=json.dumps({"conds": [{"type": "text", "op": "pattern", "value": "*E####"}],
                                                "actions": [{"type": "emoji", "emoji": "✈️"}, {"type": "emoji", "emoji": "🧳"}], "apply": "all"})).json()["id"]
    e = next(x for x in main.store.load_events(lid) if "E1234" in x.title)
    ok(e.title.startswith("✈️ 🧳 "), f"a rule's two emojis both go in front of the title ({e.title!r})")
    post("/rules/save", rule=json.dumps({"conds": [{"type": "any", "op": "contains", "value": "gate C71"}], "actions": [{"type": "color", "color": "#f6bf26"}], "apply": "all"}))
    e = next(x for x in main.store.load_events(lid) if "E1234" in x.title)
    ok(e.rule_color == "#f6bf26", "Any text looks at the place and notes too")

    # --- History: Undo / Redo, a stack -----------------------------------------------------------------
    n = len(main.all_rules())
    post("/rules/delete", id=rid)
    top, nxt = main.store.undo_stack()
    old = [h["id"] for h in main.store.recent_log(50) if h["state"] == "done"][1]
    ok(post("/history/undo", entry=str(old)).status_code == 400, "only the newest change can be undone first")
    ok(post("/history/undo", entry=str(top)).status_code == 200 and len(main.all_rules()) == n, "Undo puts the deleted rule back")
    _, nxt = main.store.undo_stack()
    ok(nxt == top and post("/history/undo", entry=str(top), redo="1").status_code == 200 and len(main.all_rules()) == n - 1, "Redo deletes it again")
    ok(main.store.recent_log(1)[0]["kind"] in ("Rule", "Event", "Calendar", "Sync"), "every line has a Type")

    # --- Deleted events: struck through, Restore, gone when their Undo pops off ------------------------
    trip = next(x for x in main.store.load_events(lid) if "E1234" in x.title)
    post("/event/delete", uid=trip.uid)
    p = c.get(f"/?date={trip.start[:10]}", headers={"accept": "text/html"}).text   # its month (3 days ahead can be next month)
    ok(re.search(rf'data-uid="{re.escape(trip.uid)}" class="ev[^"]*deleted', p) and "Deleted in CalendarStream" in p and "/event/restore" in p,
       "a deleted event stays, struck through, saying where, with Restore")
    post("/event/restore", uid=trip.uid)
    ok(not main.store.get_event(trip.uid).deleted, "Restore brings it back")
    post("/event/delete", uid=trip.uid)
    post("/history/keep", keep="1")
    for i in range(2):       # two newer changes: the delete pops off, and the event is gone for good
        post("/rules/save", rule=json.dumps({"title": f"x{i}", "conds": [], "actions": [{"type": "color", "color": "#039be5"}], "apply": [lid]}))
    ok(main.store.get_event(trip.uid) is None and trip.uid not in page(), "…until its Undo pops off History (kept: the last 1): then it's gone")
    post("/history/keep", keep="20")

    # --- United removes an event: kept struck through, Restore keeps it ----------------------------------
    raw = DEMO.decode()
    future = [m for m in re.finditer(r"BEGIN:VEVENT.*?END:VEVENT\r?\n", raw, re.DOTALL) if (m2 := re.search(r"DTSTART[^:]*:(\d{8})", m.group(0))) and m2[1] >= TODAY.strftime("%Y%m%d")]
    if future:
        gone = future[0].group(0)
        title = re.search(r"SUMMARY:(.*)", gone)[1].strip()
        c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", raw.replace(gone, "").encode())})
        kept = [x for x in main.store.load_events("ccs") if x.deleted.startswith("united|")]
        ok(kept and title.replace("\\,", ",") in kept[0].title, "an event United removed stays here, struck through (Removed by United)")
        top, _ = main.store.undo_stack()
        line = next(h for h in main.store.recent_log(10) if h["msg"].startswith("United removed"))
        ok(top != line["id"] and line["state"] == "", "…done outside CalendarStream: Restore on the event, no Undo on the stack")
        post("/event/restore", uid=kept[0].uid)
        ok(not main.store.get_event(kept[0].uid).deleted and main.store.get_event(kept[0].uid).origin == "custom",
           "…Restore keeps it, as an event added here")
    else:
        ok(False, "the demo schedule has a future event to remove")

    # --- Import: dates (All), Merge | Delete for one already there; Undo -----------------------------------
    ics = main.build_feed([main.Event(title="Dentist", start=f"{TODAY + timedelta(days=5)}T15:00:00-04:00", end=f"{TODAY + timedelta(days=5)}T16:00:00-04:00", uid="imp-1@x"),
                           main.Event(title="Far away", start=f"{TODAY + timedelta(days=400)}T15:00:00-05:00", end=f"{TODAY + timedelta(days=400)}T16:00:00-05:00", uid="imp-2@x")],
                          "Mine", "America/New_York")
    r = c.post("/sources/import", data={"csrf": csrf, "sid": lid, "start": "", "end": (TODAY + timedelta(days=30)).isoformat()},
               files={"file": ("mine.ics", ics)}, headers={"X-CS-Async": "1"})
    j = r.json()
    ok(r.status_code == 200 and j["total"] == 1 and not j["conflicts"], "Import: only the events in the dates (To: 30 days)")
    post("/sources/import/finish", token=j["token"], choices="{}")
    dent = [x for x in main.store.load_events(lid) if x.title == "Dentist"]
    ok(len(dent) == 1 and dent[0].origin == "custom", "…added to the calendar")
    j = c.post("/sources/import", data={"csrf": csrf, "sid": lid}, files={"file": ("mine.ics", ics.replace(b"Dentist", b"Dentist (moved)"))},
               headers={"X-CS-Async": "1"}).json()
    ok(j["total"] == 2 and len(j["conflicts"]) == 1 and j["conflicts"][0]["file"]["title"] == "Dentist (moved)", "All: every date; the one already there is asked about")
    post("/sources/import/finish", token=j["token"], choices=json.dumps({j["conflicts"][0]["key"]: "merge"}))
    titles = sorted(x.title for x in main.store.load_events(lid) if x.title.startswith(("Dentist", "Far")))
    ok(titles == ["Dentist (moved)", "Far away"], f"Merge: the file's version updates it; the new one is added {titles}")
    top, _ = main.store.undo_stack()
    post("/history/undo", entry=str(top))
    ok(sorted(x.title for x in main.store.load_events(lid) if x.title.startswith(("Dentist", "Far"))) == ["Dentist"], "Undo takes the import back")

    # --- Remove: Merge (with its rules) or Delete; Download a copy ------------------------------------------
    c.post("/sources/add", data={"csrf": csrf, "type": "local", "name": "Second"})
    sid2 = next(x for x in locals_() if x != lid)
    c.post("/event/save", data={"csrf": csrf, "title": "Lunch", "start_date": TODAY.isoformat(), "start_time": "12:00",
                                "end_date": TODAY.isoformat(), "end_time": "13:00", "source": sid2})
    own = post("/rules/save", rule=json.dumps({"conds": [{"type": "text", "op": "is", "value": "Lunch"}], "actions": [{"type": "color", "color": "#33b679"}], "apply": [sid2]})).json()["id"]
    exp = c.get(f"/sources/export?sid={sid2}")
    ok(exp.status_code == 200 and b"SUMMARY:Lunch" in exp.content and "attachment" in exp.headers["content-disposition"], "Download a copy: the calendar as a .ics file")
    p = page()
    ok(re.search(rf'data-sid="{sid2}" data-name="Second" data-empty=""\s+data-rules="1"', p) is not None, "a calendar's Remove knows its own rules (1)")
    c.post("/sources/remove", data={"csrf": csrf, "sid": sid2, "keep": "merge", "into": lid, "rules": "move"})
    ok(sid2 not in main.source_ids() and any(x.title == "Lunch" for x in main.store.load_events(lid)), "Merge: its events go into the chosen calendar")
    ok(next(r for r in main.all_rules() if r["id"] == own)["apply"] == [lid], "…and its rules move with them")
    top, _ = main.store.undo_stack()
    post("/history/undo", entry=str(top))
    ok(sid2 in main.source_ids() and not any(x.title == "Lunch" for x in main.store.load_events(lid))
       and next(r for r in main.all_rules() if r["id"] == own)["apply"] == [sid2], "Undo: the calendar, its events and rules are back as they were")
    c.post("/sources/remove", data={"csrf": csrf, "sid": sid2, "keep": "delete"})
    ok(sid2 not in main.source_ids() and own not in [r["id"] for r in main.all_rules()], "Delete: its events and own rules go")
    # the last CalendarStream calendar is emptied, not removed
    c.post("/sources/remove", data={"csrf": csrf, "sid": lid, "keep": "delete"})
    ok(lid in main.source_ids() and main.sources()[0]["id"] == lid and not main.customs_for(lid), "the last CalendarStream calendar is emptied: it stays, on top")
    # CCS+ removed: its sign-in kept (encrypted) only while it can be undone
    main.logins.save_ccs("U123456", "pw12345")
    c.post("/sources/remove", data={"csrf": csrf, "sid": "ccs", "keep": "delete"})
    ok("ccs" not in main.source_ids() and not main.store.get("ccs_login"), "CCS+ removed: its sign-in is forgotten…")
    top, _ = main.store.undo_stack()
    post("/history/undo", entry=str(top))
    ok("ccs" in main.source_ids() and main.logins.ccs()[0] == "U123456", "…but Undo brings it back, sign-in included (kept encrypted meanwhile)")

    # --- Search: All is every date ---------------------------------------------------------------------
    far = TODAY + timedelta(days=700)
    c.post("/event/save", data={"csrf": csrf, "title": "Far future zebra", "start_date": far.isoformat(), "start_time": "9:00",
                                "end_date": far.isoformat(), "end_time": "10:00", "source": lid})
    ok("Far future zebra" in c.get("/?q=zebra", headers={"accept": "text/html"}).text, "Search with All (no dates): every date")

    # --- Google: 1-way, a Gmail of its own, its color, deletions struck through ------------------------------
    main.google.save_client(mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET)
    main.store.set("public_url", "https://cal.example.com")
    def sign_in(url):
        back = G.get(url, follow_redirects=False); cb = urlparse(back.headers["location"])
        c.get(cb.path + "?" + cb.query, follow_redirects=False)
    sign_in(main.google.sign_in_url("https://cal.example.com/google/callback"))
    ok(main.google.connected, "the first Google account connected (Settings)")
    c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Two way"})
    c.post("/destinations/add", data={"csrf": csrf, "type": "google1", "name": "One way"})
    two, one = (next(d for d in main.destinations("google") if d["name"] == n) for n in ("Two way", "One way"))
    ok(one["oneway"] and not two["oneway"], "+ Google 1-way Sync and Google 2-way Sync")
    for d in (two, one):        # (0.2.8-beta.17: a new module has an account of its own; these two go on the first one)
        c.post("/google/account", data={"csrf": csrf, "did": d["id"], "action": "first"})
    two, one = (next(d for d in main.destinations("google") if d["name"] == n) for n in ("Two way", "One way"))
    c.post("/destinations/update", data={"csrf": csrf, "did": two["id"], "name": "Two way", "sources": ["ccs"], "color": "#0b8043"})
    ok(run(main.google_sync_once(True)), "both synced")
    cal2 = main.google.cal_info(two["id"])["calendar_id"]; cal1 = main.google.cal_info(one["id"])["calendar_id"]
    ok(S["calendars"][cal2].get("backgroundColor") == "#0b8043", "a Google module's color is set in Google Calendar")
    # deleted in Google: struck through here (two-way); put back (one-way)
    gid2 = next(iter(k for k, v in S["events"][cal2].items() if v.get("status") != "cancelled"))
    uid2 = S["events"][cal2][gid2]["extendedProperties"]["private"]["uid"]
    S["events"][cal2][gid2]["status"] = "cancelled"; S["events"][cal2][gid2]["updated"] = mockgoogle._now()
    gid1 = next(iter(k for k, v in S["events"][cal1].items() if v.get("status") != "cancelled"     # (another event: the one deleted
                     and v["extendedProperties"]["private"]["uid"] != uid2))                       # in the 2-way calendar goes from every feed)
    S["events"][cal1][gid1]["status"] = "cancelled"; S["events"][cal1][gid1]["updated"] = mockgoogle._now()
    run(main.google_sync_once(True))
    ok(main.store.get_event(uid2).deleted.startswith("google|") and "Deleted in Google Calendar" in page(), "2-way: an event deleted in Google is struck through here")
    gline = next(h for h in main.store.recent_log(10) if h["msg"].startswith("Deleted in Google Calendar"))
    ok(gline["kind"] == "Google" and gline["state"] == "" and main.store.undo_stack()[0] != gline["id"], "…its History line (Google) has no Undo icon: Restore is on the event")
    ok(S["events"][cal1][gid1]["status"] == "confirmed", "1-way: an event deleted in Google is put back")
    # a Gmail of its own
    S["email"] = "second@example.com"
    r = c.post("/google/account", data={"csrf": csrf, "did": one["id"], "action": "connect"}, follow_redirects=False)
    sign_in(r.headers["location"])
    one = next(d for d in main.destinations("google") if d["id"] == one["id"])
    g1 = main.dest_google(one)
    ok(one["account"] and g1.connected and g1.info().get("email") == "second@example.com" and main.google.info().get("email") == "pilot@example.com",
       "a Google module can use a Gmail of its own; the first account stays")
    run(main.google_sync_once(True))
    ok(S["calendars"][g1.cal_info(one["id"])["calendar_id"]]["owner"] == "second@example.com", "…and its calendar is made in that person's Google")
    p = page()
    ok("second@example.com" in p and "Google 1-way Sync" in p and "Google 2-way Sync" in p, "the modules say their kind and account")
    S["email"] = "pilot@example.com"
    # Remove asks: delete it in Google too, or leave it
    c.post("/destinations/remove", data={"csrf": csrf, "did": two["id"], "delete": "1"})
    ok(cal2 not in S["calendars"], "Remove › Yes, and delete it from Google Calendar")

    # --- Signing in: the page's own sign-in page; Basic still works for scripts --------------------------------
    if True:      # (no `with`: a second lifespan would close the database pool)
        b = TestClient(main.app, base_url="https://cal.example.com")
        r = b.get("/", headers={"accept": "text/html"}, follow_redirects=False)
        ok(r.status_code == 303 and r.headers["location"].startswith("/login"), "no login: the sign-in page (not the browser's pop-up)")
        lp = b.get("/login").text; tok = re.search(r'name="csrf" value="([^"]+)"', lp)[1]
        ok(b.post("/login", data={"csrf": tok, "user": "t", "password": "nope"}).status_code == 400, "a wrong password: refused")
        r = b.post("/login", data={"csrf": tok, "user": "t", "password": "password1", "next": "//evil.example/"}, follow_redirects=False)
        ok(r.status_code == 303 and r.headers["location"] == "/" and "cs_session" in r.headers.get("set-cookie", ""), "signed in (a session cookie); never sent to another site")
        ok(main._safe_next("/\t/evil.example/") == "/" and main._safe_next("/?month=2026-10#cal") == "/?month=2026-10#cal", "…nor by a hidden tab (/<tab>/ is // to a browser)")
        ok(b.get("/", headers={"accept": "text/html"}).status_code == 200, "…the page opens")
        b.post("/logout", data={"csrf": main.CSRF_TOKEN}, follow_redirects=False)
        ok(b.get("/", headers={"accept": "text/html"}, follow_redirects=False).status_code == 303, "Sign out")
    ok(c.get("/api/status").status_code == 200, "HTTP Basic still works (scripts)")
    log = c.get("/history/container")
    ok(log.status_code == 200 and log.headers["content-type"].startswith("text/plain"), "History › Container log")

    # --- In a browser: the test box marks the matched part, by characters (an emoji in the title) --------
    #     (the browser's requests are answered by the test client: no second server on the app's loop)
    from playwright.sync_api import sync_playwright
    def answer(route):
        rq = route.request
        r = c.request(rq.method, urlparse(rq.url).path + ("?" + urlparse(rq.url).query if urlparse(rq.url).query else ""),
                      headers={k: v for k, v in rq.headers.items() if k.lower() not in ("host", "content-length")},
                      content=rq.post_data_buffer, auth=A)
        route.fulfill(status=r.status_code, headers={k: v for k, v in r.headers.items() if k.lower() not in ("content-length", "content-encoding")}, body=r.content)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.route("http://cs.test/**", answer)
        pg.goto("http://cs.test/"); pg.wait_for_timeout(500)
        pg.evaluate("document.querySelector('#rules .sfoot .newrule').click()"); pg.wait_for_timeout(200)
        pg.select_option("#ruledialog .cond .cop", "regex"); pg.wait_for_timeout(100)
        pg.eval_on_selector("#ruledialog .rxsamples", "t => { t.value = '✈️ RDO day'; }")
        pg.fill("#ruledialog .cond .cval", "RDO"); pg.wait_for_timeout(1200)
        ok(pg.inner_text("#ruledialog .rxlist mark") == "RDO", f"the test box marks RDO in “✈️ RDO day” ({pg.inner_text('#ruledialog .rxlist')!r})")
        ok(not errs, f"no script errors {errs}")
        b.close()
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
