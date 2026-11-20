"""Holds: calendar sources.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import secrets
from urllib.parse import urlparse


def skey(sid: str, base: str) -> str:
    """The database key of one of a source's settings."""
    return base if sid == "ccs" else f"{base}:{sid}"


def sources(*, SID_RE, store) -> list[dict]:
    """The calendar sources, in their order on the page (the first is the default calendar):
    [{"id", "type", "url"?}, …]."""
    return [
        x
        for x in (store.get("sources") or [])
        if isinstance(x, dict) and SID_RE.match(str(x.get("id", "")))
    ]


def source(sid: str, *, sources) -> dict | None:
    return next((x for x in sources() if x["id"] == sid), None)


def source_ids(*, sources) -> list[str]:
    return [x["id"] for x in sources()]


def default_sid(*, sources, store) -> str:
    """The default calendar (0.2.8-beta.28, I2): the one kv "default_source" names when it is still a CalendarStream
    calendar, else the first CalendarStream calendar, else the first source. Its place in the list doesn't matter.
    """
    found = sources()
    want = store.get("default_source")
    local = [x["id"] for x in found if x.get("type") == "local"]
    if want in local:
        return want
    return (local or [x["id"] for x in found] or [""])[0]


def migrate_sources(*, google, logins, store):
    """0.2 added sources and destinations. An install from before keeps what it had: CCS+ as its source,
    and the feed (its links may be in use) plus Google Autosync if it was set up. A new install starts empty.
    """
    if store.get("sources") is not None:
        return
    had = (
        logins.ccs_configured
        or store.get_calendar("source") is not None
        or store.event_count() > 0
    )
    store.set("sources", [{"id": "ccs", "type": "ccs"}] if had else [])
    store.set(
        "destinations",
        (["feed"] if had else []) + (["google"] if google.configured else []),
    )


def calendar_url(*, settings, store) -> str:
    """The CCS+ Calendar Sync link."""
    return store.get("calendar_url") or settings.calendar_url


def source_url(sid: str, *, calendar_url, source) -> str:
    return calendar_url() if sid == "ccs" else str((source(sid) or {}).get("url", ""))


def calendar_name(sid: str, *, settings, skey, source_url, store) -> str:
    """A source's name, set on the status page; for CCS+ else CALENDAR_NAME from .env."""
    saved = store.get(skey(sid, "calendar_name"))
    if saved:
        return saved
    if sid == "ccs":
        return settings.calendar_name
    return urlparse(source_url(sid)).hostname or "Calendar"


def calendar_color(sid: str, *, COLOR_RE, skey, store) -> str:
    """A source's color (#rrggbb), or "" for none. Validated again on the way out because it is
    written into the page's CSS."""
    color = store.get(skey(sid, "calendar_color")) or ""
    return color.lower() if COLOR_RE.match(color) else ""


def first_named_calendar(*, calendar_name, sources) -> str:
    """A new feed's name when none is given: the first calendar that comes from somewhere (not a Local
    one, which would name every feed "Local")."""
    named = [x["id"] for x in sources() if x.get("type") != "local"]
    return calendar_name(named[0]) if named else "CalendarStream"


def ensure_local(*, destinations, new_local, save_destinations, sources, store):
    """There's always a CalendarStream (local) calendar, and the default calendar (the one events added here go to) is
    always one (0.2.8-beta.15; since 0.2.8-beta.28 it needn't be on top: kv "default_source"). A missing one is made, in
    every feed; an old install's top CalendarStream calendar becomes the default once.
    """
    found = sources()
    locals_ = [x for x in found if x.get("type") == "local"]
    if not locals_:
        sid = new_local()
        store.set("sources", [{"id": sid, "type": "local"}] + found)
        store.set(
            f"calendar_name:{sid}",
            "CalendarStream" if store.get("local_made") else "Local",
        )
        save_destinations(
            [{**d, "sources": [sid] + d["sources"]} for d in destinations()]
        )
        store.set("local_made", True)
        store.set("default_source", sid)
    elif store.get("default_source") not in [x["id"] for x in locals_]:
        store.set("default_source", locals_[0]["id"])


def is_local(sid: str, *, source) -> bool:
    return (source(sid) or {}).get("type") == "local"


def last_local(sid: str, *, is_local, sources) -> bool:
    """The only CalendarStream calendar left: it can be emptied, not removed."""
    return is_local(sid) and sum(1 for x in sources() if x.get("type") == "local") == 1


def new_local(*, source_ids) -> str:
    taken = set(source_ids())
    while (sid := "l" + secrets.token_hex(3)) in taken:
        pass
    return sid
