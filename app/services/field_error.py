"""Holds: field error.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from fastapi import HTTPException


class FieldError(HTTPException):
    """A refused Save that names the fields to fix (0.2.8-beta.17, F8): the page outlines them in amber."""

    def __init__(self, message: str, *fields: str):
        super().__init__(400, message, headers={"X-CS-Fields": ",".join(fields)})
