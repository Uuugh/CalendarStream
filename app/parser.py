"""Turn whatever the schedule page returned into a list of events.

Two strategies, tried in order:
  1. JSON captured from the page's own API calls (most reliable when present).
  2. HTML tables/rows containing dates and times.

Because the page is behind a login, these heuristics were written without seeing
its exact markup. If events come out wrong, look at /data/debug/ (or the GUI's
debug links) and adjust FIELD_HINTS or parse_html below.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from dateutil import parser as dtparse


@dataclass
class Event:
    title: str
    start: str            # ISO datetime, or ISO date for all-day
    end: str
    all_day: bool = False
    location: str = ""
    description: str = ""

    @property
    def uid(self) -> str:
        return hashlib.sha1(f"{self.start}|{self.title}".encode()).hexdigest() + "@ccs-calendar"

    def to_dict(self):
        d = asdict(self)
        d["uid"] = self.uid
        return d


@dataclass
class Defaults:
    """How to handle items that have a start time but no end time."""
    mode: str = "hours"     # "hours" -> timed event of `hours` length; "allday" -> all-day event
    hours: float = 1.0


def _open_ended(title: str, start: datetime, d: Defaults, **kw) -> Event:
    if d.mode == "allday":
        day = start.date()
        note = f"Start: {start.strftime('%H:%M')}"
        kw["description"] = f"{note}\n{kw.get('description', '')}".strip()
        return Event(title, day.isoformat(), (day + timedelta(days=1)).isoformat(), all_day=True, **kw)
    return Event(title, start.isoformat(), (start + timedelta(hours=d.hours)).isoformat(), **kw)


FIELD_HINTS = {
    "start": ["starttime", "startdatetime", "start", "begin", "begintime", "reporttime", "report",
              "dutystart", "departuretime", "departure", "deptime", "std", "startdate", "date"],
    "end": ["endtime", "enddatetime", "end", "releasetime", "release", "dutyend", "arrivaltime",
            "arrival", "arrtime", "sta", "enddate"],
    "title": ["title", "subject", "pairing", "pairingnumber", "tripnumber", "trip", "flightnumber",
              "flight", "activity", "activitycode", "code", "type", "name", "description"],
    "origin": ["origin", "departurestation", "depstation", "from", "startstation"],
    "dest": ["destination", "arrivalstation", "arrstation", "to", "endstation"],
    "location": ["location", "layover", "station", "hotel"],
}


def _norm(k: str) -> str:
    return re.sub(r"[^a-z]", "", k.lower())


def _pick(d: dict, kind: str):
    keys = {_norm(k): k for k in d}
    for hint in FIELD_HINTS[kind]:
        if hint in keys and d[keys[hint]] not in (None, "", [], {}):
            return d[keys[hint]]
    return None


def _to_dt(value, tz: ZoneInfo):
    if value is None or isinstance(value, (dict, list, bool)):
        return None
    try:
        if isinstance(value, (int, float)):  # epoch seconds or ms
            v = value / 1000 if value > 1e11 else value
            if v < 1e9:
                return None
            return datetime.fromtimestamp(v, tz)
        s = str(value).strip()
        if not re.search(r"\d", s) or len(s) < 6:
            return None
        dt = dtparse.parse(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=tz)
    except (ValueError, OverflowError, TypeError):
        return None


def parse_json(payloads: list, tz: ZoneInfo, defaults: Defaults) -> list[Event]:
    events: list[Event] = []

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
        elif isinstance(node, dict):
            start = _to_dt(_pick(node, "start"), tz)
            title = _pick(node, "title")
            if start and title and not isinstance(title, (dict, list)):
                end = _to_dt(_pick(node, "end"), tz)
                if end and end < start:
                    end += timedelta(days=1)
                orig, dest = _pick(node, "origin"), _pick(node, "dest")
                loc = _pick(node, "location")
                location = f"{orig} → {dest}" if orig and dest else str(loc or orig or "")
                desc = "\n".join(f"{k}: {v}" for k, v in node.items()
                                 if not isinstance(v, (dict, list)) and v not in (None, ""))
                title = f"Trip {title}" if str(title).isdigit() else str(title)
                if end:
                    events.append(Event(title, start.isoformat(), end.isoformat(),
                                        location=location, description=desc[:2000]))
                else:
                    events.append(_open_ended(title, start, defaults, location=location, description=desc[:2000]))
            for v in node.values():
                if isinstance(v, (dict, list)):
                    walk(v)

    for p in payloads:
        walk(p.get("data"))
    return events


# --- HTML fallback ---------------------------------------------------------

MONTHS = "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC"
DATE_RES = [
    re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"),                                   # 2026-10-19
    re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b"),                              # 10/19/2026
    re.compile(rf"\b(\d{{1,2}})\s?({MONTHS})[a-z]*\s?(\d{{2,4}})?\b", re.I),       # 19OCT / 19 Oct 26
    re.compile(rf"\b({MONTHS})[a-z]*\.?\s(\d{{1,2}}),?\s?(\d{{4}})?\b", re.I),     # Oct 19, 2026
]
TIME_RE = re.compile(r"\b([01]?\d|2[0-3]):?([0-5]\d)\b(?!\s?/)")
MON_IDX = {m: i + 1 for i, m in enumerate(MONTHS.split("|"))}


def _infer_year(month: int, day: int) -> int:
    today = date.today()
    cands = [date(y, month, day) for y in (today.year - 1, today.year, today.year + 1)
             if _valid(y, month, day)]
    return min(cands, key=lambda d: abs((d - today).days)).year if cands else today.year


def _valid(y, m, d):
    try:
        date(y, m, d)
        return True
    except ValueError:
        return False


def _find_date(text: str):
    for i, rx in enumerate(DATE_RES):
        m = rx.search(text)
        if not m:
            continue
        try:
            if i == 0:
                y, mo, d = int(m[1]), int(m[2]), int(m[3])
            elif i == 1:
                mo, d, y = int(m[1]), int(m[2]), int(m[3])
                y += 2000 if y < 100 else 0
            elif i == 2:
                d, mo = int(m[1]), MON_IDX[m[2][:3].upper()]
                y = int(m[3]) if m[3] else _infer_year(mo, d)
                y += 2000 if y < 100 else 0
            else:
                mo, d = MON_IDX[m[1][:3].upper()], int(m[2])
                y = int(m[3]) if m[3] else _infer_year(mo, d)
            if _valid(y, mo, d):
                return date(y, mo, d), m.span()
        except (KeyError, ValueError):
            continue
    return None, None


def parse_html(html: str, tz: ZoneInfo, defaults: Defaults) -> list[Event]:
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()

    rows = soup.select("tr") or soup.select("[class*=event i], [class*=duty i], [class*=trip i], li")
    events: list[Event] = []
    current_day = None

    for row in rows:
        cells = [c.get_text(" ", strip=True) for c in (row.find_all(["td", "th"]) or [row])]
        text = " | ".join(c for c in cells if c)
        if not text or len(text) > 600:
            continue
        day, span = _find_date(text)
        if day:
            current_day = day
            rest = text[:span[0]] + text[span[1]:]
        elif current_day:
            rest = text  # continuation row under a date heading
        else:
            continue

        times = [(int(h), int(m)) for h, m in TIME_RE.findall(rest)]
        title = re.sub(r"\s*\|\s*", " · ", TIME_RE.sub("", rest)).strip(" ·-")
        title = re.sub(r"(\s·\s)+", " · ", title)
        if not title or not re.search(r"[A-Za-z0-9]", title):
            continue

        if times:
            start = datetime(current_day.year, current_day.month, current_day.day, *times[0], tzinfo=tz)
            if len(times) > 1:
                end = datetime(current_day.year, current_day.month, current_day.day, *times[-1], tzinfo=tz)
                if end <= start:
                    end += timedelta(days=1)
                events.append(Event(title[:200], start.isoformat(), end.isoformat(), description=text))
            else:
                events.append(_open_ended(title[:200], start, defaults, description=text))
        elif day:
            events.append(Event(title[:200], current_day.isoformat(),
                                (current_day + timedelta(days=1)).isoformat(), all_day=True, description=text))
    return events


def extract_events(html: str, payloads: list, tz_name: str, defaults: Defaults) -> tuple[list[Event], str]:
    tz = ZoneInfo(tz_name)
    events = parse_json(payloads, tz, defaults)
    source = "json"
    if not events:
        events = parse_html(html, tz, defaults)
        source = "html"
    # de-duplicate
    seen, unique = set(), []
    for e in sorted(events, key=lambda e: e.start):
        if e.uid not in seen:
            seen.add(e.uid)
            unique.append(e)
    return unique, source
