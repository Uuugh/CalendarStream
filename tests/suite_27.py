"""0.2.2 tests: the source box after the mockups: header line, Configure, Site Address, built-in rules."""
import os, re, sys
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main
A = ("t", "p"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        patch.object(main, "run_once", noop), TestClient(main.app) as c:
    p = c.get("/", auth=A).text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    post = lambda path, **d: c.post(path, auth=A, data={"csrf": csrf, **d}, follow_redirects=False)
    ok('id="cfg-ccs"' in p and 'id="cfg-ccs" hidden' not in p, "Configure open while setup is needed")
    r = post("/setup/ccs", uid="U123456", password="pw12345", url="https://ccsplus.ual.com/other/link")
    ok(r.status_code == 303 and main.calendar_url() == "https://ccsplus.ual.com/other/link" and main.logins.ccs_configured, "Site Address saved with the login")
    ok(post("/setup/ccs", uid="U123456", password="", url="http://x").status_code == 400, "Site Address must be https://")
    post("/setup/ccs", uid="U123456", password="", url="")
    ok(main.store.get("calendar_url") is None, "an empty Site Address goes back to United's link")
    c.post("/setup/upload", auth=A, data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read().replace(
        b"END:VCALENDAR", b"BEGIN:VEVENT\r\nUID:sick-1\r\nDTSTART;TZID=America/New_York:20261019T000100\r\nDTEND;TZID=America/New_York:20261019T235959\r\nSUMMARY:SCK\r\nEND:VEVENT\r\nEND:VCALENDAR"))})
    p = c.get("/", auth=A).text
    ok(re.search(r'<p class="srcstatus">Last synced <b>[^<]+</b></p>', p) is not None, "0.2.8-beta.5: header: Last synced (time)")
    ok('id="cfg-ccs" hidden' in p, "Configure folded once healthy")
    ok(re.search(r'<svg class="mi arr l"[^>]*>.*?</svg><span class="expandword"><span class="long">Expand for Details or to Edit Configuration</span><span class="short">Expand</span></span><span class="closeword">Close</span><svg class="mi arr r"', p) is not None
       and 'class="statusbox good"' in p and ">Sync Now<" in p, "> Expand < (Close when open), status box with Sync Now")
    ok("Items without an end time" in p and "24-hour events" in p, "the source starts with the two predefined rules")
    import json
    before = main.store.load_events("ccs")
    no_end, day24 = main.all_rules()[:2]
    save = lambda r: post("/rules/save", rule=json.dumps(r))
    r = save({**no_end, "actions": [{"type": "change", "to": "length", "minutes": 120}]})
    ok(r.status_code == 303 and main.all_rules()[0]["actions"][0] == {"type": "change", "to": "length", "minutes": 120}, "built-in rule changed: items without an end time last 2:00")
    ok(post("/rules/delete", id=day24["id"]).status_code == 303 and len(main.all_rules()) == 1, "the 24-hour rule removed")
    after = main.store.load_events("ccs")
    sck = lambda evs: next(e for e in evs if e.title == "SCK")
    ok(sck(before).all_day and not sck(after).all_day, "24-hour events keep their times without it")
    ok(save({**no_end, "conds": [{"type": "length", "op": "is"}], "actions": []}).status_code == 400, "a rule needs a Then")
    save({**no_end, "actions": [{"type": "change", "to": "allday"}]})
    ok(main.all_rules()[0]["actions"][0]["to"] == "allday", "items without an end can be all-day")
print("FAILS", fails)
