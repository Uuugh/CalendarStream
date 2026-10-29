"""The theme suite (0.2.8-beta.9): the whole page checked against build_rules/theme.md, its look and its
interaction, in light and dark, on a computer and a phone. Each Clarification in theme.md has a check here
(named after it); a new Clarification gets its check in the same beta."""
import os, re, sys, threading, time
from datetime import datetime, timezone
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="", IMAGE_TAG="beta")
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
async def fake_download(url, *a, **k):
    time.sleep(0.3)
    return calsync.Download(200, body=FEED, debug={"url": url})
async def fake_check():
    r = {"checked": datetime.now(timezone.utc).isoformat(), "channel": "beta", "newest": main.__version__}
    main.store.set("update_check", r); return r
CLAR = open(os.path.join(os.path.dirname(HERE), "build_rules", "theme.md")).read().split("## Clarifications", 1)[1]
# One look per meaning (beta.14): every status word and the look it must have (theme.md, section 2). A word not
# listed here fails: add it, with its meaning, to theme.md and here.
MEANING = {"good": r"Healthy|Connected|Ready|In Google|Read by Google|Up to date|\d+ Rules?|\d+ Templates?",
           "run": r"Syncing…|Starting|Paused|Setup needed|Ready to connect|Ready to turn on|Not set up|Not checked|Update available|Not connected|Invited|Not read yet|\d+ to check",
           "warn": r"Sign-in rejected|Blocked|Error|Address missing|Client rejected|Sync problem|Unhealthy",
           "bad": r"Internal error|Sync problem|Update failed"}
# Words on the page (beta.14): click paths and short lines; no sentence over 20 words outside the (?) help
WORDS = r"""() => {
  const body = document.body.cloneNode(true);
  body.querySelectorAll('.helptip, #cal, .logwin, script, style, template, select, textarea, code, input').forEach(e => e.remove());
  const long = [];
  body.querySelectorAll('p, li, summary, label, .mnote, .gsteptext, .note, h3, dd, td').forEach(e => {
    if (e.querySelector('p, li, ul, ol, div')) return;
    e.textContent.split(/(?<=[.!?])\s+|\s+›\s+|\s+·\s+|\n/).forEach(x => { x = x.replace(/\s+/g, ' ').trim(); if (x.split(' ').length > 20) long.push(x); });
  });
  return {long: [...new Set(long)], chips: [...document.querySelectorAll('.chip')].map(c => [c.textContent.trim(), (c.className.match(/\b(good|warn|bad|run)\b/) || [''])[0]])};
}"""

