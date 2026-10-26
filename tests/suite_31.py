"""0.2.7-beta.2 tests: Settings tint, TZ label, source wording, Username, half-width slot,
destination boxes with Configure, Rule Templates / Event Templates / Activities and Logs, spacing."""
import os, re, sys, threading, time
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8099, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2)
    c = httpx.Client(base_url="http://127.0.0.1:8099", auth=("t", "password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    post = lambda path, **d: c.post(path, data={"csrf": csrf, **d})
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    main.store.set("public_url", "https://cal.example.com")
    r = post("/destinations/add", type="feed", name="")
    feeds = main.destinations("feed")
    ok(feeds[-1]["name"] == main.calendar_name("ccs"), "F4.2: an empty Name gets the source's name")
    p = c.get("/").text
    ok('placeholder="How your calendar will be titled via stream"' in p, "F4.2: the Name's hint")
    ok('<span class="long">Time Zone</span><span class="short" title="Time Zone">TZ</span>' in p, "F2.1: Time Zone (TZ when tight)")
    ok('<span class="long">Last check was successful @ ' in p and '<span class="short">Checked @ ' in p, "F3: shorter wording when the box is narrow (0.2.7-beta.5: Check every sits under Configure)")
    ok("<span>Username</span>" in p and "<span>UID</span>" not in p, "F3.3: Username")
    order = [m.group(1) for m in re.finditer(r'<section class="card[^"]*" id="([a-z]+)"', p)]
    ok(order == ["sources", "destinations", "rules", "templates", "activity"], f"F5/F6/F7: section order ({order})")
    ok(re.search(r'id="rulestitle"><svg[^>]*>.*?</svg>All Rules<span class="helpdot', p) and re.search(r'id="tplstitle"><svg[^>]*>.*?</svg>Event Templates<span class="helpdot', p) and ">Activities and Logs</span>" in p, "F5.2/F6/F7.1: section names")
    did = feeds[-1]["id"]
    ok(f'id="dest-{did}" data-section="dest:{did}"' in p and f'aria-controls="cfg-dest-{did}"' in p and f'id="cfg-dest-{did}" hidden' in p, "F4.1: a destination folds under Configure")
    ok(post("/ui/section", section=f"dest:{did}", open="1").status_code == 204 and f'id="cfg-dest-{did}" hidden' not in c.get("/").text, "F4.1: …and stays open once opened")
    ok(post("/ui/section", section="dest:../x", open="1").status_code == 400, "unknown section refused")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w in (1400, 900, 390):
            pg = b.new_page(viewport={"width": w, "height": 900}, http_credentials={"username": "t", "password": "password1"})
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("http://127.0.0.1:8099/?view=month"); pg.wait_for_timeout(400)
            over = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            ok(over <= 0 and not errs, f"F8.1: {w}px: no sideways scrolling ({over}px), no script errors")
            # I1 (0.2.7-beta.4): each source header fits: the status lines beside the title, both starting
            # at the same left edge (the short wording when the long one would wrap)
            if w != 390:
                for sid in ("ccs",):
                    L = pg.locator(f"#src-{sid} .srcleft").bounding_box(); R = pg.locator(f"#src-{sid} .srcright").bounding_box()
                    st, nx = pg.locator(f"#src-{sid} .srcstatus").bounding_box(), pg.locator(f"#src-{sid} .srcnext").bounding_box()
                    xs = [round(R["x"] + R["width"] - st["x"] - st["width"]), round(R["x"] + R["width"] - nx["x"] - nx["width"])]
                    ok(R["y"] < L["y"] + L["height"] and xs == [0, 0], f"I1: {w}px: the status lines sit beside the title, both on the right by Sync Now (F3.4, 0.2.8-beta.3) ({xs})")
            if w == 1400:
                act = pg.locator("#activity").bounding_box(); cal = pg.locator("#cal").bounding_box()
                ok(abs(act["width"] - cal["width"]) < 2, "F7.2: Activities and Logs spans the full width")
                rb, tb = pg.locator("#rules").bounding_box(), pg.locator("#templates").bounding_box()
                ok(abs(rb["y"] - tb["y"]) < 2 and tb["x"] > rb["x"], "F6.2: Event Templates beside Rule Templates")
                gap = pg.locator("#destinations").bounding_box()["x"] - (pg.locator("#sources").bounding_box()["x"] + pg.locator("#sources").bounding_box()["width"])
                ok(round(gap) == 10, f"F8.2: 10px between sections ({gap})")
                if pg.locator("#cfg-ccs[hidden]").count(): pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(200)
                ok(round(pg.locator("#src-ccs .okslot").bounding_box()["width"]) == 80, "F3.4: ✓ Validated is half as wide (80px)")
                pg.click("#menubtn"); pg.wait_for_timeout(150)
                bg = pg.evaluate("getComputedStyle(document.getElementById('menu')).backgroundColor")
                ok(bg == "rgb(232, 239, 255)", f"F1.1: Settings opens in light blue ({bg})")
            if w == 390:
                ok(pg.is_visible(".tzlabel .short") and not pg.is_visible(".tzlabel .long"), "F2.1: TZ on a phone")
                ok(pg.is_visible("#src-ccs .srcstatus .short") and not pg.is_visible("#src-ccs .srcstatus .long"), "F3: the short status line on a phone")
        b.close()
    srv.should_exit = True
print("FAILS", fails)
