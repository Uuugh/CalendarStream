"""Holds: RuleError validation exception.
Depends on: no other app files.
Used by: app/rule_engine/validation.py, app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations


class RuleError(ValueError):
    """A rule that can't be saved; the message says why."""
