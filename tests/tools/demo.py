"""A demo CalendarStream for looking at the page: the made-up schedule, work calendar, rules and feeds (seed.py),
nothing downloaded, nothing sent to Google. Started by demo.sh; prints READY when the page can be opened.

http://127.0.0.1:$DEMO_PORT (8177), signed in as t / password1."""
import os, re, subprocess, sys, threading, time
TESTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB, PORT = "csdemo", int(os.environ.get("DEMO_PORT", "8177"))
H, P = os.environ.get("TEST_DB_HOST", "127.0.0.1"), os.environ.get("TEST_DB_PORT", "55432")
U, PW = os.environ.get("TEST_DB_USER", "ccs"), os.environ.get("TEST_DB_PASSWORD", "testpw")
subprocess.run(["psql", "-q", "-h", H, "-p", P, "-U", U, "-d", "postgres", "-c", f"DROP DATABASE IF EXISTS {DB}",
                "-c", f"CREATE DATABASE {DB}"], env={**os.environ, "PGPASSWORD": PW})
os.environ.update(DB_HOST=H, DB_PORT=P, DB_NAME=DB, DB_USER=U, DB_PASSWORD=PW, GUI_USERNAME="t", GUI_PASSWORD="password1",
                  TZ="America/New_York", PUBLIC_URL="", IMAGE_TAG="beta")
for k in ("CCS_USERNAME", "CCS_PASSWORD", "http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
    os.environ.pop(k, None)
sys.path.insert(0, os.path.dirname(TESTS)); sys.path.insert(0, TESTS)
from unittest.mock import patch
import uvicorn, httpx, seed
from app import main, calsync
async def noop(*a, **k): pass
WORK = open(os.path.join(TESTS, "data", "work.ics"), "rb").read()
async def fake_download(url, *a, **k): return calsync.Download(200, body=WORK, debug={"url": url})
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), patch.object(main, "update_loop", noop), \
        patch.object(main, "download", fake_download):
    srv = uvicorn.Server(uvicorn.Config(main.app, port=PORT, log_level="warning"))
    threading.Thread(target=srv.run, daemon=True).start(); time.sleep(2.5)
    c = httpx.Client(base_url=f"http://127.0.0.1:{PORT}", auth=("t", "password1"))
    seed.demo(c, re.search(r'name="csrf" value="([^"]+)"', c.get("/").text)[1], main)
    print("READY", flush=True)
    while True:
        time.sleep(60)
