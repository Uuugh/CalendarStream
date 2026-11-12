# Theme

Read before changing how the page looks. Written so anyone (the Developer, Claude, a Reviewer) can check
a change against it without asking: every look, status, transition and word rule is here, each with the
card of the **CalendarStream Theme Rules** picture that shows it.

- The picture: `build_rules/CalendarStream_Theme_Rules_Light.png` and `…_Dark.png` (each also as a `.pdf`, made from the picture), drawn from the page
  itself (every size in it is measured). **Part 1** is the whole page with each part named where it is,
  a module open in every section. **Part 2** is numbered cards; "Picture 2·5" below means part 2, card 5.
  Since 0.2.8-beta.31 (F22) Part 2 (the cards) is at the top, under the title, and Part 1 (the whole page) follows it;
  the parts keep their numbers.
- The stylesheet is `app/styles/*.css` (sent as one file, in their number order), the script
  `app/templates/js/*.js` (put together by `page.js`, made once per language; AGENTS.md has the map),
  the color tokens `app/templates/_theme.html`. Change those, never inline copies.
- When the theme changes, update this file. (0.2.8-beta.33, R7: the Developer no longer wants the pictures kept up to
  date with every change - they stay as they are, a snapshot, not a thing to redraw each time. A new Clarification
  with no card is expected now, not a mistake to fix.)

The sections below follow the picture's Part 2, card by card (0.2.8-beta.24, R1): section N is card 2·N (R1: 16 cards; the color box and emoji sit on card 11 with Pop-ups, Spacing on card 9 with Modules).
**Cancel/Save buttons** = the pair at the bottom right of a module or pop-up (section 6). **Status/Action
buttons** = a status box: the state, with its action under it (section 7). Other words (Cancel | Yes, No | Yes)
are still used where they fit.


## Reading these rules

The numbered sections describe the current design. Clarifications record the Developer's decisions and their
origin; when an older decision was superseded, the current value is stated here rather than retaining both as
competing requirements. The pictures are historical snapshots, not a second specification.

The shared values live in `app/templates/_theme.html`: 5 px between content parts, 1 px between a label and its
field, 12 px dialog/menu padding, 9 px module side padding, 5 px module vertical padding, and 13 px notes.
Component files own their base, states, responsive and print rules. `17-spacing.css` contains shared flow rules;
it is not a final override layer. See AGENTS.md for the CSS ownership map.

## 1. Fonts

Picture 2·1. IBM Plex Sans (`--font`) for everything; IBM Plex Mono (`--mono`) only for what's typed or copied
exactly (links, IDs, the Username, the client ID, the stream name). Served by CalendarStream, never Google Fonts.
Module kind 17 px/700 (15 px on a phone), default text 14 px, labels 600, notes 13 px muted.
General top-bar icon buttons are 34 × 34 px; the compact calendar toolbar uses 28 × 28 px icons.

## 2. Website color palette

Picture 2·2. Every color is a token with a light and a dark value. Light is the Soft palette. (The calendar
palette, Google Calendar's 11 colors, is the color box's: section 14.)

| Token | Light | Dark | Used for |
| --- | --- | --- | --- |
| `--bg` | #f7f6f3 | #0f1218 | the page |
| `--card` | #fdfcfa | #171b23 | sections, modules, pop-ups; words on a filled button |
| `--soft` | #f1efeb | #1d222c | quiet fills (instruction tiles, hover) |
| `--line` | #e8e4de | #2a303b | every border and divider |
| `--text` / `--muted` | #2b2f36 / #626c7c | #e6e8ec / #98a2b3 | text / labels, notes, status lines |
| `--accent` (`--onaccent`) | #40609c (#fff) | #93b4ff (#0f1218) | pressable buttons only |
| `--ok` / `--okbg` | #2f7d62 / #eef5f0 | #4ade80 / #0f2a20 | green: done, OK |
| `--run` / `--runbg` | #40609c / #eef1f7 | #93b4ff / #14203d | pressed: in action, or waiting on you |
| `--warn` / `--warnbg` | #946a24 / #faf3e6 | #fbbf24 / #2b2110 | amber: a problem outside CalendarStream |
| `--bad` / `--badbg` | #b4483c / #faeeeb | #f87171 / #2d1414 | red: CalendarStream itself failed |

