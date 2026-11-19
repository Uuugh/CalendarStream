# Requirements: events

The event pop-up, linked events, hiding and reverting. Issues against this feature: none open on the Dashboard.

| ID | status | statement | test | was |
|---|---|---|---|---|
| EVT-01 | planned | When editing an event, the event dialog has a Duplicate icon immediately right of "Edit <event>" and immediately left of the Print icon (today it sits to the right of Print). Duplicate opens an editor holding a copy of the event in the same calendar; the user may then choose a different calendar with the calendar dropdown before saving. The Duplicate icon in the calendar view (the event tools) stays as it is. | — | F62 |
| EVT-02 | planned | Right of Duplicate there is a Move icon, shown only for events CalendarStream itself owns, never for a read-only source such as CCS+ (United) (CAP-03). | — | F62 |
| EVT-03 | planned | Print includes the event card, not only the calendar grid. | — | F62 |
| EVT-05 | planned | A new event defaults to the system clock's time zone, or to the calendar's time zone when the calendar has one selected (Developer, Nov 17). It can be saved into any calendar chosen in the source selector; with none chosen it goes to the initial Local calendar. A custom event appears on its calendar page. | — | S19-33, S26-30, S36-21, S65-04 |
| EVT-04 | proposed | Clicking a day (or the plus) opens the new-event dialog for that date. The dialog follows the shared dialog rules (UI-01, UI-02). | — | S26-03, S46-15, S36-57, S67-13 |
| EVT-06 | proposed | Title, start and end dates and start and end times are required; leaving one out blocks saving. | — | S57-03 |
| EVT-07 | proposed | Rule-generated events cannot be opened in the editor and cannot be picked as link targets (CAP-01, CAP-04). | — | S26-21, S58-10 |
| EVT-08 | proposed | The confirmation after saving an event names the event (UI-13). | — | S36-36, S36-51 |
| EVT-10 | proposed | Times show in the page's time notation (TIM-10) and accept typed forms: 9:30, 9:30pm, 21:30, 930, 1:30 pm and 1505 are read as the times they mean (13:30 and 15:05 for the last two); an entry such as 13pm or 25:00 is not valid (UI-19) and blocks saving. | — | S19-05..07, S19-10..12, S19-14, S19-39, changelog_gaps_1801-2100:17 |
| EVT-11 | proposed | Changing the start keeps the duration: start 11am moves a one-hour end to 12pm; start 2300 with 90 minutes ends 12:30am the next day; moving an overnight event's start date moves its end date by the same days. Changing the end sets the duration that later start changes keep. | — | S19-34, S19-37, S19-38, changelog_gaps_1801-2100:23 |
| EVT-12 | proposed | The end time offers suggestions that show their duration (12:30pm, 1h30); choosing one sets the end. | — | S19-35, S19-36 |
| EVT-13 | proposed | The end may be in a different time zone from the start; changing the start keeps the end in its own zone (10am New York start, 11am Los Angeles end), and the event reopens with both zones. | — | S19-43, S19-45, S19-46, S59-11 |
| EVT-14 | proposed | An all-day event (TIM-04) is entered without times. | — | S59-18, S65-37 |
| EVT-15 | proposed | The location field updates a map link whose address is the URL-encoded location; the map action opens the location in Google Maps. | — | S46-23, changelog_gaps_901-1200:16 |
| EVT-16 | proposed | An event color is one of the shared palette colors (UI-10, UI-20); the chosen color shows on the calendar and on the edit page. | — | S19-08, S19-11, S19-13, S19-15, S19-17 |
| EVT-17 | proposed | An event's own color beats its source color and any rule tag; changing an imported event's color keeps it and marks the event edited, not stale. | — | S19-16, S19-18 |
| EVT-18 | proposed | The default color follows the chosen calendar until a color is picked; a picked color survives a later calendar choice. | — | S59-12..14 |
| EVT-19 | proposed | An event's reminders are chosen from the offered times, which range from the event start through one week before it; at most five can be set, only valid ones are stored (15, 60, 7 stores 15, 60), and none stores nothing. | — | S36-25, S36-28, S36-29, readme_gaps:44, changelog_gaps_1201-1500:17, readme_gaps:44, changelog_gaps_1201-1500:17 |
| EVT-20 | proposed | An imported event can be hidden (asking first, UI-06) and shown again; both are recorded in History. Hide then Show on an unedited event leaves no edit record. Hiding an unknown UID returns 404. A renamed hidden event stays hidden when saved. | — | S57-10..14, S57-16, S57-33, S57-34, S57-36, S26-58 |
| EVT-21 | proposed | A custom event is deleted (asking first, UI-06) and leaves its calendar; cancelling leaves it.\ | — | Yes) and leaves its calendar; cancelling leaves it. A deleted event keeps a deletion marker in storage. |
| EVT-22 | proposed | Restoring a deleted or externally removed event clears its marker and gives it custom origin. | — | S49-15, S49-19 |
| EVT-23 | proposed | The footer of an imported event explains that edits persist across downloads and never change CCS+; a custom event shows Delete (with confirmation) and no Hide; a new event shows no Delete or Hide. | — | S57-06, S57-08, S57-17, S58-03, S58-04 |
| EVT-24 | proposed | The Calendar label has an info text (UI-07) explaining that changes affect CalendarStream and Google only. | — | S58-01, S58-34 |
| EVT-27 | proposed | An event can be linked to another event or to a rule. Choosing the target uses the shared calendar picker (UI-09), opened on the edited event's month; the event itself and rule-generated events cannot be chosen. Picking an event sets the link target, and saving keeps it. | — | S37-50..52, S57-26, S58-10, S58-28, S37-52, S58-30, S58-33 |
| EVT-29 | proposed | Removing a link hides its panel and clears the target; cancelling the editor afterwards keeps the stored original link. | — | S57-27, S57-31, S58-27 |
| EVT-30 | proposed | A saved linked event shows its link (event or rule, and the target) when reopened, and following the link opens the target. | — | S57-18, S58-13, S45-27, readme_gaps:45, changelog_gaps_301-600:42, changelog_gaps_901-1200:22 |
| EVT-31 | proposed | A linked event follows its target: moving the target by two hours moves the linked event by two hours; deleting the target removes the linked event and its link. Linking an imported event alone adds no stored edit. Moving shifts start and end together (an all-day event is a 24-hour event, TIM-04, so it needs no special case). | — | S37-05, S37-14, S37-17..19, S62-10 |
| EVT-32 | proposed | Starting a new event-derived rule closes the event dialog; closing the rule dialog restores it (UI-02). | — | S67-14, S67-17 |
| EVT-33 | proposed | A meeting link (Zoom and similar) is found in an event's conference fields, text or location with its query intact; plain text yields none. Extraction keeps an online meeting address the user already entered. | — | S63-01, S63-02, readme_gaps:50, changelog_gaps_301-600:21, changelog_gaps_301-600:21 |
| EVT-38 | proposed | A linked event’s delete-with and move-with actions can each be enabled or removed independently through its link rule (RUL-11). | — | readme_gaps:46, changelog_gaps_301-600:31 |
| EVT-39 | proposed | Choosing Rule for an event opens its associated rule, or starts a rule for that event when it has none; returning to the event follows EVT-32 and UI-02. | — | readme_gaps:46 |
| EVT-41 | proposed | An event’s online meeting address is exported in its ICS URL property; feed round-trip preservation follows FED-04. | — | readme_gaps:50 |
| EVT-42 | proposed | Local edits to an imported event survive subsequent source downloads; the source itself is unchanged (EVT-23). | — | readme_gaps:51, changelog_gaps_2101-2336:27 |
| EVT-43 | proposed | An edited imported event identifies that it has local edits and indicates when its source changes after those edits. | — | readme_gaps:51, changelog_gaps_2101-2336:27 |
| EVT-44 | proposed | An imported event’s local edits can be reverted to the current source version. | — | changelog_gaps_2101-2336:27 |
| EVT-47 | proposed | Starting a rule from an unsaved new event uses its currently entered title and date (RUL-36). | — | changelog_gaps_301-600:16 |
| EVT-48 | proposed | An event’s online meeting address can be opened. | — | changelog_gaps_301-600:21 |

Retired IDs (merged or dropped; numbers are never reused): EVT-45 into EVT-10; EVT-46 into EVT-11; EVT-51 into EVT-15; EVT-35 and EVT-36 into EVT-19; EVT-28 into EVT-27; EVT-37 into EVT-30; EVT-40 and EVT-49 into EVT-33; EVT-25 (already merged into EVT-01); EVT-50 (migration is DEP-14; EVT-31 and EVT-38 already keep the behavior).

## Notes from the draft

Not requirements: source-text checks (S62-12, S62-16, S62-17, S65-01..03 partly, S66-19, S66-20, S77-22 failure
callback), `ok(True)`-style markers, and the layout rows listed in the header.
