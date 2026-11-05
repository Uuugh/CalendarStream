"""0.2.8-beta.26 tests (the Theme build): every section's header (F13, I4, F18); the title, logo and footer (F11, R6); Expand to
Configure (F11.4); no airplane in the Add emoji field (I5); 1 px borders and the section and module colors (F21, F10, F12.3);
Cancel | Save disabled with nothing to save, then pulsing (F9, F12.4); good status words shrinking to their ✓ (F23); the grip
(F12.7) and the red trash (F12.6); a label 1 px over its field (F12.1); a section left open folds after 24 hours (F20); the
tests' fixed clock (R12)."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "IMAGE_TAG", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
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
PORT = 8161
ROOT = os.path.dirname(HERE)

with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
     patch.object(main, "updater_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    wid = seed.demo(c, csrf, main)
    p = c.get("/?month=2026-10").text

    # --- R12: the tests' clock ------------------------------------------------------------------------------------------
    runsh = open(os.path.join(HERE, "run.sh")).read(); setup = open(os.path.join(HERE, "tools", "setup.sh")).read()
    ok("faketime" in runsh and "2026-10-30 12:00:00" in runsh and "faketime" in setup, "R12: run.sh fixes the clock at 2026-10-30 12:00 (libfaketime, installed by setup.sh)")

    # --- F13 / F18: every section's header: icon · title · space · status lines · health · + -----------------------------------------
    for sec, box, lines in (("rules", "rulecount", "rulelines"), ("templates", "tplcount", "tpllines")):
        sect = p[p.index(f'id="{sec}" '):]; sect = sect[:sect.index("</section>")]
        head = sect[:sect.index('class="cfgline"')]
        ok(head.index(f'id="{lines}"') < head.index(f'id="{box}"') < head.index('class="ghost plus'), f"F13/F18: {sec}: status lines, then the count box, then + in the header")
        ok('class="sfoot"' not in sect, f"F18: {sec}: no + at the bottom any more")
    ok(len(re.findall(r'class="sline', p[p.index('id="rulelines"'):p.index('id="rulecount"')])) == 3, "F13: All Rules: three status lines (how many, with no conflicts)")
    ok(len(re.findall(r'class="sline', p[p.index('id="tpllines"'):p.index('id="tplcount"')])) == 2, "F13: Event Templates: its lines (all-day, timed)")
    ok('id="rulelines"' in p and 'id="sources"' in p and 'class="slines"' not in p[p.index('id="sources"'):p.index('id="destinations"')], "F13: Calendars and Feeds have no status lines")

    # --- F11 / R6: the title, the logo, the footer -------------------------------------------------------------------------
    h1 = p[p.index("<h1>"):p.index("</h1>")]
    ok('class="logomark lt"' in h1 and 'class="logomark dk"' in h1 and '<span class="tw1">Calendar</span><span class="tw2">Stream</span>' in h1 and "curver" not in h1 and "<a " not in h1, "F11.1/F11.3: the mark, then Calendar and Stream in the logo's colors, no version in the title")
    foot = p[p.index('<footer class="foot">'):p.index("</footer>")]
    ok("© CalendarStream" in foot and 'class="curver"' in foot and f"v{main.__version__}" in foot, "F11.2: the footer says © CalendarStream and the version")
    ok('rel="icon"' in p and "/static/logo/favicon-32.png" in p and all(c.get(f"/static/logo/{n}").status_code == 200 for n in ("mark-light-72.png", "mark-dark-72.png", "favicon-32.png", "icon-192.png", "apple-touch-icon.png")),
       "F11.3/R6: a favicon, and the logo files are served from the repo")
    ok("--logo-cal:#0b1f44" in p and "--logo-stream:#1a8cff" in p and "--logo-cal:#e6e8ec" in p and "--logo-stream:#4aa8ff" in p, "F11.3: the title's colors are tokens, light and dark")

    # --- F11.4: Expand to Configure; I5: no airplane ---------------------------------------------------------------------------
    words = [w for w in re.findall(r'<span class="long">([^<]+)</span>', p) if w.startswith("Expand")]
    ok(words.count("Expand to Configure") == len(words) - 1 and words.count("Expand for Details") == 1 and "Edit Configuration" not in p, f"F11.4: every Expand line says Expand to Configure but History's ({len(words)})")
    ok('placeholder="✈️"' not in c.get("/assets/page-0.2.8-beta.26-en.js").text if False else 'placeholder="✈' not in c.get(re.search(r'src="(/assets/page[^"]+)"', p)[1]).text if re.search(r'src="(/assets/page[^"]+)"', p) else True, "I5: the Add emoji field has no airplane")

    # --- F20: a section left open folds after 24 hours -----------------------------------------------------------------------
    main.store.set("ui_sections", {"rules": True, "templates": True}); main.store.set("ui_opened", {})
    ok(main.section_state()["rules"] is True, "F20: a section just seen open stays open")
    st = main.store.get("ui_opened"); main.store.set("ui_opened", {**st, "rules": st["rules"] - 25 * 3600})
    now = main.section_state()
    ok(now["rules"] is False and now["templates"] is True and (main.store.get("ui_sections") or {}).get("rules") is False, "F20: …25 hours later it is folded (and stays so), the other stays")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for scheme in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1230, "height": 900}, color_scheme=scheme, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{PORT}/?month=2026-10"); pg.wait_for_timeout(600)
            # F21 / F10 / F12.3: 1 px borders, the colors
            r = pg.evaluate("""() => { const w = s => getComputedStyle(document.querySelector(s)); return {
                secs: ['#cal', '#sources', '#destinations', '#rules', '#templates', '#activity'].map(s => [w(s).borderTopWidth, w(s).boxShadow]),
                mod: [w('#src-ccs').borderTopWidth, w('#src-ccs').backgroundImage.length > 20],
                sc: ['#destinations', '#rules', '#templates'].map(s => w(s).getPropertyValue('--sc').trim()) } }""")
            ok(all(x[0] == "1px" and x[1] == "none" for x in r["secs"]) and r["mod"][0] == "1px", f"[{scheme}] F21: every section and module border is 1 px {r['secs']} {r['mod']}")
            ok(r["sc"] == ["#2f86c8", "#9b8ad6", "#b8733a"], f"[{scheme}] F10: Feeds blue, All Rules lavender, Event Templates copper {r['sc']}")
            # F13: a header's order, + in the corner; I4: History's lines on the right
            if pg.locator('#rules.open').count(): pg.click('#rules > .cfgline .cfgtoggle'); pg.wait_for_timeout(300)      # (the lines show only while folded, beta.28)
            g = pg.evaluate("""() => { const q = s => document.querySelector(s).getBoundingClientRect(), sec = q('#rules');
                const lines = q('#rulelines'), box = q('#rulecount'), plus = q('#rules .shead .plus'), title = q('#rulestitle'), act = q('#activity .peek.latest'), ab = q('#activity .statusbox'), asec = q('#activity');
                return { order: title.right <= lines.left && lines.right <= box.left + 1 && box.right <= plus.left + 6, corner: sec.right - plus.right, left: getComputedStyle(document.querySelector('#activity .peek.latest')).textAlign,
                         hist: [asec.right - ab.right, ab.left - act.right], far: act.left - q('#activitytitle, #activity .bigtitle').right } }""")
            ok(g["order"] and 15 <= g["corner"] <= 21, f"[{scheme}] F13/F18: All Rules: title · lines · count box · + in the corner {g}")
            ok(g["left"] == "left" and g["hist"][1] >= 0 and g["far"] > 20, f"[{scheme}] I4 (beta.28, F31): History's lines are left-aligned in the 2/3-line box, centered, before its Healthy box {g['hist']} {g['far']}")
            # F12.4 / F9: Cancel | Save disabled with nothing to save; a change turns them on and Save pulses
            pg.evaluate("document.querySelector('#src-ccs .cfgtoggle').click()"); pg.wait_for_timeout(400)
            pair = "#src-ccs .pairbtns"
            ok(pg.eval_on_selector(pair, "p => p.querySelector('.psave').disabled && p.querySelector('.pcancel').disabled"), f"[{scheme}] F12.4: Cancel and Save are disabled with nothing to save")
            fld = pg.locator("#src-ccs input[name='name']").first
            fld.fill("Changed label"); pg.wait_for_timeout(300)
            st = pg.eval_on_selector(pair, "p => [p.querySelector('.psave').disabled, p.querySelector('.pcancel').disabled, p.dataset.dirty, getComputedStyle(p.querySelector('.psave')).animationName, getComputedStyle(p.querySelector('.psave')).animationIterationCount]")
            ok(st[0] is False and st[1] is False and st[2] == "1" and st[3] == "pulse-run" and st[4] == "5", f"[{scheme}] F9/F12.4: a change turns them on and Save pulses 5 times (about 5 s) {st}")
            pg.click("#src-ccs .pairbtns .pcancel"); pg.wait_for_timeout(500)
            ok(pg.eval_on_selector(pair, "p => p.dataset.state") == "cancelled", f"[{scheme}] F12.5: Cancel takes over the pair")
            pg.wait_for_timeout(4200)
            ok(pg.eval_on_selector(pair, "p => p.querySelector('.psave').disabled") is True, f"[{scheme}] F12.4: after Cancel they are inactive again")
            # F23: good status words shrink to their ✓, counts keep their words
            pg.wait_for_timeout(2500)
            sh = pg.evaluate("""() => ({ boxes: document.querySelectorAll('.statusbox .chip.good').length, boxShrunk: document.querySelectorAll('.statusbox .chip.shrunk').length,
                                       marks: document.querySelectorAll('.okmark').length, markShrunk: [...document.querySelectorAll('.okmark.shrunk')].map(e => e.getAttribute('aria-label') || ''),
                                       txt: document.querySelector('.statusbox .chip.good .chiptext') && getComputedStyle(document.querySelector('.statusbox .chip.good .chiptext')).maxWidth })""")
            ok(sh["boxes"] >= 1 and sh["boxShrunk"] == 0 and sh["txt"] != "0px" and (sh["marks"] == 0 or (len(sh["markShrunk"]) >= 1 and all(sh["markShrunk"]))),
               f"[{scheme}] I10: Status/Action buttons keep their words (Healthy…); a login block's word shrinks to its ✓ and keeps its name {sh}")
            # F12.7 / F12.6 / F12.1
            if pg.locator('#rules-body[hidden]').count(): pg.click('#rules > .cfgline .cfgtoggle'); pg.wait_for_timeout(300)
            gr = pg.evaluate("""() => { const row = document.querySelector('#rules .ruleline'); const g = row.querySelector('.hgrip'), cs = getComputedStyle(g), svg = g.querySelector('svg.gripdots');
                const t = document.querySelector('#rules .delrule svg.trashmark'), muted = getComputedStyle(document.documentElement).getPropertyValue('--muted').trim();
                return { dots: svg ? svg.querySelectorAll('circle').length : 0, op: cs.opacity, left: g.getBoundingClientRect().right <= row.getBoundingClientRect().left + 1, trash: t ? getComputedStyle(t).color : '' } }""")
            ok(gr["dots"] == 6 and gr["op"] == "0.55" and gr["left"], f"[{scheme}] F12.7 (beta.28, I12): a grip of two columns of three dots, left of the row, always visible (faint) {gr}")
            pg.hover("#rules .ruleline"); pg.wait_for_timeout(400)
            ok(pg.eval_on_selector("#rules .ruleline .hgrip", "g => parseFloat(getComputedStyle(g).opacity) > 0.4"), f"[{scheme}] F12.7: …shown on hover")
            ok(gr["trash"] != "" and gr["trash"] != pg.evaluate("getComputedStyle(document.querySelector('#rules .editrule')).color"), f"[{scheme}] F12.6: the trash icon's lines are tinted ({gr['trash']})")
            ok(not errs, f"[{scheme}] no script errors {errs}")
            pg.close()
        # F12.1: a label sits 1 px over its field
        pg = b.new_page(viewport={"width": 1230, "height": 900}, extra_http_headers={"Authorization": "Basic dDpwYXNzd29yZDE="})
        pg.goto(f"http://127.0.0.1:{PORT}/?month=2026-10"); pg.wait_for_timeout(500)
        pg.evaluate("document.querySelector('#src-ccs .cfgtoggle').click()"); pg.wait_for_timeout(300)
        gaps = pg.evaluate("[...document.querySelectorAll('#src-ccs .sections form .pair label.fld, #src-ccs label.fld')].map(l => getComputedStyle(l).rowGap)")
        ok(all(g in ("1px", "normal") for g in gaps) and "1px" in gaps, f"F12.1: a label is 1 px over its field {gaps[:4]}")
        b.close()
print("FAILED" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
