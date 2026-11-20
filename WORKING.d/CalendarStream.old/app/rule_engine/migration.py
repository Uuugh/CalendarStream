"""Holds: Legacy rule conversion and starter rules.
Depends on: app/rule_engine/schema.py, app/rule_engine/validation.py.
Used by: app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
from .schema import MAX_RULES, MODE_TO_OP
import secrets
from .validation import normalize


def from_v3(lib: list[dict], subs: dict[str, list[str]], sids: list[str]) -> list[dict]:
    """The rules of 0.2.6–0.2.8-beta.1 (a library of one-condition rules, and each calendar's list of the
    ones it used, in its order) as rules of this kind, in one priority order: the calendars' orders
    merged (the first calendar's first), then rules no calendar used."""
    order: list[str] = []
    for sid in sids:
        for rid in subs.get(sid, []):
            if rid not in order:
                order.append(rid)
    order += [r["id"] for r in lib if r["id"] not in order]
    by_id = {r["id"]: r for r in lib}
    found = []
    for rid in order:
        r = by_id.get(rid)
        if not r:
            continue
        users = [s for s in sids if rid in subs.get(s, [])]
        if r.get("owner"):
            users = [r["owner"]] if r["owner"] in sids else []
        apply = (
            "all" if users and len(users) == len(sids) else users
        )  # every calendar used it: a shared rule
        text = (
            [
                {
                    "type": "text",
                    "op": MODE_TO_OP.get(r.get("mode"), "word"),
                    "value": r.get("tag", ""),
                    "case": bool(r.get("case")),
                }
            ]
            if r.get("tag")
            else []
        )
        kind = r.get("type")
        if kind == "color":
            new = {
                "conds": text,
                "actions": [{"type": "color", "color": r.get("color")}],
            }
        elif kind == "event":
            new = {
                "conds": text,
                "actions": [
                    {
                        "type": "event",
                        "template": r.get("template"),
                        "when": r.get("when"),
                        "offset": r.get("offset"),
                    }
                ],
            }
        elif kind == "changes":
            new = {"conds": text, "actions": [{"type": "changes"}]}
        elif kind == "no_end":
            new = {
                "title": "Items without an end time",
                "conds": [{"type": "length", "op": "is", "minutes": 0}],
                "actions": [
                    (
                        {"type": "change", "to": "allday"}
                        if r.get("no_end_mode") == "allday"
                        else {
                            "type": "change",
                            "to": "length",
                            "minutes": r.get("minutes", 60),
                        }
                    )
                ],
            }
        elif kind == "allday24":
            if not r.get("allday", True):
                continue  # "keep their times": nothing to do any more
            new = {
                "title": "24-hour events",
                "conds": [{"type": "length", "op": "days", "minutes": 1440}],
                "actions": [{"type": "change", "to": "allday"}],
            }
        else:
            continue
        rule = normalize({"id": rid, "apply": apply, **new}, sids)
        if rule:
            found.append(rule)
    return found[:MAX_RULES]


def starters(no_end_type: str, no_end_hours: float, allday_24h: bool) -> list[dict]:
    """The rules a new install starts with (from DEFAULT_EVENT_TYPE / DEFAULT_EVENT_HOURS / ALLDAY_24H)."""
    found = [
        {
            "id": "t" + secrets.token_hex(3),
            "title": "Items without an end time",
            "apply": "all",
            "conds": [{"type": "length", "op": "is", "minutes": 0}],
            "actions": [
                (
                    {"type": "change", "to": "allday"}
                    if no_end_type == "allday"
                    else {
                        "type": "change",
                        "to": "length",
                        "minutes": round(no_end_hours * 60),
                    }
                )
            ],
        }
    ]
    if allday_24h:
        found.append(
            {
                "id": "t" + secrets.token_hex(3),
                "title": "24-hour events",
                "apply": "all",
                "conds": [{"type": "length", "op": "days", "minutes": 1440}],
                "actions": [{"type": "change", "to": "allday"}],
            }
        )
    return [normalize(r) for r in found]


def ccs_starters(which, sid: str = "ccs") -> list[dict]:
    """The rules a CCS+ calendar added through + comes with (0.2.8-beta.28, F16.1), for that calendar only: "noend" = items
    without an end time last 1:00; "allday24" = 24-hour events become all-day. The Developer can remove either while adding.
    """
    found = []
    if "noend" in which:
        found.append(
            {
                "id": "t" + secrets.token_hex(3),
                "title": "Items without an end time",
                "apply": [sid],
                "conds": [{"type": "length", "op": "is", "minutes": 0}],
                "actions": [{"type": "change", "to": "length", "minutes": 60}],
            }
        )
    if "allday24" in which:
        found.append(
            {
                "id": "t" + secrets.token_hex(3),
                "title": "24-hour events",
                "apply": [sid],
                "conds": [{"type": "length", "op": "days", "minutes": 1440}],
                "actions": [{"type": "change", "to": "allday"}],
            }
        )
    return [normalize(r) for r in found]
