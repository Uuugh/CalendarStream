# Theme

Read before changing how the page looks. Written so anyone (the Developer, Claude, a Reviewer) can check
a change against it without asking: every look, status, transition and word rule is here, each with the
card of the **CalendarStream Theme Rules** picture that shows it.

- The picture: `build_rules/CalendarStream_Theme_Rules_Light.png` and `…_Dark.png`, drawn from the page
  itself (every size in it is measured). **Part 1** is the whole page with each part named where it is,
  a module open in every section. **Part 2** is numbered cards; "Picture 2·5" below means part 2, card 5.
- The stylesheet is `app/styles/*.css` (sent as one file, in their number order), the script
  `app/templates/js/*.js` (put together by `page.js`, made once per language; AGENTS.md has the map),
  the color tokens `app/templates/_theme.html`. Change those, never inline copies.
- When the theme changes, update this file and redraw the picture (at the latest in the Deploy's documentation part, 5-deploy.md). A rule
  here with no card, or a card with no rule, is a mistake: fix whichever is missing.

The sections below follow the picture's Part 2, card by card (0.2.8-beta.24, R1): section N is card 2·N.
Until the picture is redrawn in this order (at the next Deploy), its cards still carry their old numbers: old → new
1→1, 2→4, 3→3, 4→9, 5→7, 6→6, 7→10, 8→11, 9→12, 10→2, 11→6 and 7, 12→7, 13→7, 14→8, 15→13, 16→14, 17→15, 18→11,
19→16; 20 (spacing) and 21 (the event pop-up) are still to be drawn, as 17 and 18.
**Cancel/Save buttons** = the pair at the bottom right of a module or pop-up (section 6). **Status/Action
buttons** = a status box: the state, with its action under it (section 7). Other words (Cancel | Yes, No | Yes)
are still used where they fit.

## 1. Fonts

Picture 2·1. IBM Plex Sans (`--font`) for everything; IBM Plex Mono (`--mono`) only for what's typed or copied
exactly (links, IDs, the Username, the client ID, the stream name). Served by CalendarStream, never Google Fonts.
Module kind 17 px/700, text 14, labels 600, notes 13 muted.

## 2. Website color palette

Picture 2·2. Every color is a token with a light and a dark value. Light is the Soft palette. (The calendar
palette, Google Calendar's 11 colors, is the color box's: section 14.)

| Token | Light | Dark | Used for |
| --- | --- | --- | --- |
| `--bg` | #f7f6f3 | #0f1218 | the page |
| `--card` | #fdfcfa | #171b23 | sections, modules, pop-ups; words on a filled button |
| `--soft` | #f1efeb | #1d222c | quiet fills (instruction tiles, hover) |
| `--line` | #e8e4de | #2a303b | every border and divider |
| `--text` / `--muted` | #2b2f36 / #7a8291 | #e6e8ec / #98a2b3 | text / labels, notes, status lines |
| `--accent` (`--onaccent`) | #40609c (#fff) | #93b4ff (#0f1218) | pressable buttons only |
| `--ok` / `--okbg` | #2f7d62 / #eef5f0 | #4ade80 / #0f2a20 | green: done, OK |
| `--run` / `--runbg` | #40609c / #eef1f7 | #93b4ff / #14203d | pressed: in action, or waiting on you |
| `--warn` / `--warnbg` | #946a24 / #faf3e6 | #fbbf24 / #2b2110 | amber: a problem outside CalendarStream |
| `--bad` / `--badbg` | #b4483c / #faeeeb | #f87171 / #2d1414 | red: CalendarStream itself failed |

Section colors (0.2.8-beta.24, F7), each a muted border (mixed half with `--line`) on `--card`: Calendar slate blue
#5b6f9a, Calendars teal #2a9d8f, Feeds violet #7c5cc4, All Rules amber #c08a2b, Event Templates green #4c9a5b,
History grey #8a8f98 (section 9).

## 3. Icons

Picture 2·3. Material Symbols Rounded, weight 400, only from `app/material_symbols/symbols.json`; 13–24 px, in the
text color. Add new ones with `tools/vendor_icons.py`, never changing existing ones.

## 4. Corners

Picture 2·4. Rounded rectangles only, never pills. Controls 8 px (`--r`); sections, modules, pop-ups and menus
12 px (`--rbox`); small marks (a color, today, a switch) 4–6 px.

Sizes: 50 px module headers, 34 px controls (fields, buttons), the 132 × 50 px Status/Action buttons, the 130 × 34 px
Cancel/Save buttons. Sections and modules have a 2 px border (a module with 1 px less padding all round, a section
drawn as 1 px plus a 1 px inset line, so both keep their size); everything else 1 px.

## 5. Static & Icon buttons

Picture 2·5. Buttons that do one thing and don't show a state: icon buttons (34 × 34 px, the icon `--muted`, `--soft`
behind it on hover), every +, Copy (the icon becomes "Copied" for 1.8 s), Open, Expand / Close. A field saved in
place shows ✓ once saved, then ✕ | ✓ while typing (✕ puts it back, ✓ saves it).

