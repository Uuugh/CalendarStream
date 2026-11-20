"""Holds: Bound Change compatibility constructor.
Depends on: app/services/change.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: no I/O; supplied dependency providers are called by the bound service.
Dart note: application composition; bind constructor dependencies while retaining legacy signatures.
"""

from ..services.change import Change as _Change


def bind_change(
    *, get_SOURCE_BASES, get_UNDO_KEYS, get_pop_undo, get_skey, get_state, get_store
):
    class Change(_Change):
        """Compatibility constructor; dependencies are wired by the app."""

        def __init__(self, sids=(), whole=(), uids=()):
            super().__init__(
                sids,
                whole,
                uids,
                get_SOURCE_BASES=get_SOURCE_BASES,
                get_UNDO_KEYS=get_UNDO_KEYS,
                get_pop_undo=get_pop_undo,
                get_skey=get_skey,
                get_state=get_state,
                get_store=get_store,
            )

    return Change
