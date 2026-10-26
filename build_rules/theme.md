# Theme

Read before changing how the page looks.

- The rules, measured from the page itself, are in the **CalendarStream Theme Rules** picture:
  `build_rules/CalendarStream_Theme_Rules_Light.png` and `…_Dark.png`. Part 1 is the whole page with
  each part named where it is (top bar, calendar, sections, section header, module, module header,
  subsection, fields, instruction tile, Expand and Close bars, rule line, footer…) and a module open
  in every section; part 2 gives the rules, ending with the Clarifications below.
- In short: IBM Plex Sans (IBM Plex Mono for what's typed or copied exactly), Material Symbols
  icons only, rounded rectangles only (8 px controls, 12 px sections and modules; no pills), 50 px
  module headers, 34 px controls, 5 px between modules and groups, colors only from the tokens in
  `app/templates/_theme.html` (each with a light and a dark value).
- The page's stylesheet is `app/static/app.css`; its script is `app/templates/page.js` (made once per
  language). Both are cached by the browser for a version, so change them, never inline copies.
- When the theme changes, redraw the picture (Deploy step e at the latest) and update this file.

## Enforced by tests

The theme defines one consistent look **and interaction**; it is checked, not just described.

- `tests/suite_44.py` (the theme suite) checks the whole page, light and dark, against the rules here:
  each Clarification below has at least one check in it. A new Clarification gets its check in the
  same beta; a change that breaks one fails `tests/run.sh`, so it can't be published.
- Every page change is checked in the states the Developer sees, not only on a fresh page: after the
  change's own action, after an in-place redraw (a Save, Check now, Sync Now), after an update, on a
  phone (390 px) and in dark.
- Before writing any new part, Claude reads this file and finds the existing part it should behave
  like (a status-box button → Sync Now; a field row → the login; a list → handles); a new part copies
  that part's look and interaction instead of inventing its own.

## Clarifications

The Developer's decisions about how the page looks. Always keep them: every change follows them, and
the picture's part 2 shows this list (it's read from here when the picture is drawn). Add each new
one here.

- Module handles (▲ ☰ ▼) sit in the section's right margin: they take up no extra space, and modules
  (and All Rules' lines) are as wide as the section header (their right edge lines up with its +).
  No handle where there's nothing to reorder (a list of one).
- Calendar and feed module headers share one layout. Line 1: the color (calendars only), the module's
  kind (fixed text, 17 px, 15 on a phone where it may take two lines: CalendarStream, United Airlines CCS+, Google Calendar, Apple Calendar,
  Calendar Feed…), then on the right "Last synced 00:31" and the status box (Healthy…). Line 2: its
  name (a field while expanded) with a raised (i) after it when it has a note (the note is changed
  under Close), then on the right "Next check @ 00:44" and Sync Now. A line with nothing to say is
  left blank.
- Status words: "Last synced 00:31" or "Sync failed 00:31", never "Last check was successful @…";
  a feed says "Last read by Google 00:31" (or "Last read …"); Settings → Updates "Last checked 00:31".
- The status box is a multi-button: an overall status over the action that updates it ("Healthy" over
  Sync Now on United Airlines CCS+ is the model). Wherever an overall status and its update share a
  box, it works the same: every button in a status box (Sync Now, Settings → Check now, Update now,
  any new one) says what it's doing at once (Syncing…, Checking…, Updating…) and grows over the box
  as the status word fades, then pulses green (done) or yellow (failed, or something found) for
  2.4 s, then shrinks back with the box redrawn to the new status. Never a button that gives no sign
  it was pressed, and never a status left showing while its update runs.
- Module-like sections (All Rules, Event Templates): the count box in the top right corner; + in the
  bottom right corner of the open section.
- A box means you can change it: fixed text (a title, the release channel) is plain text, never in a
  field box. A group that looks like a module but has nothing to fold (Settings → Updates) uses the
  module header layout, always open, with no Expand.
- Copy buttons sit inside their field, like the password box's eye. Client ID / secret pairs are laid
  out like a login, connected or not.
- Adding something (+ Add a calendar…) ends with the standard Cancel | Save pair, like editing it.
- After an update the page reloads, so the new version's script and stylesheet run its parts.
- Expand / Close lines: ▸ Expand ◂ points at the words; Close's triangles point up.
- Pop-ups: a dark backdrop (rgba(0,0,0,.55)) that keeps the page in view, and a 200 ms fade and
  scale-up (none with reduced motion). Every Cancel | Save, pop-ups included, is the 130 × 34 pair.
- An opened event: Close in the bottom left corner, its icons (link, reminders, edit, duplicate,
  delete) on the right; when it's too narrow for one line, the icons go on a line above Close.
- Events show the color Google shows: their own, their rule's, else their calendar's.
- Rule lines say what the rule does, titled or not ("Items without an end time → Change length to 1:00").
- Fields everywhere, pop-ups included: a 12 px muted label over a 34 px field, 2 px apart; a value that
  can't be changed (an event's calendar) is plain text. Related fields share a line (Calendar | Title,
  Location beside the event's color, link and duplicate; Starts | Ends, each with its Time under it).
- Every section's + is in a corner: the top right (Calendars, Feeds, the calendar), or the bottom right
  of an open module-like section. The calendar's search icon sits left of its Time Zone.
- A credentials row (Client ID / secret) ends with a trash, which asks before deleting.
- A row of settings that belong together is one line (Check for updates [Hourly] ☐ Auto-update).
- Google calendars say "Next push instantaneous" (each change goes at once).
- A rule's color is one of Google Calendar's 11 event colors; rule lines read "Color ■ (Name)".
- Light is the Soft palette (warm off-white, muted blue accent), still named Light with its icon.