Muted text must reach 4.5:1 against `--card`, `--bg` and `--soft` in both palettes. The light muted
value is #626c7c (replacing #7a8291, which reached only 3.77:1 on cards). This is a readability correction;
the accent and status colors are unchanged.

Section colors (0.2.8-beta.24, F7; 0.2.8-beta.26, F10), each a muted border (35% of the color, mixed with `--line`) on `--card`:
Calendar slate blue #5b6f9a, Calendars teal #2a9d8f, Feeds a clear blue #2f86c8 (not the buttons' #40609c, not Calendar's slate),
All Rules lavender #9b8ad6, Event Templates copper #b8733a, History grey #8a8f98 (section 9).

The title's two words use the logo's colors (0.2.8-beta.26, F11.3): `--logo-cal` (Calendar: navy #0b1f44, light #e6e8ec in dark)
and `--logo-stream` (Stream: #1a8cff, #4aa8ff in dark).

## 3. Icons

Picture 2·3. Material Symbols Rounded, weight 400, only from `app/material_symbols/symbols.json`; 13–24 px, in the
text color. Add new ones with `tools/vendor_icons.py`, never changing existing ones.

## 4. Corners

Picture 2·4. Rounded rectangles only, never pills. Controls 8 px (`--r`); sections, modules, pop-ups and menus
12 px (`--rbox`); small marks (a color, today, a switch) 4–6 px.

Sizes: 50 px module headers, 34 px controls (fields, buttons), the 132 × 50 px Status/Action buttons, the 130 × 34 px
Cancel/Save buttons. Every border is 1 px (0.2.8-beta.26, F21: sections and modules were 2 px). The one 2 px line is today's
day in the calendar (Clarifications), and the focus outline.

## 5. Static & Icon buttons

Picture 2·5. Buttons that do one thing and don't show a state: icon buttons (34 × 34 px in the general toolbar; 28 × 28 px in the compact calendar toolbar, the icon `--muted`, `--soft`
behind it on hover), every +, Copy (the icon becomes "Copied" for 1.8 s), Open, Expand / Close. A field saved in
place shows ✓ once saved, then ✕ | ✓ while typing (✕ puts it back, ✓ saves it).

## 6. Responsive Cancel/Save buttons

Picture 2·6. Cancel | Save, 130 × 34 px, at the bottom of what it saves; the pressed side fills the pair ("Saved",
"Cancelled") for 3 s. With nothing to save (F12.4) both are truly disabled: greyed and faded, not focusable, announced as
unavailable (a pop-up's Cancel, which only closes it, stays available; so do the buttons of a + Add pop-up, which can be
saved with its defaults). The first change (F9) turns them on and Save pulses in the pressed look for about 5 seconds, then
stays in full color (WCAG 2.2.2); Save or Cancel brings the inactive look back. Cancel grows over the whole pair in 1 s and
shrinks back in 1 s. A question's answers can be the same pair (No | Yes). **Blue** is for these and every other
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
| Cancel \| Save | press | the pressed side grows over the pair (flex) and fades its words; Cancel takes 1 s, in and back | 0.3 s ease (Cancel 1 s) | 3 s, then idle |
| Save pulse | the first change in a form | Save pulses in the pressed look (`pulse-run`) once a second, 5 times, then stays in full color; none with reduced motion | 1 s ease-out × 5 | about 5 s |
| Good status word | a green status appears | the word shows 2.4 s, then shrinks to its ✓ (the word stays as its tooltip and accessible name); count boxes keep their numbers | 0.5 s ease | — |
| Field saved in place | Save | ✓ fades in (`slotfade`) | 0.45 s ease (messages 0.3 s) | until typing |
| Expand / Close | press | the triangles turn (Close points up) | 0.15 s | — |
| Copy | press | the icon becomes "Copied" | instant | 1.8 s |
| Calendar search | typing | results after a pause | 300 ms debounce | — |

## 9. Modules

Picture 2·9. Every calendar and feed: a 50 px header is all a folded one shows; a 1 px border. Line 1: the color
box, the kind (fixed text), "Last synced 00:31" and the Status/Action buttons on the right. Line 2: the label
(plain text; a field of the same size while expanded) with a raised (i), "Next check @ 00:44" on the right. Expand
sits in the bottom border; open, a Close line sits under the header.

Colors (0.2.8-beta.24, F7; 0.2.8-beta.26, F10, F12.3): a module's border is its calendar's or feed's color at 45%, its header a 6%
tint and the rest a 3% tint of it, in light and dark; each section has its own muted border (section 2) on `--card`, so
sections and modules are told apart while everything else stays as it was.

**The 2/3-line**: status lines are unboxed: no border or fill, right-aligned next to their Status/Action
button, visible only while collapsed (0.2.8-beta.32, I27 supersedes the earlier boxed, centred layout).
**Default** sits right of a CalendarStream calendar's title; while expanded, the other local calendars offer
it as a button and read-only calendars show it disabled. **On | Off** sits inline before an expanded module's
note; Off dims the module and keeps its settings. The control is a 28 px-high, 8 px-cornered segmented switch.


(i) is info, about this module: what it is, then its note when it has one; (?) is help (section 12).

### Spacing (was card 17)

R11, 0.2.8-beta.21; tried for now and adapted as needed:
- 5 px between parts: sections, modules, the parts of a module or a pop-up, buttons in a row.
- 1 px between a label and its field (the label over it; From and To beside their dates, 5 px). (0.2.8-beta.26, F12.1: was 2 px.)
- 9 px inside a module's border at the sides, 5 px top and bottom; the 50 px header unchanged. A box
  inside a module (Include, an instruction tile) is 5 px 9 px too.
- 12 px inside every pop-up, so all pop-ups and all modules are formatted alike.
- These values govern spacing between content parts. Internal control geometry, calendar cells and anchored
  header layouts use the component sizes below; they are not extra flow spacing. A folded section keeps 14 px
  below it for the Expand line in its border.
- A module's Close line has 2 px less above and below it (0.2.8-beta.26, F12.2). The bottom padding is the same folded and open:
  5 px in a module, 18 px (as at its top) in a module-like section (0.2.8-beta.26, I6).
- Values are shared tokens in `_theme.html`; shared flow selectors live in `17-spacing.css`. A component's
  spacing belongs in its component file, not in a later file that overrides it. The theme suite measures values.
- The calendar key starts 5 px below the calendar. Header date/navigation gaps remain 8 px; tool gaps are 5 px;
  the wrapped second row has a 6 px gap. These compact header dimensions are deliberate component geometry.

## 10. Handles

Picture 2·10. (0.2.8-beta.28, I12) One handle in the margin on the left of the module or rule line: ▲ above, the grip (two columns of three faint dots, like Gmail's), ▼ below; always visible; none with nothing to reorder. Left is the default; Theme can place grips in the right margin. Drag the grip to reorder, or use ▲ ▼ with the keyboard. Every request about the "hamburger slider" means this grip.

## 11. Pop-ups

Picture 2·11. Modal pop-ups: 12 px corners and 12 px padding, ← and the title; the whole screen on a phone
(≤ 700 px), with square edge-to-edge corners. The page behind is dimmed (rgba(0,0,0,.55)) and blurred (2 px). Every + opens one, centred. A question
is one too, never the browser's alert / confirm box: its answers on one line, or one under the other when they're
sentences; a second line under the question is a note, muted and not bold. A choice of calendars is a drop-down
of ticks.

Anchored month, view and language menus keep their compact panel positioning on a phone. Their panel padding
and corners are also 12 px. The month menu's grid cells and arrow buttons retain their own compact geometry;
these anchored menus do not dim the page or fill the phone. Full-screen behavior applies to modal dialogs.

### Color box and emoji (was card 14)

The palette (names and codes, from `GOOGLE_COLORS` in `app/gsync.py`): Tomato #d50000 · Flamingo #e67c73 · Tangerine #f4511e · Banana #f6bf26 · Sage #33b679 · Basil #0b8043 · Peacock #039be5 · Blueberry #3f51b5 · Lavender #7986cb · Grape #8e24aa · Graphite #616161. Card 11 shows each with its name and code.

**Color box**: one palette everywhere, Google Calendar's 11 colors (what Google shows for an event):
calendars, feeds, rules, event templates, events. A click opens it (in a module: while expanded); the choice goes
with the module's Save. **Emoji**: the common ones beside the field, then a rounded "Search for more emojis" field
that opens every emoji (Unicode up to Emoji 13.0, no flags, drawn by the device): ten a line, scrolling, filtered
as you type. One older Windows may not draw has a small i (Clarifications).

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

## 14. Date range and Import row

Picture 2·14. **Date range**: From | To | ☐ All, in that order, everywhere a range is asked for (search, feeds,
Print Preview, Import). All clears the dates and greys them; typing in is done after unticking it. All is what an
empty range means. **Import row**: the heading, the file field (a file icon and "Choose Calendar.ics…", filling the
line), the dates, the button on the right. The same row in every calendar; CCS+'s is Manual Upload (it replaces the
schedule, so no dates).

## 15. Deleted events and History

Picture 2·15. **Deleted event**: struck through and greyed, saying where it was deleted (CalendarStream, Google
Calendar, United, the feed), with Restore, until its Undo pops off History. **History**: Time | Type | Event | Undo;
a filter (Type, words, time) on top; folded, the latest lines with Undo / Redo where it applies (a stack: newest
first). Something done outside CalendarStream (deleted in Google, removed by United) has no Undo icon: Restore is
on the event.

## 16. The event pop-up

Picture 2·16. Its layout is in the Clarifications (0.2.8-beta.22, F11; 0.2.8-beta.24, F5).

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

- Module handles (▲ grip ▼; 0.2.8-beta.28, I12) sit in the margin on the left of the module or rule line: they take up no extra space,
  they are always visible (faint), never over a box, and modules (and All Rules' lines) are as wide as the section header (their right
  edge lines up with its +). The grip is two columns of three dots; it is centered on the module's 50 px header or on the rule line. Theme may put grips on the right; left is the default. No
  handle where there's nothing to reorder (a list of one). (Picture 2·10)
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
- Every section's header reads: icon · title · space · status lines · health · +. Calendars and Feeds have no status lines; All Rules and
  Event Templates up to three (the conflicts or errors, otherwise how many), with their count box and +; History its three
  latest lines, left-aligned, on the right before its Healthy box. + is in the top right corner of every section that has
  one. (0.2.8-beta.26, F13, I4, F18; Part 1)
- A good login word (Signed in, Validated, a connection status inside a module) shrinks to its ✓ after about 2.4 s; the word
  stays as the tooltip and accessible name. The Status/Action buttons (Healthy, Up to date, Connected, Read by Google, the
  counts) never lose a word. (0.2.8-beta.26, F23; 0.2.8-beta.27, I10; Picture 2·8)
- Calendars, Feeds, All Rules and Event Templates say "Expand to Configure"; History says "Expand for Details". (0.2.8-beta.26, F11.4)
- The title bar: the logo's mark (no words; the Light mark on light pages, the Dark mark on dark ones) left of the title, the title in the logo's colors, the version in the footer with ©
  CalendarStream; a matching favicon, one transparent file for light and dark. (0.2.8-beta.26, F11)
- Trash icons: the icon's lines tinted red (30% `--bad` in `--muted`, at least 3:1), the button itself unchanged; fully red on
  hover. (0.2.8-beta.26, F12.6)
- A section or module left open folds again after 24 hours. (0.2.8-beta.26, F20)
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
- Fields everywhere, pop-ups included: a 12 px muted label over a 34 px field, 1 px apart; a value that
  can't be changed (an event's calendar) is plain text. Related fields share a line (Calendar | Title,
  Location beside the event's color, link and duplicate; Starts | Ends, each with its Time under it). (Picture 2·1)
- Every section's + is in its top right corner (Calendars, Feeds, All Rules, Event Templates, the calendar). The calendar's search
  icon sits left of its Time Zone. (Part 1)
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
- Every date range has All: From | To | ☐ All (search, Print Preview, Import). (Picture 2·14) A feed module's Include says it in words instead: Dates (optional; empty = all), From over To (0.2.8-beta.17).
- No browser alert or confirm boxes: every question and notice is the page's own pop-up. (Picture 2·11)
  Deleting or hiding an event asks the question, a note in muted words on the line under it, and No | Yes
  as the 130 × 34 Cancel/Save buttons (0.2.8-beta.23, F16).
- (i) is info (what the module is, then your note); (?) is help (how to). (Pictures 2·9, 2·12)
- Every + opens a centred pop-up, the page dimmed and out of focus behind it. (Picture 2·11)
- Every border is 1 px wide, sections and modules included. (0.2.8-beta.26, F21; Picture 2·4)
- A module's name is its label: plain text until the module is expanded, then a field of the same size. (Picture 2·9)
- One color palette everywhere: Google Calendar's 11 colors, in the color box. (Picture 2·11)
- A deleted event stays struck through and greyed, saying where it was deleted, with Restore, until its
  Undo pops off History. (0.2.8-beta.31, I3: an event added here and deleted here is not drawn at all; History › Undo still brings it
  back.) (Picture 2·15)
- Importing a calendar file is one row in every calendar: heading, the file field filling the line, the
  dates, the button on the right (CCS+: Manual Upload). (Picture 2·14)
- Emoji: the common ones, then a rounded "Search for more emojis" field that opens every emoji, ten a line, scrolling, filtered as you type. (Picture 2·11)
- Emoji older Windows may not draw (newer than Emoji 12.0, and flags): a small i at the emoji's upper right in the
  list, and the page's own (i) beside the field when one is chosen, both "May not show on older Windows". (0.2.8-beta.19, F8)
- A Google module's colors end with a muted line, "Color change does not carry to Google", while Google refuses the
  color: only after it refused the RGB color, the nearest calendar color and a full update (0.2.8-beta.21, I1).
  (0.2.8-beta.19, I1.1)
- Spacing: 5 px between parts, 1 px between a label and its field, 9 px inside a module's border (5 px top and
  bottom), 12 px inside pop-ups; nothing extra. (0.2.8-beta.21, R11, F9; Picture 2·9)
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
  bottom left, the Cancel/Save buttons at the right. On a phone, one column. (0.2.8-beta.22, F11; Picture 2·16)
  The end's column: Time with All-day Event on its label line, right of "Time *" (ticked, it stays there as the Time
  fields hide); Different end time zone beside Time zone's field, End time zone under it when ticked. (0.2.8-beta.24, F5)
