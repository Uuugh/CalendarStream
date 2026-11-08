"""Holds: event links.
Depends on: app/calendars/event.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from ..calendars.event import Event
import secrets


def event_links(*, all_rules, links_mod) -> dict[str, dict]:
    """{following event's ID: its link}, read from the link rules (the event pop-up's Link to makes them)."""
    return links_mod.from_rules(all_rules())


def set_event_links(found: dict[str, dict], *, all_rules, save_rules):
    """Write links back to their rules: a link's rule follows its event's ID, the linked event, its calendar and the
    start last seen; a link taken out of `found` takes its rule with it. (Rules without a link are left alone.)
    """
    by_rule = {
        link["rule"]: (uid, link) for uid, link in found.items() if link.get("rule")
    }
    out = []
    for r in all_rules():
        link = r.get("link")
        if link:
            hit = by_rule.get(r["id"])
            if not hit:
                continue
            uid, l = hit
            own = l.get("own") or link["own"]
            r = {
                **r,
                "link": {
                    **link,
                    "uid": uid,
                    "to": l["to"],
                    "src": l["src"],
                    "at": l["at"],
                    "own": own,
                    "name": l.get("name", link["name"]),
                },
            }
            if own != link["own"] and r["apply"] == [link["own"]]:
                r["apply"] = [own]
        out.append(r)
    save_rules(out)


def link_rule_for(uid: str, *, all_rules) -> dict | None:
    return next(
        (r for r in all_rules() if (r.get("link") or {}).get("uid") == uid), None
    )


def migrate_links(*, all_rules, links_mod, rules_mod, save_rules, source_ids, store):
    """0.2.8-beta.27 (F3), once: the links kept in kv "event_links" become link rules (Delete this event / Move this
    event with the linked event, as the two boxes were ticked), so they show in All Rules, each Then removable.
    """
    old = links_mod.clean(store.get("event_links"))
    if not old:
        return
    found = all_rules()
    have = {(r.get("link") or {}).get("uid") for r in found}
    for uid, l in old.items():
        e = store.get_event(uid)
        other = store.get_event(l["to"])
        actions = ([{"type": "delete"}] if l["delete"] else []) + (
            [{"type": "move", "minutes": 0, "with_link": True}] if l["move"] else []
        )
        if uid in have or not actions or e is None:
            continue
        rule = rules_mod.normalize(
            {
                "id": "t" + secrets.token_hex(3),
                "conds": [],
                "actions": actions,
                "apply": [e.source],
                "link": {
                    "uid": uid,
                    "own": e.source,
                    "to": l["to"],
                    "src": l["src"],
                    "at": l["at"],
                    "name": other.title if other else "",
                },
            },
            source_ids(),
        )
        if rule:
            found.append(rule)
    save_rules(found)
    store.set("event_links", {})


def _hide(e: Event, *, Event, store, united_original):
    """Hide a source's own event from every destination (deleting it would only bring it back)."""
    original = united_original(e.uid, e.source)
    if not original:
        return
    edit = store.get_edits().get(e.uid) or {
        "title": e.title,
        "start": e.start,
        "end": e.end,
        "all_day": e.all_day,
        "location": e.location,
        "description": e.description,
        "color": e.color,
        "base": original.fingerprint(),
    }
    store.set_edit(e.uid, {**edit, "hidden": True})


def follow_links(
    sid: str,
    events: list[Event],
    *,
    _hide,
    event_links,
    links_mod,
    rebuild,
    set_event_links,
    state,
    store,
    united_original,
    get_following,
    set_following,
):
    """After a calendar is built: the events linked to its events follow them (deleted with them, moved
    with them), and their calendars are built again."""
    found = event_links()
    todo = links_mod.plan(found, sid, events)
    if (
        not todo or get_following()
    ):  # (a calendar built because of a link: its own links are followed next time)
        return
    touched = set()
    edits = store.get_edits()
    customs = {c["uid"]: c for c in store.get_customs()}
    for step in todo:
        kind, uid = step[0], step[1]
        if kind == "seen":
            found[uid]["at"], found[uid]["name"] = step[2], step[3]
            continue
        if kind == "unlink":
            found.pop(uid, None)
            continue
        e = store.get_event(uid)
        if e is None or e.origin == "rule":
            found.pop(uid, None)
            continue
        if kind == "delete":
            if e.origin == "custom":
                store.delete_custom(uid)
            else:
                _hide(e)
            state.record(
                "info",
                f'Deleted "{e.title}" ({e.start[:10]}) with the event it\'s linked to',
            )
            found.pop(uid, None)
        else:  # move
            start, end = links_mod.shifted(e.start, e.end, step[2])
            if e.origin == "custom" and uid in customs:
                store.set_custom(uid, {**customs[uid], "start": start, "end": end})
            elif e.origin == "united":
                original = united_original(uid, e.source)
                if original:
                    base = edits.get(uid) or {
                        "title": e.title,
                        "all_day": e.all_day,
                        "location": e.location,
                        "description": e.description,
                        "color": e.color,
                        "base": original.fingerprint(),
                    }
                    store.set_edit(uid, {**base, "start": start, "end": end})
            state.record(
                "info",
                f"Moved \"{e.title}\" to {start[:16].replace('T', ' ')} with the event it's linked to",
            )
        touched.add(e.source)
    set_event_links(found)
    set_following(True)
    try:
        for one in touched:
            rebuild(one)
    finally:
        set_following(False)
