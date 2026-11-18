# DRAFT requirements: common (shared by every feature; for the Developer's review)

Not approved. Requirements that more than one feature depends on are written ONCE here and the features reference them by ID
(Developer, Nov 17: "these requirements belong in common; the Google sync feature has a requirement to use the common
requirement, as could other feature modules"). Two groups: **Time** (prefix TIM) and **UI** (prefix UI). In the port this is the
shared domain package (time) and the client's shared widgets (UI). Evidence keys are from `requirements/inventory/`; looks stay in
`build_rules/theme.md`.

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
