"""R18/R19 refactor contracts: isolated domain/services, injection and import boundaries.

Uses only made-up events and in-memory collaborators; no app, database or browser.
"""

import ast
import asyncio
import importlib
import logging
from pathlib import Path
import re
import sys
import unittest
from datetime import date, datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import calsync
from app.calendars.defaults import Defaults
from app.calendars.event import Event
from app.calendars.errors import SourceError
from app.calendars import parsing, feed, edits, validation
from app.rule_engine import migration, validation as rule_validation
from app.rule_engine.ruleset import Ruleset
from app.services import (
    calendar_sources,
    event_templates,
    addresses,
    authentication,
    event_links,
)
from app.services.state import State
from app.services.change import Change
from app.services.google_job import GoogleJob


class MemoryStore:
    def __init__(self, values=None):
        self.values = dict(values or {})
        self.logs = []

    def get(self, key):
        return self.values.get(key)

    def set(self, key, value):
        self.values[key] = value

    def add_log(self, *args):
        self.logs.append(args)
        return len(self.logs)


class RefactorContracts(unittest.TestCase):
    def test_isolated_modules_and_headers(self):
        paths = []
        for folder in ("calendars", "rule_engine", "runtime", "services", "routes"):
            paths.extend(sorted((ROOT / "app" / folder).glob("*.py")))
        for path in paths:
            with self.subTest(path=path.name):
                tree = ast.parse(path.read_text())
                doc = ast.get_docstring(tree) or ""
                if path.name != "__init__.py" or path.parent.name != "calendars":
                    for label in (
                        "Holds:",
                        "Depends on:",
                        "Used by:",
                        "Reads/writes:",
                        "Dart note:",
                    ):
                        self.assertIn(label, doc)
                self.assertLessEqual(
                    sum(isinstance(n, ast.ClassDef) for n in tree.body),
                    4 if path.name == "errors.py" else 1,
                )
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        self.assertNotEqual(node.module, "main")
                        self.assertFalse(any(a.name == "main" for a in node.names))
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.assertFalse(
                            any(
                                isinstance(x, (ast.Import, ast.ImportFrom))
                                for x in ast.walk(node)
                            )
                        )
                module = ".".join(path.relative_to(ROOT).with_suffix("").parts)
                importlib.import_module(module)
        self.assertNotIn("app.main", sys.modules)

    def test_calendar_round_trip_and_bad_payload(self):
        raw = b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nBEGIN:VEVENT\r\nUID:made-up\r\nDTSTART:20261030T120000Z\r\nDTEND:20261030T130000Z\r\nSUMMARY:Made up\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
        _, events, _ = parsing.parse(raw, "UTC", Defaults())
        result = feed.build_feed(events, "Demo", "UTC")
        _, restored, _ = parsing.parse(result, "UTC", Defaults())
        self.assertEqual(
            [(e.title, e.start, e.end) for e in restored],
            [(e.title, e.start, e.end) for e in events],
        )
        with self.assertRaises(SourceError):
            validation.check_calendar(b"<html>not a calendar</html>")
        with self.assertRaises(SourceError):
            parsing.parse(b"not an ics", "UTC", Defaults())
        self.assertEqual(edits.apply_changes(events, {}, [], "ccs"), events)

    def test_rules_apply_without_storage(self):
        rules = migration.starters("hours", 2, False)
        normalized = rule_validation.normalize_all(rules, ["ccs"])
        event = Event(
            uid="demo",
            title="No end",
            start="2026-10-30T12:00:00+00:00",
            end="2026-10-30T12:00:00+00:00",
            all_day=False,
            no_end=True,
        )
        changed = Ruleset(normalized, ZoneInfo("UTC")).change_times([event])[0]
        self.assertEqual(changed.end, "2026-10-30T14:00:00+00:00")
        self.assertEqual(event.end, "2026-10-30T12:00:00+00:00")

    def test_default_calendar_priority_and_creation(self):
        store = MemoryStore({"default_source": "l000002"})
        sources = lambda: [
            {"id": "ccs", "type": "ccs"},
            {"id": "l000001", "type": "local"},
            {"id": "l000002", "type": "local"},
        ]
        self.assertEqual(
            calendar_sources.default_sid(sources=sources, store=store), "l000002"
        )
        store.set("default_source", "removed")
        self.assertEqual(
            calendar_sources.default_sid(sources=sources, store=store), "l000001"
        )
        saved = []
        calendar_sources.ensure_local(
            sources=lambda: [],
            new_local=lambda: "l000003",
            destinations=lambda: [{"id": "d000001", "sources": []}],
            save_destinations=saved.extend,
            store=store,
        )
        self.assertEqual(store.get("default_source"), "l000003")
        self.assertEqual(saved[0]["sources"], ["l000003"])

    def test_template_validation_and_public_addresses(self):
        store = MemoryStore(
            {
                "event_templates": [
                    {"id": "bad!", "title": "Ignore"},
                    {"id": "t1", "title": "  Demo  event ", "minutes": 1},
                ],
                "public_urls_extra": ["https://b.example", "https://a.example", None],
            }
        )
        templates = event_templates.event_templates(
            EVENT_COLORS=set(), MAX_TEMPLATES=5, store=store
        )
        self.assertEqual(
            [(t["title"], t["minutes"]) for t in templates], [("Demo event", 5)]
        )
        self.assertEqual(
            addresses.public_addresses(
                public_url=lambda: "https://a.example", store=store
            ),
            ["https://a.example", "https://b.example"],
        )

    def test_state_uses_late_bound_collaborators(self):
        store = MemoryStore()
        current = [store]
        state = State(
            "f000001",
            get_TZ=lambda: ZoneInfo("UTC"),
            get_calendar_name=lambda: lambda sid: "Demo",
            get_log=lambda: logging.getLogger("test"),
            get_log_kind=lambda: lambda msg, sid: "Sync",
            get_skey=lambda: lambda sid, key: key + ":" + sid,
            get_store=lambda: current[0],
            get_iso=lambda: lambda value: value.isoformat() if value else None,
            get_from_iso=lambda: lambda value: (
                datetime.fromisoformat(value) if value else None
            ),
        )
        state.record("info", "first")
        self.assertEqual(store.logs[0][1], "Demo: first")
        replacement = MemoryStore()
        current[0] = replacement
        state.record("info", "second")
        state.status = "ok"
        state.save()
        self.assertEqual(len(store.logs), 1)
        self.assertEqual(replacement.get("status:f000001")["status"], "ok")

    def test_link_guard_and_csrf_rotation(self):
        # A recursive rebuild must stop before touching edits or writing storage.
        event_links.follow_links(
            "ccs",
            [],
            event_links=lambda: {},
            links_mod=SimpleNamespace(plan=lambda *args: [("move", "demo")]),
            get_following=lambda: True,
            set_following=lambda value: self.fail("guard changed"),
            _hide=None,
            rebuild=None,
            set_event_links=None,
            state=None,
            store=None,
            united_original=None,
        )
        first, second = authentication.new_csrf_token(), authentication.new_csrf_token()
        self.assertNotEqual(first, second)
        authentication.check_csrf(first, None, CSRF_TOKEN=first)
        with self.assertRaises(Exception) as error:
            authentication.check_csrf(first, None, CSRF_TOKEN=second)
        self.assertEqual(error.exception.status_code, 400)

    def test_download_cache_override_is_preserved(self):
        with patch.object(calsync, "_curl_version", "fake curl version"):
            self.assertEqual(asyncio.run(calsync.curl_version()), "fake curl version")
            self.assertEqual(calsync._curl_version, "fake curl version")

    def test_job_wakeup_and_change_snapshot(self):
        job = GoogleJob()
        self.assertTrue(job.full)
        self.assertFalse(job.running)
        self.assertFalse(job.wake.is_set())
        from_values = {"value": 1}
        store = SimpleNamespace(snapshot=lambda *args: dict(from_values))
        entries = []
        state = SimpleNamespace(
            record=lambda *args, **kwargs: entries.append(kwargs) or 7
        )
        trimmed = []
        change = Change(
            get_SOURCE_BASES=lambda: (),
            get_UNDO_KEYS=lambda: ("rules",),
            get_pop_undo=lambda: lambda: trimmed.append(True),
            get_skey=lambda: lambda *args: "",
            get_state=lambda: state,
            get_store=lambda: store,
        )
        from_values["value"] = 2
        self.assertEqual(change.done("Rule", "changed"), 7)
        self.assertEqual(entries[0]["undo"]["before"], {"value": 1})
        self.assertEqual(entries[0]["undo"]["after"], {"value": 2})
        self.assertEqual(trimmed, [True])


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RefactorContracts)
    )
    print("ALL PASSED" if result.wasSuccessful() else "FAIL refactor contracts")
    sys.exit(0 if result.wasSuccessful() else 1)
