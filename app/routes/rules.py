"""Rules (If/Then) and event templates: save, test, clone, delete, move, apply, and settle conflicts.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import json
import re
import secrets
from itertools import zip_longest

from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from ..main import (_is_async, _sid, all_rules, app, calendar_name, Change, check_csrf, EVENT_COLORS,
    event_templates, gui_auth, ignored_conflicts, lang_for, MAX_TEMPLATES, rebuild, rule_label, save_rules,
    show_duration, source_ids, store)
from .. import rules as rules_mod


DURATION_RE = re.compile(r"^\s*(?:(\d{1,3})\s*[:h]\s*(\d{1,2})?|(\d{1,3}(?:[.,]\d+)?)\s*(h|m|min)?)\s*$", re.I)


def parse_duration(text: str, default: int = 0) -> int:
    """Minutes from "1:30", "1h30", "2" (hours), "1.5" (hours), "90m"; `default` when empty.
    Raises ValueError when it isn't a duration."""
    text = (text or "").strip()
    if not text:
        return default
    m = DURATION_RE.match(text)
    if not m:
        raise ValueError(text)
    if m.group(1) is not None:
        return int(m.group(1)) * 60 + int(m.group(2) or 0)
    value = float(m.group(3).replace(",", "."))
    return round(value if (m.group(4) or "").lower() in ("m", "min") else value * 60)


def _rule_or_400(rid: str) -> tuple[list[dict], int]:
    found = all_rules()
    i = next((n for n, r in enumerate(found) if r["id"] == rid), None)
    if i is None:
        raise HTTPException(400, "That rule doesn't exist (any more).")
    return found, i


def _rule_done(request: Request, rule: dict | None, anchor: str = "/#rules"):
    if _is_async(request):
        return {"ok": True, "id": rule["id"] if rule else "", "label": rule_label(rule, lang_for(request)) if rule else ""}
    return RedirectResponse(anchor, status_code=303)


@app.post("/rules/save", dependencies=[Depends(gui_auth)])
async def save_rule(request: Request, csrf: str = Form(""), rule: str = Form("")):
    """Save a rule from the rule dialog (`rule`: the rule as JSON, see app/rules.py). A new one goes in
    at its place (one for a single calendar above that calendar's shared rules, others last); a
    changed one keeps its place."""
    check_csrf(csrf)
    ch = Change()
    try:
        raw = json.loads(rule)
        checked = rules_mod.normalize(raw, source_ids(), {t["id"] for t in event_templates()}, strict=True)
    except (ValueError, TypeError) as e:
        raise HTTPException(400, str(e) if isinstance(e, rules_mod.RuleError) else "That rule couldn't be read.")
    found = all_rules()
    ids = [r["id"] for r in found]
    if raw.get("id") in ids:
        checked["id"] = raw["id"]
        found[ids.index(raw["id"])] = checked
        what = "changed"
    else:
        if len(found) >= rules_mod.MAX_RULES:
            raise HTTPException(400, f"Up to {rules_mod.MAX_RULES} rules can be kept.")
        while checked["id"] in ids:
            checked["id"] = "t" + secrets.token_hex(3)
        found.insert(rules_mod.insert_position(found, checked), checked)
        what = "added"
    save_rules(found)
    rebuild()
    ch.done("Rule", f"Rule {what}: {rule_label(checked)}")
    return _rule_done(request, checked)


@app.post("/rules/test", dependencies=[Depends(gui_auth)])
async def test_rule(csrf: str = Form(""), value: str = Form(""), op: str = Form("regex"), case: str = Form(""),
                    samples: str = Form("")):
    """The rule dialog's regex test box (0.2.8-beta.15): which of the given titles (one per line) a Title
    condition matches, with the same matching the rule uses, or why the pattern can't be used."""
    check_csrf(csrf)
    if op not in rules_mod.TEXT_OPS:
        raise HTTPException(400, "Unknown way to match.")
    lines = [x.strip() for x in samples.splitlines() if x.strip()][:30]
    return rules_mod.test_text(value.strip()[:rules_mod.MAX_REGEX], op, bool(case), [x[:300] for x in lines])


