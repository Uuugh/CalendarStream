"""Holds: logging setup.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import logging


def tail_logs(*, LOG_TAIL):
    """Keep the log lines from here on (called at start-up, once uvicorn has set up its own loggers):
    the app's (the root logger) and uvicorn's, which don't pass theirs up."""
    for name in ("", "uvicorn", "uvicorn.access"):
        logger = logging.getLogger(name)
        if LOG_TAIL not in logger.handlers and (not name or not logger.propagate):
            logger.addHandler(LOG_TAIL)
