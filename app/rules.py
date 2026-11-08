"""Holds: Compatibility interface for the rule domain.
Depends on: app/calendars/event.py, app/links.py, app/rule_engine/conflicts.py, app/rule_engine/matching.py, app/rule_engine/migration.py, app/rule_engine/rule_error.py, app/rule_engine/ruleset.py, app/rule_engine/schema.py, app/rule_engine/text_matching.py, app/rule_engine/validation.py, app/rules_words.py.
Used by: app/item_order.py, app/main.py, app/routes/events.py, app/routes/page.py, app/routes/rules.py, app/routes/sources.py, app/services/publishing.py, app/services/rule_settings.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from .rule_engine.schema import (
    ACTION_TYPES,
    ALLDAY_TOLERANCE,
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
    MODE_TO_OP,
    REGEX_TIMEOUT,
    SHADOWED,
    SID_RE,
)
from .rules_words import COND_TYPES
from .rules_words import DAY_NAMES
from .calendars.event import Event
from .rules_words import OPS
from .rules_words import TEXT_FIELDS
from .rules_words import TEXT_KINDS
from .rules_words import TEXT_OPS
from .rules_words import WHEN
from zoneinfo import ZoneInfo
from .rules_words import _hm
from .rules_words import action_text
from .rules_words import actions_text
from .rules_words import cond_text
from datetime import date
from datetime import datetime
from datetime import time as dtime
import json
from .rules_words import label
from .rules_words import length_text
import re
from dataclasses import replace
import regex as rxe
import secrets
from .links import shifted
from datetime import timedelta
from .rule_engine.rule_error import RuleError
from .rule_engine.validation import (
    _int,
    _day,
    _clock,
    _cond,
    _text,
    _action,
    _link,
    balanced,
    normalize,
    normalize_all,
    applies,
    is_local,
    for_source,
    insert_position,
    move,
)
from .rule_engine.text_matching import (
    wildcard,
    pattern_error,
    test_text,
    _text_regex,
    _text_test,
)
from .rule_engine.conflicts import (
    shadow_kind,
    _cond_key,
    same_events,
    shared_calendars,
    conflict_key,
    conflicts,
    merge,
)
from .rule_engine.migration import from_v3, starters, ccs_starters
from .rule_engine.matching import _range_test, _days_test, _test, _compile, event_info
from .rule_engine.ruleset import Ruleset, _from_template
