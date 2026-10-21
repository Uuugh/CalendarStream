"""Checking for a newer CalendarStream (Settings → Check for updates).

The release channel comes from IMAGE_TAG in .env (the installer writes it): "beta" follows the
newest version, "latest" (stable) and exact versions (e.g. 0.1.9) follow the last stable one, so a
stable install is never told about a beta. The newest version of each channel is read from the
repository's VERSION (beta) and STABLE (stable) files; only this install's version is sent (in the
User-Agent).
Saved in kv "update_check": {"checked": iso, "newest": "0.1.19", "channel": "beta", "error": "..."}.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone

import httpx

from . import __version__

RAW = "https://raw.githubusercontent.com/Uuugh/CalendarStream/main/"
RELEASES = "https://github.com/Uuugh/CalendarStream/releases"
FREQUENCIES = {"hourly": timedelta(hours=1), "weekly": timedelta(days=7), "monthly": timedelta(days=30), "never": None}
DEFAULT_FREQUENCY = "weekly"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def channel() -> str:
    """"beta", or "stable" for latest and for a pinned exact version."""
    tag = (os.environ.get("IMAGE_TAG") or "latest").strip().lower()
    return "beta" if tag == "beta" else "stable"


def _parts(version: str) -> tuple[int, ...] | None:
    return tuple(int(p) for p in version.split(".")) if VERSION_RE.match(version or "") else None


def is_newer(candidate: str, current: str = __version__) -> bool:
    a, b = _parts(candidate), _parts(current)
    return bool(a and b and a > b)


class Updates:
    def __init__(self, store):
        self.store = store

    def frequency(self) -> str:
        value = self.store.get("update_frequency")
        return value if value in FREQUENCIES else DEFAULT_FREQUENCY

    def set_frequency(self, value: str):
        if value not in FREQUENCIES:
            raise ValueError(value)
        self.store.set("update_frequency", value)

    def info(self) -> dict:
        saved = self.store.get("update_check") or {}
        if saved.get("channel") != channel():      # the channel changed since: that result doesn't apply
            return {}
        return saved

    def due(self, now: datetime) -> bool:
        every = FREQUENCIES[self.frequency()]
        if every is None:
            return False
        checked = self.info().get("checked")
        return not checked or now - datetime.fromisoformat(checked) >= every

    async def check(self) -> dict:
        """Read the newest version of this install's channel and save it."""
        name = "VERSION" if channel() == "beta" else "STABLE"
        result = {"checked": datetime.now(timezone.utc).isoformat(), "channel": channel()}
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                r = await client.get(RAW + name, headers={"User-Agent": f"CalendarStream/{__version__}"})
            newest = r.text.strip()
            if r.status_code != 200 or not VERSION_RE.match(newest):
                raise ValueError(f"HTTP {r.status_code}")
            result["newest"] = newest
        except (httpx.HTTPError, ValueError) as e:
            result["error"] = f"Couldn't check for updates ({type(e).__name__}: {e})"
            result["newest"] = self.info().get("newest")      # keep the last answer
        self.store.set("update_check", result)
        return result

    def available(self) -> str:
        """The newer version for this channel, or ""."""
        newest = self.info().get("newest") or ""
        return newest if is_newer(newest) else ""
