"""Status for programs and for debugging: /api/status, the report data, debug files, /healthz.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import os
import platform
import re

from fastapi import Depends, HTTPException
from fastapi.responses import Response

from .. import main as core
from ..main import (app, calendar_name, destinations, google, google_job, gui_auth, log, logins, public_url, skey,
    source, source_ids, sources, st, State, store, TZ, updater)
from ..config import settings
from ..updates import channel as release_channel


@app.get("/api/status", dependencies=[Depends(gui_auth)])
def api_status():
    """Machine-readable status for monitoring (status-page login)."""
    fmt = lambda d: d.isoformat() if d else None

    def one(sid: str) -> dict:
        S = st(sid)
        return {"id": sid, "name": calendar_name(sid), "type": (source(sid) or {}).get("type"), "status": S.status,
                "message": S.message, "running": S.running, "last_attempt": fmt(S.last_attempt),
                "last_success": fmt(S.last_success), "last_change": fmt(S.last_change), "next_run": fmt(S.next_run),
                "events": S.event_count}
    found = [one(sid) for sid in source_ids()]
    # The top-level fields are CCS+'s (as before 0.2), or the first source's.
    first = st("ccs") if "ccs" in source_ids() else (st(source_ids()[0]) if found else State("none"))
    return {"version": core.__version__, "updating": core.updating_to(), "status": first.status, "message": first.message, "running": first.running,
            "last_attempt": fmt(first.last_attempt), "last_success": fmt(first.last_success),
            "last_change": fmt(first.last_change), "last_auth": fmt(first.last_auth),
            "last_auth_ok": first.last_auth_ok, "next_run": fmt(first.next_run), "events": first.event_count,
            "sources": found,
            "destinations": [{k: d[k] for k in ("id", "type", "name", "sources")} for d in destinations()],
            # Google: a sync asked for (pending) or running, and whether the last one failed
            "google": {"connected": google.connected, "running": google_job.running, "pending": google_job.wake.is_set(),
                       "error": bool(google.info().get("last_error"))}}


def redact(text: str) -> str:
    """Take private details out of text for a problem report: the CCS+ username, feed links and
    stream names, the public address, e-mail addresses, the Google client ID and long secrets."""
    out = text or ""
    secrets_ = [logins.ccs()[0], public_url(), store.get("admin_email") or "", (google.client_id or "")]
    secrets_ += [x.get("url") or "" for x in sources()] + [d.get("token") or "" for d in destinations()]
    for value in sorted({v for v in secrets_ if v and len(v) >= 3}, key=len, reverse=True):
        out = out.replace(value, "[private]")
    out = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[e-mail]", out)
    out = re.sub(r"(?i)(password|secret|token|authorization|cookie)([\"']?\s*[:=]\s*)\S+", r"\1\2[private]", out)
    return re.sub(r"\b[A-Za-z0-9_-]{32,}\b", "[private]", out)


@app.get("/report/data", dependencies=[Depends(gui_auth)])
def report_data():
    """What Report a problem can attach, private details taken out: the recent History lines
    lines, each source's last download details, and this install's setup. The page shows it in the
    report's preview; nothing is sent anywhere from here."""
    lines = [f"{h['time'].astimezone(TZ):%Y-%m-%d %H:%M:%S} {h['level']:5} {h['msg']}" for h in store.recent_log(60)]
    found = []
    for sid in source_ids():
        S, debug = st(sid), store.get_debug(skey(sid, "response"))
        found.append({"id": sid, "name": calendar_name(sid), "type": (source(sid) or {}).get("type"),
                      "status": f"{S.status}: {S.message}",
                      "debug": redact(debug[0].decode("utf-8", "replace") if debug else "")[:6000]})
    return {"version": core.__version__, "image_tag": os.environ.get("IMAGE_TAG") or "latest", "channel": release_channel(),
            "server": f"Python {platform.python_version()} on {platform.system()} {platform.machine()}",
            "time_zone": settings.timezone, "sources": [{**x, "status": redact(x["status"])} for x in found],
            "destinations": [d["type"] for d in destinations()], "google_connected": bool(google.connected),
            "updater": updater.ready, "activity": redact("\n".join(lines))}


@app.get("/debug/{name}", dependencies=[Depends(gui_auth)])
def debug_file(name: str):
    """The last download's response details or calendar file, for debugging (status-page login)."""
    ok = re.fullmatch(r"(source|response)(:f[0-9a-f]{6})?", name)
    found = store.get_debug(name) if ok else None
    if not found:
        raise HTTPException(404)
    content, content_type = found
    if name.startswith("source"):   # show it in the browser rather than downloading
        content_type = "text/plain; charset=utf-8"
    return Response(content, media_type=content_type)


@app.get("/healthz")
def health():
    try:
        store.event_count()
    except Exception as e:
        log.warning("Health check: database unavailable: %s", e)
        raise HTTPException(503, "database unavailable")
    return {"ok": True}
