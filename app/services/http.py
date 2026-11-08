"""Holds: http.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from fastapi import HTTPException
from fastapi import Request
from fastapi.exception_handlers import http_exception_handler as default_http_error
from fastapi.responses import JSONResponse, Response


async def protect(request: Request, call_next, *, __version__, app):
    """Refuse form posts sent from other websites (the browser marks them Sec-Fetch-Site: cross-site),
    except Google's change notifications, and add headers that stop other sites framing the pages and
    the pages leaking their address."""
    if (
        request.method == "POST"
        and request.headers.get("sec-fetch-site") == "cross-site"
        and request.url.path != "/google/notify"
    ):
        return Response("Cross-site requests aren't accepted.", status_code=403)
    response = await call_next(request)
    # Only this site may show its pages in a frame (the event and print previews do, 0.2.8)
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Content-Security-Policy", "frame-ancestors 'self'")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    # Caching (0.2.8-beta.4): files whose address names the version (?v=…, /assets/…-<version>-…) never
    # change, so browsers keep them a year; other static files (the fonts) a day, then ask again.
    path = request.url.path
    if path.startswith(("/static/", "/assets/")) and response.status_code == 200:
        versioned = request.query_params.get("v") == __version__ or path.startswith(
            f"/assets/page-{__version__}-"
        )
        response.headers["Cache-Control"] = (
            "public, max-age=31536000, immutable"
            if versioned
            else "public, max-age=86400"
        )
    return response


async def http_error(
    request: Request, exc: HTTPException, *, _is_async, app, i18n, lang_for, page
):
    """Show form errors as a small page in the visitor's language (the API keeps JSON). Sign-in
    prompts (401) and redirects (303) pass through unchanged."""
    if _is_async(request) and exc.status_code not in (303, 401):
        # A login saved from its Save button (see verify): the message, for next to the boxes
        try:
            lang = lang_for(request)
        except Exception:
            lang = "en"
        return JSONResponse(
            {"detail": str(i18n.message(lang, str(exc.detail)))},
            status_code=exc.status_code,
            headers=getattr(exc, "headers", None),
        )  # (X-CS-Fields: the fields to outline)
    wants_page = "text/html" in request.headers.get(
        "accept", ""
    ) and not request.url.path.startswith("/api/")
    if exc.status_code in (303, 401) or not wants_page:
        return await default_http_error(request, exc)
    try:
        lang = lang_for(request)
    except Exception:
        lang = "en"
    return page(
        request,
        "error.html",
        {"detail": exc.detail, "code": exc.status_code},
        status_code=exc.status_code,
        lang=lang,
    )


def _is_async(request: Request) -> bool:
    """A login form saved by the page's script (Save → Saved → Verifying… → ✓ / ✗), not a plain post."""
    return request.headers.get("x-cs-async") == "1"
