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

## Clarifications

The Developer's decisions about how the page looks. Always keep them: every change follows them, and
the picture's part 2 shows this list (it's read from here when the picture is drawn). Add each new
one here.

- Module handles (▲ ☰ ▼) sit in the section's right margin: they take up no extra space, and modules
  are as wide as the section header (their right edge lines up with its +).
- Calendar and feed module headers share one layout. Line 1: the color (calendars only), the name,
  then on the right "Last synced 00:31" and the status box (Healthy…). Line 2: the note, then on the
  right "Next check @ 00:44" and Sync Now. A line with nothing to say is left blank.
- Status words: "Last synced 00:31" or "Sync failed 00:31", never "Last check was successful @…";
  a feed says "Last read by Google 00:31" (or "Last read …").
- Module-like sections (All Rules, Event Templates): the count box, then + in the top right corner.
- A box means you can change it: fixed text (a title, the release channel) is plain text, never in a
  field box. A group that looks like a module but has nothing to fold (Settings → Updates) uses the
  module header layout, always open, with no Expand.
- Copy buttons sit inside their field, like the password box's eye.
- A rule's color is one of Google Calendar's 11 event colors; rule lines read "Color ■ (Name)".
- Light is the Soft palette (warm off-white, muted blue accent), still named Light with its icon.
