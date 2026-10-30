"""Signing in: the first-visit page, the sign-in page, unlock links, signing out, changing the login.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import hmac
import secrets
from urllib.parse import quote

from fastapi import Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse

from .. import main as core
from ..main import (_check_lockout, _count_failure, _count_success, _known_sig, _session_sig, _unlock, app,
    check_csrf, gui_auth, known_browser, KNOWN_COOKIE, KNOWN_DAYS, logins, now, page, renew_csrf, SESSION_COOKIE,
    session_user, state, WELCOME_TOKEN)
from ..logins import LoginError


def new_known() -> str:
    issued = int(now().timestamp())
    return f"{issued}.{_known_sig(issued)}"


def _secure(request: Request) -> bool:
    return request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"


def set_known(back, request: Request):
    """Mark this browser as known (each successful sign-in renews it)."""
    back.set_cookie(KNOWN_COOKIE, new_known(), max_age=KNOWN_DAYS * 86400, httponly=True, samesite="lax",
                    secure=_secure(request))
SESSION_DAYS = 30


def new_session(user: str) -> str:
    until = int(now().timestamp()) + SESSION_DAYS * 86400
    return f"{quote(user, safe='')}.{until}.{_session_sig(user, until)}"


# --- Logins -----------------------------------------------------------------------

@app.get("/welcome")
def welcome(request: Request):
    """First visit: create the status-page login (needs the setup code from the container log)."""
    if logins.has_page_login:
        return RedirectResponse("/", status_code=303)
    return page(request, "welcome.html", {"csrf": WELCOME_TOKEN, "error": ""})


@app.post("/welcome")
def create_login(request: Request, csrf: str = Form(""), code: str = Form(""), user: str = Form(""),
                 password: str = Form(""), confirm: str = Form("")):
    check_csrf(csrf, WELCOME_TOKEN)
    if logins.has_page_login:
        return RedirectResponse("/", status_code=303)
    ip = core._client_ip(request)
    _check_lockout(ip)
    error = ""
    if not logins.check_setup_code(code):
        _count_failure(ip, "setup codes")
        error = ("That setup code isn't right. It's in the container log (docker compose logs | grep "
                 "\"setup code\", in the folder with docker-compose.yml).")
    else:
        try:
            logins.set_page_login(user, password, confirm)
        except LoginError as e:
            error = str(e)
    if error:
        return page(request, "welcome.html", {"csrf": WELCOME_TOKEN, "error": error, "user": user}, status_code=400)
    renew_csrf()
    state.record("info", f"Status-page login created for \"{logins.page_user}\"")
    back = RedirectResponse("/", status_code=303)       # signed in already: no need to type it again
    back.set_cookie(SESSION_COOKIE, new_session(logins.page_user), max_age=SESSION_DAYS * 86400, httponly=True,
                    samesite="lax", secure=_secure(request))
    set_known(back, request)
    return back


LOGIN_TOKEN = secrets.token_urlsafe(24)    # the sign-in page's own form token


def _safe_next(target: str) -> str:
    """Only a path on this site (never another site's address) to go back to after signing in. Browsers drop
    tabs and line breaks from an address ("/<tab>/other.site" is "//other.site"), so no control characters."""
    ok = target.startswith("/") and not target.startswith("//") and "\\" not in target and all(ord(ch) > 32 for ch in target)
    return target if ok else "/"


@app.get("/login")
def login_page(request: Request, next_: str = Query("/", alias="next")):
    """The sign-in page (0.2.8-beta.15)."""
    if not logins.has_page_login:
        return RedirectResponse("/welcome", status_code=303)
    if session_user(request):
        return RedirectResponse(_safe_next(next_), status_code=303)
    return page(request, "login.html", {"csrf": LOGIN_TOKEN, "error": "", "next": _safe_next(next_)})


@app.post("/login")
def login_submit(request: Request, csrf: str = Form(""), user: str = Form(""), password: str = Form(""),
                 next_: str = Form("/", alias="next")):
    check_csrf(csrf, LOGIN_TOKEN)
    ip = core._client_ip(request)
    _check_lockout(ip, known_browser(request))
    if not logins.check_page_login(user, password):
        _count_failure(ip)
        return page(request, "login.html", {"csrf": LOGIN_TOKEN, "error": "That user name or password isn't right.",
                                            "next": _safe_next(next_), "user": user}, status_code=400)
    _count_success(ip)
    back = RedirectResponse(_safe_next(next_), status_code=303)
    back.set_cookie(SESSION_COOKIE, new_session(logins.page_user), max_age=SESSION_DAYS * 86400, httponly=True,
                    samesite="lax", secure=_secure(request))
    set_known(back, request)
    return back


@app.get("/unlock/{token}")
def unlock(request: Request, token: str):
    """(0.2.8-beta.19, F6) The one-time link from the container log: this browser becomes a known browser, so the
    limit for all addresses lets it through to the sign-in page. It works once, within an hour."""
    good = (_unlock["token"] and _unlock["until"] and now() < _unlock["until"]
            and hmac.compare_digest(token.encode(), _unlock["token"].encode()))
    if not good:
        raise HTTPException(404, "This unlock link has expired or was already used.")
    _unlock.update(token=None, until=None)
    state.record("info", f"Unlock link used from {core._client_ip(request)}: that browser can sign in again", kind="Settings")
    back = RedirectResponse("/login", status_code=303)
    set_known(back, request)
    return back


@app.post("/logout", dependencies=[Depends(gui_auth)])
def logout(csrf: str = Form("")):
    """Sign out (Settings › Administrator): this browser's session ends."""
    check_csrf(csrf)
    back = RedirectResponse("/login", status_code=303)
    back.delete_cookie(SESSION_COOKIE)
    return back


@app.post("/settings/login", dependencies=[Depends(gui_auth)])
def change_login(request: Request, csrf: str = Form(""), current: str = Form(""), user: str = Form(""),
                 password: str = Form(""), confirm: str = Form("")):
    """Change the status-page user name and/or password (Settings menu). Needs the current password."""
    check_csrf(csrf)
    ip = core._client_ip(request)
    if not logins.check_page_login(logins.page_user, current):
        _count_failure(ip)
        raise HTTPException(400, "The current password isn't right.")
    try:
        logins.set_page_login(user or logins.page_user, password or current, confirm if password else None)
    except LoginError as e:
        raise HTTPException(400, str(e))
    renew_csrf()
    state.record("info", f"Status-page login changed (user \"{logins.page_user}\")")
    # Every session (this one too) ended with the old password: this browser signs in again with the new one
    back = RedirectResponse("/login", status_code=303)
    back.delete_cookie(SESSION_COOKIE)
    return back
