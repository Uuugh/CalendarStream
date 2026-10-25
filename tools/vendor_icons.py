"""Copy the Material Symbols the app uses into app/material_symbols/symbols.json.

The page draws its icons inline (no icon font and nothing fetched from Google), so only the path of
each icon is kept. To add one: put its name in NAMES, then run

    npm install @material-symbols/svg-400
    python tools/vendor_icons.py node_modules/@material-symbols/svg-400

Names come from https://fonts.google.com/icons (style Rounded, weight 400); "-fill" is the filled form.
"""

import json
import re
import sys
from pathlib import Path

NAMES = [
    "add", "arrow_drop_down", "arrow_right", "bolt", "calendar_month", "cancel", "check", "check_circle",
    "chevron_left", "chevron_right", "close", "content_copy", "contrast", "dark_mode", "delete", "edit",
    "error", "event_note", "help", "history", "info", "keep", "keep-fill", "language", "light_mode",
    "location_on", "menu", "print", "progress_activity", "radio_button_unchecked", "rule", "sensors",
    "subdirectory_arrow_right", "sync", "visibility", "visibility_off", "warning",
]


def main(package: str) -> None:
    out = {}
    for name in NAMES:
        svg = (Path(package) / "rounded" / f"{name}.svg").read_text(encoding="utf-8")
        paths = re.findall(r'<path d="([^"]+)"', svg)
        if len(paths) != 1 or 'viewBox="0 -960 960 960"' not in svg:
            raise SystemExit(f"{name}: unexpected SVG")
        out[name] = paths[0]
    target = Path(__file__).resolve().parent.parent / "app" / "material_symbols" / "symbols.json"
    target.write_text(json.dumps(out, indent=0, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(out)} icons → {target}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "node_modules/@material-symbols/svg-400")
