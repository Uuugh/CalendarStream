# Theme clarifications still to place (temporary)

Where each decision in the legacy `build_rules/theme.md` Clarifications goes, when its feature file is converted. Delete a line when its row exists. The generic decisions are already UI-25 to UI-36 and THM-01 to THM-09. Items marked (old) are history, superseded or already covered, and are dropped.

**calendar.md**
- The view picker is icons: closed it shows only the current view's icon (Month calendar_month, Week view_week, Day view_day, List view_list); open, each choice shows its icon left of its word. 12h | 24h is one hollow clock icon with the current format as a badge, its tooltip names the mode; Time Zone is a globe whose tooltip names the zone and opens the same picker. When the right zone's controls do not fit one line the right group drops to a second line.
- Week and Day show an hourly grid: all 24 hours in a scrolling area that starts at the first event or 7 am; events placed by time, side by side when they overlap, all-day events above. The hour-height handle sits left of the times.
- Full page: the Calendar fills the window and every other section is hidden; a day is at most 2:3 (width:length) and weeks of the next and previous month are added until the page is full; the page fits the window with no scrollbar of its own. The Full page button is in the top bar, left of the menu, and its icon becomes the restore-down icon.
- Today has a 2 px accent border around its whole day, as well as its filled date.
- The grid turns the page on a horizontal swipe on a touch screen (left: next, right: previous); a vertical swipe still scrolls.
- The stretch control: see UI-16 (twelve dots, a fixed collapse and a fixed expand arrow); Collapse goes to the fewest lines the view needs, Expand to the window's bottom.
- (old) the search icon left of Time Zone (Search is global, SRH-01); (old) pixel stretch limits.

**calendar_filter.md**
- The key has two parts under the calendar, Calendars (each with its (i)) and Key (rule colors, Edited, changed by the source since, Hidden from Google, Deleted), side by side with a thin vertical line, in columns of at most three rows; a click dims or hides an item's events on the calendar and in Print, in every mode. View All (an eye icon on the Key title's line, shown only when something is dimmed) clears every dimmed item. A rule's key name is cut to 25 characters with its full name as the tooltip. The header shows the title and controls only; the filter lists calendars and event states only, no Timed, All-day or Added color labels.

**events.md**
- The event dialog: ← and the title, with its tools in the upper right (Choose from template, Print, Duplicate); fields on the left, Notes on the right as tall as them (dragging Notes taller grows the dialog); Link to below, closed until Event or Rule; Delete (Hide or Show for a calendar source's event, with its (i)) at the bottom left; Cancel | Save at the right; one column on a phone. All-day Event sits on the Ends line and Different end time zone on the end Time's line; the dialog never resizes as they are ticked; its icons stay on one line, shrinking before they wrap. An opened event shows Close at the bottom left and its icons on the right.
- A deleted event stays struck through and greyed, saying where it was deleted (CalendarStream, Google Calendar, United, the feed), with Restore, until its Undo leaves History; an event added here and deleted here is not drawn at all (History Undo brings it back).
- Cancel in the rule dialog opened from the event dialog reopens the event exactly as it was, unsaved edits included; Escape does the same (UI-02).

**history.md**
- History is a table Time | Type | Event | Undo, with a filter (UI-21: type, words, time) on top; folded it shows the latest lines with Undo and Redo where they apply, newest first (a stack); something done outside CalendarStream has no Undo icon and Restore is on the event. The column headers slide to reorder, or move with the left and right arrows when focused; Undo starts at the end. An accepted sign-in is a ✓ with no words. History's three latest lines sit left-aligned before its Healthy box.

**settings.md**
- Settings order: Updates first, then Login & password, Domains, Theme last, then other modules; Login & password has its status box, Sign out and login fields, Domains one list of address rows (+ at the end of the first row; trashing the domain row clears it, never removes it); each has its own Cancel | Save; the current password is asked only when the user name or password changes. Updates reads the running version ("v1.2.3"), not a plain "Up to date". Theme: your own logo and favicon (PNG, SVG, WebP, JPEG or ICO up to 256 KB), Animation intensity and duration, Reorder grips Left or Right, Reset to defaults. The first theme after install is System.
- Changing the public address with Google API Sync set up pops up a notice pointing at the module's assist box (SET-04).

**sources.md, feeds.md, google.md**
- A credentials row (Client ID / secret) ends with a trash that asks before deleting; a Settings part that works shows everything at once, nothing under Expand, with its Remove (red, lower left) and its options beside it. A row of settings that belong together is one line (Check for updates [Hourly] ☐ Auto-update).
- The flows of the Status/Action buttons (theme section 7): Sync Now, Check now, Update now, Connect, Remove a calendar, Import.


**shell.md**: the title bar has the logo's mark (the Light mark on light pages, the Dark mark on dark ones) left of the title, the title in the logo's colors, the version and © in the footer, one transparent favicon for both; sections say "Expand to Configure" (Calendars, Feeds, All Rules, Event Templates) or "Expand for Details" (History); every section's header reads icon · title · space · status lines · health · + (Calendars and Feeds have no status lines; All Rules and Event Templates up to three, the conflicts or errors, otherwise how many; + top right).
