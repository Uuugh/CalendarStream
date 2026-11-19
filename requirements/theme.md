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
| THM-05 | proposed | Buttons share one look, and a status has one look per meaning. | — | theme.md sections 5 to 7 |
| THM-05.a |  | An icon button's icon is the muted color, with soft behind it on hover. | — | theme.md section 5 |
| THM-05.b |  | Every pressable button uses the accent look: accent fill and onaccent words. Accent is never used for a status. | — | theme.md section 6 |
| THM-05.c |  | A disabled Cancel \| Save pair is greyed and faded. The pulse of a first change is the pressed look. | — | theme.md section 6 |
| THM-05.d |  | Done or OK is green: ok words on okbg; a done button fills ok. | — | theme.md section 7 |
| THM-05.e |  | In action, or waiting on the user, is pressed: run words on runbg; a working button is card with run words. | — | theme.md section 7 |
| THM-05.f |  | A problem outside CalendarStream (United, Google, GitHub, the internet), or an entry that was refused, is amber: warn words on warnbg; a failed button fills warn. | — | theme.md section 7 |
| THM-05.g |  | CalendarStream itself failing is red: bad words on badbg; a failed button fills bad. | — | theme.md section 7 |
| THM-06 | proposed | Every change of state moves as the rows below say. When reduced motion is requested nothing slides, grows, fades, spins or pulses: each state replaces the last, with the same words and hold times. | — | theme.md section 8; picture 2·8 |
| THM-06.a |  | A pop-up opens with a fade and a scale from 0.96 to 1 in 0.2 s ease-out; its backdrop (black at 55%, the page blurred 2 px) fades in. | — | theme.md sections 8 and 11 |
| THM-06.b |  | The color box and the emoji list open at once, with no motion. | — | theme.md section 8 |
| THM-06.c |  | The pressed side of a Cancel \| Save pair grows over the pair and fades its words in 0.3 s ease; Cancel takes 1 s, in and back. Save pulses in the pressed look once a second, five times, in 1 s ease-out. | — | theme.md section 8 |
| THM-06.d |  | A good status word shrinks to its ✓ in 0.5 s ease. A ✓ saved in place fades in in 0.45 s ease (messages 0.3 s). | — | theme.md section 8 |
| THM-06.e |  | The triangles of Expand and Close turn in 0.15 s; Close points up. | — | theme.md section 8 |
| THM-06.f |  | A Status/Action button grows from the bottom 22 px to the whole box in 0.25 s ease while its chip fades out in 0.2 s; its working words fade in in 0.25 s ease-out beside an icon that turns once a second, linear. | — | theme.md section 7 |
| THM-06.g |  | A done, failed or found result fills the button with its status color and a ring pulses out from 0 to 9 px, twice, in 1.1 s ease-out each. | — | theme.md section 7 |
| THM-06.h |  | After its hold the button shrinks to the bottom in 0.25 s ease; then the new status word fades in, 0.2 s after a 0.25 s delay, never through the old word. | — | theme.md section 7 |
| THM-06.i |  | The words of the top-bar Update now fade in in 0.25 s ease-out; the bar under them slides in 1.2 s ease-in-out, repeating. | — | theme.md section 7 |
| THM-07 | proposed | Spacing between content parts uses one set of values. Internal control geometry, calendar cells and anchored header layouts use the component sizes (THM-04), not these. | — | theme.md section 9 (Spacing) |
| THM-07.a |  | There are 5 px between parts: sections, modules, the parts of a module or a dialog, and buttons in a row. | — | theme.md section 9 |
| THM-07.b |  | There is 1 px between a label and its field (the label over it); From and To beside their dates have 5 px. | — | theme.md section 9 |
| THM-07.c |  | Inside a module's border there are 9 px at the sides and 5 px at the top and bottom, the 50 px header unchanged; a box inside a module (Include, an instruction tile) is 5 px by 9 px. The bottom padding is the same folded and open: 5 px in a module, 18 px in a module-like section. | — | theme.md section 9 |
| THM-07.d |  | Inside every dialog there are 12 px, and the panels of anchored menus have 12 px padding and corners. | — | theme.md sections 9 and 11 |
| THM-07.e |  | A folded section keeps 14 px below it for the Expand line in its border. A module's Close line has 2 px less above and below it. | — | theme.md section 9 |
| THM-07.f |  | The calendar key starts 5 px below the calendar. The header's date and navigation gaps are 8 px, tool gaps 5 px, and the wrapped second row has a 6 px gap. | — | theme.md section 9 |
| THM-08 | proposed | A module's border is its calendar's or feed's color at 45%, its header a 6% tint and the rest a 3% tint of it, in light and dark. Each section has its own border color (THM-02.l) on card. | — | theme.md section 9; picture 2·9 |
| THM-08.a |  | A dialog has 12 px corners; in a phone-width window it fills the screen with square, edge-to-edge corners. | — | theme.md section 11 |
| THM-08.b |  | The grip of a handle is two columns of three faint dots, centered on the module's 50 px header or on the rule line. | — | theme.md section 10 |
| THM-08.c |  | The (?) icon is 15 px, raised after the word it explains. | — | theme.md section 12 |
| THM-09 | proposed | The event color palette (UI-10) is Google Calendar's eleven colors. | — | theme.md section 11 (Color box) |
| THM-09.a |  | Tomato #d50000, Flamingo #e67c73, Tangerine #f4511e, Banana #f6bf26, Sage #33b679, Basil #0b8043, Peacock #039be5, Blueberry #3f51b5, Lavender #7986cb, Grape #8e24aa, Graphite #616161. | — | theme.md section 11; picture 2·11 |

Dart note: THM-01 becomes the text theme, THM-02 the color scheme plus an extension for the status colors (ok, run, warn, bad), THM-03 the icon theme, THM-04 the shapes and the component themes.

Conversion progress (temporary): sections 1 to 14 of the legacy file are converted. To convert: section 15 (a deleted event, and the History table: to events.md and history.md in their passes), section 16 and the Clarifications (the event pop-up layout and the detailed decisions). The flows in section 7 (the words each Status/Action button says, in order, and the Remove-a-calendar and Import flows) go into their features: Sync Now (SRC-31), Check now (SET-20), Update now (SET-31), Connect (GGL), Remove a calendar and Import (SRC).
