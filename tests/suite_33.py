"""0.2.7-beta.5 tests: the source box (mockup), rules changed in a source (local / shared), presets,
Record changes, folding template sections, the report form, and sync / views without reloads."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main, calsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    await __import__("asyncio").sleep(1.5)
    return calsync.Download(200, body=FEED, debug={"url": url})
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8096, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8096", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    main.logins.save_ccs("U123456", "pw12345"); main.state.last_auth_ok = True
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", DEMO)})
    # F2.3 presets: Google / Apple are calendar feeds with their own help and note
    post("/sources/add", type="ics", preset="google", url="https://calendar.google.com/calendar/ical/x/private-abc/basic.ics", name="Family")
    gid = main.source_ids()[-1]
    p = c.get("/").text
    ok(main.source(gid)["preset"] == "google" and '<div class="srckind" title="Google Calendar">Google Calendar</div>' in p and "How to get your Google Calendar’s secret address" in p and "How to enable Google Calendar" in p,
       "F2.3.1: the Google preset: its note and step-by-step help")
    ok('<div class="srckind" title="United Airlines CCS+">United Airlines CCS+</div>' in p and "<b>Note:</b>" not in p.split('id="src-ccs"')[1].split('class="srcright"')[0],
       "F2.3.3 (beta.9): the CCS+ module's kind is United Airlines CCS+; no note until one is written (its (i) says what it is)")
    ok(">How to enable CCS+</p>" in p and ">Accomplished</p>" in p, "F2.1.4.1: How to enable CCS+ | Accomplished")
    q = p[p.index('id="src-ccs"'):]
    i_auto, i_man, i_rules = q.index(">Automatic Upload<"), q.index(">Manual Upload<"), q.index('class="cfghead">Rules<')
    ok(i_auto < q.index('id="interval-ccs"') < i_man < i_rules, "F2.1.1/F2.1.2: Automatic Upload (with Check every), then Manual Upload, then Rules")
    post("/feed/tags", sid="ccs", note="", name="United CCS Schedule")
    ok('<b>Note:</b>' not in c.get("/").text.split('id="src-ccs"')[1].split('class="srcright"')[0], "F2.3.3: the note can be emptied like any other")
    # 0.2.8 (F4): one rule, applied to the calendars chosen in its Apply to; changing it changes it for each
    import json, seed
    rdo = seed.rule(c, csrf, "", [seed.text("RDO")], [{"type": "color", "color": "#d50000"}], ["ccs", gid])
    ids = lambda x: [r["id"] for r in main.source_rules(x)]
    ok(rdo in ids("ccs") and rdo in ids(gid), "a rule for two calendars")
    p = c.get("/").text
    ok('class="scope calbadge shared" data-cal="many" style="background:repeating-linear-gradient(135deg' in p and "2 calendars" in p, "each line says who uses it (2 calendars)")
    r = next(x for x in main.all_rules() if x["id"] == rdo)
    post("/rules/save", rule=json.dumps({**r, "apply": ["ccs"]}))
    ok(rdo in ids("ccs") and rdo not in ids(gid), "Apply to: only CCS+ now")
    p = c.get("/").text
    ok('class="scope calbadge local" data-cal="one"' in p and "This calendar" in p, "…so its line says This calendar")
    # F3.2 clone
    n = len(main.all_rules()); post("/rules/clone", id=rdo)
    ok(len(main.all_rules()) == n + 1, "F3.2: Copy makes a new rule")
    # F3.3 Record changes: a note on the event and a line in the log
    rid = seed.rule(c, csrf, "", [], [{"type": "changes"}], [gid])
    ok(next(x for x in main.all_rules() if x["id"] == rid)["actions"] == [{"type": "changes"}] and main.ruleset(gid).records_changes, "F3.3: a Record changes rule (every event)")
    v1 = FEED; uid = re.search(rb"UID:([^\r\n]+)", v1)[1]
    m = re.search(rb"DTSTART[^:\r\n]*:(\d{8}T\d{4})", v1); old = m[1]
    v2 = v1.replace(b"DTSTART" + m[0][7:], b"DTSTART" + m[0][7:].replace(old, old[:9] + b"1111"), 1)
    main.apply_calendar(v1, "downloaded", gid); main.apply_calendar(v2, "downloaded", gid)
    notes = main.store.get(main.skey(gid, "change_notes")) or {}
    evs = [e for e in main.store.load_events(gid) if notes.get(e.uid)]
    ok(notes and evs and "Changed" in evs[0].description and "time" in evs[0].description, f"F3.3: the changed event's notes say what changed ({list(notes.values())[:1]})")
    ok("Family changed" in c.get("/").text, "F3.3: …and Activities and Logs has a line")
    # F5 report data: private details taken out
    d = c.get("/report/data").json()
    blob = str(d)
    ok(d["version"] == main.__version__ and "U123456" not in blob and "private-abc" not in blob, "F5: report data, with the username and feed links taken out")
    # I1 Sync Now answers at once from the page's script
    r = c.post("/run", data={"csrf": csrf, "sid": gid}, headers={"X-CS-Async": "1"})
    ok(r.status_code == 200 and r.json()["ok"], "I1.1: Sync Now answers at once (no page reload)")
    time.sleep(2.5)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        loads = []; pg.on("load", lambda: loads.append(1))
        pg.goto("http://127.0.0.1:8096/?view=month"); pg.wait_for_timeout(400); loads.clear()
        pg.click('.viewseg [data-view="week"]'); pg.wait_for_timeout(800)
        ok(pg.locator(".weekgrid").count() == 1 and not loads and "view=" not in pg.url, "I1.1: Week shows straight away, without reloading the page")
        pg.click('.viewseg [data-view="list"]'); pg.wait_for_timeout(800)
        ok(pg.locator(".agenda").count() == 1 and not loads, "…and List")
        pg.click('.viewseg [data-view="month"]'); pg.wait_for_timeout(800)
        # sync: only the status, calendar and log change
        box = f"#src-{gid}"
        if pg.locator(f"#cfg-{gid}[hidden]").count(): pg.click(f"{box} .cfgtoggle")
        pg.fill(f"{box} .nameinput", "Typed but not saved")
        pg.click(f"{box} .syncnow"); pg.wait_for_timeout(500)
        ok(pg.inner_text(f"{box} .statusbox .chip") == "Syncing…" and not loads, "I1.1: Sync Now: Syncing… in place")
        pg.wait_for_timeout(4500)
        ok(pg.inner_text(f"{box} .statusbox .chip") == "Healthy" and not loads and pg.input_value(f"{box} .nameinput") == "Typed but not saved",
           "I1.1: then Healthy, without a reload (what was being typed is kept)")
        # Cancel puts the box back
        pg.click(f"{box} .pcancel"); pg.wait_for_timeout(1200)
        ok(pg.input_value(f"{box} .nameinput") == "Family" and pg.locator(f"#cfg-{gid}[hidden]").count() == 1, "F1.1 (0.2.8): Cancel undoes the changes and closes the module")
        # ✎ on a calendar's rule: the rule dialog with that rule; Apply saves it in place
        pg.click(f"{box} .cfgtoggle"); pg.wait_for_timeout(100)
        line = pg.locator(f"{box} .ruleline").first
        rid = line.get_attribute("data-rule-id")
        line.locator(".editrule").click(); pg.wait_for_timeout(200)
        ok(pg.eval_on_selector("#ruledialog", "d => d.open") and pg.inner_text("#rdtitle") == "Change rule" and pg.is_visible("#ruledialog .rdremove"), "✎: Change rule, with Remove")
        pg.fill("#rdname", "Renamed rule"); pg.click("#ruledialog .psave"); pg.wait_for_timeout(1500)
        ok(next(x for x in main.all_rules() if x["id"] == rid)["title"] == "Renamed rule" and "Renamed rule" in pg.inner_text(f"{box} .srcrules") and not loads, "…Apply saves it, in place")
        # presets in + Add a calendar source
        pg.click("#sources .plus"); pg.click('.preset[data-preset="apple"]'); pg.wait_for_timeout(100)
        ok("Apple Calendar" in pg.inner_text('.presetform[data-for~="other"] b') and pg.input_value('.presetform[data-for~="other"] input[name=preset]') == "apple", "F2.3.1: the Apple preset")
        pg.keyboard.press("Escape")
        # folding sections
        ok(pg.locator("#rules-body[hidden]").count() == 1 and pg.locator("#templates-body[hidden]").count() == 1 and pg.locator("#rules > .shead .plus").count() == 0, "F3.1/F4.1: Rule and Event Templates fold to their title (+ at the bottom right when open, beta.11), + in the corner")
        # report form
        pg.click(".reportbtn[data-kind=bug]"); pg.wait_for_timeout(800)
        pg.fill("#rpwhat", "The calendar is empty")
        txt = pg.text_content("#reportdialog pre.preview")
        ok("The calendar is empty" in txt and "CalendarStream " + main.__version__ in txt and "U123456" not in txt, "F5: the report's preview, private details out")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILS", fails)
