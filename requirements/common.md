# Requirements: common

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | was |
|---|---|---|---|---|
| TIM-01 |  | Every event's start and end are stored in UTC together with the time zone each was recorded in. | — | Developer, Nov 17 |
| TIM-02 |  | An event's time zone is set when it is created (imported: from the source, or the zone the source's calendar reports; added: the system zone, or the calendar's zone if one is selected, EVT-05) and stays as recorded until the user edits the event with Edit Event. | — | Developer, Nov 17 |
| TIM-03 |  | The calendar shows every event in the Local time zone: the system (device) zone, or the fixed zone chosen in Settings > Time Zones (SET-47). Changing the Local zone changes only how times are shown. | — | Developer, Nov 17 |
| TIM-04 |  | An all-day event is a 24-hour event, local midnight to the next local midnight in its own time zone, stored in UTC like any other. It is shown like any other event, so it is one day in its own zone and can span two days in another (CAL-65). When it is sent to an outside calendar that has an all-day type (Google, calendar feeds), it is sent as an all-day event for its stored time zone, with that zone's local dates. | — | Developer, Nov 17 |
| TIM-05 |  | Rules do not depend on a time zone. A rule is applied to an event, and the event's recorded time zone decides what "Friday" or "22:00" means. Only a rule that is literally about a time zone uses a zone. | — | Developer, Nov 17 |
| TIM-06 |  | Syncing with an outside calendar reads the time zone of that calendar and of each incoming event and records it with the event (TIM-02), and sends each event's recorded time zone with its times. | — | Developer, Nov 17 |
| TIM-07 |  | Calendar feeds carry each event's times with its time zone. | — | Developer, Nov 17 |
| TIM-10 |  | The time format (12-hour, such as 1:30pm, or 24-hour, such as 13:30) is a view setting that is local to the device and applies to every time shown in every feature. Until the user chooses, it defaults to 12-hour when the device is in a US time zone and 24-hour elsewhere. One control in the top bar, to the right of the language control, switches it and shows the current setting as a badge (build_rules/theme.md, 13b). The notation inside each format is a Theme setting (SET-58). (Developer, Nov 17; replaces CAL-02 and CAL-21) | — | Developer, Nov 17; F15.2, F43, S19-03, S19-04, S21-05, S21-07, S21-08, S21-09, S66-16, S79-10..13 |
| UI-12 |  | One shared multi-select dropdown (the language dropdown and the Calendar filter use it): it opens from a single icon; a single click or tap toggles an item and takes effect at once; Ctrl and Shift select several on a keyboard; Select all and Select none are offered; choosing outside the dropdown (losing focus) closes it. (Developer, Nov 17) | — | Developer |
| UI-13 |  | A change the user makes (a filter, a view, a theme, a setting) is shown at once: nothing needs a page reload or an Apply step. (Developer, Nov 17: the client redraws only the element that changed.) | — | Developer |
| UI-14 |  | Every row of controls has left, center and right zones, each keeping its own alignment. A row that is too narrow is handled in this order: (1) the zones stack, left on top, then center, then right; (2) fonts and icons scale down within their zone, never below readable text and a 24×24 px target (scaling is always tried before clipping); (3) what still does not fit depends on the zone's kind: a control zone clips it at its edge, a content zone (calendar grid, list, table, log) scrolls it. The layout does not mirror for right-to-left languages. No component has its own responsive rule (build_rules/theme.md, 13a). | — | Developer, Nov 17 |
| UI-15 |  | A badge or other overlay on an image or control is placed by one of nine anchor points of its parent (the corners, the edge middles and the center) plus an offset relative to the parent's size, both defined in the theme (build_rules/theme.md, 13b); no component places its own badge. | — | Developer, Nov 17 |

## Proposed (not yet reviewed)

## Time (TIM)

| ID | status | statement |
|---|---|---|
| TIM-08 | proposed (?) | An imported event that carries no time zone gets a default zone (open: Q-T9). |
| TIM-09 | proposed | A time zone name that is not a real zone is refused wherever a zone is chosen (S19-30). |

Decided elsewhere, not repeated: UTC instants hide daylight-saving jumps, and the default rule "24-hour events" (RUL-29) realigns a
fixed 24-hour source span to the local day.

## UI (UI)

| ID | status | statement | evidence |
|---|---|---|---|
| UI-01 | proposed | A dialog opens centered over a dimmed backdrop. In a phone-width window it fills the screen and shows a Back control instead of the dialog header. | S44-27, S57-20, S36-57, S57-37 |
| UI-02 | proposed | Back closes the dialog. Escape closes only the topmost open layer (a menu, time list or picker) and a second Escape closes the dialog. A dialog opened from another returns to it when closed. | S57-28..30, S58-32, S37-36, S67-15..17 |
| UI-03 | proposed | A dialog fits the window height; its content area grows with a taller field (such as Notes). | S57-23, S57-24 |
| UI-05 | proposed | A section (Rules, Event Templates, History...) shows a title, status lines, a count box and one plus control; its body stays hidden until expanded; clicking the title alone does not expand it. | S33-24, S38-01, S38-13, S61-02 |
| UI-06 | proposed | An action that hides or deletes something asks first with a No \| Yes pair; cancelling changes nothing. | S57-33, S58-24, S58-25, S58-35, S44-26 |
| UI-07 | proposed | An info dot shows its explanatory text on click and opens above or below its icon as space allows. | S58-01, S58-34, S57-35, S66-18 |
| UI-08 | proposed | A checkbox's label ticks it when clicked; empty space beside the label does not. | S21-19, S21-20 |
| UI-09 | proposed | The calendar picker is a small month calendar with previous/next month and Today; it opens on a given month, can mark items unselectable, and closes when an item is picked. | S58-07..12, S58-28..30 |
| UI-10 | proposed | One shared color palette of named colors (Google's eleven event colors) is used wherever a color is chosen (rule action, event, calendar); the event editor adds a "calendar default" choice. A picked color shows and closes the palette. | S19-08, S19-41, S19-44, S40-09..11 |

Pending: the Save | Cancel pair is covered by SET-07; the section header color tokens belong to the theme.
| UI-11 | proposed | One shared emoji picker, with search, is used wherever an emoji is chosen. | S44-41 |

## Capabilities (CAP)

What a user may do with a calendar or an event follows from where it comes from, stated once here. Features reference these rows
instead of listing "never for read-only", "not for rule events" and similar exceptions (Developer, Nov 17: fix the requirement,
do not add exceptions). Origins: **imported** (from a source CalendarStream only reads, such as CCS+), **custom** (added in
CalendarStream), **rule** (made by a rule).

| ID | status | statement |
|---|---|---|
| CAP-01 | proposed | Imported and custom events can be edited; a rule event cannot be opened for editing, because its rule controls it (remote edits to it are corrected on sync, GGL-55). |
| CAP-02 | proposed | An imported event can be hidden and shown again, never deleted from its source; a custom event can be deleted, and a deletion can be undone. |
| CAP-03 | proposed | Only custom events can be moved to another calendar; an imported event of a read-only source never is (EVT-02). |
| CAP-04 | proposed | Imported and custom events can be link targets; a rule event cannot. |
| CAP-05 | proposed | Any calendar CalendarStream owns (a Local calendar) can be the default calendar; a read-only source calendar cannot. |
| CAP-06 | proposed | Sync Now is offered only for calendars that download from outside; a Local calendar has nothing to download. |
