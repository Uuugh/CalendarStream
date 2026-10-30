"""The status page itself: the page (/), its stylesheet and script, the calendar views, Print, and the
page's own settings (/ui/…: open sections, language, clock, view, time zone, theme).

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

import calendar as pycal
import gzip
import re
import secrets
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Depends, Form, HTTPException, Query, Request
from fastapi.responses import Response

from .. import main as core
from ..main import (_invites, _local_time, _opt_day, _parse_month, _span, admin_email, ALARM_CHOICES, alarm_text,
    all_rules, ALL_ZONES, app, base_url, cal_view, calendar_color, calendar_name, check_csrf, CLOCKS, COMMON_ZONES,
    COPY_ICON, customs_for, dates_for, DELETED_WHERE, dest_google, DESTINATION_TYPES, destinations, display_tz,
    display_zone, EARLIEST, event_links, event_templates, feed_url, first_named_calendar, google, google_view,
    gui_auth, ignored_conflicts, interval_minutes, lang_for, LOG_KINDS, logins, MODULE_ABOUT, notify_address, now,
    page, public_addresses, public_url, rule_label, rule_label_html, section_state, SECTIONS, skey, source,
    source_ids, SOURCE_PRESETS, source_rules, source_url, st, state, store, subscribe_links, templates, THEMES,
    TRASH_ICON, TZ, undo_keep, valid_zone)
from .. import i18n, icons, rules as rules_mod
from ..calsync import Event
from ..config import DEFAULT_CALENDAR_URL, settings
from ..gsync import GOOGLE_COLORS


# --- The status page's stylesheet and script, cached (0.2.8-beta.4) -----------------------------------
# They used to be inside every page (about 150 KB, sent again on each load and each in-place save). Now
# they're files the browser keeps: the stylesheet as it is, the script made once per language (its words
# are translated). Both are sent compressed when the browser accepts it: they hold no secrets, so
# compressing them is safe (the pages themselves, which hold the form token, are not compressed).
_ASSETS: dict[str, tuple[bytes, bytes]] = {}


def _asset(key: str, make) -> tuple[bytes, bytes]:
    if key not in _ASSETS:
        raw = make()
        _ASSETS[key] = (raw, gzip.compress(raw, 9))
    return _ASSETS[key]


def _send_asset(request: Request, key: str, make, media_type: str) -> Response:
    raw, packed = _asset(key, make)
    if "gzip" in request.headers.get("accept-encoding", ""):
        return Response(packed, media_type=media_type, headers={"Content-Encoding": "gzip", "Vary": "Accept-Encoding"})
    return Response(raw, media_type=media_type, headers={"Vary": "Accept-Encoding"})


# (0.2.8-beta.20, F12) The stylesheet is kept in parts, app/styles/NN-<what>.css, sent as one file: the parts in
# their number order, which is the cascade's (a later rule wins a tie), so a part is never reordered.
STYLES = Path(__file__).parent.parent / "styles"


def stylesheet() -> bytes:
    return b"".join(p.read_bytes() for p in sorted(STYLES.glob("*.css")))


@app.get("/assets/app.css")
def app_css(request: Request):
    return _send_asset(request, "app.css", stylesheet, "text/css; charset=utf-8")


@app.get("/assets/page-{version}-{lang}.js")
def page_js(request: Request, version: str, lang: str):
    if version != core.__version__ or lang not in i18n.LANGS:
        raise HTTPException(404)
    make = lambda: templates.env.get_template("page.js").render(
        _=lambda text, **kw: i18n.tr(lang, text, **kw), lang=lang).encode()
    return _send_asset(request, f"page-{lang}.js", make, "text/javascript; charset=utf-8")


def feed_reads(lang: str, did: str) -> dict:
    reads = store.get(f"feed_reads:{did}") or {}
    return {k: _local_time(reads.get(k), lang) for k in ("google", "other")}


def dest_base(request: Request, d: dict | None = None) -> str:
    """The address a feed's links use: the one chosen in its Feed link (if it's still one of the public
    addresses), else the main one."""
    chosen = (d or {}).get("base") or ""
    return chosen if chosen in public_addresses() else base_url(request)


def _watch_one(lang: str, d: dict) -> dict:
    """(0.2.8-beta.18) One Google module's instant updates, for its header (☰ Settings no longer shows them):
    on (with the last notice) or why not."""
    if not notify_address():
        return {"on": False, "why": "needs a public https:// address (☰ → Public address)"}
    w = dest_google(d).watch_info(d["id"])
    if w.get("error") and w.get("address") == notify_address():
        return {"on": False, "why": w["error"]}
    if w.get("id"):
        return {"on": True, "last": _local_time(w.get("last_notice") or None, lang)}
    return {"on": False, "why": "starts with the next sync"}


VIEWS = ("month", "week", "day", "list")


def ui_view() -> str:
    """The calendar's view on the status page: month, week, day or list (agenda)."""
    view = store.get("ui_view")
    return view if view in VIEWS else "month"


