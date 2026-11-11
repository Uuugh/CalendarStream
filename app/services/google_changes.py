"""Holds: google changes.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import secrets
from datetime import datetime


def google_held(*, store) -> dict:
    """{uid: {dest, title, start}}: events deleted in Google that waited for the person's choice (0.2.8-beta.10
    to beta.14; taken as deletions at the next sync since beta.15)."""
    found = store.get("google_pending_deletes")
    return found if isinstance(found, dict) else {}


def _same_time(a: str, b: str) -> bool:
    if a == b:
        return True
    try:
        return datetime.fromisoformat(a) == datetime.fromisoformat(b)
    except ValueError:
        return False


async def apply_google_changes(
    d: dict,
    changes: list[dict],
    *,
    _FIELDS,
    _same_time,
    calendar_name,
    delete_events,
    dest_google,
    google_held,
    rebuild,
    source,
    state,
    store,
    united_original,
) -> list[str]:
    """Make the changes found in a destination's Google calendar here. Returns the log lines."""
    lines, touched = [], set()
    customs = {c["uid"]: c for c in store.get_customs()}
    edits = store.get_edits()
    held = google_held()
    restoring = set(
        store.get("google_restoring") or []
    )  # "Put them back": not deletions any more

    def still_here(uid):
        e = store.get_event(uid)
        return e is not None and not e.hidden

    # Deleted in Google (0.2.8-beta.15): struck through here, in no other feed, with Undo (Restore) in History;
    # any held by an earlier version ("more than 3 at once wait for you") are taken the same way now
    deleted = [
        c
        for c in changes
        if c["kind"] == "deleted" and c["uid"] not in restoring and still_here(c["uid"])
    ]
    deleted += [
        {"kind": "deleted", "uid": uid}
        for uid in held
        if still_here(uid) and uid not in {c["uid"] for c in deleted}
    ]
    if held:
        store.delete("google_pending_deletes")
    gone = []
    for c in deleted:
        e = store.get_event(c["uid"])
        if e is None:
            continue
        if e.origin == "rule":
            lines.append(f'"{e.title}" is made by a rule, so it was put back')
            continue
        gone.append(e)
        touched.add(e.source)
    if gone:
        names = ", ".join(f'"{e.title}" ({e.start[:10]})' for e in gone[:5]) + (
            " …" if len(gone) > 5 else ""
        )
        delete_events(gone, "google", f"Deleted in Google Calendar: {names}")
    for c in (c for c in changes if c["kind"] == "edited"):
        e = store.get_event(c["uid"])
        if e is None or c["uid"] in held:
            continue
        new = {k: c[k] for k in _FIELDS}
        if all(
            (
                _same_time(new[k], getattr(e, k))
                if k in ("start", "end")
                else new[k] == getattr(e, k)
            )
            for k in _FIELDS
        ):
            continue  # only its color or reminders changed there: put back
        if e.origin == "rule":
            lines.append(
                f'"{e.title}" is made by a rule, so Google\'s change was undone'
            )
            continue
        local_at = store.changed_at(e.uid)
        try:
            remote_at = datetime.fromisoformat(c["at"].replace("Z", "+00:00"))
        except ValueError:
            remote_at = None
        if (
            local_at
            and local_at > c["synced_at"]
            and (remote_at is None or local_at > remote_at)
        ):
            lines.append(
                f'"{e.title}" was changed here and in Google; the newer change, here, was kept'
            )
            continue
        if e.origin == "custom" and e.uid in customs:
            store.set_custom(e.uid, {**customs[e.uid], **new})
        else:
            original = united_original(e.uid, e.source)
            if not original:
                continue
            base = edits.get(e.uid) or {
                "title": e.title,
                "start": e.start,
                "end": e.end,
                "all_day": e.all_day,
                "location": e.location,
                "description": e.description,
                "color": e.color,
                "base": original.fingerprint(),
            }
            store.set_edit(e.uid, {**base, **new})
        lines.append(
            f"\"{new['title']}\" ({new['start'][:10]}) was changed in Google; the change is saved here"
        )
        touched.add(e.source)
    locals_ = [
        sid for sid in d["sources"] if (source(sid) or {}).get("type") == "local"
    ]
    told = set(
        store.get("google_left_alone") or []
    )  # events added in Google that can't come here: said once
    for c in (c for c in changes if c["kind"] == "created"):
        if c["repeats"] or not locals_:
            if c["gid"] not in told:
                lines.append(
                    f"\"{c['title']}\" was added in Google, but "
                    + (
                        "repeating events can't be copied here yet"
                        if c["repeats"]
                        else "this calendar gets no CalendarStream calendar to put it in"
                    )
                    + "; it's left as it is in Google"
                )
                told.add(c["gid"])
                store.set("google_left_alone", sorted(told)[-500:])
            continue
        uid = f"cs-{secrets.token_hex(8)}@calendar_stream"
        store.set_custom(
            uid, {**{k: c[k] for k in _FIELDS}, "color": "", "source": locals_[0]}
        )
        await dest_google(d).delete_event(
            d["id"], c["gid"]
        )  # it comes back as CalendarStream's own copy
        lines.append(
            f"\"{c['title']}\" ({c['start'][:10]}) was added in Google; it's now in {calendar_name(locals_[0])}"
        )
        touched.add(locals_[0])
    for sid in touched:
        rebuild(sid)
    if touched:
        state.save()
    return lines
