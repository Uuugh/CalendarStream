"""Holds: Text patterns and bounded matching.
Depends on: app/rule_engine/schema.py.
Used by: app/rule_engine/matching.py, app/rule_engine/validation.py, app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
from .schema import REGEX_TIMEOUT
import re
import regex as rxe


def wildcard(value: str) -> str:
    """A simple pattern as a regular expression: * any text, # a digit, ? one character, the rest as typed;
    it must match the whole text ("*E####": anything ending in E and four digits)."""
    out = "".join(
        {"*": ".*", "#": r"\d", "?": "."}.get(ch) or re.escape(ch) for ch in value
    )
    return rf"^\s*{out}\s*$"


def pattern_error(value: str, op: str) -> str:
    """Why a regex can't be used ("" when it can), in words for the page."""
    if op != "regex":
        return ""
    try:
        rxe.compile(value)
    except rxe.error as e:
        where = f" (at character {e.pos + 1})" if e.pos is not None else ""
        return f"Not a valid regex: {e.msg}{where}."
    return ""


def test_text(value: str, op: str, case: bool, samples: list[str]) -> dict:
    """The regex test box (0.2.8-beta.15): which sample texts a Title / Any text condition matches, with the
    matched part of each: {"error": "", "results": [{"text", "match", "span": [start, end]}]}.
    """
    error = pattern_error(value, op)
    if error or not value:
        return {"error": error, "results": []}
    rx = _text_regex({"value": value, "op": op, "case": case})
    results = []
    for text in samples[:30]:
        try:
            m = rx.search(text, timeout=REGEX_TIMEOUT)
        except TimeoutError:
            return {
                "error": "Too slow: this pattern takes too long to check (simplify the repeats, e.g. (a|aa)+).",
                "results": [],
            }
        results.append(
            {
                "text": text,
                "match": m is not None,
                "span": [m.start(), m.end()] if m else [],
            }
        )
    return {"error": "", "results": results}


def _text_regex(c: dict):
    """The condition as a compiled pattern. A typed regex or wildcard pattern uses the `regex` engine, so its
    searches can be given a time limit (REGEX_TIMEOUT); the fixed kinds are escaped text, safe with `re`.
    """
    value = c["value"]
    flags = 0 if c["case"] else re.IGNORECASE
    if c["op"] == "regex":
        return rxe.compile(value, rxe.IGNORECASE if not c["case"] else 0)
    if c["op"] == "pattern":
        return rxe.compile(
            wildcard(value), (0 if c["case"] else rxe.IGNORECASE) | rxe.DOTALL
        )
    v = re.escape(value)
    return re.compile(
        {
            "is": r"^\s*" + v + r"\s*$",
            "contains": v,
            "word": r"(?<!\w)" + v + r"(?!\w)",
            "begins": r"^\s*" + v,
            "ends": v + r"\s*$",
        }[c["op"]],
        flags,
    )


def _text_test(c: dict):
    rx, field = _text_regex(c), "title" if c["type"] == "text" else "text"
    if c["op"] not in ("regex", "pattern"):
        return lambda e, info: rx.search(info[field]) is not None
    slow = (
        []
    )  # set once a search ran out of time: the condition then matches nothing for this run

    def test(e, info):
        if slow:
            return False
        try:
            return rx.search(info[field], timeout=REGEX_TIMEOUT) is not None
        except TimeoutError:
            slow.append(True)
            return False

    return test
