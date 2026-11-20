"""Reorder stored items using existing rules ordering semantics.

Holds: _moved.
Depends on: app.rules and FastAPI HTTPException.
Used by: app.main and its route compatibility imports.
Reads/writes: reads caller-supplied items; returns reordered list.
Dart note: Feature-independent list ordering domain helper; inject move strategy during port.
"""
from fastapi import HTTPException
from . import rules as rules_mod

def _moved(items: list[dict], key: str, before: str, after: str) -> list[dict]:
    """`items` with the one whose id is `key` put just above `before` (or just below `after`)."""
    ids = [x["id"] for x in items]
    if key not in ids:
        raise HTTPException(400, "That isn't there (any more).")
    as_rules = rules_mod.move([{"id": x["id"]} for x in items], key, before, after)
    by_id = {x["id"]: x for x in items}
    return [by_id[x["id"]] for x in as_rules]


