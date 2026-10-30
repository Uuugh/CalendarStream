"""Google Calendar: the API client, connecting accounts, the sign-in callback, change notifications,
Sync now, opening a calendar in Google, and inviting someone to connect theirs.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import re
import secrets
from urllib.parse import parse_qs, urlencode, urlparse

from fastapi import Depends, Form, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPBasicCredentials

from .. import main as core
from ..main import (_did, _invites, _is_async, _remember_calendar, _remembered_calendar, _session_key,
    _shared_grant, app, basic, check_csrf, dest_google, destination, destinations, forget_invites, google,
    google_accounts, google_for, google_job, google_redirect_uri, GOOGLE_SETTINGS, google_view, gui_auth,
    make_invite, page, request_google_sync, save_destinations, state, store)
from ..gsync import GoogleError


# --- Google Calendar connection ---------------------------------------------------

@app.post("/google/client", dependencies=[Depends(gui_auth)])
async def google_client(request: Request, csrf: str = Form(""), client_id: str = Form(""),
                        client_secret: str = Form(""), action: str = Form("save"), back: str = Form("")):
    """Save or remove the Google OAuth client (Google Calendar Autosync box). The secret is stored encrypted and
    never shown again. It can't change while connected: the sign-in belongs to that client."""
    check_csrf(csrf)
    if any(google_for(a).connected for a in google_accounts()) and action == "remove":
        # the trash at the end of the credentials (0.2.8-beta.11, confirmed in the page): disconnect first
        # (CalendarStream's calendars stay in Google), then delete the client; every account uses it (beta.15)
        async with google_job.lock:
            for account in google_accounts():
                g = google_for(account)
                if g.connected:
                    await g.stop_watch(sorted({d["id"] for d in destinations("google") if d["account"] == account} | set(g.calendar_sids())))
                    await g.disconnect(delete_calendar=False)
        state.record("info", "Google Calendar disconnected to delete the OAuth client")
    elif google.connected:
        raise HTTPException(400, "Disconnect Google Calendar before changing the OAuth client.")
    if action == "remove":
        google.clear_client()
        state.record("info", "Google OAuth client removed")
    elif action == "check":
        if google.configured:
            await google.check_client(google_redirect_uri(request))
    else:
        try:
            google.save_client(client_id, client_secret)
        except GoogleError as e:
            raise HTTPException(400, str(e))
        google.record_error("")
        if _is_async(request):
            state.record("info", f"Google OAuth client saved ({google.client_id.split('.')[0][:12]}…)")
            return JSONResponse({"saved": True})      # the page then asks /verify
        check = await google.check_client(google_redirect_uri(request))
        state.record("info" if check["ok"] else "warn",
                     f"Google OAuth client saved ({google.client_id.split('.')[0][:12]}…): {check['message']}")
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


GOOGLE_CLIENTS_PAGE = "https://console.cloud.google.com/auth/clients"


@app.post("/google/step", dependencies=[Depends(gui_auth)])
async def google_step(request: Request, csrf: str = Form(""), step: str = Form(""), client_id: str = Form(""),
                      client_secret: str = Form("")):
    """Connect, one straight line (0.2.8-beta.14): the page runs these steps in order, showing each in
    the status box (Saving…, Checking…, Checking address…), and stops at the first that fails, saying
    what to fix: "save" (the ID and secret typed, if any), "client" (Google accepts them), "address"
    (Google accepts this page's /google/callback for the client), "go" (Google's sign-in page)."""
    check_csrf(csrf)
    view = google_view(request)
    uri = view["redirect_uri"]
    def stop(message: str, **fix):
        return JSONResponse({"ok": False, "step": step, "message": message, "fix": fix})
    if step == "save":
        if client_id.strip() and (client_id.strip() != google.client_id or client_secret.strip()):
            try:
                google.save_client(client_id, client_secret)
            except GoogleError as e:
                return stop(str(e))
            google.record_error("")
            state.record("info", f"Google OAuth client saved ({google.client_id.split('.')[0][:12]}…)")
        if not google.configured:
            return stop("Client ID and Client secret: from Google Cloud › Clients › CalendarStream (Guided setup, below).", guide=True)
        return JSONResponse({"ok": True, "step": step})
    if step == "client":
        check = await google.check_client(uri)
        if check.get("ok") is False:
            return stop(f"{check['message']}: Google Cloud › Clients › CalendarStream › copy both again › Connect.", open=GOOGLE_CLIENTS_PAGE)
        if check.get("ok") is None:
            return stop(check.get("message") or "Couldn't check the client with Google.", retry=True)
        return JSONResponse({"ok": True, "step": step})
    if step == "address":
        if not view["redirect_ok"]:
            return stop("☰ Settings › Public address: this page's https:// address › Save › Connect.")
        ok = await google.check_redirect(uri)
        if ok is False:
            state.record("warn", f"Google doesn't list {uri} under the client's Authorized redirect URIs")
            return stop(f"Address not on your client: Google Cloud › Clients › CalendarStream › Authorized redirect URIs › "
                        f"+ Add URI › {uri} › Save › wait 5 min › Connect.", copy=uri, open=GOOGLE_CLIENTS_PAGE)
        return JSONResponse({"ok": True, "step": step, "confirmed": ok is True})
    if step == "go":
        # 0.2.8-beta.17 (F13): ☰ Settings sets up the API only; each Google module connects its own account
        state.record("info", "Google Calendar API Sync is ready: the Google modules can be added in Feeds", kind="Google")
        return JSONResponse({"ok": True, "step": step, "url": ""})
    raise HTTPException(400, "Unknown step.")


