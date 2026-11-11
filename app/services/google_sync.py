"""Holds: google sync.
Depends on: app/calendars/event.py, app/gsync.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from ..calendars.event import Event
from ..gsync import Google
import asyncio
from datetime import date
from urllib.parse import urlparse


def request_google_sync(full: bool, *, google_job):
    google_job.full = google_job.full or full
    google_job.wake.set()


def notify_address(*, public_url) -> str:
    """Where Google sends change notifications, or "" when there's no public https:// address
    (Google only delivers them to https:// with a valid certificate)."""
    base = public_url()
    host = urlparse(base).hostname or ""
    if (
        not base.startswith("https://")
        or host in ("localhost", "127.0.0.1")
        or host.endswith(".local")
    ):
        return ""
    return f"{base}/google/notify"


async def ensure_watch(
    sid: str,
    *,
    GoogleError,
    WATCH_RENEW,
    WATCH_RETRY,
    dest_google,
    destination,
    destinations,
    google,
    notify_address,
    now,
    state,
):
    """Keep Google's change notifications ("webhooks") running for a destination's calendar: start
    them, move them to a new public address, renew them before they run out. If Google refuses,
    Autosync carries on as before (daily check) and asks again later."""
    address = notify_address()
    d = destination(sid)
    g = dest_google(d) if d else google
    if (
        not address
        or not g.connected
        or not g.watch_due(sid, address, now(), WATCH_RENEW, WATCH_RETRY)
    ):
        return
    before = g.watch_info(sid)
    had = bool(before.get("id")) or any(
        g.watch_info(x["id"]).get("id")
        for x in destinations("google")
        if x["id"] != sid
    )
    try:
        await g.start_watch(sid, address)
        if not had:
            state.record(
                "info",
                "Google: instant updates turned on (changes made in Google are checked within seconds)",
            )
    except GoogleError as e:
        if str(e) != before.get("error"):  # say so once, not at every retry
            state.record(
                "warn",
                f"Google: instant updates aren't available ({e}); changes made in Google are checked daily instead",
            )


def source_off(sid: str, *, skey, store) -> bool:
    """0.2.8-beta.28, F25: a calendar switched Off is unavailable (greyed in every feed that has it selected; the selection is kept)."""
    return bool(store.get(skey(sid, "off")))


def dest_events(d: dict, *, Event, TZ, _span, source_off, store) -> list[Event]:
    """A destination's events: those of its sources (not those switched Off), within its dates (Start / End; empty = no limit)."""

    def inside(e: Event) -> bool:
        first, last, _, _ = _span(e, TZ)
        return (not d.get("start") or last.isoformat() >= d["start"]) and (
            not d.get("end") or first.isoformat() <= d["end"]
        )

    return sorted(
        (
            e
            for sid in d["sources"]
            if not source_off(sid)
            for e in store.load_events(sid)
            if inside(e)
        ),
        key=lambda e: e.start,
    )


def event_colorer(*, calendar_color, source_ids):
    """A function giving an event's color: its own, else its rules', else its source's ("" for none)."""
    colors = {sid: calendar_color(sid) for sid in source_ids()}
    return lambda e: e.color or e.rule_color or colors.get(e.source, "")


def sync_window_start(*, now) -> date:
    """Decision 5: events from the first day of the current month onward are synced."""
    return now().date().replace(day=1)


def _say_not_signed_in(mods: list[dict], *, _unsigned_said, state):
    """A Google module whose account has no sign-in is skipped by every sync; say so once (until it signs in),
    so a feed that "does nothing" has a line in History saying why."""
    for d in mods:
        if d.get("off") or d["id"] in _unsigned_said:
            continue
        _unsigned_said.add(d["id"])
        state.record(
            "warn",
            f"Google, {d['name']}: not signed in to a Google account yet, so it isn't synced: open it and Connect me",
            kind="Google",
        )


async def google_sync_once(
    full: bool,
    *,
    _say_not_signed_in,
    _sync_account,
    _unsigned_said,
    destinations,
    event_colorer,
    google,
    google_accounts,
    google_for,
    google_health,
    google_job,
) -> bool:
    """Run one sync of every Google module, account by account (0.2.8-beta.15). Returns False if one failed."""
    async with google_job.lock:
        dests = destinations("google")
        if not (google.configured and dests):
            return True
        google_job.running = True
        ok = True
        try:
            color_for = event_colorer()
            for account in google_accounts():
                mine = [d for d in dests if d["account"] == account]
                g = google_for(account)
                if mine and g.connected:
                    _unsigned_said.difference_update(d["id"] for d in mine)
                    if not google_health.may_sync(
                        account
                    ):  # waiting out a back-off after a failure
                        continue
                    ok = (
                        await _sync_account(g, mine, len(dests), color_for, full) and ok
                    )
                else:
                    _say_not_signed_in(mine)
        finally:
            google_job.running = False
        return ok


async def _sync_account(
    g: Google,
    dests: list[dict],
    total: int,
    color_for,
    full: bool,
    *,
    CALENDAR_COLORS,
    COLOR_TRY,
    COLOR_WAY_TEXT,
    EARLIEST,
    Google,
    GoogleError,
    _remember_calendar,
    apply_google_changes,
    dest_events,
    ensure_watch,
    google_health,
    google_held,
    nearest_calendar_color,
    state,
    store,
) -> bool:
    try:
        for d in dests:
            if d.get("off"):  # F25: switched Off
                continue
            first = date.fromisoformat(d["start"]) if d.get("start") else EARLIEST
            who = "Google" if total == 1 else f"Google, {d['name']}"
            if (
                full and not d["oneway"]
            ):  # two-way: what changed in Google comes here first (0.2.8-beta.10)
                for line in await apply_google_changes(d, await g.pull(d["id"], first)):
                    state.record("info", f"{who}: {line}")
            result = await g.sync(
                d["id"],
                dest_events(d),
                d["name"],
                color_for,
                first,
                full,
                hold=frozenset(google_held()),
            )
            if full and store.get("google_restoring"):
                store.set("google_restoring", [])  # put back in Google by this sync
            if result.changed or result.notes:
                state.record(
                    "info",
                    f"{who}: {result.summary()}"
                    + ("; " + "; ".join(result.notes) if result.notes else ""),
                )
            info = g.cal_info(d["id"])
            # (0.2.8-beta.19, I1) tried again once after updating, so History gets Google's own reason for a refusal
            tried = (
                info.get("color_tried") == d["color"]
                and info.get("color_try") == COLOR_TRY
            )
            if (
                d["color"] and info.get("color") != d["color"] and not tried
            ):  # its color box (0.2.8-beta.15)
                # (0.2.8-beta.18, I4) tried once per color: Google refusing it is said once and never makes the
                # module's sync a "Sync problem" (before, it failed after every successful sync)
                kept = info.get("color_way")
                try:
                    way = await g.set_color(d["id"], d["color"])
                except GoogleError as e:
                    way = None
                    # out of reach or busy: tried again at the next sync (which says so itself); anything else, said once
                    said = str(e)
                    if not (
                        said.startswith("Couldn't reach Google Calendar")
                        or said.startswith("Google Calendar is busy")
                    ):
                        refused = said.startswith("Google Calendar refused")
                        g._update_cal(
                            d["id"],
                            color_tried=d["color"],
                            color_try=COLOR_TRY,
                            color_refused=d["color"] if refused else None,
                        )
                        how = (
                            "it refused the RGB color, the nearest calendar color and a full update "
                            if refused
                            else ""
                        )
                        state.record(
                            "warn",
                            f"{who}: the calendar's color couldn't be set in Google Calendar: {how}({e}); "
                            "set it there by hand if you like",
                            kind="Google",
                        )
                if way:
                    g._update_cal(d["id"], color_refused=None)
                    # (I1) the way Google takes is said once, when it's first known or changes; the nearest calendar
                    # color always, since Google then shows a color a little different from the color box's
                    how = ""
                    if way == "colorId":
                        how = f" {COLOR_WAY_TEXT[way]} ({CALENDAR_COLORS[nearest_calendar_color(d['color'])]})"
                    elif way != kept:
                        how = f" {COLOR_WAY_TEXT[way]}"
                    if way != kept:
                        how += "; that way is kept"
                    state.record(
                        "info",
                        f"{who}: color set in Google Calendar{how}",
                        kind="Google",
                    )
            _remember_calendar(d["id"], g)
            await ensure_watch(d["id"])
        google_health.record_success(g.account)
        return True
    except GoogleError as e:
        message = str(e)
        google_health.check_and_recover(g.account, e)
    except Exception as e:  # keep the loop alive whatever happens
        message = f"Google sync failed: {type(e).__name__}: {e}"
        google_health.check_and_recover(
            g.account, e
        )  # (REVIEW 2, #11 #1) an unexpected failure is classified too (UNKNOWN)
    if message != g.info().get("last_error"):  # log each new problem once
        state.record("error", f"Google: {message}")
    g.record_error(message)
    return False


def _remember_calendar(did: str, g: Google, *, Google, store):
    """(0.2.8-beta.18, I5) The Google calendar a module writes to, kept apart from its sign-in: a module that
    connects again (a new sign-in, the same Gmail) finds it and uses it again, instead of making a second one.
    """
    cid = g.cal_info(did).get("calendar_id")
    found = store.get("google_calendar_ids") or {}
    if cid and found.get(did) != cid:
        store.set("google_calendar_ids", {**found, did: cid})


def _remembered_calendar(did: str, *, store) -> str | None:
    return (store.get("google_calendar_ids") or {}).get(did)


async def google_loop(
    *, GOOGLE_FULL_CHECK, GOOGLE_RETRY, google_job, google_sync_once, log, now
):
    next_full = now()
    while True:
        google_job.wake.clear()
        full = google_job.full or now() >= next_full
        google_job.full = False
        try:
            ok = await google_sync_once(full)
        except (
            Exception
        ) as e:  # e.g. the database restarting: keep the loop alive, retry later
            log.error("Google sync failed: %s", e)
            ok = False
        if ok and full:
            next_full = now() + GOOGLE_FULL_CHECK
        wait = next_full - now()
        if not ok:
            wait = min(wait, GOOGLE_RETRY)
        try:
            await asyncio.wait_for(
                google_job.wake.wait(), timeout=max(60, wait.total_seconds())
            )
            await asyncio.sleep(
                2
            )  # let a burst of changes (e.g. several edits) settle first
        except asyncio.TimeoutError:
            pass