## 6. Responsive Cancel/Save buttons

Picture 2·6. Cancel | Save, 130 × 34 px, at the bottom of what it saves; the pressed side fills the pair ("Saved",
"Cancelled") for 3 s. A question's answers can be the same pair (No | Yes). **Blue** is for these and every other
pressable button only: `--accent` fill, `--onaccent` words; never a status.

## 7. Responsive Status/Action buttons

Picture 2·7. A multi-button, 132 × 50 px: the status chip over the action that updates it (Sync Now, Check now,
Update now, Connect, Fix).

**One look per meaning.** A status looks one way for one meaning, everywhere: a chip, a Status/Action button, a
button's done or failed state, a line of text. Never pick a color because it looks nice there.

| Look | Means | Drawn as | Words that use it (add new ones here) |
| --- | --- | --- | --- |
| **Green** | done, OK | `--ok` on `--okbg` (`good`); a done button fills `--ok` with a green pulse | Healthy, Connected, Read by Google, Up to date, Synced, Updated, Saved, N Rules, N Templates |
| **Pressed** | in action, or waiting on you | `--run` words on `--runbg` (`run`); a working button is `--card` with `--run` words | Syncing…, Checking…, Downloading…, Restarting…, Starting, Update found, Update available, Not checked, Not set up, Not connected, Invited, Not read yet, Setup needed, Paused, N to check (rule conflicts) |
| **Amber** | a problem outside CalendarStream (United, Google, GitHub, the internet), or what you typed was refused | `--warn` on `--warnbg` (`warn`); a failed button fills `--warn` with an amber pulse | Sign-in rejected, Blocked, Error (a download), Address missing, Client rejected, Sync problem (Google's answer), Couldn't check, Failed, Stopped, Unhealthy, a refused Save ("Not a valid regex…"), Sign-in failed |
| **Red** | CalendarStream itself failed | `--bad` on `--badbg` (`bad`); a failed button fills `--bad` with a red pulse (`data-cause="inside"`) | Internal error, Sync problem (Google sync failed inside), Update failed |

The theme suite fails any status word whose look isn't in this table (Blue, for buttons: section 6).

**Transitions** of the Status/Action buttons (the rest are in section 8):

| Transition | Trigger | Style | Duration, easing | Holds |
| --- | --- | --- | --- | --- |
| Button grows | press (or a sync seen running) | the button grows from the bottom 22 px to the whole box; the chip fades out under it at once | grow 0.25 s ease; chip fade 0.2 s | while working |
| Working words | the button grows | words fade in (`sn-in`) with a spinning icon (1 s per turn, linear) | 0.25 s ease-out | at least 0.7 s (Check now), 0.5 s per Connect step |
| Done | the action succeeded | fills green; a ring pulses out (`pulse-ok`, 0 → 9 px) twice | 1.1 s ease-out × 2 | 2.4 s |
| Failed outside | United, Google, GitHub or the internet said no | fills amber; `pulse-warn` × 2 | 1.1 s ease-out × 2 | 2.4 s |
| Failed inside | CalendarStream failed | fills red; `pulse-bad` × 2 | 1.1 s ease-out × 2 | 2.4 s |
| Found / waiting on you | Check now found an update | the pressed look; `pulse-run` × 2 | 1.1 s ease-out × 2 | 2.4 s |
| Shrink back | after the hold | the button shrinks to the bottom; **then** the new status word fades in (never a fade through the old one) | shrink 0.25 s ease; word 0.2 s after a 0.25 s delay | — |
| Top-bar Update now | press, or an update started elsewhere (Auto-update, another tab) | only the words change, fading in (never a blank pill); a bar slides under them | words 0.25 s ease-out; bar 1.2 s ease-in-out, repeating | until restarted |
| Update finished | the new version answers | "Updated" (green), then the page reloads: 15 s after it showed Restarting… (0.8 s if it never did) | — | — |

**Flows**: the words each Status/Action button says, in order. Every copy of an action (the top bar and Settings;
Feeds and Settings) shows the same words at the same moment and ends together.

- **Sync Now**: Sync Now → Syncing… → Synced (green) or Failed (amber; red if CalendarStream failed) →
  Sync Now, the box redrawn with the new status.
- **Check now**: Check now → Checking… → Up to date (green), Update found (pressed) or Couldn't check
  (amber) → Check now, Updates redrawn.
- **Update now**: Update now → Downloading… → Restarting… → Updated (green) → the page reloads; or
  Update failed (red) → Update now. An update started elsewhere (Auto-update at the frequency chosen in Settings,
  or another tab) shows the same words on every open page, which reloads the same way (0.2.8-beta.24, F1).
- **Connect** (Google Calendar API Sync; Reconnect when healthy, Fix after a fault): → Saving… → Checking… →
  Checking address… → Healthy (the Google modules in Feeds then connect their own accounts). The first step that fails stops it: Stopped (amber), and the line under it
  says what to fix as a click path, with Copy and Open.
- **Remove a calendar**: Merge into [calendar] | Delete, ☐ Download a copy (.ics) first, and with a Merge
  and rules of its own: Move to [calendar] | Delete them → Remove (the last CalendarStream calendar:
  Empty). Undo in History.
- **Import**: Choose Calendar.ics… → dates (All) → Import → each event already there, one at a time:
  Delete | Merge, ☐ Do this for all remaining → added. Undo in History.

## 8. Every transition

Picture 2·8. Every change of state, with what starts it, how it moves and how long it stays (the Status/Action
buttons' own are in section 7). With **reduced motion** (`prefers-reduced-motion: reduce`) nothing slides, grows,
fades, spins or pulses: each state simply replaces the last, with the same words and hold times.

| Transition | Trigger | Style | Duration, easing | Holds |
| --- | --- | --- | --- | --- |
| Pop-up opens | a click that opens one (every +, a question) | fade + scale 0.96 → 1; the backdrop (rgba(0,0,0,.55), the page blurred 2 px) fades in | 0.2 s ease-out | — |
| Color box / emoji list | a click | opens under it at once | instant | until a choice or a click elsewhere |
| Regex test box | typing | ✓ / ✕ redrawn | 300 ms after the last key | — |
| Cancel \| Save | press | the pressed side grows over the pair (flex) and fades its words | 0.3 s ease | 3 s, then idle |
| Field saved in place | Save | ✓ fades in (`slotfade`) | 0.45 s ease (messages 0.3 s) | until typing |
| Expand / Close | press | the triangles turn (Close points up) | 0.15 s | — |
| Copy | press | the icon becomes "Copied" | instant | 1.8 s |
| Calendar search | typing | results after a pause | 300 ms debounce | — |

## 9. Modules

Picture 2·9. Every calendar and feed: a 50 px header is all a folded one shows; a 2 px border. Line 1: the color
box, the kind (fixed text), "Last synced 00:31" and the Status/Action buttons on the right. Line 2: the label
(plain text; a field of the same size while expanded) with a raised (i), "Next check @ 00:44" on the right. Expand
sits in the bottom border; open, a Close line sits under the header.

Colors (0.2.8-beta.24, F7): a module's border is its calendar's or feed's color at 65%, its header a 10% tint and the
rest a 5% tint of it, in light and dark; each section has its own muted border (section 2) on `--card`, so
sections and modules are told apart while everything else stays as it was.

(i) is info, about this module: what it is, then its note when it has one; (?) is help (section 12).

## 10. Handles

Picture 2·10. ▲ ☰ ▼ in the section's right margin; none with nothing to reorder.

## 11. Pop-ups

Picture 2·11. Pop-ups and drop-downs: 12 px corners, 12 px padding, ← and the title; the whole screen on a phone
(≤ 700 px); the page behind dimmed (rgba(0,0,0,.55)) and blurred (2 px). Every + opens one, centred. A question
is one too, never the browser's alert / confirm box: its answers on one line, or one under the other when they're
sentences; a second line under the question is a note, muted and not bold. A choice of calendars is a drop-down
of ticks.

## 12. (?) help

Picture 2·12. (?) is help: how to do something. A 15 px icon raised right after the word it explains; hover, focus
or a click shows it. Explanations live in an (i) or a (?), never on the page (section 13). Its pop-up opens with
its upper left at the icon; past the window's right edge, its upper right sits at that edge; past the bottom, its
lower corners sit at the bottom (F4).

## 13. Words on the page

Picture 2·13. In-page words are click paths and short lines: `Place › Place › Field: value › Button`,
e.g. "Google Cloud › Clients › CalendarStream › Authorized redirect URIs › + Add URI › Save". No
paragraphs: the why goes in the (?). Status words are a word or two (section 7). The theme suite fails a
sentence on the page longer than 20 words (the (?), the calendar and the log aside).

## 14. Color box and emoji

Picture 2·14. **Color box**: one palette everywhere, Google Calendar's 11 colors (what Google shows for an event):
calendars, feeds, rules, event templates, events. A click opens it (in a module: while expanded); the choice goes
with the module's Save. **Emoji**: the common ones beside the field, then a rounded "Search for more emojis" field
that opens every emoji (Unicode up to Emoji 13.0, no flags, drawn by the device): ten a line, scrolling, filtered
as you type. One older Windows may not draw has a small i (Clarifications).

## 15. Date range and Import row

Picture 2·15. **Date range**: From | To | ☐ All, in that order, everywhere a range is asked for (search, feeds,
Print Preview, Import). All clears the dates and greys them; typing in is done after unticking it. All is what an
empty range means. **Import row**: the heading, the file field (a file icon and "Choose Calendar.ics…", filling the
line), the dates, the button on the right. The same row in every calendar; CCS+'s is Manual Upload (it replaces the
schedule, so no dates).

## 16. Deleted events and History

Picture 2·16. **Deleted event**: struck through and greyed, saying where it was deleted (CalendarStream, Google
Calendar, United, the feed), with Restore, until its Undo pops off History. **History**: Time | Type | Event | Undo;
a filter (Type, words, time) on top; folded, the latest lines with Undo / Redo where it applies (a stack: newest
first). Something done outside CalendarStream (deleted in Google, removed by United) has no Undo icon: Restore is
on the event.

## 17. Spacing

Picture 2·17 (drawn at the next Deploy). R11, 0.2.8-beta.21; tried for now and adapted as needed:
- 5 px between parts: sections, modules, the parts of a module or a pop-up, buttons in a row.
- 2 px between a label and its field (the label over it; From and To beside their dates, 5 px).
- 9 px inside a module's border at the sides, 5 px top and bottom; the 50 px header unchanged. A box
  inside a module (Include, an instruction tile) is 5 px 9 px too.
- 12 px inside every pop-up, so all pop-ups and all modules are formatted alike.
- No other padding or margin (F9). The one exception: a folded module or module-like section keeps 14 px
  below it, for the Expand line in its border.
- The rule lives in `app/styles/17-spacing.css`, last, so it wins; the theme suite measures it.

## 18. The event pop-up

Picture 2·18 (drawn at the next Deploy). Its layout is in the Clarifications (0.2.8-beta.22, F11; 0.2.8-beta.24, F5).

## Enforced by tests

The theme defines one consistent look **and interaction**; it is checked, not just described.

- `tests/suite_44.py` (the theme suite) checks the whole page, light and dark, against the rules here:
  each Clarification below has at least one check in it. A new Clarification gets its check in the
  same beta; a change that breaks one fails `tests/run.sh`, so it can't be published.
- Every page change is checked in the states the Developer sees, not only on a fresh page: after the
  change's own action, after an in-place redraw (a Save, Check now, Sync Now), after an update, on a
  phone (390 px) and in dark.
- Before writing any new part, Claude reads this file and finds the existing part it should behave
  like (a Status/Action button → Sync Now; a field row → the login; a list → handles); a new part copies
  that part's look and interaction instead of inventing its own.

## Clarifications

The Developer's decisions about how the page looks. Always keep them: every change follows them, and
the picture's last card shows this list (it's read from here when the picture is drawn). Add each new
one here, with its card.

