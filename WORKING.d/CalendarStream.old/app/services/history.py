"""Holds: history.
Depends on: app/services/state.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from .state import State as SourceState


def log_kind(msg: str, sid: str) -> str:
    """A line's Type, from its words, for the lines that don't say."""
    m = msg.split(": ", 1)[1] if sid != "ccs" and ": " in msg else msg
    for kind, starts in (
        ("Rule", ("Rule ", "Event templates")),
        (
            "Calendar",
            (
                "Calendar source",
                "Default calendar",
                "Calendar settings",
                "Calendar Sync link",
                "Checks every",
                "Imported",
                "Emptied",
                "Moved ",
            ),
        ),
        ("Feed", ("Destination", "Feed link", "Stream name")),
        (
            "Event",
            (
                'Added "',
                'Updated "',
                'Deleted "',
                'Hid "',
                'Edited "',
                "Reminders for",
                "Reverted",
                'Restored "',
            ),
        ),
        ("Google", ("Google",)),
        (
            "Settings",
            ("Public address", "Admin e", "Status page", "Status-page", "Signed "),
        ),
        ("Update", ("Update", "Updating", "Auto-update", "Auto")),
    ):
        if m.startswith(starts):
            return kind
    return "Sync"


def undo_keep(*, UNDO_KEEP, store) -> int:
    n = store.get("undo_keep")
    return n if isinstance(n, int) and 1 <= n <= 200 else UNDO_KEEP


def pop_undo(*, finish_deletions, store, undo_keep):
    """Drop what's kept for changes beyond the ones remembered (and finish their deletions)."""
    popped = store.trim_undo(undo_keep())
    if popped:
        finish_deletions()


def after_restore(
    *,
    ensure_local,
    rebuild,
    source_ids,
    source_tasks,
    start_source,
    state,
    states,
    stop_source,
    store,
):
    """After an undo or redo: checks started or stopped for calendars that came or went, statuses read
    again, every calendar rebuilt."""
    ensure_local()
    ids = source_ids()
    for sid in list(source_tasks):
        if sid not in ids:
            stop_source(sid)
    for (
        sid
    ) in (
        store.event_sources()
    ):  # a calendar that's gone again (its adding undone): nothing of it is kept
        if sid not in ids:
            store.forget_source(sid)
    for sid in ids:
        states.pop(sid, None) if sid != "ccs" else state.load()
        start_source(sid)
    rebuild()


def st(sid: str, *, State, states) -> SourceState:
    """A source's status (loaded from the database the first time)."""
    if sid not in states:
        states[sid] = State(sid)
        if sid != "ccs":
            states[sid].load()
    return states[sid]
