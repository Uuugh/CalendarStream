"""Deploy fixes: public address, redirect check, guide, cross-site guard, headers, tokens, https-only downloads."""
import asyncio, os, re, sys
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="", GUI_PASSWORD="", TZ="America/New_York", PUBLIC_URL="http://192.168.1.5:8080")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"): os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
import httpx
from fastapi.testclient import TestClient
from app import main, gsync, calsync
from app.config import normalise_public_url
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), TestClient(main.app, base_url="https://css.uuugh.com") as c:
    ok(main.settings.public_base_url == "" and main.public_url() == "", "the old installer default (http://<IP>:8080) counts as no public address")
    # First visit: its own token
    w = c.get("/welcome").text
    wtok = re.search(r'name="csrf" value="([^"]+)"', w)[1]
    ok(wtok != main.CSRF_TOKEN, "the first-visit page has its own token")
    main.logins.set_page_login("pilot", "longenough1", "longenough1")
    A = ("pilot", "longenough1")
    ok(c.post("/settings/public-url", auth=A, data={"csrf": wtok, "url": "x.com"}).status_code == 400, "the first-visit token can't post status-page forms")
    p = c.get("/", auth=A).text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    ok("https://css.uuugh.com/google/callback" in p, "no public address: the redirect URI uses the address the page is opened at")
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "CSS.UUugh.com/", "action": "save"})
    ok(main.public_url() == "https://css.uuugh.com", f"public address tidied: lower case, https, no slash ({main.public_url()})")
    ok([normalise_public_url(v) for v in ("HTTPS://X.com:443/", "http://a.b:80")] == ["https://x.com", "http://a.b"], "default ports dropped, scheme lower-cased")
    # Redirect URI check
    class Resp:
        def __init__(self, body): self.content = b"x"; self._b = body; self.status_code = 400
        def json(self): return self._b
    class C:
        body = {}
        def __init__(self, *a, **k): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *a): pass
        async def post(self, *a, **k): return Resp(C.body)
    main.store.set("google_client", {"id": "1-abc.apps.googleusercontent.com", "secret": main.google._seal("s")}); main.google._client = None
    with patch.object(gsync.httpx, "AsyncClient", C):
        C.body = {"error": "redirect_uri_mismatch"}
        r = asyncio.run(main.google.check_client("https://css.uuugh.com/google/callback"))
        ok(r["ok"] is True and r["redirect_ok"] is False, "redirect_uri_mismatch: ID and secret ✓, redirect URI ✗")
        p = c.get("/", auth=A).text
        ok("Address missing" in p and "Authorized redirect URIs › + Add URI › https://css.uuugh.com/google/callback" in p
           and "Check both values" not in p, "page: Address missing, and the line under the row with the exact URI to add (beta.14)")
        ok('<button type="button" class="ghost gcopyaddr" onclick' in p and 'class="btn ghostbtn gopenclient"' in p and 'gopenclient" href="https://console.cloud.google.com/auth/clients" target="_blank" rel="noopener" hidden' not in p,
           "…with Copy the address and Open your client")
        c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://other.example.com", "action": "save"})
        p = c.get("/", auth=A).text
        ok("Address missing" not in p, "a check of another address doesn't count")
        c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://css.uuugh.com", "action": "save"})
        C.body = {"error": "invalid_grant"}
        r = asyncio.run(main.google.check_client("https://css.uuugh.com/google/callback"))
        ok(r["ok"] is True, "invalid_grant → ✓ (ID, secret and redirect accepted)")
    p = c.get("/", auth=A).text
    ok("doesn’t list" not in p and "doesn&#39;t list" not in p and "Ready to connect" in p and 'class="syncnow gconnectbtn"' in p, "after a good check: Ready to connect")
    ok([normalise_public_url(v) for v in ("https://x.com/a",)] == ["https://x.com/a"], "paths kept")
    for bad in ("http:/example.com", "https://x.com/a;b"):
        try: normalise_public_url(bad); ok(False, f"{bad} refused")
        except ValueError: ok(True, f"{bad} refused")
    os.environ["PUBLIC_URL"] = "http://localhost:8080"
    from app import config as cfgmod
    ok(cfgmod._public_url() == "", "the old macOS default (http://localhost:8080) counts as not set too")
    os.environ["PUBLIC_URL"] = "http://192.168.1.5:8080"
    # Guide hides an unusable redirect URI
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://192.168.1.5", "action": "save"})
    p = c.get("/", auth=A).text
    ok("https://192.168.1.5/google/callback" not in p and "First: ☰ Settings › <b>Public address</b>" in p, "an https IP address: no redirect URI shown, asks for the public address")
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://printer.local", "action": "save"})
    p = c.get("/", auth=A).text
    ok("https://printer.local/google/callback" not in p, "a .local address isn't offered to Google")
    c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "https://css.uuugh.com", "action": "save"})
    # Global failure limit: guesses from many made-up addresses still stop
    main._global_failures.clear(); main._gui_failures.clear()
    with patch.object(main, "_client_ip", lambda request: request.headers.get("x-forwarded-for", "?")):   # as if each came from its own address
        main._good_ips.clear()
        codes = [c.get("/", auth=("pilot", f"wrong{i}"), headers={"X-Forwarded-For": f"203.0.113.{i}"}).status_code for i in range(60)]
        ok(codes.count(429) >= 9 and codes[:50].count(429) == 0, f"after {main.GLOBAL_MAX_FAILURES} failures from any addresses, new addresses wait ({codes.count(429)} refused)")
        main._good_ips["198.51.100.7"] = main.now()     # the owner logged in from here earlier
        ok(c.get("/", auth=A, headers={"X-Forwarded-For": "198.51.100.7"}).status_code == 200, "…but the owner's recent address still gets in (no lock-out by strangers)")
        ok(c.get("/", auth=A, headers={"X-Forwarded-For": "203.0.113.200"}).status_code == 429, "…while a new address waits even with the right password")
    # a check saved by 0.1.20 reads as "ID and secret fine, redirect missing"
    main.store.set("google_client", {"id": "1-abc.apps.googleusercontent.com", "secret": main.google._seal("s"),
        "check": {"ok": False, "message": "Google doesn't list https://css.uuugh.com/google/callback under Authorised redirect URIs; add it to the client in Google Cloud", "at": "2026-10-21T10:00:00+00:00"}})
    main.google._client = None
    ck = main.google.client_check()
    ok(ck["ok"] is True and ck["redirect_ok"] is False and ck["redirect_uri"] == "https://css.uuugh.com/google/callback", "a 0.1.20 check upgrades to the new state")
    main._global_failures.clear(); main._gui_failures.clear()
    # Cross-site guard and headers
    r = c.post("/settings/public-url", auth=A, data={"csrf": csrf, "url": "evil.com"}, headers={"Sec-Fetch-Site": "cross-site"})
    ok(r.status_code == 403 and main.public_url() == "https://css.uuugh.com", "cross-site form posts are refused")
    ok(c.post("/google/notify", headers={"Sec-Fetch-Site": "cross-site", "X-Goog-Channel-ID": "x"}).status_code == 200, "Google's notifications still accepted")
    r = c.get("/", auth=A)
    ok(r.headers.get("x-frame-options") == "SAMEORIGIN" and "frame-ancestors 'self'" in r.headers.get("content-security-policy", "")
       and r.headers.get("x-content-type-options") == "nosniff" and r.headers.get("referrer-policy") == "no-referrer", "security headers on every page")
    ok(c.get("/calendar/%C3%A9.ics").status_code == 404, "a non-ASCII feed token is a 404, not a crash")
    # https-only downloads
    try:
        asyncio.run(calsync.download("http://127.0.0.1:9/Calendar.ics", "u", "p"))
        ok(False, "http download refused")
    except calsync.SourceError as e:
        ok("must start with https://" in str(e), f"http download refused by curl: {e}")
print("FAILED:", fails) if fails else print("ALL PASSED")
