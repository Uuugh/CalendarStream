"""Holds: Bound State compatibility constructor.
Depends on: app/services/state.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: no I/O; supplied dependency providers are called by the bound service.
Dart note: application composition; bind constructor dependencies while retaining legacy signatures.
"""

from ..services.state import State as _State


def bind_source_state(
    *,
    get_TZ,
    get_calendar_name,
    get_from_iso,
    get_iso,
    get_log,
    get_log_kind,
    get_skey,
    get_store
):
    class State(_State):
        """Compatibility constructor; dependencies are wired by the app."""

        def __init__(self, sid: str = "ccs"):
            super().__init__(
                sid,
                get_TZ=get_TZ,
                get_calendar_name=get_calendar_name,
                get_from_iso=get_from_iso,
                get_iso=get_iso,
                get_log=get_log,
                get_log_kind=get_log_kind,
                get_skey=get_skey,
                get_store=get_store,
            )

    return State
