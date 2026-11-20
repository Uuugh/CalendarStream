"""Checking for a newer CalendarStream (Settings → Check for updates).

Versions are semver: x.y.z for a stable release, x.y.z-beta.N for the betas leading up to it
(0.2.7-beta.1 < 0.2.7-beta.2 < 0.2.7). The release channel comes from IMAGE_TAG in .env (the
installer writes it): "beta" and exact beta versions (e.g. 0.2.7-beta.1) follow the newest version,
"latest" (stable) and exact stable versions (e.g. 0.1.9) follow the last stable one, so a stable
install is never told about a beta. The newest version of each channel is read from the
repository's VERSION (beta) and STABLE (stable) files; only this install's version is sent (in the
User-Agent).
Saved in kv "update_check": {"checked": iso, "newest": "0.1.19", "channel": "beta", "error": "...",
"logged": the version last announced in the activity log}.
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
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-beta\.(\d+))?$")


def channel() -> str:
    """"beta" for beta and a pinned beta version, "stable" for latest and a pinned stable version."""
    tag = (os.environ.get("IMAGE_TAG") or "latest").strip().lower()
    return "beta" if tag == "beta" or "-beta." in tag else "stable"


def is_stable(version: str) -> bool:
    """True for x.y.z, False for a beta (x.y.z-beta.N) or anything else."""
    m = VERSION_RE.match(version or "")
    return bool(m) and m[4] is None


def _parts(version: str) -> tuple[int, ...] | None:
    """A sort key: (x, y, z, 1, 0) for x.y.z and (x, y, z, 0, N) for x.y.z-beta.N, so every
    beta of a version comes before the version itself. None if it isn't a version."""
    m = VERSION_RE.match(version or "")
    if not m:
        return None
    x, y, z, beta = m.groups()
    return (int(x), int(y), int(z), 0, int(beta)) if beta else (int(x), int(y), int(z), 1, 0)


def is_newer(candidate: str, current: str | None = None) -> bool:
    """True if `candidate` comes after `current` (this install's version by default)."""
    a, b = _parts(candidate), _parts(current if current is not None else __version__)
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

    def next_check(self, now: datetime) -> datetime | None:
        """When the next automatic check is due (now, if it's overdue), or None when they're off.
        The background loop looks once an hour, so it can come up to an hour later."""
        every = FREQUENCIES[self.frequency()]
        if every is None:
            return None
        checked = self.info().get("checked")
        due = datetime.fromisoformat(checked) + every if checked else now
        return max(due, now)

    async def check(self) -> dict:
        """Read the newest version of this install's channel and save it."""
        name = "VERSION" if channel() == "beta" else "STABLE"
        result = {"checked": datetime.now(timezone.utc).isoformat(), "channel": channel(),
                  "logged": self.info().get("logged")}      # the version already announced in the log
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                r = await client.get(RAW + name, headers={"User-Agent": f"CalendarStream/{__version__}"})
            newest = r.text.strip()
            if r.status_code != 200 or not VERSION_RE.match(newest):
                raise ValueError(f"HTTP {r.status_code}")
            if name == "STABLE" and not is_stable(newest):     # STABLE never names a beta
                raise ValueError(f"STABLE says {newest!r}")
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


# --- Updating from the status page ------------------------------------------------------------
# With the optional updater container (Watchtower, nicholas-fedor's maintained fork; install.sh asks)
# "Update now" asks it to pull this install's image tag again and restart the container with it.
# Watchtower's API is only reachable inside the Docker network, behind a random token kept in
# .secrets/UPDATER_TOKEN.txt; it updates only containers labelled for it (this one, not the database).

IMAGE = "ghcr.io/uuugh/calendarstream"


class UpdaterError(RuntimeError):
    """The updater couldn't be asked to update; the message says why."""


class Updater:
    def __init__(self):
        self.ready = False          # the updater answered its last health check

    @staticmethod
    def url() -> str:
        return (os.environ.get("UPDATER_URL") or "").rstrip("/")

    @staticmethod
    def token() -> str:
        path = os.environ.get("UPDATER_TOKEN_FILE") or ""
        try:
            return open(path, encoding="utf-8").read().strip() if path else ""
        except OSError:
            return ""

    @staticmethod
    def pinned() -> bool:
        """An exact version in IMAGE_TAG: updating would only fetch the same version again."""
        return (os.environ.get("IMAGE_TAG") or "latest").strip().lower() not in ("latest", "beta")

    async def probe(self) -> bool:
        """Is the updater running? (Its /livez needs no token.) Saved in `ready`."""
        ok = False
        if self.url() and self.token():
            try:
                async with httpx.AsyncClient(timeout=3) as client:
                    ok = (await client.get(self.url() + "/livez")).status_code == 200
            except httpx.HTTPError:
                ok = False
        self.ready = ok
        return ok

    async def update(self):
        """Ask the updater to pull this install's image and restart CalendarStream with it. It answers
        at once and works in the background; this container is stopped and replaced along the way."""
        if not (self.url() and self.token()):
            raise UpdaterError("The updater isn't set up. Run the installer again and answer yes to updating from the status page.")
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.post(self.url() + "/v1/update", params={"image": IMAGE, "async": "true"},
                                      headers={"Authorization": f"Bearer {self.token()}"})
        except httpx.HTTPError as e:
            raise UpdaterError(f"Couldn't reach the updater ({type(e).__name__}). Is its container running?")
        if r.status_code in (200, 202, 429):        # 429: an update is already running
            return
        if r.status_code == 401:
            raise UpdaterError("The updater refused the token. Run the installer again to set them up together.")
        raise UpdaterError(f"The updater answered HTTP {r.status_code}.")
