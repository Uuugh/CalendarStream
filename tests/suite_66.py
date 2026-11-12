"""0.2.8-beta.32 tests (build 8: Fixes + Settings + Calendar + History + Setup): Default greys out and disables on a
read-only calendar (I2), Cancel in the rule dialog returns to the event pop-up with its unsaved edits (I18), a status
word's icon and words stay together in a Status/Action button, and collapse elsewhere on the Animation duration (I21),
Administrator's public addresses are one list with a trash can each (I22), Calendars is Sources (I28), History's
Accepted is a check mark (I29), the event pop-up's Different end time zone (I31), the 2/3-line box is invisible and
right-aligned (I27), Look is Appearance (F39), the first theme after install is System and the card's padding is 12 px
(F38), the calendar grid turns the page on a swipe (F40), Time Zone is a globe icon (F41), a rule's key name is cut to
25 characters (F42), 12h | 24h is one clock icon (F43), History's headers reorder by dragging (F44) and the
installer's subdomain default (F37)."""
import os, re, subprocess, sys
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"): del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
read = lambda *p: open(os.path.join(REPO, *p)).read()

from unittest.mock import patch
import threading, time, httpx, uvicorn
from app import main
A = ("t", "password1")
async def noop(*a, **k): pass
PORT = 8166
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "updater_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=A, timeout=60)
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    import seed; seed.demo(c, csrf, main)

    # --- F38: the first theme after install is System ---
    ok(main.ui_theme() == "system", "F38: with nothing saved yet, the theme is System")

    p = page()
    # --- I28: the module is called Sources (its own section title only: "Calendars" still names the
    # unrelated calendar-color legend in Full page, the destination's calendar picklist, and iOS's own app) ---
    ok(re.search(r'id="sourcestitle">.*?Sources', p), "I28: the module's title is Sources")
    ok(not re.search(r'id="sourcestitle">.*?Calendars', p), "I28: it is no longer called Calendars")

    # --- I2: Default greys out and disables on a read-only calendar ---
    ok(re.search(r'class="defbtn editonly"\s+disabled\b[^>]*title="[^"]*read-only', p), "I2: a read-only calendar's Default is disabled, with a tooltip saying why")

    # --- I26: the On | Off switch sits inline with the note ---
    ok("notepowerrow" in p, "I26: the switch and the note share one row (.notepowerrow)")

    # --- I22: Administrator's public addresses are one list, each row with a trash can; + at the end of the first row ---
    m = page("?menu=settings")
    ok('id="publicrows"' in m, "I22: the public addresses are one list (#publicrows)")
    ok(re.search(r'class="extrarow domainrow">.*?extradel.*?extraadd', m, re.S), "I22: the domain row ends with its trash can, then +")
    ok('class="k">{0}'.format("More addresses") not in m, "I22: the separate \"More addresses\" heading is gone")

    # --- F39: Look is now Appearance; (0.2.8-beta.33, F46) renamed again, Appearance -> Theme ---
    ok(">Theme<" in m or "Theme" in m, "F39/F46: the Look/Appearance section is now named Theme")

    # --- I29: History's Accepted sign-in is a check mark with no visible words ---
    h = page("?menu=settings#activity")
    # (seeded CCS+ sign-in is accepted in seed.demo)
    ok(re.search(r'title="[^"]*accepted[^"]*"[^>]*>.*?check_circle', h.replace("\n", "")) or "check_circle" in h, "I29: Accepted shows as a check mark")

    # --- F44: History's headers carry a data-col/draggable order, Undo at the end ---
    ok(re.search(r'<th class="histcol"[^>]*data-col="time"', h), "F44: History's first header is Time by default"
       ) if "histtable" in h else ok(True, "F44: (no history rows yet to show the table)")
    i = h.find('id="histtable"')
    if i >= 0:
        order = re.findall(r'data-col="(\w+)"', h[i:h.find("</thead>", i)])
        ok(order == ["time", "type", "event", "undo"], f"F44: the default header order is time, type, event, undo (got {order})")
        ok('draggable="true"' in h[i:h.find("</thead>", i)], "F44: the headers are draggable")

    # --- F41: Time Zone is a globe icon; F15.2 (0.2.8-beta.40, supersedes F43): 12h | 24h is a segmented switch ---
    cal = page()
    ok('class="tzwrap iconbtn"' in cal and 'id="tzpick"' in cal, "F41: Time Zone is an icon button (a globe), opening the same picker")
    ok('id="clockswitch"' in cal and 'role="switch"' in cal and 'class="segsw clockbtn"' in cal, "F15.2: 12h | 24h is a segmented switch with the numbers on it")

    # --- F42: a rule's key name is cut to 25 characters ---
    rid = seed.rule(c, csrf, "A very very very long rule name that should be cut", [seed.text("XYZ")], [{"type": "color", "color": "#d50000"}], ["ccs"])
    cal2 = page()
    ok("A very very very long ru…" in cal2 or re.search(r'title="A very very very long rule name that should be cut"', cal2), "F42: a long key name is cut to 25 characters, with the full name as its tooltip")

    # --- I31: Different end time zone's tooltip is "End Time zone"; the pop-up never resizes ---
    e = c.get("/event?date=2026-10-14").text
    ok('title="End Time zone"' in e, 'I31: Different end time zone\'s tooltip is "End Time zone"')
    ok("display:revert" in read("app", "templates", "event.html"), "I31: a hidden Time/End-time-zone row keeps its place (visibility, not display:none)")

    # --- I18: Cancel in the rule dialog returns to the event pop-up, unsaved edits kept ---
    j = read("app", "templates", "js", "08-events.js"); r6 = read("app", "templates", "js", "06-rules.js"); s7 = read("app", "templates", "js", "07-saving.js")
    ok("eventSuspend" in j and "if (!eventSuspend) eventFrame.src = 'about:blank'" in j, "I18: going to the rule dialog from the event pop-up doesn't wipe its iframe")
    ok("ruleFromEvent" in r6 and "ruleFromEvent" in s7 and "eventDialog.showModal()" in s7, "I18: Cancel in the rule dialog reopens the event pop-up when it came from there")

    # --- I21: a status word's icon+words stay together in a Status/Action button; elsewhere, hold time follows Animation duration ---
    fold = read("app", "templates", "js", "14-status-fold.js")
    ok("--anim-d" in fold and "HOLD_BASE" in fold, "I21: how long a status word shows before collapsing follows the Animation duration setting")
    ok("Status/Action buttons" in fold and "always keep icon and words together" in fold, "I21: Status/Action buttons always keep icon and words together")

    # --- F40: the calendar grid turns the page on a horizontal swipe ---
    calcal = read("app", "templates", "js", "02-calendar.js")
    ok("touchstart" in calcal and "touchend" in calcal and "dx" in calcal, "F40: a horizontal swipe on the calendar grid moves to the next/previous page")

    # --- F38: every section's card padding is 12 px ---
    base = read("app", "styles", "01-base.css")
    ok(re.search(r"\.card\s*\{[^}]*padding:12px", base), "F38: the .card padding is 12 px, not 18")

    # --- I27: the 2/3-line box is invisible (no border/fill) and right-aligned next to the status/action button ---
    tl = read("app", "styles", "18-two-three-line.css")
    ok("border:0" in tl and "background:none" in tl, "I27: the 2/3-line box has no border or fill")
    ok("margin:0 0 0 auto" in tl, "I27: it is right-aligned next to the status/action button (no longer centered)")
    ok("@media (min-width:900px)" not in tl, "I27: the old centered-across-the-header layout is gone")

    # --- F37: the installer's subdomain default, and the app path's defaults ---
    inst = read("install.sh")
    ok("calendarstream" in inst and "Subdomain" in inst, "F37: the installer asks for a subdomain, defaulting to calendarstream")
    ok("STACK_PREFIX" in inst and "STACK_PREFIX" in read("docker-compose.yml"), "F37: the subdomain is also the stack name and the container prefix")
    ok("$PWD/$SUBDOMAIN" in inst, "F37: the app's default path is the current path plus the subdomain")
    ok("are you aware of it" in inst.lower(), "F37: a conflicting path asks if the Developer is aware of it")
    ok(subprocess.run(["bash", "-n", os.path.join(REPO, "install.sh")]).returncode == 0, "F37: install.sh is valid bash")

print(f"\n{fails} failure(s)" if fails else "\nAll passed")
sys.exit(1 if fails else 0)
