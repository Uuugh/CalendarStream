# Requirements: connections

What every connection does; each kind of connection adds only its specifics, in `connections.d/`. Connections are modules listed in a section; a connection is a local, one-way or two-way synchronization, and may need a plugin (plugins.md).
Terms: **one-way** sends changes from CalendarStream to the other side only, **two-way** also reads changes made on the other side; a **downloaded** connection (CCS+, a calendar link) reads a calendar from the internet and is read-only here; a **published** event is an event sent out by a feed or by a Google connection.
Connections: Local Calendar (`local_calendar.md`), Generic Feed (`generic_feed.md`), CCS+ (`ccs.md`), calendar link (`calendar_link.md`), Google one-way sync (`google_one_way.md`) and Google two-way sync (`google_two_way.md`), all in `connections.d/`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CON-01 | | A connection synchronizes calendar events locally, one-way or two-way. | — | — |
| CON-01.a | | Local Calendar, Generic Feed, CCS+, calendar link, Google one-way sync and Google two-way sync are connections. | — | — |
| CON-01.b | | A connection that needs a plugin can be added only while that plugin is set up: a Google connection requires the Google plugin (GAP-01). | — | — |
| CON-02 | proposed | A connection is named, colored and annotated. | — | — |
| CON-02.a | proposed | A source can be renamed and given a note; saving updates its name and explanatory note, and clearing the note removes its content. | — | S18-17, S29-11, S33-05, S39-18, S44-16 |
| CON-02.b | proposed | Source color can be changed and saved; the new color is reflected immediately in its source display. | — | S38-15, S59-22 |
| CON-02.c | proposed | Legacy source notes that merely repeat the source kind are treated as absent notes. | — | changelog_gaps_901-1200:24 |
| CON-02.d | proposed | The user can change source-calendar and outgoing-feed order, and the new order is saved immediately; shared interaction follows UI-13. | — | readme_gaps:59, changelog_gaps_1201-1500:15 |
| CON-03 | proposed | Each source shows its status and can be synced or turned off. | — | — |
| CON-03.a | proposed | Sync Now updates a source in the background: it reports Syncing during work and Healthy on success, and keeps unrelated unsaved source edits. | — | S33-15, S33-18, S33-19, S35-28, S35-29, S35-31, S44-18 |
| CON-03.b | proposed | A source reports when it last synced (a download or an upload) or that a read, check or download failed. | — | S44-11, S27-05, S31-04, S31-19, S40-04, S35-32 |
| CON-03.c | proposed | A successful feed download reports healthy status even when another source has no events. | — | S26-11 |
| CON-03.d | proposed | The source status event count counts the published feed events, with event visibility determined by CAP-02. | — | changelog_gaps_2101-2336:30 |
| CON-03.e | proposed | A source can be turned off and back on, with its saved off state cleared when reenabled. | — | S63-20, S63-21, S63-23 |
| CON-03.f | proposed | Turning a source off removes its events from published feeds while retaining its selected feed memberships for reenabling. | — | changelog_gaps_301-600:23 |
| CON-03.g |  | A module's status line says "Last synced" or "Sync failed" with its time, never "Last check was successful"; the line beside the action says "Next check @" with its time. | — | theme.md Clarifications |
| CON-04 | proposed | The user can remove a source, and keep or merge its events. | — | — |
| CON-04.a | proposed | Removing a source removes its stored events and its membership from destinations, while keeping a combined Google destination. | — | S26-50, S26-51 |
| CON-04.b | proposed | Removing a source can preserve its events by creating a Local calendar with its prior color and destination memberships, or by merging into an existing Local calendar. The original source is removed. | — | S37-20, S37-21, S37-22, S49-28 |
| CON-04.c | proposed | Calendar removal identifies its owned rules, and deleting the calendar removes those rules. | — | S49-27, S49-31 |
| CON-04.d | proposed | When merging a calendar into another, the user can transfer its owned rules to the target or delete those rules. | — | readme_gaps:63, changelog_gaps_601-900:39 |
| CON-05 | proposed | A source is downloaded automatically on a schedule, and the user can change the schedule. | — | — |
| CON-05.a | proposed | The automatic-download interval is an admin setting kept in the database; the installation's value is only its starting value (DEP-05, DEF-01). | — | S14-04, S14-05, S14-11, S14-12, changelog_gaps_2101-2336:38 |
| CON-05.b | proposed | The download interval stays within the limits in DEF-01; a value outside them, or not a number, is not valid (UI-19). | — | S14-08, S14-09, readme_gaps:31, changelog_gaps_1801-2100:34 |
| CON-05.c | proposed | The next download is scheduled from the last attempt plus the configured interval; if that time has passed, changing the interval schedules an immediate download. | — | S14-06, S14-07 |
| CON-05.d | proposed | Changes to download settings or source credentials follow the shared form-security rules (ACC-09). | — | S14-10, S16-28 |
| CON-06 | proposed | A download gets the calendar safely and reports clearly when it cannot. | — | — |
| CON-06.a | proposed | Calendar downloads, including a custom CCS+ site address, require HTTPS; a plain HTTP address is not valid. Clearing a custom CCS+ address removes the override. | — | S23-28, S26-07, S60-21, S27-02, S27-03, S27-04 |
| CON-06.b | proposed | An HTTPS redirect on the same host can complete the download; a redirect to plain HTTP is refused, and a redirect loop is reported. | — | S60-14, S60-15, S60-16 |
| CON-06.c | proposed | Following a calendar redirect to a different host does not forward the source’s authorization credentials. | — | S60-18 |
| CON-06.d | proposed | Calendar downloads keep sign-in credentials out of process command-line arguments; stored and displayed secret protection follows ACC-05. | — | changelog_gaps_2101-2336:31 |
| CON-06.e | proposed | A download larger than the size limit in DEF-01 is not accepted. | — | S60-17 |
| CON-06.f | proposed | A download keeps at most the number of events in DEF-01; the earliest events are kept, whatever the input order. | — | S53-14, changelog_gaps_601-900:22 |
| CON-06.g | proposed | A downloaded calendar retains calendar content and cache validators; a matching ETag can return an unchanged result rather than downloading the content again. | — | S60-05, S60-10 |
| CON-06.h | proposed | A wrong download password is reported as a credential rejection; upstream protection denial is reported as blocking, not as invalid credentials. A rejected password ends the download attempt at once, without trying another connection mode or spending a retry delay. | — | S60-11, S60-12, S60-25, S60-26, changelog_gaps_301-600:40 |
| CON-06.i | proposed | A successful HTTP response containing HTML instead of calendar data is refused; malformed calendar data is also refused. | — | S60-13, S77-08, S77-09 |
| CON-06.j | proposed | A download that does not reply reports a timeout and explains the manual-upload alternative. | — | S60-19 |
| CON-06.k | proposed | Download failure feedback distinguishes failure to connect from a connected server that does not reply. | — | changelog_gaps_2101-2336:33 |
| CON-06.l | proposed (?) | Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? | — | S60-22, S60-23, S60-24 |
| CON-06.m | proposed | A failed source download preserves the previously downloaded schedule. | — | readme_gaps:22, changelog_gaps_2101-2336:37 |
| CON-06.n | proposed (?) | A source download that unexpectedly returns an empty calendar preserves the previous schedule. How is an unexpected empty response distinguished from an intentionally emptied source? | — | readme_gaps:22, changelog_gaps_2101-2336:37 |
| CON-07 | proposed | A downloaded or imported schedule becomes events with their times and recurrences. | — | — |
| CON-07.a | proposed | Recurring source events expand into distinct occurrences while retaining source-qualified identities. Moving one recurrence preserves the occurrence identities and updates its changed title. | — | S26-10, S53-13 |
| CON-07.b | proposed | Recurring source events are expanded over the period in DEF-01. | — | readme_gaps:61, changelog_gaps_1501-1800:24 |
| CON-07.c | proposed | When a recurring source occurrence moves, its existing local edits remain attached using its original-start identity. | — | changelog_gaps_601-900:21 |
| CON-07.d | proposed | Free/busy information from an imported calendar is preserved: events marked transparent remain free. | — | S13-01 |
| CON-07.e | proposed | When source events conflict, the earlier source in the saved source order has priority. | — | readme_gaps:60, changelog_gaps_301-600:27 |
| CON-07.f | proposed | A future event that disappears from a refreshed source schedule is kept for restoration, with its title, until its deletion leaves History (HIS-03). | — | S49-17 |
| CON-08 | proposed | A connection's calendar can be exported. | — | — |
| CON-08.a | proposed | Calendar export downloads an ICS attachment containing its events. | — | S49-26 |
| CON-09 | proposed | Events published by a feed or a Google connection carry the same event content. | — | — |
| CON-09.a | proposed | A published event keeps its own time zone (TIM-07), its title, and its start and end; the page's display time zone does not change them. | — | S19-32, S77-07 |
| CON-09.b | proposed | A published event carries its display reminders, including fifteen-minute and one-hour reminders. Reminder selection belongs to EVT-03. | — | S36-26 |
| CON-09.c | proposed | A published event's online meeting address is also the first line of its notes (EVT-03 owns the ICS URL). | — | changelog_gaps_301-600:22 |
| CON-09.d | proposed | A hidden event is not published, and hiding an event removes its published copy. Visibility is CAP-02 and EVT-04. | — | readme_gaps:47, S13-17 |
