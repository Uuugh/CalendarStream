# Requirements: connections

This file establishes the rules for creating a connection module: what every connection does and what each one must state in its own file in `connections.d/` (its role, its connection method when it downloads, and the plugin it needs), and nothing else that is common. Connections are modules listed in a section; a connection is a local, one-way or two-way synchronization (plugins are in plugins.md).
Terms: **one-way** moves events in one direction only (a source brings them in, a feed sends them out), **two-way** does both; a **downloaded** connection (CCS+, a calendar link) reads a calendar from the internet and is read-only here; a **published** event is an event sent out by a feed or by a Google connection.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CON-01 | backlog | A connection synchronizes calendar events locally, one-way or two-way. | — | — |
| CON-01.a | backlog | Every kind of connection is a connection module with its own file in `connections.d/`. | — | — |
| CON-01.c | backlog | Each connection is a source (it brings events in), a feed (it sends events out) or both, and says so in its own file. A section contains every connection that has its capability, so a connection that is both is contained by the Sources and the Feeds sections: it is one module, and a change or removal made in either place applies to the connection. | — | — |
| CON-01.b | backlog | A connection that needs a plugin can be added only while that plugin is set up: a Google connection requires the Google plugin (PGAP-01). | — | — |
| CON-01.d | backlog | The number of connections has the limit in DEF-01; at the limit the + of a section is disabled and says the limit. | — | readme_gaps:20 |
| CON-01.e | proposed | Each connection has a generated identifier that is never equal to another's: the letter f and six hexadecimal digits for a calendar link, the letter l and six hexadecimal digits for a Local calendar. | — | R4 gap |
| CON-01.f | proposed | Adding a source records History msg:calendarSourceAdded (can be undone), builds its calendar content and starts its checks at once. | — | R4 gap |
| CON-02 | proposed | A connection is named, colored and annotated. | — | — |
| CON-02.a | proposed | A source can be renamed and given a note; saving updates its name and explanatory note, and clearing the note removes its content. | — | S18-17, S29-11, S33-05, S39-18, S44-16 |
| CON-02.b | proposed | Source color can be changed and saved; the new color is reflected immediately in its source display. | — | S38-15, S59-22 |
| CON-02.c | proposed | A note that merely repeats the connection's kind is treated as no note. | — | changelog_gaps_901-1200:24 |
| CON-02.d | backlog | A connection's kind is fixed text in its module header, stated in its own file. | — | theme.md Clarifications |
| CON-02.e | proposed | A connection is shown as a module: its header, Expand and Close follow UIC-29, and its look follows THM-08. | — | — |
| CON-02.f | proposed | A connection's name is cut to the length in DEF-01 after repeated whitespace is collapsed, and its note to the length in DEF-01. | — | R4 gap |
| CON-02.g | proposed | Saving a name or color records History msg:sourceSaved ({source} is the connection, {name} its name, {color} #rrggbb or msg:defaultColor2), can be undone and rebuilds the connection's calendar content (CON-07). | — | R4 gap |
| CON-02.h | proposed | A color is #rrggbb in any letter case, stored in lower case; anything else is refused with msg:chooseTheColorWithThe. Choosing the default color deletes the saved one; a connection with no color shows the theme's accent color and its published events carry none. | — | R4 gap |
| CON-03 | proposed | Each source shows its status and can be synced or turned off. | — | — |
| CON-03.a | proposed | Sync Now updates a source in the background: it reports Syncing during work and Healthy on success, and keeps unrelated unsaved source edits. Sync Now answers after the time in DEF-01 and, if the run is still going, the page follows its status until it is done. | — | S33-15, S33-18, S33-19, S35-28, S35-29, S35-31, S44-18 |
| CON-03.b | proposed | A source reports when it last synced (a download or an upload) or that a read, check or download failed. | — | S44-11, S27-05, S31-04, S31-19, S40-04, S35-32 |
| CON-03.c | proposed | A successful feed download reports healthy status even when another source has no events. | — | S26-11 |
| CON-03.d | proposed | The source status event count counts the published feed events, with event visibility determined by CAP-02. | — | changelog_gaps_2101-2336:30 |
| CON-03.e | proposed | A source can be turned off and back on, with its saved off state cleared when reenabled. | — | S63-20, S63-21, S63-23 |
| CON-03.f | proposed | Turning a source off removes its events from published feeds while retaining its selected feed memberships for reenabling. | — | changelog_gaps_301-600:23 |
| CON-03.g | backlog | A connection's status line says when it last did its work, with its time, in its own words: "Last synced" or "Sync failed" for a connection that synchronizes, "Last read" for a feed (CFED-05); never "Last check was successful". A connection that checks on a schedule also shows "Next check @" with its time beside the action. | — | theme.md Clarifications |
| CON-03.h | proposed | A source's status chip reads msg:healthy (good), msg:syncing, msg:starting, msg:setupNeeded, msg:paused (in progress), msg:signInRejected, msg:blocked, msg:error (warning) or msg:internalError (bad). | — | R4 gap |
| CON-03.i | proposed | A download run ends Healthy, Sign-in rejected, Blocked, Error or Internal error, and records History msg:signInRejected2 for a rejected sign-in, msg:blocked2 for a block, msg:downloadFailed for any other source error and msg:unexpectedError for a failure of the app itself. | — | R4 gap |
| CON-03.j | proposed | An accepted download sets the status to Healthy, records the last-success time and, when the calendar differs, the last-change time; its detail is msg:firstCopy for the first copy, msg:newRemoved ({n} new and {n2} removed events, counted by identifier) when it changed and msg:noChanges when it did not; the status message is msg:eventsInFeed2 and History records msg:scheduleEventsInFeed, where {how} is msg:downloadedFromCcs, msg:uploadedByHand or msg:downloadedFromHost. | — | R4 gap |
| CON-03.k | proposed | A source's status, message, attempt, success and change times, last sign-in, count of rejected sign-ins, event count and last detail are kept across a restart; a status of Syncing at the time of the stop comes back as Starting. | — | R4 gap |
| CON-03.l | proposed | A source's module opens by itself when its status is not Healthy, Syncing or Starting, or when CCS+ has no credentials. | — | R4 gap |
| CON-03.m | proposed | A paused connection shows msg:automaticChecksPaused in place of the next-check time. | — | R4 gap |
| CON-03.n | proposed | Turning a calendar Off or On is recorded in History as msg:calendarSwitchedOff or msg:calendarSwitchedOn and can be undone, and every Google connection that carries the calendar then runs a full sync (CGOW-04). | — | R4 gap |
| CON-03.o | proposed | Verifying a downloaded connection waits for a running download (at most the time in DEF-01), runs a download as Sync Now does and answers msg:validated or msg:verifyFailed; it succeeds when the status is Healthy afterward (CCCS-02 adds a condition for CCS+). | — | R4 gap |
| CON-04 | proposed | The user can remove a source, and keep or merge its events. | — | — |
| CON-04.a | proposed | Removing a source removes its stored events and its membership from destinations, while keeping a combined Google destination. | — | S26-50, S26-51 |
| CON-04.b | proposed | Removing a source can preserve its events by creating a Local calendar with its prior color and destination memberships, or by merging into an existing Local calendar. The original source is removed. | — | S37-20, S37-21, S37-22, S49-28 |
| CON-04.c | proposed | Calendar removal identifies its owned rules, and deleting the calendar removes those rules. | — | S49-27, S49-31 |
| CON-04.d | proposed | When merging a calendar into another, the user can transfer its owned rules to the target or delete those rules. | — | readme_gaps:63, changelog_gaps_601-900:39 |
| CON-04.e | proposed | Removing a source asks what to do with its events: delete them (the default) or merge them into another calendar; with a merge it also asks whether its own rules move with them or are deleted (the default). | — | R4 gap |
| CON-04.f | proposed | Merged events are in their current state with their edits, without hidden events and events made by rules; their start and end are kept, their time-zone overrides are cleared, and their reminders and links follow them. | — | R4 gap |
| CON-04.g | proposed | The rules that belong only to the removed calendar are deleted or moved to the target; a rule that belongs to several calendars loses the removed one; a rule that belongs to all calendars stays. | — | R4 gap |
| CON-04.h | proposed | Removing a source stops its checks, removes it from every feed and deletes all its stored settings, and records History msg:calendarSourceRemoved, msg:calendarSourceRemovedMerged or msg:calendarSourceRemovedMergedRules; the removal can be undone. | — | R4 gap |
| CON-04.i | proposed | Before a source is removed the user is offered a copy of its calendar to download. | — | R4 gap |
| CON-05 | proposed | A source is downloaded automatically on a schedule, and the user can change the schedule. | — | — |
| CON-05.a | proposed | The automatic-download interval is an admin setting kept in the database; the installation's value is only its starting value (DEP-05, DEF-01). | — | S14-04, S14-05, S14-11, S14-12, changelog_gaps_2101-2336:38 |
| CON-05.b | proposed | The download interval stays within the limits in DEF-01; a value outside them, or not a number, is not valid (UIC-19). | — | S14-08, S14-09, readme_gaps:31, changelog_gaps_1801-2100:34 |
| CON-05.c | proposed | The next download is scheduled from the last attempt plus the configured interval; if that time has passed, changing the interval schedules an immediate download. | — | S14-06, S14-07 |
| CON-05.d | proposed | Changes to download settings or source credentials follow the shared form-security rules (ACC-09). | — | S14-10, S16-28 |
| CON-05.e | proposed | Each source that downloads is checked once when the app starts or the source is added, and then once per interval after the previous check ended. | — | R4 gap |
| CON-05.f | proposed | After an unexpected failure of a scheduled check the next check is made after the time in DEF-01. | — | R4 gap |
| CON-05.g | proposed | Saving the interval wakes the schedule and records History msg:checksEveryMinFromNow. | — | R4 gap |
| CON-05.h | proposed | The interval field offers whole numbers in the step in DEF-01, within the limits in DEF-01. | — | R4 gap |
| CON-06 | proposed | A download gets the calendar safely and reports clearly when it cannot. | — | — |
| CON-06.a | proposed | A downloaded connection states its connection method in its own file (for example HTTPS, curl, web scrape or RSS), and downloads with it. | — | S23-28, S26-07, S60-21, S27-02, S27-03, S27-04 |
| CON-06.b | proposed | A redirect on the same host can complete the download; a redirect to a less secure address than the connection's method is refused, and a redirect loop is reported. | — | S60-14, S60-15, S60-16 |
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
| CON-06.n | proposed | A download that returns no events while the connection already has events is refused and the previous schedule stays; an empty download is accepted only when there were no events. | — | readme_gaps:22, changelog_gaps_2101-2336:37 |
| CON-06.o | proposed | Cache validators are stored when a download is accepted and are sent when they are not empty; a not-modified answer sets the status to Healthy, records History msg:scheduleNoChanges as information and shows msg:upToDateEventsIn. | — | R4 gap |
| CON-06.p | proposed | The first bytes of a reply (the length in DEF-01) must contain the calendar start BEGIN:VCALENDAR; a reply that lacks it is reported as msg:whoAnsweredNotCalendar ({who} is CCS+ or the link's host, {type} the content type or msg:unknownType, {details} the first characters of the reply, the length in DEF-01). | — | R4 gap |
| CON-06.q | proposed | HTTP 403 is reported as a block: msg:accessDeniedByHttp4032, or msg:accessDeniedByHttp403 when the reply carries a reference number ({ref}); {who} is msg:akamaiUnitedsBotProtection when the Server header contains akamai in any letter case, else the Server header, else msg:theServer. | — | R4 gap |
| CON-06.r | proposed | Any other HTTP status of 400 or more is reported as msg:whoAnsweredHttp ({who} as above, {details} the first characters of the reply without tags, the length in DEF-01, or msg:noDetails). | — | R4 gap |
| CON-06.s | proposed | Failing to connect within the connect time limit in DEF-01 is reported as msg:couldnTConnectToWithin and any other network failure as msg:couldnTReach. | — | R4 gap |
| CON-06.t | proposed | A reply over the download size in DEF-01 is reported with msg:sentMoreThan5Mb. | — | R4 gap |
| CON-07 | proposed | A downloaded or imported schedule becomes events with their times and recurrences. | — | — |
| CON-07.a | proposed | Recurring source events expand into distinct occurrences while retaining source-qualified identities. Moving one recurrence preserves the occurrence identities and updates its changed title. | — | S26-10, S53-13 |
| CON-07.b | proposed | Recurring source events are expanded over the period in DEF-01. | — | readme_gaps:61, changelog_gaps_1501-1800:24 |
| CON-07.c | proposed | When a recurring source occurrence moves, its existing local edits remain attached using its original-start identity. | — | changelog_gaps_601-900:21 |
| CON-07.d | proposed | Free/busy information from an imported calendar is preserved: events marked transparent remain free. | — | S13-01 |
| CON-07.e | proposed | When source events conflict, the earlier source in the saved source order has priority. | — | readme_gaps:60, changelog_gaps_301-600:27 |
| CON-07.f | proposed | A future event that disappears from a refreshed source schedule is kept for restoration, with its title, until its deletion leaves History (HIS-03). It is kept, struck through, while it ends today or later, at most the number per download in DEF-01; an ended, hidden or rule-made event is not kept; History records msg:unitedRemovedEvents for CCS+ or msg:goneFromTheFeedEvents for a link, listing the first events in DEF-01 and ending with " …" when there are more, and each can be restored. | — | S49-17 |
| CON-07.g | proposed | An event without a start is skipped; its end is its end time, else its start plus its duration; an all-day event with no end lasts one day. | — | R4 gap |
| CON-07.h | proposed | An event with no title is titled msg:noTitle, its notes are cut to the length in DEF-01, and an event with no identifier gets one made from its start and title. | — | R4 gap |
| CON-07.i | proposed | A repeating event with an invalid rule is skipped without dropping the rest of the file, an event whose status is cancelled is skipped, and of two events with the same identifier in one file the first is kept. | — | R4 gap |
| CON-07.j | proposed | Events of different sources never merge or replace one another. | — | R4 gap |
| CON-07.k | proposed | Any change of a connection's name, color, rules or events rebuilds its calendar from the last downloaded copy without downloading again, applying in this order: time changes by rules, edits and added events, events made by rules, rule colors and emoji, reminders; hidden events are not counted. | — | R4 gap |
| CON-08 | proposed | A connection's calendar can be exported. | — | — |
| CON-08.a | proposed | Calendar export downloads an ICS attachment containing its events. | — | S49-26 |
| CON-08.b | proposed | An export holds the connection's events as they are now with their edits, without hidden events and events made by rules. | — | R4 gap |
| CON-08.c | proposed | The exported file is named after the connection with every character other than letters, digits, space, dot, underscore and hyphen removed, plus .ics (calendar.ics when nothing is left); its header carries the name, the Local time zone and the color in the format of a feed (CFED-04). | — | R4 gap |
| CON-09 | proposed | Events published by a feed or a Google connection carry the same event content. | — | — |
| CON-09.a | proposed | A published event keeps its own time zone (TIM-07), its title, and its start and end; the page's display time zone does not change them. | — | S19-32, S77-07 |
| CON-09.b | proposed | A published event carries its display reminders, including fifteen-minute and one-hour reminders. Reminder selection belongs to EVT-03. | — | S36-26 |
| CON-09.c | proposed | A published event's online meeting address is also the first line of its notes (EVT-03 owns the ICS URL). | — | changelog_gaps_301-600:22 |
| CON-09.d | proposed | A hidden event is not published, and hiding an event removes its published copy. Visibility is CAP-02 and EVT-04. | — | readme_gaps:47, S13-17 |
| CON-09.e | proposed | A published calendar can be limited by a date range (UIC-23); with no range it publishes its full event set. | — | S29-02, S29-04, S39-19, S29-03, S51-13 |
| CON-09.f | proposed | A published event carries its identifier, the time it was published (UTC), its title, and its location and notes when they are not empty; a free event is marked transparent. | — | R4 gap |
| CON-09.g | proposed | A published event carries a marker saying whether it was added on the page (added), made by a rule (rule), a source event changed on the page (edited) or unchanged from its source (source). | — | R4 gap |
| CON-09.h | proposed | A published event's reminders are display reminders titled with the event's title, in whole minutes, without duplicates, largest first. | — | R4 gap |
| CON-01.g | proposed | A Google account added later gets an identifier of the letter a and six hexadecimal digits, and the CCS+ connection has the identifier ccs. | — | R6 gap |
| CON-03.p | proposed | A failed download of a feed is always Error, with the reason as its message. | — | R6 gap |
| CON-03.q | proposed | A rejected sign-in raises the count of rejected sign-ins in a row by one, and a successful reply sets it to 0. | — | R6 gap |
| CON-03.r | proposed | A CCS+ check with no login saved sets only the status Setup with msg:enterYourCcsUsernameAnd and records no History line. | — | R6 gap |
| CON-06.u | proposed | Checks start when the app starts and when a source is added; a Local calendar has no checks. | — | R6 gap |
| CON-06.v | proposed | The browser-like download client imitates the newest browser version it knows; a feed is always downloaded with the plain client. | — | R6 gap |
| CON-06.w | proposed | Every download waits for the connect time and the total time in DEF-01 (Download time limits) and reports a timeout as a download failure. | — | R6 gap |
| CON-06.x | proposed | A reply that does not look like a calendar is quoted in the error from the start of the reply up to the length in DEF-01, shortened to the snippet length in DEF-01. | — | R6 gap |
| CON-07.l | proposed | A source event with a date only as its start is an all-day event, lasting one day when it has no end. | — | R6 gap |
| CON-07.m | proposed | A timed source event starting exactly at midnight with no end or duration becomes one all-day event. | — | R6 gap |
| CON-07.n | proposed | A timed source event not starting at midnight with no end is read with its end equal to its start and flagged as having no end, so that rules decide its length; one that no rule changes gets the default length (the event hours setting). | — | R6 gap |