@app.post("/rules/clone", dependencies=[Depends(gui_auth)])
async def clone_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id")):
    """All Rules: a copy of a rule, just below it, applying to no calendar yet; it opens in the rule
    dialog to be changed."""
    check_csrf(csrf)
    ch = Change()
    found, i = _rule_or_400(rid)
    if len(found) >= rules_mod.MAX_RULES:
        raise HTTPException(400, f"Up to {rules_mod.MAX_RULES} rules can be kept.")
    copy = {**found[i], "id": "t" + secrets.token_hex(3), "apply": []}
    found.insert(i + 1, copy)
    save_rules(found)
    ch.done("Rule", f"Rule copied: {rule_label(copy)}")
    return RedirectResponse(f"/?rule={copy['id']}#rules", status_code=303)


@app.post("/rules/delete", dependencies=[Depends(gui_auth)])
async def delete_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id")):
    """Delete a rule (from every calendar)."""
    check_csrf(csrf)
    ch = Change()
    found, i = _rule_or_400(rid)
    gone = found.pop(i)
    save_rules(found)
    rebuild()
    ch.done("Rule", f"Rule deleted: {rule_label(gone)}")
    return _rule_done(request, None)


@app.post("/rules/move", dependencies=[Depends(gui_auth)])
async def move_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id"), before: str = Form(""),
                    after: str = Form("")):
    """Change a rule's priority: put it just above `before` (or just below `after`). The page sends the
    neighbour it now has in the list it was moved in (All Rules, or a calendar's)."""
    check_csrf(csrf)
    found, _ = _rule_or_400(rid)
    moved = rules_mod.move(found, rid, before, after)
    if moved != found:
        save_rules(moved)
        rebuild()
    return _rule_done(request, next(r for r in moved if r["id"] == rid))


@app.post("/rules/resolve", dependencies=[Depends(gui_auth)])
async def resolve_rules(request: Request, csrf: str = Form(""), key: str = Form(""), how: str = Form("")):
    """Settle a conflict between two rules (All Rules): put the lower rule first, take the action it
    loses out of it, merge duplicates, or leave them as they are (it's not shown again)."""
    check_csrf(csrf)
    ch = Change()
    found = all_rules()
    c = next((x for x in rules_mod.conflicts(found, source_ids()) if rules_mod.conflict_key(x) == key), None)
    if c is None:
        raise HTTPException(400, "That conflict isn't there any more.")
    if how not in {"duplicate": ("merge", "ignore"), "shadowed": ("up", "drop", "ignore")}[c["kind"]]:
        raise HTTPException(400, "Unknown choice.")
    ids = [r["id"] for r in found]
    a, b = found[ids.index(c["a"])], found[ids.index(c["b"])]
    if how == "ignore":
        store.set("rule_conflicts_ignored", (ignored_conflicts() + [key])[-200:])
        return _rule_done(request, b)
    if how == "up":
        found = rules_mod.move(found, b["id"], before=a["id"])
    elif how == "merge":
        found[ids.index(a["id"])] = rules_mod.merge(a, b)
        found.pop(ids.index(b["id"]))
    else:
        left = [x for x in b["actions"] if x["type"] != c["action"]]
        if left:
            found[ids.index(b["id"])] = {**b, "actions": left}
        else:
            found.pop(ids.index(b["id"]))
    save_rules(found)
    rebuild()
    ch.done("Rule", f"Rule conflict settled ({how}): {rule_label(b)}")
    return _rule_done(request, a)


