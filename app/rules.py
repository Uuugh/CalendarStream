"""Rules (0.2.8): "If <conditions> Then <actions>", applied to a calendar's events.

A rule is one dict, kept in an ordered list (kv "rules"); the order is the priority: for a color, an
emoji or a time change, the highest rule that matches wins. Each rule says which calendars it applies
to ("all", or a list of source IDs). Nothing here touches the database or the web page.

    {"id": "t1a2b3c", "title": "Days off in red",
     "conds": [{"type": "text", "op": "contains", "value": "RDO", "case": False, "open": 1, "close": 0, "join": "and"},
               {"type": "text", "op": "contains", "value": "VAC", "case": False, "open": 0, "close": 1, "join": "or"}, …],
     "actions": [{"type": "color", "color": "#d50000"}, {"type": "emoji", "emoji": "🏝️"}, …],
     "apply": "all" | ["ccs", "f1a2b3c"]}

Conditions are joined to the line before them by "and" or "or" ("and" binds tighter, as usual), and
grouped with brackets: "open" brackets before a line, "close" brackets after it. No conditions: every
event matches.

Condition types (the event's start, in the calendar's time zone):
  text   (title)  is / contains / word (whole word) / begins / ends / regex; "case": match capitals exactly
  date            is / after / before / between ("value", "value2": YYYY-MM-DD)
  time            the same, with HH:MM (never matches an all-day event)
  days            is (any of "days", 0 = Monday … 6 = Sunday) / after / before / between (wrapping round)
  length          is ("minutes"; 0 = no end time) / days (a whole number of days, 24 h, 48 h…)

Action types:
  color    "color" (#rrggbb): the event's color (its own color, chosen on the event page, still wins)
  emoji    "emoji": put in front of the title
  event    add an event: "template" (an event template's ID), or a new one ("title", "minutes",
           "all_day", "location"); "offset" minutes "when" (before_start / after_start / after_end)
  change   the event's time: "to" "allday" (all-day, on the days it covers) or "length" ("minutes")
  changes  record the changes the source makes to it (a note on the event, a line in the log)
"""

from __future__ import annotations

import json
import re
import secrets
from dataclasses import replace
from datetime import date, datetime, timedelta
from datetime import time as dtime
from zoneinfo import ZoneInfo

from .calsync import Event

COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
ID_RE = re.compile(r"^[a-z0-9]{1,16}$")
SID_RE = re.compile(r"^(ccs|[fl][0-9a-f]{6})$")
MAX_RULES, MAX_CONDS, MAX_ACTIONS, MAX_BRACKETS = 60, 12, 6, 3
MAX_TEXT, MAX_REGEX, MAX_TITLE, MAX_EMOJI = 200, 100, 80, 16
MAX_OFFSET, MAX_LENGTH = 7 * 24 * 60, 52 * 7 * 24 * 60      # minutes
ALLDAY_TOLERANCE = timedelta(minutes=5)     # CCS+ writes whole days as 00:01–23:59:59

COND_TYPES = {"text": "Text", "date": "Date", "time": "Time", "days": "Day(s)", "length": "Length"}
OPS = {
    "text": {"is": "is", "contains": "contains", "word": "whole word", "begins": "begins with", "ends": "ends with", "regex": "regex"},
    "date": {"is": "is", "after": "after", "before": "before", "between": "between"},
    "time": {"is": "is", "after": "after", "before": "before", "between": "between"},
    "days": {"is": "is", "after": "after", "before": "before", "between": "between"},
    "length": {"is": "is", "days": "is whole days"},
}
ACTION_TYPES = {"color": "Color", "emoji": "Add emoji to title", "event": "Create event", "change": "Change",
                "changes": "Record changes"}
WHEN = {"before_start": "before the start", "after_start": "after the start", "after_end": "after the end"}
DAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


class RuleError(ValueError):
    """A rule that can't be saved; the message says why."""


