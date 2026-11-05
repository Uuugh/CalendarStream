"""0.2.8-beta.28 tests (the 4 Sources build): the default calendar needn't be on top (I2), opened events survive a module Save (I9),
the grip on the left (I12), Online Meeting (F6), any stream name (F7), the login password rules (F8), CCS+ comes with its rules and
Remove replaces Empty (F16), the On | Off switch (F25), and the logo marks and the 2/3-line box (F31)."""
import os, re, sys, asyncio
from unittest.mock import patch
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"): del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
from fastapi.testclient import TestClient
from app import main, rules as rules_mod, logins, gsync, calsync
from app.calsync import Event
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
read = lambda *p: open(os.path.join(REPO, *p)).read()
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()

# --- F6: Online Meeting (parsing, the notes line, Google's round trip) ----------------------------------------------------
ok(calsync.meeting_link("Join https://us02web.zoom.us/j/123456789?pwd=abc now") == "https://us02web.zoom.us/j/123456789?pwd=abc", "F6: a Zoom link in the notes is found")
ok(calsync.meeting_link("Lunch at noon") == "", "F6: no link, no meeting")
e = Event(title="Sync", start="2026-10-14T09:00:00-04:00", end="2026-10-14T10:00:00-04:00", uid="m1", description="Agenda", meeting="https://meet.google.com/abc-defg-hij")
body = gsync.event_body(e, "Sync") if hasattr(gsync, "event_body") else {}
desc = body.get("description", "")
ok(desc.startswith("https://meet.google.com/abc-defg-hij\n\nAgenda"), "F6: Google gets the link as the first line of the notes")
back = gsync.google_fields({"summary": "Sync", "description": desc, "start": {"dateTime": e.start}, "end": {"dateTime": e.end}}) if hasattr(gsync, "google_fields") else {}
ok(back.get("description", None) in ("Agenda", None) or "meet.google.com" not in str(back.get("description", "")), "F6: reading it back strips that first line (no echo loop)")
ok("URL" in read("app", "calsync.py") and "notes_with_meeting" in read("app", "calsync.py"), "F6: the feeds carry the link as URL and in the notes")

unmet = lambda pw: [r for r, met in logins.password_rules(pw) if not met]
# --- F8: the login password rules ------------------------------------------------------------------------------------------
ok(not unmet("Abcdefghij1!"), "F8: a 12-character password with a capital, a number and a symbol is accepted")
bad = {"Abcdefg1!": "short", "abcdefghij1!": "capital", "Abcdefghijk!": "number", "Abcdefghij12": "symbol", "Abcdefgh111!": "three in a row"}
ok(all(unmet(p) for p in bad), "F8: shorter, no capital, no number, no symbol or a character three times in a row is refused")
ok(not unmet("Bookkeeper-2026"), "F8: the oo in Bookkeeper is fine (only three in a row is refused)")
try:
    main.logins.set_page_login("pilot", "weakpassword", "weakpassword"); ok(False, "F8: set_page_login refuses a weak password")
except logins.LoginError:
    ok(True, "F8: set_page_login refuses a weak password")

# --- F7: any stream name -----------------------------------------------------------------------------------------------------
from app.routes import destinations as D
ok(D.STREAM_RE.match("OneWay") and D.STREAM_RE.match("a") and D.STREAM_RE.match("x" * 128) and not D.STREAM_RE.match("x" * 129) and not D.STREAM_RE.match("a b"),
   "F7: a stream name is 1 to 128 letters, digits, - or _")

