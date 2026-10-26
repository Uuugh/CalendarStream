"""0.0.12 tests: Google connect / disconnect against the mock Google."""
import os, re, sys, threading, time
from urllib.parse import parse_qs, urlparse
for k in list(os.environ):
    if k.lower() in ("http_proxy", "https_proxy", "all_proxy"):
        del os.environ[k]
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="p", TZ="America/New_York", PUBLIC_URL="http://localhost",
                  CCS_USERNAME="", CCS_PASSWORD="")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(__file__))
import uvicorn, mockgoogle
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import gsync, main

M = "http://127.0.0.1:8099"
gsync.AUTH_URL, gsync.TOKEN_URL, gsync.REVOKE_URL, gsync.API_URL = M + "/auth", M + "/token", M + "/revoke", M + "/calendar/v3"
srv = uvicorn.Server(uvicorn.Config(mockgoogle.app, port=8099, log_level="warning"))
threading.Thread(target=srv.run, daemon=True).start(); time.sleep(1)
GI = lambda: {**main.google.info(), **(main.google.cal_info(main.destinations('google')[0]['id']) if main.destinations('google') else {})}
S, A = mockgoogle.S, ("t", "p")
import httpx
G = httpx.Client()
async def noop(*a, **k): pass
ok = lambda c, label: print(("PASS " if c else "FAIL ") + label)


def connect(c, csrf):
    r = c.post("/google/connect", auth=A, data={"csrf": csrf}, follow_redirects=False)
    assert r.status_code == 303, r.text
    to_google = r.headers["location"]
    q = parse_qs(urlparse(to_google).query)
    back = G.get(to_google, follow_redirects=False)               # the "consent" step
    cb = urlparse(back.headers["location"])
    return q, c.get(cb.path + "?" + cb.query, auth=A, follow_redirects=False)


