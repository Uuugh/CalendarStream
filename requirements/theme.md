# Requirements: theme

How the app looks: colors, fonts, icons, corners and sizes, in a light and a dark palette. Every component uses this theme by default; a row elsewhere states a look only to depart from it. Components, and what they do, are in `common.md`. Values are written here once and no other file repeats them. Converted from `build_rules/theme.md` (the legacy file, kept only as the oracle until the product built from these rows exists).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| THM-01 | proposed | All text uses one font family; text that is typed or copied exactly uses a monospace family; sizes and weights follow the text styles below. | — | theme.md section 1 |
| THM-01.a |  | IBM Plex Sans is the font for everything. | — | theme.md section 1; picture 2·1 |
| THM-01.b |  | IBM Plex Mono is used only for what is typed or copied exactly: links, IDs, the Username, the client ID and the stream name. | — | theme.md section 1; picture 2·1 |
| THM-01.c |  | The module kind is 17 px at weight 700 (15 px in a phone-width window, DEF-01). | — | theme.md section 1 |
| THM-01.d |  | Default text is 14 px; labels are weight 600; notes are 13 px in the muted color. | — | theme.md section 1 |
| THM-02 | proposed | Every color is a named token with a light value and a dark value. The light palette is the Soft palette. The event colors that a user picks are not in this theme; they are the shared color palette (UI-10). | — | theme.md section 2; picture 2·2 |
| THM-02.a |  | bg is the page: light #f7f6f3, dark #0f1218. | — | theme.md section 2 |
| THM-02.b |  | card is sections, modules and pop-ups, and the words on a filled button: light #fdfcfa, dark #171b23. | — | theme.md section 2 |
| THM-02.c |  | soft is quiet fills (instruction tiles, hover): light #f1efeb, dark #1d222c. | — | theme.md section 2 |
| THM-02.d |  | line is every border and divider: light #e8e4de, dark #2a303b. | — | theme.md section 2 |
| THM-02.e |  | text is the text color: light #2b2f36, dark #e6e8ec. muted is labels, notes and status lines: light #626c7c, dark #98a2b3. | — | theme.md section 2 |
| THM-02.f |  | Muted text reaches a contrast of 4.5:1 against card, bg and soft in both palettes. | — | theme.md section 2 |
| THM-02.g |  | accent is for pressable buttons only: light #40609c, dark #93b4ff; the text on it (onaccent) is light #ffffff, dark #0f1218. | — | theme.md section 2 |
| THM-02.h |  | ok (green: done, OK) is light #2f7d62 on #eef5f0, dark #4ade80 on #0f2a20 (the second color is okbg, its background). | — | theme.md section 2 |
| THM-02.i |  | run (pressed: in action, or waiting on you) is light #40609c on #eef1f7, dark #93b4ff on #14203d (runbg). | — | theme.md section 2 |
| THM-02.j |  | warn (amber: a problem outside CalendarStream) is light #946a24 on #faf3e6, dark #fbbf24 on #2b2110 (warnbg). | — | theme.md section 2 |
| THM-02.k |  | bad (red: CalendarStream itself failed) is light #b4483c on #faeeeb, dark #f87171 on #2d1414 (badbg). | — | theme.md section 2 |
| THM-02.l |  | Each section has its own border color, shown as 35% of the color mixed with line, on card: Calendar slate blue #5b6f9a, Calendars teal #2a9d8f, Feeds clear blue #2f86c8, All Rules lavender #9b8ad6, Event Templates copper #b8733a, History grey #8a8f98. | — | theme.md section 2 |
| THM-02.m |  | The title's two words use the logo colors: Calendar is navy #0b1f44 in light and #e6e8ec in dark; Stream is #1a8cff in light and #4aa8ff in dark. | — | theme.md section 2 |
| THM-03 | proposed | Icons are one family in one style, in the text color. | — | theme.md section 3; picture 2·3 |
| THM-03.a |  | The icon family is Material Symbols Rounded at weight 400. | — | theme.md section 3 |
| THM-03.b |  | Icons are 13 to 24 px. Adding an icon does not change an existing one. | — | theme.md section 3 |
| THM-04 | proposed | Corners are rounded rectangles, never pills, and components have the sizes below; every border is 1 px. | — | theme.md section 4; picture 2·4 |
| THM-04.a |  | Controls have 8 px corners. Sections, modules, pop-ups and menus have 12 px corners. Small marks (a color, today, a switch) have 4 to 6 px corners. | — | theme.md section 4 |
| THM-04.b |  | Module headers are 50 px high; controls (fields and buttons) are 34 px high. | — | theme.md section 4 |
| THM-04.c |  | Status/Action buttons are 132 × 50 px. Cancel/Save buttons are 130 × 34 px. | — | theme.md section 4 |
| THM-04.d |  | Icon buttons are 34 × 34 px in the general toolbar and 28 × 28 px in the compact calendar toolbar. | — | theme.md sections 1 and 5 |
| THM-04.e |  | Every border is 1 px. The two 2 px lines are today's day in the calendar and the focus outline. | — | theme.md section 4 |

Dart note: THM-01 becomes the text theme, THM-02 the color scheme plus an extension for the status colors (ok, run, warn, bad), THM-03 the icon theme, THM-04 the shapes and the component themes.

Conversion progress (temporary): sections 1 to 4 of the legacy file are converted. To convert: sections 5 to 16 and the Clarifications.