# --- Routes ----------------------------------------------------------------------

def source_view(request: Request, sid: str, lang: str, sections: dict) -> dict:
    """One calendar's module on the status page."""
    S = st(sid)
    kind = (source(sid) or {}).get("type", "ccs")
    if kind == "local":       # nothing to download: always fine
        S.status, S.message = "ok", ""
    url = source_url(sid)
    d = dates_for(lang)
    view = {"id": sid, "type": kind, "name": calendar_name(sid), "default": source_ids()[:1] == [sid],
            "color": calendar_color(sid), "s": S, "interval": interval_minutes(sid),
            "url": url, "host": urlparse(url).hostname or url,
            # Configure is folded unless it's been opened, or something needs doing
            "open": sections.get(f"src:{sid}", False) or S.status not in ("ok", "running", "starting")
                    or (sid == "ccs" and not logins.ccs_configured),
            "downloaded": store.get_calendar(skey(sid, "source")) is not None,
            "has_debug": store.has_debug(skey(sid, "source")),
            "last_when": d.when(S.last_success, now().date()) if S.last_success else "",
            # "Last check was successful @ 14:34" / "Last check failed @ 14:49"
            "last_check": ("ok" if S.status in ("ok", "running") and S.last_success else "failed" if S.last_attempt else ""),
            "check_when": d.when(S.last_success if S.status in ("ok", "running") else S.last_attempt, now().date())
                          if (S.last_success or S.last_attempt) else "",
            "added": sum(1 for c in customs_for(sid)),
            # its rules, highest priority first (its own ones first, unless moved)
            "rules": [{**r, "label": rule_label(r, lang), "html": rule_label_html(r, lang), "local": rules_mod.is_local(r, sid)} for r in source_rules(sid)],
            "preset": (source(sid) or {}).get("preset", "other"), "next_when": dates_for(lang).when(S.next_run, now().date()) if S.next_run else "",
            # the note under the title: as set (even empty), else the kind of calendar
            "note": source_note(sid)}
    if sid == "ccs":
        view["setup"] = {
            "uid": logins.ccs()[0], "has_password": bool(logins.ccs()[1]), "configured": logins.ccs_configured,
            "url": url, "url_is_default": url == DEFAULT_CALENDAR_URL, "url_from_gui": bool(store.get("calendar_url")),
            "downloaded": view["downloaded"]}
    return view


def dest_view(request: Request, d: dict, lang: str, sections: dict) -> dict:
    """One destination's box on the status page ("open": its Configure part, as last left)."""
    view = {**d, "names": [calendar_name(x) for x in d["sources"]], "open": sections.get(f"dest:{d['id']}", False)}
    if d["type"] == "feed":
        base = dest_base(request, d)
        view.update(feed=feed_url(request, d["token"], base), links=subscribe_links(request, d["token"], base, d["name"]),
                    reads=feed_reads(lang, d["id"]), base=base)
    else:
        g = dest_google(d)
        cal = g.cal_info(d["id"])
        view.update(cal=cal, last_sync=_local_time(cal.get("last_sync"), lang), connected=g.connected,
                    email=g.info().get("email", ""), error=g.info().get("last_error", ""), own_account=bool(d["account"]),
                    invite=invite_view(request, d["id"], lang), watch=_watch_one(lang, d))
    return view


