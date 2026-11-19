# Requirements: calendar

Month, week, day and list views, the stretch bar, print. Issues against this feature (kept in the issues database): I43, I44, I49 (stretch), I35 and I46 (icon alignment).

Terms: the **Local time zone** is defined in TIM-03; an **event line** is one event's line height, with its padding and margins, defined in the theme; **Itinerary** is a printed list of events grouped by day.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CAL-01 | proposed | The calendar shows the user's events in the view the user chooses and lets them move to any date. | — | — |
| CAL-01.a |  | The calendar displays the events of its source calendars, as far as the Calendar filter (FLT-01) and event visibility (CAP-02) allow. | — | S26-12 |
| CAL-01.b |  | Month, Week, 5-day (Monday through Friday), Day and List can be selected from the shared dropdown (UI-12); the chosen view is indicated as selected. Week, 5-day and Day provide an hourly view. | — | S26-60, S64-01, S64-03, S67-35, S67-40, S33-16, S33-17 |
| CAL-01.c |  | Week view shows its date range and navigates backward and forward by one week. | — | S26-61 |
| CAL-01.d |  | Selecting a month and year navigates the calendar to that month and year; date selection follows UI-09. | — | S21-01, S21-02, S21-03 |
| CAL-01.e | proposed | Today returns the main calendar to the current month. | — | changelog_gaps_2101-2336:35 |
| CAL-01.f | proposed | Before the user has chosen a view, a phone-width window (DEF-01) opens the calendar in List view. | — | changelog_gaps_1501-1800:18 |
| CAL-01.g | proposed | A day cell shows how many of its visible events do not fit; event visibility follows CAP-02 and the Calendar filter. | — | changelog_gaps_301-600:15 |
| CAL-01.h |  | Week and Day show an hourly grid: every hour of the day in a scrolling area that starts at the first event or at the hour in DEF-01; events are placed by their time, side by side when they overlap, and all-day events sit above. | — | theme.md Clarifications |
| CAL-01.i |  | Today is marked by a filled date and an accent border around its whole day (THM-04.e). | — | theme.md Clarifications |
| CAL-01.j |  | On a touch screen a horizontal swipe on the calendar turns the page (left: next, right: previous); a vertical swipe still scrolls. | — | theme.md Clarifications |
| CAL-02 | proposed | The calendar shows times in the Local time zone (TIM-03), and the user can look at another zone for a while. | — | — |
| CAL-02.a |  | Selecting a time zone in the calendar's own picker shows event times in that zone as a temporary view change; the Time Zones setting (SET-02) is not changed. | — | S19-31; Developer, Nov 17 |
| CAL-03 | proposed | The user can move an event they may edit by pressing and dragging it. | — | — |
| CAL-03.a |  | A long-press-drag moves an event, for the events that can be edited (CAP-01). | — | F61 |
| CAL-03.b |  | In Week and Day the start snaps to the drag step in DEF-01. | — | — |
| CAL-03.c |  | In Month the event moves to the day it is dropped on and keeps its time. | — | — |
| CAL-03.d |  | The press must be held for the long-press time set in Settings > Theme (SET-03, DEF-01). | — | — |
| CAL-04 | proposed | The user can change how tall the calendar is, and Full page gives it the whole window. | — | — |
| CAL-04.a | planned | The Full page icon hides every other section and becomes the restore-down icon (two squares) while it is on. Full page always resizes to the available window; that is its definition. | — | F15.4; S64-04, S65-10, S65-12, S65-13, S65-33, S67-41 |
| CAL-04.b |  | The calendar uses the shared resize bar (UI-16). Its height is measured in event lines, not pixels, changes by whole lines, is saved, and has no fixed pixel minimum or maximum. | — | Developer, Nov 17; S64-06, S79-06, S79-07, S79-08 |
| CAL-04.c |  | Collapse gives the fewest lines the view needs; Expand gives the most lines that fit the visible window. | — | — |
| CAL-04.d |  | The hour height in Week and Day is measured in event lines per hour, changed by whole lines and saved, within the limits in DEF-01, so a line of an event always fits. | — | Developer, Nov 17; S65-14, S65-15 |
| CAL-04.e | proposed | Full page also hides the page footer. | — | changelog_gaps_1-300:36 |
| CAL-04.f |  | In Full page a day is at most 2:3 (width:length), weeks of the next and previous month are added until the page is full, and the page fits the window with no scrollbar of its own. | — | theme.md Clarifications |
| CAL-05 | proposed | The user can print the calendar through Print Preview (PRT-01). | — | — |
| CAL-05.a |  | Until the user chooses an orientation it is automatic: landscape for Month, Week and 5-day sheets, portrait for Day and Itinerary sheets (PRT-01.c). | — | S65-18..22 |
| CAL-05.b | proposed | The views that can be printed are the calendar's views (CAL-01.b) and Itinerary, which lists events grouped by day. | — | S36-33, readme_gaps:53, changelog_gaps_1201-1500:16 |
| CAL-05.c |  | Printing two months produces a sheet for each month. | — | S36-32 |
| CAL-05.d | proposed | Print All sets the date range (UI-23) from the first event through the last event. | — | readme_gaps:52 |
| CAL-05.e | proposed | Printing one event uses Day view for that print (EVT-06). | — | changelog_gaps_301-600:43 |
| CAL-06 | proposed | The calendar header's right zone holds the view controls in a fixed order, and what the user chooses with them stays on the device until the user changes it. | — | — |
| CAL-06.a | proposed | The right zone holds, in this order: Time Zone, View, 12/24 clock, Print, Full page, and + last (UI-24). Zone alignment and stacking follow UI-14; what each control does is in its own requirement (CAL-02.a, CAL-01.b, TIM-10, CAL-05, CAL-04). | — | theme.md 13c (to confirm) |
| CAL-06.b | proposed | The state of each right-zone control that holds one (the time zone, the view, the time format, Full page) is a user setting (SET-01). A default is stated in the control's own requirement. | — | Developer, Nov 18 |
| CAL-06.c |  | The view picker shows icons, not words: closed it shows only the current view's icon (Month calendar_month, Week view_week, Day view_day, List view_list); open, each choice shows its icon left of its word. The 12h \| 24h control is one hollow clock icon with the current format as a badge, and its tooltip names the mode. Time Zone is a globe whose tooltip names the zone and which opens the zone picker. When the right zone's controls do not fit on one line the right group drops to a second line. | — | theme.md Clarifications |