- Sections and modules are told apart by color, nothing else changing: each section's 1 px border its own muted
  color (35%) on `--card`; each calendar's or feed's module bordered in its color at 45%, its header tinted 6% and the rest
  3%; light and dark. (0.2.8-beta.24, F7; 0.2.8-beta.26, F10, F12.3; Pictures 2·2, 2·9)
- The 2/3-line (0.2.8-beta.28, F31): the status lines of every module and section share a standard width, shown only while collapsed. The current presentation is unboxed and right-aligned next to its Status/Action box (I27 below supersedes the original border/fill and centring). (Picture 2·9)
- The On | Off switch (0.2.8-beta.28, F25): at the upper right of an expanded module, like the 12h | 24h switch; Off dims the module grey and the setting is never lost. (Picture 2·9)
- The calendar's header (0.2.8-beta.29, F15, F26): the view is a drop-down (Month, Week, 5 days, Day, List), 12h | 24h is a clock icon with the current format in its tooltip. Calendar toolbar icons are 28 px square; the On | Off switch of a module is a 28 px-high segmented control with 8 px corners. Time Zone,
  view, 12h | 24h, search, Print and Full page sit in the right group; the + is the upper right corner. When they do not fit one line the right
  group drops to a second line. (Suites 21, 64)
- The calendar's key (0.2.8-beta.29, F15): two parts under the calendar, Calendars (each with its (i)) and Key (rule colors, Edited, United
  changed it since, Hidden from Google, Deleted), side by side, a thin vertical line between, in as many columns of at most three rows as the
  width needs. In every calendar mode, clicks dim/hide an item's events on the calendar and in Print (F48 supersedes the old Full-page-only restriction). (Suites 21, 64)