def _parse_day(value: str | None, month: str | None) -> date:
    """The day the calendar is around: ?date=YYYY-MM-DD, else the first of ?month=YYYY-MM, else today
    (in the display time zone); today's day when only the month is today's."""
    try:
        d = date.fromisoformat(value or "")
        if 2000 <= d.year <= 2100:
            return d
    except ValueError:
        pass
    today = now().astimezone(display_tz()).date()
    if month:
        y, m = _parse_month(month)
        return today if (y, m) == (today.year, today.month) else date(y, m, 1)
    return today


def rule_js(lang: str) -> dict:
    """What the rule dialog's script needs: every rule as saved, and the choices, in the page's language."""
    tr = lambda text: str(i18n.tr(lang, text))
    return {"rules": {r["id"]: r for r in all_rules()},
            "types": {k: tr(v) for k, v in rules_mod.COND_TYPES.items()},
            "ops": {k: [[o, tr(v)] for o, v in ops.items()] for k, ops in rules_mod.OPS.items()},
            "actions": [[k, tr(v)] for k, v in rules_mod.ACTION_TYPES.items()],
            "when": [[k, tr(v)] for k, v in rules_mod.WHEN.items()],
            "templates": [[t["id"], t["title"]] for t in event_templates()],
            "days": [tr(d) for d in rules_mod.DAY_NAMES],
            "calendars": [[sid, calendar_name(sid)] for sid in source_ids()],
            "emoji": ["✈️", "🏝️", "📚", "🏠", "🚗", "⭐", "❗", "🛌", "🎓", "🎉"],
            "samples": rule_samples(),
            # what each insert helper of the regex test box puts in (0.2.8-beta.15)
            "rx": {k: tr(v) for k, v in {"starts": "Starts with (^)", "ends": "Ends with ($)", "word": "Whole word (\\b…\\b)",
                                         "either": "Either: the selected words, or A|B", "any": "Any text (.*)", "digits": "Digits (\\d+)",
                                         "space": "A space (\\s)", "optional": "The one before is optional (?)",
                                         "literal": "The selected text exactly (escapes . ( ) + * ?)",
                                         "anyText": "* any text", "digit": "# a digit", "oneChar": "? one character"}.items()},
            # Google's 11 event colors: a rule's Color is one of them (0.2.8-beta.5), as an event's is
            "palette": [[hexc, str(i18n.tr(lang, name))] for name, hexc in GOOGLE_COLORS.values()],
            "t": {"and": tr("and"), "or": tr("or"), "weeks": tr("weeks"), "days": tr("days"), "hours": tr("hours"),
                  "minutes": tr("minutes"), "caps": tr("Match capitals exactly"), "remove": tr("Take this line out"),
                  "newEvent": tr("New event…"), "noCalendar": tr("No calendar yet"), "color": tr("Color"), "title": tr("Title"), "location": tr("Location"), "allDay": tr("All day"),
                  "length": tr("Length (hours:minutes)"), "time": tr("Time (hours:minutes)"), "allCalendars": tr("All calendars"),
                  "toAllDay": tr("all-day"), "toLength": tr("a length of"), "changeTo": tr("to"), "emoji": tr("Emoji"),
                  "open": tr("Open a bracket here"), "close": tr("Close a bracket here"),
                  "noEnd": tr("0 = no end time"), "editSamples": tr("Change the titles to test"),
                  "matchCount": tr("{n} of {total} match"), "andAdd": tr("and: another line"), "orAdd": tr("or: another line"),
                  "searchEmoji": tr("Search for more emojis"), "noEmoji": tr("No emoji with that name"),
                  "olderWindows": tr("May not show on older Windows"),
                  "lasting": tr("lasting"), "at": tr("at")},
            "info_icon": str(icons.svg("info", 15)),     # (0.2.8-beta.19, F8) the (i) beside an emoji
            "version": core.__version__}