- Module handles (▲ ☰ ▼) sit in the section's right margin: they take up no extra space, and modules
  (and All Rules' lines) are as wide as the section header (their right edge lines up with its +).
  No handle where there's nothing to reorder (a list of one). (Picture 2·10)
- Calendar and feed module headers share one layout. Line 1: the color (calendars only), the module's
  kind (fixed text, 17 px, 15 on a phone where it may take two lines: CalendarStream, United Airlines CCS+, Google Calendar, Apple Calendar,
  Calendar Feed…), then on the right "Last synced 00:31" and the Status/Action buttons (Healthy…). Line 2: its
  label (plain text; a field while expanded) with a raised (i) after it (what it is, and its note, changed
  under Close), then on the right "Next check @ 00:44" and Sync Now. A line with nothing to say is
  left blank. (Picture 2·9)
- Status words: "Last synced 00:31" or "Sync failed 00:31", never "Last check was successful @…";
  a feed says "Last read by Google 00:31" (or "Last read …"); Settings → Updates "Last checked 00:31". (Picture 2·9)
- The Status/Action buttons are a multi-button: an overall status over the action that updates it ("Healthy" over
  Sync Now on United Airlines CCS+ is the model). Wherever an overall status and its update share a
  box, it works the same: every action in Status/Action buttons (Sync Now, Settings → Check now, Update now,
  Connect, any new one) says what it's doing at once (Syncing…, Checking…, Downloading…) and grows over the box
  as the status word fades, then pulses (done, failed or found, in its look) for
  2.4 s, then shrinks back before the new status word fades in. Never a button that gives no sign
  it was pressed, and never a status left showing while its update runs. (Picture 2·7)
- One look per meaning, everywhere: green is done or OK; the pressed look (blue words on the box) is
  in action or waiting on you; amber is a problem outside CalendarStream (United, Google, GitHub, the
  internet); red is CalendarStream itself failing; blue fills are pressable buttons only. (Pictures 2·6, 2·7)
- Module-like sections (All Rules, Event Templates): the count box in the top right corner; + in the
  bottom right corner of the open section. (Part 1)
- A box means you can change it: fixed text (a title, the release channel) is plain text, never in a
  field box. A group that looks like a module but has nothing to fold (Settings → Updates) uses the
  module header layout, always open, with no Expand. (Part 1)
- Copy buttons sit inside their field, like the password box's eye. Client ID / secret pairs are laid
  out like a login, connected or not. (Picture 2·1)
- Adding something (+ Add a calendar…) ends with the standard Cancel/Save buttons, like editing it. (Picture 2·6)
- After an update the page reloads, so the new version's script and stylesheet run its parts. (Picture 2·7)
- Expand / Close lines: ▸ Expand ◂ points at the words; Close's triangles point up. (Picture 2·9)
- Pop-ups: a dark backdrop (rgba(0,0,0,.55)) that keeps the page in view, out of focus (blurred 2 px), and
  a 200 ms fade and scale-up (none with reduced motion). Every Cancel/Save buttons, pop-ups included, are the
  130 × 34 pair. (Pictures 2·11, 2·8)
- An opened event: Close in the bottom left corner, its icons (link, reminders, edit, duplicate,
  delete) on the right, as near the event's right edge as Close is to its left one; when it's too narrow for
  one line, the icons go on a line above Close. (Part 1)
- Events show the color Google shows: their own, their rule's, else their calendar's. (Part 1)
- Rule lines say what the rule does, titled or not ("Items without an end time → Change length to 1:00"). (Picture 2·10)
- Fields everywhere, pop-ups included: a 12 px muted label over a 34 px field, 2 px apart; a value that
  can't be changed (an event's calendar) is plain text. Related fields share a line (Calendar | Title,
  Location beside the event's color, link and duplicate; Starts | Ends, each with its Time under it). (Picture 2·1)
- Every section's + is in a corner: the top right (Calendars, Feeds, the calendar), or the bottom right
  of an open module-like section. The calendar's search icon sits left of its Time Zone. (Part 1)
- A credentials row (Client ID / secret) ends with a trash, which asks before deleting. A Settings
  group that works shows everything at once, nothing under Expand: its header (like Updates), its
  credentials row, and its Remove (red, lower left, like a module's) with its options beside it; the
  explanations go in its (?). (Picture 2·7)
- One action, one state: when the same action appears in more than one place (Update now in the top
  bar and in Settings; Sync Now for Google in Feeds and in Settings), pressing any copy shows the same
  progress, in the same words, in every copy at once, and they all end together. (Picture 2·7)
- A row of settings that belong together is one line (Check for updates [Hourly] ☐ Auto-update). (Part 1)
- Google calendars say "Next push instantaneous" (each change goes at once). (Part 1)
- A rule's color is one of Google Calendar's 11 event colors; rule lines read "Color ■ (Name)". (Picture 2·10)
- Light is the Soft palette (warm off-white, muted blue accent), still named Light with its icon. (Picture 2·2)
- In-page instructions are click paths (Settings › Google › New Project › Name: CalendarStream › Save),
  not paragraphs, everywhere on the site; the explanations go in the (?). (Picture 2·13)
- Every date range has All: From | To | ☐ All (search, Print Preview, Import). (Picture 2·15) A feed module's Include says it in words instead: Dates (optional; empty = all), From over To (0.2.8-beta.17).
- No browser alert or confirm boxes: every question and notice is the page's own pop-up. (Picture 2·11)
  Deleting or hiding an event asks the question, a note in muted words on the line under it, and No | Yes
  as the 130 × 34 Cancel/Save buttons (0.2.8-beta.23, F16).
- (i) is info (what the module is, then your note); (?) is help (how to). (Pictures 2·9, 2·12)
- Every + opens a centred pop-up, the page dimmed and out of focus behind it. (Picture 2·11)
- Modules have a 2 px border, with 1 px less padding all round, so they keep their size. (Picture 2·9)
- A module's name is its label: plain text until the module is expanded, then a field of the same size. (Picture 2·9)
- One color palette everywhere: Google Calendar's 11 colors, in the color box. (Picture 2·14)
- A deleted event stays struck through and greyed, saying where it was deleted, with Restore, until its
  Undo pops off History. (Picture 2·16)
- Importing a calendar file is one row in every calendar: heading, the file field filling the line, the
  dates, the button on the right (CCS+: Manual Upload). (Picture 2·15)
- Emoji: the common ones, then a rounded "Search for more emojis" field that opens every emoji, ten a line, scrolling, filtered as you type. (Picture 2·14)
- Emoji older Windows may not draw (newer than Emoji 12.0, and flags): a small i at the emoji's upper right in the
  list, and the page's own (i) beside the field when one is chosen, both "May not show on older Windows". (0.2.8-beta.19, F8)
- A Google module's colors end with a muted line, "Color change does not carry to Google", while Google refuses the
  color: only after it refused the RGB color, the nearest calendar color and a full update (0.2.8-beta.21, I1).
  (0.2.8-beta.19, I1.1)
- Spacing: 5 px between parts, 2 px between a label and its field, 9 px inside a module's border (5 px top and
  bottom), 12 px inside pop-ups; nothing extra. (0.2.8-beta.21, R11, F9; Picture 2·17)
- (i) and (?) pop-ups open with their upper left at the icon; at the window's right edge their upper right sits
  at it; at the bottom their lower corners sit at it. In a pop-up, its edges count as the window's. (0.2.8-beta.21,
  F4; Picture 2·12)
