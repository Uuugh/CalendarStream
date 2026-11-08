"""Linked events (F3.2, 0.2.8-beta.3): an event can follow another one, e.g. a drive to the airport
that follows its trip. "Delete this event": when the other event is gone, this one goes too. "Move this
event": when the other event's start moves, this one moves by as much.

Since 0.2.8-beta.27 (F3) a link is a rule (app/rules.py, "link rule"): the event pop-up's Link to makes it, with
the two Thens in All Rules, each one removable. This module works with the links as {following event's ID:
{"to": the other event's ID, "src": its calendar, "own": the following event's calendar, "at": the other
event's start when last seen, "delete": bool, "move": bool, "rule": the rule's ID}}, read from the rules
(`from_rules`). What to do is worked out here from the other calendar's events; the caller stores the changes
(app/main.py: follow_links).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from .calendars.event import Event


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
    """Links as kept before 0.2.8-beta.27 (kv "event_links"), checked: they become link rules (main.migrate_links)."""
    out = {}
    for uid, link in (raw or {}).items() if isinstance(raw, dict) else ():
        if isinstance(link, dict) and isinstance(link.get("to"), str) and link["to"] != uid:
            out[uid] = {"to": link["to"], "src": str(link.get("src") or ""), "at": str(link.get("at") or ""),
                        "delete": bool(link.get("delete")), "move": bool(link.get("move"))}
    return out


def from_rules(rules: list[dict]) -> dict[str, dict]:
    """The links the link rules make: a rule applies to its event's calendar like any rule (taken off that
    calendar, it follows nothing); "Delete this event" is `delete`, "Move this event with the linked event" `move`."""
    out = {}
    for r in rules:
        link = r.get("link")
        if not link or not (r["apply"] == "all" or not link["own"] or link["own"] in r["apply"]):
            continue
        out[link["uid"]] = {"to": link["to"], "src": link["src"], "own": link["own"], "at": link["at"], "name": link["name"], "rule": r["id"],
                            "delete": any(a["type"] == "delete" for a in r["actions"]),
                            "move": any(a["type"] == "move" and a.get("with_link") for a in r["actions"])}
    return out


def plan(links: dict[str, dict], sid: str, events: list[Event]) -> list[tuple]:
    """What the links to calendar `sid`'s events (as just built) ask for, one tuple per following event:
    ("delete", uid), ("move", uid, timedelta), ("seen", uid, new start, its title) or ("unlink", uid) (the other
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
        if other.start != link["at"] or other.title != link.get("name", ""):
            todo.append(("seen", uid, other.start, other.title))
    return todo