def rule_samples(n: int = 10) -> list[str]:
    """Titles to try a pattern on: the next `n` different ones, from today, in every calendar."""
    today = now().astimezone(display_tz()).date().isoformat()
    found = sorted((e.start[:10], e.title) for sid in source_ids() for e in store.load_events(sid)
                   if e.title and not e.hidden and e.origin != "rule")
    upcoming = [t for d, t in found if d >= today] + [t for d, t in reversed(found) if d < today]
    return list(dict.fromkeys(upcoming))[:n]


def cal_search(events: list[Event], q: str, src: str, first: date | None, last: date | None, lang: str = "en") -> dict:
    """The calendar's search (0.2.8-beta.11): the events whose title, place or notes contain `q` (any
    case), in one calendar or all, between two days (0.2.8-beta.15: All, every date, when not given),
    listed by day like the List view."""
    given = {"from": first.isoformat() if first else "", "to": last.isoformat() if last else ""}
    first, last = first or EARLIEST, last or date(2100, 12, 31)
    if last < first:
        first, last = last, first
    words = q.casefold().split()
    found = [e for e in events if (not src or e.source == src)
             and all(w in f"{e.title} {e.location} {e.description}".casefold() for w in words)]
    out = cal_view(found, "list", first, lang)
    tz = display_tz()
    # every matching day from `first` to `last` (cal_view's list covers one month)
    by_day = {}
    for e in found:
        d0, d1, s, t = _span(e, tz)
        if d1 < first or d0 > last:
            continue
        by_day.setdefault(d0 if d0 >= first else first, []).append(e)
    days = []
    for d in sorted(by_day):
        one = cal_view(by_day[d], "day", d, lang)["days"]
        days += [x for x in one if x["items"]]
    n = sum(len(x["items"]) for x in days)
    return {**out, "days": days, "count": n, "search": {"q": q, "src": src, **given},
            "title": str(i18n.tr(lang, "{n} found", n=n))}


@app.get("/", dependencies=[Depends(gui_auth)])
def index(request: Request, month: str | None = None, date_: str | None = Query(None, alias="date"),
          view: str | None = None, q: str = "", qsrc: str = "", qfrom: str = "", qto: str = ""):
    """The status page. `view` shows the calendar in another view this time only (phones open on the
    list until a view has been chosen); `q` (with `qsrc`, `qfrom`, `qto`) searches it (0.2.8-beta.11)."""
    events = [e for e in store.load_events() if e.deleted != "gone"]
    ref = _parse_day(date_, month)
    history = [{**h, "time": h["time"].astimezone(TZ)} for h in store.recent_log(300)]
    undo_top, redo_next = store.undo_stack()
    lang = lang_for(request)
    sections = section_state()
    srcs = [source_view(request, sid, lang, sections) for sid in source_ids()]
    return page(request, "index.html", {
        "s": state, "cfg": settings, "history": history, "undo_top": undo_top, "redo_next": redo_next,
        "undo_keep": undo_keep(), "log_kinds": LOG_KINDS,
        "cal": (cal_search(events, q.strip()[:100], qsrc if qsrc in source_ids() else "", _opt_day(qfrom), _opt_day(qto), lang)
                if q.strip() else cal_view(events, view if view in VIEWS else ui_view(), ref, lang)), "views": VIEWS,
        "view_explicit": store.get("ui_view") in VIEWS,
        "csrf": core.CSRF_TOKEN, "name": calendar_name(), "srcs": srcs,
        "new_stream": secrets.token_urlsafe(24),       # + Add a feed's link, whole from the start (0.2.8-beta.23, F13.1)
        "dests": [dest_view(request, d, lang, sections) for d in destinations()], "dest_types": DESTINATION_TYPES,
        # every rule, highest priority first, with its label and calendars (All Rules; "+ Add a rule")
        "all_rules": [{**r, "label": rule_label(r, lang), "html": rule_label_html(r, lang),
                       "used": [calendar_name(x) for x in source_ids() if rules_mod.applies(r, x)]} for r in all_rules()],
        "rule_js": rule_js(lang),
        "rule_conflicts": rule_conflicts(lang),
        "linked": linked_titles(),
        "default_dest_name": first_named_calendar(),
        "src_names": {x["id"]: x["name"] for x in srcs},
        "has_ccs": "ccs" in source_ids(), "templates": event_templates(), "event_colors": GOOGLE_COLORS.values(),
        "deleted_where": {k: str(i18n.tr(lang, v)) for k, v in DELETED_WHERE.items()},
        "palette": list(GOOGLE_COLORS.values()), "about": {k: str(i18n.tr(lang, v)) for k, v in MODULE_ABOUT.items()},
        "sections": sections, "zone": display_zone(), "zones": ALL_ZONES, "common_zones": COMMON_ZONES,
        "google": google_view(request, lang), "open_menu": request.query_params.get("menu") == "settings",
        # The first destination offers this page's address as the public one, if it's https:// (an
        # http://<IP>:8080 address would break Google sign-in, as the old installer default did).
        "public": {"url": public_url(), "here": (lambda u: u if u.startswith("https://") else "")(str(request.base_url).rstrip("/")),
                   "extra": public_addresses()[1:], "all": public_addresses() or [base_url(request)]},
        "api_on": core.api_on(),
        "page_user": logins.page_user, "admin_email": admin_email(), "trash": TRASH_ICON, "copy_icon": COPY_ICON,
        # History, Undo & Logs, folded: Healthy unless a problem in the log is still there
        "healthy": not any(st(sid).status in ("auth_failed", "blocked", "error", "internal", "paused") for sid in source_ids())
                   and not (google.connected and google.info().get("last_error")),
        "print_prefs": print_prefs(), "print_views": PRINT_VIEWS,
        "alarm_choices": [(m, alarm_text(m, lang)) for m in ALARM_CHOICES],
    }, lang=lang)


