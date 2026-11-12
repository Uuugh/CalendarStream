"""Holds: page settings.
Depends on: app/i18n.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from .. import i18n
from fastapi import Request
import hashlib
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


SETTINGS_MODULES = ("pagelogin", "updates", "look", "googlesync")


def settings_order(*, store, modules=SETTINGS_MODULES) -> list[str]:
    """Saved Settings order, retaining known items once and appending new modules."""
    saved = store.get("ui_settings_order")
    saved = saved if isinstance(saved, list) else []
    return list(dict.fromkeys([x for x in saved if isinstance(x, str) and x in modules] + list(modules)))


def section_state(*, FOLD_AFTER, SECTIONS, store) -> dict:
    """Open/closed: the page's sections, and the Configure part of each source's box ("src:<id>")
    and destination's box ("dest:<id>", "dest:google" for the Google account). One left open for 24 hours folds
    by itself (F20): the first time it is seen open is its start (ui_opened), however it was opened.
    """
    saved = store.get("ui_sections") or {}
    found = {k: bool(saved.get(k, default)) for k, default in SECTIONS.items()}
    found.update(
        {k: bool(v) for k, v in saved.items() if k.startswith(("src:", "dest:"))}
    )
    opened = store.get("ui_opened") or {}
    now, changed, folds = datetime.now(timezone.utc).timestamp(), False, False
    for k in list(found):
        if k not in ("rules", "templates", "activity", "beta") and not k.startswith(
            ("src:", "dest:")
        ):
            continue  # (Calendar, Calendars and Feeds have no Expand line)
        if found[k]:
            if k not in opened:
                opened[k] = now
                changed = True
            elif now - opened[k] > FOLD_AFTER:
                found[k] = False
                saved[k] = False
                opened.pop(k)
                changed = folds = True
        elif k in opened:
            opened.pop(k)
            changed = True
    if changed:
        if folds:
            store.set("ui_sections", saved)
        store.set("ui_opened", opened)
    return found


def lang_for(request: Request, *, i18n, store) -> str:
    """The language chosen in the status page's language menu, else the browser's."""
    return i18n.pick(store.get("ui_lang"), request.headers.get("accept-language", ""))


def page(
    request: Request,
    name: str,
    context: dict,
    status_code: int,
    lang: str | None,
    *,
    FREQUENCIES,
    RELEASES,
    __version__,
    _local_time,
    auto_update,
    dates_for,
    i18n,
    iso,
    lang_for,
    look,
    release_channel,
    store,
    templates,
    ui_clock,
    ui_theme,
    updater,
    updates,
):
    """Render a page in the visitor's language. Templates get `_` (translate a page text),
    `msg` (translate a message made in Python), `dates` and the language menu's details.
    """
    lang = lang or lang_for(request)
    return templates.TemplateResponse(
        request,
        name,
        {
            **context,
            "lang": lang,
            "html_lang": i18n.HTML_LANG[lang],
            "langs": i18n.LANGS,
            "lang_choice": (
                store.get("ui_lang") if store.get("ui_lang") in i18n.LANGS else "auto"
            ),
            "_": lambda t, **kw: i18n.tr(lang, t, **kw),
            "msg": lambda text: i18n.message(lang, text),
            "dates": dates_for(lang),
            "theme": ui_theme(),
            "clock": ui_clock(),
            "look": look(),
            "update": {
                "available": updates.available(),
                "channel": release_channel(),
                "frequency": updates.frequency(),
                "frequencies": list(FREQUENCIES),
                "info": updates.info(),
                "releases": RELEASES,
                "checked": _local_time(updates.info().get("checked"), lang),
                "next": _local_time(
                    iso(updates.next_check(datetime.now(timezone.utc))), lang
                ),
                "updater": updater.ready,
                "can_update": updater.ready and not updater.pinned(),
                "auto": auto_update(),
            },
            "version": __version__,
        },
        status_code=status_code,
    )


def look(*, ANIM_DEFAULT, store) -> dict:
    """(0.2.8-beta.29, F14) ☰ Settings › Look: the Developer's own logo and favicon (uploaded; None = CalendarStream's own)
    and the buttons' Animation (intensity, duration; percent, 100 = as designed)."""
    saved = store.get("brand") or {}
    out = {
        "logo": None,
        "favicon": None,
        "anim": dict(ANIM_DEFAULT),
        "grips": "right" if store.get("ui_grips") == "right" else "left",
    }  # (0.2.8-beta.31, F36.1) the reorder grips' side
    for kind in ("logo", "favicon"):
        if saved.get(kind):
            out[kind] = (
                f"/brand/{kind}?v={hashlib.md5(saved[kind]['b64'].encode()).hexdigest()[:8]}"
            )
    a = store.get("ui_anim") or {}
    for k, lo, hi in (("i", 0, 200), ("d", 25, 300)):
        try:
            out["anim"][k] = min(hi, max(lo, int(a.get(k, 100))))
        except (TypeError, ValueError):
            pass
    out["style"] = (
        ""
        if out["anim"] == ANIM_DEFAULT
        else f"--anim-i:{out['anim']['i'] / 100:g};--anim-d:{out['anim']['d'] / 100:g}"
    )
    return out


def ui_clock(*, CLOCKS, store) -> str:
    """12-hour (1:00pm) or 24-hour ("military", 13:00) times on the status page, or "auto" (by language)."""
    clock = store.get("ui_clock")
    return clock if clock in CLOCKS else "auto"


def valid_zone(name: str, *, ALL_ZONES) -> bool:
    return name == "UTC" or name in ALL_ZONES


def display_zone(*, settings, store, valid_zone) -> str:
    """The calendar's time zone on the status page: chosen above the calendar, else TZ."""
    name = store.get("ui_tz") or ""
    return name if valid_zone(name) else settings.timezone


def display_tz(*, display_zone) -> ZoneInfo:
    return ZoneInfo(display_zone())


def dates_for(lang: str, *, i18n, ui_clock) -> i18n.Dates:
    """Day and month names, and times on the chosen clock."""
    return i18n.Dates(lang, {"12": False, "24": True}.get(ui_clock()))


def ui_theme(*, THEMES, store) -> str:
    """Light / dark / system, saved in the database so every browser uses the same choice."""
    theme = store.get("ui_theme")
    return theme if theme in THEMES else "system"
