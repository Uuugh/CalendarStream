"""0.0.13 tests: syncing events to Google, against the mock Google, with the real CCS+ file."""
import asyncio, os, re, sys, threading, time
from datetime import date
from urllib.parse import parse_qs, urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="http://localhost",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(HERE, "data", "Demo.ics")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
import uvicorn, httpx, mockgoogle
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main

M = "http://127.0.0.1:8099"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8099, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, A, G = mockgoogle.S, ("t", "p"), httpx.Client()
GI = lambda: {**main.google.info(), **(main.google.cal_info(main.destinations("google")[0]["id"]) if main.destinations("google") else {})}
async def noop(*a, **k): pass
fails = 0
def ok(c, label):
    global fails
    fails += not c
    print(("PASS " if c else "FAIL ") + label)

def sync(full=False):
    S["calls"].clear()
    r = asyncio.run(main.google_sync_once(full))
    return r, [c for c in S["calls"] if not c.startswith("GET")]

def live():   # events in Google that aren't deleted
    cid = GI()["calendar_id"]
    return {k: v for k, v in S["events"][cid].items() if v["status"] != "cancelled"}

def log(n=3): return [h["msg"] for h in main.store.recent_log(n)]

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), TestClient(main.app) as c:
    page = c.get("/", auth=A).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
    if len(sys.argv) < 3 or sys.argv[2] != "unconfigured":
        r = c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "test-client.apps.googleusercontent.com",
                   "client_secret": "test-secret", "action": "save"}, follow_redirects=False)
        assert r.status_code == 303, r.text
        page = c.get("/", auth=A).text
    c.post("/setup/upload", auth=A, data={"csrf": csrf}, files={"file": ("Calendar.ics", open(REAL, "rb").read())})
    events = main.store.load_events()
    first = main.sync_window_start()
    # 0.2.6: a destination's Start date limits what Google gets (empty = everything); this test keeps the month window
    def set_start(day):
        main.save_destinations([{**d, "start": day} if d["type"] == "google" else d for d in main.destinations()])
    set_start(first.isoformat())
    tz = main.TZ
    in_win = [e for e in events if not e.hidden and gsync.in_window(e, first, tz)]
    print(f"   {len(events)} events, {len(in_win)} from {first} on, {sum(e.free for e in events)} free")
    want = open(REAL, "rb").read().count(b"TRANSP:TRANSPARENT")
    ok(sum(e.free for e in events if e.origin == "united") == want, f"TRANSP:TRANSPARENT read as free ({want})")

    r = c.post("/google/connect", auth=A, data={"csrf": csrf}, follow_redirects=False)
    back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
    c.get(cb.path + "?" + cb.query, auth=A)
    ok(main.google_job.full, "connecting asks for a full sync")

    good, writes = sync(full=True)
    g = live()
    ok(good and len(g) == len(in_win), f"first sync wrote {len(g)} events (expected {len(in_win)})")
    ok(all(c_.startswith("POST") for c_ in writes) and len(writes) == len(in_win), f"first sync: inserts only {[w for w in writes if not w.startswith('POST')][:3]} {len(writes)}")
    ok(f"Google: {len(in_win)} added" in log(1)[0], f"activity log: {log(1)[0]}")
    e0 = in_win[0]; ge = g[gsync.event_id(e0.uid)]
    ok(ge["summary"] == e0.title and ge["description"].endswith("Synced by CalendarStream"), "title and notes")
    ok(ge["reminders"] == {"useDefault": False, "overrides": []}, "no reminders")
    allday = next(e for e in in_win if e.all_day); timed = next(e for e in in_win if not e.all_day)
    ok(g[gsync.event_id(allday.uid)]["start"] == {"date": allday.start[:10]}, f"all-day as dates ({allday.title})")
    ok(g[gsync.event_id(timed.uid)]["start"]["timeZone"] == "America/New_York", f"timed with time zone ({timed.title})")
    ok(all((v["transparency"] == "transparent") == next(e.free for e in in_win if gsync.event_id(e.uid) == k)
           for k, v in g.items()), "free/busy carried over")
    ok(all("colorId" not in v for v in g.values()), "no colors without tags")

    good, writes = sync()
    ok(good and writes == [], "second sync: nothing written")
    good, writes = sync(full=True)
    ok(good and writes == [], "full check with nothing changed: nothing written")

    # Edit, hide, add
    target = next(e for e in in_win if not e.all_day)
    f = main._form_values(target)
    c.post("/event/save", auth=A, data={"csrf": csrf, "uid": target.uid, "title": target.title + " (edited)",
           "start_date": f["start_date"], "start_time": f["start_time"], "end_date": f["end_date"], "end_time": f["end_time"],
           "location": target.location, "description": target.description})
    ok(main.google_job.wake.is_set(), "an edit wakes the Google sync")
    good, writes = sync()
    ok(writes == [f"PUT /calendars/{GI()['calendar_id']}/events/{gsync.event_id(target.uid)}".replace("@", "%40")]
       or (len(writes) == 1 and writes[0].startswith("PUT")), f"edit: one update {writes}")
    ok(live()[gsync.event_id(target.uid)]["summary"].endswith("(edited)"), "edited title in Google")
    hide = next(e for e in in_win if e.all_day and e.uid != target.uid)
    hf = main._form_values(hide)
    c.post("/event/save", auth=A, data={"csrf": csrf, "uid": hide.uid, "title": hide.title, "all_day": "1",
           "start_date": hf["start_date"], "end_date": hf["end_date"], "hidden": "1"})
    good, writes = sync()
    ok(len(writes) == 1 and writes[0].startswith("DELETE") and gsync.event_id(hide.uid) not in live(), "hidden event removed")
    c.post("/event/save", auth=A, data={"csrf": csrf, "title": "Dentist", "start_date": "2026-10-28", "start_time": "14:00",
           "end_date": "2026-10-28", "end_time": "15:00"})
    good, writes = sync()
    dentist = next(v for v in live().values() if v["summary"] == "Dentist")
    ok(len(writes) == 1 and dentist["start"]["dateTime"].startswith("2026-10-28T14:00") and dentist["transparency"] == "opaque",
       "added event created, busy")

    # Tag colors -> Google colorId; and the calendar name follows the status page (F2)
    tag_title = in_win[-1].title.split()[0]
    c.post("/destinations/update", auth=A, data={"csrf": csrf, "did": main.destinations("google")[0]["id"], "name": "My Trips", "sources": ["ccs"]})
    import json
    c.post("/rules/save", auth=A, data={"csrf": csrf, "rule": json.dumps({"conds": [{"type": "text", "op": "word", "value": tag_title}],
           "actions": [{"type": "color", "color": "#d60000"}], "apply": ["ccs"]})})
    good, writes = sync()
    colored = [v for v in live().values() if v.get("colorId")]
    cal = S["calendars"][GI()["calendar_id"]]
    ok(colored and all(v["colorId"] == "11" for v in colored), f"tag '{tag_title}' → Tomato on {len(colored)} events")
    ok(cal["summary"] == "My Trips" and any(w.startswith("PATCH") for w in writes), "calendar renamed in Google")
    ok("calendar renamed" in log(1)[0], f"activity log: {log(1)[0]}")
    ok(gsync.nearest_color_id("#33b679") == "2" and gsync.nearest_color_id("#1e88e5") == "7", "nearest Google color")

    # Changes made by hand in Google: left until a full check, which brings them here (two-way, 0.2.8-beta.10)
    cid = GI()["calendar_id"]
    k1, k2 = list(live())[:2]
    S["events"][cid][k1]["status"] = "cancelled"
    S["events"][cid][k2]["summary"] = "changed by hand"; S["events"][cid][k2]["updated"] = "2099-01-01T00:00:00Z"
    stray = {"id": "stray00001", "status": "confirmed", "summary": "old", "start": {"date": "2026-11-02"},
             "end": {"date": "2026-11-03"}, "transparency": "opaque", "updated": "2026-10-20T00:00:00Z",
             "extendedProperties": {"private": {"calendarstream": "1"}}}
    mine = {**stray, "id": "personal01", "summary": "my own event", "extendedProperties": {}}
    S["events"][cid]["stray00001"] = stray; S["events"][cid]["personal01"] = mine
    good, writes = sync()
    ok(writes == [], "normal sync doesn't look at Google's copy")
    good, writes = sync(full=True)
    ok(k1 not in live() and live()[k2]["summary"] == "changed by hand", "full check: a deletion in Google stays deleted (hidden here), a hand edit stays (an edit here)")
    ok("stray00001" not in live() and "personal01" in live(), "removes CalendarStream's strays, keeps events made by hand (no CalendarStream calendar to put them in)")
    ok("removed" in log(1)[0] and any("was deleted in Google, so it's hidden here" in m for m in log(6)) and any("was changed in Google" in m for m in log(6)), f"activity log: {log(6)}")

    # Next month: October's events stay in Google but aren't tracked any more
    before = set(live())
    set_start("2026-11-01")
    good, writes = sync(full=True)
    set_start(first.isoformat())
    rows = main.store.google_rows(main.destinations('google')[0]['id'])
    ok(writes == [] and set(live()) == before, "month rollover: past events left alone in Google")
    ok(all(r["ends"][:10] >= "2026-11-01" for r in rows.values()), f"…and no longer tracked ({len(rows)} still tracked)")
    good, writes = sync(full=True)
    ok(len(writes) == len(before) - len(rows) - 1 or all(w.startswith(("POST", "PUT")) for w in writes),
       f"back to October: re-tracked ({len(writes)} writes)")
    good, writes = sync(full=True)
    ok(writes == [], "…then steady")

    # Calendar deleted in Google
    del S["calendars"][cid]; del S["events"][cid]
    main.google._access = None
    c.post("/event/save", auth=A, data={"csrf": csrf, "title": "Gym", "start_date": "2026-10-29", "start_time": "07:00",
           "end_date": "2026-10-29", "end_time": "08:00", "source": "ccs"})     # (0.2.8: the default is the Local calendar)
    good, writes = sync()
    new = GI()["calendar_id"]
    ok(good and new != cid and len(live()) == len([e for e in main.store.load_events("ccs") if not e.hidden and gsync.in_window(e, first, tz)]),
       f"calendar deleted in Google: new one made and filled ({len(live())})")
    ok("new one was made" in log(1)[0], f"activity log: {log(1)[0]}")

    # Menu and status line
    p = c.get("/?menu=google", auth=A).text
    ok("Last synced <b>" in p and 'action="/google/sync"' in p and "<span class=\"k\">Google</span>" in p, "menu and status line show the sync")
    r = c.post("/google/sync", auth=A, data={"csrf": csrf}, follow_redirects=False)
    ok(r.status_code == 303 and main.google_job.full, "Sync now asks for a full check")

    # Revoked: one log line, error shown, retried later
    for t in S["refresh"]: S["revoked"].add(t)
    main.google._access = None
    n = len(main.store.recent_log(1000))
    good1, _ = sync(full=True); good2, _ = sync(full=True)
    ok(not good1 and not good2 and len(main.store.recent_log(1000)) == n + 1, "revoked: logged once")
    p = c.get("/", auth=A).text
    ok("Connect again" in p and re.search(r'</svg> error</b>', p) is not None, "revoked: shown in the menu and status line")

    # Disconnect + delete forgets the sync state
    c.post("/google/disconnect", auth=A, data={"csrf": csrf, "delete": "1"})
    ok(main.store.google_rows(main.destinations('google')[0]['id']) == {}, "disconnect + delete forgets what was synced")
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