def source_note(sid: str) -> str:
    """A calendar's own note (0.2.8-beta.9: shown as a raised (i) after its name), or "" when it has none.
    The header's first line now says what kind of calendar it is, so the old default notes (which said
    that, and were saved by any Save) count as no note."""
    note = store.get(skey(sid, "note")) or ""
    return "" if note.strip() == default_note(sid) else note


def default_note(sid: str) -> str:
    """What kind of calendar it is, as the note said until 0.2.8-beta.9 (to recognise old saved notes)."""
    x = source(sid) or {}
    if x.get("type") == "ccs":
        return "CCS+ Calendar Sync"
    if x.get("type") == "local":
        return "Events added here"
    preset = x.get("preset") if x.get("preset") in SOURCE_PRESETS else "other"
    url = x.get("url") or ""
    return SOURCE_PRESETS[preset] + ("" if preset != "other" else " · " + (urlparse(url).hostname or url))


# --- Rule conflicts (F4.2) -----------------------------------------------------------------------

CONFLICT_WHAT = {"color": "color", "emoji": "emoji", "change": "time"}


def rule_conflicts(lang: str = "en") -> list[dict]:
    """The rules' conflicts in words, each with what can be done about it (All Rules shows them)."""
    tr = lambda text, **kw: str(i18n.tr(lang, text, **kw))
    found, sids = all_rules(), source_ids()
    by_id = {r["id"]: r for r in found}
    out = []
    for c in rules_mod.conflicts(found, sids, set(ignored_conflicts())):
        a, b = rule_label(by_id[c["a"]], lang), rule_label(by_id[c["b"]], lang)
        where = "" if len(c["calendars"]) == len(sids) else " " + tr("(in {calendars})", calendars=", ".join(calendar_name(x) for x in c["calendars"]))
        if c["kind"] == "duplicate":
            text = tr("“{b}” is the same as “{a}”", a=a, b=b) + where + "."
            fixes = [("merge", tr("Merge them")), ("ignore", tr("Keep both"))]
        else:
            what = tr(CONFLICT_WHAT[c["action"]])
            text = tr("“{b}” never sets the {what}: “{a}” is above it and matches the same events", a=a, b=b, what=what) + where + "."
            fixes = [("up", tr("Put “{b}” first", b=b)), ("drop", tr("Take the {what} out of “{b}”", what=what, b=b)), ("ignore", tr("Keep as is"))]
        out.append({"key": rules_mod.conflict_key(c), "a": c["a"], "b": c["b"], "text": text, "fixes": fixes})
    return out


