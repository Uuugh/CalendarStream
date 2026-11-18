# DRAFT requirements: events (for the Developer's review)

Not approved. Behavior shared by every feature (dialog Back/Escape/phone, sections, confirmations, info dots, label ticking, the calendar picker) lives once in `common.md` (UI-NN) and is only referenced here. From the 165 `events` rows of `requirements/inventory/` (suites 12-71; pinned to d70343f). The event
pop-up: adding, editing, hiding, deleting, restoring, reminders, links between events. Existing: EVT-01..03 (planned
in `requirements/events.md`). Numbering continues from EVT-04. Pixel and alignment rows (S46-16..20, S57-21..24/35/37,
S59-15..17, S65-34..37, S44-26..28/45) are left to `theme.md` (Q-R1) except where the order itself is the behavior.

## Opening and saving

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-04 | proposed | Clicking a day (or the plus) opens the new-event dialog for that date. The dialog follows the shared dialog rules (UI-01, UI-02). | S26-03, S46-15, S36-57, S67-13 |
| EVT-05 | proposed | A new event defaults to the system clock's time zone, or to the calendar's time zone when the calendar has one selected (Developer, Nov 17). It can be saved into any calendar chosen in the source selector; with none chosen it goes to the initial Local calendar. A custom event appears on its calendar page. | S19-33, S26-30, S36-21, S65-04 |
| EVT-06 | proposed | Title, start and end dates and start and end times are required; leaving one out blocks saving. | S57-03 |
| EVT-07 | proposed | Rule-generated events cannot be opened in the editor (400) and cannot be picked as link targets. | S26-21, S58-10 |
| EVT-08 | proposed | Saving an event updates the calendar at once, and the confirmation names the event. | S36-36, S36-51 |

## Times and dates

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-10 | proposed | Times show in the page's clock mode (24-hour `09:00`, 12-hour `9:00am`) and accept typed forms: `1:30 pm` and `1505` save as 13:30 and 15:05; `13pm` and `25:00` are refused (400, and 25:00 is marked and blocks saving). | S19-05..07, S19-10..12, S19-14, S19-39 |
| EVT-11 | proposed | Changing the start keeps the duration: start 11am moves a one-hour end to 12pm; start 2300 with 90 minutes ends 12:30am the next day; moving an overnight event's start date moves its end date by the same days. | S19-34, S19-37, S19-38 |
| EVT-12 | proposed | The end time offers suggestions that show their duration (12:30pm, 1h30); choosing one sets the end. | S19-35, S19-36 |
| EVT-13 | proposed | The end may be in a different time zone from the start; changing the start keeps the end in its own zone (10am New York start, 11am Los Angeles end), and the event reopens with both zones. | S19-43, S19-45, S19-46, S59-11 |
| EVT-14 | proposed | An all-day event has no times and no end zone. | S59-18, S65-37 |
| EVT-15 | proposed | The location field updates a map link whose address is the URL-encoded location. | S46-23 |

## Color

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-16 | proposed | An event color is one of the twelve palette colors including Tomato (UI-10); a color outside Google's palette is refused; the chosen color is stored in lowercase and shows on the calendar and on the edit page. | S19-08, S19-11, S19-13, S19-15, S19-17 |
| EVT-17 | proposed | An event's own color beats its source color and any rule tag; changing an imported event's color keeps it and marks the event edited, not stale. | S19-16, S19-18 |
| EVT-18 | proposed | The default color follows the chosen calendar until a color is picked; a picked color survives a later calendar choice. | S59-12..14 |

## Reminders

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-19 | proposed | An event's reminders are chosen from the offered minutes; only valid ones are stored (15, 60, 7 stores 15, 60); none stores nothing. | S36-25, S36-28, S36-29 |

## Hide, delete, restore

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-20 | proposed | An imported event can be hidden (asking first, UI-06) and shown again; both are recorded in History. Hide then Show on an unedited event leaves no edit record. Hiding an unknown UID returns 404. A renamed hidden event stays hidden when saved. | S57-10..14, S57-16, S57-33, S57-34, S57-36, S26-58 |
| EVT-21 | proposed | A custom event is deleted (asking first, UI-06) and leaves its calendar; cancelling leaves it.\| Yes) and leaves its calendar; cancelling leaves it. A deleted event keeps a deletion marker in storage. | S26-59, S49-14, S58-24, S58-25, S58-35, S58-36, S65-05 |
| EVT-22 | proposed | Restoring a deleted or externally removed event clears its marker and gives it custom origin. | S49-15, S49-19 |
| EVT-23 | proposed | The footer of an imported event explains that edits persist across downloads and never change CCS+; a custom event shows Delete (with confirmation) and no Hide; a new event shows no Delete or Hide. | S57-06, S57-08, S57-17, S58-03, S58-04 |
| EVT-24 | proposed | The Calendar label has an info text (UI-07) explaining that changes affect CalendarStream and Google only. | S58-01, S58-34 |

## Duplicate, templates

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-25 | proposed | Merged into the planned EVT-01 (Duplicate: copy in the same calendar, calendar dropdown to change it). The Python app has a partial Duplicate (it opens an editor titled "Duplicate event" with the existing title and a new empty UID, S26-56), but the Developer says it was never implemented correctly nor closed out, so it is not a verified behavior; see issue I51. | S26-56 |

## Links between events

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-27 | proposed | An event can be linked to another event or to a rule. Choosing the target uses the shared calendar picker (UI-09), opened on the edited event's month; the event itself and rule-generated events cannot be chosen. | S37-50..52, S57-26, S58-10, S58-28 |
| EVT-28 | proposed | Picking an event sets the link target; saving persists the target UID. | S37-52, S58-30, S58-33 |
| EVT-29 | proposed | Removing a link hides its panel and clears the target; cancelling the editor afterwards keeps the stored original link. | S57-27, S57-31, S58-27 |
| EVT-30 | proposed | A saved linked event shows its link (event or rule, and the target) when reopened. | S57-18, S58-13, S45-27 |
| EVT-31 | proposed | A linked event follows its target: moving the target by two hours moves the linked event by two hours; deleting the target removes the linked event and its link. Linking an imported event alone adds no stored edit. The move helper handles timed moves, refuses a mix of all-day and timed, and shifts all-day endpoints together. | S37-05, S37-14, S37-17..19, S62-10 |
| EVT-32 | proposed | Starting a new event-derived rule closes the event dialog; closing the rule dialog restores it (UI-02). | S67-14, S67-17 |

## Other

| ID | status | statement | evidence |
|---|---|---|---|
| EVT-33 | proposed | A meeting link (Zoom and similar) is found in an event's text or location with its query intact; plain text yields none. | S63-01, S63-02 |
| EVT-34 | proposed (?) | Applying empty edits or hidden inputs leaves the event list unchanged. | S77-10 |

Not requirements: source-text checks (S62-12, S62-16, S62-17, S65-01..03 partly, S66-19, S66-20, S77-22 failure
callback), `ok(True)`-style markers, and the layout rows listed in the header.