with patch.object(main, "loop", noop), TestClient(main.app) as c:
    page = c.get("/", auth=A).text
    csrf = re.search(r'name="csrf" value="([^"]+)"', page)[1]
    if len(sys.argv) < 3 or sys.argv[2] != "unconfigured":
        r = c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "test-client.apps.googleusercontent.com",
                   "client_secret": "test-secret", "action": "save"}, follow_redirects=False)
        assert r.status_code == 303, r.text
        page = c.get("/", auth=A).text
    if len(sys.argv) > 2 and sys.argv[2] == "unconfigured":
        ok("Guided setup: a client ID and secret, step by step" in page and 'action="/google/connect"' not in page, "unconfigured: guide shown, no Connect")
        ok(c.post("/google/connect", auth=A, data={"csrf": csrf}).status_code == 400, "unconfigured: connect refused")
        bad = c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "nonsense", "client_secret": "x"})
        ok(bad.status_code == 400 and "client ID" in bad.text, "client ID checked")
        bad = c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "123456789012-abcdef.apps.googleusercontent.com"})
        ok(bad.status_code == 400 and "secret" in bad.text, "secret required the first time")
        ok(c.post("/google/client", auth=A, data={"csrf": "x", "client_id": "a", "client_secret": "b"}).status_code == 400, "client form needs CSRF")
        c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "123456789012-abcdef.apps.googleusercontent.com", "client_secret": "GOCSPX-shh"})
        saved = main.store.get("google_client")
        ok(saved["id"] == "123456789012-abcdef.apps.googleusercontent.com" and "GOCSPX-shh" not in str(saved), "secret stored encrypted")
        page = c.get("/", auth=A).text
        ok("GOCSPX-shh" not in page and "Saved (leave empty to keep it)" in page and 'action="/google/connect"' in page, "secret never shown; Connect appears")
        c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "987654321098-zyxwvu.apps.googleusercontent.com", "client_secret": ""})
        main.google._client = None
        ok(main.google.client() == ("987654321098-zyxwvu.apps.googleusercontent.com", "GOCSPX-shh"), "empty secret keeps the saved one")
        c.post("/google/client", auth=A, data={"csrf": csrf, "action": "remove"})
        ok(not main.google.configured and main.store.get("google_client") is None, "client removed")
        log = " | ".join(h["msg"] for h in main.store.recent_log(10))
        ok("GOCSPX" not in log, "secret never logged")
        sys.exit()
    ok('action="/google/connect"' in page and "http://localhost/google/callback" in page, "Connect button and redirect URI shown")
    ok(c.post("/google/connect", auth=A, data={"csrf": "x"}).status_code == 400, "connect needs CSRF")
    ok(c.post("/google/connect", data={"csrf": csrf}).status_code == 401, "connect needs the status-page login")
    ok(c.get("/google/callback?state=x&code=y").status_code == 401, "callback needs the status-page login")

    q, r = connect(c, csrf)
    ok(q["redirect_uri"] == ["http://localhost/google/callback"] and q["prompt"] == ["consent"], "consent URL parameters")
    ok(r.status_code == 303 and r.headers["location"] == "/?menu=settings#googlesync", "callback returns to Google Calendar sync in Settings (0.2.8-beta.4)")
    info = GI()
    ok(main.google.connected and info.get("email") == "pilot@example.com", f"connected as {info.get('email')}")
    ok(info.get("calendar_id") in S["calendars"] and S["calendars"][info["calendar_id"]]["summary"] == main.calendar_name(),
       f"calendar created: {info.get('calendar_name')}")
    ok(S["calendars"][info["calendar_id"]]["timeZone"] == "America/New_York", "calendar time zone")
    saved = main.store.get("google_token")
    refresh = next(iter(S["refresh"]))
    ok(refresh not in str(saved) and saved.get("v") == 1, "refresh token stored encrypted")
    p = c.get("/?menu=google", auth=A).text
    ok('title="pilot@example.com">pilot@example.com</div>' in p, "the Google box shows the account (in its header, beta.12)")
    ok(c.post("/google/client", auth=A, data={"csrf": csrf, "client_id": "new-1.apps.googleusercontent.com", "client_secret": "z"}).status_code == 400,
       "client can't change while connected")
    log = [h["msg"] for h in main.store.recent_log(5)]
    ok(any("connected as pilot@example.com" in m and "created" in m for m in log), "activity log: connected")

    # Reusing the state value must fail (one-time)
    r = c.get(f"/google/callback?state={q['state'][0]}&code=abc", auth=A, follow_redirects=False)
    ok("expired or was already used" in GI().get("last_error", ""), "state is one-time")

    # Access token refresh: drop the cached token and call the API
    import asyncio
    main.google._access = None
    main.google._keys = {}
    got = asyncio.run(main.google.api("GET", f"/calendars/{info['calendar_id']}"))
    ok(got and got["id"] == info["calendar_id"], "refresh token decrypts and refreshes the access token")

    # Retry on rate limit, then succeed
    S["fail_next"] = [(403, "rateLimitExceeded"), (503, "backendError")]
    t0 = time.time(); got = asyncio.run(main.google.api("GET", f"/calendars/{info['calendar_id']}"))
    ok(got and time.time() - t0 >= 2.5, f"backs off on rate limit and 503 ({time.time() - t0:.1f}s)")

    # Reconnect: same account reuses the calendar
    first = info["calendar_id"]
    q, r = connect(c, csrf)
    ok(GI()["calendar_id"] == first and len(S["calendars"]) == 1, "reconnect reuses the calendar")

    # Disconnect keeping the calendar
    r = c.post("/google/disconnect", auth=A, data={"csrf": csrf}, follow_redirects=False)
    ok(not main.google.connected and first in S["calendars"] and S["revoked"], "disconnect: revoked, calendar kept")
    ok(GI().get("calendar_id") == first, "calendar ID remembered for a reconnect")
    q, r = connect(c, csrf)
    ok(GI()["calendar_id"] == first, "reconnect after disconnect finds it again")

    # Disconnect deleting the calendar
    c.post("/google/disconnect", auth=A, data={"csrf": csrf, "delete": "1"})
    ok(not S["calendars"] and not GI().get("calendar_id"), "disconnect + delete removes the calendar")
    log = [h["msg"] for h in main.store.recent_log(3)]
    ok(any("and its calendar deleted" in m for m in log), "activity log: disconnected and deleted")

    # Calendar permission unticked on the consent screen
    S["grant_calendar"] = False
    q, r = connect(c, csrf)
    ok(not main.google.connected and "calendar permission" in GI().get("last_error", ""), "refuses a sign-in without the calendar permission")
    p = c.get("/", auth=A).text
    ok("calendar permission ticked" in p, "error shown in the menu")
    S["grant_calendar"] = True

    # Cancelled on Google's page
    c.get("/google/callback?error=access_denied&state=x", auth=A)
    ok(GI().get("last_error") .startswith("Google sign-in was cancelled or refused."), "cancel reported")

    # Successful sign-in clears the error; a different account starts a new calendar
    q, r = connect(c, csrf)
    one = GI()["calendar_id"]
    ok(not GI().get("last_error"), "successful sign-in clears the error")
    c.post("/google/disconnect", auth=A, data={"csrf": csrf})
    S["email"] = "other@example.com"
    q, r = connect(c, csrf)
    ok(GI()["calendar_id"] != one and GI()["email"] == "other@example.com", "other account gets its own calendar")

    # Revoked in Google: the stored sign-in stops working
    for t in S["refresh"]: S["revoked"].add(t)
    main.google._access = None
    try:
        asyncio.run(main.google.api("GET", "/calendars/x")); ok(False, "revoked detected")
    except gsync.AccessRevoked as e:
        ok("Connect again" in str(e), "revoked access detected")

    # Wrong DB_PASSWORD can't decrypt the token
    from app.secretbox import SecretBox; main.google.box = SecretBox("different")
    try:
        main.google._refresh_token(); ok(False, "wrong key")
    except gsync.AccessRevoked as e:
        ok("DB_PASSWORD" in str(e), "a different DB_PASSWORD can't read the token")
srv.should_exit = True