- A folded module's (i) is a superscript right after its label's last word. (0.2.8-beta.21, F5; Picture 2·9)
- An Include box's calendars run down a column three tall (5 px apart), then a second column; with no room for
  another column, the columns grow taller instead; in every module. Its From / To: each label only
  as wide as the longer, 5 px from its date, the dates lined up; a Calendar Feed's Add to… buttons are as wide as
  the longest of them. (0.2.8-beta.21, F5.1, F5.2, F5.3; Part 1)
- Today has a 2 px accent border around its whole day, as well as its filled date. (0.2.8-beta.21, F10; Part 1)
- The event pop-up: ← and its title, with its tools in the upper right corner (Choose from template; Print and
  Duplicate); the fields on the left, Notes on the right as tall as them (dragging Notes taller grows the pop-up);
  Link to below, closed until Event or Rule; Delete (Hide or Show for a calendar source's event, with its (i)) at the
  bottom left, the Cancel/Save buttons at the right. On a phone, one column. (0.2.8-beta.22, F11; Picture 2·18, drawn at the next Deploy)
  The end's column: Time with All-day Event on its label line, right of "Time *" (ticked, it stays there as the Time
  fields hide); Different end time zone beside Time zone's field, End time zone under it when ticked. (0.2.8-beta.24, F5)
- Sections and modules are told apart by color, nothing else changing: each section's 2 px border its own muted
  color on `--card`; each calendar's or feed's module bordered in its color at 65%, its header tinted 10% and the rest
  5%; light and dark. (0.2.8-beta.24, F7; Pictures 2·2, 2·9)
