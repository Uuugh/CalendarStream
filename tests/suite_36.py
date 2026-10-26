"""0.2.8-beta.2 tests: the If/Then rules (F4), the Local calendar (F3.2), handles (F1.2), event
reminders (F2.2.5), Print Preview (F2.1), the event pop-up (F1.3), Activities as a module (F5)."""
import os, re, sys, threading, time
from datetime import timedelta
from zoneinfo import ZoneInfo
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
from unittest.mock import patch
import json, uvicorn, httpx, seed
from app import main, calsync, gsync, rules as R
from app.calsync import Event
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    return calsync.Download(200, body=FEED, debug={"url": url})

# --- The rules engine on its own --------------------------------------------------------------
TZ = ZoneInfo("America/New_York")
def ev(title, start="2026-10-14T09:00:00-04:00", end="2026-10-14T10:00:00-04:00", all_day=False, **k):
    return Event(title=title, start=start, end=end, all_day=all_day, uid=title, **k)
def rule(conds, actions, rid="", apply="all", title=""):
    return R.normalize({"id": rid, "title": title, "conds": conds, "actions": actions, "apply": apply})
def t(value, op="contains", **k): return {"type": "text", "op": op, "value": value, **k}
def matches(conds, e):
    return R._compile(R.normalize({"conds": conds, "actions": [{"type": "changes"}]})["conds"])(e, R.event_info(e, TZ))

ok([matches([t("RDO", op)], ev(x)) for op, x in (("is", " RDO "), ("contains", "xRDOx"), ("word", "RDO-1"), ("begins", "RDO x"), ("ends", "x RDO"))] == [True] * 5
   and not matches([t("RDO", "word")], ev("RDOS")) and not matches([t("rdo", "contains", case=True)], ev("RDO"))
   and matches([t(r"^R\wO$", "regex")], ev("RDO")), "text: is, contains, whole word, begins, ends, regex; Aa")
A, B, C = t("A", "word"), t("B", "word"), t("C", "word")
ok(matches([A, {**B, "join": "or"}, {**C, "join": "and"}], ev("A")) and not matches([{**A, "open": 1}, {**B, "join": "or", "close": 1}, {**C, "join": "and"}], ev("A")),
   "and binds tighter than or; brackets group: A or B and C ≠ (A or B) and C")
ok(R.normalize({"conds": [{**A, "open": 1}, B], "actions": [{"type": "changes"}]})["conds"][0]["open"] == 0, "unpaired brackets dropped when reading")
try:
    R.normalize({"conds": [{**A, "open": 1}, B], "actions": [{"type": "changes"}]}, strict=True); ok(False, "unpaired brackets refused when saving")
except R.RuleError:
    ok(True, "unpaired brackets refused when saving")
for bad in ({"conds": [t("(", "regex")], "actions": [{"type": "changes"}]}, {"conds": [], "actions": []}, {"conds": [{"type": "date", "op": "between", "value": "2026-10-01"}], "actions": [{"type": "changes"}]}):
    try:
        R.normalize(bad, strict=True); ok(False, f"refused: {bad}")
    except R.RuleError:
        ok(True, f"refused: {str(bad)[:60]}")
fri, sun, wed = ev("x", "2026-10-16T09:00:00-04:00", "2026-10-16T10:00:00-04:00"), ev("x", "2026-10-18T09:00:00-04:00", "2026-10-18T10:00:00-04:00"), ev("x")
days = lambda op, d: {"type": "days", "op": op, "days": d}
ok(matches([days("between", [4, 0])], fri) and matches([days("between", [4, 0])], sun) and not matches([days("between", [4, 0])], wed), "Day(s) between Fri – Mon wraps round the weekend")
ok(matches([days("is", [2, 6])], sun) and matches([days("after", [3])], fri) and matches([days("before", [3])], wed), "Day(s): is (several), after, before")
late = ev("x", "2026-10-14T23:00:00-04:00", "2026-10-14T23:30:00-04:00")
ok(matches([{"type": "time", "op": "between", "value": "22:00", "value2": "06:00"}], late) and not matches([{"type": "time", "op": "between", "value": "22:00", "value2": "06:00"}], wed),
   "Time between 22:00 – 06:00 is overnight")
