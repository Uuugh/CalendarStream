"""Holds: deletions.
Depends on: app/calendars/event.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from ..calendars.event import Event
import secrets


def mark_deleted(e: Event, where: str, *, Event, _hide, now, store):
    """Delete an event, keeping it struck through (see above)."""
    stamp = f"{where}|{now().isoformat(timespec='seconds')}"
    if e.origin == "custom":
        c = next((x for x in store.get_customs() if x["uid"] == e.uid), None)
        if c:
            store.set_custom(
                e.uid, {k: v for k, v in c.items() if k != "uid"} | {"deleted": stamp}
            )
        return
    had_edit = e.uid in store.get_edits()
    _hide(e)
    ed = store.get_edits().get(e.uid)
    if ed:
        store.set_edit(
            e.uid,
            {
                **ed,
                "hidden": True,
                "deleted": stamp,
                **({} if had_edit else {"for_delete": True}),
            },
        )


def unmark_deleted(uid: str, *, store):
    """Undo a delete: the event is back, as it was."""
    c = next((x for x in store.get_customs() if x["uid"] == uid), None)
    if c:
        store.set_custom(
            uid, {k: v for k, v in c.items() if k not in ("uid", "deleted")}
        )
        return
    ed = store.get_edits().get(uid)
    if ed and ed.get("for_delete"):
        store.delete_edit(uid)
    elif ed:
        store.set_edit(
            uid,
            {k: v for k, v in ed.items() if k not in ("deleted",)} | {"hidden": False},
        )
    store.google_forget(uid)  # it's written to Google again


def delete_events(
    found: list[Event], where: str, msg: str, *, Event, mark_deleted, pop_undo, state
) -> int | None:
    """Delete events (kept struck through) as one change that can be undone. Deleted outside CalendarStream
    (in Google), it's Restore on each event instead: no Undo on the stack, which is for changes made here.
    """
    for e in found:
        mark_deleted(e, where)
    entry = state.record(
        "info",
        msg,
        kind="Google" if where == "google" else "Event",
        undo={"type": "deleted", "where": where, "uids": [e.uid for e in found]},
        stack=where == "calendarstream",
    )
    pop_undo()
    return entry


def finish_deletions(*, rebuild, source_ids, store):
    """Deleted events whose Undo has popped off: an added one goes for good; a source's stays hidden
    and is no longer shown ("gone")."""
    live = {uid for undo in store.undo_payloads("deleted") for uid in undo["uids"]}
    touched = set()
    for c in store.get_customs():
        if c.get("deleted") and c["uid"] not in live:
            store.delete_custom(c["uid"])
            touched.add(c.get("source", "ccs"))
    for uid, ed in store.get_edits().items():
        if ed.get("deleted") and ed["deleted"] != "gone" and uid not in live:
            store.set_edit(uid, {**ed, "deleted": "gone"})
            e = store.get_event(uid)
            touched.add(e.source if e else "ccs")
    for sid in touched & set(source_ids()):
        rebuild(sid)


def keep_removed(
    sid: str,
    previous: list[Event],
    events: list[Event],
    *,
    Event,
    TZ,
    calendar_name,
    now,
    pop_undo,
    publish,
    skey,
    state,
    store,
):
    """Events the source no longer has (United removed them, or they're gone from the feed): kept here
    struck through, as added events of this calendar, so Undo (Restore) can keep them. Past events that
    simply drop off the schedule aren't kept."""
    today = now().astimezone(TZ).date().isoformat()
    still = {e.uid for e in events}
    gone = [
        e
        for e in previous
        if e.origin == "united"
        and not e.hidden
        and e.uid not in still
        and e.end[:10] >= today
    ]
    if not gone:
        return
    where = "united" if sid == "ccs" else "feed"
    kept = []
    for e in gone[:200]:
        uid = f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(
            uid,
            {
                "title": e.title,
                "start": e.start,
                "end": e.end,
                "all_day": e.all_day,
                "location": e.location,
                "description": e.description,
                "color": e.color,
                "source": sid,
                "deleted": f"{where}|{now().isoformat(timespec='seconds')}",
            },
        )
        kept.append(uid)
    names = ", ".join(f'"{e.title}" ({e.start[:10]})' for e in gone[:5]) + (
        " …" if len(gone) > 5 else ""
    )
    who = (
        "United removed"
        if sid == "ccs"
        else f"{calendar_name(sid)}: gone from the feed:"
    )
    state.record(
        "info",
        f"{who} {len(gone)} event{'s' if len(gone) != 1 else ''}: {names}",
        kind="Event",
        undo={"type": "deleted", "where": where, "uids": kept},
        stack=False,
    )  # Restore on each event
    pop_undo()
    publish_again = store.get_calendar(skey(sid, "source"))
    if publish_again:
        publish(publish_again[0], publish_again[1], sid)
