"""0.2.8-beta.21 tests, against the mock Google: a calendar color Google refuses (I1): RGB, then the nearest of
Google's calendar colors (colorId), then a full update (PUT); History says once which way Google takes, and that way
is kept and tried first; refused every way: said once with Google's reasons, and the note under the colors."""
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
    main.google_job.wake.clear(); asyncio.run(main.google_sync_once(True))
    cid = g.cal_info(d["id"])["calendar_id"]
    entry = lambda: S["calendars"][cid]
    def recolor(color, refuse):
        S["refuse_color"] = refuse; S["calls"].clear()
        c.post("/destinations/update", data={"csrf": csrf, "did": d["id"], "name": "Flying", "sources": ["ccs"], "color": color})
        done = asyncio.run(main.google_sync_once(True))
        S["refuse_color"] = False
        return done
    said = lambda: next((m for m in log() if "color" in m and "Google Calendar" in m), "")
    patches = lambda: sum(x.startswith("PATCH /users/me/calendarList") for x in S["calls"])
    puts = lambda: sum(x.startswith("PUT /users/me/calendarList") for x in S["calls"])

    # --- the nearest calendar color -----------------------------------------------------------------------------------
    ok(len(gsync.CALENDAR_COLORS) == 24 and gsync.nearest_calendar_color("#4986e7") == "16"
       and gsync.nearest_calendar_color("#d50000") == "3", "I1: the nearest of Google's 24 calendar colors")

    # --- RGB taken: said once ------------------------------------------------------------------------------------------
    ok(recolor("#d50000", False) and entry().get("backgroundColor") == "#d50000", "I1: the RGB color, when Google takes it")
    ok(said().endswith("color set in Google Calendar as its RGB color; that way is kept"), "I1: History says which way, once")
    ok(g.cal_info(d["id"]).get("color_way") == "rgb", "I1: …and keeps it")
    recolor("#e67c73", False)
    ok(said().endswith("Flying: color set in Google Calendar") or said().endswith("Google: color set in Google Calendar"),
       "I1: the next color doesn't say it again")

    # --- RGB refused: the nearest calendar color -----------------------------------------------------------------------
    ok(recolor("#039be5", {"rgb"}), "I1: a refused RGB color doesn't fail the sync")
    near = gsync.nearest_calendar_color("#039be5")
    ok(entry().get("colorId") == near and not entry().get("backgroundColor"), "I1: …the nearest calendar color (colorId) is set")
    ok(f"as the nearest of Google's calendar colors ({gsync.CALENDAR_COLORS[near]}); that way is kept" in said()
       and "couldn't be set" not in said(), "I1: History says so, with the color Google shows")
    ok(g.cal_info(d["id"]).get("color_way") == "colorId" and "palnote" not in module(d["id"]), "I1: kept; no note under the colors")
    recolor("#3f51b5", {"rgb"})
    ok(patches() == 1 and entry().get("colorId") == gsync.nearest_calendar_color("#3f51b5"),
       "I1: the next color goes the kept way first (RGB isn't tried again)")
    ok("that way is kept" not in said() and "nearest of Google's calendar colors" in said(), "I1: …and the way isn't said again")

    # --- RGB and colorId refused: a full update ------------------------------------------------------------------------
    ok(recolor("#33b679", {"rgb", "colorId"}), "I1: a refused colorId doesn't fail the sync")
    put = S["list_put"] or {}
    ok(entry().get("backgroundColor") == "#33b679" and puts() == 1, "I1: …a full update (PUT) sets the color")
    ok(put.get("defaultReminders") == [{"method": "popup", "minutes": 30}] and put.get("selected") is True
       and "colorId" not in put and "etag" not in put, "I1: …starting from Google's own entry, so nothing else in it changes")
    ok("with a full update of the calendar's entry; that way is kept" in said(), "I1: History says so")
    ok(g.cal_info(d["id"]).get("color_way") == "put", "I1: …and keeps it")
    S["list_put"] = None
    recolor("#f6bf26", {"rgb", "colorId", "get"})
    put = S["list_put"] or {}
    ok(put.get("backgroundColor") == "#f6bf26" and put.get("selected") is True and put.get("hidden") is False,
       "I1: Google's entry refused: the full update still shows the calendar (selected, not hidden)")
    ok(patches() == 0, "I1: …the kept way first")

    # --- every way refused --------------------------------------------------------------------------------------------
    ok(recolor("#f4511e", True), "I1: every way refused: the sync still succeeds")
    w = said()
    ok("couldn't be set in Google Calendar: it refused the RGB color, the nearest calendar color and a full update" in w
       and "HTTP 401 authError" in w and "Invalid Credentials" in w and w.count("Request had invalid") == 2 and "refused PUT" in w,
       "I1: History says all three were refused, with Google's own reasons (the same one said once)")
    ok(not g.info().get("last_error"), "I1: …and the module stays healthy")
    ok('class="palnote">Color change does not carry to Google<' in module(d["id"]), "I1: the note under the colors")
    recolor("#f4511e", False)
    ok(patches() == 0 and puts() == 0, "I1: a refused color isn't tried again")
    recolor("#0b8043", False)
    ok(entry().get("backgroundColor") == "#0b8043" and "palnote" not in module(d["id"]),
       "I1: a new color Google takes: the note goes")

    # --- Google out of reach: tried again later, not called refused -----------------------------------------------------
    real = g.api
    async def unreachable(*a, **k): raise gsync.GoogleError("Couldn't reach Google Calendar (ConnectError).")
    g.api = unreachable
    try:
        asyncio.run(g.set_color(d["id"], "#e67c73")); ok(False, "unreachable")
    except gsync.GoogleError as e:
        ok("Couldn't reach" in str(e), "I1: Google out of reach: no other way is tried")
    g.api = real
    ok(g.cal_info(d["id"]).get("color_tried") != "#e67c73", "I1: …and the color isn't marked as refused")
    with patch.object(gsync.Google, "set_color", unreachable):
        c.post("/destinations/update", data={"csrf": csrf, "did": d["id"], "name": "Flying", "sources": ["ccs"], "color": "#e67c73"})
        n = len([m for m in log(60) if "color couldn't be set" in m])
        ok(asyncio.run(main.google_sync_once(True)), "I1: Google out of reach during the color: the sync goes on")
        ok(len([m for m in log(60) if "color couldn't be set" in m]) == n and g.cal_info(d["id"]).get("color_tried") != "#e67c73",
           "I1: …nothing said about the color, and it's tried again at the next sync")

srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
