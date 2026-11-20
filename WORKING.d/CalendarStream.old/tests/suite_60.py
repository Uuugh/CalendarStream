"""0.2.8-beta.25 tests: CCS+ downloads with a browser-like client when United's protection holds curl (I8): the clients
(auto, browser, browser-patient, curl) against a local https server standing in for CCS+ (made-up schedule, Username
U123456): sign-in, 304, 401, a 403 from "Akamai", the silent hold (connected, no reply), a hold that clears on the second
try, https-only redirects, no sign-in sent to another host, five redirects at most, 5 MB at most; feeds still identify
themselves as curl."""
import asyncio, os, ssl, subprocess, sys, tempfile, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "CCS_CLIENT"): os.environ.pop(k, None)
from app import calsync
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)

DEMO = open(os.path.join(HERE, "data", "Demo.ics"), "rb").read()
SEEN = []          # (path, user-agent, has Authorization) of each request
HOLDS = {"flaky": 1}

class Quiet(ThreadingHTTPServer):
    def handle_error(self, request, client_address): pass     # a client that hangs up on /big is expected

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a): pass
    def send(self, code, body=b"", headers=None):
        self.send_response(code)
        for k, v in (headers or {}).items(): self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        path = self.path
        SEEN.append((path, self.headers.get("User-Agent", ""), "Authorization" in self.headers))
        if path == "/hold":
            time.sleep(6); return
        if path == "/flaky" and HOLDS["flaky"] > 0:
            HOLDS["flaky"] -= 1; time.sleep(6); return
        if path in ("/ok", "/flaky"):
            import base64
            want = "Basic " + base64.b64encode(b"U123456:pw").decode()
            if self.headers.get("Authorization") != want:
                return self.send(401, b"no", {"WWW-Authenticate": 'Basic realm="x"'})
            if self.headers.get("If-None-Match") == '"v1"':
                return self.send(304, b"", {"ETag": '"v1"'})
            return self.send(200, DEMO, {"Content-Type": "text/calendar", "ETag": '"v1"', "Last-Modified": "Mon, 02 Nov 2026 10:00:00 GMT"})
        if path == "/deny":
            return self.send(403, b"<html>Access Denied Reference #18.abcd.1234</html>", {"Server": "AkamaiGHost", "Content-Type": "text/html"})
        if path == "/to-ok":
            return self.send(302, b"", {"Location": "/ok"})
        if path == "/to-http":
            return self.send(302, b"", {"Location": "http://localhost:1/ok"})
        if path == "/loop":
            return self.send(302, b"", {"Location": "/loop"})
        if path == "/xhost":
            return self.send(302, b"", {"Location": f"https://127.0.0.1:{self.server.server_port}/echo"})
        if path == "/echo":
            return self.send(200, DEMO if "Authorization" not in self.headers else b"LEAKED", {"Content-Type": "text/calendar"})
        if path == "/big":
            return self.send(200, b"BEGIN:VCALENDAR\n" + b"x" * (6 * 1024 * 1024), {"Content-Type": "text/calendar"})
        if path == "/html":
            return self.send(200, b"<html><body>Please wait</body></html>", {"Content-Type": "text/html"})
        self.send(404, b"nope")

tmp = tempfile.mkdtemp()
cert, key = os.path.join(tmp, "c.pem"), os.path.join(tmp, "k.pem")
subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", key, "-out", cert, "-days", "2", "-subj", "/CN=localhost",
                "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1"], check=True, capture_output=True)
srv = Quiet(("127.0.0.1", 0), H)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); ctx.load_cert_chain(cert, key)
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"https://localhost:{srv.server_port}"
calsync._SESSION_EXTRA = {"verify": cert}
os.environ["CURL_CA_BUNDLE"] = cert          # the curl program trusts the test certificate too
calsync.PAUSE_SCALE = 0

def dl(path, client, **kw):
    kw.setdefault("timeout", 2.0)
    return asyncio.run(calsync.download(BASE + path, "U123456", kw.pop("password", "pw"), client=client, **kw))
def fails_with(path, client, exc, **kw):
    try: dl(path, client, **kw)
    except exc as e: return e
    except Exception as e: return e
    return None

# The client in use
ok(calsync.ccs_client() == "auto", "CCS_CLIENT unset: auto")
os.environ["CCS_CLIENT"] = "Browser"; ok(calsync.ccs_client() == "browser", "CCS_CLIENT is read, in any case")
os.environ["CCS_CLIENT"] = "nonsense"; ok(calsync.ccs_client() == "auto", "an unknown CCS_CLIENT is auto")
os.environ.pop("CCS_CLIENT"); ok(calsync.ccs_client("curl") == "curl", "the argument wins")