ok(matches([{"type": "date", "op": "between", "value": "2026-10-20", "value2": "2026-10-10"}], wed) and matches([{"type": "date", "op": "after", "value": "2026-10-13"}], wed), "Date between (either order), after")
noend = ev("x", end="2026-10-14T09:00:00-04:00", no_end=True)
day24 = ev("SCK", "2026-10-19T00:01:00-04:00", "2026-10-19T23:59:59-04:00")
ok(matches([{"type": "length", "op": "is", "minutes": 0}], noend) and not matches([{"type": "length", "op": "is", "minutes": 0}], wed)
   and matches([{"type": "length", "op": "days"}], day24) and matches([{"type": "length", "op": "is", "minutes": 60}], wed), "Length: no end, whole days, 1:00")
rs = R.Ruleset([rule([{"type": "length", "op": "days"}], [{"type": "change", "to": "allday"}]),
                rule([t("x")], [{"type": "change", "to": "length", "minutes": 30}])], TZ, no_end=("hours", 2.0))
a, b, n = rs.change_times([day24, wed, ev("y", end="2026-10-14T09:00:00-04:00", no_end=True)])
ok(a.all_day and a.start == "2026-10-19" and a.end == "2026-10-20" and "Original time:" in a.description and b.end == "2026-10-14T09:30:00-04:00"
   and n.end == "2026-10-14T11:00:00-04:00", "Change: to all-day (the old time noted), to a length; no end and no rule: the .env default (2:00)")
rs = R.Ruleset([rule([t("VAC")], [{"type": "color", "color": "#0b8043"}]), rule([t("VAC")], [{"type": "color", "color": "#d50000"}, {"type": "emoji", "emoji": "🏝️"}])], TZ)
f = rs.finish([ev("VAC day")])[0]
ok(f.rule_color == "#0b8043" and f.title == "🏝️ VAC day" and rs.finish([f])[0].title == "🏝️ VAC day", "priority: the higher rule's color wins; the lower one still adds its emoji (once)")
rs = R.Ruleset([rule([t("Meeting")], [{"type": "event", "title": "Prep", "minutes": 45, "when": "before_start", "offset": 60, "location": "Desk"}])], TZ)
made = rs.made([ev("Meeting")], TZ)
ok(len(made) == 1 and made[0].start == "2026-10-14T08:00:00-04:00" and made[0].end == "2026-10-14T08:45:00-04:00" and made[0].origin == "rule", "Create event (new): 1:00 before, 45 min")
rl = [rule([t("a")], [{"type": "changes"}], "r1", "all"), rule([t("b")], [{"type": "changes"}], "r2", ["ccs"]), rule([t("c")], [{"type": "changes"}], "r3", "all")]
ok(R.insert_position(rl, rule([t("d")], [{"type": "changes"}], "r4", ["ccs"])) == 0 and R.insert_position(rl, rule([t("d")], [{"type": "changes"}], "r4", "all")) == 3,
   "a new rule for one calendar goes above the shared rules it uses; a shared one at the end")
ok([r["id"] for r in R.move(rl, "r1", after="r3")] == ["r2", "r3", "r1"] and [r["id"] for r in R.move(rl, "r3", before="r1")] == ["r3", "r1", "r2"], "move: below / above a neighbour")
lib = [{"id": "a1", "type": "color", "tag": "RDO", "mode": "word", "color": "#d50000"}, {"id": "a2", "type": "no_end", "no_end_mode": "hours", "minutes": 90},
       {"id": "a3", "type": "allday24", "allday": True}, {"id": "a4", "type": "color", "tag": "X", "mode": "starts", "color": "#000000", "owner": "f000001"}]
mig = R.from_v3(lib, {"ccs": ["a1", "a2", "a3"], "f000001": ["a4", "a2", "a3"]}, ["ccs", "f000001"])
ok([(r["id"], r["apply"]) for r in mig] == [("a1", ["ccs"]), ("a2", "all"), ("a3", "all"), ("a4", ["f000001"])] and mig[3]["conds"][0]["op"] == "begins"
   and mig[1]["actions"] == [{"type": "change", "to": "length", "minutes": 90}], "0.2.8-beta.1 rules → If/Then: order, Apply to, Starts with → begins with")

