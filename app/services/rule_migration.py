"""Holds: rule migration.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import re
import secrets


def _v3_rules(
    raw: list, *, COLOR_RE, MAX_TAG_LEN, RULE_WHEN, TAG_MODES, V3_TYPES, rules_mod
) -> list[dict]:
    """Rules as 0.2.6–0.2.8-beta.1 saved them, each with every field."""
    found = []
    for i, t in enumerate(raw if isinstance(raw, list) else []):
        if not isinstance(t, dict):
            continue
        kind = t.get("type") or t.get("action") or "color"
        kind = kind if kind in V3_TYPES else "color"
        tag, color = str(t.get("tag", "")).strip()[:MAX_TAG_LEN], str(
            t.get("color", "")
        )
        if kind in ("color", "event") and (
            not tag or (kind == "color" and not COLOR_RE.match(color))
        ):
            continue
        rid = str(t.get("id") or f"r{i}")
        found.append(
            {
                "id": rid if re.fullmatch(r"[a-z0-9]{1,16}", rid) else f"r{i}",
                "type": kind,
                "tag": tag,
                "color": color.lower() if COLOR_RE.match(color) else "",
                "mode": t.get("mode") if t.get("mode") in TAG_MODES else "word",
                "case": bool(t.get("case")),
                "template": str(t.get("template") or "")[:16],
                "when": t.get("when") if t.get("when") in RULE_WHEN else "before_start",
                "offset": rules_mod._int(t.get("offset"), 0, rules_mod.MAX_OFFSET),
                "no_end_mode": (
                    "allday" if t.get("no_end_mode") == "allday" else "hours"
                ),
                "minutes": rules_mod._int(t.get("minutes"), 5, 24 * 60, 60),
                "allday": bool(t.get("allday", True)),
                "owner": (
                    str(t.get("owner") or "")
                    if re.fullmatch(r"ccs|f[0-9a-f]{6}", str(t.get("owner") or ""))
                    else ""
                ),
            }
        )
    return found


def _v3_add(lib: list[dict], rule: dict, *, _V3_KEYS, _v3_rules) -> str:
    """Add a rule to a 0.2.6 library (unless the same one is there); returns its ID."""
    rule = _v3_rules([rule])[0]
    for r in lib:
        if (
            r["type"] == rule["type"]
            and r["owner"] == rule["owner"]
            and all(r[k] == rule[k] for k in _V3_KEYS[r["type"]])
        ):
            return r["id"]
    rid, taken = rule["id"], {r["id"] for r in lib}
    while rid in taken:
        rid = "t" + secrets.token_hex(3)
    lib.append({**rule, "id": rid})
    return rid


def _migrate_rules_v3(*, _v3_add, _v3_rules, settings, skey, source_ids, store):
    """0.2.6: every rule into the library; a source's own rules (0.2.5 and before), the rule templates it
    ticked and its two built-in settings became the rules it used, in that order."""
    if store.get("rules_v3"):
        return
    lib = _v3_rules(store.get("rule_templates") or [])
    for sid in source_ids():
        own = _v3_rules(store.get(skey(sid, "calendar_tags")) or [])
        subs = [_v3_add(lib, r) for r in own] + [
            x for x in store.get(skey(sid, "rule_subs")) or []
        ]
        saved = store.get(skey(sid, "defaults")) or {}
        try:
            hours = float(saved.get("hours", settings.default_event_hours))
        except (TypeError, ValueError):
            hours = settings.default_event_hours
        subs.append(
            _v3_add(
                lib,
                {
                    "type": "no_end",
                    "id": "t" + secrets.token_hex(3),
                    "no_end_mode": saved.get("mode", settings.default_event_type),
                    "minutes": round(hours * 60),
                },
            )
        )
        subs.append(
            _v3_add(
                lib,
                {
                    "type": "allday24",
                    "id": "t" + secrets.token_hex(3),
                    "allday": saved.get("allday_24h", settings.allday_24h),
                },
            )
        )
        store.set(skey(sid, "rule_subs"), list(dict.fromkeys(subs)))
        store.delete(skey(sid, "calendar_tags"))
        store.delete(skey(sid, "defaults"))
    store.set("rule_templates", lib)
    store.set("rules_v3", True)
