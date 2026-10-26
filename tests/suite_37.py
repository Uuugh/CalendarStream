"""0.2.8-beta.3 tests: rule conflicts (F4.2), Apply to as a drop-down with its defaults (F4.1), a lone ")"
pairs itself (F), Change to a length shows its field (I), linked events (F3.2), removing a calendar
keeps / merges / deletes its events (F3.1), converted rules shared (I), Settings (F2), the color box only
while expanded, status lines on the right, (?) next to its word, Sync Now filling the status box (F1.2)."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, HERE)
from datetime import timedelta
from unittest.mock import patch
import json, uvicorn, httpx, seed
from app import main, calsync, links, rules as R
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
MODE = {"slow": 0}
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    import asyncio
    await asyncio.sleep(MODE["slow"])
    return calsync.Download(200, body=FEED, debug={"url": url})

# --- Conflicts and links on their own -------------------------------------------------------------
def rule(rid, conds, actions, apply="all"):
    return R.normalize({"id": rid, "conds": conds, "actions": actions, "apply": apply})
t = lambda v, op="word": {"type": "text", "op": op, "value": v}
red, green = {"type": "color", "color": "#d50000"}, {"type": "color", "color": "#0b8043"}
rl = [rule("a1", [t("RDO")], [red], ["ccs"]), rule("a2", [t("rdo")], [green, {"type": "emoji", "emoji": "x"}], "all"),
      rule("a3", [t("VAC")], [red], ["ccs"]), rule("a4", [t("VAC")], [red], ["f000001"]), rule("a5", [t("VAC")], [red], ["ccs", "f000001"])]
found = R.conflicts(rl, ["ccs", "f000001"])
ok([(c["kind"], c["a"], c["b"], c.get("action")) for c in found] == [("shadowed", "a1", "a2", "color"), ("duplicate", "a3", "a5", None), ("duplicate", "a4", "a5", None)]
   and found[0]["calendars"] == ["ccs"], f"conflicts: a lower color never shows (same events, case aside); duplicates where they overlap ({found})")
ok(R.conflicts(rl, ["ccs", "f000001"], {R.conflict_key(found[0])})[0]["kind"] == "duplicate", "a conflict kept as is isn't shown again")
ok(R.conflicts([rule("b1", [], [red]), rule("b2", [t("X")], [green])], ["ccs"])[0]["b"] == "b2", "a rule with no conditions above matches everything")
ok(R.merge(rl[2], rl[3])["apply"] == ["ccs", "f000001"] and R.merge(rl[2], rl[1])["apply"] == "all", "merging duplicates joins their calendars")
ok(links.moved_by("2026-10-14T09:00:00-04:00", "2026-10-14T10:30:00-04:00") == timedelta(minutes=90) and links.moved_by("2026-10-14", "2026-10-14T09:00:00-04:00") is None
   and links.shifted("2026-10-14", "2026-10-15", timedelta(days=2)) == ("2026-10-16", "2026-10-17"), "links: how far an event moved; moving all-day by days")

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8093, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8093", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    wid = seed.demo(c, csrf, main)
    L = main.source_ids()[0]
    # I: rules converted from beta.1 that every calendar used are shared (and so in Local's list too)
    main.store.set("rules", [{**r, "apply": ["ccs", wid]} if r["title"] == "Items without an end time" else r for r in main.all_rules()])
    main.store.delete("rules_shared_b3"); main.share_converted_rules()
    ok(next(r for r in main.all_rules() if r["title"] == "Items without an end time")["apply"] == "all"
       and any(r["title"] == "Items without an end time" for r in main.source_rules(L)), "I: a converted rule every calendar used is for All calendars, so Local lists it")
    ok(R.from_v3([{"id": "x1", "type": "color", "tag": "A", "color": "#d50000"}], {"ccs": ["x1"]}, ["ccs"])[0]["apply"] == "all", "…also when there was only one calendar")
    # F4.2: conflicts in All Rules, settled there
    dup = seed.rule(c, csrf, "", [seed.text("rdo")], [{"type": "color", "color": "#0b8043"}], ["ccs"])
    p = c.get("/").text
    box = p[p.index('id="ruleconflicts"'):]; box = box[:box.index('<div class="rulelist')]
    ok("never sets the color" in box and "Put “Text whole word “rdo” → Color (Basil)” first" in box and "Keep as is" in box and "to check" in p,
       "All Rules says the new RDO color never shows, with what to do")
    key = re.search(r'name="key" value="([^"]+)"', box)[1]
    ok(post("/rules/resolve", key=key, how="up").status_code == 303 and [r["id"] for r in main.source_rules("ccs")][0] == dup, "Put it first: it moves above")
    p = c.get("/").text
    key = re.search(r'id="ruleconflicts".*?name="key" value="([^"]+)"', p, re.S)[1]
    post("/rules/resolve", key=key, how="drop")
    ok(not any(r["id"] != dup and r["conds"] and r["conds"][0].get("value") == "RDO" for r in main.all_rules()), "Take the color out: the other rule had only that, so it's gone")
    twin = seed.rule(c, csrf, "", [seed.text("rdo")], [{"type": "color", "color": "#0b8043"}], ["ccs", wid])
    p = c.get("/").text
    ok("is the same as" in p and "Merge them" in p, "duplicates: Merge them")
    key = re.search(r'id="ruleconflicts".*?name="key" value="([^"]+)"', p, re.S)[1]
    post("/rules/resolve", key=key, how="merge")
    merged = [r for r in main.all_rules() if r["conds"] and r["conds"][0].get("value") == "rdo"]
    ok(len(merged) == 1 and set(merged[0]["apply"]) == {"ccs", wid}, "…one rule for both calendars")
    ok(post("/rules/resolve", key="nope", how="up").status_code == 400, "an old conflict can't be settled twice")
    # F3.2: linked events
    trip = next(e for e in main.store.load_events("ccs") if e.title.startswith("UA") and not e.all_day and e.start[:7] == "2026-10")
    r = post("/event/save", month="2026-10", title="Pack", start_date=trip.start[:10], start_time="06:00", end_date=trip.start[:10], end_time="06:30",
             source=L, link_to=trip.uid, link_delete="1", link_move="1")
    pack = next(e for e in main.store.load_events(L) if e.title == "Pack")
    ok(main.event_links()[pack.uid]["to"] == trip.uid and main.event_links()[pack.uid]["src"] == "ccs", "an added event linked to a trip")
    e = c.get(f"/event?uid={pack.uid}&month=2026-10").text
    ok('id="linkbox"' in e and f'<option value="{trip.uid}" selected' in e and 'class="iconbtn linkbtn on"' in e, "its page shows the link (icon on)")
    ok("Linked to “" + trip.title + "”" in c.get("/?month=2026-10").text, "…and its details on the calendar")
    # the trip moves 2 h later (an edit, as a download would): Pack moves with it
    f = main._form_values(trip)
    s_, e_ = main.datetime.fromisoformat(trip.start) + timedelta(hours=2), main.datetime.fromisoformat(trip.end) + timedelta(hours=2)
    post("/event/save", uid=trip.uid, month="2026-10", title=trip.title, start_date=f"{s_:%Y-%m-%d}", start_time=f"{s_:%H:%M}", end_date=f"{e_:%Y-%m-%d}", end_time=f"{e_:%H:%M}")
    pack2 = main.store.get_event(pack.uid)
    ok(main.datetime.fromisoformat(pack2.start) - main.datetime.fromisoformat(pack.start) == timedelta(hours=2), f"Move with it: 2 h later too ({pack.start} → {pack2.start})")
    post("/event/delete", uid=trip.uid)
    ok(main.store.get_event(pack.uid) is None and pack.uid not in main.event_links(), "Delete with it: hiding the trip deletes Pack")
    # linking a source's own event doesn't mark it edited
    other = next(e for e in main.store.load_events("ccs") if e.title == "RDO")
    ff = main._form_values(other)
    post("/event/save", uid=other.uid, month="2026-10", title=other.title, all_day="1", start_date=ff["start_date"], start_time="", end_date=ff["end_date"], end_time="", link_to=trip.uid)
    ok(other.uid not in main.store.get_edits(), "linking a source's event alone isn't an edit")
    # F3.1: removing a calendar
    work = [e for e in main.store.load_events(wid) if not e.hidden and e.origin != "rule"]
    color = main.calendar_color(wid)
    had = [d["id"] for d in main.destinations() if wid in d["sources"]]
    ok(post("/sources/remove", sid=wid, keep="local").status_code == 303 and wid not in main.source_ids(), "Remove Work, keeping its events…")
    new = next(x["id"] for x in main.sources() if x["type"] == "local" and main.calendar_name(x["id"]) == "Work")
    ok(len(main.store.load_events(new)) == len(work) and main.calendar_color(new) == color and had and all(new in main.destination(x)["sources"] for x in had),
       f"…in a Local calendar named Work, same color, same feeds ({len(work)} events)")
    ok(post("/sources/remove", sid=new, keep="merge", into=L).status_code == 303 and len(main.store.load_events(L)) >= len(work), "a Local calendar merged into another")
    ok(post("/sources/remove", sid=new, keep="nope").status_code == 400, "an unknown choice is refused")
    # F2: Settings
    p = c.get("/?menu=settings").text
    menu = p[p.index('id="menu"'):p.index('</header>')]
    ok(menu.count('class="okslot"') == 3 and 'action="/settings/admin-email" class="clientform watch"' in menu, "F2.1: Public address and Admin e-mail save like the login (✓ | ✕ ✓)")
    ok(">Check now<" in menu and "upgradebtn" not in menu, "no newer version: Check now")
    with patch.object(main.updates, "available", lambda: "9.9.9"):
        p = c.get("/?menu=settings").text
    menu = p[p.index('id="menu"'):p.index('</header>')]
    ok("upgradebtn" in menu and ">Check now<" not in menu, "F2.2: a newer version: Update instead of Check now")

    # --- In a browser -------------------------------------------------------------------------
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8093/?month=2026-10"); pg.wait_for_timeout(500)
        # (?) next to its word, everywhere
        pg.evaluate("document.querySelectorAll('.cfgtoggle[aria-expanded=false], .section .toggle[aria-expanded=false]').forEach(b => b.click())"); pg.wait_for_timeout(400)
        far = pg.evaluate("""() => [...document.querySelectorAll('.helpdot')].filter(d => d.offsetParent).map(d => {
            let p = d.previousSibling; while (p && p.nodeType === 3 && !p.textContent.trim()) p = p.previousSibling;
            if (!p) return 0; const rg = document.createRange(); rg.selectNode(p); return Math.round(d.getBoundingClientRect().left - rg.getBoundingClientRect().right); }).filter(x => x > 12)""")
        ok(not far, f"every (?) sits right after its word ({far})")
        # the color box: only while expanded
        pg.evaluate("document.querySelectorAll('.box.src .cfgtoggle[aria-expanded=true]').forEach(b => b.click())"); pg.wait_for_timeout(200)
        ok(pg.evaluate("getComputedStyle(document.querySelector('#src-ccs input.colorpick')).pointerEvents") == "none", "folded: the color box only shows the color")
        pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(150)
        ok(pg.evaluate("getComputedStyle(document.querySelector('#src-ccs input.colorpick')).pointerEvents") != "none", "expanded: it changes it")
        # status lines on the right
        R_ = pg.locator("#src-ccs .srcright").bounding_box(); S_ = pg.locator("#src-ccs .srcstatus").bounding_box()
        ok(abs((R_["x"] + R_["width"]) - (S_["x"] + S_["width"])) < 2, "Last check was successful … on the right")
        # Sync Now: the button fills the status box while it syncs
        MODE["slow"] = 1.5
        pg.click("#src-ccs .syncnow"); pg.wait_for_timeout(450)
        sb, bt = pg.locator("#src-ccs .statusbox").bounding_box(), pg.locator("#src-ccs .syncnow").bounding_box()
        ok(pg.evaluate("getComputedStyle(document.querySelector('#src-ccs .statusbox .chip')).opacity") == "0" and bt["height"] > sb["height"] - 12, f"F1.2: syncing: no Healthy, the button fills the box ({bt['height']:.0f}/{sb['height']:.0f})")
        MODE["slow"] = 0; pg.wait_for_timeout(4500)
        ok(pg.is_visible("#src-ccs .statusbox .chip"), "…then Healthy again")
        # F4.1: Apply to: a drop-down, starting with this calendar (from a module) or All (from All Rules)
        pg.click("#rules-ccs .addrule"); pg.click("#rules-ccs .rulemenu .newrule"); pg.wait_for_timeout(200)
        ok(pg.eval_on_selector_all("#ruledialog .rdapply input:checked", "i => i.map(x => x.value)") == ["ccs"] and "United CCS Schedule" in pg.inner_text("#ruledialog .ddbtn"),
           "a rule made in a calendar starts with that calendar")
        pg.click("#ruledialog .ddbtn"); pg.wait_for_timeout(100)
        ok(pg.is_visible("#ruledialog .ddmenu") and pg.locator("#ruledialog .ddmenu .ddsw").count() == len(main.sources()) + 1, "the drop-down lists every calendar with its color")
        pg.click(f'#ruledialog .ddmenu input[value="{L}"]'); pg.click('#ruledialog .ddmenu input[value="all"]'); pg.wait_for_timeout(50)
        ok(pg.eval_on_selector_all("#ruledialog .rdapply input:checked", "i => i.map(x => x.value)") == ["all"], "All calendars takes the others out")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        ok(pg.eval_on_selector("#ruledialog", "d => d.open") and not pg.is_visible("#ruledialog .ddmenu"), "Escape closes the menu first")
        # I: Change → to a length shows its field
        pg.locator("#ruledialog .act .atype").select_option("change"); pg.wait_for_timeout(50)
        pg.locator("#ruledialog .act .ato").select_option("length"); pg.wait_for_timeout(50)
        ok(pg.is_visible("#ruledialog .act .amin") and pg.input_value("#ruledialog .act .amin") == "1:00", "Change to a length of: its field appears")
        pg.locator("#ruledialog .act .atype").select_option("event"); pg.wait_for_timeout(50)
        pg.locator("#ruledialog .act .atpl").select_option(""); pg.wait_for_timeout(50)
        ok(pg.is_visible("#ruledialog .act .anew.title"), "Create event → New event…: its fields appear")
        # a lone ")" gets its "("
        pg.fill("#ruledialog .cond .cval", "RDO"); pg.select_option("#ruledialog .cond .cjoin", "or"); pg.wait_for_timeout(50)
        pg.locator("#ruledialog .cond").nth(1).locator(".cval").fill("VAC")
        pg.locator("#ruledialog .cond").nth(1).locator(".brk.spare.close").click(); pg.wait_for_timeout(100)
        ok(pg.locator("#ruledialog .cond").nth(0).get_attribute("data-open") == "1" and pg.locator("#ruledialog .cond").nth(0).locator(".brk.on.open.flash").count() == 1
           and not pg.eval_on_selector("#ruleform", "f => f.classList.contains('unbalanced')"), "a ) with no ( before it: a ( is added on the first line, and flashes")
        order = pg.locator("#ruledialog .cond").nth(1).locator(".brks.close .brk").evaluate_all("bs => bs.map(b => b.classList.contains('on') ? 'on' : 'spare')")
        ok(order == ["on", "spare"], f"the line ends with the chosen ) then the grey one ({order})")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
        pg.click("#rules .sfoot .newrule"); pg.wait_for_timeout(150)
        ok(pg.eval_on_selector_all("#ruledialog .rdapply input:checked", "i => i.map(x => x.value)") == ["all"], "a rule made in All Rules starts with All calendars")
        pg.keyboard.press("Escape")
        # F3.1: the remove dialog
        pg.click("#src-ccs .removecal"); pg.wait_for_timeout(150)
        ok(pg.locator("#removedialog[open]").count() == 1 and pg.is_checked('#removedialog input[value="local"]') and
           pg.eval_on_selector('#removedialog .rminto option[value="ccs"]', "o => o.disabled"), "Remove asks: keep (the default), add to another calendar, or delete")
        pg.click("#removedialog [data-close]"); pg.wait_for_timeout(100)
        ok(pg.locator("#removedialog[open]").count() == 0 and "ccs" in main.source_ids(), "Cancel removes nothing")
        # F3.2: the link icon on the event page
        pg.goto("http://127.0.0.1:8093/event?date=2026-10-14&month=2026-10"); pg.wait_for_timeout(300)
        ok(not pg.is_visible("#linkbox"), "a new event: not linked")
        pg.click("#linkbtn"); pg.wait_for_timeout(100)
        ok(pg.is_visible("#linkbox") and pg.locator("#link_to option").count() > 5 and pg.is_checked("input[name=link_delete]") and pg.is_checked("input[name=link_move]"),
           "the link icon: Linked to (events around it), Delete with it, Move with it")
        ok(not errs, f"no script errors {errs}")
        b.close()
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
