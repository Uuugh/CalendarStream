"""Holds: route helpers.
Depends on: app/calendars/event.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from ..calendars.event import Event
from fastapi import Request
from fastapi import HTTPException


def _sid(sid: str, *, source_ids) -> str:
    """A source ID from a form, which must be one of the sources."""
    if sid not in source_ids():
        raise HTTPException(400, "That calendar source doesn't exist (any more).")
    return sid


def api_on(*, google) -> bool:
    """Google Calendar API Sync is set up (☰ Settings): the Google feed modules can be added and connected."""
    return google.configured and google.client_check().get("ok") is not False


def _did(did: str, *, destination) -> dict:
    d = destination(did)
    if not d:
        raise HTTPException(400, "That destination doesn't exist (any more).")
    return d


async def sent_fields(request: Request, *names: str) -> list[str | None]:
    """Form fields as sent: "" when sent empty (e.g. a note cleared), None when not sent at all. (FastAPI
    reads an empty field as None for `str | None`, which can't tell the two apart.)"""
    form = await request.form()
    return [str(form[n]) if n in form else None for n in names]


def show_duration(minutes: int) -> str:
    return f"{minutes // 60}:{minutes % 60:02d}"


def ignored_conflicts(*, store) -> list[str]:
    return [x for x in store.get("rule_conflicts_ignored") or [] if isinstance(x, str)]


def united_original(uid: str, sid: str, *, Event, preview, skey, store) -> Event | None:
    """The source's own version of an event, from its last download (United's, for CCS+)."""
    found = store.get_calendar(skey(sid, "source"))
    if not found:
        return None
    base, _ = preview(sid, found[0])
    return next((e for e in base if e.uid == uid), None)


def alarm_text(minutes: int, lang: str, *, i18n) -> str:
    """e.g. "at the start", "15 min before", "1 day before"."""
    tr = lambda t, **kw: str(i18n.tr(lang, t, **kw))
    if minutes == 0:
        return tr("at the start")
    for size, one, many in (
        (10080, "1 week before", "{n} weeks before"),
        (1440, "1 day before", "{n} days before"),
        (60, "1 hour before", "{n} hours before"),
    ):
        if minutes % size == 0:
            return tr(one) if minutes == size else tr(many, n=minutes // size)
    return tr("{n} min before", n=minutes)
