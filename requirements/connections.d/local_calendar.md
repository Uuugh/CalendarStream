# Requirements: Local calendar

The Local calendar connection: a calendar the user keeps in the app itself, which can be added to and edited. Common connection rules are in `connections.md`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CLCL-01 | proposed | A Local calendar is a calendar the user keeps in the app itself. | — | — |
| CLCL-01.f | proposed | A Local calendar is a source. | — | — |
| CLCL-01.a | proposed | A fresh installation starts with one Local calendar as the default, with no configured CCS+ source or destinations. | — | S26-01, S26-02, S36-19, S49-01, S63-12 |
| CLCL-01.b | proposed | Local calendars do not offer Sync Now (CAP-06); the default calendar is identified (CLCL-03). | — | S36-20, S36-23, S36-24, S49-02, S63-16 |
| CLCL-01.c | proposed | Additional Local calendars can be created; an unnamed one is named Local. | — | S36-22, S36-48 |
| CLCL-01.d | proposed | When a Local calendar is created because none exists, it is added to every existing feed; after that each feed decides which calendars it carries (CFED-01). | — | changelog_gaps_1201-1500:18 |
| CLCL-01.e | proposed | Removing the last Local calendar keeps that calendar and empties its events, rather than leaving no Local calendar; its feed and rule memberships are kept, and ensuring a Local calendar afterward does not create a duplicate. | — | S36-46, S36-47, S49-32, readme_gaps:63, changelog_gaps_601-900:39 |
| CLCL-01.g | proposed | A Local calendar's status is Healthy with no message, and no checks run for it. | — | R4 gap |
| CLCL-01.h | proposed | A Local calendar created because none exists is named msg:local the first time and CalendarStream afterward, is placed first in the list and becomes the default. | — | R4 gap |
| CLCL-02 | proposed | The user can import a calendar file into a Local calendar. | — | — |
| CLCL-02.a | proposed | Source calendars offer file import. | — | S18-15, S44-38 |
| CLCL-02.b | proposed | Importing with a date range (UIC-23) excludes events outside it; completing import creates events from the included entries. | — | S49-21, S49-22 |
| CLCL-02.c | proposed | Importing an entry that conflicts with an existing event identifies the conflict; choosing merge preserves the incoming changed event and other included entries. | — | S49-23, S49-24 |
| CLCL-02.d | proposed | When an imported event conflicts with an existing event, the user can discard the incoming copy. | — | readme_gaps:62, changelog_gaps_601-900:36 |
| CLCL-02.e | proposed | An import-conflict choice can be applied to all remaining conflicts in that import. | — | readme_gaps:62, changelog_gaps_601-900:36 |
| CLCL-02.f | proposed | An import file larger than the download size in DEF-01 is refused with msg:thatFileIsTooLargeToImport; a file that does not start like a calendar is refused with msg:thatFileIsnTA. | — | R4 gap |
| CLCL-02.g | proposed | Import dates are days (YYYY-MM-DD) in the years in DEF-01; recurring events of the file are expanded within the range, cancelled events are skipped, and at most the events per download in DEF-01 are read. | — | R4 gap |
| CLCL-02.h | proposed | When no event is left after the range, the import is refused with msg:noEventsInThatFile. | — | R4 gap |
| CLCL-02.i | proposed | An imported event is a conflict when its identifier (without the import prefix) equals that of an event in the calendar that is neither made by a rule nor deleted, or of an event imported before; the conflict list shows the title, day and time of both. | — | R4 gap |
| CLCL-02.j | proposed | Checking a file gives a check result with the number of events and the conflicts; it is valid for the time in DEF-01 and for one finish only, and an older or used result is refused with msg:thatImportHasExpired. | — | R4 gap |
| CLCL-02.k | proposed | Finishing an import for a calendar that was removed meanwhile is refused with msg:thatCalendarIsntHereAnyMore. | — | R4 gap |
| CLCL-02.l | proposed | Finishing the import adds each event without a match to the calendar with no color and a new identifier of the form cs-<16 hexadecimal digits>@calendar_stream, remembering the file's own identifier so that importing the file again matches it. | — | R4 gap |
| CLCL-02.m | proposed | For a match, the choice Merge replaces the title, start, end, all-day setting, location and notes of the existing event with the file's (stored as an edit when the event comes from a source, EVT-01), and any other choice keeps the existing event; a merge onto an event that has vanished is not counted. | — | R4 gap |
| CLCL-02.n | proposed | A finished import is recorded in History as msg:importedFileInto ({file} is the file name, or Calendar.ics when it has none), then msg:importedMerged when events were merged and msg:importedAlreadyThere when events were already there; it can be undone. | — | R4 gap |
| CLCL-03 | proposed | One Local calendar is the default for the events the user adds. | — | — |
| CLCL-03.a | proposed | A Local calendar can be selected as default; a read-only CCS+ calendar cannot (CAP-05). | — | S63-13, S63-14, S63-15, S66-04 |
| CLCL-03.b | proposed | A valid saved Local default calendar is used whatever the source order; if it no longer exists, the first Local calendar is used. With no sources, creating a Local calendar also makes it the default. | — | S77-13, S77-14, S77-15 |
| CLCL-03.c | proposed | Making a calendar the default is recorded in History as msg:defaultCalendarName and can be undone; choosing the calendar that already is the default changes nothing. | — | R4 gap |
