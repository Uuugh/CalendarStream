"""0.2.8-beta.27 tests (the 3 Rules + installer build): the new Thens Delete this event / Move this event (F4), Add and Change's
"to" fields (F30), the Then order and its renamed Record changes (F19), link rules instead of Delete with it / Move with it (F3),
the rule delete shown as Deleted by a rule (I3), Add a rule always opening the pop-up (I1), Different end time zone on Time
zone's line (F17.1), good-status words that keep their words in Status/Action buttons (I10), and the installer's defaults (F29)."""
import os, re, sys
from zoneinfo import ZoneInfo
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "ccs"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
from app import rules as R, links as L
from app.calsync import Event
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
TZ = ZoneInfo("America/New_York")
def ev(title, start="2026-10-14T09:00:00-04:00", end="2026-10-14T10:00:00-04:00", **k): return Event(title=title, start=start, end=end, uid=title, **k)
def rule(conds, actions, rid="", apply="all"): return R.normalize({"id": rid, "conds": conds, "actions": actions, "apply": apply})
def t(value): return {"type": "text", "op": "contains", "value": value}
read = lambda *p: open(os.path.join(REPO, *p)).read()

# --- F4: Delete this event / Move this event ---------------------------------------------------------------------------
ok(R.ACTION_TYPES.get("delete") == "Delete this event" and R.ACTION_TYPES.get("move") == "Move this event" and R.ACTION_TYPES.get("changes") == "Record changes in the event notes section",
   "F4/F19: the Thens are Delete this event, Move this event and Record changes in the event notes section")
rs = R.Ruleset([rule([t("Gone")], [{"type": "delete"}])], TZ)
g, k = rs.finish([ev("Gone one"), ev("Keep")])
ok(g.hidden and g.deleted.startswith("rule|") and not k.hidden, "F4: Delete this event leaves the event out of the feeds (hidden, deleted by a rule)")
rs = R.Ruleset([rule([t("Shift")], [{"type": "move", "minutes": 90}])], TZ)
m = rs.change_times([ev("Shift me")])[0]
ok(m.start == "2026-10-14T10:30:00-04:00" and m.end == "2026-10-14T11:30:00-04:00", "F4: Move this event by +1:30 moves start and end")
rs = R.Ruleset([rule([t("Shift")], [{"type": "move", "minutes": -30}])], TZ)
ok(rs.change_times([ev("Shift me")])[0].start == "2026-10-14T08:30:00-04:00", "F4: a negative amount moves it earlier")

# --- F30: Change takes Title/Notes/Location; Add puts text at the end ------------------------------------------------------
rs = R.Ruleset([rule([t("Trip")], [{"type": "change", "to": "title", "text": "Renamed"}, {"type": "add", "to": "notes", "text": "Bring ID"}, {"type": "add", "to": "location", "text": "Gate 4"}])], TZ)
f = rs.finish([ev("Trip", description="Old notes", location="JFK")])[0]
ok(f.title == "Renamed" and f.description.startswith("Old notes") and f.description.endswith("Bring ID") and "\nBring ID" in f.description and f.location == "JFK Gate 4",
   f"F30: Change sets the Title; Add puts notes on a new line and a location after it, never overwriting ({f.title!r}, {f.description!r}, {f.location!r})")
try:
    R.normalize({"conds": [t("x")], "actions": [{"type": "add", "to": "title", "text": ""}]}, strict=True); ok(False, "F30: Add with no text is refused")
except R.RuleError:
    ok(True, "F30: Add with no text is refused")
ok(R.shadow_kind({"type": "change", "to": "title", "text": "x"}) != R.shadow_kind({"type": "change", "to": "notes", "text": "x"}), "F30: Change to Title and to Notes are different kinds (no false conflict)")

# --- F3: a link rule instead of Delete with it / Move with it --------------------------------------------------------------
lr = R.normalize({"id": "l1", "conds": [], "apply": ["ccs"], "link": {"uid": "a@x", "to": "b@x", "src": "s2", "own": "ccs", "at": "2026-10-14T09:00:00-04:00", "name": "Other"},
                  "actions": [{"type": "delete"}, {"type": "move", "minutes": 0, "with_link": True}]})
