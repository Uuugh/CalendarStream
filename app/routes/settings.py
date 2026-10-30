"""☰ Settings: the public address and more addresses, the administrator's e-mail, updates.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from .. import main as core
from ..main import (app, auto_update, check_csrf, mark_updating, EMAIL_RE, FieldError, GOOGLE_SETTINGS, gui_auth, public_url,
    state, store, updater, updates)
from ..config import normalise_public_url
from ..updates import UpdaterError


@app.post("/update/now", dependencies=[Depends(gui_auth)])
async def update_now(csrf: str = Form("")):
    """Update now (next to "(vX is available)"): ask the updater container to pull this install's
    image and restart CalendarStream with it. The page then follows along through /api/status:
    still the old version while it downloads, no answer while it restarts, the new version after."""
    check_csrf(csrf)
    target = updates.available()
    if not target:
        raise HTTPException(400, "CalendarStream is already up to date.")
    if updater.pinned():
        raise HTTPException(400, "This install runs an exact version (IMAGE_TAG); choose latest or beta with the installer to update from here.")
    try:
        await updater.update()
    except UpdaterError as e:
        state.record("warn", f"Update to CalendarStream {target} not started: {e}")
        raise HTTPException(502, str(e))
    mark_updating(target)
    state.record("info", f"Updating to CalendarStream {target}: downloading, then restarting")
    return {"ok": True, "from": core.__version__, "to": target}


@app.post("/settings/updates", dependencies=[Depends(gui_auth)])
async def update_settings(csrf: str = Form(""), frequency: str = Form(""), action: str = Form("save"),
                          auto: str = Form(""), autoform: str = Form("")):
    """Settings → Check for updates: how often, Auto-update (the form always sends its tick box, with
    `autoform`), or check now."""
    check_csrf(csrf)
    if frequency:
        try:
            updates.set_frequency(frequency)
        except ValueError:
            raise HTTPException(400, "Unknown update frequency.")
    if autoform and (auto == "1") != auto_update():
        store.set("update_auto", auto == "1")
        state.record("info", "Auto-update " + ("on: newer versions are installed by themselves" if auto == "1" else "off"))
    if action == "check":
        await updates.check()
    return RedirectResponse("/?menu=settings#updates", status_code=303)


# --- Public address (Settings) ---------------------------------------------------

@app.post("/settings/public-url", dependencies=[Depends(gui_auth)])
async def set_public_url(csrf: str = Form(""), url: str = Form(""), action: str = Form("save")):
    """Save the public address (Settings menu); empty removes it. It's used for the feed and subscribe
    links and Google's sign-in redirect."""
    check_csrf(csrf)
    if not url.strip():
        store.delete("public_url")
        state.record("info", "Public address removed")
    else:
        try:
            value = normalise_public_url(url)
        except ValueError:
            raise HTTPException(400, "Enter the address people use to reach this page, e.g. https://cal.example.com")
        store.set("public_url", value)
        state.record("info", f"Public address set to {value}")
    return RedirectResponse(GOOGLE_SETTINGS, status_code=303)


@app.post("/settings/public-extra", dependencies=[Depends(gui_auth)])
async def set_public_extra(request: Request, csrf: str = Form("")):
    """☰ Settings › Public addresses (0.2.8-beta.17, F11): more addresses people reach this page at, under the
    main one, each editable, + for another. The main one is for Google's sign-in and notices; a Calendar
    Feed's link can use any of them. An address left empty is taken out."""
    check_csrf(csrf)
    form = await request.form()
    found, bad = [], []
    for i, url in enumerate(form.getlist("url")):
        url = str(url).strip()
        if not url:
            continue
        try:
            found.append(normalise_public_url(url))
        except ValueError:
            bad.append(f"url{i}")
    if bad:
        raise FieldError("Enter the address people use to reach this page, e.g. https://cal.example.com", *bad)
    found = [x for x in dict.fromkeys(found) if x != public_url()]
    store.set("public_urls_extra", found)
    state.record("info", "More public addresses: " + (", ".join(found) or "none"), kind="Settings")
    return RedirectResponse(GOOGLE_SETTINGS.replace("#googlesync", "#public"), status_code=303)


@app.post("/settings/admin-email", dependencies=[Depends(gui_auth)])
async def set_admin_email(csrf: str = Form(""), email: str = Form("")):
    check_csrf(csrf)
    email = email.strip()
    if not email:
        store.delete("admin_email")
        state.record("info", "Admin e-mail removed")
    elif not EMAIL_RE.match(email) or len(email) > 254:
        raise HTTPException(400, "That doesn't look like an e-mail address.")
    else:
        store.set("admin_email", email)
        state.record("info", f"Admin e-mail set to {email}")
    return RedirectResponse("/?menu=settings#admin", status_code=303)
