"""Material Symbols (Rounded, weight 400; Apache License 2.0) drawn inline as SVG.

Only the icons in material_symbols/symbols.json are available; tools/vendor_icons.py adds more. `sprite()`
puts every icon in a page once; `svg()` draws one by pointing at it; `mask()` gives a CSS url() for icons
drawn by stylesheets.
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
    """An icon in the text color, hidden from screen readers (its button has the label). It points at
    the page's sprite (see sprite()), so each icon's drawing is in the page once."""
    path(name)              # an unknown name fails here, not as an empty square in the page
    classes = f"mi {cls}".strip()
    # No viewBox here: the symbol has it, and fills the box (whatever size CSS gives it)
    return Markup(f'<svg class="{escape(classes)}" width="{size}" height="{size}" fill="currentColor" aria-hidden="true" '
                  f'focusable="false"><use href="#mi-{name}" width="100%" height="100%"/></svg>')


def sprite() -> Markup:
    """Every icon once, for svg() to point at: put it at the top of a page's <body>. (Not display:none:
    browsers don't draw symbols from an SVG that isn't displayed.)"""
    symbols = "".join(f'<symbol id="mi-{n}" viewBox="{_VIEWBOX}"><path d="{d}"/></symbol>' for n, d in sorted(_paths().items()))
    return Markup(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_VIEWBOX}" width="0" height="0" style="position:absolute;overflow:hidden" aria-hidden="true">{symbols}</svg>')


def mask(name: str) -> Markup:
    """A CSS url() of the icon, for `mask-image` (an icon a stylesheet draws, e.g. before a list item).
    Safe to put in a <style> as it is: the SVG is percent-encoded."""
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_VIEWBOX}"><path d="{path(name)}"/></svg>'
    return Markup(f'url("data:image/svg+xml,{quote(doc)}")')
