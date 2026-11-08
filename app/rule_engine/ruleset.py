"""Holds: Ruleset application and companion event construction.
Depends on: app/calendars/event.py, app/links.py, app/rule_engine/matching.py, app/rules_words.py.
Used by: app/rules.py.
Reads/writes: no database, network or files; operates on supplied values.
Dart note: rule domain functions and models; preserve ordered matching and regex time limits.
"""

from __future__ import annotations
from ..calendars.event import Event
from ..rules_words import TEXT_FIELDS
from zoneinfo import ZoneInfo
from datetime import date
from datetime import datetime
from datetime import time as dtime
from dataclasses import replace
from ..links import shifted
from datetime import timedelta
from .matching import _compile, event_info


class Ruleset:
    """A calendar's rules, ready to apply to its events (highest priority first)."""

    def __init__(
        self,
        rules: list[dict],
        tz: ZoneInfo,
        templates: dict[str, dict] | None = None,
        no_end: tuple[str, float] = ("hours", 1.0),
    ):
        self.tz = tz
        self.templates = templates or {}
        self.no_end = (
            no_end  # what an event with no end time gets when no rule changes it
        )
        # (0.2.8-beta.27, F3) a link rule follows one event and is never matched here: app/links.py works it out
        self.rules = [(r, _compile(r["conds"])) for r in rules if not r.get("link")]

    def _first_where(self, wanted, e: Event, info: dict):
        for r, test in self.rules:
            for a in r["actions"]:
                if wanted(a) and test(e, info):
                    return a
        return None

    def _first(self, kind: str, e: Event, info: dict):
        return self._first_where(lambda a: a["type"] == kind, e, info)

    def _all_where(self, wanted, e: Event, info: dict) -> list[dict]:
        """Every action `wanted` accepts, of the highest matching rule that has one."""
        for r, test in self.rules:
            found = [a for a in r["actions"] if wanted(a)]
            if found and test(e, info):
                return found
        return []

    def _all_of_first(self, kind: str, e: Event, info: dict) -> list[dict]:
        """Every `kind` action of the highest matching rule that has one (a rule can add two emojis)."""
        return self._all_where(lambda a: a["type"] == kind, e, info)

    def change_times(self, events: list[Event]) -> list[Event]:
        """The time changes (before any edit): the first matching "Change" rule for each event, then the first
        matching "Move this event" (F4); an event with no end time that no rule changes gets the default
        (DEFAULT_EVENT_TYPE / _HOURS)."""
        out = []
        for e in events:
            info = event_info(e, self.tz)
            a = self._first_where(
                lambda x: x["type"] == "change" and x["to"] in ("allday", "length"),
                e,
                info,
            )
            if a is None and e.no_end:
                a = (
                    {"to": "allday"}
                    if self.no_end[0] == "allday"
                    else {"to": "length", "minutes": round(self.no_end[1] * 60)}
                )
            ev = self._changed(e, a) if a else e
            m = self._first("move", e, info)
            if m and m["minutes"]:
                start, end = shifted(ev.start, ev.end, timedelta(minutes=m["minutes"]))
                ev = replace(ev, start=start, end=end, ruled=True)
            out.append(ev)
        return out

    def _changed(self, e: Event, a: dict) -> Event:
        if e.all_day:
            return e
        s, t = datetime.fromisoformat(e.start).astimezone(
            self.tz
        ), datetime.fromisoformat(e.end).astimezone(self.tz)
        if a["to"] == "length":
            return replace(
                e,
                end=(s + timedelta(minutes=a["minutes"])).isoformat(),
                no_end=False,
                ruled=True,
            )
        # all-day, on the day(s) it covers (a whole number of days when it's about that long)
        days = max(1, round((t - s) / timedelta(days=1)))
        note = (
            f"Start: {s:%H:%M}"
            if e.no_end
            else f"Original time: {s:%a %b %d %H:%M} – {t:%a %b %d %H:%M}"
        )
        return replace(
            e,
            start=s.date().isoformat(),
            end=(s.date() + timedelta(days=days)).isoformat(),
            all_day=True,
            description=f"{note}\n{e.description}".strip()[:2000],
            no_end=False,
            ruled=True,
        )

    def finish(self, events: list[Event]) -> list[Event]:
        """After edits: each event's rule color, its text changes and adds (F30), its emoji in front of the title,
        and its deletion (F4). An event edited here keeps its own title, notes and location (a Change leaves
        them); an Add never writes over anything."""
        out = []
        for e in events:
            if e.origin == "rule":
                out.append(e)
                continue
            info = event_info(e, self.tz)
            color = self._first("color", e, info)
            text = {"title": e.title, "notes": e.description, "location": e.location}
            for field in TEXT_FIELDS:
                a = (
                    None
                    if e.edited
                    else self._first_where(
                        lambda x, f=field: x["type"] == "change" and x.get("to") == f,
                        e,
                        info,
                    )
                )
                if a:
                    text[field] = a["text"]
                for a in self._all_where(
                    lambda x, f=field: x["type"] == "add" and x.get("to") == f, e, info
                ):
                    text[field] = (
                        (f"{text[field]}\n{a['text']}" if text[field] else a["text"])
                        if field == "notes"
                        else f"{text[field]} {a['text']}".strip()
                    )
            emoji = " ".join(a["emoji"] for a in self._all_of_first("emoji", e, info))
            title = text["title"]
            if emoji and not title.startswith(emoji):
                title = f"{emoji} {title}"
            ev = replace(
                e,
                title=title,
                description=text["notes"][:4000],
                location=text["location"][:200],
                rule_color=color["color"] if color else "",
            )
            if not e.hidden and not e.deleted and self._first("delete", e, info):
                ev = replace(
                    ev, hidden=True, deleted="rule|"
                )  # left out of the feeds, struck through; the rule says so
            out.append(ev)
        return out

    def made(self, events: list[Event], tz: ZoneInfo) -> list[Event]:
        """The events "Create event" rules add next to matching events."""
        found = {}
        for e in events:
            if e.origin == "rule" or e.hidden:
                continue
            info = event_info(e, self.tz)
            if self._first(
                "delete", e, info
            ):  # an event a rule deletes makes no companions
                continue
            for r, test in self.rules:
                for i, a in enumerate(r["actions"]):
                    if a["type"] != "event" or not test(e, info):
                        continue
                    t = self.templates.get(a["template"]) if a["template"] else a
                    if t:
                        ev = _from_template(
                            e, r["id"] if i == 0 else f"{r['id']}-{i}", a, t, tz
                        )
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
    at = {"before_start": s0 - off, "after_start": s0 + off, "after_end": s1 + off}[
        a["when"]
    ].astimezone(tz)
    if t["all_day"]:
        start, end = at.date().isoformat(), (at.date() + timedelta(days=1)).isoformat()
    else:
        start, end = at.isoformat(), (at + timedelta(minutes=t["minutes"])).isoformat()
    return Event(
        title=t["title"],
        start=start,
        end=end,
        all_day=t["all_day"],
        location=t.get("location", ""),
        description=t.get("description", ""),
        uid=f"{e.uid}#rule-{key}",
        origin="rule",
        color=t.get("color", ""),
        source=e.source,
    )
