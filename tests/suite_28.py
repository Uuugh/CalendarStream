import os, sys, threading, time, re, asyncio
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York")
for k in ("CCS_USERNAME","CCS_PASSWORD","PUBLIC_URL","http_proxy","https_proxy","HTTP_PROXY","HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import uvicorn, httpx
from app import main, calsync
async def noop(*a, **k): pass
SCHEME = "light"; fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
DEMO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "Demo.ics"), "rb").read()
async def fake_download(url, username="", password="", etag="", last_modified="", who="CCS+", **k):
    await asyncio.sleep(1.2)
    if password == "wrong":
        raise calsync.AuthError("CCS+ rejected the UID or Calendar Sync password (HTTP 401). Check both in the CCS+ Calendar Sync box (the Calendar Sync password, not your CCS login).")
    return calsync.Download(200, body=DEMO, debug={"url": url})
errs = []
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=8093, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2)
    c = httpx.Client(base_url="http://127.0.0.1:8093", auth=("t","password1"))
    csrf = re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1]
    c.post("/sources/add", data={"csrf": csrf, "type": "ccs"})
    main.logins.save_ccs("U123456", "pw12345"); asyncio.run(main.run_once(manual=True))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(extra_http_headers={"Authorization":"Basic dDpwYXNzd29yZDE="}, viewport={"width":1100,"height":900}, color_scheme=SCHEME)
        pg = ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8093/"); pg.wait_for_timeout(300)
        pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(150)
        form = pg.locator("#src-ccs form.ccsform"); slotsel = "#src-ccs .okslot"
        shot = lambda name: None
        state = lambda: pg.get_attribute(slotsel, "data-state")
        ok(state() == "ok", "starts at ✓ Validated")
        pg.fill("#src-ccs input[name=password]", "pw12345"); pg.wait_for_timeout(350)
        ok(state() == "edit" and pg.is_visible("#src-ccs .slotsave") and pg.is_visible("#src-ccs .slotcancel"), "typing: Save and Cancel")
        pg.click("#src-ccs .slotcancel"); pg.wait_for_timeout(120); ok(state() == "cancel", "Cancel fills the slot")
        pg.wait_for_timeout(600); ok(state() == "ok" and pg.input_value("#src-ccs input[name=password]") == "", "… then fades back to ✓, typing undone")
        pg.fill("#src-ccs input[name=password]", "pw12345"); pg.wait_for_timeout(350)
        pg.click("#src-ccs .slotsave"); pg.wait_for_timeout(150); ok(state() in ("saving", "verifying"), "Save fills the slot")
        seen = set()
        for _ in range(30):
            seen.add(pg.inner_text("#src-ccs .slotsave")); pg.wait_for_timeout(50)
        ok("Saved" in seen, "… says Saved")
        states = []
        for _ in range(60):
            states.append((state(), pg.inner_text("#src-ccs .slotmsg"))); pg.wait_for_timeout(50)
            if states[-1][0] == "valid": break
        ok(("verifying", "Verifying…") in states, "… then Verifying…")
        ok(states[-1][0] == "valid" and "Validated" in states[-1][1], "… then ✓ Validated")
        pg.wait_for_timeout(2500)
        if pg.locator("#cfg-ccs[hidden]").count(): pg.click("#src-ccs .cfgtoggle"); pg.wait_for_timeout(150)
        ok(state() == "ok", "page drawn again with ✓")
        pg.fill("#src-ccs input[name=password]", "wrong"); pg.wait_for_timeout(200)
        pg.click("#src-ccs .slotsave"); pg.wait_for_timeout(3500); ok(state() == "failed" and "Failed" in pg.inner_text("#src-ccs .slotmsg") and pg.locator("#src-ccs .slotnote").count() == 1, "a wrong password: ✗ Verification failed, with the reason")
        pg.fill("#src-ccs input[name=uid]", "U123457"); pg.wait_for_timeout(200); ok(state() == "edit" and pg.locator("#src-ccs .slotnote").count() == 0, "typing again: Save and Cancel, reason cleared")
        pg.goto("http://127.0.0.1:8093/?menu=settings"); pg.wait_for_timeout(300)
        pg.fill("#lnew", "x"); pg.wait_for_timeout(300); ok(pg.is_visible("#pagelogin .slotcancel") and pg.is_visible("#lcur"), "page login: Save and Cancel, current password asked")
        r = c.post("/setup/ccs", data={"csrf": csrf, "uid": "bad id!", "password": ""}, headers={"X-CS-Async": "1"})
        ok(r.status_code == 400 and "Username" in r.json().get("detail", ""), "a refused save answers with the reason (for under the boxes)")
        r = c.post("/verify", data={"csrf": csrf, "kind": "nope"}, headers={"X-CS-Async": "1"})
        ok(r.status_code == 400, "unknown kinds refused")
        b.close()
    srv.should_exit = True
ok(not errs, f"no script errors {errs}")
print("FAILS", fails)
