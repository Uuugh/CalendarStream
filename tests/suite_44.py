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
    const plus = sec.querySelector('.cardhead .plus, .shead .headplus');
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
                pg = b.new_page(viewport={"width": w, "height": 900}, color_scheme=scheme, http_credentials={"username": "t", "password": "password1"})
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
                    # Clarification: + in the top right corner of module-like sections, after the count box
                    for sec, box in (("#rules", "#rulecount"), ("#templates", "#tplcount")):
                        r = pg.evaluate(f"""() => {{ const s = document.querySelector('{sec}').getBoundingClientRect(), p = document.querySelector('{sec} > .shead .headplus').getBoundingClientRect(),
                                         b = document.querySelector('{box}').getBoundingClientRect(); return [s.right - p.right, p.left - b.right, p.top - s.top]; }}""")
                        ok(17 <= r[0] <= 21 and 0 <= r[1] <= 12 and r[2] < 30, f"[{tag}] Clarification '+ in the corner': {sec} + after the count box, top right {r}")
                    # Clarification: a note is a raised (i) after the name, only when there is one
                    ok(pg.locator(f"#src-{wid} .nameline .notedot").count() == 1 and pg.locator("#src-ccs .nameline .notedot").count() == 0,
                       f"[{tag}] Clarification 'note': (i) after the name only when there's a note")
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
                        pg.click("#updates .checknow"); pg.wait_for_timeout(150)
                        ok(pg.get_attribute("#updates .checknow", "data-state") == "syncing", f"[{tag}] Check now press {n}: Checking… at once")
                        pg.wait_for_timeout(3800)
                    # Clarification: a box means you can change it (Updates' title and channel are plain text)
                    bx = pg.evaluate("""() => [...document.querySelectorAll('#updates .srcleft > *')].map(e => getComputedStyle(e).borderTopColor + '|' + getComputedStyle(e).backgroundColor)""")
                    ok(all(x.endswith("rgba(0, 0, 0, 0)") for x in bx), f"[{tag}] Clarification 'a box means you can change it': Updates' fixed text has no box {bx}")
                pg.close()
        # Clarification: no handle with nothing to reorder (one feed)
        for d in main.destinations()[1:]:
            c.post("/destinations/remove", data={"csrf": csrf, "did": d["id"]})
        pg = b.new_page(viewport={"width": 1230, "height": 900}, http_credentials={"username": "t", "password": "password1"})
        pg.goto("http://127.0.0.1:8106/?month=2026-10"); pg.wait_for_timeout(400)
        ok(len(main.destinations()) == 1 and pg.evaluate("getComputedStyle(document.querySelector('#destinations .modrow > .handle')).visibility") == "hidden",
           "Clarification 'handles': a lone feed has no handle")
        # Clarification: adding ends with Cancel | Save
        pg.click("#sources .cardhead .plus"); pg.click('#addsrc .preset[data-preset="local"]'); pg.wait_for_timeout(200)
        ok(pg.locator("#addsrc-local .pairbtns .pcancel").is_visible() and pg.locator("#addsrc-local .pairbtns .psave").is_visible()
           and pg.locator("#addsrc button", has_text="Add").count() == 0, "Clarification 'Cancel | Save when adding': + Add a calendar ends with Cancel | Save")
        pg.click("#addsrc-local .pcancel"); pg.wait_for_timeout(1000)
        ok(pg.locator("#addsrc").is_hidden(), "…Cancel closes it")
        b.close()
    # Each Clarification in theme.md is covered above (by its key word)
    keys = {"handles": "Module handles", "module headers": "module headers share one layout", "status words": "Status words",
            "+ in the corner": "Module-like sections", "a box means you can change it": "A box means you can change it",
            "Copy": "Copy buttons", "rule colors": "rule's color is one of Google", "Light = Soft": "Light is the Soft palette",
            "status-box buttons": "Every button in a status box", "note": "raised (i)",
            "Cancel | Save when adding": "Adding something", "reload after an update (suite 42)": "After an update the page reloads"}
    bullets = [x for x in re.split(r"\n- ", CLAR) if x.strip()][1:]
    unchecked = [x.split("\n")[0][:60] for x in bullets if not any(k in " ".join(x.split()) for k in keys.values())]
    ok(not unchecked, f"every Clarification in theme.md has a check in this suite (none unchecked: {unchecked})")
    srv.should_exit = True
print("FAILED:", fails) if fails else print("ALL PASSED")
