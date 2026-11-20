"""Holds: google view.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from fastapi import Request
import ipaddress
from datetime import datetime
from urllib.parse import urlparse


def _local_time(value: str | None, lang: str, *, TZ, dates_for, now) -> str:
    """An ISO time as local "15:42" today, or "Oct 19, 15:42" on another day."""
    try:
        when = datetime.fromisoformat(value).astimezone(TZ)
    except (TypeError, ValueError):
        return ""
    return dates_for(lang).when(when, now().date())


def _watch_view(
    lang: str, *, _local_time, destinations, google, notify_address
) -> dict:
    """Instant updates from Google, for the page: on (every source's calendar has them, with the last
    notice) or why not."""
    if not notify_address():
        return {
            "on": False,
            "why": "needs a public https:// address (☰ → Public address)",
        }
    watches = [google.watch_info(d["id"]) for d in destinations("google")]
    for w in watches:
        if w.get("error") and w.get("address") == notify_address():
            return {"on": False, "why": w["error"]}
    if watches and all(w.get("id") for w in watches):
        last = max((w.get("last_notice") or "" for w in watches), default="")
        return {"on": True, "last": _local_time(last or None, lang)}
    return {"on": False, "why": "starts with the next sync"}


def _host_mismatch(request: Request, *, _is_ip, public_url) -> tuple[str, str] | None:
    """(public address host, this page's host) when they differ, e.g. a typo such as ccs vs css."""
    public = urlparse(public_url()).hostname or ""
    here = (request.url.hostname or "").lower()
    if (
        public
        and here
        and public != here
        and here not in ("localhost", "127.0.0.1")
        and not _is_ip(here)
    ):
        return public, here
    return None


def _is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host.strip("[]"))
        return True
    except ValueError:
        return False


def google_view(
    request: Request,
    lang: str,
    *,
    _host_mismatch,
    _is_ip,
    _local_time,
    _watch_view,
    admin_email,
    dest_google,
    destinations,
    google,
    google_job,
    google_redirect_uri,
) -> dict:
    uri = google_redirect_uri(request)
    host = urlparse(uri).hostname or ""
    info = google.info()
    return {
        "configured": google.configured,
        "connected": google.connected,
        "info": info,
        "client_id": google.client_id,
        "has_secret": bool(google.client_secret),
        "check": google.client_check(),
        "checked_at": _local_time(google.client_check().get("at"), lang),
        # Google said it doesn't list this page's redirect URI (only counts for the address checked)
        "redirect_missing": google.client_check().get("redirect_ok") is False
        and google.client_check().get("redirect_uri") == uri,
        "running": google_job.running,
        "last_sync": _local_time(info.get("last_sync"), lang),
        "redirect_uri": uri,
        "watch": _watch_view(lang),
        "host_mismatch": _host_mismatch(request),
        "admin_email": admin_email(),
        "on": bool(destinations("google")),
        "calendars": [
            {"did": d["id"], "name": d["name"], **dest_google(d).cal_info(d["id"])}
            for d in destinations("google")
        ],
        "events": sum(
            int(dest_google(d).cal_info(d["id"]).get("events") or 0)
            for d in destinations("google")
        ),
        # Google only sends sign-ins back to https:// addresses with a public domain name (not a bare IP or .local),
        # or to http://localhost on this computer.
        "redirect_ok": (
            uri.startswith("https://")
            and not _is_ip(host)
            and not host.endswith(".local")
        )
        or host in ("localhost", "127.0.0.1"),
    }
