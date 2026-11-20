"""Holds: calendar view.
Depends on: app/calendars/event.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from ..calendars.event import Event
from zoneinfo import ZoneInfo
import calendar as pycal
import re
from datetime import date, datetime, timedelta


def _span(
    e: Event, tz: ZoneInfo | None, *, Event, display_tz
) -> tuple[date, date, datetime | None, datetime | None]:
    """First and last calendar day an event covers (in `tz`, by default the display time zone)."""
    tz = tz or display_tz()
    if e.all_day:
        first, end = date.fromisoformat(e.start[:10]), date.fromisoformat(e.end[:10])
        return first, max(first, end - timedelta(days=1)), None, None
    s = datetime.fromisoformat(e.start).astimezone(tz)
    t = datetime.fromisoformat(e.end).astimezone(tz)
    last = (t - timedelta(microseconds=1)).date() if t > s else s.date()
    return s.date(), last, s, t


def _hidden_by(e: Event, hide: set[str], *, Event) -> bool:
    """Is `e` one of the kinds the key has switched off (0.2.8-beta.29, F28)? A calendar ("src:<id>"), edited here,
    changed by United since ("stale"), hidden from Google ("hidden") or deleted ("deleted").
    """
    # (0.2.8-beta.31, I3) an event added here and deleted here is gone from the calendar at once ("we control the calendar");
    # it is still in History › Undo until that pops off. Events a source sent stay struck through (their own Restore).
    if (
        e.deleted
        and e.origin == "custom"
        and e.deleted.split("|")[0] == "calendarstream"
    ):
        return True
    if not hide:
        return False
    return (
        f"src:{e.source}" in hide
        or ("deleted" in hide and bool(e.deleted))
        or (
            not e.deleted
            and (
                ("hidden" in hide and e.hidden)
                or ("stale" in hide and e.stale)
                or ("edited" in hide and e.edited and not e.stale)
            )
        )
    )


def cal_view(
    events: list[Event],
    view: str,
    ref: date,
    lang: str,
    pad: int,
    hide: set[str] | None,
    *,
    DEFAULT_COLOR,
    Event,
    _hidden_by,
    _lanes,
    _range_text,
    _span,
    calendar_color,
    dates_for,
    display_tz,
    i18n,
    now,
    source_ids,
) -> dict:
    """The calendar around `ref`: a month grid, one week, one day, or a list of a month's days
    with events. ‹ › move by a month, week or day. `pad` (full page, F27) adds that many weeks after and before
    the month's own (next month's first); `hide` is what the key has switched off (F28).
    """
    events = [e for e in events if not _hidden_by(e, hide or set())]
    tz = display_tz()
    dates = dates_for(lang)
    hm = dates.clock
    cont = str(i18n.tr(lang, "cont."))
    month_first = ref.replace(day=1)
    month_last = ref.replace(day=pycal.monthrange(ref.year, ref.month)[1])
    if view == "week":
        first_day = ref - timedelta(
            days=(ref.weekday() + 1) % 7
        )  # Sunday first, like CCS+
        last_day = first_day + timedelta(days=6)
        prev, nxt = ref - timedelta(days=7), ref + timedelta(days=7)
        title = f"{dates.day(first_day)} – {dates.day(last_day)}, {last_day.year}"
    elif view == "day":
        first_day = last_day = ref
        prev, nxt = ref - timedelta(days=1), ref + timedelta(days=1)
        title = f"{dates.day(ref)}, {ref.year}"
    else:  # month grid or list: the month's weeks / days
        weeks = pycal.Calendar(firstweekday=6).monthdatescalendar(ref.year, ref.month)
        first_day, last_day = (
            (weeks[0][0], weeks[-1][-1])
            if view == "month"
            else (month_first, month_last)
        )
        if view == "month" and pad:
            first_day, last_day = first_day - timedelta(
                days=7 * pad
            ), last_day + timedelta(days=7 * pad)
        prev = month_first - timedelta(days=1)
        nxt = month_last + timedelta(days=1)
        title = dates.title(ref)
    colors = {sid: calendar_color(sid) or DEFAULT_COLOR for sid in source_ids()}
    by_day: dict[date, list] = {}
    count = 0
    span_first, span_last = (
        (month_first, month_last)
        if view in ("month", "list")
        else (first_day, last_day)
    )
    for e in events:
        d0, d1, s, t = _span(e, tz)
        if d1 < first_day or d0 > last_day:
            continue
        if d1 >= span_first and d0 <= span_last:
            count += 1
        d = max(d0, first_day)
        while d <= min(d1, last_day):
            if s is None:
                when = "" if d == d0 else cont
            elif d0 == d1:
                when = f"{hm(s)}–{hm(t)}"
            elif d == d0:
                when = f"{hm(s)} →"
            elif d == d1:
                when = f"→ {hm(t)}"
            else:
                when = cont
            m0 = m1 = None
            if (
                s is not None
            ):  # minutes into this day, for the hourly grid (Week and Day)
                m0 = 0 if d > d0 else s.hour * 60 + s.minute
                m1 = (
                    1440
                    if d < d1
                    else min(
                        1440,
                        max(m0 + 15, t.hour * 60 + t.minute if t.date() == d else 1440),
                    )
                )
            by_day.setdefault(d, []).append(
                {
                    "e": e,
                    "when": when,
                    "first": d == d0,
                    "tag_color": e.color or e.rule_color,
                    "src_color": colors.get(e.source, ""),
                    "multi": d0 != d1,
                    "range": _range_text(e, s, t, lang),
                    "m0": m0,
                    "m1": m1,
                    "lane": 0,
                    "lanes": 1,
                }
            )
            d += timedelta(days=1)
    for items in by_day.values():
        _lanes(items)
    days = [
        first_day + timedelta(days=i) for i in range((last_day - first_day).days + 1)
    ]
    cell = lambda d: {
        "date": d,
        "in_month": d.month == ref.month,
        "items": by_day.get(d, []),
    }
    weeks_out = (
        [[cell(d) for d in days[i : i + 7]] for i in range(0, len(days), 7)]
        if view in ("month", "week")
        else []
    )
    # full page (F27): each added week says where it comes from, "n1" the first week after the month, "p1" the first before it…
    ext = [""] * len(weeks_out)
    if view == "month" and pad:
        for k in range(pad):
            ext[len(weeks_out) - 1 - k] = f"n{pad - k}"
            ext[k] = f"p{pad - k}"
    return {
        "view": view,
        "title": title,
        "dow": dates.dow,
        "ref": ref.isoformat(),
        "weeks": weeks_out,
        "week_ext": ext,
        "pad": pad,
        "hours": (
            [
                re.sub(r":00(?=[ap]m)", "", hm(datetime(2000, 1, 1, h)))
                for h in range(24)
            ]
            if view in ("week", "day")
            else []
        ),
        "days": (
            [cell(d) for d in days if view == "day" or by_day.get(d)]
            if view in ("day", "list")
            else []
        ),
        "prev": prev.isoformat(),
        "next": nxt.isoformat(),
        "month": f"{ref:%Y-%m}",
        "today": now().astimezone(tz).date(),
        "count": count,
    }


def month_view(
    events: list[Event], year: int, month: int, lang: str, *, Event, cal_view
) -> dict:
    """The month grid (kept for callers from before the other views)."""
    return cal_view(events, "month", date(year, month, 1), lang)


def _range_text(e: Event, s, t, lang: str, *, Event, dates_for, i18n) -> str:
    """When an event happens, e.g. "Mon Oct 5, 09:00–10:00" or "Mon Oct 5 – Wed Oct 7 (all day)"."""
    dates = dates_for(lang)
    day, hm = dates.day, dates.clock
    if s is None:
        a, b = date.fromisoformat(e.start[:10]), date.fromisoformat(
            e.end[:10]
        ) - timedelta(days=1)
        return (
            day(a)
            + ("" if a == b else f" – {day(b)}")
            + " "
            + str(i18n.tr(lang, "(all day)"))
        )
    if s.date() == t.date():
        return f"{day(s.date())}, {hm(s)}–{hm(t)}"
    return f"{day(s.date())} {hm(s)} – {day(t.date())} {hm(t)}"


def _parse_month(value: str | None, *, now) -> tuple[int, int]:
    try:
        y, m = map(int, (value or "").split("-"))
        if 2000 <= y <= 2100 and 1 <= m <= 12:
            return y, m
    except ValueError:
        pass
    today = now().date()
    return today.year, today.month