- Week and Day show an hourly grid (0.2.8-beta.29, F28): all 24 hours in a scrolling area (it starts at the first event or 7 am), events
  placed by their time, side by side when they overlap, all-day events above. The stretch handle adds height to a day or hour and is kept.
  (Suite 64)
- Full page (0.2.8-beta.29, F27): the Calendar fills the window and every other section is hidden; the button's icon becomes the two-window restore icon. A day is at
  most 2:3 (width:length); extra weeks of the next and the previous month are added until the page is full. (Suite 64)
- Print (0.2.8-beta.29, I11) lays each sheet out for the paper: landscape for the month, week and 5 days, portrait for the day and the
  itinerary; Letter for English, A4 otherwise; one sheet per page, whole titles wrap, a day that would not fit gets smaller type, and
  the paper is white unless Dark is chosen. (Suite 64)
- Administrator (0.2.8-beta.29, F32, F33) is one Settings section: the login and the public addresses in one form. Its Status/Action box says
  Signed in (green; Not signed in in yellow) over Sign out; when something changes, the action half becomes Cancel | Save at the action's text
  size. The current password is asked only when the user name or password changes. (Suite 64)
- Look (0.2.8-beta.29, F14) is the last Settings section: your own logo and favicon (PNG, SVG, WebP, JPEG or ICO up to 256 KB), and
  the buttons' Animation intensity and duration (percent), with Reset to defaults and one Cancel | Save. (Suite 64; 0.2.8-beta.32, F39:
  renamed Appearance; 0.2.8-beta.33, F46: renamed again to Theme, details to follow in 0.3 Theming — same section, same place.)
