# Requirements: Local calendar

The Local calendar connection: a calendar the user keeps in the app itself, which can be added to and edited. Common connection rules are in `connections.md`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CLL-01 | proposed | A Local calendar is a calendar the user keeps in the app itself. | — | — |
| CLL-01.f | proposed | A Local calendar is a source. | — | — |
| CLL-01.a | proposed | A fresh installation starts with one Local calendar as the default, with no configured CCS+ source or destinations. | — | S26-01, S26-02, S36-19, S49-01, S63-12 |
| CLL-01.b | proposed | Local calendars do not offer Sync Now (CAP-06); the default calendar is identified (CLL-03). | — | S36-20, S36-23, S36-24, S49-02, S63-16 |
| CLL-01.c | proposed | Additional Local calendars can be created; an unnamed one is named Local. | — | S36-22, S36-48 |
| CLL-01.d | proposed | When a Local calendar is created because none exists, it is added to every existing feed; after that each feed decides which calendars it carries (CFO-01). | — | changelog_gaps_1201-1500:18 |
| CLL-01.e | proposed | Removing the last Local calendar keeps that calendar and empties its events, rather than leaving no Local calendar; its feed and rule memberships are kept, and ensuring a Local calendar afterward does not create a duplicate. | — | S36-46, S36-47, S49-32, readme_gaps:63, changelog_gaps_601-900:39 |
| CLL-02 | proposed | The user can import a calendar file into a Local calendar. | — | — |
| CLL-02.a | proposed | Source calendars offer file import. | — | S18-15, S44-38 |
| CLL-02.b | proposed | Importing with a date range (UI-23) excludes events outside it; completing import creates events from the included entries. | — | S49-21, S49-22 |
| CLL-02.c | proposed | Importing an entry that conflicts with an existing event identifies the conflict; choosing merge preserves the incoming changed event and other included entries. | — | S49-23, S49-24 |
| CLL-02.d | proposed | When an imported event conflicts with an existing event, the user can discard the incoming copy. | — | readme_gaps:62, changelog_gaps_601-900:36 |
| CLL-02.e | proposed | An import-conflict choice can be applied to all remaining conflicts in that import. | — | readme_gaps:62, changelog_gaps_601-900:36 |
| CLL-03 | proposed | One Local calendar is the default for the events the user adds. | — | — |
| CLL-03.a | proposed | A Local calendar can be selected as default; a read-only CCS+ calendar cannot (CAP-05). | — | S63-13, S63-14, S63-15, S66-04 |
| CLL-03.b | proposed | A valid saved Local default calendar is used whatever the source order; if it no longer exists, the first Local calendar is used. With no sources, creating a Local calendar also makes it the default. | — | S77-13, S77-14, S77-15 |
