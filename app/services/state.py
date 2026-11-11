"""Holds: source state.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/runtime/state.py, app/services/history.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from datetime import datetime
import asyncio
import logging


class State:
    """A source's download status (CCS+ or a feed), saved in the database."""

    def __init__(
        self,
        sid: str = "ccs",
        *,
        get_TZ,
        get_calendar_name,
        get_from_iso,
        get_iso,
        get_log,
        get_log_kind,
        get_skey,
        get_store,
    ):
        self._get_TZ = get_TZ
        self._get_calendar_name = get_calendar_name
        self._get_from_iso = get_from_iso
        self._get_iso = get_iso
        self._get_log = get_log
        self._get_log_kind = get_log_kind
        self._get_skey = get_skey
        self._get_store = get_store
        self.sid = sid
        self.status = "starting"  # ok | auth_failed | blocked | error | paused | running | starting
        self.message = ""
        self.last_attempt: datetime | None = None
        self.last_success: datetime | None = None
        self.last_change: datetime | None = None
        self.last_auth: datetime | None = None
        self.last_auth_ok: bool | None = None
        self.next_run: datetime | None = None
        self.login_failures = 0
        self.event_count = 0
        self.last_detail = (
            ""  # what the last download changed: "3 new, 1 removed", "no changes"…
        )
        self.running = False
        self.wake = asyncio.Event()

    def record(
        self,
        level: str,
        msg: str,
        kind: str = "",
        undo: dict | None = None,
        stack: bool = True,
    ) -> int | None:
        """Add a line to History (a feed source's lines start with its name). `kind` is its Type (worked out
        from the words when not given); `undo` makes it a change that can be undone (0.2.8-beta.15).
        """
        if self.sid != "ccs":
            msg = f"{self._get_calendar_name()(self.sid)}: {msg}"
        self._get_log().log(
            {"warn": logging.WARNING, "error": logging.ERROR}.get(level, logging.INFO),
            msg,
        )
        try:
            return self._get_store().add_log(
                level, msg, kind or self._get_log_kind()(msg, self.sid), undo, stack
            )
        except Exception as e:
            self._get_log().error("Couldn't write activity log to the database: %s", e)
            return None

    _TIMES = ("last_attempt", "last_success", "last_change", "last_auth")
    _SAVED = _TIMES + (
        "status",
        "message",
        "last_auth_ok",
        "login_failures",
        "event_count",
        "last_detail",
    )

    def save(self):
        data = {k: getattr(self, k) for k in self._SAVED}
        for k in self._TIMES:
            data[k] = self._get_iso()(data[k])
        try:
            self._get_store().set(self._get_skey()(self.sid, "status"), data)
        except Exception as e:
            self._get_log().error("Couldn't save status to the database: %s", e)

    def load(self):
        data = self._get_store().get(self._get_skey()(self.sid, "status")) or {}
        for k in self._SAVED:
            if k in data:
                v = data[k]
                if k in self._TIMES:
                    v = self._get_from_iso()(v)
                    v = v.astimezone(self._get_TZ()) if v else None
                setattr(self, k, v)
        if self.status == "running":  # container stopped mid-run
            self.status = "starting"
