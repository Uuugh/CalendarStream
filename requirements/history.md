# Requirements: history

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| HIS-01 | proposed | History records what changes in the app and what happens with Google, so the user can see what happened and why. | — | — |
| HIS-01.a | proposed | Activity records calendar changes, identifying the changed calendar. | — | S33-13 |
| HIS-01.b | proposed | A synchronization that changes events records in its activity summary how many events it added and how many it updated. | — | changelog_gaps_2101-2336:19, changelog_gaps_2101-2336:19 |
| HIS-01.c | proposed | When a Google change is saved locally, History records that outcome; when a newer local change wins, it records that the local change was kept. | — | S45-08, S45-17 |
| HIS-01.d | proposed | A deletion received from Google is recorded with its Google origin. | — | S45-20 |
| HIS-01.e | proposed | If a former Google client’s calendar cannot be reached for cleanup, History warns that manual deletion is needed. | — | S48-22 |
| HIS-01.f | proposed | A Google color-update failure records the failed operation, the upstream status and its reasons so the refusal can be diagnosed (CGOW-03). | — | S55-12, S56-20 |
| HIS-01.g | proposed | An unsigned Google connection produces one not-signed-in or unsynced warning; resetting the remembered warning permits a new one. | — | S68-03, S68-04, S68-05 |
| HIS-01.h | proposed | A failure or warning that repeats unchanged is recorded in History once, until it changes or clears. | — | CGOW-06, CGOW-05, CGOW-06, HIS-21 |
| HIS-01.i | proposed | An external removal or Google notification without an undoable local change does not become the current Undo entry. | — | S49-18, S49-41 |
| HIS-01.j | backlog | History's Activity health is the section health of UIC-05.g, with its sources as its items. | — | S36-43, S36-44 |
| HIS-01.k | proposed | When remote cleanup is deferred because the write budget was reached, History reports the deferred work. | — | S53-07, S53-08 |
| HIS-01.l | proposed | Completing Google API setup records a message identifying each Google connection that needs sign-in, has a sync error or has not completed its first sync. | — | changelog_gaps_1-300:L22 |
| HIS-02 | proposed | History lists its entries with their type, in a table the user can filter and rearrange. | — | — |
| HIS-02.a | proposed | History names the type of each change: Calendar, Rule, Event, Sync, Feed, Google, Settings or Update. | — | S49-13, changelog_gaps_601-900:31 |
| HIS-02.b | proposed | History has a filter that follows the common filter rules (UIC-21), with three parts: the change type (the types in HIS-02), words in its entries, and the time of its entries. | — | readme_gaps:71, changelog_gaps_601-900:31 |
| HIS-02.c | proposed | The user can choose the order of History's columns by sliding a header, or with the left and right arrows when a header is focused; Undo starts at the end. | — | readme_gaps:71, changelog_gaps_1-300:27 |
| HIS-02.d | backlog | History is a table: Time \| Type \| Event \| Undo; folded it shows the latest lines with Undo and Redo where they apply, newest first (a stack). | — | theme.md section 15; picture 2·15 |
| HIS-02.e | backlog | Something done outside CalendarStream (deleted in Google, removed by United) has no Undo icon; Restore is on the event. | — | theme.md section 15 |
| HIS-02.f | backlog | An accepted sign-in is shown as a ✓ with no words; the word stays as its tooltip and accessible name. | — | theme.md Clarifications |
| HIS-02.g | backlog | History's three latest lines sit left-aligned in its section header, before its Healthy box. | — | theme.md Clarifications |
| HIS-03 | proposed | The user can undo and redo what History records. | — | — |
| HIS-03.a | proposed | Only the newest completed undoable change can be undone. | — | S49-10 |
| HIS-03.b | proposed | Undo restores the state before any undoable change and Redo reapplies it (HIS-03), in the order HIS-03 sets. This covers rule deletions; feed and event-template changes; an import (the event set before it); a calendar merge (the original calendar and its rule scope, with the merged events removed from the target); CCS+ removal (the source and its saved credentials); and Hide (the event's visible state, EVT-04). | — | S49-11, S49-12, S49-25, S49-30, S49-34, S57-15, changelog_gaps_601-900:32, changelog_gaps_601-900:32 |
| HIS-03.c | proposed | An undoable change records what is needed to restore it, before and after. | — | S77-32, S77-33 |
| HIS-03.d | proposed | A deleted event kept for Undo is permanently removed when its deletion leaves the retained history. | — | S49-16 |
| HIS-03.e | proposed | When removal of a CCS+ calendar leaves retained Undo history, its retained sign-in credentials are forgotten; protection while retained follows ACC-05. | — | changelog_gaps_601-900:33 |
| HIS-04 | proposed | History keeps a limited number of changes and does not show secrets unless the user may see them. | — | — |
| HIS-04.a | proposed | History keeps the number of changes set in Settings (DEF-01 has the default and the limits); saving a different number updates the effective retention and the displayed value, and a number outside the limits is not valid (UIC-19). | — | S58-19, S58-20 |
| HIS-04.b | proposed | History has a Show secrets switch for every log view on the page. By default secrets are masked: authorization headers, client secrets, tokens, authorization codes, and any secret value the app stores, wherever it appears in the text. Turning the switch on shows them, only to a user authorized to see secrets, and it turns off again whenever the page is opened (ACC-05.d). | — | Developer, Nov 18 |
| HIS-02.h | proposed | History's Type menu starts with msg:historyEveryType and then lists the eight types of HIS-02.a. | — | R6 gap |
| HIS-02.i | proposed | History's words box is labelled msg:historyWords; its Time menu offers msg:historyAnyTime, msg:historyLastHour, msg:historyLast24Hours, msg:historyLast7Days and msg:historyLast30Days. | — | R6 gap |
| HIS-02.j | proposed | Changing a History filter acts on the lines already loaded, without reloading the page. | — | R6 gap |
| HIS-02.k | proposed | A History filter request names the type, the words, the earliest time and the number of lines; words match without regard to letter case, and the characters %, _ and backslash match as themselves. | — | R6 gap |
| HIS-02.l | proposed | Each line has the type it was recorded with: calendar added, removed, emptied, imported, saved, switched On or Off and default-calendar lines are Calendar; destination lines are Feed; rule lines are Rule; event lines are Event; Google deletions and Google account lines are Google; Settings lines are Settings; update lines are Update; every other line is Sync. | — | R6 gap |
| HIS-03.f | proposed | Each line has an undo state: none, done or undone; a change made on the page is done. | — | R6 gap |
| HIS-03.g | proposed | Undo shows only on the newest done line, and Redo only on the oldest undone line that is newer than it. | — | R6 gap |
| HIS-03.h | proposed | Asking to undo or redo any other line is not allowed and shows msg:historyNewerFirst. | — | R6 gap |
| HIS-03.i | proposed | Asking to undo a line that has nothing left to restore shows msg:historyCantUndo. | — | R6 gap |
| HIS-03.j | proposed | After an undo the line is undone; after a redo it is done again. | — | R6 gap |
| HIS-03.k | proposed | An undo or redo writes msg:historyUndone or msg:historyRedone ({message} is the line's message) to the container log and makes no History line. | — | R6 gap |
| HIS-03.l | proposed | Recording a new undoable change discards the restore data and state of every undone line, so they cannot be redone. | — | R6 gap |
| HIS-03.m | proposed | A change's restore data holds, for each calendar: its name, color, tags, rule list, defaults, note, interval, download cache, status, counters and On or Off, and for CCS+ also its login and Calendar Sync link. | — | R6 gap |
| HIS-03.n | proposed | A change may name single events whose edit data and added-event data are held for it. | — | R6 gap |
| HIS-03.o | proposed | A restore is all or nothing: it succeeds completely in one step or changes nothing, and settings the saved data does not hold are deleted. | — | R6 gap |
| HIS-03.p | proposed | After a restore the checks start or stop for each calendar, the data of calendars that are gone is forgotten, every status is read again and the calendars are rebuilt. | — | R6 gap |
| HIS-03.q | proposed | A deleted event stays visible, struck through and greyed, labelled with where it was deleted: CalendarStream, Google, United or its feed. | — | R6 gap |
| HIS-03.r | proposed | Undoing the deletion of a calendar-source event removes its hidden mark and any edit record made only for the deletion, and writes the event to Google again. | — | R6 gap |
| HIS-04.c | proposed | Saving a History count records msg:historyKeepSaved ({n} the count), with type Settings, and trims at once. | — | R6 gap |
| HIS-04.d | proposed | Trimming keeps the restore data of the newest lines that have any, up to the count in Settings; older lines keep their text and lose their restore data and state. It also runs after every recorded change and finishes the deletions whose undo is gone (HIS-03.d). | — | R6 gap |
| HIS-04.e | proposed | History keeps the number of lines in DEF-01; recording a line removes the oldest beyond it. | — | R6 gap |
| HIS-05 | proposed | Every line History records has a level, a type, a time and a message, and is written so that no secret reaches it. | — | — |
| HIS-05.a | proposed | A line's level is info, warn or error; the Event cell shows each level in its own color of the theme. | — | R6 gap |
| HIS-05.b | proposed | A line is shown in the language of the page when it is read; one with no translation in that language is shown in English. | — | R6 gap |
| HIS-05.c | proposed | A line about a connection whose message does not name it starts with the connection's name and ": ". | — | R6 gap |
| HIS-05.d | proposed | Every line is also written to the container log at the matching level. | — | R6 gap |
| HIS-05.e | proposed | When a line cannot be saved the failure is logged as msg:historyWriteFailed ({reason} the cause) and the work carries on. | — | R6 gap |
| HIS-05.f | proposed | A line's time is the moment it was recorded, with its time zone. | — | R6 gap |
| HIS-05.g | proposed | A download that finds nothing new records msg:scheduleNoChanges ({how} is the source of the schedule) and sets the status msg:upToDateEventsIn ({n} events); a republished identical schedule does the same. | — | R6 gap |
| HIS-05.h | proposed | A refused hand-made upload records the error msg:uploadRejected ({error} the reason). | — | R6 gap |
| HIS-05.i | proposed | A line that mentions a link or a key holds only a safe part of it: a feed link its host (msg:feedLinkChangedTo), a Calendar Sync link its host and path (msg:calendarSyncLinkSetTo), a Google client the start of its ID (PGAP-01.t), a CCS+ login only msg:ccsUsernameAndCalendarSyncSaved; a password, secret or token is never written. | — | R6 gap |
| HIS-05.j | proposed | Page login lines name the user: msg:statusPageLoginCreatedFor and msg:statusPageLoginChangedUser. | — | R6 gap |
| HIS-05.k | proposed | Calendar lines are msg:calendarSourceAdded, msg:calendarSourceRemoved, msg:defaultCalendarName, msg:calendarEmptied ({name}, {note}), msg:importedFileInto, msg:calendarSettingsSaved, msg:calendarSwitchedOff, msg:calendarSwitchedOn, msg:checksEveryMinFromNow and msg:calendarSyncLinkResetTo. | — | R6 gap |
| HIS-05.l | proposed | Destination lines are msg:destinationAddedCalendarFeed, msg:destinationSwitchedOff, msg:destinationSwitchedOn, msg:streamNameChanged and msg:morePublicAddresses ({list} the addresses, or msg:remindersNone when there are none). | — | R6 gap |
| HIS-05.m | proposed | Event lines are msg:added, msg:updated, msg:edited, msg:deleted, msg:eventHidFromFeeds, msg:eventShownInFeeds, msg:eventReverted, msg:eventRestored and msg:remindersChanged; linked events add msg:eventDeletedWithLinked and msg:eventMovedWithLinked ({when} the new start). | — | R6 gap |
| HIS-05.n | proposed | Event template changes record msg:templatesSaved. | — | R6 gap |
| HIS-05.o | proposed | Update lines have type Update: msg:updateAvailableAuto, msg:updateAvailablePress or msg:updateAvailableCalendarstreamRunThe by how the update can be installed ({v} the version); msg:updatingTo and msg:autoUpdatingTo when an update starts; and, as warnings, msg:updateNotStarted and msg:autoUpdateNotStarted ({reason} the cause). | — | R6 gap |
| HIS-05.p | proposed | Sign-in protection records, as warnings, msg:statusPageLockedForAfter and msg:lockedManyAddresses ({n} the count and {minutes} the period in DEF-01), and with type Settings msg:unlockLinkUsedFrom. | — | R6 gap |
| HIS-05.q | proposed | Importing logins from the old secret files at start-up records msg:importedTheCcsUidAnd, msg:importedTheCcsUidAnd2 or msg:importedTheStatusPageLogin. | — | R6 gap |
| HIS-06 | proposed | The open History section shows the state of its sources and Google before its table. | — | — |
| HIS-06.a | proposed | The open section shows in this order: one status line per source, the Google line, the filter, the table (msg:nothingYet when it has no lines), the footer and the debug links of DIA-01. | — | R6 gap |
| HIS-06.b | proposed | A source's status line shows msg:notYet, msg:accepted or msg:rejected with its time for the sign-in of a connection that signs in; then msg:lastCheck, msg:scheduleChanged, msg:nextCheck and msg:eventsInFeed ({n}); and, when above 0, msg:rejectedSignInsInA ({n}) in red. The source's name is in bold when there is more than one. | — | R6 gap |
| HIS-06.c | proposed | A time in the status line is a clock time when it is today, otherwise the short date and a clock time, and msg:never when there is none. | — | R6 gap |
| HIS-06.d | proposed | The Google line is shown when a Google account is connected: an error in red when its last call failed, msg:syncing while a sync runs, otherwise the time of the last sync or msg:notYet. | — | R6 gap |
| HIS-06.e | proposed | Activity is unhealthy when a source's status is Sign-in rejected, Blocked, Error, Internal error or Paused, or when Google is connected and its last call failed; Healthy, Running, Starting and Setup do not make it unhealthy. | — | R6 gap |
| HIS-06.f | proposed | The table lists the newest lines, the number in DEF-01, newest first. | — | R6 gap |
| HIS-06.g | proposed | A saved column order that holds each of the four columns once is used; any other is replaced by the default order, and a bad order is not saved and shows msg:historyColumnOrderUnknown. | — | R6 gap |
| HIS-06.h | proposed | The Undo column's header is text for screen readers only. | — | R6 gap |
| HIS-06.i | proposed | A line whose change was undone ends with msg:historyUndoneMark and is greyed. | — | R6 gap |
