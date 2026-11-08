"""Holds: Calendar source exception family.
Depends on: no other app files.
Used by: app/calendars/downloads.py, app/calendars/parsing.py, app/calendars/validation.py, app/calsync.py.
Reads/writes: values supplied by callers.
Dart note: calendar data adapters; inject transports and limits; preserve the compatibility facade.
"""


class AuthError(Exception):
    """401: UID or Calendar Sync password rejected."""


class BlockedError(Exception):
    """403 or similar: the server refused the request (e.g. Akamai 'Access Denied')."""


class SourceError(Exception):
    """Anything else: network trouble, server errors, or a response that isn't a calendar."""


class NoReplyError(SourceError):
    """Connected, but nothing came back in time: the silent hold (I8)."""
