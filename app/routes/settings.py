"""Holds: settings HTTP routes and their private helpers.
Depends on: app/config.py, app/logins.py, app/updates.py. Other collaborators are explicit arguments/providers.
  arguments/providers.
Used by: app/routes/__init__.py.
Reads/writes: HTTP requests and responses; supplied services perform persistence and network operations.
Dart note: settings UI/controller layer with injected application services.
"""

from __future__ import annotations
import base64
from fastapi import Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse, Response
from ..config import normalise_public_url
from ..updates import UpdaterError
from fastapi.responses import JSONResponse
from ..logins import LoginError


def register(
    *,
    EMAIL_RE,
    FieldError,
    GOOGLE_SETTINGS,
    SESSION_COOKIE,
    _count_failure,
    app,
    auto_update,
    check_csrf,
    google,
    gui_auth,
    logins,
    mark_updating,
    public_url,
    renew_csrf,
    state,
    store,
    updater,
    updates,
    get___version__,
    get__client_ip,
):
    """Register this area; return legacy helper exports for the composition layer."""

    @app.post("/update/now", dependencies=[Depends(gui_auth)])
    async def update_now(csrf: str = Form("")):
        """Update now (next to "(vX is available)"): ask the updater container to pull this install's
        image and restart CalendarStream with it. The page then follows along through /api/status:
        still the old version while it downloads, no answer while it restarts, the new version after.
        """
        check_csrf(csrf)
        target = updates.available()
        if not target:
            raise HTTPException(400, "CalendarStream is already up to date.")
        if updater.pinned():
            raise HTTPException(
                400,
                "This install runs an exact version (IMAGE_TAG); choose latest or beta with the installer to update from here.",
            )
        try:
            await updater.update()
        except UpdaterError as e:
            state.record("warn", f"Update to CalendarStream {target} not started: {e}")
            raise HTTPException(502, str(e))
        mark_updating(target)
        state.record(
            "info", f"Updating to CalendarStream {target}: downloading, then restarting"
        )
        return {"ok": True, "from": get___version__(), "to": target}

    @app.post("/settings/updates", dependencies=[Depends(gui_auth)])
    async def update_settings(
        csrf: str = Form(""),
        frequency: str = Form(""),
        action: str = Form("save"),
        auto: str = Form(""),
        autoform: str = Form(""),
    ):
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
            state.record(
                "info",
                "Auto-update "
                + (
                    "on: newer versions are installed by themselves"
                    if auto == "1"
                    else "off"
                ),
            )
        if action == "check":
            await updates.check()
        return RedirectResponse("/?menu=settings#updates", status_code=303)

    # --- Public address (Settings) ---------------------------------------------------

    @app.post("/settings/public-url", dependencies=[Depends(gui_auth)])
    async def set_public_url(
        csrf: str = Form(""), url: str = Form(""), action: str = Form("save")
    ):
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
                raise HTTPException(
                    400,
                    "Enter the address people use to reach this page, e.g. https://cal.example.com",
                )
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
            raise FieldError(
                "Enter the address people use to reach this page, e.g. https://cal.example.com",
                *bad,
            )
        found = [x for x in dict.fromkeys(found) if x != public_url()]
        store.set("public_urls_extra", found)
        state.record(
            "info",
            "More public addresses: " + (", ".join(found) or "none"),
            kind="Settings",
        )
        return RedirectResponse(
            GOOGLE_SETTINGS.replace("#googlesync", "#public"), status_code=303
        )

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

    @app.post("/settings/administrator", dependencies=[Depends(gui_auth)])
    async def set_administrator(request: Request, csrf: str = Form("")):
        """☰ Settings › Administrator (0.2.8-beta.29, F32): the public address, the more addresses and the status-page
        login in one Cancel | Save. The addresses are applied first; a changed user name or password needs the
        current password, and ends every session (this browser is sent to the sign-in page).
        """
        check_csrf(csrf)
        form = await request.form()
        user, password = str(form.get("user", "")).strip(), str(
            form.get("password", "")
        )
        current, confirm = str(form.get("current", "")), str(form.get("confirm", ""))
        login_changed = bool(password) or (user not in ("", logins.page_user))
        if login_changed and not logins.check_page_login(logins.page_user, current):
            _count_failure(get__client_ip()(request))
            raise FieldError("The current password isn't right.", "current")
        main = str(form.get("main", "")).strip()
        found, bad = [], []
        for i, url in enumerate(form.getlist("url")):
            url = str(url).strip()
            if not url:
                continue
            try:
                found.append(normalise_public_url(url))
            except ValueError:
                bad.append(f"url{i}")
        try:
            value = normalise_public_url(main) if main else ""
        except ValueError:
            value = None
        if value is None or bad:
            raise FieldError(
                "Enter the address people use to reach this page, e.g. https://cal.example.com",
                *(["main"] if value is None else []),
                *bad,
            )
        if login_changed:
            try:
                logins.set_page_login(
                    user or logins.page_user,
                    password or current,
                    confirm if password else None,
                    strict=bool(password),
                )
            except LoginError as e:
                raise HTTPException(400, str(e))
        # (0.2.8-beta.33, F56) a changed (or newly set) main address breaks Google's redirect URI match, which Google
        # sign-in uses: prompt to fix it, since it always becomes unhealthy otherwise.
        domain_changed = bool(value) and value != (public_url() or "")
        if value != (public_url() or ""):
            if value:
                store.set("public_url", value)
                state.record("info", f"Public address set to {value}")
            else:
                store.delete("public_url")
                state.record("info", "Public address removed")
        found = [x for x in dict.fromkeys(found) if x != public_url()]
        store.set("public_urls_extra", found)
        if login_changed:
            renew_csrf()
            state.record(
                "info", f'Status-page login changed (user "{logins.page_user}")'
            )
            back = JSONResponse({"redirect": "/login"})
            back.delete_cookie(SESSION_COOKIE)
            return back
        if domain_changed and google.configured:
            return RedirectResponse(
                GOOGLE_SETTINGS.replace("?menu=settings", "?menu=settings&fixapi=1"),
                status_code=303,
            )
        return RedirectResponse(
            GOOGLE_SETTINGS.replace("#googlesync", "#public"), status_code=303
        )

    # --- Look: logo, favicon, animation (0.2.8-beta.29, F14) --------------------------------

    BRAND_MAX = 256 * 1024

    def _image_kind(data: bytes) -> str:
        """The media type of an uploaded picture, by what it is (not by its name); '' if it isn't one we take."""
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return "image/png"
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            return "image/webp"
        if data[:4] == b"\x00\x00\x01\x00":
            return "image/x-icon"
        if data[:3] == b"\xff\xd8\xff":
            return "image/jpeg"
        head = data[:600].lstrip().lower()
        if (
            (head.startswith(b"<svg") or head.startswith(b"<?xml"))
            and b"<svg" in data[:2000].lower()
            and b"<script" not in data.lower()
            and b"onload" not in data.lower()
        ):
            return "image/svg+xml"
        return ""

    @app.get("/brand/{kind}")
    def brand_image(kind: str):
        """The uploaded logo or favicon. Public (the sign-in page shows the favicon); sandboxed so a picture never runs anything."""
        saved = (
            (store.get("brand") or {}).get(kind)
            if kind in ("logo", "favicon")
            else None
        )
        if not saved:
            raise HTTPException(404, "No such picture.")
        return Response(
            base64.b64decode(saved["b64"]),
            media_type=saved["mime"],
            headers={
                "Cache-Control": "private, max-age=86400",
                "Content-Security-Policy": "sandbox; default-src 'none'; style-src 'unsafe-inline'",
                "X-Content-Type-Options": "nosniff",
            },
        )

    @app.post("/settings/look", dependencies=[Depends(gui_auth)])
    async def set_look(request: Request, csrf: str = Form("")):
        """☰ Settings › Look: upload a logo and/or a favicon (or go back to CalendarStream's own), and set the buttons'
        Animation intensity and duration (Reset puts both back to 100 %)."""
        check_csrf(csrf)
        form = await request.form()
        saved = dict(store.get("brand") or {})
        for kind in ("logo", "favicon"):
            if form.get(f"remove_{kind}"):
                saved.pop(kind, None)
            up = form.get(kind)
            if isinstance(up, UploadFile) or hasattr(up, "read"):
                data = await up.read()
                if not data:
                    continue
                if len(data) > BRAND_MAX:
                    raise FieldError("That picture is over 256 KB.", kind)
                mime = _image_kind(data)
                if not mime:
                    raise FieldError("Use a PNG, SVG, WebP, JPEG or ICO picture.", kind)
                saved[kind] = {"mime": mime, "b64": base64.b64encode(data).decode()}
        if saved:
            store.set("brand", saved)
        else:
            store.delete("brand")
        grips = form.get("grips")
        if grips in (
            "left",
            "right",
        ):  # (0.2.8-beta.31, F36.1) which side of a module or rule line the reorder grip is on
            if grips == "right":
                store.set("ui_grips", "right")
            else:
                store.delete("ui_grips")
        if form.get("reset"):
            store.delete("ui_anim")
            store.delete("ui_grips")
        else:
            try:
                i, d = int(form.get("intensity", 100)), int(form.get("duration", 100))
            except ValueError:
                raise FieldError(
                    "Intensity and duration are whole percentages.",
                    "intensity",
                    "duration",
                )
            if not (0 <= i <= 200 and 25 <= d <= 300):
                raise FieldError(
                    "Intensity is 0–200 % and duration 25–300 %.",
                    "intensity",
                    "duration",
                )
            store.set("ui_anim", {"i": i, "d": d})
        state.record(
            "info", "Look changed (logo, favicon, grips, animation)", kind="Settings"
        )
        return RedirectResponse("/?menu=settings", status_code=303)

    return {
        "BRAND_MAX": BRAND_MAX,
        "_image_kind": _image_kind,
        "brand_image": brand_image,
        "set_admin_email": set_admin_email,
        "set_administrator": set_administrator,
        "set_look": set_look,
        "set_public_extra": set_public_extra,
        "set_public_url": set_public_url,
        "update_now": update_now,
        "update_settings": update_settings,
    }