@app.post("/ui/section", dependencies=[Depends(gui_auth)])
async def set_section(csrf: str = Form(""), section: str = Form(""), open_: str = Form("", alias="open")):
    """Remember whether a status-page section is open (the page sends this when it's toggled)."""
    check_csrf(csrf)
    if section not in SECTIONS and not re.fullmatch(r"src:(ccs|[fl][0-9a-f]{6})|dest:(google|d[0-9a-f]{6})", section):
        raise HTTPException(400, "Unknown section.")
    saved = store.get("ui_sections") or {}
    saved[section] = open_ == "1"
    store.set("ui_sections", saved)
    return Response(status_code=204)


@app.post("/ui/lang", dependencies=[Depends(gui_auth)])
async def set_lang(csrf: str = Form(""), lang: str = Form("")):
    """Remember the status page's language (the language menu sends this); "auto" follows the browser."""
    check_csrf(csrf)
    if lang == "auto":
        store.delete("ui_lang")
    elif lang in i18n.LANGS:
        store.set("ui_lang", lang)
    else:
        raise HTTPException(400, "Unknown language.")
    return Response(status_code=204)


@app.post("/ui/clock", dependencies=[Depends(gui_auth)])
async def set_clock(csrf: str = Form(""), clock: str = Form("")):
    """Remember 12-hour / 24-hour times (the 12h / 24h switch above the calendar); "auto" follows the language."""
    check_csrf(csrf)
    if clock not in CLOCKS:
        raise HTTPException(400, "Unknown time format.")
    if clock == "auto":
        store.delete("ui_clock")
    else:
        store.set("ui_clock", clock)
    return Response(status_code=204)


@app.post("/ui/view", dependencies=[Depends(gui_auth)])
async def set_view(csrf: str = Form(""), view: str = Form("")):
    """Remember the calendar's view (month, week, day or list), chosen above the calendar."""
    check_csrf(csrf)
    if view not in VIEWS:
        raise HTTPException(400, "Unknown view.")
    store.set("ui_view", view)
    return Response(status_code=204)


@app.post("/ui/tz", dependencies=[Depends(gui_auth)])
async def set_display_tz(csrf: str = Form(""), tz: str = Form("")):
    """The time zone the calendar is shown in here; "" goes back to TZ from .env."""
    check_csrf(csrf)
    if not tz or tz == settings.timezone:
        store.delete("ui_tz")
    elif valid_zone(tz):
        store.set("ui_tz", tz)
    else:
        raise HTTPException(400, "Unknown time zone.")
    return Response(status_code=204)


PRINT_VIEWS = ("itinerary", "day", "5day", "week", "month")


def print_prefs() -> dict:
    """The last print's choices (Print Preview starts with them): view, weekends, theme; {} before the first."""
    saved = store.get("ui_print") or {}
    return {k: saved[k] for k in ("view", "weekends", "theme") if k in saved} if isinstance(saved, dict) else {}


@app.post("/ui/print", dependencies=[Depends(gui_auth)])
async def set_print(csrf: str = Form(""), view: str = Form(""), weekends: str = Form("1"), theme: str = Form("light")):
    check_csrf(csrf)
    store.set("ui_print", {"view": view if view in PRINT_VIEWS else "month", "weekends": weekends == "1",
                           "theme": "dark" if theme == "dark" else "light"})
    return {"ok": True}