@app.post("/google/connect", dependencies=[Depends(gui_auth)])
async def google_connect(request: Request, csrf: str = Form("")):
    """Send the browser to Google's consent page."""
    check_csrf(csrf)
    view = google_view(request)
    if not view["configured"]:
        raise HTTPException(400, "Save the Google OAuth client ID and secret first.")
    if not view["redirect_ok"]:
        raise HTTPException(400, "Set the public address (Settings → Public address) to this page's https:// address first.")
    return RedirectResponse(google.sign_in_url(view["redirect_uri"]), status_code=303)


def callback_auth(request: Request, creds: HTTPBasicCredentials | None = Depends(basic)):
    """Google's sign-in comes back here: the status page's login, except for an invited person's sign-in
    (0.2.8-beta.17), whose single-use state from the invite page is the permission."""
    if request.query_params.get("state", "") in _invite_states:
        return
    gui_auth(request, creds)


@app.get("/google/callback", dependencies=[Depends(callback_auth)])
async def google_callback(request: Request, state_: str = Query("", alias="state"), code: str = "", error: str = ""):
    """Google sends the browser back here after the consent page, with a one-time code."""
    invited = _invite_states.pop(state_, None)
    if invited is not None:
        return await _invite_finish(request, invited, state_, code, error)
    # (0.2.8-beta.15) the account this sign-in was started for: the first one, or a Google module's own
    g = next((x for x in [google_for(a) for a in google_accounts()] if state_ in x._pending), google)
    mods = [d for d in destinations("google") if d["account"] == g.account]
    # (0.2.8-beta.18, F1) a module's Connect me comes back to that module (open), saying Connected or what went wrong
    back = f"/#dest-{mods[0]['id']}" if g.account and mods else GOOGLE_SETTINGS
    if g.account and mods:
        saved = store.get("ui_sections") or {}
        store.set("ui_sections", {**saved, f"dest:{mods[0]['id']}": True})
    try:
        if error or not code:
            raise GoogleError("Google sign-in was cancelled or refused. If Google said the app is only for "
                              "testers, add your Gmail address under Audience → Test users in Google Cloud."
                              if error in ("access_denied", "") else f"Google sign-in failed: {error[:80]}.")
        async with google_job.lock:      # no sync may start while the calendars are being found or made
            info = await g.finish_sign_in(state_, code)
            g.record_error("")
            found = []
            for d in mods:     # each of its Google modules' calendar: the one from before (I5: also after a new sign-in), or a new one
                await g.ensure_calendar(d["id"], d["name"], _remembered_calendar(d["id"]))
                _remember_calendar(d["id"], g)
                cal = g.cal_info(d["id"])
                found.append(f"calendar \"{cal.get('calendar_name', '')}\" "
                             + ("created" if cal.get("created") else "found again"))
        state.record("info", f"Google Calendar connected as {info.get('email') or 'your account'}"
                     + "".join("; " + f for f in found))
        request_google_sync(full=True)
    except GoogleError as e:
        g.record_error(str(e))
        state.record("error", f"Google: {e}")
    return RedirectResponse(back, status_code=303)


