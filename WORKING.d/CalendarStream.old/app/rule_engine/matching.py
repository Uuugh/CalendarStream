"""Holds: Condition compilation and event facts.
Depends on: app/calendars/event.py, app/rule_engine/schema.py, app/rule_engine/text_matching.py, app/rules_words.py.
  app/rules_words.py.
Used by: app/rule_engine/ruleset.py, app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
from .schema import ALLDAY_TOLERANCE
from ..calendars.event import Event
from ..rules_words import TEXT_KINDS
from zoneinfo import ZoneInfo
from datetime import date
from datetime import datetime
from datetime import timedelta
from .text_matching import _text_test


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
    if kind in TEXT_KINDS:
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
    if c["op"] == "days":  # a whole number of days (24 h, 48 h…), within a few minutes

        def whole(e, info):
            if info["length"] is None or e.all_day:
                return False
            days = round(info["length"] / timedelta(days=1))
            return (
                days >= 1
                and abs(info["length"] - timedelta(days=days)) <= ALLDAY_TOLERANCE
            )

        return whole
    if c["minutes"] == 0:
        return lambda e, info: not e.all_day and info["length"] == timedelta(0)
    return lambda e, info: info["length"] is not None and abs(
        info["length"] - want
    ) <= (ALLDAY_TOLERANCE if want >= timedelta(hours=1) else timedelta(0))


def _compile(conds: list[dict]):
    """A function (event, info) -> bool for a rule's conditions: brackets first, then "and" before "or"."""
    if not conds:
        return lambda e, info: True
    tokens: list = []
    for i, c in enumerate(conds):
        if i:
            tokens.append(c["join"])
        tokens += ["("] * c["open"] + [_test(c)] + [")"] * c["close"]

    def parse(pos: int):  # or-expression
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
            return ("group", node), pos + 1  # skip ")"
        return ("test", tokens[pos]), pos + 1

    tree, _ = parse(0)

    def run(alts, e, info) -> bool:
        return any(
            all(
                run(n[1], e, info) if n[0] == "group" else n[1](e, info)
                for n in factors
            )
            for factors in alts
        )

    return lambda e, info: run(tree, e, info)


def event_info(e: Event, tz: ZoneInfo) -> dict:
    """What conditions look at: the title (and all its text: title, location, notes), the start's day,
    weekday and time, and the length."""
    text = "\n".join(x for x in (e.title, e.location, e.description) if x)
    if e.all_day:
        day = date.fromisoformat(e.start[:10])
        length = date.fromisoformat(e.end[:10]) - day
        return {
            "title": e.title,
            "text": text,
            "day": day.isoformat(),
            "weekday": day.weekday(),
            "clock": None,
            "length": length,
        }
    s, t = datetime.fromisoformat(e.start).astimezone(tz), datetime.fromisoformat(
        e.end
    ).astimezone(tz)
    return {
        "title": e.title,
        "text": text,
        "day": s.date().isoformat(),
        "weekday": s.weekday(),
        "clock": f"{s:%H:%M}",
        "length": t - s,
    }