# --- Checking -----------------------------------------------------------------------------

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
    out = {"type": kind, "op": op, "open": _int(c.get("open"), 0, MAX_BRACKETS), "close": _int(c.get("close"), 0, MAX_BRACKETS),
           "join": "or" if c.get("join") == "or" else "and"}
    if kind == "text":
        value = str(c.get("value") or "").strip()[:MAX_REGEX if op == "regex" else MAX_TEXT]
        if not value:
            return None
        if op == "regex":
            try:
                re.compile(value)
            except re.error:
                return None
        out.update(value=value, case=bool(c.get("case")))
    elif kind in ("date", "time"):
        norm = _day if kind == "date" else _clock
        value, value2 = norm(c.get("value")), norm(c.get("value2"))
        if not value or (op == "between" and not value2):
            return None
        out.update(value=value, value2=value2 if op == "between" else "")
    elif kind == "days":
        days = list(dict.fromkeys(_int(d, 0, 6) for d in (c.get("days") or []) if str(d).strip().lstrip("-").isdigit()))
        if op != "between":
            days.sort()          # "between" keeps its order: Fri – Mon wraps round the weekend
        if not days or (op == "between" and len(days) != 2) or (op in ("after", "before") and len(days) != 1):
            return None
        out.update(days=days)
    else:   # length
        out.update(minutes=_int(c.get("minutes"), 0, MAX_LENGTH))
        if op == "days" and out["minutes"] < 24 * 60:
            out["minutes"] = 24 * 60
    return out


def _action(a, templates: set[str] | None = None) -> dict | None:
    if not isinstance(a, dict) or a.get("type") not in ACTION_TYPES:
        return None
    kind = a["type"]
    if kind == "color":
        color = str(a.get("color") or "")
        return {"type": kind, "color": color.lower()} if COLOR_RE.match(color) else None
    if kind == "emoji":
        emoji = " ".join(str(a.get("emoji") or "").split())[:MAX_EMOJI]
        return {"type": kind, "emoji": emoji} if emoji and not re.search(r"[<>&\"]", emoji) else None
    if kind == "event":
        tid = str(a.get("template") or "")
        out = {"type": kind, "when": a.get("when") if a.get("when") in WHEN else "before_start",
               "offset": _int(a.get("offset"), 0, MAX_OFFSET)}
        if tid and ID_RE.match(tid) and (templates is None or tid in templates):
            return {**out, "template": tid}
        title = " ".join(str(a.get("title") or "").split())[:200]
        if not title:
            return None
        return {**out, "template": "", "title": title, "all_day": bool(a.get("all_day")),
                "minutes": _int(a.get("minutes"), 5, 24 * 60, 60), "location": str(a.get("location") or "").strip()[:200]}
    if kind == "change":
        if a.get("to") == "allday":
            return {"type": kind, "to": "allday"}
        return {"type": kind, "to": "length", "minutes": _int(a.get("minutes"), 5, 7 * 24 * 60, 60)}
    return {"type": "changes"}


def balanced(conds: list[dict]) -> bool:
    """Whether the brackets pair up."""
    depth = 0
    for c in conds:
        depth += c["open"]
        depth -= c["close"]
        if depth < 0:
            return False
    return depth == 0


def normalize(raw, sids: list[str] | None = None, templates: set[str] | None = None, strict: bool = False) -> dict | None:
    """A rule as saved, checked again on the way out (colors are written into the page's CSS).
    With `strict`, problems raise RuleError (saving); otherwise a broken rule is left out (None)."""
    def bad(msg):
        if strict:
            raise RuleError(msg)
    if not isinstance(raw, dict):
        return bad("Not a rule.")
    rid = str(raw.get("id") or "")
    conds = [c for c in (_cond(c) for c in (raw.get("conds") or [])[:MAX_CONDS]) if c]
    if strict and len(conds) != len([c for c in raw.get("conds") or [] if c]):
        return bad("Fill in every condition (or take the empty ones out).")
    if conds and not balanced(conds):
        if strict:
            return bad("The brackets don't pair up: every ( needs a ) after it.")
        for c in conds:
            c["open"] = c["close"] = 0
    actions = [a for a in (_action(a, templates) for a in (raw.get("actions") or [])[:MAX_ACTIONS]) if a]
    if not actions:
        return bad("Add at least one Then.")
    apply = raw.get("apply")
    if apply != "all":
        apply = [s for s in dict.fromkeys(apply if isinstance(apply, list) else []) if SID_RE.match(str(s))
                 and (sids is None or s in sids)]
    return {"id": rid if ID_RE.match(rid) else "t" + secrets.token_hex(3),
            "title": " ".join(str(raw.get("title") or "").split())[:MAX_TITLE], "conds": conds, "actions": actions,
            "apply": apply}


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