# --- The app ------------------------------------------------------------------------------------
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8098, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8098", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    wid = seed.demo(c, csrf, main)
    L = main.source_ids()[0]
    # F3.2: Local
    ok(main.source(L)["type"] == "local" and main.calendar_name(L) == "Local" and L in main.destinations("feed")[0]["sources"] and L in main.destinations("feed")[-1]["sources"], "Local: at the top, in the feeds")
    p = c.get("/?month=2026-10").text
    top = p[p.index(f'id="src-{L}"'):p.index('id="src-ccs"')]
    ok('class="deflabel"' in top and p.count('class="deflabel"') == 1 and "Events added here" in top and "syncnow" not in top and "0 events added here" in top,
       "F3.2/F3.3: Local is the Default calendar (the label), no Sync Now, its count")
    r = post("/event/save", month="2026-10", title="Dentist", start_date="2026-10-14", start_time="15:00", end_date="2026-10-14", end_time="16:00")
    dentist = next(e for e in main.store.load_events() if e.title == "Dentist")
    ok(r.status_code == 303 and dentist.source == L, "a new event goes into the top calendar")
    ok('<option value="local"' in p or 'data-preset="local"' in p, "F3.2.4: Local calendar in + Add")
    ok(post("/sources/move", sid=L, after="ccs").status_code == 303 and main.source_ids()[:2] == ["ccs", L], "F1.2: moving a module changes the order…")
    p = c.get("/?month=2026-10").text
    ok(p.index('class="deflabel"') > p.index('id="src-ccs"') and p.index('class="deflabel"') < p.index(f'id="src-{L}"'), "…and the top one is now the Default")
    post("/sources/move", sid=L, before="ccs")
    # F2.2.5: reminders
    ok(post("/event/alarms", uid=dentist.uid, minutes=["15", "60", "7"]).status_code == 303 and main.store.get_event(dentist.uid).alarms == "15,60", "reminders saved (only the choices offered)")
    feed = main.destinations("feed")[0]
    ics = c.get(f"/calendar/{feed['token']}.ics").text
    block = ics[ics.index("SUMMARY:Dentist"):]; block = block[:block.index("END:VEVENT")]
    ok("BEGIN:VALARM" in block and "TRIGGER:-PT15M" in block and "TRIGGER:-PT1H" in block and "ACTION:DISPLAY" in block, "…written into the feed (VALARM)")
    body = gsync.event_body(main.store.get_event(dentist.uid), "America/New_York")
    ok(body["reminders"]["useDefault"] is False and sorted(o["minutes"] for o in body["reminders"]["overrides"]) == [15, 60], "…and sent to Google")
    p = c.get("/?month=2026-10").text
    ok('data-alarms="15,60"></span>' in p and "Reminders for" in c.get("/?month=2026-10").text, "the bell shows them; the log has a line")
    post("/event/alarms", uid=dentist.uid)
    ok(main.store.get_event(dentist.uid).alarms == "", "no choices: no reminders")
    # F2.1: Print Preview
    ok(post("/ui/print", view="week", weekends="0", theme="dark").status_code in (200, 204) and main.print_prefs() == {"view": "week", "weekends": False, "theme": "dark"}, "print choices remembered")
    pp = c.get("/print?start=2026-10-12&end=2026-10-17").text
    ok('data-theme="dark"' in pp and "repeat(5," in pp and pp.count('class="sheet"') == 1 and "Dentist" in pp, "Print: last choices (week, no weekends, dark)")
    pp = c.get("/print?view=month&start=2026-10-01&end=2026-11-30&weekends=1&theme=light").text
    ok(pp.count('class="sheet"') == 2 and "repeat(7," in pp and 'data-theme="light"' in pp, "month: a page per month, with weekends")
    pp = c.get("/print?view=itinerary&start=2026-10-14&end=2026-10-14").text
    ok("Dentist" in pp and 'class="aday"' in pp, "itinerary: the days with events")
    pp = c.get("/print?view=5day&start=2026-10-12&end=2026-10-18").text
    ok("repeat(5," in pp, "5-day: Monday to Friday")
    # F1.3: the event page in the pop-up
    e = c.get("/event?date=2026-10-14&month=2026-10&embed=1").text
    ok('class="embed"' in e and 'name="embed" value="1"' in e, "the event page knows it's in the pop-up")
    r = c.post("/event/save", data={"csrf": csrf, "month": "2026-10", "embed": "1", "title": "Lunch", "start_date": "2026-10-15", "start_time": "12:00",
                                    "end_date": "2026-10-15", "end_time": "13:00"}, follow_redirects=False)
    ok(r.status_code == 303 and r.headers["location"] == "/event/done" and "calendarstream:event-saved" in c.get("/event/done").text, "saving in the pop-up closes it")
    hdr = c.get("/").headers
    ok(hdr.get("x-frame-options") == "SAMEORIGIN" and "frame-ancestors 'self'" in hdr.get("content-security-policy", ""), "pages can be framed only by this site")
    # F4 routes
    rid = seed.rule(c, csrf, "Gym", [t("Gym")], [{"type": "color", "color": "#f4511e"}], ["ccs"])
    order = main.source_rules("ccs"); at = [r["id"] for r in order].index(rid)
    ok(all(r["apply"] == ["ccs"] for r in order[:at + 1]) and order[at + 1]["apply"] != ["ccs"], "a new rule for one calendar goes below its own rules, above the shared ones")
    other = order[at - 1]["id"]
    ok(post("/rules/move", id=rid, before=other).status_code == 303 and [r["id"] for r in main.source_rules("ccs")][at - 1:at + 1] == [rid, other], "/rules/move")
    ok(c.post("/rules/save", data={"csrf": csrf, "rule": json.dumps({"conds": [{"type": "text", "op": "regex", "value": "("}], "actions": [{"type": "changes"}], "apply": "all"})}).status_code == 400,
       "a bad regex is refused")
    before_ids = {r["id"] for r in main.all_rules()}; post("/rules/clone", id=rid)
    copy = [r for r in main.all_rules() if r["id"] not in before_ids]
    ids_now = [r["id"] for r in main.all_rules()]
    ok(len(copy) == 1 and copy[0]["apply"] == [] and copy[0]["title"] == "Gym" and ids_now.index(copy[0]["id"]) == ids_now.index(rid) + 1, "Copy: just below, for no calendar yet")
    p = c.get("/").text
    data = json.loads(re.search(r'<script type="application/json" id="ruledata">(.*?)</script>', p, re.S)[1])
    ok(rid in data["rules"] and "text" in data["types"] and data["ops"]["length"] and len(data["calendars"]) == len(main.sources()), "the rule dialog's data")
    # F5: Activities and Logs as a module, Healthy / Unhealthy
    ok('id="activity"' in p and re.search(r'id="activity".*?class="statusbox good"', p, re.S) and ">Healthy<" in p.split('id="activity"')[1][:4000], "Activities: Healthy when nothing's wrong")
    main.st("ccs").status = "error"
    p = c.get("/").text
    ok(">Unhealthy<" in p.split('id="activity"')[1][:4000], "…Unhealthy while a problem is in the log")
    # I1: the Accomplished list's check marks are outside the text
    css = c.get("/assets/app.css").text
    ok(re.search(r"\.checks li \{[^}]*padding-left:22px", css) is not None and re.search(r"\.checks li::before \{[^}]*position:absolute", css) is not None, "I1: a line's words wrap under its first word, not the check")
    # Removing the default calendar: the next one becomes the default
    post("/sources/remove", sid=L)
    ok(main.source_ids()[0] == "ccs" and not main.store.get("local_made") is False, "Local removed: CCS+ is the default")
    main.ensure_local()
    ok(L not in main.source_ids() and all(main.source(x)["type"] != "local" for x in main.source_ids()), "…and it isn't made again")
    ok(post("/sources/add", type="local", name="").status_code == 303 and main.sources()[-1]["type"] == "local" and main.calendar_name(main.source_ids()[-1]) == "Local",
       "+ Local calendar: another can be added")

    # --- In a browser -------------------------------------------------------------------------
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e) + " " + str(e.stack)[:400]))
        pg.goto("http://127.0.0.1:8098/?month=2026-10"); pg.wait_for_timeout(400)
        # event: open, alarm popover, edit in a pop-up
        post("/event/save", month="2026-10", title="Lunch", start_date="2026-10-15", start_time="12:00", end_date="2026-10-15", end_time="13:00", source="ccs")
        pg.goto("http://127.0.0.1:8098/?month=2026-10"); pg.wait_for_timeout(400)
        d = pg.locator("details.ev").filter(has_text="Lunch").first
        d.locator("summary").click(); pg.wait_for_timeout(100)
        d.locator(".evalarm").click(); pg.wait_for_timeout(150)
        ok(pg.is_visible("#alarmpop"), "the bell opens the reminder choices")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        d.locator(".evedit").click(); pg.wait_for_timeout(800)
        ok(pg.locator("#eventdialog[open]").count() == 1 and "uid=" in pg.locator("#eventdialog iframe").get_attribute("src"), "F1.3: ✎ edits the event in a pop-up")
        fr = pg.frame_locator("#eventdialog iframe")
        fr.locator("#title").fill("Lunch with Sam"); fr.get_by_role("button", name="Save", exact=True).click(); pg.wait_for_timeout(1500)
        ok(pg.locator("#eventdialog[open]").count() == 0 and "Lunch with Sam" in pg.inner_text("#cal"), "…Save closes it and the calendar shows the change")
        # Print Preview
        pg.click("#printbtn"); pg.wait_for_timeout(800)
        ok(pg.locator("#printdialog[open]").count() == 1 and pg.locator("#printdialog .viewpick [aria-checked=true]").get_attribute("data-v") == "week", "Print Preview starts with the last print's choices")
        pg.click('#printdialog .viewpick [data-v="month"]'); pg.wait_for_timeout(800)
        ok("view=month" in pg.locator("#printdialog iframe").get_attribute("src"), "…and redraws when changed")
        pg.keyboard.press("Escape")
        # the rule dialog: brackets, day buttons, Then +
        pg.click("#rules .toggle"); pg.click("#rules .newrule.headplus"); pg.wait_for_timeout(200)
        ok(pg.evaluate("[...document.querySelectorAll('.helptip')].every(t => !t.offsetParent)"), "no (?) explanation shows until asked (the page and the rule dialog)")
        pg.select_option("#ruledialog .cond .ctype", "days"); pg.wait_for_timeout(100)
        pg.click("#ruledialog .cond .wd[data-d='5']"); pg.click("#ruledialog .cond .wd[data-d='6']", modifiers=["Control"])
        pg.click("#ruledialog .act .aadd"); pg.wait_for_timeout(100)
        pg.locator("#ruledialog .act").nth(1).locator(".atype").select_option("emoji"); pg.wait_for_timeout(100)
        pg.locator("#ruledialog .act").nth(1).locator(".aval").fill("🎉")
        pg.click("#ruledialog .psave"); pg.wait_for_timeout(1500)
        new = main.all_rules()[-1]
        ok(new["conds"][0]["days"] == [5, 6] and [a["type"] for a in new["actions"]] == ["color", "emoji"] and new["apply"] == "all", f"a rule: Day(s) is Sat, Sun (ctrl-click) → color, emoji ({new['conds']})")
        # phone: dialogs fill the screen; the event page has its Back button
        pg.set_viewport_size({"width": 390, "height": 800}); pg.wait_for_timeout(200)
        pg.click("#rules .newrule.headplus"); pg.wait_for_timeout(200)
        box = pg.locator("#ruledialog").bounding_box()
        ok(round(box["width"]) == 390 and pg.is_visible("#ruledialog .dlgback"), f"phone: the rule dialog is a full page with ← ({box['width']:.0f})")
        pg.click("#ruledialog .dlgback"); pg.wait_for_timeout(100)
        pg.locator(".day[data-add]").nth(10).dispatch_event("click"); pg.wait_for_timeout(1200)     # (a click on the day itself, not on an event)
        ok("/event?" in pg.url and pg.is_visible(".backbtn"), "phone: Add event opens the page, with ← Back")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
