"""Bounded in-memory tail of application log records.

Holds: _LogTail.
Depends on: nothing.
Used by: app/main.py.
Reads/writes: in-memory log lines.
Dart note: Log-tail sink in the login/data-independent diagnostics layer.
"""
import logging
from collections import deque

class _LogTail(logging.Handler):
    """The container's log as it's written (what `docker logs` shows for this app), kept in memory for
    History › Container log (0.2.8-beta.15): the last LOG_TAIL_LINES lines."""
    def __init__(self, keep: int):
        super().__init__()
        self.lines: deque[str] = deque(maxlen=keep)
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

    def emit(self, record):
        try:
            self.lines.append(self.format(record))
        except Exception:  # noqa: BLE001 - a line that can't be formatted is reported the logging way, never raised
            self.handleError(record)


