"""Holds: settings HTTP routes and their private helpers.
Depends on: app/config.py, app/logins.py, app/updates.py. app/services/page_settings.py, app/services/appearance_settings.py, app/item_order.py. Other collaborators are explicit arguments/providers.
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
from ..item_order import _moved
from ..services.page_settings import settings_order
from ..services.appearance_settings import appearance_values
from ..updates import FREQUENCIES


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

    @app.post("/settings/move", dependencies=[Depends(gui_auth)])
    async def move_setting(
        csrf: str = Form(""),
        id: str = Form(""),
        before: str = Form(""),
        after: str = Form(""),
    ):
        """Persist a Settings module's drag or arrow move using the shared ordering rules."""
        check_csrf(csrf)
        found = [{"id": key} for key in settings_order(store=store)]
        moved = _moved(found, id, before, after)
        if moved != found:
            store.set("ui_settings_order", [item["id"] for item in moved])
        return {"ok": True}

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

    def save_appearance(values):
        brand, grips, animation = values
        if brand:
            store.set("brand", brand)
        else:
            store.delete("brand")
        if grips == "right":
            store.set("ui_grips", grips)
        else:
            store.delete("ui_grips")
        store.set("ui_anim", animation)

    @app.post("/settings/user", dependencies=[Depends(gui_auth)])
    async def set_user_settings(request: Request, csrf: str = Form("")):
        """One normal-mode Save, or an independent Full-mode Login, Updates or Theme Save.

        Validate all preference fields before changing the login (which ends sessions) or preferences.
        Domains are deliberately not part of this form.
        """
        check_csrf(csrf)
        form = await request.form()
        scope = form.get("scope", "user")
        if scope not in ("user", "login", "updates", "look"):
            raise HTTPException(400, "Unknown settings section.")
        appearance = None
        if scope in ("user", "look"):
            appearance = await appearance_values(form, brand=store.get("brand"), image_kind=_image_kind,
                                                  field_error=FieldError, max_bytes=BRAND_MAX)
        frequency = form.get("frequency", "")
        if scope in ("user", "updates") and frequency not in FREQUENCIES:
            raise FieldError("Unknown update frequency.", "frequency")
        login_changed = False
        if scope in ("user", "login"):
            user, password = str(form.get("user", "")).strip(), str(form.get("password", ""))
            current, confirm = str(form.get("current", "")), str(form.get("confirm", ""))
            login_changed = bool(password) or user not in ("", logins.page_user)
            if login_changed:
                if not logins.check_page_login(logins.page_user, current):
                    _count_failure(get__client_ip()(request))
                    raise FieldError("The current password isn't right.", "current")
                try:
                    logins.set_page_login(user or logins.page_user, password or current,
                                          confirm if password else None, strict=bool(password))
                except LoginError as error:
                    raise FieldError(str(error), "user", "password", "confirm")
        if appearance is not None:
            save_appearance(appearance)
        if scope in ("user", "updates"):
            updates.set_frequency(str(frequency))
            store.set("update_auto", form.get("auto") == "1")
        state.record("info", "User settings saved", kind="Settings")
        if login_changed:
            renew_csrf()
            back = JSONResponse({"redirect": "/login"})
            back.delete_cookie(SESSION_COOKIE)
            return back
        return RedirectResponse("/?menu=settings", status_code=303)

    @app.post("/settings/look", dependencies=[Depends(gui_auth)])
    async def set_look(request: Request, csrf: str = Form("")):
        """☰ Settings › Look: upload a logo and/or a favicon (or go back to CalendarStream's own), and set the buttons'
        Animation intensity and duration (Reset puts both back to 100 %)."""
        check_csrf(csrf)
        form = await request.form()
        values = await appearance_values(form, brand=store.get("brand"), image_kind=_image_kind,
                                         field_error=FieldError, max_bytes=BRAND_MAX)
        save_appearance(values)
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
        "set_user_settings": set_user_settings,
        "move_setting": move_setting,
        "set_public_extra": set_public_extra,
        "set_public_url": set_public_url,
        "update_now": update_now,
        "update_settings": update_settings,
    }
