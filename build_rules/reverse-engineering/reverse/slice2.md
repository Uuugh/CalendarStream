# Slice 2: calendar views, drawing, drag/resize/full page, print, search, filter and key

Row format: | ID | statement | evidence (file:function) |
All paths are under app/ unless stated. "unsure" marks ambiguous code. "Not implemented" rows record claims in the README that the code does not meet.

## Topic 1. Calendar views and navigation

| ID | Statement | Evidence |
|---|---|---|
| R2-01 | The calendar offers these views | |
| R2-01.a | The calendar views are exactly Month, Week, Day and List. | routes/page.py:VIEWS; templates/index/calendar.html (view menu) |
| R2-01.b | A "5 days" calendar view is NOT offered (README says the drop-down has "5 days"; the code has a 5-day option only in Print Preview). Not implemented; unsure whether wanted. | README.md "The status page"; routes/page.py:VIEWS |
| R2-01.c | The view is chosen from a button showing only the current view's icon (Month: calendar_month, Week: view_week, Day: view_day, List: view_list); its tooltip is "View: <name>" and its accessible name is "View". | templates/index/calendar.html (viewbtn) |
| R2-01.d | Pressing the view button opens a menu of the four views, each shown as its icon followed by its word, the current one marked as the checked choice (radio semantics). | templates/index/calendar.html (viewmenu) |
| R2-01.e | Choosing a view closes the menu, saves the choice as the stored default view, and redraws the calendar in place without reloading the page. | js/02-calendar.js:chooseView, loadCal |
| R2-01.f | The view menu also closes on a click outside it or on Escape. | js/02-calendar.js:initCal |
| R2-01.g | The stored default view is Month until one is saved; an unknown stored value is treated as Month. | routes/page.py:ui_view |
| R2-01.h | A view name outside month, week, day, list is refused when saving (error "Unknown view."). | routes/page.py:set_view |
| R2-01.i | A request that names a view shows that view for that request only (the stored default is not changed); an unknown view name falls back to the stored default. | routes/page.py:index |
| R2-01.j | On a screen at most 700 px wide, when no view has ever been explicitly chosen and the calendar would open on Month, it opens on List instead. | js/02-calendar.js (phone default); routes/page.py:index (view_explicit) |
| R2-01.k | The view is saved on the server, so every browser sees the same default view. | routes/page.py:set_view (store ui_view) |
| R2-02 | Navigation: previous, next, Today | |
| R2-02.a | The top-left of the calendar has a previous button, a next button and a "Today" button, then the title. | templates/index/calendar.html (calleft) |
| R2-02.b | Previous and next move by one month in Month and List, by 7 days in Week, by 1 day in Day. | services/calendar_view.py:cal_view (prev, nxt) |
| R2-02.c | In Month and List, previous goes to the last day of the previous month and next goes to the first day of the next month (so the reference date becomes that day). | services/calendar_view.py:cal_view (prev, nxt) |
| R2-02.d | Previous/next tooltips and accessible names are "Previous month"/"Next month" (Month, List), "Previous week"/"Next week" (Week), "Previous day"/"Next day" (Day). | templates/index/calendar.html (step) |
| R2-02.e | "Today" returns to the current date, in the display time zone, in the current view. | templates/index/calendar.html (Today link to "/"); routes/page.py:_parse_day |
| R2-02.f | Previous, next and Today redraw the calendar in place; with Ctrl, Command or Shift held, or a non-primary mouse button, they instead open as an ordinary link (new tab). | js/02-calendar.js (navbtn click handler) |
| R2-02.g | On a touch screen, a horizontal swipe on the calendar body moves to the next period (swipe left) or previous period (swipe right), like the buttons. | js/02-calendar.js (touchstart/touchend) |
| R2-02.h | A swipe counts only when it is at least 50 px horizontally and its horizontal distance is at least 1.5 times its vertical distance; otherwise nothing happens and vertical scrolling is untouched. A swipe that starts with more than one finger is ignored. | js/02-calendar.js (touchend) |
| R2-03 | The date the calendar is around | |
| R2-03.a | The calendar is positioned by a date (year-month-day). If the date is missing or invalid or its year is outside 2000 to 2100 inclusive, the date is today in the display time zone. | routes/page.py:_parse_day |
| R2-03.b | If no valid date is given but a month (year-month) is, the calendar is around the first day of that month, except when that month is the current month, when it is around today. | routes/page.py:_parse_day |
| R2-03.c | A month value is valid only with year 2000 to 2100 inclusive and month 1 to 12; otherwise the current month is used. | services/calendar_view.py:_parse_month |
| R2-03.d | After an in-place redraw the address keeps the date or month but not the view. | js/02-calendar.js:loadCal |
| R2-04 | Title and month picker | |
| R2-04.a | Month and List title: month name and year, first letter capitalised, in the page language (English "October 2026"; Spanish "Octubre de 2026"; French "Octobre 2026"). | services/calendar_view.py:cal_view; i18n.py:Dates.title |
| R2-04.b | Week title: "<weekday> <month> <day> – <weekday> <month> <day>, <year>" from the first (Sunday) to the last (Saturday) day, year of the last day, e.g. "Sun Oct 4 – Sat Oct 10, 2026" (the day text format is language specific). | services/calendar_view.py:cal_view; i18n.py:DATES |
| R2-04.c | Day title: "<weekday> <month> <day>, <year>". | services/calendar_view.py:cal_view |
| R2-04.d | The title is a button (tooltip "Jump to a month") with a drop-down caret; it opens a month picker (a dialog labelled "Jump to a month") with a year row and twelve month buttons. | templates/index/calendar.html (monthwrap) |
| R2-04.e | The year row has "Previous year" and "Next year" buttons changing the shown year by 1 with no limit in the picker; the shown year starts at the displayed month's year each time the picker opens. | templates/index/calendar.html; js/02-calendar.js:initCal |
| R2-04.f | The twelve buttons are the language's abbreviated month names in calendar order; the button of the currently displayed year-month is marked. | js/02-calendar.js:initCal (draw) |
| R2-04.g | Choosing a month goes to the 1st of that month in the current view. | js/02-calendar.js:initCal |
| R2-04.h | The picker closes on an outside click or Escape. | js/02-calendar.js:closeMonthPick |
| R2-04.i | A year outside 2000 to 2100 chosen in the picker makes the calendar open on today's date (the server ignores the date). unsure | routes/page.py:_parse_day |
| R2-05 | What each view shows | |
| R2-05.a | Month shows whole weeks, Sunday first, from the Sunday on or before the 1st to the Saturday on or after the last day; 4 to 6 weeks. | services/calendar_view.py:cal_view |
| R2-05.b | Week shows 7 days, Sunday to Saturday, containing the reference date. | services/calendar_view.py:cal_view |
| R2-05.c | Day shows one day. | services/calendar_view.py:cal_view |
| R2-05.d | List shows, for the month of the reference date, one row per day that has at least one event; with none it says "No events this month." | services/calendar_view.py:cal_view; calendar.html |
| R2-05.e | Weekday column headings are two letters in English, Sunday first: Su Mo Tu We Th Fr Sa (other languages have their own). | i18n.py:DATES |
| R2-05.f | In Month, days outside the displayed month have a muted background and muted day number. | calendar.html; styles/04-calendar.css |
| R2-05.g | Each Month day cell shows the day number and a small "+" (tooltip "Add an event on <day>") that is visible on hover or focus, and always visible (at reduced opacity) on devices without hover. | calendar.html; styles/04-calendar.css |
| R2-05.h | A Month cell's tooltip is "Click an empty spot to add an event on <day>"; clicking an empty part of a day cell, a Week or Day column or an all-day cell opens Add event for that date (not when the click is on an event, link or button). | calendar.html; js/08-events.js |
| R2-05.i | A "+" in the top right corner of the calendar (tooltip "Add an event") opens Add event for today in the display time zone. | calendar.html (calplus) |
| R2-05.j | List rows show the day number, the day text (e.g. "Mon Oct 5") and a hover "+" for that day; a day with no events does not appear in List (a row with "No events." only appears for a day that is passed in without events). | calendar.html; services/calendar_view.py:cal_view |
| R2-05.k | On screens at most 600 px wide a List row's date sits above its events instead of beside them; the date column is 150 px otherwise. | styles/04-calendar.css |
| R2-06 | The top line layout | |
| R2-06.a | Right of the title, in order: Time Zone (globe), view, 12h/24h clock, Search, Print; the "+" sits in the top right corner. Full page is a button in the title bar left of the settings menu, not in the calendar's top line. | calendar.html; templates/index/topbar.html |
| R2-06.b | When the left group, right group and "+" do not fit in one line (their widths plus 36 px exceed the line), the tools move to a second line, right-aligned, and the "+" stays in the top right corner. Re-evaluated on window resize (after 80 ms) and once fonts load. | js/02-calendar.js:fitCalHead |
| R2-06.c | Compact calendar controls are 28 px; navigation buttons are 34 px. | styles/19-calendar-header.css |
| R2-07 | Time zone and clock | |
| R2-07.a | The time zone control is a globe icon whose tooltip is "Time zone: <zone>" (underscores shown as spaces); opening it shows a list. | calendar.html (tzpick) |
| R2-07.b | The list has a group "Common" and a group "All time zones" (every other zone). | calendar.html |
| R2-07.c | Common zones, in this order: America/New_York, America/Chicago, America/Denver, America/Phoenix, America/Los_Angeles, America/Anchorage, Pacific/Honolulu, Pacific/Guam, UTC, Europe/London, Europe/Frankfurt, Asia/Tokyo, Asia/Hong_Kong, Australia/Sydney. | main.py:COMMON_ZONES |
| R2-07.d | All zones are the system's zones that contain a "/" (area/city), excluding the prefixes Etc/, SystemV/, posix/ and right/, sorted by name; "UTC" is also accepted as valid. | main.py:ALL_ZONES; services/page_settings.py:valid_zone |
| R2-07.e | The server's configured zone (TZ) is marked with a star after its name in the list. | calendar.html |
| R2-07.f | Choosing a zone is saved on the server and applies to this page's calendar only; feeds and Google keep the configured zone. Choosing the configured zone or an empty value removes the saved choice. An unknown zone is refused ("Unknown time zone."). | routes/page.py:set_display_tz; services/page_settings.py:display_zone |
| R2-07.g | The calendar redraws in place after a zone change. | js/02-calendar.js:initCal |
| R2-07.h | The 12h/24h control is one hollow-clock icon with the current format ("12" or "24") as a badge over its lower-right corner. Its tooltip is "Time format: 12h (click for 24h)" or "Time format: 24h (click for 12h)"; it is a switch whose on state means 24-hour. | calendar.html (clockicon) |
| R2-07.i | Clicking it saves the format ("12" or "24") and reloads the whole page. | js/02-calendar.js:initCal |
| R2-07.j | The saved time format can be auto, 12 or 24; auto means 12-hour for English and 24-hour for every other language. Any other value is refused ("Unknown time format."). | routes/page.py:set_clock; i18n.py:Dates |
| R2-07.k | The clock button only ever writes 12 or 24 (it never returns to auto). | js/02-calendar.js:initCal |

