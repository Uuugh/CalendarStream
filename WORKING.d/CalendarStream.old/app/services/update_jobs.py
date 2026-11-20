"""Holds: update jobs.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timedelta, timezone


def mark_updating(target: str, *, __version__, store):
    """(0.2.8-beta.24, F1) An update was asked of the updater: open pages see it in /api/status ("updating") and
    follow along (Downloading…, Restarting…), then refresh themselves."""
    store.set(
        "update_running",
        {
            "from": __version__,
            "to": target,
            "at": datetime.now(timezone.utc).isoformat(),
        },
    )


def updating_to(*, __version__, store) -> str:
    """The version an update asked for in the last 15 minutes is going to, or "" (the restart clears it: the new
    version isn't the one it came from)."""
    run = store.get("update_running") or {}
    try:
        recent = datetime.now(timezone.utc) - datetime.fromisoformat(
            run.get("at", "")
        ) < timedelta(minutes=15)
    except ValueError:
        return ""
    return run.get("to", "") if recent and run.get("from") == __version__ else ""


def auto_update(*, store) -> bool:
    """Settings → Updates → Auto-update (beta.3): install a newer version by itself (needs the updater)."""
    return store.get("update_auto") is True


async def update_loop(
    *, auto_install, auto_update, log, state, store, updater, updates
):
    """Settings → Check for updates: look for a newer version of this install's channel when due, and
    with Auto-update on (and the updater running), install it."""
    await asyncio.sleep(30)
    while True:
        try:
            if updates.due(datetime.now(timezone.utc)):
                found = await updates.check()
                if updates.available() and found.get("newest") != found.get("logged"):
                    state.record(
                        "info",
                        f"Update available: CalendarStream {found['newest']} "
                        + (
                            "(Auto-update will install it)"
                            if auto_update() and updater.ready and not updater.pinned()
                            else (
                                "(press Update now next to the version)"
                                if updater.ready and not updater.pinned()
                                else "(run the installer again to update)"
                            )
                        ),
                    )
                    store.set("update_check", {**found, "logged": found["newest"]})
            await auto_install()
        except Exception as e:  # never let this stop the app
            log.warning("Update check failed: %s", e)
        # (0.2.8-beta.24, F1) wake when the next check is due at the frequency chosen in Settings (at most an hour
        # later, so a changed frequency is seen), not only on the hour
        nxt = updates.next_check(datetime.now(timezone.utc))
        wait = (
            3600 if nxt is None else (nxt - datetime.now(timezone.utc)).total_seconds()
        )
        await asyncio.sleep(min(3600, max(60, wait)))


async def auto_install(
    *, UpdaterError, auto_update, mark_updating, state, store, updater, updates
):
    """With Auto-update on: ask the updater for a newer version (once per version, so a failing
    update isn't tried every hour)."""
    target = updates.available()
    if (
        not (target and auto_update() and updater.ready and not updater.pinned())
        or store.get("update_auto_tried") == target
    ):
        return
    store.set("update_auto_tried", target)
    try:
        await updater.update()
        mark_updating(target)
        state.record(
            "info",
            f"Auto-update: updating to CalendarStream {target}: downloading, then restarting",
        )
    except UpdaterError as e:
        state.record("warn", f"Auto-update to CalendarStream {target} not started: {e}")


async def updater_loop(*, log, updater):
    """Whether the optional updater container is running (checked now and every 5 minutes), so the
    page knows whether to offer "Update now"."""
    while True:
        try:
            await updater.probe()
        except Exception as e:  # never let this stop the app
            log.warning("Updater check failed: %s", e)
        await asyncio.sleep(300)