# --- Conflicts (F4.2, 0.2.8-beta.3) ------------------------------------------------------------
# Only the highest matching rule sets an event's color, emoji or time change. A lower rule that matches
# the same events (the same conditions, or a higher rule with none) for some of the same calendars
# never gets to: that's a conflict. Two rules with the same conditions and the same actions are
# duplicates.

SHADOWED = ("color", "emoji", "change")      # the actions only the highest matching rule applies


def _cond_key(c: dict) -> tuple:
    value = c.get("value", "")
    if c["type"] == "text" and not c["case"] and c["op"] != "regex":
        value = value.casefold()
    return (c["type"], c["op"], value, c.get("value2", ""), tuple(c.get("days", ())), c.get("minutes", 0),
            c.get("case", False), c["open"], c["close"], c["join"])


def same_events(a: dict, b: dict) -> bool:
    """Whether rule `a` matches every event `b` does: the same conditions, or none at all."""
    return not a["conds"] or [_cond_key(c) for c in a["conds"]] == [_cond_key(c) for c in b["conds"]]


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
    for i, a in enumerate(rules):
        for b in rules[i + 1:]:
            cals = shared_calendars(a, b, sids)
            if not cals or not same_events(a, b):
                continue
            def acts(r):
                return sorted(json.dumps(x, sort_keys=True) for x in r["actions"])
            if a["conds"] and acts(a) == acts(b):
                hit = [{"kind": "duplicate", "a": a["id"], "b": b["id"], "calendars": cals}]
            else:
                kinds = [k for k in SHADOWED if any(x["type"] == k for x in a["actions"]) and any(x["type"] == k for x in b["actions"])]
                hit = [{"kind": "shadowed", "a": a["id"], "b": b["id"], "action": k, "calendars": cals} for k in kinds]
            found += [h for h in hit if conflict_key(h) not in ignored]
    return found


def merge(a: dict, b: dict) -> dict:
    """Duplicate rules as one: `a`, applying to the calendars of both."""
    if a["apply"] == "all" or b["apply"] == "all":
        return {**a, "apply": "all"}
    return {**a, "apply": list(dict.fromkeys(a["apply"] + b["apply"]))}


# --- From the rules of 0.2.6–0.2.8-beta.1 -------------------------------------------------------

MODE_TO_OP = {"word": "word", "contains": "contains", "starts": "begins", "exact": "is"}


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
        apply = "all" if users and len(users) == len(sids) else users     # every calendar used it: a shared rule
        text = [{"type": "text", "op": MODE_TO_OP.get(r.get("mode"), "word"), "value": r.get("tag", ""),
                 "case": bool(r.get("case"))}] if r.get("tag") else []
        kind = r.get("type")
        if kind == "color":
            new = {"conds": text, "actions": [{"type": "color", "color": r.get("color")}]}
        elif kind == "event":
            new = {"conds": text, "actions": [{"type": "event", "template": r.get("template"), "when": r.get("when"),
                                               "offset": r.get("offset")}]}
        elif kind == "changes":
            new = {"conds": text, "actions": [{"type": "changes"}]}
        elif kind == "no_end":
            new = {"title": "Items without an end time", "conds": [{"type": "length", "op": "is", "minutes": 0}],
                   "actions": [{"type": "change", "to": "allday"} if r.get("no_end_mode") == "allday"
                               else {"type": "change", "to": "length", "minutes": r.get("minutes", 60)}]}
        elif kind == "allday24":
            if not r.get("allday", True):
                continue            # "keep their times": nothing to do any more
            new = {"title": "24-hour events", "conds": [{"type": "length", "op": "days", "minutes": 1440}],
                   "actions": [{"type": "change", "to": "allday"}]}
        else:
            continue
        rule = normalize({"id": rid, "apply": apply, **new}, sids)
        if rule:
            found.append(rule)
    return found[:MAX_RULES]


