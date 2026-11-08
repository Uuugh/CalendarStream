"""Holds: addresses.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from fastapi import Request
from urllib.parse import quote, urlencode


def public_url(*, normalise_public_url, store) -> str:
    """The public address (☰ Settings), or "" (then links use the address the page was opened at).
    Always in normalise_public_url's form."""
    saved = store.get("public_url") or ""
    try:
        return normalise_public_url(saved) if saved else ""
    except ValueError:
        return ""


def import_public_url(*, settings, state, store):
    """PUBLIC_URL used to be set in .env. Copy it into Settings once, so .env no longer needs it
    (an address cleared in Settings later isn't brought back)."""
    if store.get("public_url_imported"):
        return
    if settings.public_base_url and not store.get("public_url"):
        store.set("public_url", settings.public_base_url)
        state.record(
            "info",
            f"Public address {settings.public_base_url} moved from .env to ☰ Settings "
            "(PUBLIC_URL can be deleted from .env)",
        )
    store.set("public_url_imported", True)


def base_url(request: Request, *, public_url) -> str:
    return public_url() or str(request.base_url).rstrip("/")


def public_addresses(*, public_url, store) -> list[str]:
    """Every public address (0.2.8-beta.17, F11): the main one (☰ Settings › Public addresses, first; Google's
    sign-in and notices use it), then any others a feed's link can use instead."""
    extra = [x for x in (store.get("public_urls_extra") or []) if isinstance(x, str)]
    return list(dict.fromkeys([x for x in [public_url(), *extra] if x]))


def feed_url(request: Request, token: str, base: str, *, base_url) -> str:
    return f"{base or base_url(request)}/calendar/{token}.ics"


def subscribe_links(
    request: Request, token: str, base: str, name: str, *, base_url, feed_url
) -> dict:
    base = base or base_url(request)
    feed = feed_url(request, token, base)
    return {
        "feed": feed,
        # Opens Google Calendar's "add this calendar?" prompt. Google expects the feed as webcal://.
        "google": "https://calendar.google.com/calendar/r?cid="
        + quote("webcal://" + feed.split("://", 1)[1], safe=""),
        # webcal:// hands the feed to Apple Calendar (and the phone's own calendar app).
        "webcal": "webcal://" + feed.split("://", 1)[1],
        # Outlook on the web's "Subscribe from web" (0.2.8-beta.17)
        "outlook": "https://outlook.live.com/calendar/0/addfromweb?"
        + urlencode({"url": feed, "name": name or "CalendarStream"}),
        "page": f"{base}/subscribe/{token}",
        "is_public": feed.startswith("https://")
        and not any(h in feed for h in ("localhost", "127.0.0.1", "testserver")),
    }


def google_redirect_uri(request: Request, *, base_url) -> str:
    """Where Google sends the browser back after sign-in. It must be listed exactly like this among
    the OAuth client's authorised redirect URIs in Google Cloud."""
    return f"{base_url(request)}/google/callback"