@app.post("/google/account", dependencies=[Depends(gui_auth)])
async def google_account(request: Request, csrf: str = Form(""), did: str = Form(""), action: str = Form("connect")):
    """A Google module's own Gmail (0.2.8-beta.15), so each module can go to a different person: `connect`
    signs in a new account for it (Google's sign-in page); `first` puts it back on the first account
    (Settings'); `disconnect` signs its account out (its calendar stays in Google)."""
    check_csrf(csrf)
    d = _did(did)
    if d["type"] != "google":
        raise HTTPException(400, "Only a Google module has a Google account.")
    view = google_view(request)
    found = destinations()
    if action == "disconnect" and not d["account"]:
        # (0.2.8-beta.17) a module from before, on the first account: it gets an account of its own, not
        # connected; the first account (and every other module on it) stays signed in
        save_destinations([{**x, "account": "a" + secrets.token_hex(3)} if x["id"] == did else x for x in found])
        state.record("info", f"Google, {d['name']}: disconnected (the account stays signed in for the others)", kind="Google")
        return RedirectResponse(f"/#dest-{did}", status_code=303)
    if action == "first":
        save_destinations([{**x, "account": ""} if x["id"] == did else x for x in found])
        state.record("info", f"Google, {d['name']}: back on the first Google account", kind="Google")
        request_google_sync(full=True)
        return RedirectResponse(f"/#dest-{did}", status_code=303)
    if action == "disconnect":
        g = dest_google(d)
        async with google_job.lock:
            await g.stop_watch([did])
            notes = await g.disconnect(delete_calendar=False, revoke=not _shared_grant(g))
        state.record("warn" if notes else "info", f"Google, {d['name']}: {g.info().get('email') or 'its account'} disconnected"
                     + ("; " + "; ".join(notes) if notes else ""), kind="Google")
        return RedirectResponse(f"/#dest-{did}", status_code=303)
    if not view["configured"] or not view["redirect_ok"]:
        raise HTTPException(400, "Needs Google Calendar API Sync, which your admin turns on in ☰ Settings.")
    account = d["account"] or "a" + secrets.token_hex(3)
    save_destinations([{**x, "account": account} if x["id"] == did else x for x in found])
    return RedirectResponse(google_for(account).sign_in_url(view["redirect_uri"]), status_code=303)


@app.post("/google/disconnect", dependencies=[Depends(gui_auth)])
async def google_disconnect(csrf: str = Form(""), delete: str = Form("")):
    """Stop syncing: optionally delete CalendarStream's calendar, then remove its access in Google."""
    check_csrf(csrf)
    if not google.connected:
        return RedirectResponse(GOOGLE_SETTINGS, status_code=303)
    email = google.info().get("email") or "your account"
    async with google_job.lock:      # not in the middle of a sync (the first account; a module's own stays)
        await google.stop_watch(sorted({d["id"] for d in destinations("google") if not d["account"]} | set(google.calendar_sids())))
        notes = await google.disconnect(delete_calendar=delete == "1")
    if delete == "1":
        store.google_forget()
    what = "and its calendar deleted" if delete == "1" and not any("calendar" in n for n in notes) else ""
    state.record("warn" if notes else "info", f"Google Calendar disconnected ({email}) {what}".strip()
                 + ("; " + "; ".join(notes) if notes else ""))
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


@app.post("/google/notify")
async def google_notify(request: Request):
    """Google's change notification for CalendarStream's calendar (no login: Google can't sign in).
    Checked by the channel ID and the secret token CalendarStream gave Google; it carries no
    details, so it just starts a check that puts back events changed or deleted in Google."""
    channel = request.headers.get("x-goog-channel-id", "")
    for account in google_accounts():      # (each Google module's channel is its account's)
        g = google_for(account)
        sid = g.notice_from(channel, request.headers.get("x-goog-channel-token", ""),
                            [d["id"] for d in destinations("google") if d["account"] == account])
        if sid:
            if request.headers.get("x-goog-resource-state") != "sync":   # "sync" only confirms the channel
                g.noticed(sid)
                request_google_sync(full=True)
            break
    return Response(status_code=200)   # anything else makes Google retry; unknown channels just expire


@app.post("/google/sync", dependencies=[Depends(gui_auth)])
async def google_sync_now(request: Request, csrf: str = Form("")):
    """Sync now, checking Google's copy too (repairs events changed or deleted in Google). From the
    page's script it answers at once, and the page follows it in /api/status (see /run)."""
    check_csrf(csrf)
    request_google_sync(full=True)
    await asyncio.sleep(0.5)
    if _is_async(request):
        return {"ok": True}
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


def google_calendar_url(email: str) -> str:
    """Google Calendar in that Gmail (0.2.8-beta.19, F7). No ?cid=: CalendarStream's calendar is already in the
    account's list, and a cid link only brings up Google's "Add calendar?" for it."""
    return "https://calendar.google.com/calendar/r" + (f"?{urlencode({'authuser': email})}" if email else "")


@app.get("/google/open/{did}", dependencies=[Depends(gui_auth)])
def google_open(request: Request, did: str, check: int = Query(0)):
    """(0.2.8-beta.19, F7) The tab a Google module's first Sync Now opens: "Making the calendar…" until the sync
    is done, then Google Calendar. With ?check=1 it answers {"url": …} once ready ({} until then)."""
    d = destination(did)
    if not d or d["type"] == "feed":
        raise HTTPException(404)
    g = dest_google(d)
    url = google_calendar_url(g.info().get("email", ""))
    if not check:
        return page(request, "gopen.html", {"name": d["name"], "fallback": url})
    cal = g.cal_info(did)
    busy = google_job.running or google_job.wake.is_set()
    if busy or (g.connected and cal.get("calendar_id") and not cal.get("last_sync") and not g.info().get("last_error")):
        return {}
    g._update_cal(did, shown=True)
    return {"url": url}