def starters(no_end_type: str, no_end_hours: float, allday_24h: bool) -> list[dict]:
    """The rules a new install starts with (from DEFAULT_EVENT_TYPE / DEFAULT_EVENT_HOURS / ALLDAY_24H)."""
    found = [{"id": "t" + secrets.token_hex(3), "title": "Items without an end time", "apply": "all",
              "conds": [{"type": "length", "op": "is", "minutes": 0}],
              "actions": [{"type": "change", "to": "allday"} if no_end_type == "allday"
                          else {"type": "change", "to": "length", "minutes": round(no_end_hours * 60)}]}]
    if allday_24h:
        found.append({"id": "t" + secrets.token_hex(3), "title": "24-hour events", "apply": "all",
                      "conds": [{"type": "length", "op": "days", "minutes": 1440}], "actions": [{"type": "change", "to": "allday"}]})
    return [normalize(r) for r in found]


# --- Matching ---------------------------------------------------------------------------------

def _text_test(c: dict):
    value = c["value"]
    flags = 0 if c["case"] else re.IGNORECASE
    if c["op"] == "regex":
        rx = re.compile(value, flags)
    else:
        v = re.escape(value)
        rx = re.compile({"is": r"^\s*" + v + r"\s*$", "contains": v, "word": r"(?<!\w)" + v + r"(?!\w)",
                         "begins": r"^\s*" + v, "ends": v + r"\s*$"}[c["op"]], flags)
    return lambda e, info: rx.search(info["title"]) is not None


def _range_test(op: str, a, b, wrap: bool = False):
    """`wrap`: a "between" that ends before it starts goes round (times: 22:00 – 06:00 is overnight);
    otherwise its ends are just swapped (dates)."""
    if op == "is":
        return lambda x: x == a
    if op == "after":
        return lambda x: x > a
    if op == "before":
        return lambda x: x < a
    if wrap and a > b:
        return lambda x: x >= a or x <= b
    lo, hi = (a, b) if a <= b else (b, a)
    return lambda x: lo <= x <= hi


def _days_test(c: dict):
    days = c["days"]
    if c["op"] == "is":
        return lambda e, info: info["weekday"] in days
    if c["op"] == "after":
        return lambda e, info: info["weekday"] > days[0]
    if c["op"] == "before":
        return lambda e, info: info["weekday"] < days[0]
    a, b = days[0], days[-1]
    if a <= b:
        return lambda e, info: a <= info["weekday"] <= b
    return lambda e, info: info["weekday"] >= a or info["weekday"] <= b


def _test(c: dict):
    """A function (event, info) -> bool for one condition."""
    kind = c["type"]
    if kind == "text":
        return _text_test(c)
    if kind == "date":
        t = _range_test(c["op"], c["value"], c["value2"])
        return lambda e, info: t(info["day"])
    if kind == "time":
        t = _range_test(c["op"], c["value"], c["value2"], wrap=True)
        return lambda e, info: info["clock"] is not None and t(info["clock"])
    if kind == "days":
        return _days_test(c)
    want = timedelta(minutes=c["minutes"])
    if c["op"] == "days":       # a whole number of days (24 h, 48 h…), within a few minutes
        def whole(e, info):
            if info["length"] is None or e.all_day:
                return False
            days = round(info["length"] / timedelta(days=1))
            return days >= 1 and abs(info["length"] - timedelta(days=days)) <= ALLDAY_TOLERANCE
        return whole
    if c["minutes"] == 0:
        return lambda e, info: not e.all_day and info["length"] == timedelta(0)
    return lambda e, info: info["length"] is not None and abs(info["length"] - want) <= (
        ALLDAY_TOLERANCE if want >= timedelta(hours=1) else timedelta(0))


def _compile(conds: list[dict]):
    """A function (event, info) -> bool for a rule's conditions: brackets first, then "and" before "or"."""
    if not conds:
        return lambda e, info: True
    tokens: list = []
    for i, c in enumerate(conds):
        if i:
            tokens.append(c["join"])
        tokens += ["("] * c["open"] + [_test(c)] + [")"] * c["close"]

    def parse(pos: int):        # or-expression
        terms, pos = parse_and(pos)
        alts = [terms]
        while pos < len(tokens) and tokens[pos] == "or":
            terms, pos = parse_and(pos + 1)
            alts.append(terms)
        return alts, pos

    def parse_and(pos: int):
        factors = []
        node, pos = parse_one(pos)
        factors.append(node)
        while pos < len(tokens) and tokens[pos] == "and":
            node, pos = parse_one(pos + 1)
            factors.append(node)
        return factors, pos

    def parse_one(pos: int):
        if tokens[pos] == "(":
            node, pos = parse(pos + 1)
            return ("group", node), pos + 1      # skip ")"
        return ("test", tokens[pos]), pos + 1

    tree, _ = parse(0)

    def run(alts, e, info) -> bool:
        return any(all(run(n[1], e, info) if n[0] == "group" else n[1](e, info) for n in factors) for factors in alts)
    return lambda e, info: run(tree, e, info)


