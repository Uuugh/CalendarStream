"""Holds: Rule limits, types and constants.
Depends on: no other app files.
Used by: app/rule_engine/conflicts.py, app/rule_engine/matching.py, app/rule_engine/migration.py, app/rule_engine/text_matching.py, app/rule_engine/validation.py, app/rules.py.
  app/rule_engine/text_matching.py, app/rule_engine/validation.py, app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
import re
from datetime import timedelta

COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


ID_RE = re.compile(r"^[a-z0-9]{1,16}$")


SID_RE = re.compile(r"^(ccs|[fl][0-9a-f]{6})$")


MAX_RULES, MAX_CONDS, MAX_ACTIONS, MAX_BRACKETS = 60, 12, 6, 3


MAX_TEXT, MAX_REGEX, MAX_TITLE, MAX_EMOJI = 200, 100, 80, 16


MAX_OFFSET, MAX_LENGTH = 7 * 24 * 60, 52 * 7 * 24 * 60  # minutes


REGEX_TIMEOUT = 0.05


ALLDAY_TOLERANCE = timedelta(minutes=5)  # CCS+ writes whole days as 00:01–23:59:59


ACTION_TYPES = {
    "color": "Color",
    "emoji": "Add emoji to title",
    "event": "Create event",
    "change": "Change",
    "add": "Add",
    "move": "Move this event",
    "delete": "Delete this event",
    "changes": "Record changes in the event notes section",
}


LINK_ACTIONS = ("delete", "move")  # the only Thens of a link rule


MAX_NOTES = 1000  # a Change / Add to Notes


MAX_MOVE = 7 * 24 * 60  # Move this event: up to a week either way


SHADOWED = (
    "color",
    "emoji",
    "change",
    "change:title",
    "change:notes",
    "change:location",
    "add:title",
    "add:notes",
    "add:location",
    "move",
)


MODE_TO_OP = {"word": "word", "contains": "contains", "starts": "begins", "exact": "is"}
