"""Holds: event templates.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import re


def event_templates(*, EVENT_COLORS, MAX_TEMPLATES, store) -> list[dict]:
    """[{"id", "title", "all_day", "minutes", "location", "description", "color"}, …]"""
    found = []
    for t in store.get("event_templates") or []:
        title = " ".join(str(t.get("title", "")).split())[:200]
        tid = str(t.get("id", ""))
        if not title or not re.fullmatch(r"[a-z0-9]{1,16}", tid):
            continue
        try:
            minutes = max(5, min(24 * 60, int(t.get("minutes") or 60)))
        except (TypeError, ValueError):
            minutes = 60
        color = str(t.get("color") or "").lower()
        found.append(
            {
                "id": tid,
                "title": title,
                "all_day": bool(t.get("all_day")),
                "minutes": minutes,
                "location": str(t.get("location") or "")[:200],
                "description": str(t.get("description") or "")[:2000],
                "color": color if color in EVENT_COLORS else "",
            }
        )
    return found[:MAX_TEMPLATES]