for client in ("browser", "curl"):
    SEEN.clear()
    d = dl("/ok", client)
    ok(d.status == 200 and b"BEGIN:VCALENDAR" in d.body and d.etag == '"v1"' and d.last_modified.startswith("Mon, 02 Nov 2026"), f"{client}: signs in and downloads, with its ETag and date")
    ok(d.debug["tried"] == [f"{client}: HTTP 200"] and d.debug["client"], f"{client}: the debug record names the client ({d.debug['client']})")
    ok(SEEN[0][2], f"{client}: the sign-in is sent")
    if client == "browser": ok(SEEN[0][1].startswith("Mozilla/5.0") and "Chrome/" in SEEN[0][1], f"browser: presents itself as a browser ({SEEN[0][1][:40]}…)")
    else: ok(SEEN[0][1].startswith("curl/"), "curl: identifies itself as curl")
    d = dl("/ok", client, etag='"v1"')
    ok(d.not_modified and d.status == 304, f"{client}: 304 when nothing changed")
    e = fails_with("/ok", client, calsync.AuthError, password="wrong")
    ok(isinstance(e, calsync.AuthError) and "rejected the UID" in str(e), f"{client}: a wrong password is an AuthError")
    e = fails_with("/deny", client, calsync.BlockedError)
    ok(isinstance(e, calsync.BlockedError) and "Akamai" in str(e) and "18.abcd.1234" in str(e), f"{client}: a 403 is a BlockedError with United's reference")
    e = fails_with("/html", client, calsync.SourceError)
    ok(isinstance(e, calsync.SourceError) and "not with a calendar file" in str(e), f"{client}: a page that isn't a calendar is refused")
    ok(dl("/to-ok", client).status == 200, f"{client}: a redirect to the same host keeps the sign-in")
    e = fails_with("/to-http", client, calsync.SourceError)
    ok(isinstance(e, calsync.SourceError) and "must start with https://" in str(e), f"{client}: a redirect to http is refused")
    e = fails_with("/loop", client, calsync.SourceError)
    ok(isinstance(e, calsync.SourceError) and "redirected too many times" in str(e), f"{client}: more than five redirects are refused")
    e = fails_with("/big", client, calsync.SourceError)
    ok(isinstance(e, calsync.SourceError) and "more than 5 MB" in str(e), f"{client}: more than 5 MB is refused")
    SEEN.clear()
    d = asyncio.run(calsync.download(BASE + "/xhost", "U123456", "pw", client=client, timeout=2.0))
    ok(d.body == DEMO and not any(a for path, _, a in SEEN if path == "/echo"), f"{client}: the sign-in isn't sent to another host")
    e = fails_with("/hold", client, calsync.NoReplyError, timeout=1.0)
    ok(isinstance(e, calsync.NoReplyError) and "sent no reply within 1 seconds" in str(e) and "Upload & publish" in str(e), f"{client}: the silent hold is a NoReplyError with the usual message")

# An http link is refused before anything is sent, for every client
for client in ("browser", "curl", "auto"):
    try: asyncio.run(calsync.download("http://127.0.0.1:9/Calendar.ics", "u", "p", client=client)); ok(False, f"{client}: http refused")
    except calsync.SourceError as e: ok("must start with https://" in str(e), f"{client}: an http link is refused")

# auto: the second try is longer, and a hold that clears is passed
HOLDS["flaky"] = 1
t0 = time.time(); d = dl("/flaky", "auto", timeout=1.5)
ok(d.status == 200 and d.debug["tried"] == ["browser: no reply in 1 s", "browser: HTTP 200"], f"auto: a hold that clears on the second try is passed ({d.debug['tried']})")
# auto: a hold that doesn't clear tries browser, browser, then curl, and says so
t0 = time.time()
e = fails_with("/hold", "auto", calsync.NoReplyError, timeout=1.0)
ok(isinstance(e, calsync.NoReplyError) and time.time() - t0 >= 3.5, f"auto: browser, browser (longer), then curl before giving up ({time.time() - t0:.1f} s)")
# browser-patient: three tries
HOLDS["flaky"] = 2
d = dl("/flaky", "browser-patient", timeout=1.0)
ok(d.status == 200 and len(d.debug["tried"]) == 3, f"browser-patient: three tries ({d.debug['tried']})")
# auto: a refusal from the browser-like client goes on to the next client; a wrong password does not
e = fails_with("/deny", "auto", calsync.BlockedError)
ok(isinstance(e, calsync.BlockedError), "auto: refused by every client is a BlockedError")
t0 = time.time(); e = fails_with("/ok", "auto", calsync.AuthError, password="wrong")
ok(isinstance(e, calsync.AuthError) and time.time() - t0 < 3, "auto: a rejected password stops at once (no more tries, which would lock the account)")

# Feeds identify themselves honestly: curl, whatever CCS_CLIENT says
os.environ["CCS_CLIENT"] = "browser"; SEEN.clear()
d = asyncio.run(calsync.download(BASE + "/echo", who="localhost", timeout=2.0))
ok(d.status == 200 and SEEN[0][1].startswith("curl/") and d.debug["client"].startswith("curl"), f"a feed's download is curl's, not the browser-like client's ({SEEN[0][1]})")
os.environ.pop("CCS_CLIENT")

srv.shutdown()
print("FAILED:", fails) if fails else print("ALL PASSED")
