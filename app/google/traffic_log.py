"""F59: the Beta traffic view's recorder — the last calls made to Google, for the Developer to watch while
developing a fix. One instance is shared by every Google account (app/main.py), so the view shows all of them
together, in the order they happened.

Holds: TrafficLog, a bounded, in-memory list of TrafficEntry.
Depends on: app/google/traffic_entry.py.
Used by: app/google/api.py (records each call), app/routes/google.py (the Beta traffic view, GET and Clear).
Reads/writes: nothing; a bounded list in memory, cleared on restart and by the Clear button. Never the
database, so a restart or an upgrade loses it, by design (F59: debugging traffic, not a record to keep).

Dart note: a small service class (`TrafficLog`) in the `domain` layer; in Flutter, a `ValueNotifier` or
similar so a widget can show it live instead of this module's polling.
"""
from __future__ import annotations

from collections import deque

from .traffic_entry import TrafficEntry

MAX_ENTRIES = 200   # enough to watch one sync; old ones drop off so memory can't grow without bound


class TrafficLog:
    def __init__(self, maxlen: int = MAX_ENTRIES):
        self._entries: deque[TrafficEntry] = deque(maxlen=maxlen)

    def record(self, entry: TrafficEntry):
        self._entries.append(entry)

    def recent(self) -> list[TrafficEntry]:
        """Newest first."""
        return list(reversed(self._entries))

    def clear(self):
        self._entries.clear()