# What the page must look like: measured in the browser
MEASURE = """() => {
  const R = e => e.getBoundingClientRect(), vis = e => !!e.offsetParent;
  const out = {heads: [], kinds: [], margins: [], lone: [], statusButtons: [], copy: [], words: []};
  document.querySelectorAll('.box.module').forEach(m => {
    const h = m.querySelector(':scope > .srchead'), k = h.querySelector('.srcleft > .srckind'), n = h.querySelector('.srcleft > .nameline');
    out.heads.push([m.id, Math.round(R(h).height)]);
    out.kinds.push([m.id, !!k && !!n && R(k).top < R(n).top, k ? parseFloat(getComputedStyle(k).fontSize) : 0, k ? getComputedStyle(k).borderTopStyle : '', !!(k && k.querySelector('input'))]);
  });
  // handles in the section's right margin: modules (Calendars, Feeds) and All Rules' lines
  document.querySelectorAll('.sortable.modules > .modrow, #rules .rulelist > .ruleline').forEach(row => {
    const sec = row.closest('section'), h = row.querySelector(':scope > .handle'), box = row.firstElementChild;
    const plus = sec.querySelector('.cardhead .plus, .shead .countbox');
    if (!vis(row)) return;
    out.margins.push([sec.id, Math.round(R(box).right), Math.round(R(plus).right), Math.round(R(h).left), Math.round(R(h).right), Math.round(R(sec).right)]);
  });
  document.querySelectorAll('.sortable, .rulelist').forEach(list => {
    const rows = list.querySelectorAll(':scope > .modrow, :scope > .ruleline');
    if (rows.length === 1) { const h = rows[0].querySelector(':scope > .handle'); if (h && vis(rows[0])) out.lone.push([list.closest('[id]').id, getComputedStyle(h).visibility]); }
  });
  document.querySelectorAll('.statusbox button, .statusbox a.btn').forEach(b => out.statusButtons.push([b.closest('[id]').id, b.className, b.querySelectorAll('.sn').length]));
  document.querySelectorAll('.copybtn').forEach(b => out.copy.push([b.closest('[id]') ? b.closest('[id]').id : '', !!b.closest('.inbox, .feed')]));
  document.querySelectorAll('.srcstatus').forEach(p => out.words.push(p.textContent.trim()));
  out.scroll = document.documentElement.scrollWidth;
  out.bg = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim();
  return out;
}"""

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(main, "download", fake_download), patch.object(main.updates, "check", fake_check):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8106, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8106", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    wid = seed.demo(c, csrf, main)
    c.post("/feed/tags", data={"csrf": csrf, "sid": wid, "name": "Work", "note": "Shared with the office"})
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for scheme in ("light", "dark"):
            for w in (1230, 390):
                pg = b.new_page(viewport={"width": w, "height": 900}, color_scheme=scheme, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
                errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.goto("http://127.0.0.1:8106/?month=2026-10"); pg.wait_for_timeout(500)
                for t in ("#rules > .cfgline .cfgtoggle", "#templates > .cfgline .cfgtoggle"):
                    pg.click(t)
                pg.wait_for_timeout(300)
                m = pg.evaluate(MEASURE); tag = f"{scheme} {w}px"
                ok(m["scroll"] <= w, f"[{tag}] no sideways scroll")
                ok(m["heads"] and all(h == 50 if w > 600 else h >= 50 for _, h in m["heads"]), f"[{tag}] module headers are 50 px (on a phone at least 50, the status lines under) {m['heads']}")
                # Clarification: module headers share one layout (kind over name)
                ok(all(k and n for _, k, *_x in m["kinds"] for n in [True]) and all(fs >= (17 if w > 600 else 15) and bs == "none" and not inp for _, _k, fs, bs, inp in m["kinds"]),
                   f"[{tag}] Clarification 'module headers': the kind (fixed text, 17 px (15 on a phone), no box) over the name {m['kinds']}")
                # Clarification: handles in the section's right margin
                if w > 600:
                    ok(m["margins"] and all(abs(box - plus) <= 1 and hl >= box and hr <= sr - 1 for _s, box, plus, hl, hr, sr in m["margins"]),
                       f"[{tag}] Clarification 'handles': modules and All Rules' lines as wide as the header (up to its +), handles in the margin {m['margins']}")
                ok(all(v == "hidden" for _, v in m["lone"]), f"[{tag}] no handle where there's nothing to reorder {m['lone']}")
                # Clarification: every button in a status box works like Sync Now
                ok(m["statusButtons"] and all("syncnow" in cls and n == 4 or "syncnow" in cls and n == 5 or "upgradebtn" in cls for _, cls, n in m["statusButtons"]),
                   f"[{tag}] Clarification 'status-box buttons': each is a Sync Now (its states) {m['statusButtons']}")
                # Clarification: status words
                ok(all(re.match(r"^(|Last synced .+|Sync failed .+|Last read( by Google)? .+|Last checked .+)$", t) for t in m["words"]) and "Last check was" not in pg.content(),
                   f"[{tag}] Clarification 'status words': Last synced / Sync failed / Last read / Last checked {m['words']}")
                # Clarification: Copy buttons sit inside their field
                ok(all(inside for _, inside in m["copy"]), f"[{tag}] Clarification 'Copy': inside its field {m['copy']}")
                # Clarification: Light is the Soft palette
                if scheme == "light":
                    ok(m["bg"] == "#f7f6f3", f"[{tag}] Clarification 'Light = Soft': --bg {m['bg']}")
                ok(not errs, f"[{tag}] no script errors {errs}")
                if w > 600 and scheme == "light":
                    # Clarification: module-like sections: the count box top right, + bottom right (beta.11)
                    for sec, box in (("#rules", "#rulecount"), ("#templates", "#tplcount")):
                        r = pg.evaluate(f"""() => {{ const s = document.querySelector('{sec}').getBoundingClientRect(), p = document.querySelector('{sec} .sfoot .plus').getBoundingClientRect(),
                                         b = document.querySelector('{box}').getBoundingClientRect(); return [s.right - p.right, s.bottom - p.bottom, s.right - b.right, b.top - s.top, document.querySelectorAll('{sec} > .shead .plus').length]; }}""")
                        ok(17 <= r[0] <= 21 and r[1] <= 21 and 17 <= r[2] <= 21 and r[3] < 30 and r[4] == 0,
                           f"[{tag}] Clarification '+ in the corner': {sec} count box top right, + bottom right, none in the header {r}")
                    # Clarification: a note is a raised (i) after the name, only when there is one
                    ok(pg.locator(f"#src-{wid} .nameline .notedot").count() == 1 and "Shared with the office" in pg.locator(f"#src-{wid} .nameline .helptip").text_content()
                       and "Note:" not in pg.locator("#src-ccs .nameline .helptip").text_content(),
                       f"[{tag}] Clarification 'note': the (i) after the label says what it is, then the note when there is one")
                    # Clarification: rule colors (Google's 11) and "Color ■ (Name)"
                    ok(re.search(r'Color <span class="swatch"[^>]*></span> \(Tomato\)', pg.content()) is not None, f"[{tag}] Clarification 'rule colors': Color ■ (Name)")
                    # Interaction: status-box buttons answer at once, and keep answering after in-place redraws
                    for n in (1, 2):
                        sel = f"#src-{wid} .syncnow"
                        pg.click(sel); pg.wait_for_timeout(150)
                        ok(pg.get_attribute(sel, "data-state") in ("syncing", "done"), f"[{tag}] Sync Now press {n}: answers at once ({pg.get_attribute(sel, 'data-state')})")
                        pg.wait_for_timeout(4000)
                    pg.click("#menubtn"); pg.wait_for_timeout(300)
                    for n in (1, 2):
                        pg.click("#updates .checknow"); pg.wait_for_timeout(350)
                        fade = pg.evaluate("getComputedStyle(document.querySelector('#updates .statusbox .chip')).opacity")
                        ok(pg.get_attribute("#updates .checknow", "data-state") == "syncing" and float(fade) < 0.1,
                           f"[{tag}] Check now press {n}: Checking… at once, the status word faded under it (multi-button, {fade})")
                        pg.wait_for_timeout(3800)
                    # Clarification: a box means you can change it (Updates' title and channel are plain text)
                    bx = pg.evaluate("""() => [...document.querySelectorAll('#updates .srcleft > *')].map(e => getComputedStyle(e).borderTopColor + '|' + getComputedStyle(e).backgroundColor)""")
                    ok(all(x.endswith("rgba(0, 0, 0, 0)") for x in bx), f"[{tag}] Clarification 'a box means you can change it': Updates' fixed text has no box {bx}")
                    # Clarification: one look per meaning; in-page words are click paths
                    wd = pg.evaluate(WORDS)
                    wrong = [(t, k) for t, k in wd["chips"] if not re.fullmatch(MEANING.get(k, "(?!)"), t)]
                    ok(wd["chips"] and not wrong, f"[{tag}] Clarification 'one look per meaning': each status word has its meaning's look (wrong: {wrong})")
                    ok(not wd["long"], f"[{tag}] Clarification 'click paths': no sentence over 20 words on the page (outside the (?)) {wd['long']}")
                pg.close()
        # Clarification: no handle with nothing to reorder (one feed)
        for d in main.destinations()[1:]:
            c.post("/destinations/remove", data={"csrf": csrf, "did": d["id"]})
        pg = b.new_page(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg.goto("http://127.0.0.1:8106/?month=2026-10"); pg.wait_for_timeout(400)
        ok(len(main.destinations()) == 1 and pg.evaluate("getComputedStyle(document.querySelector('#destinations .modrow > .handle')).visibility") == "hidden",
           "Clarification 'handles': a lone feed has no handle")
        # Clarification: Close's triangles point up; Expand's point at the words
        pg.click("#rules > .cfgline .cfgtoggle"); pg.wait_for_timeout(250)
        rot = pg.evaluate("""() => getComputedStyle(document.querySelector('#rules > .cfgline .arr')).transform""")
        ok(rot.startswith("matrix(") and rot.split(",")[1].strip().startswith("-1"), f"Clarification 'Close points up': Close's triangle turned up ({rot})")
        # Clarification: an opened event: Close on the left, its icons on the right
        ev = pg.locator("#cal details.ev").first
        ev.locator("summary").click(); pg.wait_for_timeout(200)
        r = pg.evaluate("""() => { const d = [...document.querySelectorAll('#cal details.ev')].find(x => x.open), t = d.querySelector('.evtools').getBoundingClientRect(),
                          c = d.querySelector('.evclose').getBoundingClientRect(), i = d.querySelector('.evicons').getBoundingClientRect();
                          return [Math.round(c.left - t.left), Math.round(t.right - i.right), d.querySelectorAll('.evicons .evlinkto').length,
                                  Math.abs((i.top + i.bottom) / 2 - (c.top + c.bottom) / 2) <= 3 || i.bottom <= c.top + 1]; }""")
        ok(r[0] <= 2 and r[1] <= 2 and r[2] == 1 and r[3], f"Clarification 'event tools': Close at the bottom left, the icons (with Link) at the right, beside it or on a line above {r}")
        # Clarification: pop-ups: dark backdrop, 200 ms fade and scale-up; the theme's Cancel | Save
        ev.locator(".evedit").click(); pg.wait_for_timeout(700)
        bd = pg.evaluate("""() => { const d = document.getElementById('eventdialog'); return [getComputedStyle(d, '::backdrop').backgroundColor, getComputedStyle(d).animationName, getComputedStyle(d).animationDuration]; }""")
        ok(bd[0] == "rgba(0, 0, 0, 0.55)" and bd[1] == "popin" and bd[2] == "0.2s", f"Clarification 'pop-ups': dark backdrop, 200 ms fade and scale-up {bd}")
        fr = pg.frame_locator("#eventdialog iframe")
        pr = fr.locator(".pairbtns").bounding_box()
        ok(pr and round(pr["width"]) == 130 and round(pr["height"]) == 34, f"…its Cancel | Save is the 130 × 34 pair ({pr})")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        # Clarification: adding ends with Cancel | Save
        pg.click("#sources .cardhead .plus"); pg.click('#addsrc .preset[data-preset="local"]'); pg.wait_for_timeout(200)
        ok(pg.locator("#addsrc-local .pairbtns .pcancel").is_visible() and pg.locator("#addsrc-local .pairbtns .psave").is_visible()
           and pg.locator("#addsrc button", has_text="Add").count() == 0, "Clarification 'Cancel | Save when adding': + Add a calendar ends with Cancel | Save")
        pg.click("#addsrc-local .pcancel"); pg.wait_for_timeout(1000)
        ok(pg.locator("#addsrc").is_hidden(), "…Cancel closes it")
        # --- 0.2.8-beta.15 Clarifications -----------------------------------------------------------
        # every + opens a centred pop-up, the page dimmed and blurred behind it
        for plus, dlg in (("#sources .cardhead .plus", "#addsrc"), ("#destinations .cardhead .plus", "#adddestpop")):
            pg.click(plus); pg.wait_for_timeout(350)
            r = pg.evaluate(f"""() => {{ const d = document.querySelector('{dlg}'), b = d.getBoundingClientRect();
                return [d.open && d.matches(':modal'), Math.abs((b.left + b.right) / 2 - innerWidth / 2) <= 2, getComputedStyle(d, '::backdrop').backdropFilter]; }}""")
            ok(r[0] and r[1] and "blur" in r[2], f"Clarification '+ pop-ups': {plus} opens a centred pop-up, the page blurred behind {r}")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        pg.click("#templates > .cfgline .cfgtoggle"); pg.wait_for_timeout(200)
        pg.click("#templates .sfoot .plus"); pg.wait_for_timeout(350)
        ok(pg.evaluate("document.getElementById('tpladd').matches(':modal')"), "…Event Templates' + too")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        r = pg.evaluate("""() => { const m = document.querySelector('.box.module'), cs = getComputedStyle(m), n = m.querySelector('.srcname');
            return [cs.borderTopWidth, cs.paddingTop, cs.paddingLeft, getComputedStyle(n).borderTopColor, getComputedStyle(n).backgroundColor,
                    document.querySelectorAll('.box.module').length, document.querySelectorAll('.box.module .nameline .notedot').length,
                    document.querySelectorAll('input[type=color]').length,
                    [...document.querySelectorAll('.palpop')].every(p => p.querySelectorAll('.pal:not(.nocolor)').length === 11),
                    [...document.querySelectorAll('main input[type=date]')].every(i => (i.closest('.daterange') && i.closest('.daterange').querySelector('.rangeall')) || i.closest('.destdates')),
                    [...document.querySelectorAll('.box.src .cfgbody')].every(c => { const f = c.querySelector('form.importrow'); return f && f.querySelector('.filefield') && f.lastElementChild.tagName === 'BUTTON'; })]; }""")
        ok(r[0] == "2px" and r[1] == "5px" and r[2] == "9px", f"Clarification '2 px border': modules have a 2 px border, 1 px less padding {r[:3]}")
        ok(r[3] in ("rgba(0, 0, 0, 0)", "transparent") and r[4] == "rgba(0, 0, 0, 0)", f"Clarification 'label': a folded module's label is plain text {r[3:5]}")
        ok(r[5] and r[5] == r[6], f"Clarification '(i) is info': every module has its (i) after the label ({r[6]} of {r[5]})")
        ok(r[7] == 0 and r[8], f"Clarification 'one palette': no free color picker; every color box offers Google's 11 {r[7:9]}")
        ok(r[9], "Clarification 'date ranges': every date range on the page has From | To | All")
        ok(r[10], "Clarification 'import row': every calendar has the import row (heading, file field, …, the button last)")
        src = open(os.path.join(os.path.dirname(HERE), "app", "templates", "page.js")).read() + open(os.path.join(os.path.dirname(HERE), "app", "templates", "event.html")).read()
        ok(not re.search(r"(?<![\w.])(alert|confirm|prompt)\(", src), "Clarification 'no browser dialogs': no alert / confirm / prompt in the page's scripts")
        ok("cls: 'danger'" not in src and "cls: 'danger ghost'" not in src,
           "Clarification 'one look per meaning': a pop-up's red choice is a red fill ('danger solid') or red words ('ghost danger'), never red on blue")
        # emoji: ten a line, scrolling, a search on top
        pg.click("#rules > .cfgline .cfgtoggle") if pg.locator("#rules .sfoot .newrule").is_hidden() else None
        pg.click("#rules .sfoot .newrule"); pg.wait_for_timeout(300)
        pg.evaluate("() => { const s = document.querySelector('#ruledialog .atype'); s.value = 'emoji'; s.dispatchEvent(new Event('change', {bubbles:true})); }")
        pg.click("#ruledialog .emofind"); pg.wait_for_timeout(700)
        r = pg.evaluate("""() => { const g = document.querySelector('#ruledialog .emogrid'), cs = getComputedStyle(g), f = document.querySelector('#ruledialog .emofind'), fs = getComputedStyle(f);
            return [cs.gridTemplateColumns.split(' ').length, cs.overflowY, f.placeholder, g.querySelectorAll('.emo').length,
                    parseFloat(fs.borderTopLeftRadius) < parseFloat(fs.height) / 2 - 0.5]; }""")
        ok(r[0] == 10 and r[1] == "auto" and r[2] == "Search for more emojis" and r[3] > 1000 and r[4],
           f"Clarification 'emoji': ten a line, scrolling, opened from a rounded search field (0.2.8-beta.17) {r}")
        pg.evaluate("document.getElementById('ruledialog').close()")
        # a deleted event: struck through, greyed, where, Restore
        uid = pg.locator("#cal details.ev:not(.custom)").first.get_attribute("data-uid")
        c.post("/event/delete", data={"csrf": csrf, "uid": uid})
        pg.reload(); pg.wait_for_timeout(500)
        d = pg.locator(f'#cal details.ev[data-uid="{uid}"]').first
        r = pg.evaluate("""uid => { const d = document.querySelector(`#cal details.ev[data-uid="${CSS.escape(uid)}"]`), s = d.querySelector('summary');
            return [d.classList.contains('deleted'), getComputedStyle(s).textDecorationLine, getComputedStyle(d).filter, !!d.querySelector('.evrestore'), d.querySelector('.delnote').textContent]; }""", uid)
        ok(r[0] and "line-through" in r[1] and "grayscale" in r[2] and r[3] and "Deleted in CalendarStream" in r[4], f"Clarification 'deleted events': struck through, greyed, where, Restore {r}")
        b.close()
    # Each Clarification in theme.md is covered above (by its key word)
    keys = {"handles": "Module handles", "module headers": "module headers share one layout", "status words": "Status words",
            "+ in the corner": "Module-like sections", "a box means you can change it": "A box means you can change it",
            "Copy": "Copy buttons", "rule colors": "rule's color is one of Google", "Light = Soft": "Light is the Soft palette",
            "status-box buttons": "The status box is a multi-button", "note": "raised (i)",
            "Cancel | Save when adding": "Adding something", "reload after an update (suite 42)": "After an update the page reloads",
            "Close points up": "Close's triangles point up", "pop-ups": "Pop-ups: a dark backdrop", "event tools": "An opened event: Close in the bottom left",
            "event colors (suite 45)": "Events show the color Google shows", "rule summaries": "Rule lines say what the rule does",
            "fields (suite 46: 34 px, layout)": "Fields everywhere, pop-ups included", "+ in a corner (suite 46)": "Every section's + is in a corner",
            "credentials trash (suite 46)": "A credentials row", "one line of settings (suite 46)": "A row of settings that belong together",
            "next push (suite 46)": "Next push instantaneous", "one action, one state (suite 47)": "One action, one state",
            "a working Settings group shows everything (suite 47)": "A Settings",
            "one look per meaning": "One look per meaning", "click paths": "In-page instructions are click paths",
            "date ranges": "Every date range has All", "no browser dialogs": "No browser alert or confirm boxes",
            "(i) is info": "(i) is info", "+ pop-ups": "Every + opens a centred pop-up", "2 px border": "Modules have a 2 px border",
            "label": "A module's name is its label", "one palette": "One color palette everywhere",
            "deleted events": "A deleted event stays struck through", "import row": "Importing a calendar file is one row",
            "emoji": "Emoji: the common ones"}
    bullets = [x for x in re.split(r"\n- ", CLAR) if x.strip()][1:]
    unchecked = [x.split("\n")[0][:60] for x in bullets if not any(k in " ".join(x.split()) for k in keys.values())]
    ok(not unchecked, f"every Clarification in theme.md has a check in this suite (none unchecked: {unchecked})")
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
