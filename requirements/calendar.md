# Requirements: calendar

Month, week, day and list views, the stretch bar, print.

Terms: the **Local time zone** is defined in TIM-03; an **event line** is one event's line height, with its padding and margins, defined in the theme; **Itinerary** is a printed list of events grouped by day.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CAL-01 | proposed | The calendar shows the user's events in the view the user chooses and lets them move to any date. | — | — |
| CAL-01.a | backlog | The calendar displays the events of its source calendars, as far as the Calendar filter (FLT-01) and event visibility (CAP-02) allow. | — | S26-12 |
| CAL-01.b | backlog | Month, Week, 5-day (Monday through Friday), Day and List can be selected from the shared dropdown (UIC-12); the chosen view is indicated as selected. Choosing a view closes the menu and shows it at once (UIC-13). Week, 5-day and Day provide an hourly view. | — | S26-60, S64-01, S64-03, S67-35, S67-40, S33-16, S33-17 |
| CAL-01.c | backlog | Week view shows its date range and navigates backward and forward by one week. | — | S26-61 |
| CAL-01.d | backlog | Selecting a month and year navigates the calendar to that month and year; date selection follows UIC-09. | — | S21-01, S21-02, S21-03 |
| CAL-01.e | proposed | Today returns the main calendar to the current month. | — | changelog_gaps_2101-2336:35 |
| CAL-01.f | proposed | Before the user has chosen a view, a phone-width window (DEF-01) opens the calendar in List view. | — | changelog_gaps_1501-1800:18 |
| CAL-01.g | proposed | A day cell shows how many of its visible events do not fit; event visibility follows CAP-02 and the Calendar filter. | — | changelog_gaps_301-600:15 |
| CAL-01.h | backlog | Week and Day show an hourly grid: every hour of the day in a scrolling area that starts at the first event or at the hour in DEF-01; events are placed by their time, side by side when they overlap, and all-day events sit above. | — | theme.md Clarifications |
| CAL-01.i | backlog | Today is marked by a filled date and an accent border around its whole day (THM-04.e). | — | theme.md Clarifications |
| CAL-01.j | backlog | On a touch screen a horizontal swipe on the calendar turns the page (left: next, right: previous); a vertical swipe still scrolls. A swipe counts only when it meets the swipe size in DEF-01; a swipe with more than one finger is ignored. | — | theme.md Clarifications |
| CAL-02 | proposed | The calendar shows times in the Local time zone (TIM-03), and the user can look at another zone. | — | — |
| CAL-02.a | backlog | Selecting a time zone in the calendar's own picker shows event times in that zone as a view choice kept on the device (CAL-06.b); the Time Zones setting (SET-02) is not changed. | — | S19-31; Developer, Nov 17 |
| CAL-03 | proposed | The user can move an event they may edit by pressing and dragging it. | — | — |
| CAL-03.a | backlog | A long-press-drag moves an event, for the events that can be edited (CAP-01). | — | F61 |
| CAL-03.b | backlog | In Week and Day the start snaps to the drag step in DEF-01. | — | — |
| CAL-03.c | backlog | In Month the event moves to the day it is dropped on and keeps its time. | — | — |
| CAL-03.d | backlog | The press must be held for the long-press time set in Settings > Theme (SET-03, DEF-01). | — | — |
| CAL-04 | proposed | The user can change how tall the calendar is, and Full page gives it the whole window. | — | — |
| CAL-04.a | proposed | The Full page icon hides every other section and becomes the restore-down icon (two squares) while it is on. Full page always resizes to the available window; that is its definition. | — | F15.4; S64-04, S65-10, S65-12, S65-13, S65-33, S67-41 |
| CAL-04.b | backlog | The calendar uses the shared resize bar (UIC-16). Its height is measured in event lines, not pixels, changes by whole lines, is saved, and has no fixed pixel minimum or maximum. | — | Developer, Nov 17; S64-06, S79-06, S79-07, S79-08 |
| CAL-04.c | backlog | Collapse gives the fewest lines the view needs; Expand gives the most lines that fit the visible window. | — | — |
| CAL-04.d | backlog | The hour height in Week and Day is measured in event lines per hour, changed by whole lines and saved, within the limits in DEF-01, so a line of an event always fits. | — | Developer, Nov 17; S65-14, S65-15 |
| CAL-04.e | proposed | Full page also hides the page footer. | — | changelog_gaps_1-300:36 |
| CAL-04.f | backlog | In Full page a day is at most 2:3 (width:length), weeks of the next and previous month are added until the page is full, and the page fits the window with no scrollbar of its own. | — | theme.md Clarifications |
| CAL-05 | proposed | The user can print the calendar through Print Preview (PRT-01). | — | — |
| CAL-05.a | backlog | Until the user chooses an orientation it is automatic: landscape for Month, Week and 5-day sheets, portrait for Day and Itinerary sheets (PRT-01.c). | — | S65-18..22 |
| CAL-05.b | proposed | The views that can be printed are the calendar's views (CAL-01.b) and Itinerary, which lists events grouped by day. | — | S36-33, readme_gaps:53, changelog_gaps_1201-1500:16 |
| CAL-05.c | backlog | Printing two months produces a sheet for each month. | — | S36-32 |
| CAL-05.d | proposed | Print All uses the empty date range (UIC-23, All), which prints from the first event through the last event. | — | readme_gaps:52 |
| CAL-05.e | proposed | Printing one event uses Day view for that print (EVT-06). | — | changelog_gaps_301-600:43 |
| CAL-06 | proposed | The calendar header's right zone holds the view controls in a fixed order, and what the user chooses with them stays on the device until the user changes it. | — | — |
| CAL-06.a | proposed | The right zone holds, in this order: Time Zone, View, 12/24 clock, Print, Full page, and + last (UIC-24). Zone alignment and stacking follow UIC-14; what each control does is in its own requirement (CAL-02.a, CAL-01.b, TIM-10, CAL-05, CAL-04). | — | theme.md 13c (to confirm) |
| CAL-06.b | proposed | The state of each right-zone control that holds one (the time zone, the view, the time format, Full page) is a user setting (SET-01). A default is stated in the control's own requirement. | — | Developer, Nov 18 |
| CAL-06.c | backlog | The view picker shows icons, not words: closed it shows only the current view's icon (Month calendar_month, Week view_week, Day view_day, List view_list); open, each choice shows its icon left of its word. Its tooltip is msg:viewTooltip, where {name} is the current view's name (msg:viewMonth, msg:viewWeek, msg:viewFiveDay, msg:viewDay or msg:viewList), and its accessible name is msg:viewName. The 12h \| 24h control is one hollow clock icon with the current format as a badge, and its tooltip names the mode. Time Zone is a globe whose tooltip names the zone and which opens the zone picker. When the right zone's controls do not fit on one line the right group drops to a second line. | — | theme.md Clarifications |
| CAL-01.k | proposed | Until the user chooses a view, the calendar is in Month view (CAL-01.f says what a phone-width window starts with). | — | R2 gap |
| CAL-01.l | proposed | The top left of the calendar header holds, in this order: the previous button, the next button, Today (msg:today) and then the title. | — | R2 gap |
| CAL-01.m | proposed | Previous and next move by one month in Month and List (to the last day of the previous month, or the first day of the next), by one week in Week and by one day in Day. | — | R2 gap |
| CAL-01.n | proposed | The tooltip and accessible name of previous and next name the step of the view: msg:previousMonth and msg:nextMonth (Month, List), msg:previousWeek and msg:nextWeek (Week), msg:previousDay and msg:nextDay (Day). | — | R2 gap |
| CAL-01.o | proposed | The calendar shows only dates in the supported years in DEF-01; a date outside them, or none, puts the calendar on today. | — | R2 gap |
| CAL-01.p | proposed | Selecting a month in the picker puts the calendar on the 1st of that month, or on today when it is the current month. | — | R2 gap |
| CAL-01.q | proposed | The title of Month and List is the month name and year, first letter capitalised, in the page language; the title of Day is the weekday, month, day and year in the page language. | — | R2 gap |
| CAL-01.r | proposed | The month picker's year row has msg:previousYear and msg:nextYear buttons that change the shown year by one with no limit; the shown year starts at the displayed month's year each time the picker opens. | — | R2 gap |
| CAL-01.s | proposed | The month picker shows the page language's twelve abbreviated month names in calendar order, with the displayed year and month marked. | — | R2 gap |
| CAL-04.g | proposed | Stretching enlarges the calendar by dividing the added height equally among the displayed weeks in Month, and enlarges the scrolling hour area in Week and Day. | — | R2 gap |
| CAL-04.h | proposed | Only Month adds weeks in Full page (CAL-04.f). Week and Day limit the hour area to the available height (at least the hour area minimum in DEF-01), and List scrolls inside the available height. | — | R2 gap |
| CAL-04.i | proposed | The available height in Full page is the window's height minus the calendar body's top, the key's height and the margin in DEF-01, and is at least the Full page height minimum in DEF-01. | — | R2 gap |
| CAL-04.j | proposed | The resize bar is not shown in Full page or in List. | — | R2 gap |
| CAL-04.k | proposed | Full page is fitted again when the window is resized (after the delay in DEF-01) and when fonts finish loading. | — | R2 gap |
| CAL-04.l | proposed | In Full page a Month day cell has no minimum height and scrolls its own content. | — | R2 gap |
| CAL-06.d | proposed | The right zone decides again whether its controls fit on one line when the window is resized (after the delay in DEF-01) and when fonts finish loading. | — | R2 gap |
| CAL-06.e | proposed | The 12h \| 24h control sets 12-hour or 24-hour and never returns to the default of TIM-10. | — | R2 gap |
| CAL-07 | proposed | Each view shows its days and cells as the rows below say. | — | R2 gap |
| CAL-07.a | proposed | Month shows whole weeks, Sunday first, from the Sunday on or before the 1st to the Saturday on or after the last day: 4 to 6 weeks. | — | R2 gap |
| CAL-07.b | proposed | Week shows the seven days, Sunday to Saturday, that contain the date. | — | R2 gap |
| CAL-07.c | proposed | List shows one row for each day of the date's month that has events; a month with none shows msg:noEventsThisMonth. | — | R2 gap |
| CAL-07.d | proposed | Weekday headings are the page language's two-letter day names, Sunday first. | — | R2 gap |
| CAL-07.e | proposed | In Month, days outside the displayed month have a muted background and a muted day number. | — | R2 gap |
| CAL-07.f | proposed | A Month day cell shows its day number and a + that opens Add event for that day (msg:addAnEventOn, {day} is the day); the + shows on hover or focus, and dimmed but always on a device without hover. | — | R2 gap |
| CAL-07.g | proposed | Clicking an empty spot of a Month day cell, a Week or Day column or an all-day cell opens Add event for that date (EVT-01.a); the Month cell's tooltip is msg:clickAnEmptySpotTo ({day} is the day). | — | R2 gap |
| CAL-07.h | proposed | A List row shows the day number, the day text and a + as in CAL-07.f; the date sits above its events in a window no wider than the narrow list width in DEF-01, and in a column of the date column width in DEF-01 beside them otherwise. | — | R2 gap |
| CAL-07.i | proposed | In the page the Month grid is at least the Month grid width in DEF-01 and scrolls sideways when the area is narrower; in Full page it fits the window (CAL-04.f). | — | R2 gap |
| CAL-07.j | proposed | In Month, all-day and timed events look alike: each is a one-line colored bar. | — | R2 gap |
| CAL-08 | proposed | An event is shown on the days it covers, in order. | — | R2 gap |
| CAL-08.a | proposed | An event is shown on every day it covers in the displayed zone (CAL-02), from its first day to its last. | — | R2 gap |
| CAL-08.b | proposed | A timed event's last day is the day of its end; an end exactly at midnight does not include the new day, and an end at or before the start leaves the event on its start day only. | — | R2 gap |
| CAL-08.c | proposed | An all-day event covers its start date up to the day before its end date, and at least its first day. | — | R2 gap |
| CAL-08.d | proposed | Within a day, events are in the order of their start. | — | R2 gap |
| CAL-09 | proposed | Each event line shows a time label, the title and marks. | — | R2 gap |
| CAL-09.a | proposed | An event line wraps in the hourly grid, in List and in all-day cells, and is cut with an ellipsis in Month. | — | R2 gap |
| CAL-09.b | proposed | The tooltip of an event line is msg:eventLineTooltip, where {title} is the title and {state} is where the event was deleted (EVT-07.c) or msg:hiddenFromGoogle; an event that is neither deleted nor hidden has the title alone. | — | R2 gap |
| CAL-09.c | proposed | A timed event within one day is labelled "start–end"; across days the first day is labelled "start →", the last "→ end" and the days between msg:cont. | — | R2 gap |
| CAL-09.d | proposed | A single-day all-day event has no label; a multi-day all-day event has none on its first day and msg:cont on each following day. | — | R2 gap |
| CAL-09.e | proposed | After the title come marks: a warning when the source changed an edited event (msg:unitedChangedThisSinceYour for United's schedule, msg:feedChangedThisSinceYourEdit for another source); else an edit icon (msg:editedHere); else, for an event added by a rule, an icon with msg:addedByRule. A deleted event shows none of these. | — | R2 gap |
| CAL-09.f | proposed | An event with reminders shows a reminder icon (msg:hasReminders) after the other marks. | — | R2 gap |
| CAL-10 | proposed | The hourly grid places each timed event by its minutes. | — | R2 gap |
| CAL-10.a | proposed | Hour labels run from midnight to 11 pm in the time format (TIM-10): 12am to 11pm, or 00:00 to 23:00; the midnight label is hidden. | — | R2 gap |
| CAL-10.b | proposed | A timed event starts at its minutes from the start of the day and is as tall as its duration, at least the shortest drawn event in DEF-01; an event that continues past midnight is cut at 24:00 and continues from 00:00 on the next day. | — | R2 gap |
| CAL-10.c | proposed | The scrolling hour area is at most the hour area height in DEF-01 plus the stretch (CAL-04.g), or the available height in Full page (CAL-04.h). | — | R2 gap |
| CAL-10.d | proposed | An opened event expands to the full column width and its own height, with a shadow, above the others (THM-10.d). | — | R2 gap |
| CAL-11 | proposed | Events that overlap in time in Week and Day are placed side by side in lanes. | — | R2 gap |
| CAL-11.a | proposed | Lanes exist only in Week and Day, are worked out for each day, and a multi-day event has its own segment, and lane, on each day. | — | R2 gap |
| CAL-11.b | proposed | The timed events of one day are ordered by start, and by longer first when the start is the same. | — | R2 gap |
| CAL-11.c | proposed | A cluster is a run of overlapping events; a new cluster starts when an event starts at or after the latest end of the current cluster, so events that touch do not overlap. | — | R2 gap |
| CAL-11.d | proposed | An event takes the first lane, counted from 0, whose last event ends at or before its start, or a new lane. | — | R2 gap |
| CAL-11.e | proposed | Every event of a cluster has the cluster's number of lanes (at least 1); its width is 1 over that number of the column less the lane gap, and its left edge is its lane over that number of the column plus the lane offset (THM-10.e). | — | R2 gap |
