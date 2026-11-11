"""Holds: change.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/runtime/change.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations


class Change:
    """A change that can be undone: what it touches is kept as it was (settings, and the whole of the
    calendars in `whole`), then as it is after; done() writes its History line.

        ch = Change(sids=[sid], whole=[sid]); …change things…; ch.done("Calendar", "Calendar source removed: Work")
    """

    def __init__(
        self,
        sids=(),
        whole=(),
        uids=(),
        *,
        get_SOURCE_BASES,
        get_UNDO_KEYS,
        get_pop_undo,
        get_skey,
        get_state,
        get_store,
    ):
        self._get_SOURCE_BASES = get_SOURCE_BASES
        self._get_UNDO_KEYS = get_UNDO_KEYS
        self._get_pop_undo = get_pop_undo
        self._get_skey = get_skey
        self._get_state = get_state
        self._get_store = get_store
        keys = list(self._get_UNDO_KEYS())
        for sid in dict.fromkeys(
            sids
        ):  # (its settings; `whole` adds its events, without its sign-in)
            keys += [self._get_skey()(sid, b) for b in self._get_SOURCE_BASES()] + (
                ["ccs_login", "calendar_url"] if sid == "ccs" else []
            )
        self.keys, self.whole, self.uids = keys, list(whole), list(uids)
        self.before = self._get_store().snapshot(self.keys, self.whole, self.uids)

    def done(self, kind: str, msg: str) -> int | None:
        after = self._get_store().snapshot(self.keys, self.whole, self.uids)
        entry = self._get_state().record(
            "info",
            msg,
            kind=kind,
            undo={"type": "snapshot", "before": self.before, "after": after},
        )
        self._get_pop_undo()()
        return entry
