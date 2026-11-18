# Requirements: calendar

Month, week, day and list views, the stretch bar, the key, print. Issues against this feature (kept in the issues
database): I43, I44, I49 (stretch), I35 and I46 (icon alignment).

| ID | status | statement | test | was |
|---|---|---|---|---|
| CAL-01 | planned | A space separates the date picker and Time Zone; when the top line does not fit, its right half goes under the +, right-aligned. | — | F15.1 |
| CAL-02 | built | The 12 h / 24 h choice is one outlined clock icon with a 12 or 24 badge showing the current setting; clicking it toggles between the two. | — | F15.2, F43 |
| CAL-03 | planned | Search sits left of Print; when open, From and To appear as hints in the date fields, in the date's format. | — | F15.3 |
| CAL-04 | planned | A Full page icon sits right of Print; it hides every other section and becomes a Back icon. | — | F15.4 |
| CAL-05 | planned | The lower-left (?) is removed. | — | F15.5 |
| CAL-06 | planned | The key shows calendars in columns of three from the left and filters in stacks of three from the right; the calendar row grows one row taller when they do not fit; "struck, grey" reads as Deleted. | — | F15.8 |
| CAL-07 | planned | In Full page, a click on a key item dims it and hides its events there; nothing is deleted. The hidden choices are kept when leaving Full page (see CAL-08). Week and Day have an hourly grid. | — | F15.9 |
| CAL-08 | open | A key item's dim-and-hide works in Month, Full and Config modes, and stays applied on leaving Full page. | — | F48 |
| CAL-09 | built | The footer's vertical rule is centered by default and moves only to make room for extra calendars or keys. | — | F49 |
| CAL-10 | open | A View All (eye) button sits right-aligned in the key's title line, with Calendar and Key; one click clears every dimmed item. | — | F50 |
| CAL-11 | built | The calendar's stretch control is a bar centered at the bottom of the calendar (not the module), independent of the left/right grips setting, drawn as two rows of six dots like a slider's. | — | F51 |
| CAL-12 | built | The stretch bar can compress the calendar enough to remove the module's vertical scrollbar. | — | F51 |
| CAL-13 | built | Beside the stretch bar, arrows point up when the calendar is expanded (click: collapse to minimum height) and down when it is collapsed (click: expand to the bottom of the visible browser window). | — | F51 |
| CAL-14 | built | The view selector (Month, Week, Day, List) shows only the current view's Material icon when closed; each open choice shows its icon left of its word. | — | F52 |
| CAL-15 | planned | Long-press-drag moves an event, and a Theme setting sets how long the press must be held. | — | F61 |
