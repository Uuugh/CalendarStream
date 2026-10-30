"""0.2.8-beta.22 tests: the event pop-up (F11): ← and its title, with Choose from template (a new event), Print and
Duplicate (a saved one) in the upper right corner; two columns, the fields on the left (Title*, Location, Calendar |
Change color, All-day | the end's time zone, Starts* | Ends*, Time* | Time*, Time zone | End time zone) and Notes on
the right, as tall as them, dragging it growing the pop-up; Link to closed until Event or Rule, Remove taking the link
off at Save (F11.2); Delete at the bottom left, Hide / Show for an event from a calendar source, with its (i) (F11.3)."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main, calsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", **k):
    return calsync.Download(200, body=FEED, debug={"url": url})
PORT = 8157
U = "demo-RDO-2026-10-02@example"          # an event from United's schedule (made up)

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    seed.demo(c, csrf, main)
    L = main.source_ids()[0]
    ev = lambda q: c.get("/event?" + q).text
    log = lambda n=5: [h["msg"] for h in main.store.recent_log(n)]

    # --- The page, as the server draws it ---------------------------------------------------------------
    p = ev("date=2026-10-21&month=2026-10&embed=1")
    head = p[p.index('<header class="evhead">'):p.index('</header>')]
    ok('class="iconbtn backbtn evback"' in head and "<h1>Add event</h1>" in head and 'id="tplpick"' in head and "Choose from template" in head
       and "Drive to the airport" in head and "evprint" not in head and "copy=" not in head,
       "F11.1: a new event's header: ←, Add event, and Choose from template (no Print or Duplicate yet)")
    ok('id="template"' not in p and "Start from a template" not in p, "…the template picker is in the corner, not a field")
    labels = re.findall(r'<label for="(\w+)"[^>]*>[^<]*<span class="req"', p)
    ok(labels == ["title", "start_date", "end_date", "start_time", "end_time"], f"F11: Title, Starts, Ends and both Times have their * ({labels})")
    ok(">Change color</span>" in p and p.index('id="title"') < p.index('id="location"') < p.index('id="source"') < p.index('id="colorpick"')
       < p.index('id="all_day"') < p.index('id="end_tz_differs"') < p.index('id="start_date"') < p.index('id="end_date"') < p.index('id="start_time"')
       < p.index('id="end_time"') < p.index('id="start_tz"') < p.index('id="end_tz"') < p.index('id="description"') < p.index('id="linkbox"'),
       "F11: the fields in the picture's order, Notes after them, Link to below")
    lk = p[p.index('id="linkbox"'):p.index('class="actions bottom"')]
    ok(re.search(r'data-kind="event" aria-expanded="false"', lk) and re.search(r'data-kind="rule"[^>]*disabled', lk) and 'data-kind="remove"' in lk
       and re.search(r'id="linkevent" hidden', lk) and 'id="linkbtn"' not in p,
       "F11.2: Link to starts closed, with Event | Rule (not until it's saved) | Remove")
    ok("evdelbtn" not in p and "evhidebtn" not in p and 'name="hidden"' not in p, "a new event has no Delete or Hide")

    p = ev(f"uid={U}&month=2026-10&embed=1")
    head = p[p.index('<header class="evhead">'):p.index('</header>')]
    ok("<h1>Edit United event</h1>" in head and 'href="/?month=2026-10&print=2026-10-02#cal"' in head and 'data-date="2026-10-02"' in head
       and f"copy={U.replace('@', '%40')}" in head and "tplpick" not in head,
       "F11.1: a saved event's corner: Print (Print Preview on its day) and Duplicate, no template picker")
    bottom = p[p.index('class="actions bottom"'):p.index("</form>")]
    ok('form="hideform" class="danger evhidebtn" data-ask="Hide this event from the feeds?' in bottom and "> Hide</button>" in bottom
       and 'class="infodot"' in bottom and "can’t be removed from there, but it can be hidden from the feeds" in bottom
       and "evdelbtn" not in bottom and bottom.index("evhidebtn") < bottom.index("pairbtns"),
       "F11.3: an event from a calendar source: Hide (it asks first) with its (i), at the bottom left; no Delete")
    ok('name="hidden"' not in p and "Hide from Google Calendar" not in p, "…the Hide from Google Calendar box is gone (Q7)")

    # Hide, Show, Undo; Save keeps it hidden
    r = post("/event/hide", uid=U, month="2026-10")
    ok(r.status_code in (200, 303) and main.store.get_event(U).hidden and log(1)[0] == 'Hid "RDO" (2026-10-02) from the feeds',
       f"F11.3: Hide hides it from the feeds, with a History line ({log(1)})")
    p = ev(f"uid={U}&month=2026-10&embed=1")
    ok('class="ghost evhidebtn">' in p and "> Show</button>" in p and 'name="show" value="1"' in p and "data-ask" not in p[p.index("evhidebtn") - 80:p.index("evhidebtn") + 60],
       "…then it says Show (and Show doesn't ask)")
    hf = re.search(r'name="start_date" value="([^"]+)"', p)[1]
    post("/event/save", uid=U, month="2026-10", title="RDO day", all_day="1", start_date=hf, end_date=hf, start_tz="America/New_York", end_tz="America/New_York")
    e = main.store.get_event(U)
    ok(e.hidden and e.title == "RDO day", "Save keeps a hidden event hidden (the box that used to say so is gone)")
    post("/event/hide", uid=U, show="1", month="2026-10")
    e = main.store.get_event(U)
    ok(not e.hidden and e.title == "RDO day" and log(1)[0].startswith('Showed "RDO day"'), "Show brings it back, keeping the edit")
    post("/event/revert", uid=U, month="2026-10")
    post("/event/hide", uid=U, month="2026-10"); post("/event/hide", uid=U, show="1", month="2026-10")
    ok(not main.store.get_event(U).hidden and U not in main.store.get_edits(), "Hide then Show on an unedited event leaves it unedited")
    post("/event/hide", uid=U, month="2026-10")
    top = re.search(r'form="undoform" name="entry" value="(\d+)"', c.get("/").text)
    post("/history/undo", entry=top[1] if top else "")
    ok(top and not main.store.get_event(U).hidden, "History › Undo un-hides it")
    ok(post("/event/hide", uid="no-such-event").status_code == 404, "Hide: an event that isn't there is refused")

    # An added event: Delete at the bottom left (asks first); linked, Link to opens at Event
    post("/event/save", title="Lunch", start_date="2026-10-14", end_date="2026-10-14", start_time="12:00", end_time="13:00",
         start_tz="America/New_York", end_tz="America/New_York", source=L, link_to=U, link_delete="1", link_move="1")
    cu = next(x.uid for x in main.store.load_events() if x.title == "Lunch")
    p = ev(f"uid={cu.replace('@', '%40')}&month=2026-10&embed=1")
    bottom = p[p.index('class="actions bottom"'):p.index("</form>")]
    ok('form="deleteform" class="danger evdelbtn" data-ask="Delete this event?' in bottom and "> Delete</button>" in bottom and "evhidebtn" not in bottom,
       "F11.3: an added event says Delete (asking today's question, Q8)")
    lk = p[p.index('id="linkbox"'):p.index('class="actions bottom"')]
    ok('class="seg on" data-kind="event" aria-expanded="true"' in lk and 'id="linkevent" hidden' not in lk and f'<option value="{U}" selected' in lk,
       "F11.2: a linked event opens with Event open (Q11)")
    p = ev("date=2026-10-21&month=2026-10&link=1&embed=1")
    ok('class="seg on" data-kind="event"' in p, "…as does the calendar's Link icon")

    # --- In the browser ---------------------------------------------------------------------------------
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []
        pg.on("pageerror", lambda x: errs.append(str(x))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(f"http://127.0.0.1:{PORT}/?month=2026-10"); pg.wait_for_timeout(500)
        pg.evaluate("openEvent('/event?date=2026-10-21&month=2026-10')"); pg.wait_for_timeout(1200)
        fr = pg.frame_locator("#eventdialog iframe")
        ok(pg.is_hidden("#eventdialog > .dlghead") and fr.locator(".evhead h1").inner_text() == "Add event" and fr.locator(".evback").is_visible(),
           "F11: the pop-up's header is the page's own: ← Add event")
        g = pg.evaluate("""() => { const f = document.querySelector('#eventdialog iframe'), d = f.contentDocument, r = s => d.querySelector(s).getBoundingClientRect();
            const t = r('#title'), n = r('#description'), z = r('#start_tz'), h = r('.evhead'), k = r('.tplpick'), lb = r('#linkbox'), dl = document.getElementById('eventdialog').getBoundingClientRect();
            return { right: n.left > t.right, top: Math.abs(n.top - t.top) <= 1, tall: Math.abs(n.bottom - z.bottom) <= 2, corner: Math.abs(h.right - k.right) <= 1,
                     below: lb.top > n.bottom && lb.top > z.bottom, frame: f.getBoundingClientRect().height, page: d.querySelector('main').getBoundingClientRect().height,
                     fits: dl.height < innerHeight - 48, lines: n.height >= 10 * 21 }; }""")
        ok(g["right"] and g["top"] and g["tall"] and g["below"] and g["lines"], f"F11: Notes on the right, from the Title's line down to the Time zone's, at least 10 lines; Link to under both {g}")
        ok(g["corner"], "F11.1: Choose from template in the upper right corner")
        ok(g["fits"] and abs(g["frame"] - g["page"]) <= 1, f"F11: the pop-up is as tall as the page ({g['frame']} / {g['page']})")
        fr.locator("#description").evaluate("t => t.style.height = '520px'"); pg.wait_for_timeout(400)
        h2 = pg.evaluate("document.querySelector('#eventdialog iframe').getBoundingClientRect().height")
        ok(h2 > g["frame"] + 150, f"…dragging Notes taller grows the pop-up ({g['frame']} → {h2})")
        fr.locator(".tplpick summary").click(); pg.wait_for_timeout(150)
        fr.locator(".tplitem", has_text="Drive to the airport").click(); pg.wait_for_timeout(200)
        ok(fr.locator("#title").input_value() == "Drive to the airport" and fr.locator("#location").input_value() == "EWR"
           and fr.locator("#end_time").input_value() == "10:30am" and not fr.locator(".tplmenu").is_visible(),
           "F11.1: Choose from template fills in the event and closes")
        fr.locator('.linkkind [data-kind="event"]').click(); pg.wait_for_timeout(100)
        ok(fr.locator("#linkevent").is_visible() and fr.locator("#link_to option").count() > 5, "F11.2: Event opens the events to link to")
        fr.locator("#link_to").select_option(index=2)
        fr.locator('.linkkind [data-kind="remove"]').click(); pg.wait_for_timeout(100)
        ok(fr.locator("#linkevent").is_hidden() and fr.locator("#link_to").input_value() == "" and fr.locator(".linkkind .seg.on").count() == 0,
           "…Remove closes it and takes the link off")
        fr.locator(".evback").click(); pg.wait_for_timeout(300)
        ok(pg.locator("#eventdialog[open]").count() == 0, "← closes the pop-up")
        pg.evaluate("openEvent('/event?date=2026-10-21&month=2026-10')"); pg.wait_for_timeout(1200)
        fr.locator("#start_time").click(); pg.wait_for_timeout(150); pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
        ok(fr.locator("#timelist").is_hidden() and pg.locator("#eventdialog[open]").count() == 1, "Escape in a time's list closes only the list")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        ok(pg.locator("#eventdialog[open]").count() == 0, "…and then Escape closes the pop-up, as before")
        # Remove on a linked event: only at Save (Cancel keeps it)
        pg.evaluate(f"openEvent('/event?uid={cu.replace('@', '%40')}&month=2026-10')"); pg.wait_for_timeout(1200)
        fr.locator('.linkkind [data-kind="remove"]').click(); fr.locator(".evcancel").click(); pg.wait_for_timeout(300)
        ok(main.event_links().get(cu, {}).get("to") == U, "F11.2: Remove, then Cancel: still linked (Q11)")
        # Print: Print Preview on the event's day, the pop-up still there behind it
        pg.evaluate(f"openEvent('/event?uid={U.replace('@', '%40')}&month=2026-10')"); pg.wait_for_timeout(1200)
        fr.locator(".evprint").click(); pg.wait_for_timeout(500)
        pp = pg.evaluate("""() => { const d = document.getElementById('printdialog'), f = d.querySelector('form');
            return [d.open, f.elements.start.value, f.elements.end.value, d.querySelector('.viewpick [aria-checked=true]').dataset.v, document.getElementById('eventdialog').open]; }""")
        ok(pp == [True, "2026-10-02", "2026-10-02", "day", True], f"F11.1: Print opens Print Preview on its day (Q9) {pp}")
        pg.click("#printdialog .ppcancel"); pg.wait_for_timeout(200)
        # Hide asks first; Yes hides it and closes the pop-up
        fr.locator(".evhidebtn").click(); pg.wait_for_timeout(300)
        ok(fr.locator("#askdialog").is_visible() and fr.locator("#asktext").inner_text().startswith("Hide this event from the feeds?"), "F11.3: Hide asks first (Q8)")
        fr.locator(".askyes").click(); pg.wait_for_timeout(1500)
        ok(main.store.get_event(U).hidden and pg.locator("#eventdialog[open]").count() == 0, "…Yes hides it and closes the pop-up")
        pg.evaluate(f"openEvent('/event?uid={U.replace('@', '%40')}&month=2026-10')"); pg.wait_for_timeout(1200)
        fr.locator(".infodot").hover(); pg.wait_for_timeout(150)
        tip = fr.locator(".infodot .tip").bounding_box(); dot = fr.locator(".infodot").bounding_box()
        ok(tip and tip["y"] + tip["height"] <= dot["y"] + 1 and abs(tip["x"] - dot["x"]) <= 1, f"F11.3: its (i) opens upwards from the icon, inside the pop-up ({tip})")
        fr.locator(".evhidebtn").click(); pg.wait_for_timeout(1500)
        ok(not main.store.get_event(U).hidden, "…Show brings it back at once")
        # A phone opens the page itself: one column, ← to go back; Print comes back to the calendar with its day
        pg.set_viewport_size({"width": 390, "height": 844})
        pg.goto(f"http://127.0.0.1:{PORT}/event?uid={U.replace('@', '%40')}&month=2026-10"); pg.wait_for_timeout(400)
        t = pg.locator("#title").bounding_box(); n = pg.locator("#description").bounding_box()
        ok(n["y"] > pg.locator("#start_date").bounding_box()["y"] and abs(n["x"] - t["x"]) <= 1 and pg.is_visible(".backbtn"),
           "phone: one column, Notes after the fields, with ←")
        ok(pg.evaluate("document.documentElement.scrollWidth <= innerWidth"), "phone: nothing wider than the screen")
        pg.click(".evprint"); pg.wait_for_timeout(1200)
        ok("print=2026-10-02" in pg.url and pg.evaluate("document.getElementById('printdialog').open"), "phone: Print opens the calendar's Print Preview on its day")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
