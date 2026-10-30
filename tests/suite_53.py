"""0.2.8-beta.18 tests, against the mock Google (review #3–#7 of the beta.15 audit): an edit made in Google right
after a sync comes here (#3.1); deletions left over at the write limit say there's more (#3.2); a feed's moved
occurrence keeps its key, and an oversized feed keeps its earliest events (#4.1, #4.2); the limit for all addresses
together says so in History, with the way back (#6.1); the installer takes a pinned version's own files (#6.2); the
import row shows From / To, and a view setting that isn't saved says so (#7.1, #7.2)."""
import asyncio, glob, os, re, sys, threading, time
from datetime import date
from urllib.parse import urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
import uvicorn, mockgoogle, httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import calsync, gsync, main
M = "http://127.0.0.1:8123"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8123, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
S, G = mockgoogle.S, httpx.Client()
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
log = lambda n=15: [h["msg"] for h in main.store.recent_log(n)]

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = ("t", "password1")
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/", headers={"accept": "text/html"}).text)[1]
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    main.google.save_client(mockgoogle.CLIENT_ID, mockgoogle.CLIENT_SECRET)
    with patch.object(main, "api_on", lambda: True):
        c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Flying", "sources": ["ccs"]})
    d = next(x for x in main.destinations("google") if x["name"] == "Flying")
    c.post("/google/account", data={"csrf": csrf, "did": d["id"], "action": "first"})
    r = c.post("/google/connect", data={"csrf": csrf}, follow_redirects=False)
    back = G.get(r.headers["location"], follow_redirects=False); cb = urlparse(back.headers["location"])
    c.get(cb.path + "?" + cb.query, follow_redirects=False)
    asyncio.run(main.google_sync_once(True))
    cal = main.google.cal_info(d["id"])["calendar_id"]
    rows = main.store.google_rows(d["id"])
    uid, row = next((u, r) for u, r in rows.items() if S["events"][cal].get(r["google_id"], {}).get("status") != "cancelled")
    ev = S["events"][cal][row["google_id"]]
    ok(row["remote_updated"] and row["remote_updated"] == ev["updated"], "#3.1: each write keeps Google's own updated time")

    # #3.1: changed in Google seconds after the sync (inside the old 30 s grace)
    ev["summary"] = "Changed in Google right away"; ev["updated"] = mockgoogle._now()
    asyncio.run(main.google_sync_once(True))
    ok(any("was changed in Google" in m for m in log()) and main.store.get_event(uid).title == "Changed in Google right away",
       "#3.1: an edit made in Google right after a sync comes here")

    # #3.2: remote-only events over the write limit
    for i in range(5):
        gid = f"orphan{i:02d}abc"
        S["events"][cal][gid] = {"id": gid, "summary": "orphan", "status": "confirmed", "updated": mockgoogle._now(),
                                 "start": {"dateTime": "2099-01-01T10:00:00Z"}, "end": {"dateTime": "2099-01-01T11:00:00Z"},
                                 "extendedProperties": {"private": {gsync.MARKER: "1"}}}
    with patch.object(gsync, "MAX_WRITES", 2):
        asyncio.run(main.google_sync_once(True))
    left = [g for g in S["events"][cal] if g.startswith("orphan") and S["events"][cal][g].get("status") != "cancelled"]
    ok(len(left) == 3 and any("(more at the next sync)" in m for m in log()), f"#3.2: deletions left at the write limit say there's more ({len(left)} left)")
    asyncio.run(main.google_sync_once(True))
    ok(not [g for g in S["events"][cal] if g.startswith("orphan") and S["events"][cal][g].get("status") != "cancelled"], "#3.2: …and the next sync finishes them")

    # #6.1: the limit for all addresses together
    main._global_failures.clear()
    for i in range(main.GLOBAL_MAX_FAILURES):
        try:
            main._count_failure(f"203.0.113.{i}")
        except Exception:
            pass
    ok(sum("failed sign-ins from many addresses" in m and "container log" in m and "restart CalendarStream" in m for m in log(30)) == 1,
       "#6.1: reaching the limit for all addresses says so once in History, with the way back in")
    # (the Developer's decision, review #6.1) local addresses and the IP the domain points at still get in
    def blocked(ip):
        try:
            main._check_lockout(ip); return False
        except Exception as e:
            return getattr(e, "status_code", 0) == 429
    main._domain_ips.update(at=None, ips=set())
    with patch.object(main.socket, "getaddrinfo", lambda host, port: [(2, 1, 6, "", ("198.51.100.99", 0))]):
        ok(blocked("198.51.100.7"), "#6.1: over the limit, a new outside address waits")
        ok(not blocked("192.168.1.20") and not blocked("10.0.0.5") and not blocked("127.0.0.1") and not blocked("fd00::5"),
           "#6.1: a local address (192.168.x.x, 10.x, this machine, IPv6 local) still gets in")
        ok(not blocked("198.51.100.99"), "#6.1: the IP the public address's domain points at still gets in")
    main._global_failures.clear(); main._domain_ips.update(at=None, ips=set())

