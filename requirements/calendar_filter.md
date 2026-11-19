# Requirements: calendar_filter

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| FLT-01 | proposed | The Calendar filter chooses which calendars and event states the calendar shows, and what is printed. | — | — |
| FLT-01.a |  | The Calendar filter is one filter icon with a dropdown (UI-12). It lists every calendar with its color and the event states (Edited, Changed by the source since the edit, Hidden from Google, Deleted); choosing items shows only those events. It changes only what the calendar shows: nothing changes in Sources, Feeds, Rules or the other sections. | — | S34-04, S45-25 |
| FLT-01.b |  | The Calendar filter follows the common filter rules (UI-21). | — | S65-09, S67-52, S67-53, S67-54, S67-55 |
| FLT-01.c |  | The Calendar filter's choices are also kept when leaving Full page (UI-21). | — | S64-05, S64-07, S65-08 |
| FLT-01.d |  | The filter applies in every view and mode (Month, Week, Day, List, Full page) and Print follows it: what the user chooses to see is what is printed (Developer, Nov 17). | — | S65-32, S67-42 |
| FLT-01.e |  | A calendar's name and color in the filter follow its source: renaming it or changing its color shows at once (UI-13). | — | S34-16, S38-16 |
| FLT-01.f |  | Under the calendar sit Calendars (each with its (i)) and Key (rule colors and the event states of FLT-01.a), side by side with a thin vertical line between, in columns of at most three rows. A click on an item dims or hides its events on the calendar and in Print, in every mode. | — | theme.md Clarifications |
| FLT-01.g |  | View All, an eye icon on the Key title's line, is shown only when something is dimmed and clears every dimmed item at once. | — | theme.md Clarifications |
| FLT-01.h |  | A rule's key name is cut to the length in DEF-01, with its full name as the tooltip. | — | theme.md Clarifications |
| FLT-01.i |  | The calendar header shows the title and controls only. The filter lists calendars and event states only, with no Timed, All-day or Added color labels. | — | theme.md Clarifications |