- Full page's button (0.2.8-beta.31, F34, F35) is in the title bar, left of ☰; its icon becomes Windows' restore down (two squares). In every
  view the page fits the window exactly, with no scrollbar of its own, and the calendar fills the width. (Suite 65)
- The hour height handle (0.2.8-beta.31, I20) is left of the times in Week and Day, inside the gutter's padding: drag it (or ↑ ↓) to make each
  hour 20 to 120 px; the height is kept. (Suite 65)
- Print's orientation (0.2.8-beta.31, I11): Auto (each view's best fit), Landscape or Portrait, one segmented choice in Print Preview; the paper's
  margins are 5 mm, so the sheet uses the page. (Suite 65)
- The reorder grips' side (0.2.8-beta.31, F36.1): ☰ Settings › Look › Reorder grips, Left (the default) or Right; the handle stays in the margin,
  never over a box. (Suite 65)
- The Administrator's status box (0.2.8-beta.31, I22) sits on the section's heading line; while nothing is changed its Cancel | Save are the
  standard ✕ and ✓. (Suite 65)
- The event pop-up's rows (0.2.8-beta.31, I19, I17): All-day Event is on the Ends line and Different end time zone on the end Time's line (a line
  higher each); its icons stay together on one line, shrinking before they wrap. (Suite 65)