_invite_states: dict[str, str] = {}      # Google sign-in state -> invite token, while the invited person signs in


def _invite(token: str) -> dict:
    v = _invites().get(token) if re.fullmatch(r"[A-Za-z0-9_-]{20,64}", token or "") else None
    d = destination(v["did"]) if v else None
    if not v or not d or d["type"] != "google" or d["account"] != v["account"]:
        raise HTTPException(404, "This invite has been used, has expired, or was withdrawn. Ask for a new one.")
    return {**v, "dest": d}


def _invite_form_token(token: str) -> str:
    return hmac.new(_session_key(), b"invite\0" + token.encode(), hashlib.sha256).hexdigest()[:32]


@app.post("/google/invite", dependencies=[Depends(gui_auth)])
async def google_invite(request: Request, csrf: str = Form(""), did: str = Form(""), action: str = Form("make")):
    """Invite someone (a Google module): make its one-time link, or withdraw it (`action=withdraw`)."""
    check_csrf(csrf)
    d = _did(did)
    if d["type"] != "google":
        raise HTTPException(400, "Only a Google module can invite someone.")
    if not core.api_on():
        raise HTTPException(400, "Needs Google Calendar API Sync, which your admin turns on in ☰ Settings.")
    if action == "withdraw":
        forget_invites(did)
        state.record("info", f"Google, {d['name']}: invite withdrawn", kind="Google")
    else:
        if not d["account"]:       # a module from before beta.17 on the shared account: it gets its own now
            d["account"] = "a" + secrets.token_hex(3)
            save_destinations([d if x["id"] == did else x for x in destinations()])
        make_invite(d)
    return RedirectResponse(f"/#dest-{did}", status_code=303)


@app.get("/invite/{token}")
def invite_page(request: Request, token: str):
    """The page an invited person opens: what they're invited to, and Continue with Google."""
    try:
        inv = _invite(token)
    except HTTPException as e:
        return page(request, "invite.html", {"error": e.detail, "token": "", "name": "", "form": ""}, status_code=404)
    return page(request, "invite.html", {"error": "", "token": token, "name": inv["dest"]["name"],
                                         "form": _invite_form_token(token), "done": False})


@app.post("/invite/{token}")
def invite_go(request: Request, token: str, form: str = Form("")):
    """Continue with Google: Google's sign-in page, for this module's account only."""
    inv = _invite(token)
    if not secrets.compare_digest(form.encode(), _invite_form_token(token).encode()):
        raise HTTPException(400, "This page has expired. Open the invite link again.")
    view = google_view(request)
    if not core.api_on() or not view["redirect_ok"]:
        raise HTTPException(400, "CalendarStream can't sign anyone in to Google right now. Let the person who invited you know.")
    g = google_for(inv["account"])
    url = g.sign_in_url(view["redirect_uri"])
    state_ = parse_qs(urlparse(url).query).get("state", [""])[0]
    while len(_invite_states) >= 50:          # (kept small: each Continue adds one until Google sends them back)
        _invite_states.pop(next(iter(_invite_states)))
    _invite_states[state_] = token
    return RedirectResponse(url, status_code=303)


async def _invite_finish(request: Request, token: str, state_: str, code: str, error: str):
    """An invited person is back from Google: their account is signed in for the module, its calendar is
    made in their Google Calendar, and the invite is used up."""
    try:
        inv = _invite(token)
    except HTTPException as e:
        return page(request, "invite.html", {"error": e.detail, "token": "", "name": "", "form": ""}, status_code=404)
    d, g = inv["dest"], google_for(inv["account"])
    try:
        if error or not code:
            raise GoogleError("Google sign-in was cancelled. Open the invite link again to try once more.")
        async with google_job.lock:
            info = await g.finish_sign_in(state_, code)
            await g.ensure_calendar(d["id"], d["name"], _remembered_calendar(d["id"]))
            _remember_calendar(d["id"], g)
        forget_invites(d["id"])
        state.record("info", f"Google, {d['name']}: {info.get('email') or 'the invited account'} connected through an invite", kind="Google")
        request_google_sync(full=True)
    except GoogleError as e:
        return page(request, "invite.html", {"error": str(e), "token": token, "name": d["name"], "form": _invite_form_token(token)}, status_code=400)
    return page(request, "invite.html", {"error": "", "token": "", "name": d["name"], "form": "", "done": True})
