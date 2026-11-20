"""Holds: source jobs.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import asyncio
import json
from datetime import timedelta
from urllib.parse import urlparse


async def run_once(
    manual: bool,
    sid: str,
    *,
    AuthError,
    BlockedError,
    MAX_AUTH_FAILURES,
    SourceError,
    apply_calendar,
    calendar_url,
    download,
    logins,
    now,
    run_feed,
    source_ids,
    state,
    store,
):
    """Download a source now (CCS+ or a feed) and publish it if it changed."""
    if sid != "ccs":
        return await run_feed(sid)
    if state.running or "ccs" not in source_ids():
        return
    if not logins.ccs_configured:
        # Nothing to do until the login is entered; the page shows the boxes for it.
        state.status = "setup"
        state.message = "Enter your CCS+ Username and Calendar Sync password to start downloading the schedule."
        state.save()
        return
    if state.login_failures >= MAX_AUTH_FAILURES and not manual:
        state.status = "paused"
        state.message = (
            f"Automatic downloads paused after {state.login_failures} rejected sign-ins, to avoid "
            "locking your account. Check the Username and Calendar Sync password in the CCS+ Calendar Sync box, then press Sync now."
        )
        state.save()
        return

    state.running, state.status = True, "running"
    state.last_attempt = now()
    try:
        have_source = store.get_calendar("source") is not None
        cache = (store.get("http_cache") or {}) if have_source else {}
        uid, password = logins.ccs()
        dl = await download(
            calendar_url(),
            uid,
            password,
            etag=cache.get("etag", ""),
            last_modified=cache.get("last_modified", ""),
        )
        store.save_debug(
            "response", json.dumps(dl.debug, indent=2).encode(), "application/json"
        )
        state.last_auth, state.last_auth_ok, state.login_failures = now(), True, 0

        if dl.not_modified:
            state.status, state.last_success, state.last_detail = (
                "ok",
                now(),
                "no changes",
            )
            state.message = (
                f"Up to date: {state.event_count} events in feed (no changes)"
            )
            state.record("info", "Schedule downloaded from CCS+: no changes")
            return

        store.save_debug("source", dl.body, "text/calendar; charset=utf-8")
        if apply_calendar(dl.body, "downloaded from CCS+"):
            store.set(
                "http_cache", {"etag": dl.etag, "last_modified": dl.last_modified}
            )

    except AuthError as e:
        state.last_auth, state.last_auth_ok = now(), False
        state.login_failures += 1
        state.status, state.message = "auth_failed", str(e)
        state.record("error", f"Sign-in rejected: {e}")
    except BlockedError as e:
        state.status, state.message = "blocked", str(e)
        state.record("error", f"Blocked: {e}")
    except SourceError as e:
        state.status, state.message = "error", str(e)
        state.record("error", f"Download failed: {e}")
    except Exception as e:
        state.status, state.message = (
            "internal",
            f"{type(e).__name__}: {e}",
        )  # CalendarStream itself failed: red (beta.14)
        state.record("error", f"Unexpected error: {state.message}")
    finally:
        state.running = False
        state.save()


async def run_feed(
    sid: str,
    *,
    AuthError,
    BlockedError,
    SourceError,
    apply_calendar,
    download,
    now,
    skey,
    source_ids,
    source_url,
    st,
    store,
):
    """Download a feed source (no login) and publish it if it changed."""
    S = st(sid)
    if S.running or sid not in source_ids():
        return
    S.running, S.status = True, "running"
    S.last_attempt = now()
    try:
        url = source_url(sid)
        host = urlparse(url).hostname or url
        have_source = store.get_calendar(skey(sid, "source")) is not None
        cache = (store.get(skey(sid, "http_cache")) or {}) if have_source else {}
        dl = await download(
            url,
            etag=cache.get("etag", ""),
            last_modified=cache.get("last_modified", ""),
            who=host,
        )
        store.save_debug(
            skey(sid, "response"),
            json.dumps(dl.debug, indent=2).encode(),
            "application/json",
        )
        if dl.not_modified:
            S.status, S.last_success, S.last_detail = "ok", now(), "no changes"
            S.message = f"Up to date: {S.event_count} events in feed (no changes)"
            S.record("info", f"Schedule downloaded from {host}: no changes")
            return
        store.save_debug(skey(sid, "source"), dl.body, "text/calendar; charset=utf-8")
        if apply_calendar(dl.body, f"downloaded from {host}", sid):
            store.set(
                skey(sid, "http_cache"),
                {"etag": dl.etag, "last_modified": dl.last_modified},
            )
    except (AuthError, BlockedError, SourceError) as e:
        S.status, S.message = "error", str(e)
        S.record("error", f"Download failed: {e}")
    except Exception as e:
        S.status, S.message = "internal", f"{type(e).__name__}: {e}"
        S.record("error", f"Unexpected error: {S.message}")
    finally:
        S.running = False
        S.save()


def interval_minutes(
    sid: str, *, MAX_INTERVAL, MIN_INTERVAL, settings, skey, store
) -> int:
    """How often to download a source: set on the status page, else SYNC_INTERVAL_MINUTES (CCS+) or an hour."""
    saved = store.get(skey(sid, "sync_interval"))
    default = settings.interval_minutes if sid == "ccs" else 60
    return (
        saved
        if isinstance(saved, int) and MIN_INTERVAL <= saved <= MAX_INTERVAL
        else default
    )


async def loop(sid: str, *, interval_minutes, log, now, run_once, st):
    """One source's checks, every interval_minutes."""
    S = st(sid)
    while True:
        try:
            await run_once(sid=sid)
            S.next_run = now() + timedelta(minutes=interval_minutes(sid))
        except (
            Exception
        ) as e:  # e.g. the database restarting: keep the loop alive, try again soon
            log.error("Scheduled check failed: %s", e)
            S.next_run = now() + timedelta(minutes=5)
        # Sleep until the next check. S.wake means the interval changed: work out the time again.
        while (remaining := (S.next_run - now()).total_seconds()) > 0:
            S.wake.clear()
            try:
                await asyncio.wait_for(S.wake.wait(), timeout=remaining)
            except asyncio.TimeoutError:
                break


def start_source(sid: str, *, loop, source, source_tasks):
    """Start a source's checks (when the app starts or the source is added); a local calendar has none."""
    if (source(sid) or {}).get("type") == "local":
        return
    if sid not in source_tasks or source_tasks[sid].done():
        source_tasks[sid] = asyncio.create_task(loop(sid))


def stop_source(sid: str, *, source_tasks):
    task = source_tasks.pop(sid, None)
    if task:
        task.cancel()


def background(coro, *, _background):
    """Start a task without waiting for it, keeping a reference so it isn't garbage-collected."""
    task = asyncio.create_task(coro)
    _background.add(task)
    task.add_done_callback(_background.discard)
    return task