def event_info(e: Event, tz: ZoneInfo) -> dict:
    """What conditions look at: the title, the start's day, weekday and time, and the length."""
    if e.all_day:
        day = date.fromisoformat(e.start[:10])
        length = date.fromisoformat(e.end[:10]) - day
        return {"title": e.title, "day": day.isoformat(), "weekday": day.weekday(), "clock": None, "length": length}
    s, t = datetime.fromisoformat(e.start).astimezone(tz), datetime.fromisoformat(e.end).astimezone(tz)
    return {"title": e.title, "day": s.date().isoformat(), "weekday": s.weekday(), "clock": f"{s:%H:%M}", "length": t - s}


class Ruleset:
    """A calendar's rules, ready to apply to its events (highest priority first)."""

    def __init__(self, rules: list[dict], tz: ZoneInfo, templates: dict[str, dict] | None = None,
                 no_end: tuple[str, float] = ("hours", 1.0)):
        self.tz = tz
        self.templates = templates or {}
        self.no_end = no_end            # what an event with no end time gets when no rule changes it
        self.rules = [(r, _compile(r["conds"])) for r in rules]

    def _first(self, kind: str, e: Event, info: dict):
        for r, test in self.rules:
            for a in r["actions"]:
                if a["type"] == kind and test(e, info):
                    return a
        return None

    def change_times(self, events: list[Event]) -> list[Event]:
        """The time changes (before any edit): the first matching "Change" rule for each event; an event
        with no end time that no rule changes gets the default (DEFAULT_EVENT_TYPE / _HOURS)."""
        out = []
        for e in events:
            a = self._first("change", e, event_info(e, self.tz))
            if a is None and e.no_end:
                a = {"to": "allday"} if self.no_end[0] == "allday" else {"to": "length", "minutes": round(self.no_end[1] * 60)}
            out.append(self._changed(e, a) if a else e)
        return out

    def _changed(self, e: Event, a: dict) -> Event:
        if e.all_day:
            return e
        s, t = datetime.fromisoformat(e.start).astimezone(self.tz), datetime.fromisoformat(e.end).astimezone(self.tz)
        if a["to"] == "length":
            return replace(e, end=(s + timedelta(minutes=a["minutes"])).isoformat(), no_end=False, ruled=True)
        # all-day, on the day(s) it covers (a whole number of days when it's about that long)
        days = max(1, round((t - s) / timedelta(days=1)))
        note = f"Start: {s:%H:%M}" if e.no_end else f"Original time: {s:%a %b %d %H:%M} – {t:%a %b %d %H:%M}"
        return replace(e, start=s.date().isoformat(), end=(s.date() + timedelta(days=days)).isoformat(), all_day=True,
                       description=f"{note}\n{e.description}".strip()[:2000], no_end=False, ruled=True)

    def finish(self, events: list[Event]) -> list[Event]:
        """After edits: each event's rule color, and its emoji in front of the title."""
        out = []
        for e in events:
            if e.origin == "rule":
                out.append(e)
                continue
            info = event_info(e, self.tz)
            color, emoji = self._first("color", e, info), self._first("emoji", e, info)
            title = e.title
            if emoji and not title.startswith(emoji["emoji"]):
                title = f"{emoji['emoji']} {title}"
            out.append(replace(e, title=title, rule_color=color["color"] if color else ""))
        return out

    def made(self, events: list[Event], tz: ZoneInfo) -> list[Event]:
        """The events "Create event" rules add next to matching events."""
        found = {}
        for e in events:
            if e.origin == "rule" or e.hidden:
                continue
            info = event_info(e, self.tz)
            for r, test in self.rules:
                for i, a in enumerate(r["actions"]):
                    if a["type"] != "event" or not test(e, info):
                        continue
                    t = self.templates.get(a["template"]) if a["template"] else a
                    if t:
                        ev = _from_template(e, r["id"] if i == 0 else f"{r['id']}-{i}", a, t, tz)
                        found[ev.uid] = ev
        return list(found.values())

    def watched(self, e: Event) -> bool:
        """Whether a "Record changes" rule follows this event."""
        return self._first("changes", e, event_info(e, self.tz)) is not None

    @property
    def records_changes(self) -> bool:
        return any(a["type"] == "changes" for r, _ in self.rules for a in r["actions"])


