"""Holds: calendar destinations.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import secrets
from datetime import date


def destinations(
    kind: str | None,
    *,
    ACCOUNT_RE,
    COLOR_RE,
    DESTINATION_TYPES,
    DID_RE,
    _iso_day,
    source_ids,
    store,
) -> list[dict]:
    """The destinations (or those of one type), in the order they were added. Sources that were
    removed are left out of their lists."""
    ids = source_ids()
    found = []
    for d in store.get("destinations") or []:
        if (
            not isinstance(d, dict)
            or not DID_RE.match(str(d.get("id", "")))
            or d.get("type") not in DESTINATION_TYPES
        ):
            continue
        if kind and d["type"] != kind:
            continue
        found.append(
            {
                "id": d["id"],
                "type": d["type"],
                "name": " ".join(str(d.get("name") or "").split())[:100]
                or "CalendarStream",
                "sources": [x for x in d.get("sources") or [] if x in ids],
                "token": str(d.get("token") or ""),
                "start": _iso_day(d.get("start")),
                "end": _iso_day(d.get("end")),
                # a feed made by + Google Calendar while Google Calendar sync wasn't set up (0.2.8-beta.4)
                "for": (
                    "google" if d["type"] == "feed" and d.get("for") == "google" else ""
                ),
                # 0.2.8-beta.15: a Google module's account ("" = the first one, connected in Settings), whether it's
                # 1-way (written by CalendarStream only; changes made in Google are put back), and its color
                "account": (
                    str(d.get("account") or "")
                    if ACCOUNT_RE.match(str(d.get("account") or ""))
                    else ""
                ),
                "oneway": bool(d.get("oneway")) and d["type"] == "google",
                "color": (
                    str(d.get("color") or "").lower()
                    if COLOR_RE.match(str(d.get("color") or ""))
                    else ""
                ),
                # 0.2.8-beta.17: its note (in the header's (i)), and a Calendar Feed's address (one of ☰ Settings')
                "note": " ".join(str(d.get("note") or "").split())[:300],
                "base": str(d.get("base") or "") if d["type"] == "feed" else "",
                # 0.2.8-beta.28, F25: Off = unavailable to everyone subscribed; the setting is kept
                "off": bool(d.get("off")),
            }
        )
    return found


def _iso_day(value) -> str:
    """A date as YYYY-MM-DD, or "" (no limit)."""
    try:
        return date.fromisoformat(str(value or "")).isoformat()
    except ValueError:
        return ""


def destination(did: str, *, destinations) -> dict | None:
    return next((d for d in destinations() if d["id"] == did), None)


def save_destinations(found: list[dict], *, store):
    store.set(
        "destinations",
        [
            {
                k: d.get(k, "")
                for k in (
                    "id",
                    "type",
                    "name",
                    "sources",
                    "token",
                    "start",
                    "end",
                    "for",
                    "account",
                    "oneway",
                    "color",
                    "note",
                    "base",
                )
            }
            | {"off": bool(d.get("off"))}
            for d in found
        ],
    )


def new_did(*, destinations) -> str:
    taken = {d["id"] for d in destinations()}
    while (did := "d" + secrets.token_hex(3)) in taken:
        pass
    return did


def migrate_destinations(
    *,
    calendar_name,
    destinations,
    google,
    new_did,
    save_destinations,
    settings,
    skey,
    source_ids,
    store,
):
    """0.2.0 kept destinations as two switches ("feed", "google") with a feed link and a Google
    calendar for each source. Each becomes a destination of its own with that one source, keeping
    its stream name (so existing links work) and its Google calendar."""
    raw = store.get("destinations") or []
    if not any(isinstance(d, str) for d in raw):
        return
    ids = source_ids()
    found = [d for d in destinations()]
    if "feed" in raw:
        for sid in ids:
            did = new_did()
            token = (
                settings.feed_token
                if sid == "ccs"
                else (store.get(f"feed_token:{sid}") or secrets.token_urlsafe(24))
            )
            found.append(
                {
                    "id": did,
                    "type": "feed",
                    "name": calendar_name(sid),
                    "sources": [sid],
                    "token": token,
                }
            )
            reads = store.get(skey(sid, "feed_reads"))
            if reads:
                store.set(f"feed_reads:{did}", reads)
            save_destinations(found)
    if "google" in raw:
        keys = [k for k in google.calendar_sids() if k in ids]
        for k in keys:
            did = new_did()
            google.rekey(k, did)
            found.append(
                {
                    "id": did,
                    "type": "google",
                    "name": google.cal_info(did).get("calendar_name")
                    or calendar_name(k),
                    "sources": [k],
                    "token": "",
                }
            )
            save_destinations(found)
        if not keys:  # Autosync was set up but had no calendar yet
            found.append(
                {
                    "id": new_did(),
                    "type": "google",
                    "name": calendar_name(ids[0]) if ids else "CalendarStream",
                    "sources": ids[:1],
                    "token": "",
                }
            )
    save_destinations(found)