- A calendar's On | Off switch and its note (0.2.8-beta.32, I26) sit on one line: the switch, then the note's text, inline. (Suite 66)
- Default (0.2.8-beta.32, I2) greys out and disables, with a tooltip saying why, on any read-only calendar (CCS+, Google, Apple, a feed): events
  can't be added there, so it can't be the default. (Suite 66)
- The calendars module (0.2.8-beta.32, I28) is called Sources. (Suite 66)
- History's Accepted sign-in (0.2.8-beta.32, I29) is a ✓ with no words (the word stays as its tooltip and accessible name). (Suite 66)
- Appearance (0.2.8-beta.32, F39) is Look's new name (translated at Deploy); renamed again to Theme at 0.2.8-beta.33 (F46). (Suite 66)
- Settings (0.2.8-beta.33, F47): Updates is the first section (above Administrator), since it's the one most worth seeing at a
  glance; Theme stays last. (Suite 67)
- Updates' "up to date" status (0.2.8-beta.33, F53) reads the running version itself ("v1.2.3"), not a plain "Up to date" — so
  the version is visible without opening the title bar's own version link. (Suite 67)
- The calendar's view picker (0.2.8-beta.33, F52) is icons, not words: closed, the button shows only the current view's
  Material icon (Month calendar_month, Week view_week, Day view_day, List view_list); open, each choice shows its icon
  left of its word, the same button + menu pattern as ☰ Settings and the language menu. (Suite 67)
