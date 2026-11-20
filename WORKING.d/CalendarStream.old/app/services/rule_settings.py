"""Holds: rule settings.
Depends on: app/rules.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from .. import rules as rules_mod
from markupsafe import Markup, escape


def all_rules(*, rules_mod, source_ids, store) -> list[dict]:
    """Every rule, highest priority first."""
    return rules_mod.normalize_all(store.get("rules"), source_ids())


def rule_used(rid: str, *, calendar_name, store) -> list[str]:
    """(0.2.8-beta.33, I35) The calendar(s) a rule names, for its All Rules badge: from the raw, unstripped
    apply list still on file, not all_rules()'s own (which normalizes a rule's apply against today's live
    sources, so a now-removed calendar silently empties it - fine for matching events, but indistinguishable,
    in the badge, from a rule that's genuinely never had one chosen). Each name may be stale (the calendar's
    own name, or a generic fallback, if that's gone too); "all" or no match gives none.
    """
    raw = next(
        (
            r
            for r in (store.get("rules") or [])
            if isinstance(r, dict) and r.get("id") == rid
        ),
        None,
    )
    apply = (raw or {}).get("apply")
    if not isinstance(apply, list):
        return []
    return [calendar_name(x) for x in apply if isinstance(x, str) and x]


def save_rules(found: list[dict], *, rules_mod, store):
    store.set("rules", found[: rules_mod.MAX_RULES])


def source_rules(sid: str, *, all_rules, rules_mod) -> list[dict]:
    """The rules a calendar uses, highest priority first."""
    return rules_mod.for_source(all_rules(), sid)


def ruleset(
    sid: str, *, TZ, event_templates, rules_mod, settings, source_rules
) -> rules_mod.Ruleset:
    """A calendar's rules, ready to apply to its events. An event with no end time that no rule
    changes gets DEFAULT_EVENT_TYPE / DEFAULT_EVENT_HOURS from .env."""
    return rules_mod.Ruleset(
        source_rules(sid),
        TZ,
        {t["id"]: t for t in event_templates()},
        (settings.default_event_type, settings.default_event_hours),
    )


def color_name(color: str, *, GOOGLE_COLORS, nearest_color_id) -> str:
    return GOOGLE_COLORS[nearest_color_id(color)][0]


def rule_label(
    r: dict, lang: str, *, color_name, event_templates, i18n, rules_mod
) -> str:
    """A rule in one line: its title, else e.g. 'Text contains “RDO” → Color (Tomato)'."""
    tr = lambda t, **kw: str(i18n.tr(lang, t, **kw))
    return rules_mod.label(r, tr, color_name, {t["id"]: t for t in event_templates()})


def _swatch(color: str) -> str:
    return (
        f'<span class="swatch" style="--c:{escape(color)}" aria-hidden="true"></span>'
    )


def rule_label_html(
    r: dict,
    lang: str,
    *,
    _swatch,
    color_name,
    event_templates,
    i18n,
    rule_label,
    rules_mod,
) -> Markup:
    """The rule's line on the page (0.2.8-beta.5): each color's swatch right after the word Color, its
    name in brackets ("Color ■ (Tomato)"). A rule with a title also says what it does (0.2.8-beta.10):
    "Items without an end time → Change to all-day"."""
    text = rule_label(r, lang)
    colors = [a["color"] for a in r["actions"] if a["type"] == "color"]
    if r["title"] and r["actions"]:
        tr = lambda t, **kw: str(i18n.tr(lang, t, **kw))
        text += " → " + rules_mod.actions_text(
            r, tr, color_name, {t["id"]: t for t in event_templates()}
        )
    html = str(escape(text))
    word = str(escape(str(i18n.tr(lang, "Color"))))
    for c in dict.fromkeys(colors):
        piece = str(escape(f"({color_name(c)})"))
        html = html.replace(f"{word} {piece}", f"{word} {_swatch(c)} {piece}", 1)
    return Markup(html)


def migrate_rules(
    *,
    _migrate_rules_v3,
    _v3_rules,
    rules_mod,
    save_rules,
    settings,
    skey,
    source_ids,
    store,
):
    """0.2.8: the rules become one list of "If … Then …" rules (app/rules.py). The rules of 0.2.6–0.2.8-beta.1
    (and, through them, those of 0.2.5 and before) are converted; a new install starts with the two
    predefined ones (items without an end time, 24-hour events), for every calendar."""
    if store.get("rules") is not None:
        return
    if (
        store.get("rules_v3")
        or store.get("rule_templates") is not None
        or any(store.get(skey(sid, "calendar_tags")) for sid in source_ids())
    ):
        _migrate_rules_v3()
        lib = _v3_rules(store.get("rule_templates") or [])
        subs = {
            sid: list(store.get(skey(sid, "rule_subs")) or []) for sid in source_ids()
        }
        save_rules(rules_mod.from_v3(lib, subs, source_ids()))
    else:
        save_rules(
            rules_mod.starters(
                settings.default_event_type,
                settings.default_event_hours,
                settings.allday_24h,
            )
        )


def share_converted_rules(*, all_rules, save_rules, sources, store):
    """0.2.8-beta.3, once: rules converted in beta.2 that every calendar used were kept for those
    calendars only, so the Local calendar made after them (and calendars added later) didn't get
    them. A rule for every calendar but the Local ones becomes a rule for All calendars.
    """
    if store.get("rules_shared_b3") or store.get("rules") is None:
        return
    others = {x["id"] for x in sources() if x.get("type") != "local"}
    found = all_rules()
    for r in found:
        if r["apply"] != "all" and others and set(r["apply"]) == others:
            r["apply"] = "all"
    save_rules(found)
    store.set("rules_shared_b3", True)
