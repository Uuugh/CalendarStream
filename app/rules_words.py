"""Human-readable rule descriptions.

Holds: _hm, length_text, cond_text, action_text, actions_text, label.
Depends on: nothing.
Used by: app/rules.py.
Reads/writes: nothing.
Dart note: Rule text formatter in rules/domain; translation and color names are caller callbacks.
"""

COND_TYPES = {"text": "Title", "any": "Any text", "date": "Date", "time": "Time", "days": "Day(s)", "length": "Length"}
TEXT_OPS = {"is": "is", "contains": "contains", "word": "whole word", "begins": "begins with", "ends": "ends with",
            "pattern": "matches pattern", "regex": "contains regex"}
TEXT_KINDS = ("text", "any")
OPS = {
    "text": TEXT_OPS, "any": TEXT_OPS,
    "date": {"is": "is", "after": "after", "before": "before", "between": "between"},
    "time": {"is": "is", "after": "after", "before": "before", "between": "between"},
    "days": {"is": "is", "after": "after", "before": "before", "between": "between"},
    "length": {"is": "is", "days": "is whole days"},
}

TEXT_FIELDS = {"title": "Title", "notes": "Notes", "location": "Location"}

WHEN = {"before_start": "before the start", "after_start": "after the start", "after_end": "after the end"}

DAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

# --- Words ---------------------------------------------------------------------------------------

def _hm(minutes: int) -> str:
    return f"{minutes // 60}:{minutes % 60:02d}"


def length_text(minutes: int) -> str:
    """e.g. "1 w 2 d 3:30", "0:45", "0" (no end)."""
    if not minutes:
        return "0"
    w, rest = divmod(minutes, 7 * 1440)
    d, rest = divmod(rest, 1440)
    parts = ([f"{w} w"] if w else []) + ([f"{d} d"] if d else []) + ([_hm(rest)] if rest else [])
    return " ".join(parts)


def cond_text(c: dict, tr) -> str:
    """One condition in words, e.g. 'Text contains "RDO"', 'Day(s) is Sat, Sun'."""
    head = f"{tr(COND_TYPES[c['type']])} {tr(OPS[c['type']][c['op']])}"
    if c["type"] in TEXT_KINDS:
        return f"{head} “{c['value']}”" + (" Aa" if c["case"] else "")
    if c["type"] in ("date", "time"):
        return f"{head} {c['value']}" + (f" – {c['value2']}" if c["op"] == "between" else "")
    if c["type"] == "days":
        names = [tr(DAY_NAMES[d]) for d in c["days"]]
        return f"{head} " + (" – ".join(names) if c["op"] == "between" else ", ".join(names))
    if c["op"] == "days":
        return tr("Length is whole days")
    return tr("No end time") if not c["minutes"] else f"{head} {length_text(c['minutes'])}"


def action_text(a: dict, tr, color_name, templates: dict[str, dict]) -> str:
    if a["type"] == "color":
        return f"{tr('Color')} ({color_name(a['color'])})"       # the page puts its swatch before the brackets
    if a["type"] == "emoji":
        return f"{a['emoji']} {tr('in front of the title')}"
    if a["type"] == "event":
        t = templates.get(a["template"]) if a["template"] else a
        return (f"{tr('Create')} “{t['title'] if t else '?'}”, "
                + tr("{time} {when}", time=_hm(a["offset"]), when=tr(WHEN[a["when"]])))
    if a["type"] == "change":
        if a["to"] in TEXT_FIELDS:
            return tr("Change {field} to “{text}”", field=tr(TEXT_FIELDS[a["to"]]), text=a["text"])
        return tr("Change to all-day") if a["to"] == "allday" else tr("Change length to {length}", length=_hm(a["minutes"]))
    if a["type"] == "add":
        return tr("Add “{text}” to {field}", text=a["text"].replace("\n", " ⏎ "), field=tr(TEXT_FIELDS[a["to"]]))
    if a["type"] == "delete":
        return tr("Delete this event")
    if a["type"] == "move":
        if a.get("with_link"):
            return tr("Move this event with the linked event")
        return tr("Move this event by {time}", time=("−" if a["minutes"] < 0 else "+") + _hm(abs(a["minutes"])))
    return tr("Record changes in the event notes section")


def actions_text(rule: dict, tr, color_name, templates: dict[str, dict]) -> str:
    """What a rule does, in a few words ('Change to all-day; Color (Tomato)')."""
    return "; ".join(action_text(a, tr, color_name, templates) for a in rule["actions"])


def label(rule: dict, tr, color_name, templates: dict[str, dict]) -> str:
    """A rule in one line: its title, else 'If … → …'."""
    if rule["title"]:
        return rule["title"]
    link = rule.get("link")
    if link:
        return (tr("Linked to “{name}”", name=link["name"] or "?") + " → "
                + "; ".join(action_text(a, tr, color_name, templates) for a in rule["actions"]))
    conds = rule["conds"]
    parts = []
    for i, c in enumerate(conds):
        if i:
            parts.append(tr(c["join"]))
        parts.append("(" * c["open"] + cond_text(c, tr) + ")" * c["close"])
    head = " ".join(parts) if conds else tr("Every event")
    return f"{head} → " + "; ".join(action_text(a, tr, color_name, templates) for a in rule["actions"])
