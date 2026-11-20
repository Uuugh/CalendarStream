"""0.2.8-beta.10 tests: two-way sync with the Google calendars CalendarStream makes (F5), against the mock
Google: an edit of a CCS+ event made in Google becomes an edit here (CCS+ untouched); an added event's edit
changes it; an event added in Google goes into a CalendarStream (local) calendar; a deletion hides the event;
a rule's events stay read-only; the newest change wins; more than 3 deletions at once wait for a choice.
Also: events added here in their calendar's color (I1), rule lines that say what they do (F4)."""
import asyncio, os, re, sys, threading, time
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="https://cal.example.com", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx, seed
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main
M = "http://127.0.0.1:8114"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8114, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, A = mockgoogle.S, ("t", "p"); G = httpx.Client(); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
run = asyncio.run
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        patch.object(main, "sync_window_start", lambda: datetime(2026, 10, 1).date()), TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d}, follow_redirects=False)
    post("/setup/upload") if False else c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    post("/sources/add", type="local", name="Home")
    L = [x["id"] for x in main.sources() if x["type"] == "local"][0]
    # a rule that makes events (read-only in Google)
    post("/templates", tpl_id="", tpl_title="Drive in", tpl_kind="timed", tpl_duration="1:00", tpl_location="", tpl_color="")
    tid = main.event_templates()[0]["id"]
    seed.rule(c, csrf, "", [seed.text("RDO")], [{"type": "event", "template": tid, "offset": 60, "when": "before_start"}])
    c.post("/google/client", data={"csrf": csrf, "client_id": "test-client.apps.googleusercontent.com", "client_secret": "test-secret", "action": "save"})
    r = c.post("/google/connect", data={"csrf": csrf}, follow_redirects=False)
    back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
    c.get(cb.path + "?" + cb.query, follow_redirects=False)
    ok(main.google.connected, "connected to the mock Google")
    if not main.destinations("google"):
        post("/destinations/add", type="google", name="Flying")
    d = main.destinations("google")[0]
    post("/destinations/update", did=d["id"], name=d["name"], sources=["ccs", L], start="", end="")
    post("/event/save", month="2026-10", title="Dentist", start_date="2026-10-28", start_time="15:00", end_date="2026-10-28", end_time="16:00", source=L)
    ok(run(main.google_sync_once(True)), "first sync")
    cid = main.google.cal_info(d["id"])["calendar_id"]
    E = lambda: S["events"][cid]
    def gid_of(title, origin=None):
        for e in main.store.load_events():
            if e.title == title and (origin is None or e.origin == origin) and e.start[:10] >= "2026-10-01":
                return e.uid, gsync.event_id(e.uid)
        return None, None
    def sync():
        return run(main.google_sync_once(True))
    def later():
        return (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
    united = [e for e in main.store.load_events("ccs") if e.origin == "united" and e.start[:10] >= "2026-10-01" and not e.all_day and gsync.event_id(e.uid) in E()]
    ok(len(united) >= 10, f"CCS+ events are in Google ({len(united)})")

    # 1. an edit of a CCS+ event in Google becomes an edit here (CCS+ untouched)
    u1 = united[0]; g1 = gsync.event_id(u1.uid)
    original = main.united_original(u1.uid, "ccs")
    E()[g1]["summary"] = "Changed in Google"; E()[g1]["location"] = "Gate C71"; E()[g1]["updated"] = later()
    ok(sync(), "sync after an edit in Google")
    ok(main.store.get_edits().get(u1.uid, {}).get("title") == "Changed in Google" and main.store.get_event(u1.uid).location == "Gate C71",
       "F5: the Google edit is now an edit here (title, place)")
    ok(main.united_original(u1.uid, "ccs").title == original.title, "…CCS+'s own event is untouched")
    ok(E()[g1]["summary"] == "Changed in Google" and E()[g1]["status"] == "confirmed", "…and Google keeps it")
    ok(any("was changed in Google; the change is saved here" in h["msg"] for h in main.store.recent_log(20)), "…logged in Activities and Logs")

    # 2. an added event's edit changes it
    du, dg = gid_of("Dentist", "custom")
    E()[dg]["summary"] = "Dentist (moved)"; E()[dg]["start"] = {"dateTime": "2026-10-28T16:00:00-04:00", "timeZone": "America/New_York"}
    E()[dg]["end"] = {"dateTime": "2026-10-28T17:00:00-04:00", "timeZone": "America/New_York"}; E()[dg]["updated"] = later()
    sync()
    ce = main.store.get_event(du)
    ok(ce.title == "Dentist (moved)" and datetime.fromisoformat(ce.start) == datetime.fromisoformat("2026-10-28T16:00:00-04:00"), "F5: an added event changed in Google changes here (title, time)")

    # 3. an event added in Google goes into the CalendarStream calendar
    E()["handmade1"] = {"id": "handmade1", "status": "confirmed", "summary": "Lunch with Sam", "location": "Cafe",
                        "start": {"dateTime": "2026-10-29T12:00:00-04:00"}, "end": {"dateTime": "2026-10-29T13:00:00-04:00"}, "updated": later()}
    sync()
    lunch = [e for e in main.store.load_events(L) if e.title == "Lunch with Sam"]
    ok(len(lunch) == 1 and lunch[0].origin == "custom" and lunch[0].location == "Cafe", "F5: an event added in Google is now in Home (local)")
    ok(E()["handmade1"]["status"] == "cancelled" and E().get(gsync.event_id(lunch[0].uid), {}).get("status") == "confirmed",
       "…and Google has CalendarStream's copy instead (no duplicate)")

    # 4. a deletion hides it here (and it isn't put back)
    u2 = united[1]; g2 = gsync.event_id(u2.uid)
    E()[g2]["status"] = "cancelled"; E()[g2]["updated"] = later()
    sync()
    ok(main.store.get_event(u2.uid).hidden and E()[g2]["status"] == "cancelled", "F5: deleted in Google: hidden here, not put back")

    # 5. a rule's events stay read-only
    ru, rg = gid_of("Drive in", "rule")
    ok(rg in E(), "a rule's event is in Google")
    E()[rg]["summary"] = "Not a drive"; E()[rg]["updated"] = later()
    sync()
    ok(E()[rg]["summary"] == "Drive in" and main.store.get_event(ru).title == "Drive in", "F5: a rule's event changed in Google is put back")
    E()[rg]["status"] = "cancelled"; E()[rg]["updated"] = later()
    sync()
    ok(E()[rg]["status"] == "confirmed", "…and deleted in Google, it comes back")

    # 6. the newest change wins
    u3 = united[2]; g3 = gsync.event_id(u3.uid)
    E()[g3]["summary"] = "Google older"; E()[g3]["updated"] = (datetime.now(timezone.utc) + timedelta(seconds=40)).isoformat().replace("+00:00", "Z")
    time.sleep(1)
    with patch.object(main.store, "changed_at", lambda uid, real=main.store.changed_at: datetime.now(timezone.utc) + timedelta(minutes=10) if uid == u3.uid else real(uid)):
        c.post("/event/save", data={"csrf": csrf, "uid": u3.uid, "month": "2026-10", "title": "Here newer", "start_date": u3.start[:10],
                                    "start_time": u3.start[11:16], "end_date": u3.end[:10], "end_time": u3.end[11:16], "location": "", "description": ""})
        sync()
    ok(main.store.get_event(u3.uid).title == "Here newer" and E()[g3]["summary"] == "Here newer", "F5: both changed, here newer: here wins (Google gets it)")
    ok(any("the newer change, here, was kept" in h["msg"] for h in main.store.recent_log(30)), "…logged")
    u4 = united[3]; g4 = gsync.event_id(u4.uid)
    c.post("/event/save", data={"csrf": csrf, "uid": u4.uid, "month": "2026-10", "title": "Here older", "start_date": u4.start[:10],
                                "start_time": u4.start[11:16], "end_date": u4.end[:10], "end_time": u4.end[11:16], "location": "", "description": ""})
    E()[g4]["summary"] = "Google newer"; E()[g4]["updated"] = "2099-01-01T00:00:00Z"
    sync()
    ok(main.store.get_event(u4.uid).title == "Google newer", "F5: both changed, Google newer: Google wins")

    # 7. (0.2.8-beta.15: replaces the held deletions) events deleted in Google stay struck through here, saying
    #    where, with Restore, however many at once
    many = united[4:8]
    for e in many:
        E()[gsync.event_id(e.uid)]["status"] = "cancelled"; E()[gsync.event_id(e.uid)]["updated"] = later()
    sync()
    ok(all(main.store.get_event(e.uid).hidden and (main.store.get_event(e.uid).deleted or "").startswith("google|") for e in many),
       "F5: 4 deleted in Google at once: deleted here too, marked Deleted in Google Calendar")
    ok(any(h["msg"].startswith("Deleted in Google Calendar:") and h["kind"] == "Google" for h in main.store.recent_log(10)), "…one History line")
    p = c.get("/?month=2026-10").text
    ok("Deleted in Google Calendar" in p and 'action="/event/restore"' in p, "…shown struck through, with Restore")
    post("/event/restore", uid=many[0].uid); sync()
    ok(not main.store.get_event(many[0].uid).hidden and not main.store.get_event(many[0].uid).deleted
       and E()[gsync.event_id(many[0].uid)]["status"] == "confirmed", "Restore: back here, and back in Google")
    ok(all(E()[gsync.event_id(e.uid)]["status"] == "cancelled" for e in many[1:]), "…the others stay deleted")

    # I1: an event added here shows its calendar's color, like Google
    main.store.set(f"calendar_color:{L}", "#33b679")
    p = c.get("/?month=2026-10").text
    m = re.search(r'<details data-uid="' + re.escape(du) + r'" class="([^"]+)"( style="([^"]+)")?', p)
    ok(m and "tint" in m.group(1) and "--cal:#33b679" in (m.group(3) or ""), f"I1: an event added here is in its calendar's color ({m.group(0) if m else None})")
    ok('>Added here</span>' not in p.split('class="legend"')[1][:3000], "…and the key has no 'Added here' color")
    # F4: a titled rule line says what it does
    rid = seed.rule(c, csrf, "Long days", [seed.text("RES")], [{"type": "change", "to": "allday"}])
    p = c.get("/").text
    ok(re.search(r'Long days → Change to all-day', p) is not None, "F4: a titled rule line says what it does")
    # F2: the event's Link icon opens the pop-up at "Linked to"
    e = c.get(f"/event?uid={du}&link=1&embed=1").text
    ok('id="linkbox"' in e and 'class="pairbtns"><a class="pcancel evcancel"' in e, "F2: Link opens the edit pop-up at Linked to; Cancel | Save is the theme's pair")
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
