"""Linked events (F3.2, 0.2.8-beta.3): an event can follow another one, e.g. a drive to the airport
that follows its trip. "Delete with it": when the other event is gone, this one goes too. "Move with
it": when the other event's start moves, this one moves by as much.

A link is kept by the following event's ID: {"to": the other event's ID, "src": its calendar,
"at": its start when last seen, "delete": bool, "move": bool}. What to do is worked out here from the
other calendar's events; the caller stores the changes (app/main.py: follow_links).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from .calsync import Event


def _when(value: str) -> date | datetime | None:
    try:
        return date.fromisoformat(value) if len(value) == 10 else datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def moved_by(old: str, new: str) -> timedelta | None:
    """How far an event's start moved; None when that can't be told (all-day ↔ timed) or it didn't."""
    a, b = _when(old), _when(new)
    if a is None or b is None or isinstance(a, datetime) != isinstance(b, datetime) or a == b:
        return None
    return b - a


def shifted(start: str, end: str, by: timedelta) -> tuple[str, str]:
    """An event's start and end moved by `by` (an all-day event by whole days)."""
    def one(value: str) -> str:
        when = _when(value)
        if isinstance(when, datetime):
            return (when + by).isoformat()
        return (when + timedelta(days=round(by / timedelta(days=1)))).isoformat()
    return one(start), one(end)


def clean(raw) -> dict[str, dict]:
    """The saved links, checked."""
    out = {}
    for uid, link in (raw or {}).items() if isinstance(raw, dict) else ():
        if isinstance(link, dict) and isinstance(link.get("to"), str) and link["to"] != uid:
            out[uid] = {"to": link["to"], "src": str(link.get("src") or ""), "at": str(link.get("at") or ""),
                        "delete": bool(link.get("delete")), "move": bool(link.get("move"))}
    return out


def plan(links: dict[str, dict], sid: str, events: list[Event]) -> list[tuple]:
    """What the links to calendar `sid`'s events (as just built) ask for, one tuple per following event:
    ("delete", uid), ("move", uid, timedelta), ("seen", uid, new start) or ("unlink", uid) (the other
    event is gone and nothing should follow it)."""
    by_uid = {e.uid: e for e in events if not e.hidden}
    todo = []
    for uid, link in links.items():
        if link["src"] != sid:
            continue
        other = by_uid.get(link["to"])
        if other is None:
            todo.append(("delete", uid) if link["delete"] else ("unlink", uid))
            continue
        by = moved_by(link["at"], other.start) if link["at"] else None
        if by is not None and link["move"]:
            todo.append(("move", uid, by))
        if other.start != link["at"]:
            todo.append(("seen", uid, other.start))
    return todo