## Topic 2. How events are drawn

| ID | Statement | Evidence |
|---|---|---|
| R2-10 | Which events appear and on which days | |
| R2-10.a | Events whose stored deletion mark is "gone" are never shown. | routes/page.py:index |
| R2-10.b | An event is placed on every day it covers in the display time zone, from its first day to its last day. | services/calendar_view.py:cal_view, _span |
| R2-10.c | A timed event's last day is the day of its end, except that an end exactly at midnight does not include the new day, and an event whose end is equal to or before its start is only on its start day. | services/calendar_view.py:_span |
| R2-10.d | An all-day event covers from its start date up to the day before its end date (end exclusive), and at least its first day. | services/calendar_view.py:_span |
| R2-10.e | Events are drawn within a day in the order they come from storage, which is sorted by start (hourly grid placement aside). | store.py:load_events |
| R2-10.f | An event added in CalendarStream and then deleted in CalendarStream disappears from the calendar at once. An event a source sent that was deleted stays on the calendar struck through and greyed. | services/calendar_view.py:_hidden_by; styles/04-calendar.css |
| R2-11 | The text on each event | |
| R2-11.a | Each event is a single line that shows, in order: a time label, the title, then marks. In the hourly grid, List and all-day cells the line wraps; in Month it is cut with an ellipsis. | calendar.html (evitem); styles/04-calendar.css |
| R2-11.b | The tooltip of the line is the title, followed by " (<where deleted>)" for a deleted event or " (hidden from Google)" for a hidden one. | calendar.html (evitem) |
| R2-11.c | A timed event within one day has the label "<start>–<end>" (en dash). | services/calendar_view.py:cal_view |
| R2-11.d | A timed event spanning days: its first day's label is "<start> →", its last day's is "→ <end>", days between are labelled with the localized text "cont." | services/calendar_view.py:cal_view |
| R2-11.e | A single-day all-day event has no label; a multi-day all-day event has no label on its first day and "cont." on each following day. | services/calendar_view.py:cal_view |
| R2-11.f | Times use the chosen clock (24h "13:05"; 12h "1:05pm" with lower-case am/pm, no leading zero on the hour, 12 for noon and midnight). | i18n.py:Dates.clock |
| R2-11.g | Marks after the title: a warning icon (tooltip "United changed this since your edit" for the CCS source, otherwise "The feed changed this since your edit") when the source changed an edited event; else an edit icon ("Edited here") when edited; else a "subdirectory_arrow_right" icon ("Added by a rule") when added by a rule. A deleted event shows none of these three. A reminder icon ("Has reminders") follows when the event has reminders. | calendar.html (evitem) |
| R2-11.h | Clicking an event opens its details inline: bold title, the range text, location with a pin icon, notes, state lines and tools. The details stay open across redraws until Close is pressed. | calendar.html; js/08-events.js |
| R2-11.i | The range text is "<day>, <start>–<end>" for one day; "<day> <start> – <day> <end>" across days; for all-day events "<day> (all day)" or "<day> – <day> (all day)" with the localized "(all day)". | services/calendar_view.py:_range_text |
| R2-11.j | State lines in the details: deleted: where it was deleted (Deleted in CalendarStream / Deleted in Google Calendar / Deleted by a rule / Removed by United (CCS+) / Gone from the feed), with the deletion date and time when known; hidden: "Hidden from Google Calendar"; stale: "United changed this event after you edited it" or "The feed changed this event after you edited it"; edited: "Edited here"; added here: "Added here", followed by "(not in the calendar it's from)" when the source is not a local calendar or "(not in United's schedule)" for the CCS source; added by a rule: "Added by a rule (change the rule or its event template to change it)"; linked: "Linked to “<title>”". | calendar.html; main.py:DELETED_WHERE |
| R2-11.k | The calendar's name is shown in the details only when more than one calendar exists. | calendar.html |
| R2-11.l | A deleted event shows a Restore button, except one deleted by a rule, which says "(change or remove the rule to bring it back)". | calendar.html |
| R2-11.m | The tools row for an opened event: Close on the left; on the right link, reminders, edit, duplicate, delete (or hide for a source's event). Delete asks "Delete this event? (It may be restored here or in History, Undo & Logs)"; hide asks "Hide this event from the feeds? (It may be shown again here or in History, Undo & Logs)". | calendar.html (evtoolstpl); js/08-events.js:fillTools |
| R2-12 | Month grid drawing | |
| R2-12.a | A Month day cell is at least 96 px tall plus its share of the stretch (stretch divided by the number of weeks); a cell grows to show all its events; there is no "+N more" overflow count. | styles/19-calendar.css; styles/04-calendar.css |
| R2-12.b | The month grid is at least 640 px wide and scrolls horizontally if the area is narrower; in Full page there is no minimum. | styles/04-calendar.css; styles/19-calendar.css |
| R2-12.c | Today's Month cell has an accent-colored 2 px inset outline and its date number is filled with the accent color; likewise today's row in List, today's column header number in Week and Day, and a faint 5% accent tint on today's column in Week and Day. | styles/04-calendar.css; styles/19-calendar.css |
| R2-12.d | In Month, all-day and timed events are drawn alike, each as a one-line colored bar. | styles/04-calendar.css |
| R2-13 | Hourly grid (Week and Day) | |
| R2-13.a | Week and Day draw a 24-hour grid; Week has 7 columns, Day has 1. Above the hours is a header row with the weekday and, in Week, the day number (Day: the full day text); below it an "all-day" row; then the hours. | calendar.html |
| R2-13.b | Hour labels run from midnight to 11 pm in the clock's format, with ":00" dropped before am/pm in 12-hour (12am, 1am … 11pm; 24-hour 00:00 … 23:00); the first label (midnight) is hidden. | services/calendar_view.py:cal_view (hours); styles/19-calendar.css |
| R2-13.c | A timed event is positioned by minutes from the start of the day and is as tall as its duration; the minimum drawn duration is 15 minutes; an event continuing past midnight is cut at 24:00 on that day and an event continuing from an earlier day starts at 00:00. | services/calendar_view.py:cal_view (m0, m1) |
| R2-13.d | All-day events (and nothing timed) are in the "all-day" row, in the day's cell. | calendar.html |
| R2-13.e | Hour height is 44 px by default, 20 to 120 px adjustable (see R2-32). | routes/page.py:calview_prefs |
| R2-13.f | The scrolling area of the hours is at most 560 px plus the stretch tall (in Full page, the space left in the window, at least 200 px). | styles/19-calendar.css; js/02-calendar.js:fitFull |
| R2-13.g | When Week or Day is drawn, the hours scroll so that the earliest timed event shown is half an hour-height from the top, but not lower than 7 am; with no timed events they open at 7 am. | js/02-calendar.js:scrollHours |
| R2-13.h | A timed event's line uses 11.5 px type; an opened event expands to the full column width and its own height with a shadow, above the others. | styles/19-calendar.css |
| R2-14 | Lanes | |
| R2-14.a | Timed events of one day are sorted by start minute, then longer first (end descending). | calendars/view_helpers.py:_lanes |
| R2-14.b | A cluster is a run of events that overlap; a new cluster starts when an event's start is at or after (>=) the latest end in the current cluster, so events that touch (one ends exactly when the next starts) do not overlap. | calendars/view_helpers.py:_lanes |
| R2-14.c | Each event takes the first lane (numbered from 0) whose last end is at or before its start, otherwise a new lane. | calendars/view_helpers.py:_lanes |
| R2-14.d | Every event in a cluster gets the same lane count = the cluster's number of lanes (at least 1); an event's width is 1/lanes of the column minus 3 px, and its left edge is lane/lanes of the column plus 1 px. | calendars/view_helpers.py:_lanes; styles/19-calendar.css |
| R2-14.e | Lanes are computed per day; a multi-day event has its own segment (and lane) on each day. | services/calendar_view.py:cal_view |
| R2-15 | Colors | |
| R2-15.a | An event's color is, in order: its own color; else the color given by a rule; else its calendar's color; else the default blue #1d4ed8. | services/calendar_view.py:cal_view (tag_color, src_color); calendar.html (tc) |
| R2-15.b | The event bar is the color mixed with the card background at 18% (dark theme) or 12% (light theme) and its text is the color mixed with the text color at 70% (dark) or 60% (light). | styles/04-calendar.css; templates/_theme.html |
| R2-15.c | Events added in CalendarStream or by a rule use a purple "custom" look: dark #2e1a47 with text #e9d5ff; light #f4eef8 with text #5e3f7a; since every event on this page also gets a color, the tint normally wins. unsure about precedence | styles/04-calendar.css; _theme.html; calendar.html |
| R2-15.d | A hidden event's line is struck through and 55% opaque; a deleted event is desaturated (85% grayscale) and its line is 45% opaque. | styles/04-calendar.css |
| R2-15.e | An event's own color is one of Google's 11 event colors. | README.md; gsync.py:GOOGLE_COLORS |
| R2-16 | Display time zone | |
| R2-16.a | Day assignment, times and "today" use the display time zone (the chosen one, else TZ). | services/calendar_view.py:cal_view; main.py:display_tz |
| R2-16.b | An all-day event's dates are not shifted by the display time zone. | services/calendar_view.py:_span |
| R2-17 | Not present | |
| R2-17.a | There is no "+N more" overflow count in any view. Not implemented. | calendar.html; styles |
| R2-17.b | Lanes exist only in Week and Day, not in Month or List. | calendar.html |

## Topic 3. Dragging, resizing and Full page

| ID | Statement | Evidence |
|---|---|---|
| R2-30 | Moving events by dragging | |
| R2-30.a | Events cannot be moved or resized by dragging on the calendar; times change only in the event form. Not implemented (the only dragging on the page is the calendar stretch bar, the hour-height grip, History column headers and handles that order lists). | js/08-events.js; js/12-handles-checks.js; js/10-fields.js |
| R2-31 | Calendar height (stretch) | |
| R2-31.a | A bar centered under the calendar (not in List and not in Full page) holds three controls: a collapse arrow, a drag handle of twelve dots (two rows of six), and an expand arrow. | calendar.html (calstretchbar) |
| R2-31.b | The stretch is the number of pixels added to the calendar's height, from -300 to 1200 inclusive, default 0. | routes/page.py:calview_prefs; js/02-calendar.js |
| R2-31.c | Dragging the handle down grows and dragging up shrinks the height one pixel per pixel moved, clamped to -300..1200; the value is saved 400 ms after the last change. | js/02-calendar.js (STRETCH_MIN, MAX, remember) |
| R2-31.d | With the handle focused, the Down arrow key adds 24 px and the Up arrow key subtracts 24 px. | js/02-calendar.js (keydown) |
| R2-31.e | The collapse arrow sets the stretch to -300. | js/02-calendar.js |
| R2-31.f | The expand arrow sets the stretch so the calendar's bottom edge is 24 px above the bottom of the visible window. | js/02-calendar.js |
| R2-31.g | The handle is exposed as a vertical slider, range -300 to 1200, labelled "Stretch the calendar (drag, or ↑ ↓)". The arrows are labelled "Collapse the calendar to its minimum height" and "Expand the calendar to the bottom of the window". | calendar.html |
| R2-31.h | The stretch is saved on the server; a value outside -300..1200 or a non-integer is refused ("Unknown stretch."); a stored out-of-range value reads as 0. | routes/page.py:set_calview, calview_prefs |
| R2-31.i | In Month the stretch is divided equally among the displayed weeks; in Week and Day it enlarges the scrolling hours area (R2-13.f). | styles/19-calendar.css |
| R2-32 | Hour height | |
| R2-32.a | In Week and Day a grip button left of the hour labels (tooltip "Drag to make each hour shorter or taller", slider labelled "Height of an hour") changes the hour height. | calendar.html (hourgrip) |
| R2-32.b | Hour height is 20 to 120 px inclusive, default 44; dragging changes it by one pixel per 6 pixels moved; with the grip focused Down adds 4 and Up subtracts 4 px; the value is saved 400 ms after the last change. | js/02-calendar.js (hourSet, hourKeep) |
| R2-32.c | An hour height outside 20..120 or non-numeric is refused when saving ("Unknown hour height."); an invalid stored value reads as 44. | routes/page.py:set_calview, calview_prefs |
| R2-33 | Full page | |
| R2-33.a | Full page is a title-bar button left of the settings menu; when on, it hides every other section, the footer and the page width cap and shows as Back (pressed); pressing it again restores the page. | topbar.html; js/02-calendar.js; styles/19-calendar.css |
| R2-33.b | The state is saved on the server (shared across browsers) and the calendar is redrawn when it changes; only "0" or "1" are accepted (otherwise "Unknown choice."). | routes/page.py:set_calview |
| R2-33.c | Clicking items of the Calendars and Key parts hides or shows events (R2-71) in every mode, Full page included. | js/02-calendar.js |
| R2-33.d | In Full page Month keeps each day cell at most 2 wide by 3 tall (height at most 1.5 times the width); more weeks are added beyond the month's own, alternately the first week after the month, then the last week before it, up to 6 on each side, until the available height is filled. | js/02-calendar.js:fitFull; services/calendar_view.py (pad=6) |
| R2-33.e | Only Month in Full page uses extra weeks. | routes/page.py:index; services/calendar_view.py |
| R2-33.f | Available height in Full page is the window height minus the calendar body's top, the key's height and 36 px, never less than 260 px. | js/02-calendar.js:fitFull |
| R2-33.g | In Full page, Week and Day limit the hour area to the available height (at least 200 px); List scrolls inside the available height. | js/02-calendar.js:fitFull |
| R2-33.h | The stretch bar is not shown in Full page. | calendar.html |
| R2-33.i | Full page refits on window resize (80 ms delay) and when fonts finish loading. | js/02-calendar.js |
| R2-33.j | In Full page a Month day cell has no minimum height and scrolls its own content. | styles/19-calendar.css |

## Topic 4. Print Preview and printing

| ID | Statement | Evidence |
|---|---|---|
| R2-50 | Opening Print Preview | |
| R2-50.a | The Print button (printer icon, tooltip "Print the calendar") in the calendar's top line opens a pop-up titled "Print Preview" with option controls, a preview frame and the buttons "Cancel" and "Print". | calendar.html; calendar-dialogs.html |
| R2-50.b | It opens with From and To set to the first and last day of the displayed month and "All" unchecked. | js/11-reminders-print.js |
| R2-50.c | It opens with the last print's choices (view, theme, orientation, weekends); on first use the view follows the calendar's view (Month, Week, Day as themselves; List as Itinerary), the theme is Light, orientation Auto, weekends included. | routes/page.py:print_prefs, print_page; js/11-reminders-print.js |
| R2-50.d | An event's Print opens the same pop-up for that event's day: From and To both that day, view Day; pressing Print then does not save Day as the remembered view (the previous remembered view is kept). | js/11-reminders-print.js:openPrintDay |
| R2-50.e | Each choice change redraws the preview after a 250 ms delay. | js/11-reminders-print.js |
| R2-50.f | Cancel closes the pop-up; Print sends the preview to the printer and saves the choices (view, theme, weekends, orientation). | js/11-reminders-print.js |
| R2-51 | What can be printed | |
| R2-51.a | The "What to print" choices are Itinerary, Day, 5-day, Week, Month. | calendar-dialogs.html; routes/page.py:PRINT_VIEWS |
| R2-51.b | Month prints one page per calendar month from the month of From through the month of To, at most 24 pages. | routes/page.py:print_pages |
| R2-51.c | Week prints one page per week (Sunday to Saturday) from the week containing From until a week starts after To, at most 60 pages. | routes/page.py:print_pages |
| R2-51.d | 5-day prints the same weeks as Week but only Monday to Friday, whether or not weekends are included, at most 60 pages. | routes/page.py:print_pages |
| R2-51.e | Day prints one page per day from From through To inclusive, at most 62 pages. | routes/page.py:print_pages |
| R2-51.f | Itinerary prints every day from From through To that has events (day text and its events) as one sheet that flows over as many paper pages as needed; its title is "<first day text>, <year> – <last day text>, <year>"; with no events it says "No events." | routes/page.py:print_pages; print.html |
| R2-51.g | "Include weekends" (checked by default): when unchecked, Week and Month omit the Saturday and Sunday columns and Itinerary omits Saturday and Sunday days. | routes/page.py:print_pages |
| R2-51.h | Day printing is not affected by the weekends choice (every day in range prints); 5-day is not affected either. | routes/page.py:print_pages |
| R2-51.i | Week, 5-day, Day and Itinerary pages show each event's location (" · <location>") and, if more than one calendar exists, its calendar's name (" · <name>"); Month pages show neither. | print.html |
| R2-51.j | A Week or Month page's title is the calendar view's title for that week or month; a Day page's title is the day title. | print.html |
| R2-51.k | A Day page with no events says "No events." | print.html |
| R2-51.l | Events hidden by the key (R2-71) are not printed. | routes/page.py:print_page |
| R2-51.m | In printed Month, days outside the month are shaded. | print.html |
| R2-52 | Date range | |
| R2-52.a | From and To are date fields; the "All" checkbox makes them read-only and means from the first event to the last. | index.html:daterange; js/11-reminders-print.js |
| R2-52.b | If From is not given it is the 1st of the current month in the display zone; if To is not given it is the last day of From's month; an invalid From or To falls back as in R2-03.a. | routes/page.py:print_page |
| R2-52.c | With All, From is the earliest start day and To the latest start day among all non-hidden events (by the server's own time zone) when any exist; otherwise the dates stay as given. | routes/page.py:print_page |
| R2-52.d | If To is before From the two are swapped. | routes/page.py:print_page |
| R2-52.e | The range is limited to 731 days after From. | routes/page.py:print_page |
| R2-53 | Orientation and paper | |
| R2-53.a | Orientation choices: Auto ("Best fit for each view"), Landscape, Portrait; Auto prints Month, Week and 5-day landscape and Day and Itinerary portrait; Landscape or Portrait sets every sheet. | calendar-dialogs.html; print.html |
| R2-53.b | Each sheet fills one page of whatever paper the printer uses, with 5 mm margins; nothing is cut off: a day cell whose content does not fit shrinks its type in steps of 4% down to 40% of its size until it fits. | print.html |
| R2-53.c | The preview shows each sheet as a page in the paper's proportion: Letter (11 × 8.5 or 8.5 × 11) when the page language is English, A4 (297 × 210 or 210 × 297) for other languages; the portrait preview is at most 760 px wide, the landscape at most 1100 px. | print.html |
| R2-53.d | Sizes in print scale with the sheet so preview and paper look alike; the heading is 1.7 times the base size. | print.html |
| R2-53.e | An itinerary flows in 12 px type and is not fitted to one page. | print.html |
| R2-53.f | Saved orientation values are land, port or auto (anything else saves as auto). | routes/page.py:set_print |
| R2-54 | Theme | |
| R2-54.a | The "Colors" choices are Light (sun icon) and Dark (moon icon). Light prints on white paper; Dark prints with the dark theme's colors. | calendar-dialogs.html; print.html |
| R2-54.b | Background colors are printed exactly (not dropped by the printer settings). | print.html |
| R2-54.c | Saved theme values are dark or light (anything else saves as light). | routes/page.py:set_print |
| R2-54.d | A printed event is tinted by its own color or rule color; otherwise by its calendar's color only for events from United's schedule; events added here or by a rule print in the custom look; hidden events print struck through at 60% opacity. | print.html (item) |
| R2-55 | Saved print choices | |
| R2-55.a | The saved choices are the view (an unknown value becomes Month), weekends (true only if sent as "1"), theme and orientation. | routes/page.py:set_print |
| R2-55.b | The print page uses the saved weekends choice when the request does not say. | routes/page.py:print_page |
| R2-56 | Printing the status page itself | |
| R2-56.a | When the status page is printed by the browser, only the calendar prints: the top bar, other sections, footer, dialogs, nav buttons, right-hand tools, month picker, caret and "+" buttons are hidden; colors are black on white; event titles wrap whole; an open event's details are not printed; a day cell does not break across pages. | styles/09-spacing-print.css; styles/19-calendar-header.css |

## Topic 5. Search

| ID | Statement | Evidence |
|---|---|---|
| R2-60 | The search line | |
| R2-60.a | The search icon (tooltip "Search the calendar") toggles a search line under the top line; it is closed by default and its open state shows on the button. | calendar.html |
| R2-60.b | The line holds: a search box (placeholder "Search titles, places and notes", at most 100 characters), a calendar selector ("All calendars" then each calendar by name), From and To dates (shown with the browser's date format as a hint when empty), and a close (✕) button ("Close the search"). | calendar.html |
| R2-60.c | Opening the line focuses the search box. | js/02-calendar.js |
| R2-60.d | Results update 300 ms after typing stops, and immediately when the calendar selector or a date changes. | js/02-calendar.js |
| R2-60.e | Only the results area and title are replaced, so the words being typed stay. | js/02-calendar.js (show) |
| R2-60.f | ✕, the search icon again, or Escape in the search line closes the line, resets its fields and brings the normal calendar back for the current date; emptying the box also brings the normal calendar back. | js/02-calendar.js (close, run) |
| R2-60.g | A search is not requested again when its address would be identical to the last one. | js/02-calendar.js (run) |
| R2-61 | What matches | |
| R2-61.a | The query is split on whitespace into words, compared case-insensitively; an event matches only if every word appears in its title, location or notes. | routes/page.py:cal_search |
| R2-61.b | The query is trimmed and limited to its first 100 characters; an empty query is no search. | routes/page.py:index |
| R2-61.c | The calendar selector restricts to one calendar; an unknown calendar id means all calendars. | routes/page.py:index, cal_search |
| R2-61.d | From and To are optional; with neither, every date (2000-01-01 to 2100-12-31) is searched; an invalid date or one outside years 2000 to 2100 is treated as empty. If To is before From they are swapped. The README says "a year back to a year ahead when empty"; the code does not do that. unsure (README and code differ) | routes/page.py:cal_search; calendars/view_helpers.py:_opt_day; README.md |
| R2-61.e | An event spanning several days is listed once, on its first day inside the range (on From when it began earlier); an event that ends before From or starts after To is not listed. | routes/page.py:cal_search |
| R2-61.f | Events switched off in the key are still found by search (the key filter is not applied); an event added and deleted in CalendarStream is not found. unsure whether intended | routes/page.py:cal_search; services/calendar_view.py:_hidden_by |
| R2-62 | Result display | |
| R2-62.a | Results are listed by day in date order like List, each day with its matching events; days with no match are omitted. | routes/page.py:cal_search |
| R2-62.b | The title becomes "<n> found" where n is the number of listed events; with no result the body says "Nothing found." | routes/page.py:cal_search; calendar.html |
| R2-62.c | Search results always show in List form regardless of the chosen view. | routes/page.py:cal_search |
| R2-62.d | Events in results open their details like those in the calendar, and open details are kept when results redraw. | js/02-calendar.js (reopenEvents) |
| R2-62.e | The search is not saved; the address of the page keeps only the typed query and filters while searching. | js/02-calendar.js (run) |

## Topic 6. Calendar filter and key

| ID | Statement | Evidence |
|---|---|---|
| R2-70 | The key | |
| R2-70.a | Under the calendar is a key with two parts separated by a vertical rule: "Calendars" (left) and "Key" (right), each with a help note. | calendar.html (legend) |
| R2-70.b | Calendars lists each calendar, by name, as a button with a swatch of the calendar's color (the color mixed 18% with the card color; default #1d4ed8). | calendar.html (legitem) |
| R2-70.c | Key lists, in order: one non-clickable swatch per color action of a rule that names specific calendars, then four buttons: "Edited" (edit icon), "United changed it since" (warning icon), "Hidden from Google" (struck-through text), "Deleted" (struck-through, faded). | calendar.html |
| R2-70.d | A rule's key entry text is the rule's title, else the first text condition's value, else the rule's label; cut to 25 characters with an ellipsis; the full name is its tooltip. Rules set to All calendars do not appear. | calendar.html |
| R2-70.e | Entries are laid in columns of three (down then across): Calendars from the left, Key from the right; when they do not fit across, every column grows one row taller until they fit. | js/02-calendar.js:fitKey; styles/19-calendar.css |
| R2-70.f | Calendars and Key share the width equally with the rule between them; above 700 px wide each side keeps at least its list's own width. | styles/19-calendar.css |
| R2-70.g | The help notes read: Calendars: "Click a calendar to hide or show its events on the calendar only. Nothing changes in Sources, Feeds, Rules or the other sections." Key: "Click an item to hide or show those events on the calendar only. Deleted events can be restored from the event or History › Undo." | calendar.html |
| R2-71 | Filtering by the key | |
| R2-71.a | Clicking a Calendars or Key button toggles it: shown (pressed) is the default; hidden is dimmed to 45% opacity and its events are removed from the calendar. | js/02-calendar.js; calendar.html |
| R2-71.b | Hiding a calendar hides all events of that calendar. | services/calendar_view.py:_hidden_by |
| R2-71.c | Hiding "Deleted" hides events that are deleted. | services/calendar_view.py:_hidden_by |
| R2-71.d | Hiding "Hidden from Google" hides events hidden from Google that are not deleted. | services/calendar_view.py:_hidden_by |
| R2-71.e | Hiding "United changed it since" hides events the source changed since an edit that are not deleted. | services/calendar_view.py:_hidden_by |
| R2-71.f | Hiding "Edited" hides edited events that are not stale and not deleted. | services/calendar_view.py:_hidden_by |
| R2-71.g | The choice applies in every view and in Full page, in printing (R2-51.l) and is kept across reloads and browsers; nothing in Sources, Feeds or Rules changes. | routes/page.py; js/02-calendar.js |
| R2-71.h | The choice is saved on the server as a list of keys; valid keys are "src:<letters, digits or underscore>", "edited", "stale", "hidden", "deleted"; at most 60 keys; an invalid key or more than 60 refuses the save ("Unknown key item."). "-" in the request means none. Invalid stored keys are ignored. | routes/page.py:set_calview, calview_prefs, HIDE_KEY |
| R2-71.i | After each toggle the calendar is redrawn in place. | js/02-calendar.js |
| R2-71.j | When any item is hidden, a "View All" button (eye icon, tooltip "View All (show everything hidden by the key)") appears at the right of the Key title; pressing it shows everything again. | calendar.html; js/02-calendar.js |
| R2-71.k | Rule color entries in the key are informational only and cannot be toggled. | calendar.html |
