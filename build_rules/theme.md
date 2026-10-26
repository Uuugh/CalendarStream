# Theme

Read before changing how the page looks.

- The rules, measured from the page itself, are in the **CalendarStream Theme Rules** picture:
  `build_rules/CalendarStream_Theme_Rules.png` (light and dark side by side). Part 1 names the page's parts
  (section, section header, module, module header, color box, status lines, status box, Sync Now,
  handle, Expand / Close line, rule line, count box…); part 2 gives the rules.
- In short: IBM Plex Sans (IBM Plex Mono for what's typed or copied exactly), Material Symbols
  icons only, rounded rectangles only (8 px controls, 12 px sections and modules; no pills), 50 px
  module headers, 34 px controls, 5 px between modules and groups, colors only from the tokens in
  `app/templates/_theme.html` (each with a light and a dark value).
- The page's stylesheet is `app/static/app.css`; its script is `app/templates/page.js` (made once per
  language). Both are cached by the browser for a version, so change them, never inline copies.
- When the theme changes, redraw the picture (Deploy step e at the latest) and update this file.
