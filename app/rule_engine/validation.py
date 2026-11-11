"""Holds: Rule normalization, validation and ordering.
Depends on: app/rule_engine/rule_error.py, app/rule_engine/schema.py, app/rule_engine/text_matching.py, app/rules_words.py.
  app/rules_words.py.
Used by: app/rule_engine/migration.py, app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
from .schema import (
    ACTION_TYPES,
    COLOR_RE,
    ID_RE,
    LINK_ACTIONS,
    MAX_ACTIONS,
    MAX_BRACKETS,
    MAX_CONDS,
    MAX_EMOJI,
    MAX_LENGTH,
    MAX_MOVE,
    MAX_NOTES,
    MAX_OFFSET,
    MAX_REGEX,
    MAX_RULES,
    MAX_TEXT,
    MAX_TITLE,
    SID_RE,
)
from ..rules_words import COND_TYPES
from ..rules_words import OPS
from ..rules_words import TEXT_FIELDS
from ..rules_words import TEXT_KINDS
from ..rules_words import WHEN
from datetime import date
import re
import secrets
from .rule_error import RuleError
from .text_matching import pattern_error


def _int(value, lo: int, hi: int, default: int = 0) -> int:
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default


def _day(value) -> str:
    try:
        return date.fromisoformat(str(value or "")).isoformat()
    except ValueError:
        return ""


def _clock(value) -> str:
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", str(value or "").strip())
    return f"{int(m[1]):02d}:{m[2]}" if m and int(m[1]) < 24 and int(m[2]) < 60 else ""


def _cond(c) -> dict | None:
    """One condition as saved, checked; None when it's incomplete."""
    if not isinstance(c, dict) or c.get("type") not in COND_TYPES:
        return None
    kind = c["type"]
    op = c.get("op") if c.get("op") in OPS[kind] else next(iter(OPS[kind]))
    out = {
        "type": kind,
        "op": op,
        "open": _int(c.get("open"), 0, MAX_BRACKETS),
        "close": _int(c.get("close"), 0, MAX_BRACKETS),
        "join": "or" if c.get("join") == "or" else "and",
    }
    if kind in TEXT_KINDS:
        value = str(c.get("value") or "").strip()[
            : MAX_REGEX if op in ("regex", "pattern") else MAX_TEXT
        ]
        if not value or pattern_error(value, op):
            return None
        out.update(value=value, case=bool(c.get("case")))
    elif kind in ("date", "time"):
        norm = _day if kind == "date" else _clock
        value, value2 = norm(c.get("value")), norm(c.get("value2"))
        if not value or (op == "between" and not value2):
            return None
        out.update(value=value, value2=value2 if op == "between" else "")
    elif kind == "days":
        days = list(
            dict.fromkeys(
                _int(d, 0, 6)
                for d in (c.get("days") or [])
                if str(d).strip().lstrip("-").isdigit()
            )
        )
        if op != "between":
            days.sort()  # "between" keeps its order: Fri – Mon wraps round the weekend
        if (
            not days
            or (op == "between" and len(days) != 2)
            or (op in ("after", "before") and len(days) != 1)
        ):
            return None
        out.update(days=days)
    else:  # length
        out.update(minutes=_int(c.get("minutes"), 0, MAX_LENGTH))
        if op == "days" and out["minutes"] < 24 * 60:
            out["minutes"] = 24 * 60
    return out


def _text(value, field: str, multiline: bool = False) -> str:
    """The text of a Change / Add: Notes keep their lines, the others are one line."""
    if multiline:
        return "\n".join(
            x.rstrip() for x in str(value or "").replace("\r", "").split("\n")
        ).strip()[:MAX_NOTES]
    return " ".join(str(value or "").split())[: MAX_TEXT if field != "title" else 200]


def _action(a, templates: set[str] | None = None, linked: bool = False) -> dict | None:
    if not isinstance(a, dict) or a.get("type") not in ACTION_TYPES:
        return None
    kind = a["type"]
    if linked and kind not in LINK_ACTIONS:
        return None
    if kind == "delete":
        return {"type": kind}
    if kind == "move":
        if a.get("with_link") and linked:
            return {"type": kind, "minutes": 0, "with_link": True}
        minutes = _int(a.get("minutes"), -MAX_MOVE, MAX_MOVE)
        return (
            {"type": kind, "minutes": minutes, "with_link": False}
            if minutes and not linked
            else None
        )
    if kind == "add":
        field = a.get("to") if a.get("to") in TEXT_FIELDS else "title"
        text = _text(a.get("text"), field, field == "notes")
        return {"type": kind, "to": field, "text": text} if text else None
    if kind == "color":
        color = str(a.get("color") or "")
        return {"type": kind, "color": color.lower()} if COLOR_RE.match(color) else None
    if kind == "emoji":
        emoji = " ".join(str(a.get("emoji") or "").split())[:MAX_EMOJI]
        return (
            {"type": kind, "emoji": emoji}
            if emoji and not re.search(r"[<>&\"]", emoji)
            else None
        )
    if kind == "event":
        tid = str(a.get("template") or "")
        out = {
            "type": kind,
            "when": a.get("when") if a.get("when") in WHEN else "before_start",
            "offset": _int(a.get("offset"), 0, MAX_OFFSET),
        }
        if tid and ID_RE.match(tid) and (templates is None or tid in templates):
            return {**out, "template": tid}
        title = " ".join(str(a.get("title") or "").split())[:200]
        if not title:
            return None
        return {
            **out,
            "template": "",
            "title": title,
            "all_day": bool(a.get("all_day")),
            "minutes": _int(a.get("minutes"), 5, 24 * 60, 60),
            "location": str(a.get("location") or "").strip()[:200],
        }
    if kind == "change":
        if a.get("to") == "allday":
            return {"type": kind, "to": "allday"}
        if a.get("to") in TEXT_FIELDS:
            field = a["to"]
            text = _text(a.get("text"), field, field == "notes")
            if (
                not text and field == "title"
            ):  # a title can't be empty (Notes and Location can be emptied)
                return None
            return {"type": kind, "to": field, "text": text}
        return {
            "type": kind,
            "to": "length",
            "minutes": _int(a.get("minutes"), 5, 7 * 24 * 60, 60),
        }
    return {"type": "changes"}


