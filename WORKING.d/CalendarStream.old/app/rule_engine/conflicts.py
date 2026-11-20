"""Holds: Rule conflict detection and merging.
Depends on: app/rule_engine/schema.py, app/rules_words.py.
Used by: app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
from .schema import SHADOWED
from ..rules_words import TEXT_FIELDS
from ..rules_words import TEXT_KINDS
import json


def shadow_kind(a: dict) -> str:
    """Which of the SHADOWED actions `a` is (its type, or "change:<field>" / "add:<field>" for a text field)."""
    if a["type"] in ("change", "add") and a.get("to") in TEXT_FIELDS:
        return f"{a['type']}:{a['to']}"
    return a["type"]


def _cond_key(c: dict) -> tuple:
    value = c.get("value", "")
    if c["type"] in TEXT_KINDS and not c["case"] and c["op"] != "regex":
        value = value.casefold()
    return (
        c["type"],
        c["op"],
        value,
        c.get("value2", ""),
        tuple(c.get("days", ())),
        c.get("minutes", 0),
        c.get("case", False),
        c["open"],
        c["close"],
        c["join"],
    )


def same_events(a: dict, b: dict) -> bool:
    """Whether rule `a` matches every event `b` does: the same conditions, or none at all."""
    return not a["conds"] or [_cond_key(c) for c in a["conds"]] == [
        _cond_key(c) for c in b["conds"]
    ]


def shared_calendars(a: dict, b: dict, sids: list[str]) -> list[str]:
    """The calendars both rules apply to."""

    def cals(r):
        return set(sids) if r["apply"] == "all" else set(r["apply"])

    both = cals(a) & cals(b)
    return [s for s in sids if s in both]


def conflict_key(found: dict) -> str:
    return "|".join((found["kind"], found["a"], found["b"], found.get("action", "")))


def conflicts(rules: list[dict], sids: list[str], ignored=()) -> list[dict]:
    """The conflicts between rules, highest first: {"kind": "duplicate" | "shadowed", "a": the higher
    rule's id, "b": the lower one's, "action": the action b loses (shadowed), "calendars": where}.
    Those in `ignored` (conflict_key) are left out."""
    found = []
    rules = [
        r for r in rules if not r.get("link")
    ]  # a link rule follows one event: it conflicts with nothing
    for i, a in enumerate(rules):
        for b in rules[i + 1 :]:
            cals = shared_calendars(a, b, sids)
            if not cals or not same_events(a, b):
                continue

            def acts(r):
                return sorted(json.dumps(x, sort_keys=True) for x in r["actions"])

            if a["conds"] and acts(a) == acts(b):
                hit = [
                    {"kind": "duplicate", "a": a["id"], "b": b["id"], "calendars": cals}
                ]
            else:
                kinds = [
                    k
                    for k in SHADOWED
                    if any(shadow_kind(x) == k for x in a["actions"])
                    and any(shadow_kind(x) == k for x in b["actions"])
                ]
                hit = [
                    {
                        "kind": "shadowed",
                        "a": a["id"],
                        "b": b["id"],
                        "action": k,
                        "calendars": cals,
                    }
                    for k in kinds
                ]
            found += [h for h in hit if conflict_key(h) not in ignored]
    return found


def merge(a: dict, b: dict) -> dict:
    """Duplicate rules as one: `a`, applying to the calendars of both."""
    if a["apply"] == "all" or b["apply"] == "all":
        return {**a, "apply": "all"}
    return {**a, "apply": list(dict.fromkeys(a["apply"] + b["apply"]))}