@app.post("/rules/apply", dependencies=[Depends(gui_auth)])
async def apply_rule(request: Request, csrf: str = Form(""), rid: str = Form("", alias="id"), sid: str = Form(""),
                     on: str = Form("1")):
    """Add a calendar to a rule's calendars (a calendar module's "+ Add a rule" menu), or take it off
    (the bin on a rule in a calendar module)."""
    check_csrf(csrf)
    ch = Change()
    sid = _sid(sid)
    found, i = _rule_or_400(rid)
    r = found[i]
    users = list(source_ids()) if r["apply"] == "all" else list(r["apply"])
    users = list(dict.fromkeys(users + [sid])) if on == "1" else [x for x in users if x != sid]
    r["apply"] = "all" if on == "1" and r["apply"] == "all" else users
    save_rules(found)
    rebuild(sid)
    ch.done("Rule", f"Rule {'added to' if on == '1' else 'taken off'} {calendar_name(sid)}: {rule_label(r)}")
    return _rule_done(request, r, f"/#src-{sid}")


@app.post("/templates", dependencies=[Depends(gui_auth)])
async def set_templates(csrf: str = Form(""), tpl_id: list[str] = Form([]), tpl_title: list[str] = Form([]),
                        tpl_kind: list[str] = Form([]), tpl_duration: list[str] = Form([]),
                        tpl_location: list[str] = Form([]), tpl_color: list[str] = Form([])):
    """Save the event templates. Rows with no title are dropped; rules using a removed template stop
    adding events."""
    check_csrf(csrf)
    ch = Change()
    found = []
    old = {t["id"]: t for t in event_templates()}
    for tid, title, kind, dur, loc, color in zip_longest(tpl_id, tpl_title, tpl_kind, tpl_duration, tpl_location,
                                                         tpl_color, fillvalue=""):
        title = " ".join(title.split())[:200]
        if not title:
            continue
        try:
            minutes = parse_duration(dur, 60)
        except ValueError:
            raise HTTPException(400, f"Check the length of \"{title}\" (e.g. 1:30).")
        if kind != "allday" and not 5 <= minutes <= 24 * 60:
            raise HTTPException(400, f"\"{title}\" can last from 0:05 to 24:00.")
        color = color.lower()
        if color and color not in EVENT_COLORS:
            raise HTTPException(400, "Choose one of the colors offered.")
        tid = tid if re.fullmatch(r"[a-z0-9]{1,16}", tid or "") else "t" + secrets.token_hex(3)
        found.append({"id": tid, "title": title, "all_day": kind == "allday", "minutes": minutes if kind != "allday" else 60,
                      "location": loc.strip()[:200], "description": (old.get(tid) or {}).get("description", ""),
                      "color": color})
    if len(found) > MAX_TEMPLATES:
        raise HTTPException(400, f"Up to {MAX_TEMPLATES} templates can be kept.")
    store.set("event_templates", found)
    rebuild()
    ch.done("Rule", f"Event templates saved: {len(found)}")
    return RedirectResponse("/#templates", status_code=303)


@app.post("/templates/add", dependencies=[Depends(gui_auth)])
async def add_template(csrf: str = Form(""), tpl_title: str = Form(""), tpl_kind: str = Form("timed"),
                       tpl_duration: str = Form("1:00"), tpl_location: str = Form(""), tpl_color: str = Form("")):
    """+ Add an event template (0.2.8-beta.15, the pop-up): the templates as they are, and this one at the end."""
    if not " ".join(tpl_title.split()):
        raise HTTPException(400, "Give it a title.")
    old = event_templates()
    return await set_templates(csrf=csrf, tpl_id=[t["id"] for t in old] + [""], tpl_title=[t["title"] for t in old] + [tpl_title],
                               tpl_kind=["allday" if t["all_day"] else "timed" for t in old] + [tpl_kind],
                               tpl_duration=[show_duration(t["minutes"]) for t in old] + [tpl_duration],
                               tpl_location=[t.get("location", "") for t in old] + [tpl_location],
                               tpl_color=[t.get("color", "") for t in old] + [tpl_color])
