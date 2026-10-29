"""0.2.8-beta.1 tests: the theme (IBM Plex fonts served here, Material Symbols, rounded rectangles only),
modules with 50 px headers, Expand in a folded module's bottom border, Sync Now's states, (?) raised
after its word, icon-only ✕ | ✓ for inline edits, "Cancelled", License & Attribution."""
import glob, os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from unittest.mock import patch
import uvicorn, httpx
from app import main, calsync, icons
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
FEED = open(os.path.join(HERE, "data", "work.ics"), "rb").read()
MODE = {"fail": False, "slow": 0}
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    import asyncio
    await asyncio.sleep(MODE["slow"])
    if MODE["fail"]:
        raise calsync.SourceError("The feed answered 500")
    return calsync.Download(200, body=FEED, debug={"url": url})

# Icons: every icon the templates and code name is vendored; nothing else is drawn by hand.
src = "".join(open(f, encoding="utf-8").read() for f in glob.glob(REPO + "/app/templates/*.html") + [REPO + "/app/main.py"])
names = set(re.findall(r'icon(?:_mask)?\("([a-z_\-]+)"', src)) | set(re.findall(r'icons\.svg\("([a-z_\-]+)"', src))
missing = [n for n in names if n not in icons._paths()]
ok(names and not missing, f"every icon used is a vendored Material Symbol ({len(names)} used; missing {missing})")
try:
    icons.svg("no_such_icon"); ok(False, "an unknown icon name raises")
except KeyError:
    ok(True, "an unknown icon name raises KeyError (a typo shows up)")
