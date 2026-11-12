"""Copy the Material Symbols the app uses into app/material_symbols/symbols.json.

The page draws its icons inline (no icon font and nothing fetched from Google), so only the path of
each icon is kept. To add one: put its name in NAMES, then run

    npm install @material-symbols/svg-400
    python tools/vendor_icons.py node_modules/@material-symbols/svg-400

Names come from https://fonts.google.com/icons (style Rounded, weight 400); "-fill" is the filled form.
STYLE_OVERRIDE sources a name from a different style folder instead (e.g. "outlined" for a hollow look,
used for F15.2's clock icon) - the vendored name still goes in NAMES, in the symbols.json key it's stored
under, not the on-disk filename it was read from.
"""

import json
import re
import sys
from pathlib import Path

NAMES = [
    "add", "alarm", "alarm_on", "arrow_back", "arrow_drop_down", "arrow_drop_up", "arrow_right", "bolt",
    "calendar_month", "cancel", "check", "check_circle", "chevron_left", "chevron_right", "close",
    "content_copy", "contrast", "dark_mode", "delete", "edit", "error", "event_note",
    "help", "history", "info", "language", "light_mode", "link", "link_off", "location_on", "menu", "print",
    "progress_activity", "radio_button_unchecked", "rule", "sensors", "subdirectory_arrow_right", "sync",
    "smart_toy", "checklist", "swap_horiz", "map", "search", "upgrade", "visibility", "visibility_off", "warning",
    "add_reaction", "undo", "redo", "upload_file", "download", "filter_list", "terminal", "logout",
    "send", "mail", "sms", "share", "fullscreen", "unfold_more", "filter_none", "public", "schedule",
    "view_week", "view_day", "view_list",   # 0.2.8-beta.33, F52: the Week/Day/List icons for the view picker
    "schedule_hollow",   # 0.2.8-beta.41, F15.2 rework: the 12 | 24 control's own hollow clock face
]

# name (as vendored) -> (style folder, on-disk file name without .svg). Omitted names come from "rounded".
STYLE_OVERRIDE = {
    "schedule_hollow": ("outlined", "schedule"),
}


def main(package: str) -> None:
    out = {}
    for name in NAMES:
        style, disk_name = STYLE_OVERRIDE.get(name, ("rounded", name))
        svg = (Path(package) / style / f"{disk_name}.svg").read_text(encoding="utf-8")
        paths = re.findall(r'<path d="([^"]+)"', svg)
        if len(paths) != 1 or 'viewBox="0 -960 960 960"' not in svg:
            raise SystemExit(f"{name}: unexpected SVG")
        out[name] = paths[0]
    target = Path(__file__).resolve().parent.parent / "app" / "material_symbols" / "symbols.json"
    target.write_text(json.dumps(out, indent=0, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(out)} icons → {target}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "node_modules/@material-symbols/svg-400")