def _from_template(e: Event, key: str, a: dict, t: dict, tz: ZoneInfo) -> Event:
    """The event a "Create event" rule makes next to a matching event `e` (all-day events count from midnight)."""
    if e.all_day:
        s0 = datetime.combine(date.fromisoformat(e.start[:10]), dtime(), tz)
        s1 = datetime.combine(date.fromisoformat(e.end[:10]), dtime(), tz)
    else:
        s0, s1 = datetime.fromisoformat(e.start), datetime.fromisoformat(e.end)
    off = timedelta(minutes=a["offset"])
    at = {"before_start": s0 - off, "after_start": s0 + off, "after_end": s1 + off}[a["when"]].astimezone(tz)
    if t["all_day"]:
        start, end = at.date().isoformat(), (at.date() + timedelta(days=1)).isoformat()
    else:
        start, end = at.isoformat(), (at + timedelta(minutes=t["minutes"])).isoformat()
    return Event(title=t["title"], start=start, end=end, all_day=t["all_day"], location=t.get("location", ""),
                 description=t.get("description", ""), uid=f"{e.uid}#rule-{key}", origin="rule",
                 color=t.get("color", ""), source=e.source)


# --- Words ---------------------------------------------------------------------------------------

def _hm(minutes: int) -> str:
    return f"{minutes // 60}:{minutes % 60:02d}"


def length_text(minutes: int) -> str:
    """e.g. "1 w 2 d 3:30", "0:45", "0" (no end)."""
    if not minutes:
        return "0"
    w, rest = divmod(minutes, 7 * 1440)
    d, rest = divmod(rest, 1440)
    parts = ([f"{w} w"] if w else []) + ([f"{d} d"] if d else []) + ([_hm(rest)] if rest else [])
    return " ".join(parts)


def cond_text(c: dict, tr) -> str:
    """One condition in words, e.g. 'Text contains "RDO"', 'Day(s) is Sat, Sun'."""
    head = f"{tr(COND_TYPES[c['type']])} {tr(OPS[c['type']][c['op']])}"
    if c["type"] == "text":
        return f"{head} “{c['value']}”" + (" Aa" if c["case"] else "")
    if c["type"] in ("date", "time"):
        return f"{head} {c['value']}" + (f" – {c['value2']}" if c["op"] == "between" else "")
    if c["type"] == "days":
        names = [tr(DAY_NAMES[d]) for d in c["days"]]
        return f"{head} " + (" – ".join(names) if c["op"] == "between" else ", ".join(names))
    if c["op"] == "days":
        return tr("Length is whole days")
    return tr("No end time") if not c["minutes"] else f"{head} {length_text(c['minutes'])}"


def action_text(a: dict, tr, color_name, templates: dict[str, dict]) -> str:
    if a["type"] == "color":
        return f"{tr('Color')} ({color_name(a['color'])})"       # the page puts its swatch before the brackets
    if a["type"] == "emoji":
        return f"{a['emoji']} {tr('in front of the title')}"
    if a["type"] == "event":
        t = templates.get(a["template"]) if a["template"] else a
        return (f"{tr('Create')} “{t['title'] if t else '?'}”, "
                + tr("{time} {when}", time=_hm(a["offset"]), when=tr(WHEN[a["when"]])))
    if a["type"] == "change":
        return tr("Change to all-day") if a["to"] == "allday" else tr("Change length to {length}", length=_hm(a["minutes"]))
    return tr("Record changes")


def label(rule: dict, tr, color_name, templates: dict[str, dict]) -> str:
    """A rule in one line: its title, else 'If … → …'."""
    if rule["title"]:
        return rule["title"]
    conds = rule["conds"]
    parts = []
    for i, c in enumerate(conds):
        if i:
            parts.append(tr(c["join"]))
        parts.append("(" * c["open"] + cond_text(c, tr) + ")" * c["close"])
    head = " ".join(parts) if conds else tr("Every event")
    return f"{head} → " + "; ".join(action_text(a, tr, color_name, templates) for a in rule["actions"])
