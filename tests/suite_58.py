"""0.2.8-beta.23 tests: an open event's icons at the event's right edge (I1); the "Changes here only affect…" line
out of the event pop-up, into an (i) beside Calendar (an added event) or Hide's (i) (a source's event) (I2); Link to ›
Event's small calendar (F1) and its ✕ (F2); + Add a feed's link whole, with its title, and its Label and Notes taking
the top calendar's name and note (F13–F13.2); All Rules' "All calendars" badge (F14); History: 100 changes by default,
the latest lines in the header open or folded, Undo in its own column (F15–F15.2); deleting asks with No | Yes (F16)."""
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
PORT = 8158
U = "demo-RDO-2026-10-02@example"          # an event from United's schedule (made up)
V = "demo-RDO-2026-10-08@example"
q = lambda uid: uid.replace("@", "%40")

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    seed.demo(c, csrf, main)
    L = main.source_ids()[0]
    ev = lambda qs: c.get("/event?" + qs).text

    # --- I2: the line is gone from the pop-up; an (i) beside Calendar, or in Hide's (i) -------------------
    p = ev("date=2026-10-21&month=2026-10&embed=1")
    cal = p[p.index('<label for="source"'):p.index('id="source"', p.index('<label for="source"'))]
    ok('class="infodot down"' in cal and "An event added here goes to CalendarStream, its feeds and Google. CCS+ is never changed." in cal,
       "I2: a new event has an (i) beside Calendar")
    ok("Changes here only affect" not in p and 'class="muted foot"' not in p, "I2: …and no line about CCS+ in the pop-up")
    p = ev(f"uid={q(U)}&month=2026-10&embed=1")
    bottom = p[p.index('class="actions bottom"'):p.index("</form>")]
    ok("Changes here only affect CalendarStream and Google; CCS+ is never changed." in bottom and "Your edit is kept when the schedule is downloaded again." in bottom
       and 'class="infodot down"' not in p and 'class="muted foot"' not in p, "I2: a source's event has the whole line in Hide's (i), and not at the bottom")
    post("/event/save", title="Lunch", start_date="2026-10-14", end_date="2026-10-14", start_time="12:00", end_time="13:00",
         start_tz="America/New_York", end_tz="America/New_York", source=L)
    cu = next(x.uid for x in main.store.load_events() if x.title == "Lunch")
    p = ev(f"uid={q(cu)}&month=2026-10&embed=1")
    ok("Added on this page" not in p and 'class="infodot down"' in p, "I2: a saved added event: the (i) in place of the note at the top")

    # --- F1, F2: Link to's line: Event | Rule, the pick, ✕ ------------------------------------------------
    lk = p[p.index('id="linkbox"'):p.index('class="actions bottom"')]
    ok('<select id="link_to"' not in p and 'type="hidden" name="link_to" id="link_to" value=""' in lk and 'id="linkpicked"' in lk
       and re.search(r'id="linkpicked"[^>]*hidden', lk), "F1: no drop-down; the pick goes on Link to's line (none yet)")
    ok(re.search(r'class="iconbtn linkremove" data-kind="remove" title="Remove the link" aria-label="Remove the link">\s*<svg', lk)
       and "Remove</button>" not in lk and lk.index('data-kind="rule"') < lk.index("linkremove"), "F2: Remove is an ✕ (icon only) at the end of the line")
    r = c.get(f"/event/pick?uid={q(cu)}&month=2026-10")
    pk = r.text
    ok(r.status_code == 200 and "October 2026" in pk and 'data-month="2026-09"' in pk and 'data-month="2026-11"' in pk and "pktoday" in pk
       and "<html" not in pk, "F1: the small calendar: a month, with ‹ › Today")
    ok('class="pkev off self"' in pk and "Lunch" in pk[pk.index("pkev off self"):pk.index("pkev off self") + 400], "F1: this event can't be picked")
    ok(f'data-uid="{cu}"' not in pk and f'data-uid="{U}" data-label="RDO · Fri Oct 2"' in pk, f"F1: another one can, labelled \"Title · date\"")
    ok(re.search(r'class="pkev off" [^>]*title="Made by a rule', pk) and not re.search(r'<button[^>]*data-uid="[^"]*#rule-', pk),
       "F1: rule-made events can't be picked")
    ok("/event?date=" not in pk and "data-add" not in pk and "evedit" not in pk, "F1: nothing to add or edit there")
    ok(c.get("/event/pick?month=2026-11&uid=").status_code == 200 and "November 2026" in c.get("/event/pick?month=2026-11").text, "F1: ‹ › move it a month")
    post("/event/save", uid=cu, title="Lunch", start_date="2026-10-14", end_date="2026-10-14", start_time="12:00", end_time="13:00",
         start_tz="America/New_York", end_tz="America/New_York", link_to=U, link_delete="1", link_move="1")
    p = ev(f"uid={q(cu)}&month=2026-10&embed=1")
    lk = p[p.index('id="linkbox"'):p.index('class="actions bottom"')]
    ok(f'value="{U}"' in lk and re.search(r'id="linkpicked" title="Pick another event">RDO · Fri Oct 2</button>', lk) and 'class="seg on" data-kind="event"' in lk
       and 'id="linkevent" hidden' not in lk, "F1: a linked event shows its pick on the line, with Delete with it / Move with it under it")
    p = ev("date=2026-10-21&month=2026-10&link=1&embed=1")
    ok('data-pick-now="1"' in p, "F1: the calendar's Link icon opens the small calendar at once")

    # --- F13.2: the label and note, left empty, from the top calendar it includes ---------------------------
    sids = main.source_ids()
    named = [x for x in sids if (main.source(x) or {}).get("type") != "local"]
    main.store.set(main.skey(named[0], "note"), "Trips and reserve days")
    page = c.get("/").text
    ok("(or enter your own calendar url)" in page and re.search(r'name="stream" class="code fstream" form="adddest" value="[\w-]{20,}"', page),
       "F13.1: + Add a feed's link is whole from the start, with its title")
    ok('data-note="Trips and reserve days"' in page and ">Label<" in page and 'data-default="Label"' in page, "F13.2: Label and Notes have titles; the calendars carry their names and notes")
    n = len(main.destinations())
    r = post("/destinations/add", type="feed", name="", note="", sources=named[0])
    d = main.destinations()[-1]
    ok(len(main.destinations()) == n + 1 and d["name"] == main.calendar_name(named[0]) and d["note"] == "Trips and reserve days",
       f"F13.2: left empty, Label and Notes take the top calendar's name and note ({d['name']!r}, {d['note']!r})")
    post("/destinations/add", type="feed", name="Mine", note="My note", sources=named[0])
    d = main.destinations()[-1]
    ok(d["name"] == "Mine" and d["note"] == "My note", "F13.2: typed ones are kept")

    # --- F14, F15 ---------------------------------------------------------------------------------------------
    ok(main.UNDO_KEEP == 100 and main.undo_keep() == 100 and 'name="keep" min="1" max="200" value="100"' in page, "F15: Remember the last 100 changes by default")
    post("/history/keep", keep="37")
    ok(main.undo_keep() == 37 and 'value="37"' in c.get("/").text, "F15: …a number saved is kept")
    post("/history/keep", keep="100")
    page = c.get("/").text
    hd = re.search(r'<thead><tr><th class="htime">.*?</tr></thead>', page)[0]
    ok(re.findall(r'<th class="(\w*)"|<th>', hd) == ["htime", "htype", "hundo", ""], f"F15.2: Undo between Type and Event")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []
        pg.on("pageerror", lambda x: errs.append(str(x))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(f"http://127.0.0.1:{PORT}/?month=2026-10"); pg.wait_for_timeout(500)
        # F14
        st = pg.evaluate("""() => { const x = document.querySelector('.calbadge[data-cal="all"]'); if (!x) return null; const s = getComputedStyle(x);
            const a = getComputedStyle(document.body).getPropertyValue('--accent'); return [s.backgroundColor, s.color, s.borderTopColor]; }""")
        acc = pg.evaluate("""() => { const t = document.createElement('span'); t.style.color = 'var(--accent)'; document.body.appendChild(t); const c = getComputedStyle(t).color; t.remove(); return c; }""")
        ok(st and st[0] == "rgba(0, 0, 0, 0)" and st[1] == acc and st[2] == acc, f"F14: All calendars: blue words and border, clear background {st}")
        # F15.1: the latest lines in the header, folded and open, left-aligned beside Healthy
        def peek():
            return pg.evaluate("""() => { const p = document.querySelector('#activity > .shead .peek.latest'), h = document.querySelector('#activity > .shead .statusbox');
                if (!p) return null; const r = p.getBoundingClientRect(), s = h.getBoundingClientRect(), l = p.querySelector('.peekline').getBoundingClientRect();
                return [getComputedStyle(p).display !== 'none' && r.height > 0, p.querySelectorAll('.peekline').length, Math.round(l.left - r.left), r.right <= s.left + 1]; }""")
        folded = peek()
        pg.evaluate("document.querySelector('#activity').classList.add('open')"); pg.wait_for_timeout(100)
        opened = peek()
        ok(folded and folded[0] and folded[1] == 3 and folded[2] <= 1 and folded[3] and opened and opened[0], f"F15.1: three lines beside Healthy, left-aligned, folded {folded} and open {opened}")
        pg.evaluate("document.querySelector('#activity').classList.remove('open')")
        # F16: deleting from the calendar asks with No | Yes
        pg.evaluate(f"document.querySelector('details[data-uid=\"{cu}\"]').open = true"); pg.wait_for_timeout(200)
        pg.locator(f'details[data-uid="{cu}"] .evdel button').click(); pg.wait_for_timeout(300)
        a = pg.evaluate("""() => { const d = document.getElementById('askdialog'); return [d.open, d.querySelector('.asktext').firstChild.textContent, (d.querySelector('.asksub') || {}).textContent,
            [...d.querySelectorAll('.pairbtns button')].map(b => b.textContent), d.querySelector('.pairbtns').getBoundingClientRect().width]; }""")
        ok(a[0] and a[1] == "Delete this event?" and a[2] == "(It may be restored here or in History, Undo & Logs)" and a[3] == ["No", "Yes"] and abs(a[4] - 130) <= 1,
           f"F16: Delete this event? / (It may be restored…) with the pair No | Yes {a}")
        pg.locator("#askdialog .pcancel").click(); pg.wait_for_timeout(300)
        ok(not main.store.get_event(cu).deleted, "F16: No keeps it")
        # I1: the icons at the event's right edge, on a narrow day
        pg.set_viewport_size({"width": 900, "height": 900}); pg.wait_for_timeout(200)
        pg.evaluate(f"document.querySelector('details[data-uid=\"{U}\"]').open = true"); pg.wait_for_timeout(200)
        g = pg.evaluate(f"""() => {{ const d = document.querySelector('details[data-uid="{U}"]'), e = d.getBoundingClientRect(), c = d.querySelector('.evclose').getBoundingClientRect();
            const right = Math.max(...[...d.querySelectorAll('.evicons > *')].filter(x => x.offsetParent).map(x => x.getBoundingClientRect().right));
            return [Math.round(c.left - e.left), Math.round(e.right - right), getComputedStyle(d.querySelector('.body')).paddingRight]; }}""")
        ok(g[2] == "6px" and g[1] <= 9 and abs(g[0] - g[1]) <= 2, f"I1: the icons end at the event's right edge, as far in as Close {g}")
        pg.set_viewport_size({"width": 1400, "height": 900})
        # F1, F2 in the pop-up
        pg.evaluate(f"openEvent('/event?uid={q(cu)}&month=2026-10')"); pg.wait_for_timeout(1200)
        fr = pg.frame_locator("#eventdialog iframe")
        fr.locator('.linkkind [data-kind="remove"]').click(); pg.wait_for_timeout(100)
        ok(fr.locator("#linkpicked").is_hidden() and fr.locator("#linkevent").is_hidden() and fr.locator("#link_to").input_value() == "", "F2: ✕ takes the link off")
        fr.locator('.linkkind [data-kind="event"]').click(); pg.wait_for_timeout(700)
        ok(fr.locator("#pickdialog").is_visible() and fr.locator("#picktitle").inner_text() == "October 2026", "F1: Event opens the small calendar at once, on this event's month")
        fr.locator('#pickdialog .pknav').nth(1).click(); pg.wait_for_timeout(500)
        ok(fr.locator("#picktitle").inner_text() == "November 2026", "F1: › goes to the next month")
        fr.locator('#pickdialog .pknav').first.click(); pg.wait_for_timeout(500)
        fr.locator(f'#pickdialog button.pkev[data-uid="{V}"]').first.click(); pg.wait_for_timeout(300)
        ok(fr.locator("#pickdialog").is_hidden() and fr.locator("#link_to").input_value() == V and fr.locator("#linkpicked").inner_text() == "RDO · Thu Oct 8"
           and fr.locator("#linkevent").is_visible(), "F1: a click picks the event and closes it; the pick shows on the line, with the boxes under it")
        fr.locator("#linkpicked").click(); pg.wait_for_timeout(700)
        ok(fr.locator("#pickdialog").is_visible(), "F1: a click on the pick opens the calendar again")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        ok(fr.locator("#pickdialog").is_hidden() and pg.locator("#eventdialog[open]").count() == 1, "F1: Escape closes only the small calendar")
        fr.locator("#evform .psave").click(); pg.wait_for_timeout(1500)
        ok(main.event_links().get(cu, {}).get("to") == V, "F1: Save links it to the event picked")
        # I2: the (i) beside Calendar opens downwards, inside the pop-up
        pg.evaluate(f"openEvent('/event?uid={q(cu)}&month=2026-10')"); pg.wait_for_timeout(1200)
        fr.locator(".withinfo .infodot").hover(); pg.wait_for_timeout(150)
        tip = fr.locator(".withinfo .tip").bounding_box(); dot = fr.locator(".withinfo .infodot").bounding_box()
        ok(tip and tip["y"] >= dot["y"] + dot["height"] - 1, f"I2: the Calendar (i) opens downwards ({tip})")
        # F16 in the pop-up
        fr.locator(".evdelbtn").click(); pg.wait_for_timeout(300)
        ok(fr.locator(".askq").inner_text() == "Delete this event?" and fr.locator("#askdialog .asksub").inner_text() == "(It may be restored here or in History, Undo & Logs)"
           and fr.locator("#askdialog .pcancel").inner_text() == "No" and fr.locator("#askdialog .psave").inner_text() == "Yes", "F16: the pop-up asks the same, No | Yes")
        fr.locator("#askdialog .psave").click(); pg.wait_for_timeout(1500)
        ok(main.store.get_event(cu).deleted, "F16: Yes deletes it")
        # F13.2: the grey text follows the calendars ticked
        pg.click("#destinations .addwrap .plus"); pg.wait_for_timeout(300); pg.click(".pickdest[data-type=feed]"); pg.wait_for_timeout(300)
        ph = lambda: [pg.locator("#adddest .nameinput").get_attribute("placeholder"), pg.locator("#adddest .noteinput").get_attribute("placeholder")]
        first = ph()
        ok(first == [main.calendar_name(named[0]), "Trips and reserve days"], f"F13.2: Label and Notes show the top calendar's name and note {first}")
        pg.locator(f'#adddest input[name=sources][value="{named[0]}"]').uncheck(); pg.wait_for_timeout(100)
        ok(ph()[0] != first[0], f"F13.2: …and follow the calendars ticked {ph()}")
        t = pg.locator("#adddest .fstitle").bounding_box(); s_ = pg.locator("#adddest .fstream").bounding_box()
        ok(t and abs(t["x"] - s_["x"]) <= 1 and t["y"] + t["height"] <= s_["y"], "F13.1: the title is over the stream name")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
