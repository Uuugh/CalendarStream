# Requirements: connections

What every connection does; each kind of connection adds only its specifics, in `connections.d/`. Connections are modules listed in a section; a connection is a local, one-way or two-way synchronization, and may need a plugin (plugins.md).
Terms: **one-way** sends changes from CalendarStream to the other side only, **two-way** also reads changes made on the other side.
Connections: Local Calendar, Generic Feed (feeds feature), CCS+ (sources feature), `connections.d/google_one_way.md`, `connections.d/google_two_way.md`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CON-01 | | A connection synchronizes calendar events locally, one-way or two-way. | — | — |
| CON-01.a | | Local Calendar, Generic Feed, CCS+, Google one-way sync and Google two-way sync are connections. | — | — |
| CON-01.b | | A connection that needs a plugin can be added only while that plugin is set up: a Google connection requires the Google plugin (GAP-01). | — | — |
