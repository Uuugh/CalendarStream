"""Holds: authentication.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from fastapi import Request
from fastapi.security import HTTPBasicCredentials
import hashlib
import hmac
import ipaddress
import secrets
import socket
from datetime import timedelta
from urllib.parse import unquote, urlencode, urlparse
from fastapi import HTTPException


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "?"


def _own_network(ip: str, *, _LOCAL_NETS, _domain_ips, now, public_addresses) -> bool:
    """An address the limit for all addresses together never shuts out (review #6.1, the Developer's decision): a
    local one (192.168.x.x, 10.x, 172.16–31.x, this machine, IPv6 local) or the IP a public address's domain
    points at (the owner's own connection, when CalendarStream is reached at home through it).
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    if any(addr in net for net in _LOCAL_NETS if net.version == addr.version):
        return True
    if _domain_ips["at"] is None or now() - _domain_ips["at"] > timedelta(minutes=10):
        found = set()
        for url in public_addresses():
            host = urlparse(url).hostname
            if not host:
                continue
            try:
                found |= {i[4][0] for i in socket.getaddrinfo(host, None)}
            except OSError:
                pass
        _domain_ips.update(at=now(), ips=found)
    return ip in _domain_ips["ips"]


def _known_sig(issued: int, *, _session_key) -> str:
    return hmac.new(
        _session_key(), f"known\0{issued}".encode(), hashlib.sha256
    ).hexdigest()


def known_browser(
    request: Request, *, KNOWN_COOKIE, KNOWN_DAYS, _known_sig, now
) -> bool:
    """The browser has signed in here before (its signed cookie, within KNOWN_DAYS)."""
    try:
        issued, sig = request.cookies.get(KNOWN_COOKIE, "").split(".")
        issued_n = int(issued)
    except ValueError:
        return False
    if now().timestamp() - issued_n > KNOWN_DAYS * 86400:
        return False
    return hmac.compare_digest(sig, _known_sig(issued_n))


def _new_unlock(*, UNLOCK_FOR, _unlock, now, public_addresses) -> str:
    """A one-time unlock link for the container log, replacing any earlier one."""
    token = secrets.token_urlsafe(24)
    _unlock.update(token=token, until=now() + UNLOCK_FOR)
    base = (public_addresses() or [""])[0].rstrip("/")
    return f"{base}/unlock/{token}"


def _check_lockout(
    ip: str,
    known: bool,
    *,
    GLOBAL_MAX_FAILURES,
    GOOD_IP_FOR,
    GUI_LOCKOUT,
    _failures_lock,
    _global_failures,
    _good_ips,
    _gui_failures,
    _own_network,
    now,
):
    own = _own_network(ip)  # (looked up before the lock: it may ask DNS)
    with _failures_lock:
        locked_until = _gui_failures.get(ip, [0, None])[1]
        if locked_until and now() < locked_until:
            raise HTTPException(429, "Too many failed attempts. Try again later.")
        # A limit for all addresses together, so guessing from many (made-up) addresses doesn't help.
        # Addresses that logged in successfully in the last 7 days (since the last restart) are exempt, so
        # strangers can't lock out the browsers the owner uses.
        cutoff = now() - GUI_LOCKOUT
        while _global_failures and _global_failures[0] < cutoff:
            _global_failures.pop(0)
        trusted = _good_ips.get(ip)
        if (
            len(_global_failures) >= GLOBAL_MAX_FAILURES
            and not own
            and not known
            and not (trusted and now() - trusted < GOOD_IP_FOR)
        ):
            raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_failure(
    ip: str,
    what: str,
    *,
    GLOBAL_MAX_FAILURES,
    GUI_LOCKOUT,
    GUI_MAX_FAILURES,
    _failures_lock,
    _global_failures,
    _gui_failures,
    _new_unlock,
    log,
    now,
    state,
):
    with _failures_lock:
        if (
            len(_gui_failures) > 10_000
        ):  # bounded: forget addresses that aren't locked out first
            for key in [
                k
                for k, (_, until) in list(_gui_failures.items())
                if not until or until < now()
            ][:5_000]:
                _gui_failures.pop(key, None)
        _global_failures.append(now())
        everyone = (
            len(_global_failures) == GLOBAL_MAX_FAILURES
        )  # the moment the limit for all addresses is reached
        count = _gui_failures.get(ip, [0, None])[0] + 1
        locked = now() + GUI_LOCKOUT if count >= GUI_MAX_FAILURES else None
        _gui_failures[ip] = [0 if locked else count, locked]
    if everyone:  # (review #6.1) said once, with the ways back in
        link = _new_unlock()
        log.warning(
            "Sign-ins paused for new browsers after %s failed attempts. To let your browser in, open this "
            "link in it within an hour (it works once): %s",
            GLOBAL_MAX_FAILURES,
            link,
        )
        state.record(
            "warn",
            f"{GLOBAL_MAX_FAILURES} failed sign-ins from many addresses in {int(GUI_LOCKOUT.total_seconds() // 60)} min: "
            "new browsers wait 15 minutes, except browsers that have signed in here before, your own network (a local "
            "address, or the IP your domain points at) and addresses signed in here in the last 7 days. Locked out "
            "yourself? Open the one-time link in the container log (docker compose logs) within an hour, or restart "
            "CalendarStream (docker compose restart).",
            kind="Settings",
        )
    if locked:
        state.record(
            "warn",
            f"Status page locked for {ip} after {GUI_MAX_FAILURES} failed {what}",
        )
        raise HTTPException(429, "Too many failed attempts. Try again later.")


def _count_success(ip: str, *, _failures_lock, _good_ips, _gui_failures, now):
    with _failures_lock:
        _gui_failures.pop(ip, None)
        if len(_good_ips) > 1_000:
            _good_ips.clear()
        _good_ips[ip] = now()


def _session_key(*, store) -> bytes:
    key = store.get("session_key")
    if not isinstance(key, str) or len(key) < 64:
        key = secrets.token_hex(32)
        store.set("session_key", key)
    return bytes.fromhex(key)


def _session_sig(user: str, until: int, *, _session_key, logins) -> str:
    saved = logins.page_login() or {}
    stamp = (saved.get("password") or {}).get("hash", "")
    return hmac.new(
        _session_key(), f"{user}\0{until}\0{stamp}".encode(), hashlib.sha256
    ).hexdigest()


def session_user(request: Request, *, SESSION_COOKIE, _session_sig, logins, now) -> str:
    """The signed-in user from the session cookie, or ""."""
    raw = request.cookies.get(SESSION_COOKIE, "")
    try:
        user_q, until, sig = raw.split(".")
        user, until_n = unquote(user_q), int(until)
    except ValueError:
        return ""
    if until_n < now().timestamp() or user != logins.page_user:
        return ""
    return user if hmac.compare_digest(sig, _session_sig(user, until_n)) else ""


def gui_auth(
    request: Request,
    creds: HTTPBasicCredentials | None,
    *,
    _check_lockout,
    _client_ip,
    _count_failure,
    _count_success,
    _is_async,
    basic,
    known_browser,
    logins,
    session_user,
):
    """The status-page login. Before one exists, every page leads to the first-visit form; then the sign-in
    page (a session cookie), or HTTP Basic sent by a script."""
    if not logins.has_page_login:
        raise HTTPException(303, headers={"Location": "/welcome"})
    if session_user(request):
        return
    ip = _client_ip(request)
    _check_lockout(ip, known_browser(request))
    if creds and logins.check_page_login(creds.username, creds.password):
        _count_success(ip)
        return
    if creds:  # a real attempt
        _count_failure(ip)
    if (
        request.method == "GET"
        and not _is_async(request)
        and "text/html" in request.headers.get("accept", "")
    ):
        target = request.url.path + (
            f"?{request.url.query}" if request.url.query else ""
        )
        raise HTTPException(
            303, headers={"Location": "/login?" + urlencode({"next": target})}
        )
    raise HTTPException(401, "Sign in again (reload the page).")


def check_csrf(token: str, expected: str | None, *, CSRF_TOKEN):
    if not secrets.compare_digest(
        (token or "").encode(), (expected or CSRF_TOKEN).encode()
    ):
        raise HTTPException(
            400, "This form has expired. Reload the page and try again."
        )


def new_csrf_token() -> str:
    """Renew the form token after credentials change."""
    return secrets.token_urlsafe(24)
