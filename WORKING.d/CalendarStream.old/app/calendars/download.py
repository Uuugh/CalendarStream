"""Holds: Download response model.
Depends on: no other app files.
Used by: app/calendars/downloads.py, app/calsync.py.
Reads/writes: values supplied by callers.
Dart note: calendar data adapters; inject transports and limits; preserve the compatibility facade.
"""

from dataclasses import dataclass


@dataclass
class Download:
    status: int
    body: bytes = b""
    etag: str = ""
    last_modified: str = ""
    not_modified: bool = False
    debug: dict | None = None