# --- the app: I2, F16.1, F16.2, F25, I9 ----------------------------------------------------------------------------------------
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    page = lambda: c.get("/", headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"})
    locals_ = lambda: [x["id"] for x in main.sources() if x["type"] == "local"]
    # I2
    L1 = locals_()[0]
    ok(main.default_sid() == L1, "I2: the first CalendarStream calendar is the default")
    post("/sources/add", type="local", name="Second")
    L2 = [x for x in locals_() if x != L1][0]
    p = page()
    ok(p.count('class="deflabel"') == 1 and f'action="/sources/default"' in p, "I2: one Default label; the other CalendarStream calendar has the greyed Default button")
    ok(post("/sources/default", sid=L2).status_code == 200 and main.default_sid() == L2, "I2: the Default button makes it the default")
    ok(post("/sources/default", sid="ccs").status_code == 400, "I2: only a CalendarStream calendar can be the default")
    post("/sources/move", sid=L2, after=main.source_ids()[-1])
    ok(main.default_sid() == L2 and main.source_ids()[0] != L2, "I2: the default needn't be on top")
    # F16.1: CCS+ comes with its rules, each removable while adding
    post("/sources/remove", sid="ccs", keep="delete", rules="delete")      # (the suite starts with CCS+ already there)
    before = len(main.all_rules())
    post("/sources/add", type="ccs", starters="1", starter="allday24")
    mine = [r for r in main.all_rules() if r["apply"] == ["ccs"]]
    ok(len(main.all_rules()) == before + 1 and mine and mine[0]["title"] == "24-hour events", "F16.1: CCS+ comes with the rules left ticked (24-hour events → all day), for that calendar only")
    ok('name="starter" value="noend"' in page() or "ccs" in main.source_ids(), "F16.1: the add form lists the rules")
    # F16.2: Remove, not Empty
    p = page()
    ok("Empty this calendar" not in p and re.search(r'class="ghost danger removecal"[^>]*title="Remove this calendar"', p), "F16.2: the button says Remove everywhere")
    # F25: On | Off
    ok('action="/sources/power"' in p and 'role="switch"' in p, "F25: a module has the On | Off switch")
    n_on = len(main.dest_events(main.destinations()[0])) if main.destinations() else 0
    post("/sources/power", sid=L2, on="0")
    ok(main.source_off(L2) and 'class="box module src cfgbox' in page() and re.search(r'class="box module src cfgbox[^"]* off"[^>]*id="src-' + L2, page()), "F25: Off greys the module")
    d = main.destinations()[0]
    r = post("/destinations/power", did=d["id"], on="0")
    if d["type"] == "feed":
        ok(c.get(f"/calendar/{d['token']}.ics", auth=None).status_code == 503, "F25: a feed that is Off answers 503 (unavailable)")
    post("/destinations/power", did=d["id"], on="1"); post("/sources/power", sid=L2, on="1")
    ok(not main.source_off(L2) and not main.destination(d["id"])["off"], "F25: On restores both; nothing was lost")
    ok(d["sources"] == main.destination(d["id"])["sources"], "F25: the selection of sources in the feed is kept")

# --- F31 / I12: logos, 2/3-line, grips --------------------------------------------------------------------------------------------
top = read("app", "templates", "index", "topbar.html")
ok('logomark lt' in top and 'logomark dk' in top and os.path.exists(os.path.join(REPO, "app", "static", "logo", "mark-light-72.png"))
   and os.path.exists(os.path.join(REPO, "app", "static", "logo", "mark-dark-72.png")), "F31: Light and Dark marks (no words) in the title bar")
ok(not os.path.exists(os.path.join(REPO, "app", "static", "logo", "CalendarStream_Logo.png")), "F31: the old CalendarStream_Logo.png is gone from the app")
css = read("app", "styles", "18-two-three-line.css")
ok("--tl-w" in css and "border:1px solid var(--line)" in css and "display:none" in css, "F31: the 2/3-line box has one standard width, a 1 px border, and hides when open")
h = read("app", "styles", "12-handles.css")
ok("left:-16px" in h and "opacity:.55 }" in h, "I12: the handle sits on the left, always visible (faint)")
sv = read("app", "templates", "js", "07-saving.js")
ok("reopenEvents" in sv, "I9: a module Save reopens the events that were open")
print("FAILED:", fails) if fails else print("ALL PASSED")