# #4.1: a moved occurrence keeps its key (its RECURRENCE-ID), so its edits stay
FEED = b"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:s1
DTSTART:20261101T090000Z
DTEND:20261101T100000Z
RRULE:FREQ=DAILY;COUNT=3
SUMMARY:Daily
END:VEVENT
%s
END:VCALENDAR"""
MOVED = b"""BEGIN:VEVENT
UID:s1
RECURRENCE-ID:20261102T090000Z
DTSTART:20261102T150000Z
DTEND:20261102T160000Z
SUMMARY:Daily moved
END:VEVENT"""
args = ("America/New_York", calsync.Defaults(), "f000001", date(2026, 10, 30), date(2026, 11, 10))
before, _ = calsync.parse_feed(FEED % b"", *args)
after, _ = calsync.parse_feed(FEED % MOVED, *args)
ok([e.uid for e in before] == [e.uid for e in after] and any(e.title == "Daily moved" for e in after),
   "#4.1: an occurrence the feed moves keeps its key")
# #4.2: over the limit, the earliest are kept, whatever the file's order
many = b"\n".join(b"BEGIN:VEVENT\nUID:e%d\nDTSTART:2026%02d%02dT090000Z\nDTEND:2026%02d%02dT100000Z\nSUMMARY:E%d\nEND:VEVENT"
                  % (n, 12 - n // 28, 28 - n % 28, 12 - n // 28, 28 - n % 28, n) for n in range(60))
with patch.object(calsync, "MAX_FEED_EVENTS", 10):
    got, _ = calsync.parse_feed(b"BEGIN:VCALENDAR\nVERSION:2.0\n" + many + b"\nEND:VCALENDAR", "UTC", calsync.Defaults(), "f000002",
                                date(2026, 1, 1), date(2027, 1, 1))
everything, _ = calsync.parse_feed(b"BEGIN:VCALENDAR\nVERSION:2.0\n" + many + b"\nEND:VCALENDAR", "UTC", calsync.Defaults(), "f000002",
                                   date(2026, 1, 1), date(2027, 1, 1))
# (round 2: named outright) the file lists E0 (Dec 28) first and E59 (Oct 25) last; the 10 earliest are E50–E59
earliest = {f"e{n}" for n in range(50, 60)}
ok(len(everything) == 60 and len(got) == 10 and {e.uid.split("/")[1] for e in got} == earliest and [e.uid for e in got] == [e.uid for e in everything[:10]],
   f"#4.2: an oversized feed in reverse order keeps its earliest events (E50–E59 of 60: {sorted(e.title for e in got)})")

# #6.2: a pinned version's own files
inst = open(os.path.join(ROOT, "install.sh")).read()
ok('FILES="https://raw.githubusercontent.com/Uuugh/CalendarStream/v$IMAGE_TAG"' in inst and 'curl -fsSL "$FILES/docker-compose.yml"' in inst
   and '"$REPO/docker-compose.yml"' not in inst, "#6.2: an exact version's install takes docker-compose.yml from that version's tag")
import subprocess
ok(subprocess.run(["bash", "-n", os.path.join(ROOT, "install.sh")]).returncode == 0, "#6.2: install.sh is valid bash")

# #7.1, #7.2
css = "".join(open(f).read() for f in sorted(glob.glob(os.path.join(ROOT, "app", "styles", "*.css"))))  # (beta.20, F12: the stylesheet by area)
ok(".importrow .daterange .fld > span { display:none }" not in css and ".importrow .daterange .fld { display:flex" in css, "#7.1: the import row shows From / To")
js = "".join(open(f).read() for f in sorted(glob.glob(os.path.join(ROOT, "app", "templates", "js", "*.js"))))  # (beta.20, F12: page.js in parts)
sp = js[js.index("function savePref"):js.index("var CSRF")]
ok("if (!r.ok) throw" in sp and "tell(T.prefFailed)" in sp and ".then(then ||" not in sp, "#7.2: a view setting runs its next step only once saved, and says when it isn't")
srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