ok(lr and lr["link"]["to"] == "b@x" and lr["conds"] == [] and [a["type"] for a in lr["actions"]] == ["delete", "move"], "F3: a link rule keeps its link, has no If, and carries the two Thens")
d = L.from_rules([lr])
ok(d.get("a@x", {}).get("delete") is True and d["a@x"]["move"] is True and d["a@x"]["to"] == "b@x", "F3: the links come from the link rules (Delete this event, Move this event with the linked event)")
ok(R.Ruleset([lr], TZ).rules == [] or not R.Ruleset([lr], TZ).finish([ev("a@x")])[0].hidden, "F3: a link rule never matches events by itself")
ok("Delete with it" not in read("app", "templates", "event.html") and "linknote" in read("app", "templates", "event.html"), "F3: the event pop-up no longer has the Delete with it / Move with it boxes")

# --- F19: a handle on each Then ----------------------------------------------------------------------------------------------
js = "".join(read("app", "templates", "js", f) for f in sorted(os.listdir(os.path.join(REPO, "app", "templates", "js"))))
ok("THEN_HANDLE" in js and "thenDrag" in js and "hgrip" in js, "F19: each Then has a handle (the same classes as the other handles)")

# --- I3: the bin on a read-only event hides; a rule's deletion has no Restore ----------------------------------------------------
cal = read("app", "templates", "index", "calendar.html")
ok("/event/hide" in cal and "evhide" in cal and "Deleted by a rule" in read("app", "main.py"), "I3: a read-only event's bin is Hide; Deleted by a rule is a deletion place")

# --- I1: Add a rule opens the new-rule pop-up --------------------------------------------------------------------------------
src = read("app", "templates", "index", "sources.html")
ok('class="ghost addrule newrule"' in src and "New rule…" not in src and "addreuse" in src, "I1: + Add a rule always opens the new-rule pop-up; reusing another calendar's rule is a separate ▾")

# --- F17.1: Different end time zone on Time zone's label line ------------------------------------------------------------------
evh = read("app", "templates", "event.html")
tz = evh[evh.index('class="timed tzdiff"'):]
tz = tz[:tz.index("</div></div>") + 12]
ok('class="lblline"' in tz and 'class="endzone"' in tz and tz.index("end_tz_differs") < tz.index('zonepick("end_tz"'), "F17.1: Different end time zone on a label line, its time zone box under it")
ok('for="end_tz"' not in evh, "F17.1: no End time zone label")

# --- I10: only the login blocks shrink -------------------------------------------------------------------------------------------
fold = read("app", "templates", "js", "14-status-fold.js")
ok("closest('.statusbox, .countbox')" in fold, "I10: Status/Action buttons (every .statusbox) and counts keep their words")

# --- F29: the installer ----------------------------------------------------------------------------------------------------------
inst = read("install.sh"); comp = read("docker-compose.yml")
ok('"$HOME/stacks/calendarstream"' in inst and 'calendarstream$n' in inst, "F29.1: the stack folder defaults to ~/stacks/calendarstream, numbered when taken")
ok('"${CURRENT_DATA:-$DIR/data}"' in inst, "F29.2: the data folder defaults to a subfolder of the stack folder")
ok("UPD_DEFAULT=yes" in inst and inst.count("UPD_DEFAULT=no") == 2, "F29.3: Allow updating from the status page defaults to yes on a new install")
ok("STACK_NO" in inst and "calendar_stream_updater$STACK_NO" in inst and "container_name: calendar_stream${STACK_NO:-}" in comp and "calendar_stream_updater${STACK_NO:-}" in comp
   and "calendar_stream_db${STACK_NO:-}" in comp and "${PORT:-8080}:8080" in comp, "F29.4: a second stack gets a number on its container names, and its own port")
import subprocess
ok(subprocess.run(["bash", "-n", os.path.join(REPO, "install.sh")]).returncode == 0, "F29: install.sh is valid bash")
print("FAILED:", fails) if fails else print("ALL PASSED")
