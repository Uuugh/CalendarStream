"""Screenshot the demo server (demo.sh) after some steps:

    tests/tools/shot.py [--phone] [--dark] [--url /?menu=settings] out.png STEP...

STEP is CLICK <selector>, FILL <selector>=<text>, WAIT <ms>, SHOT <selector> (that element only), or JavaScript
(its result is printed). 400 ms between steps. Without SHOT, the whole window. Prints the page's errors at the end.
Desktop is 1230 × 900; --phone is 390 × 844. Opens October 2026 unless --url says otherwise."""
import argparse, base64, os
from playwright.sync_api import sync_playwright
a = argparse.ArgumentParser(); a.add_argument("--phone", action="store_true"); a.add_argument("--dark", action="store_true")
a.add_argument("--url", default="/?month=2026-10"); a.add_argument("out"); a.add_argument("steps", nargs="*")
o = a.parse_args()
port = os.environ.get("DEMO_PORT", "8177")
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844} if o.phone else {"width": 1230, "height": 900},
                    color_scheme="dark" if o.dark else "light",
                    extra_http_headers={"Authorization": "Basic " + base64.b64encode(b"t:password1").decode()})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.goto(f"http://127.0.0.1:{port}{o.url}"); pg.wait_for_timeout(700)
    shot = False
    for st in o.steps:
        if st.startswith("CLICK "): pg.click(st[6:])
        elif st.startswith("FILL "): sel, val = st[5:].split("=", 1); pg.fill(sel, val)
        elif st.startswith("WAIT "): pg.wait_for_timeout(int(st[5:]))
        elif st.startswith("SHOT "): pg.locator(st[5:]).screenshot(path=o.out); shot = True
        else: print("JS:", pg.evaluate(st))
        pg.wait_for_timeout(400)
    if not shot:
        pg.screenshot(path=o.out)
    print("errors:", errs)
    b.close()