def _link(raw) -> dict | None:
    """A link rule's "link", checked (None: not a link rule)."""
    if not isinstance(raw, dict):
        return None
    uid, to = str(raw.get("uid") or "")[:300], str(raw.get("to") or "")[:300]
    if not uid or not to or uid == to:
        return None
    own, src = str(raw.get("own") or ""), str(raw.get("src") or "")
    return {
        "uid": uid,
        "own": own if SID_RE.match(own) else "",
        "to": to,
        "src": src if SID_RE.match(src) else "",
        "at": str(raw.get("at") or "")[:40],
        "name": " ".join(str(raw.get("name") or "").split())[:200],
    }


def balanced(conds: list[dict]) -> bool:
    """Whether the brackets pair up."""
    depth = 0
    for c in conds:
        depth += c["open"]
        depth -= c["close"]
        if depth < 0:
            return False
    return depth == 0


def normalize(
    raw,
    sids: list[str] | None = None,
    templates: set[str] | None = None,
    strict: bool = False,
) -> dict | None:
    """A rule as saved, checked again on the way out (colors are written into the page's CSS).
    With `strict`, problems raise RuleError (saving); otherwise a broken rule is left out (None).
    """

    def bad(msg):
        if strict:
            raise RuleError(msg)

    if not isinstance(raw, dict):
        return bad("Not a rule.")
    rid = str(raw.get("id") or "")
    for c in (raw.get("conds") or [])[:MAX_CONDS]:
        if isinstance(c, dict) and c.get("type") in TEXT_KINDS:
            err = pattern_error(str(c.get("value") or "").strip(), c.get("op"))
            if err:
                return bad(err)
    # (review #2.2) more than the page offers is refused when saving, never cut off without a word
    if strict and len([c for c in raw.get("conds") or [] if c]) > MAX_CONDS:
        return bad(f"Up to {MAX_CONDS} conditions in a rule.")
    if strict and len([a for a in raw.get("actions") or [] if a]) > MAX_ACTIONS:
        return bad(f"Up to {MAX_ACTIONS} actions in a rule.")
    link = _link(raw.get("link"))
    # a link rule follows one event: no conditions (the page's Link to makes it; the rule dialog only lets its two Thens go)
    conds = (
        []
        if link
        else [c for c in (_cond(c) for c in (raw.get("conds") or [])[:MAX_CONDS]) if c]
    )
    if (
        strict
        and not link
        and len(conds) != len([c for c in raw.get("conds") or [] if c])
    ):
        return bad("Fill in every condition (or take the empty ones out).")
    if conds and not balanced(conds):
        if strict:
            return bad("The brackets don't pair up: every ( needs a ) after it.")
        for c in conds:
            c["open"] = c["close"] = 0
    actions = [
        a
        for a in (
            _action(a, templates, bool(link))
            for a in (raw.get("actions") or [])[:MAX_ACTIONS]
        )
        if a
    ]
    if not actions:
        return bad("Add at least one Then.")
    apply = raw.get("apply")
    if apply != "all":
        apply = [
            s
            for s in dict.fromkeys(apply if isinstance(apply, list) else [])
            if SID_RE.match(str(s)) and (sids is None or s in sids)
        ]
    out = {
        "id": rid if ID_RE.match(rid) else "t" + secrets.token_hex(3),
        "title": " ".join(str(raw.get("title") or "").split())[:MAX_TITLE],
        "conds": conds,
        "actions": actions,
        "apply": apply,
    }
    if link:
        out["link"] = link
    return out


def normalize_all(raw, sids: list[str] | None = None) -> list[dict]:
    found, seen = [], set()
    for r in raw if isinstance(raw, list) else []:
        rule = normalize(r, sids)
        if rule and rule["id"] not in seen:
            seen.add(rule["id"])
            found.append(rule)
    return found[:MAX_RULES]


def applies(rule: dict, sid: str) -> bool:
    return rule["apply"] == "all" or sid in rule["apply"]


def is_local(rule: dict, sid: str) -> bool:
    """A rule for this one calendar only."""
    return rule["apply"] != "all" and rule["apply"] == [sid]


def for_source(rules: list[dict], sid: str) -> list[dict]:
    """The rules a calendar uses, highest priority first."""
    return [r for r in rules if applies(r, sid)]


def insert_position(rules: list[dict], rule: dict) -> int:
    """Where a new rule goes: one for a single calendar above the first shared rule that calendar
    uses (so a calendar's own rules come first), anything else at the end."""
    if rule["apply"] != "all" and len(rule["apply"]) == 1:
        sid = rule["apply"][0]
        for i, r in enumerate(rules):
            if applies(r, sid) and not is_local(r, sid):
                return i
    return len(rules)


def move(rules: list[dict], rid: str, before: str = "", after: str = "") -> list[dict]:
    """The list with rule `rid` moved just above `before` (or just below `after`)."""
    moving = next((r for r in rules if r["id"] == rid), None)
    if not moving or rid in (before, after):
        return rules
    rest = [r for r in rules if r["id"] != rid]
    ids = [r["id"] for r in rest]
    if before in ids:
        at = ids.index(before)
    elif after in ids:
        at = ids.index(after) + 1
    else:
        return rules
    return rest[:at] + [moving] + rest[at:]