- The Calendars and Key footer's dim-and-hide click (0.2.8-beta.33, F48) works in every mode, not just Full page: a
  Calendars or Key item is always the clickable button (F26, F28's "in full page" is gone). (Suite 67)
- Light/Dark/System (0.2.8-beta.33, F57) is one icon, like the calendar's view picker: closed, the button shows only
  the current choice's icon; open, each choice shows its icon left of its word, in a menu next to the language one.
  (Suite 67)
- The stretch handle (0.2.8-beta.33, F51) sits at the bottom of the calendar itself (inside its scrolling body), not
  the bottom of the whole section below the Calendars/Key footer; left by default, right when Reorder grips is Right.
  (Still open: in Week, Day and Itinerary the hours themselves don't yet grow the way Month's day cells do - left for
  a later build.) (Suite 67)
- Changing or setting the public address (0.2.8-beta.33, F56), with Google Calendar API Sync already set up, pops
  up a notice that its redirect URI needs fixing, since the old one no longer matches: the Settings menu opens to
  Google Calendar API Sync (already true of any Administrator save), which redraws at once with its own existing
  "needs fixing" assist box - the pop-up only says to look there, it doesn't duplicate that guidance. (Suite 67)
- View All (0.2.8-beta.33, F50) is an eye icon on the Key title's line, right-aligned, shown only once something is
  dimmed; it clears every dimmed Calendars/Key item at once. The vertical rule between Calendars and Key (F49) now
  sits right after the Calendars list's own width, not stretched out to the middle. (Suite 67)
- A rule's key name (0.2.8-beta.32, F42) is cut to 25 characters, with its full name as the tooltip. (Suite 66)
- Time Zone (0.2.8-beta.32, F41) is a globe icon; its tooltip names the zone, and it opens the same picker. (Suite 66)
- 12h | 24h (0.2.8-beta.32, F43) is one clock icon; its tooltip names the current mode, and it toggles on a click. (Suite 66)
- 12h | 24h (0.2.8-beta.40, F15.2, superseding F43 above): the numbers themselves sit inside a rounded switch, its
  highlight sliding to the one in use, like the On | Off switch - so the current mode shows on the control itself,
  not only in its tooltip. (Suite 21)
- The calendar grid (0.2.8-beta.32, F40) turns the page on a horizontal swipe (left: next, right: previous) on a touch screen; a vertical swipe
  still scrolls. (Suite 66)
- History's headers (0.2.8-beta.32, F44) slide (drag) to reorder, or, focused, move with ← →; Undo starts at the end, not between Type and Event.
  (Suite 66)
- A status word (0.2.8-beta.32, I21) always shows its icon and words together inside a Status/Action button. Elsewhere, it shows icon and words,
  then collapses to just its icon (the words stay as its tooltip and accessible name); how long it shows first follows the Animation duration
  setting. (Suite 66)
- A collapsed status word (0.2.8-beta.33, I21/F45) then vanishes entirely, giving its line the space back, unless it's an ongoing health check
  the Developer should keep seeing (something that can become unhealthy, e.g. CCS+ or a feed's "Validated"); a plain one-off confirmation such
  as History's "Saved" after changing how many changes are remembered goes all the way. (Suite 67)
- Administrator's public addresses (0.2.8-beta.32, I22) are one list of rows (the page's own address first, then any others), each with its own
  trash can; + sits at the end of the first row. Trashing an extra row takes it out; trashing the domain row always clears it instead, never
  removing the row itself (0.2.8-beta.33: it holds the only + button, so removing it would leave no way to ever add one back). (Suite 66, Suite 67)
- The event pop-up's Different end time zone (0.2.8-beta.32, I31) has the tooltip "End Time zone"; the pop-up never resizes as All-day Event or
  Different end time zone are ticked (its height is planned for both on at once). (Suite 66)
- The first theme after install (0.2.8-beta.32, F38) is System. Every section's `.card` padding is 12 px, not 18 (the margin is unchanged); the
  reorder grips sit closer in, at the new padding's edge. (Suite 66)
- The 2/3-line box (0.2.8-beta.32, I27) is invisible now, not boxed: no border, no fill. It sits right-aligned next to its Status/Action
  button instead of centered across the header, and still shows only while collapsed. (Suite 66)
- Cancel in the rule dialog (0.2.8-beta.32, I18), opened from the event pop-up, reopens it exactly as it was, unsaved edits included. (Suite 66)
- Escape in the rule dialog (0.2.8-beta.33, I37) cancels exactly like the Cancel button, not like a plain dialog close: opened from the event
  pop-up, it brings that back too, the same as I18. (Suite 67)