ok(str(icons.mask("check")).startswith('url("data:image/svg+xml,%3Csvg') and "<" not in str(icons.mask("check")), "icon masks are percent-encoded data URLs")
tpl = "".join(open(f, encoding="utf-8").read() for f in glob.glob(REPO + "/app/templates/*.html"))
ok("999px" not in tpl and "border-radius:50%" not in tpl, "no pills or circles: rounded rectangles only")
ok('viewBox="0 0 16 16"' not in tpl and 'viewBox="0 0 24 24"' not in tpl and 'viewBox="0 0 18 18"' not in tpl, "no hand-drawn, Bootstrap or Feather icons left")

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8097, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url="http://127.0.0.1:8097", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    main.logins.save_ccs("U123456", "pw12345"); main.state.last_auth_ok = True
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    main.state.status = "ok"
    c.post("/sources/add", data={"csrf": csrf, "type": "ics", "url": "https://example.org/work.ics", "name": "Work", "note": "Office"})
    wid = main.source_ids()[-1]
    main.store.set("public_url", "https://cal.example.com")
    c.post("/destinations/add", data={"csrf": csrf, "type": "feed", "name": "Everything"})
    p = c.get("/").text
    # Fonts: served here, without a login, and used by every page
    anon = httpx.Client(base_url="http://127.0.0.1:8097")
    f = anon.get("/static/fonts/ibm-plex-sans-latin-400-normal.woff2")
    ok(f.status_code == 200 and f.content[:4] == b"wOF2", "IBM Plex Sans is served from /static (no login needed)")
    ok(anon.get("/static/fonts/ibm-plex-mono-latin-400-normal.woff2").status_code == 200 and anon.get("/static/fonts/OFL.txt").status_code == 200, "IBM Plex Mono and its licence too")
    ok(anon.get("/static/../main.py").status_code == 404, "nothing outside /static is served")
    ok('font-family:"IBM Plex Sans"' in p and "fonts.googleapis" not in p and "--font:\"IBM Plex Sans\"" in p.replace("--font:&#34;", "--font:\""), "the page uses IBM Plex, from this server only")
    ok(all(re.search(r'<input[^>]*name="%s"[^>]*class="code"|<input[^>]*class="code"[^>]*name="%s"' % (n, n), p) for n in ("uid", "url")), "the Username and links are in IBM Plex Mono (class code)")
    ok('<input type="text" class="code" id="fcid" name="client_id"' in p or 'name="client_id"' not in p, "the client ID is in IBM Plex Mono")
    tokens = c.get("/subscribe/" + main.destinations("feed")[0]["token"]).text
    ok("IBM Plex Sans" in tokens and ">content_copy<" not in tokens and '<symbol id="mi-content_copy" viewBox="0 -960 960 960"' in tokens and '<use href="#mi-content_copy"' in tokens, "the subscribe page has the fonts and icons too")
    # Footer and wording
    ok('href="https://github.com/Uuugh/CalendarStream#license--attribution"' in p and ">License & Attribution<" in p, "F1.5: License & Attribution in the footer")
    ok("Canceled" not in p and 'data-done="Cancelled"' in p, "F1.3: Cancelled (two Ls)")
    # Status API: Google's sync is reported; /google/sync answers the page's script
    j = c.get("/api/status").json()
    ok(set(j["google"]) == {"connected", "running", "pending", "error"}, "/api/status reports Google's sync")
    r = c.post("/google/sync", data={"csrf": csrf}, headers={"X-CS-Async": "1"})
    ok(r.status_code == 200 and r.json() == {"ok": True}, "/google/sync answers the page's script with JSON")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for scheme in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1400, "height": 900}, color_scheme=scheme, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("http://127.0.0.1:8097/?view=month"); pg.wait_for_timeout(600)
            fam = pg.evaluate("getComputedStyle(document.body).fontFamily")
            # (fonts load when first used; Mono may not be on screen yet, so ask for it)
            loaded = pg.evaluate("Promise.all([document.fonts.load('14px \"IBM Plex Sans\"'), document.fonts.load('14px \"IBM Plex Mono\"')]).then(r => r.every(x => x.length > 0))")
            ok(fam.startswith('"IBM Plex Sans"') and loaded, f"{scheme}: IBM Plex Sans and Mono load ({fam[:30]})")
            mono = pg.evaluate("getComputedStyle(document.querySelector('.ccsform input[name=uid]')).fontFamily")
            ok(mono.startswith('"IBM Plex Mono"'), f"{scheme}: the Username field is in Plex Mono")
            heads = pg.evaluate("""() => [...document.querySelectorAll('.box.module > .srchead')].map(h => Math.round(h.getBoundingClientRect().height))""")
            ok(heads and all(h == 50 for h in heads), f"{scheme}: every module header is 50 px tall ({heads})")
            sb = pg.evaluate("""() => [...document.querySelectorAll('.box.module .statusbox')].map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; })""")
            ok(sb and all(x == [132, 50] for x in sb), f"{scheme}: one status box size in every module ({sb})")
            btns = pg.evaluate("""() => [...document.querySelectorAll('.syncnow[data-state="idle"]')].filter(s => s.offsetParent).map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; })""")
            ok(len(btns) >= 1 and len(set(map(tuple, btns))) == 1, f"F1.1 {scheme}: every (idle) Sync Now is the same rounded rectangle ({btns})")
            # Folded: no line under the header; Expand sits in the bottom border
            fold = pg.evaluate("""() => { const m = document.querySelector('#src-%s'), t = m.querySelector('.cfgtoggle');
                const mr = m.getBoundingClientRect(), tr = t.getBoundingClientRect(), line = getComputedStyle(m.querySelector('.cfgline'), '::before').display;
                return [mr.bottom, (tr.top + tr.bottom) / 2, line, m.classList.contains('cfgopen')]; }""" % wid)
            ok(not fold[3] and abs(fold[0] - 0.5 - fold[1]) <= 1.5 and fold[2] == "none", f"F1.6 {scheme}: folded, Expand sits in the module's bottom border ({fold})")
            # (?) raised like a superscript, right after the word
            sup = pg.evaluate("""() => { const d = document.querySelector('#deststitle .helpdot'), h = document.getElementById('deststitle');
                const r = d.getBoundingClientRect(), range = document.createRange(); range.selectNodeContents(h); const rects = [...range.getClientRects()].filter(x => x.width > 30);
                const word = rects[rects.length - 1]; return [r.top, r.bottom, word.top, (word.top + word.bottom) / 2, r.left - word.right]; }""")
            ok(sup[1] < sup[3] + 2 and sup[0] <= sup[2] + 3 and 0 <= sup[4] <= 4, f"F1.2 {scheme}: (?) raised after its word ({[round(x, 1) for x in sup]})")
            radii = pg.evaluate("""() => [...document.querySelectorAll('button, input, select, .chip, .rulebox, .box, .card, .statusbox, .okslot')].filter(e => e.offsetParent)
                .map(e => getComputedStyle(e)).filter(s => parseFloat(s.borderTopLeftRadius) >= parseFloat(s.height) / 2 - 0.5 && parseFloat(s.height) > 12 && !s.borderTopLeftRadius.endsWith('%')).length""")
            ok(radii == 0, f"{scheme}: no pill-shaped controls ({radii})")
            ok(pg.locator("svg.mi").count() > 20 and pg.evaluate("[...document.querySelectorAll('svg')].every(s => s.querySelector(':scope > use[href^=\"#mi-\"]') || s.querySelector(':scope > symbol[id^=\"mi-\"]'))"), f"{scheme}: every icon on the page is a Material Symbol")
            ok(not errs, f"{scheme}: no script errors {errs}")
            pg.close()
        pg = b.new_page(viewport={"width": 1400, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        loads = []; pg.on("load", lambda: loads.append(1))
        pg.goto("http://127.0.0.1:8097/?view=month"); pg.wait_for_timeout(500); loads.clear()
        box = f"#src-{wid}"
        # Sync Now: Syncing… → Synced (green pulse) → Sync Now
        MODE.update(fail=False, slow=1.5)
        pg.click(f"{box} .syncnow"); pg.wait_for_timeout(450)
        st = pg.get_attribute(f"{box} .syncnow", "data-state")
        ok(st == "syncing" and pg.inner_text(f"{box} .syncnow").strip() == "Syncing…" and pg.inner_text(f"{box} .statusbox .chip").strip() == "Syncing…", f"F1.1: Syncing… at once ({st})")
        size0 = pg.locator(f"{box} .syncnow").bounding_box()
        pg.wait_for_function(f"document.querySelector('{box} .syncnow').dataset.state !== 'syncing'", timeout=15000)
        st = pg.get_attribute(f"{box} .syncnow", "data-state"); anim = pg.evaluate(f"getComputedStyle(document.querySelector('{box} .syncnow')).animationName")
        size1 = pg.locator(f"{box} .syncnow").bounding_box()
        ok(st == "done" and pg.inner_text(f"{box} .syncnow").strip() == "Synced" and anim == "pulse-ok" and pg.inner_text(f"{box} .statusbox .chip").strip() == "Healthy",
           f"F1.1: then Synced with a green pulse ({st}, {anim})")
        ok(round(size0["width"]) == round(size1["width"]) and round(size0["height"]) == round(size1["height"]), f"F1.1: the button keeps its size while its words change ({size0} {size1})")
        pg.wait_for_timeout(2600)
        ok(pg.get_attribute(f"{box} .syncnow", "data-state") == "idle" and pg.inner_text(f"{box} .syncnow").strip() == "Sync Now" and not loads, "…then Sync Now again, without a reload")
        # …or Failed (yellow pulse)
        MODE.update(fail=True, slow=0.5)
        pg.click(f"{box} .syncnow")
        pg.wait_for_function(f"['done', 'fail'].includes(document.querySelector('{box} .syncnow').dataset.state)", timeout=15000)
        st = pg.get_attribute(f"{box} .syncnow", "data-state"); anim = pg.evaluate(f"getComputedStyle(document.querySelector('{box} .syncnow')).animationName")
        ok(st == "fail" and pg.inner_text(f"{box} .syncnow").strip() == "Failed" and anim == "pulse-warn", f"F1.1: a failed sync pulses yellow and says Failed ({st}, {anim})")
        MODE.update(fail=False, slow=0)
        pg.wait_for_timeout(2600)
        # Expanded: the line is back under the header; title and note are fields of the same size
        pg.click(f"{box} .cfgtoggle"); pg.wait_for_timeout(200)
        ok(pg.evaluate(f"getComputedStyle(document.querySelector('{box} .cfgline'), '::before').display") == "block"
           and pg.locator(f"{box} .nameinput").bounding_box()["height"] == 24 and pg.locator(f"{box} .noteinput").is_visible()
           and round(pg.locator(f"{box} > .srchead").bounding_box()["height"]) == 50, "F1.6: expanded, a line under the 50 px header; title and note are 24 px fields")
        # Inline edits: ✕ | ✓ icons (F1.4)
        pg.fill(f"{box} input[name=url]", "https://example.org/other.ics"); pg.wait_for_timeout(400)
        slot = pg.locator(f"{box} .okslot")
        ok(slot.get_attribute("data-state") == "edit" and slot.locator(".slotcancel").inner_text().strip() == "" and slot.locator(".slotsave").inner_text().strip() == ""
           and slot.locator(".slotcancel").get_attribute("aria-label") == "Cancel" and slot.locator(".slotsave svg").is_visible(), "F1.4: typing shows ✕ | ✓ icons (named Cancel and Save)")
        slot.locator(".slotcancel").click(); pg.wait_for_timeout(600)
        got = [pg.input_value(f"{box} input[name=url]"), slot.get_attribute("data-state")]
        ok(got[0] == "https://example.org/work.ics" and got[1] in ("ok", "needs"), f"…✕ undoes the typing and the slot goes back ({got})")
        # the bottom pair says Cancelled
        pg.locator(f"{box} .pcancel").click(); pg.wait_for_timeout(200)
        ok(pg.inner_text(f"{box} .pcancel").strip() == "Cancelled", "F1.3: Cancel | Save says Cancelled")
        ok(not errs, f"no script errors {errs}")
        # Phone width: the header row keeps the title and status; the lines go under it
        pg.set_viewport_size({"width": 390, "height": 900}); pg.wait_for_timeout(300)
        sw = pg.evaluate("document.documentElement.scrollWidth")
        ok(sw <= 390, f"phone: nothing wider than the screen ({sw})")
        b.close()
    srv.should_exit = True
print("FAILS", fails)
