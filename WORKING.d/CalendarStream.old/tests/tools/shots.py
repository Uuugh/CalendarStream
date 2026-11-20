"""The standard set of screenshots of the demo server (demo.sh), for a before/after comparison (0.2.8-beta.19, R15):

    tests/tools/shots.py DIR                # before the change: shots.py /tmp/before
    (change the page, restart demo.sh)
    tests/tools/shots.py DIR                # after: shots.py /tmp/after
    tests/tools/pixdiff.py /tmp/before /tmp/after /tmp/diff

Whole pages (scrolled to the end), desktop 1230 wide and phone 390, light and dark, with every module expanded and
with the ☰ menu open. Times and the demo's random feed names are hidden, so only real changes show."""
import argparse, base64, os
from pathlib import Path
from playwright.sync_api import sync_playwright

# Text that changes on its own between two runs (times, "5 min ago"): hidden, not removed, so nothing moves
STEADY = """
  .srcstatus b, .srcnext, .ver, .ptime, #activity time, .lastrun, .nextrun, .fstream { visibility:hidden !important }
  *, *::before, *::after { animation:none !important; transition:none !important; caret-color:transparent !important }
"""
EXPAND = "document.querySelectorAll('.cfgbody[hidden]').forEach(function (b) { b.hidden = false; });" \
         "document.querySelectorAll('.cfgbox').forEach(function (b) { b.classList.add('cfgopen'); })"
VIEWS = [   # name, address, steps (JavaScript run before the shot)
    ("page", "/?month=2026-10", []),
    ("expanded", "/?month=2026-10", [EXPAND]),
    ("settings", "/?month=2026-10&menu=settings", []),
]

a = argparse.ArgumentParser(); a.add_argument("out")
o = a.parse_args()
out = Path(o.out); out.mkdir(parents=True, exist_ok=True)
port = os.environ.get("DEMO_PORT", "8177")
auth = {"Authorization": "Basic " + base64.b64encode(b"t:password1").decode()}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for phone in (False, True):
        for dark in (False, True):
            pg = b.new_page(viewport={"width": 390, "height": 844} if phone else {"width": 1230, "height": 900},
                            color_scheme="dark" if dark else "light", extra_http_headers=auth)
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            for name, url, steps in VIEWS:
                pg.goto(f"http://127.0.0.1:{port}{url}"); pg.wait_for_load_state("networkidle")
                pg.add_style_tag(content=STEADY)
                for js in steps:
                    pg.evaluate(js)
                pg.wait_for_timeout(500)
                file = out / f"{name}-{'phone' if phone else 'desktop'}-{'dark' if dark else 'light'}.png"
                pg.screenshot(path=str(file), full_page=True)
                print(file)
            if errs:
                print("errors:", errs)
            pg.close()
    b.close()