def print_pages(events: list[Event], view: str, first: date, last: date, weekends: bool, lang: str) -> list[dict]:
    """The calendar from `first` to `last` as pages to print: a month, a week (Sunday to Saturday), five
    days (Monday to Friday) or a day per page, or one itinerary (the days with events)."""
    pages: list[dict] = []
    if view == "itinerary":
        days = []
        ref = first.replace(day=1)
        while ref <= last:
            days += [d for d in cal_view(events, "list", ref, lang)["days"] if first <= d["date"] <= last]
            ref = (ref.replace(day=28) + timedelta(days=4)).replace(day=1)
        days = [d for d in days if weekends or d["date"].weekday() < 5]
        return [{"view": view, "title": "", "days": days}]
    if view == "month":
        ref = first.replace(day=1)
        while ref <= last and len(pages) < 24:
            pages.append(cal_view(events, "month", ref, lang))
            ref = (ref.replace(day=28) + timedelta(days=4)).replace(day=1)
    elif view in ("week", "5day"):
        ref = first - timedelta(days=(first.weekday() + 1) % 7)
        while ref <= last and len(pages) < 60:
            pages.append(cal_view(events, "week", ref, lang))
            ref += timedelta(days=7)
    else:
        ref = first
        while ref <= last and len(pages) < 62:
            pages.append(cal_view(events, "day", ref, lang))
            ref += timedelta(days=1)
    # Sunday-first columns: 0 = Sunday … 6 = Saturday; five days are Monday to Friday
    keep = [1, 2, 3, 4, 5] if view == "5day" or (view in ("week", "month") and not weekends) else list(range(7))
    for p in pages:
        p["dow"] = [p["dow"][i] for i in keep]
        p["weeks"] = [[w[i] for i in keep] for w in p["weeks"]]
        p["cols"] = len(keep)
    return pages


@app.get("/print", dependencies=[Depends(gui_auth)])
def print_page(request: Request, view: str = "", start: str = "", end: str = "", weekends: str = "",
               theme: str = "", all_: str = Query("", alias="all")):
    """Print Preview's page: the calendar as chosen, ready to print (the preview shows it in a frame)."""
    prefs = print_prefs()
    view = view if view in PRINT_VIEWS else prefs.get("view") or {"list": "itinerary"}.get(ui_view(), ui_view())
    today = now().astimezone(display_tz()).date()
    first = _parse_day(start, None) if start else today.replace(day=1)
    last = _parse_day(end, None) if end else first.replace(day=pycal.monthrange(first.year, first.month)[1])
    if all_ == "1":       # All (0.2.8-beta.15): from the first event to the last (up to two years)
        days = sorted(_span(e, TZ)[0] for e in store.load_events() if not e.hidden)
        first, last = (days[0], days[-1]) if days else (first, last)
    if last < first:
        first, last = last, first
    last = min(last, first + timedelta(days=731))
    lang = lang_for(request)
    weekends_on = weekends == "1" if weekends else prefs.get("weekends", True)
    return page(request, "print.html", {
        "pages": print_pages(store.load_events(), view, first, last, weekends_on, lang), "view": view,
        "first": first, "last": last, "print_theme": theme if theme in ("light", "dark") else prefs.get("theme", "light"),
        "src_names": {sid: calendar_name(sid) for sid in source_ids()}}, lang=lang)


@app.post("/ui/theme", dependencies=[Depends(gui_auth)])
async def set_theme(csrf: str = Form(""), theme: str = Form("")):
    """Remember the light / dark / system choice (the page sends this when it's changed)."""
    check_csrf(csrf)
    if theme not in THEMES:
        raise HTTPException(400, "Unknown theme.")
    store.set("ui_theme", theme)
    return Response(status_code=204)


def linked_titles() -> dict[str, str]:
    """{event ID: the title of the event it's linked to}, for the calendar's event details."""
    out = {}
    for uid, link in event_links().items():
        other = store.get_event(link["to"])
        if other:
            out[uid] = other.title
    return out


def invite_view(request: Request, did: str, lang: str) -> dict:
    for token, v in _invites().items():
        if v["did"] == did:
            until = datetime.fromtimestamp(v["expires"], tz=TZ)
            return {"url": f"{base_url(request)}/invite/{token}", "until": dates_for(lang).short(until.date())}
    return {}
