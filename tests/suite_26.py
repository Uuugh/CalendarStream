"""0.2.0 tests: calendar sources and destinations (F1), the public address on the first destination
(F2), rules and event templates (F3), stream names (F4); against the mock Google. Runs on a fresh install."""
import asyncio, os, re, sys, threading, time
from urllib.parse import urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import calsync, gsync, main
M = "http://127.0.0.1:8099"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8099, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, A = mockgoogle.S, ("t", "p"); G = httpx.Client(); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    return calsync.Download(200, body=FEED, debug={"url": url})
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        patch.object(main, "download", fake_download), TestClient(main.app, base_url="https://cal.example.com") as c:
    p = c.get("/", auth=A).text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    post = lambda path, **d: c.post(path, auth=A, data={"csrf": csrf, **d}, follow_redirects=False)
    # F1: a new install starts with only its Local calendar (0.2.8, F3.2) and no destinations
    L = main.source_ids()[0] if main.sources() else ""
    ok([x["type"] for x in main.sources()] == ["local"] and main.calendar_name(L) == "Local" and main.destinations() == [], "fresh install: a Local calendar, no destinations")
    ok("No feeds yet" in p and 'id="src-ccs"' not in p and f'id="src-{L}"' in p, "Local shown; Feeds say how to add one")
    ok(c.get("/event?date=2026-10-12", auth=A).status_code == 200, "adding an event goes to Local")
    ok(c.get(f"/calendar/{main.settings.feed_token}.ics").status_code == 404, "no feed without the feed destination")
    # Sources
    ok(post("/sources/add", type="ccs").status_code == 303 and main.source_ids() == [L, "ccs"], "+ United CCS+")
    ok(post("/sources/add", type="ccs").status_code == 400, "CCS+ only once")
    ok(post("/sources/add", type="ics", url="http://x.org/a.ics").status_code == 400, "a feed must be https:// (or webcal://)")
    r = post("/sources/add", type="ics", url="webcal://example.org/work.ics", name="Work")
    sid = main.source_ids()[2]
    ok(r.status_code == 303 and main.source(sid)["url"] == "https://example.org/work.ics" and main.calendar_name(sid) == "Work", "+ feed: webcal:// read as https://, named")
    ok(post("/sources/add", type="ics", url="https://example.org/work.ics").status_code == 400, "the same feed only once")
    asyncio.run(main.run_feed(sid))
    ev = main.store.load_events(sid)
    union = [e for e in ev if e.title == "Union meeting"]
    ok(len(union) == 8 and len({e.uid for e in union}) == 8 and all(e.uid.startswith(sid + "/") for e in ev), f"repeating events expanded, unique IDs ({len(union)})")
    ok(main.st(sid).status == "ok" and main.store.load_events("ccs") == [], "feed events kept apart from CCS+'s")
    p = c.get("/?month=2026-10", auth=A).text
    ok('id="src-ccs"' in p and f'id="src-{sid}"' in p and "Union meeting" in p, "both sources shown, events on the calendar")
    ok(p.index('id="src-ccs"') < p.index('action="/setup/ccs"') < p.index('name="url" type="url"') < p.index("How to get a Calendar Sync link, ID and secret") < p.index('action="/setup/upload"'),
       "Configure: Site Address and login, upload beside it, then the help")
    # F3: templates and rules
    ok(post("/templates", tpl_id="", tpl_title="Prep", tpl_kind="timed", tpl_duration="0:45", tpl_location="Desk", tpl_color="#616161").status_code == 303, "template saved")
    t = main.event_templates()[0]
    ok(t["minutes"] == 45 and t["color"] == "#616161" and t["location"] == "Desk", "template: length, color, location")
    ok(post("/templates", tpl_id="", tpl_title="Bad", tpl_kind="timed", tpl_duration="x", tpl_location="", tpl_color="").status_code == 400, "a bad length is refused")
    ok([main.parse_duration(x) for x in ("1:30", "2", "1.5", "90m", "1h15")] == [90, 120, 90, 90, 75], "lengths: 1:30, 2, 1.5, 90m, 1h15")
    import seed; c.auth = A
    seed.rule(c, csrf, "", [seed.text("Union")], [{"type": "event", "template": t["id"], "when": "before_start", "offset": 60}], [sid])
    seed.rule(c, csrf, "", [seed.text("Columbus")], [{"type": "color", "color": "#d50000"}], [sid])
    rules = main.source_rules(sid)
    ok([x["actions"][0]["type"] for x in rules][:2] == ["event", "color"] and rules[0]["actions"][0]["offset"] == 60, "rules saved: add event 1:00 before, color")
    made = [e for e in main.store.load_events(sid) if e.origin == "rule"]
    first = min(made, key=lambda e: e.start) if made else None
    ok(len(made) == 8 and first.start == "2026-10-06T09:00:00-04:00" and first.end == "2026-10-06T09:45:00-04:00" and first.location == "Desk",
       f"8 Prep events, 1:00 before each meeting, 45 min ({first.start if first else ''})")
    ok(main.store.load_events("ccs") == [], "rules only apply to their own source")
    from urllib.parse import quote
    ok(c.get(f"/event?uid={quote(first.uid, safe='')}", auth=A).status_code == 400, "rule-made events can't be edited")
    # 0.2.8: one list of rules (All Rules); each applies to All calendars or to the ones chosen
    union = seed.rule(c, csrf, "", [seed.text("Union")], [{"type": "color", "color": "#0b8043"}], ["ccs"])
    ids = lambda x: [r["id"] for r in main.source_rules(x)]
    ok(union in ids("ccs") and union not in ids(sid), "a rule for CCS+ only: Work doesn't use it")
    ok(post("/rules/apply", id=union, sid=sid, on="1").status_code == 303 and union in ids(sid), "Add a rule → an existing rule: Work uses it too")
    ok(post("/rules/apply", id=union, sid=sid, on="0").status_code == 303 and union not in ids(sid) and union in ids("ccs"), "the bin takes it off Work only")
    reds = [e for e in main.store.load_events(sid) if e.title.startswith("Columbus")]
    ok(reds and all(main.event_colorer()(e) == "#d50000" for e in reds), "the color rule colors Work's events")
    bad = c.post("/rules/save", auth=A, data={"csrf": csrf, "rule": '{"conds": [], "actions": [{"type": "event", "template": "nope"}], "apply": "all"}'}, follow_redirects=False)
    ok(bad.status_code == 400, "an Add event rule needs an event template (or a new event's title)")
    p = c.get("/?month=2026-10", auth=A).text
    ok("All Rules" in p and "Tag Colors" not in p and 'id="ruledialog"' in p and p.count('class="ghost unapply"') >= 4 and p.count('class="linkbtn newrule"') >= 3,
       "All Rules; each calendar's rules with a bin, and + Add a rule → New rule…")
    ok(p.count('<use href="#mi-delete"') >= 3, "the bin is an icon")
    e = c.get("/event?date=2026-10-12", auth=A).text
    ok('<select id="source" name="source"' in e and 'id="template"' in e and 'data-title="Prep"' in e, "event page: which calendar, and Start from a template")
    r = post("/event/save", title="Lunch", start_date="2026-10-12", start_time="12:00", end_date="2026-10-12", end_time="13:00", source=sid)
    ok(r.status_code == 303 and any(x.title == "Lunch" and x.origin == "custom" for x in main.store.load_events(sid)), "an added event goes into the chosen calendar")
    # Destinations: independent of sources, each with its own list; the first asks for the public address
    p = c.get("/", auth=A).text
    ok('name="public" value="https://cal.example.com"' in p and "(☰ Settings changes it later)" in p, "the first destination asks for the public address (this page filled in)")
    ok(post("/destinations/add", type="feed", name="Everything", public="cal.example.com").status_code == 303
       and main.public_url() == "https://cal.example.com", "+ feed, public address saved")
    every = main.destinations("feed")[0]
    ok(every["name"] == "Everything" and every["sources"] == [L, "ccs", sid] and len(every["token"]) >= 16, "a new destination gets every source")
    p = c.get("/", auth=A).text
    ok('name="public"' not in p, "not asked again once set")
    f = c.get(f"/calendar/{every['token']}.ics")
    ok(f.status_code == 200 and f.text.count("BEGIN:VEVENT") == 9 + 8 + 1 and "X-WR-CALNAME:Everything" in f.text, f"its feed has its sources' events ({f.text.count('BEGIN:VEVENT')})")
    post("/destinations/add", type="feed", name="Work only")
    work = main.destinations("feed")[1]
    ok(post("/destinations/update", did=work["id"], name="Work only", sources=[sid]).status_code == 303
       and main.destination(work["id"])["sources"] == [sid], "a second feed with only Work")
    ok(c.get(f"/subscribe/{work['token']}").status_code == 200 and "Work only" in c.get(f"/subscribe/{work['token']}").text, "each feed has its own subscribe page")
    # Stream names
    ok(post("/feed/stream", did=work["id"], stream="short").status_code == 400, "a stream name is at least 16 characters")
    ok(post("/feed/stream", did=work["id"], stream=every["token"]).status_code == 400, "not one another feed uses")
    ok(post("/feed/stream", did=work["id"], stream="https://cal.example.com/calendar/MyOldStreamName_123456.ics").status_code == 303
       and main.destination(work["id"])["token"] == "MyOldStreamName_123456", "a pasted old link sets the stream name")
    ok(c.get("/calendar/MyOldStreamName_123456.ics").status_code == 200 and c.get(f"/calendar/{work['token']}.ics").status_code == 404, "old links work again; the replaced one stops")
    # Google: several calendars, each with its own sources
    # (0.2.8-beta.4: + Google Calendar is a Google calendar once Google Calendar sync is set up in Settings)
    c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "test-client.apps.googleusercontent.com", "client_secret": "test-secret", "action": "save"})
    post("/destinations/add", type="google", name="Flying")
    flying = main.destinations("google")[0]
    post("/destinations/update", did=flying["id"], name="Flying", sources=["ccs"])
    post("/destinations/add", type="google", name="All of it")
    allofit = main.destinations("google")[1]
    for d in (flying, allofit):       # (0.2.8-beta.17: a new module has an account of its own; these two go on the first one)
        post("/google/account", did=d["id"], action="first")
    flying, allofit = main.destinations("google")
    r = post("/google/connect")
    back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
    c.get(cb.path + "?" + cb.query, auth=A, follow_redirects=False)
    ok(main.google.connected and len(S["calendars"]) == 2, f"connecting makes a calendar for each Google destination ({len(S['calendars'])})")
    ok(asyncio.run(main.google_sync_once(True)), "sync")
    cal_f, cal_a = main.google.cal_info(flying["id"])["calendar_id"], main.google.cal_info(allofit["id"])["calendar_id"]
    ok(S["calendars"][cal_f]["summary"] == "Flying" and S["calendars"][cal_a]["summary"] == "All of it", "named after their destinations")
    rows_f, rows_a = main.store.google_rows(flying["id"]), main.store.google_rows(allofit["id"])
    ok(not any(u.startswith(sid) for u in rows_f) and any(u.startswith(sid) for u in rows_a), f"Flying has no Work events; All of it has them ({len(rows_f)}, {len(rows_a)})")
    colored = [ev for ev in S["events"].get(cal_a, {}).values() if ev.get("summary") == "Columbus Day"]
    ok(colored and colored[0].get("colorId") == "11", "a source's rule colors its events in every destination")
    post("/destinations/update", did=allofit["id"], name="Everything (Google)", sources=["ccs", sid])
    asyncio.run(main.google_sync_once(False))
    ok(S["calendars"][cal_a]["summary"] == "Everything (Google)", "renaming a destination renames its Google calendar")
    p = c.get("/", auth=A).text
    ok('id="googlesync"' in p and p.count('class="box module cfgbox dest') == 4, "Google Calendar API Sync in Settings, four destination boxes")
    # Removing a source takes it off every list; calendars stay
    r = post("/sources/remove", sid=sid)
    ok(r.status_code == 303 and main.source_ids() == [L, "ccs"] and main.store.event_count(sid) == 0, "source removed with its events")
    ok(cal_a in S["calendars"] and all(sid not in d["sources"] for d in main.destinations()), "its destinations keep their calendars, without it")
    # Removing destinations
    ok(post("/destinations/remove", did=work["id"]).status_code == 303 and c.get("/calendar/MyOldStreamName_123456.ics").status_code == 404, "removing a feed stops its links")
    post("/destinations/remove", did=flying["id"])
    ok(cal_f in S["calendars"] and not main.google.cal_info(flying["id"]), "removing a Google destination keeps its calendar in Google by default")
    post("/destinations/remove", did=allofit["id"], delete="1")
    ok(cal_a not in S["calendars"], "… or deletes it when asked")
    st = c.get("/api/status", auth=A).json()
    ok([x["id"] for x in st["sources"]] == [L, "ccs"] and [d["name"] for d in st["destinations"]] == ["Everything"], "/api/status lists sources and destinations")
    # Events: duplicate and delete
    main.store.set("ccs_login", {"uid": "U1", "password": main.box.seal("x")}); main.logins._ccs = None
    c.post("/setup/upload", auth=A, data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    one = main.store.load_events("ccs")[0]
    from urllib.parse import quote as q_
    e = c.get(f"/event?copy={q_(one.uid, safe='')}", auth=A).text
    ok("Duplicate event" in e and f'value="{one.title}"' in e and 'name="uid" value=""' in e, "Duplicate opens a new event filled in from it")
    p = c.get(f"/?date={one.start[:10]}", auth=A).text
    ok('class="evicon"' in p and 'action="/event/delete"' in p, "the event details have Duplicate and Delete icons")
    ok(post("/event/delete", uid=one.uid).status_code == 303 and main.store.get_event(one.uid).hidden, "deleting a source's event hides it (it would come back)")
    lunch = next(x for x in main.store.load_events() if x.title == "Lunch") if any(x.title == "Lunch" for x in main.store.load_events()) else None
    post("/event/save", title="Coffee", start_date="2026-10-13", start_time="9:00", end_date="2026-10-13", end_time="9:30", source="ccs")
    coffee = next(x for x in main.store.load_events("ccs") if x.title == "Coffee")
    gone = lambda: main.store.get_event(coffee.uid)
    ok(post("/event/delete", uid=coffee.uid).status_code == 303 and (gone() is None or (gone().deleted or "").startswith("calendarstream|")),
       "deleting an added event deletes it (0.2.8-beta.15: struck through, with Restore, until its Undo is forgotten)")
    # Calendar views
    for v, mark in (("week", 'class="month weekgrid"'), ("day", 'class="agenda"'), ("list", 'class="agenda"'), ("month", 'class="month"')):
        c.post("/ui/view", auth=A, data={"csrf": csrf, "view": v})
        p = c.get("/?date=2026-10-14", auth=A).text
        ok(main.ui_view() == v and mark in p and f'data-view="{v}" aria-pressed="true"' in p, f"view: {v}")
    c.post("/ui/view", auth=A, data={"csrf": csrf, "view": "week"})
    p = c.get("/?date=2026-10-14", auth=A).text
    ok("Sun Oct 11 – Sat Oct 17, 2026" in p and 'href="?date=2026-10-07"' in p and 'href="?date=2026-10-21"' in p, "week: title and ‹ › by a week")
    c.post("/ui/view", auth=A, data={"csrf": csrf, "view": "month"})
    head = p[p.index('class="calhead"'):p.index('class="scroll"')]
    ok("times in" not in head and " events ·" not in head and head.index('id="tzpick"') < head.index('class="viewseg"') < head.index('id="clockswitch"'), "header: no event count; time zone, view, 12/24 on the right")
    order = [p.index(x) for x in ('id="cal"', 'id="sources"', 'id="destinations"', 'id="rules"', 'id="templates"', 'id="activity"')]
    ok(order == sorted(order), "sections: Calendar, Sources, Destinations, Rules (with event templates), Activity")
    # An install from before 0.2 keeps CCS+, the feed and Google Autosync
    main.store.set("ccs_login", {"uid": "U1", "password": main.box.seal("x")}); main.logins._ccs = None
    main.store.delete("sources"); main.store.delete("destinations")
    main.migrate_sources()
    main.store.set("google", {"calendar_id": "old-cal", "calendar_name": "United CCS Schedule", "synced_calendar": "old-cal"})
    main.store.google_saved("u1", "g1", "h", "2030-01-01", "ccs")
    main.migrate_destinations()
    ds = main.destinations()
    ok(main.source_ids() == ["ccs"] and [d["type"] for d in ds] == ["feed", "google"] and all(d["sources"] == ["ccs"] for d in ds), f"upgrade: CCS+ source; a feed and a Google calendar with it ({[d['type'] for d in ds]})")
    ok(ds[0]["token"] == main.settings.feed_token and main.google.cal_info(ds[1]["id"]).get("calendar_id") == "old-cal"
       and "u1" in main.store.google_rows(ds[1]["id"]) and not main.google.info().get("calendar_id"), "upgrade keeps the feed links and the Google calendar")
print("FAILS", fails)
srv.should_exit = True
