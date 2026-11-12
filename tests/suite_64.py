"""0.2.8-beta.29 tests (the 5 Calendar build): Print on real paper (I11), the view drop-down, the 12h | 24h switch, the hourly grid, the
Calendars and Key parts, Full page and the stretch handle (F15, F26, F27, F28), one Administrator section (F32, F33) and Look: logo,
favicon, Animation (F14)."""
import os, re, sys, asyncio
from unittest.mock import patch
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"): del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1],
                  DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com", CCS_USERNAME="", CCS_PASSWORD="")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO); sys.path.insert(0, HERE)
from fastapi.testclient import TestClient
from app import main, rules as rules_mod, logins, gsync, calsync
from app.calsync import Event
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
read = lambda *p: open(os.path.join(REPO, *p)).read()
DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()


import io, tempfile
from pypdf import PdfReader
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        TestClient(main.app, base_url="https://cal.example.com") as c:
    c.auth = A
    page = lambda q="": c.get("/" + q, headers={"accept": "text/html"}).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page())[1]
    post = lambda path, **f: c.post(path, data={"csrf": csrf, **f}, headers={"X-CS-Async": "1"}, follow_redirects=False)
    import seed; seed.demo(c, csrf, main)
    # --- header, view drop-down, switch, key (F15, F26) ---
    p = page("?date=2026-10-14")
    ok('id="viewbtn"' in p and 'id="clockswitch"' in p and "viewseg" not in p, "F15/F26: the view is a drop-down (0.2.8-beta.33, F52: icons, a button + menu); 12h | 24h is a segmented switch (0.2.8-beta.40, F15.2)")
    ok('legpart legcals' in p and 'legpart legkeys' in p, "F15: the legend is two parts, Calendars and Key")
    for v in ("week", "day"):
        post("/ui/view", view=v)
        ok('class="hourview"' in page("?date=2026-10-14"), f"F28: {v} is an hourly grid")
    post("/ui/view", view="month")
    # --- Full page and the stretch handle (F27, F28) ---
    ok(post("/ui/calview", full="1").status_code in (200, 204, 303) and 'class="calfull"' in page(), "F27: Full page is saved and hides the other sections")
    ok(post("/ui/calview", full="1", hide="edited").status_code in (200, 204, 303) and main.store.get("ui_calview").get("hide") == ["edited"], "F15: the key's hidden set is kept while Full page is on")
    post("/ui/calview", stretch="1500"); ok(main.store.get("ui_calview").get("stretch", 0) <= 1200, "F28: the stretch is capped")
    post("/ui/calview", full="0"); ok(main.store.get("ui_calview").get("hide") == ["edited"] and 'class="calfull"' not in page(),
       "F27: leaving Full page no longer clears what the key hid (0.2.8-beta.33, F48: hide works in every mode now)")
    post("/ui/calview", hide="-")   # leave it clean for later suites/tests
    # --- Print (I11): real PDFs, Letter and A4 ---
    from playwright.sync_api import sync_playwright
    def pdf(view, fmt, theme="light"):
        html = c.get(f"/print?view={view}&start=2026-10-01&end=2026-10-31&theme={theme}").text
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(); pg.set_content(html); pg.wait_for_timeout(400)
            data = pg.pdf(format=fmt, prefer_css_page_size=True, print_background=True)
            cut = pg.evaluate("[...document.querySelectorAll('.cell')].filter(c => c.scrollHeight > c.clientHeight + 1).length")
            b.close()
        return PdfReader(io.BytesIO(data)), cut
    for fmt in ("Letter", "A4"):
        r, cut = pdf("month", fmt); w, h = (float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height))
        ok(len(r.pages) == 1 and w > h and cut == 0, f"I11: a month is one landscape {fmt} page, no day cut ({len(r.pages)} pages, {w:.0f}x{h:.0f}, cut {cut})")
        r, cut = pdf("day", fmt); w, h = (float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height))
        ok(h > w and cut == 0, f"I11: a day is portrait {fmt}")
    r, cut = pdf("week", "Letter"); ok(len(r.pages) >= 2 and cut == 0, f"I11: each week gets its own page ({len(r.pages)})")
    # --- F32, F33: one Administrator section ---
    p = page("?menu=settings")
    ok('id="adminform"' in p and p.count('action="/settings/public-url"') == 0 and p.count('action="/settings/login"') == 0 and ">Sign out<" in p and ">Signed in<" in p,
       "F32: Administrator and Public address are one form; Signed in over Sign out")
    ok(post("/settings/administrator", user="t", password="", current="", confirm="", main="https://cal.example.com", url=["https://b.example.org"]).status_code == 303 and main.store.get("public_urls_extra") == ["https://b.example.org"],
       "F32: the addresses save without the current password")
    r = post("/settings/administrator", user="t", password="", current="", confirm="", main="not an address")
    ok(r.status_code == 400 and "main" in r.headers.get("x-cs-fields", ""), "F32: a bad address is refused, naming its field")
    r = post("/settings/administrator", user="boss", password="", current="wrong", confirm="", main="https://cal.example.com")
    ok(r.status_code == 400 and "current" in r.headers.get("x-cs-fields", "") and main.logins.page_user == "t", "F32: a new user name needs the current password")
    # --- F14: Look ---
    PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 40
    ok(c.get("/brand/logo").status_code == 404, "F14: no logo uploaded: CalendarStream's own")
    r = c.post("/settings/look", data={"csrf": csrf, "intensity": "100", "duration": "100"}, files={"logo": ("l.png", PNG, "image/png")}, follow_redirects=False)
    ok(r.status_code == 303 and c.get("/brand/logo").headers["content-type"] == "image/png" and "/brand/logo?v=" in page(), "F14: an uploaded logo is served and shown")
    r = c.post("/settings/look", data={"csrf": csrf, "intensity": "100", "duration": "100"}, files={"favicon": ("f.png", b"not a picture", "image/png")}, headers={"X-CS-Async": "1"})
    ok(r.status_code == 400 and "favicon" in r.headers.get("x-cs-fields", ""), "F14: something that isn't a picture is refused")
    r = c.post("/settings/look", data={"csrf": csrf, "intensity": "100", "duration": "100"}, files={"favicon": ("f.svg", b"<svg xmlns='http://www.w3.org/2000/svg'><script>x</script></svg>", "image/svg+xml")}, headers={"X-CS-Async": "1"})
    ok(r.status_code == 400, "F14: an SVG with a script is refused")
    post("/settings/look", intensity="150", duration="50"); ok('--anim-i:1.5;--anim-d:0.5' in page(), "F14: Animation intensity and duration reach the page")
    post("/settings/look", reset="1", remove_logo="1"); p = page()
    ok("--anim-i" not in p and c.get("/brand/logo").status_code == 404, "F14: Reset to defaults, and CalendarStream's own logo again")
    ok(post("/settings/look", intensity="500", duration="100").status_code == 400, "F14: out-of-range Animation values are refused")
print("FAILED:", fails) if fails else print("ALL PASSED")
