"""Holds: google job.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import asyncio


class GoogleJob:
    """The background Google sync: woken whenever the published schedule changes."""

    def __init__(self):
        self.wake = asyncio.Event()
        self.full = True  # the first sync after startup checks everything
        self.running = False
        self.lock = asyncio.Lock()  # one sync (or disconnect) at a time
