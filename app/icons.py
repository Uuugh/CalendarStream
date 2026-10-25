"""Material Symbols (Rounded, weight 400; Apache License 2.0) drawn inline as SVG.

Only the icons in material_symbols/symbols.json are available; tools/vendor_icons.py adds more. Nothing
here depends on the web page: `svg()` gives markup, `mask()` a CSS url() for icons drawn by stylesheets.
"""

import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

from markupsafe import Markup, escape

_FILE = Path(__file__).parent / "material_symbols" / "symbols.json"
_VIEWBOX = "0 -960 960 960"


@lru_cache(maxsize=1)
def _paths() -> dict[str, str]:
    return json.loads(_FILE.read_text(encoding="utf-8"))


def path(name: str) -> str:
    """The SVG path of an icon (KeyError for one that isn't vendored, so a typo shows up in tests)."""
    return _paths()[name]


def svg(name: str, size: int = 18, cls: str = "") -> Markup:
    """An icon as inline SVG in the text color, hidden from screen readers (its button has the label)."""
    classes = f"mi {cls}".strip()
    return Markup(f'<svg class="{escape(classes)}" width="{size}" height="{size}" viewBox="{_VIEWBOX}" '
                  f'fill="currentColor" aria-hidden="true" focusable="false"><path d="{path(name)}"/></svg>')


def mask(name: str) -> Markup:
    """A CSS url() of the icon, for `mask-image` (an icon a stylesheet draws, e.g. before a list item).
    Safe to put in a <style> as it is: the SVG is percent-encoded."""
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_VIEWBOX}"><path d="{path(name)}"/></svg>'
    return Markup(f'url("data:image/svg+xml,{quote(doc)}")')
