"""0.2.6 tests: destination dates (F4), rules moved into the Rules section (migration), title link (F1)."""
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
    ok(f'/releases/tag/v{main.__version__}"' in p, "F1.2: the version links to its release notes")
    c.post("/setup/upload", auth=A, data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    feed = main.destinations("feed")[0]
    every = c.get(f"/calendar/{feed['token']}.ics").text.count("BEGIN:VEVENT")
    r = post("/destinations/update", did=feed["id"], name=feed["name"], sources=["ccs"], start="2026-10-10", end="2026-10-20")
    some = c.get(f"/calendar/{feed['token']}.ics").text.count("BEGIN:VEVENT")
    ok(r.status_code == 303 and main.destination(feed["id"])["start"] == "2026-10-10" and 0 < some < every, f"F4: only events in its dates ({some} of {every})")
    ok(post("/destinations/update", did=feed["id"], name=feed["name"], sources=["ccs"], start="2026-10-20", end="2026-10-10").status_code == 400, "F4: the end can't be before the start")
    post("/destinations/update", did=feed["id"], name=feed["name"], sources=["ccs"], start="", end="")
    ok(c.get(f"/calendar/{feed['token']}.ics").text.count("BEGIN:VEVENT") == every, "F4: empty dates = no limit")
    p = c.get("/", auth=A).text
    ok('name="start"' in p and 'name="end"' in p and 'class="rangeall"' in p, "F4: Start and End in the destination box (0.2.8-beta.15: with All)")
    # A 0.2.5 install: a source's own rules, a ticked rule template and its built-in settings
    main.store.set("calendar_tags", [{"id": "r1", "tag": "RDO", "color": "#d50000", "mode": "word", "case": False, "action": "color"}])
    main.store.set("rule_templates", [{"id": "t9", "tag": "VAC", "color": "#0b8043", "mode": "word", "case": False, "action": "color"}])
    main.store.set("rule_subs", ["t9"])
    main.store.set("defaults", {"mode": "hours", "hours": 2, "allday_24h": False})
    main.store.delete("rules_v3"); main.store.delete("rules")
    main.migrate_rules()
    eff = main.source_rules("ccs")
    words = [main.rule_label(r) for r in eff]
    ok(len(eff) == 3 and "“RDO” → Color (Tomato)" in words[0] and "“VAC” → Color (Basil)" in words[1] and eff[2]["actions"] == [{"type": "change", "to": "length", "minutes": 120}]
       and all(r["apply"] == ["ccs"] for r in eff), f"0.2.5 → 0.2.8: own rules, then templates, then items without an end (2:00); 24-hour events kept ({words})")
    ok(main.store.get("calendar_tags") is None and main.store.get("defaults") is None, "the old settings are gone")
    p = c.get("/", auth=A).text
    ok("(Tomato)" in p and re.search(r'<span class="ruleused calbadge" data-cal="one" style="--c1:#[0-9a-f]{6}">United CCS Schedule</span>', p) is not None, "All Rules lists them, with who uses them")
    # Note (F3.1)
    r = post("/feed/tags", sid="ccs", name="United Airlines Schedule", note="Base EWR")
    p = c.get("/", auth=A).text
    ok(main.calendar_name() == "United Airlines Schedule" and re.search(r'class="helpdot notedot"[^>]*>.*?<span class="helptip" role="tooltip">[^<]*(<br>)?<b>Note:</b> Base EWR</span>', p) is not None, "F2.2/F3.1: title and note saved from the source's header")
print("FAILS", fails)
