# Requirements: sources

The Sources section: the list of the user's calendars and which one new events go to. How each kind of source works is in its connection (`connections.md` and `connections.d/`).
Terms: a **source** is a place the app reads events from (CCS+, a calendar link, an uploaded file) or a **Local** calendar the user keeps in the app itself; **read-only** means events cannot be added or changed at the source (CAP-05).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| SRC-01 | proposed | The user's calendars come from sources of several kinds, and each can be named, colored and ordered. | — | — |
| SRC-01.a | proposed | The number of calendars and feeds is not limited. There is only one CCS+ calendar, the user's own schedule (SRC-01). | — | readme_gaps:20 |
| SRC-01.b | proposed | Source presets identify the provider and offer provider-specific setup guidance, including Google secret-address guidance and the United Airlines CCS+ name. Choosing Apple selects the Apple preset. | — | S33-01, S33-02, S33-23 |
| SRC-01.c |  | A source's kind is fixed text in its module header: CalendarStream, United Airlines CCS+, Google Calendar, Apple Calendar or Calendar Feed. The module is called Sources. | — | theme.md Clarifications |
| SRC-02 | proposed | One calendar is the default for the events the user adds. | — | — |
| SRC-02.a | proposed | A Local calendar can be selected as default; a read-only CCS+ calendar cannot (CAP-05). | — | S63-13, S63-14, S63-15, S66-04 |
| SRC-02.b | proposed | A valid saved Local default calendar is used whatever the source order; if it no longer exists, the first Local calendar is used. With no sources, creating a Local calendar also makes it the default. | — | S77-13, S77-14, S77-15 |
