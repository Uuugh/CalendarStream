# DRAFT requirements: shared UI (for the Developer's review)

Not approved. Behavior that more than one feature uses lives here ONCE (prefix `UI-`); a feature's requirements
reference it by ID and never repeat it. Owned by the client's `shared/ui` (generic widgets) and `shell`. Evidence
keys are from `requirements/inventory/`. Looks (sizes, colors) stay in `build_rules/theme.md`.

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
