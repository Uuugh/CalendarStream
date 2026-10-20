"""Languages for the status page: English plus the translations in app/locales/<code>.json.

Each catalog maps an English text to its translation. Texts in the pages are looked up as they
are (`tr`). Messages made in Python (status, activity log, errors) stay in English in the database
and are translated when shown (`message`): a catalog entry like "Download failed: {error}" matches
the English message, and the parts in braces are translated in turn when they are messages too.
Anything without a translation is shown in English.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

from markupsafe import Markup

LANGS = {"en": "English", "es": "Español", "fr": "Français", "de": "Deutsch", "pt": "Português", "nl": "Vlaams"}
HTML_LANG = {"en": "en", "es": "es", "fr": "fr", "de": "de", "pt": "pt-BR", "nl": "nl-BE"}

_DIR = Path(__file__).parent / "locales"
CATALOGS: dict[str, dict[str, str]] = {
    code: json.loads((_DIR / f"{code}.json").read_text(encoding="utf-8")) for code in LANGS if code != "en"}


def pick(saved: str | None, accept_language: str = "") -> str:
    """The language to show: the one chosen on the status page, else the browser's, else English."""
    if saved in LANGS:
        return saved
    for part in (accept_language or "").split(","):
        code = part.split(";")[0].strip().lower()[:2]
        if code in LANGS:
            return code
    return "en"


def tr(lang: str, text: str, **params) -> Markup:
    """Translate a page text. Texts come from the templates (trusted, may hold simple HTML);
    the values put into {placeholders} are escaped."""
    found = CATALOGS[lang].get(text, text) if lang in CATALOGS else text
    return Markup(found).format(**params) if params else Markup(found)


# --- Messages made in Python ---------------------------------------------------------

def _compile(key: str) -> re.Pattern:
    """A regular expression matching the English message a key describes. Placeholders named n,
    n2… match numbers only; the others match any text."""
    parts = re.split(r"\{(\w+)\}", key)
    rx = "".join(re.escape(p) if i % 2 == 0 else (f"(?P<{p}>\\d+)" if re.fullmatch(r"n\d*", p) else f"(?P<{p}>.+?)")
                 for i, p in enumerate(parts))
    return re.compile(f"^{rx}$", re.S)


# Keys with placeholders, most specific (longest fixed text) first.
_PATTERNS = sorted(((k, _compile(k)) for k in (CATALOGS.get("es") or {}) if "{" in k),
                   key=lambda kp: -len(re.sub(r"\{\w+\}", "", kp[0])))


def message(lang: str, text: str) -> str:
    """Translate a message made in Python (plain text; escaped by the template)."""
    if lang not in CATALOGS or not text:
        return text
    return _message(CATALOGS[lang], str(text), 0)


def _message(cat: dict, text: str, depth: int) -> str:
    if text in cat:
        return cat[text]
    for key, rx in _PATTERNS:
        m = rx.match(text)
        if m and key in cat:
            params = {k: _part(cat, v, depth) for k, v in m.groupdict().items()}
            try:
                return cat[key].format(**params)
            except (KeyError, IndexError, ValueError):
                return text
    return text


def _part(cat: dict, value: str, depth: int) -> str:
    """A value inside a message: translated if it's a message itself, or a list of them."""
    if depth > 4:
        return value
    done = _message(cat, value, depth + 1)
    if done != value:
        return done
    for sep in ("; ", ", "):
        if sep in value:
            parts = value.split(sep)
            new = [_message(cat, p, depth + 1) for p in parts]
            if new != parts:
                return sep.join(new)
    return value


# --- Dates ------------------------------------------------------------------------------

DATES = {
    "en": {"months": "January February March April May June July August September October November December",
           "mon": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec",
           "wd": "Mon Tue Wed Thu Fri Sat Sun", "dow": "Su Mo Tu We Th Fr Sa",
           "day": "{wd} {mon} {d}", "short": "{mon} {dd}", "title": "{month} {y}"},
    "es": {"months": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre",
           "mon": "ene feb mar abr may jun jul ago sept oct nov dic",
           "wd": "lun mar mié jue vie sáb dom", "dow": "Do Lu Ma Mi Ju Vi Sá",
           "day": "{wd} {d} {mon}", "short": "{dd} {mon}", "title": "{month} de {y}"},
    "fr": {"months": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre",
           "mon": "janv. févr. mars avr. mai juin juil. août sept. oct. nov. déc.",
           "wd": "lun. mar. mer. jeu. ven. sam. dim.", "dow": "Di Lu Ma Me Je Ve Sa",
           "day": "{wd} {d} {mon}", "short": "{dd} {mon}", "title": "{month} {y}"},
    "de": {"months": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember",
           "mon": "Jan. Feb. März Apr. Mai Juni Juli Aug. Sept. Okt. Nov. Dez.",
           "wd": "Mo. Di. Mi. Do. Fr. Sa. So.", "dow": "So Mo Di Mi Do Fr Sa",
           "day": "{wd} {d}. {mon}", "short": "{dd}. {mon}", "title": "{month} {y}"},
    "pt": {"months": "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro",
           "mon": "jan. fev. mar. abr. mai. jun. jul. ago. set. out. nov. dez.",
           "wd": "seg. ter. qua. qui. sex. sáb. dom.", "dow": "Dom Seg Ter Qua Qui Sex Sáb",
           "day": "{wd} {d} {mon}", "short": "{dd} {mon}", "title": "{month} de {y}"},
    "nl": {"months": "januari februari maart april mei juni juli augustus september oktober november december",
           "mon": "jan. feb. mrt. apr. mei jun. jul. aug. sep. okt. nov. dec.",
           "wd": "ma di wo do vr za zo", "dow": "zo ma di wo do vr za",
           "day": "{wd} {d} {mon}", "short": "{dd} {mon}", "title": "{month} {y}"},
}


class Dates:
    """Day and month names in one language."""

    def __init__(self, lang: str):
        t = DATES.get(lang, DATES["en"])
        self.months, self.mon, self.wd = t["months"].split(), t["mon"].split(), t["wd"].split()
        self.dow = t["dow"].split()                     # Sunday first, like CCS+
        self._day, self._short, self._title = t["day"], t["short"], t["title"]

    def day(self, d: date) -> str:
        """Weekday, day and month: "Mon Oct 5", "lun 5 oct"."""
        return self._day.format(wd=self.wd[d.weekday()], mon=self.mon[d.month - 1], d=d.day)

    def short(self, d: date) -> str:
        """Day and month: "Oct 05", "05 oct"."""
        return self._short.format(mon=self.mon[d.month - 1], dd=f"{d.day:02d}")

    def title(self, d: date) -> str:
        """Month and year, capitalised: "October 2026", "Octubre de 2026"."""
        text = self._title.format(month=self.months[d.month - 1], y=d.year)
        return text[:1].upper() + text[1:]

    def when(self, dt: datetime, today: date, seconds: bool = False) -> str:
        """A time, with the date unless it's today: "15:42" or "Oct 19, 15:42"."""
        clock = f"{dt:%H:%M:%S}" if seconds else f"{dt:%H:%M}"
        return clock if dt.date() == today else f"{self.short(dt.date())}, {clock}"
