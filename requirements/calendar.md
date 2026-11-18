# Requirements: calendar

Month, week, day and list views, the stretch bar, print. (Moved Nov 17: CAL-03, CAL-47..51 to search.md as SRH; CAL-06, 07, 08, 10, 37, 38, 54, 55, 56 to calendar_filter.md as FLT.) Issues against this feature (kept in the issues
database): I43, I44, I49 (stretch), I35 and I46 (icon alignment).

| ID | status | statement | test | was |
|---|---|---|---|---|
| CAL-01 | planned | A space separates the date picker and Time Zone; when the top line does not fit, its right half goes under the +, right-aligned. | — | F15.1 |
| CAL-02 | built | The 12 h / 24 h choice is one outlined clock icon with a 12 or 24 badge showing the current setting; clicking it toggles between the two. | — | F15.2, F43 |
| CAL-04 | planned | A Full page icon sits right of Print; it hides every other section and becomes a Back icon. | — | F15.4 |
| CAL-05 | planned | The lower-left (?) is removed. | — | F15.5 |
| CAL-09 | built | The footer's vertical rule is centered by default and moves only to make room for extra calendars or keys. | — | F49 |
| CAL-11 | built | The calendar's stretch control is a bar centered at the bottom of the calendar (not the module), independent of the left/right grips setting, drawn as two rows of six dots like a slider's. | — | F51 |
| CAL-12 | built | The stretch bar can compress the calendar enough to remove the module's vertical scrollbar. | — | F51 |
| CAL-13 | built | Beside the stretch bar, arrows point up when the calendar is expanded (click: collapse to minimum height) and down when it is collapsed (click: expand to the bottom of the visible browser window). | — | F51 |
| CAL-14 | built | The view selector (Month, Week, Day, List) shows only the current view's Material icon when closed; each open choice shows its icon left of its word. | — | F52 |
| CAL-15 | planned | Long-press-drag moves an event, and a Theme setting sets how long the press must be held. | — | F61 |
| CAL-19 | planned | Local time: the calendar shows event times in the Local time zone, set in Settings > Time Zones (SET-47): the zone of the device in use, or a fixed zone. Existing events are viewed with the offset of that zone, while each event keeps, unchanged in the database, the time zone it was created in until the user edits it with Edit Event. (Developer, Nov 17) | — | S19-01 |
| CAL-65 | planned | An all-day (24-hour) event is shown like any timed event in the Local time zone, so it is a single day while the Local zone is the event's own zone, and can span two calendar days when the Local zone differs (for example a New York all-day event viewed from Los Angeles). (Developer, Nov 17) | — | Developer |
| CAL-25 | planned | Selecting a time zone in the calendar's own picker shows event times in that zone as a temporary view change; the Time Zones setting (SET-47) is not changed. | — | S19-31; Developer, Nov 17 |
