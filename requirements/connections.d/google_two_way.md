# Requirements: Google two-way sync

A Google connection that also reads changes made in Google. It does everything Google one-way sync does (connections.d/google_one_way.md) and adds only what is here.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CGTW-01 | proposed | A change made in Google reaches CalendarStream as well, and the newer change wins. | — | — |
| CGTW-01.f | proposed | Google two-way sync is both a source and a feed: it publishes events to Google and reads changes made there. | — | — |
| CGTW-01.a | proposed | After a full check, edits to remote imported or custom events update the local edited title, location and start time without changing the original imported source record. | — | S45-05, S45-06, S45-07, S45-09, S53-06 |
| CGTW-01.b | proposed | A handmade remote event is imported once as a local custom event, placed in a Local calendar that the destination includes; its remote identity is replaced by the mapped CalendarStream identity. | — | S45-10, S45-11, changelog_gaps_901-1200:L19 |
| CGTW-01.c | proposed | In two-way synchronization, remote deletion hides or marks the corresponding local event deleted; restoring one clears its marker and restores that remote event without restoring other deleted events. Event restoration is owned by EVT-01. | — | S45-12, S45-19, S45-22, S45-23, S49-40 |
| CGTW-01.d | proposed | Rule-generated events remain governed by the rule: remote title edits and deletions are corrected on synchronization. | — | S45-13, S45-14, S45-15 |
| CGTW-02 | proposed | Reading Google's changes brings back what a person changed in Google. | — | R5 gap |
| CGTW-02.a | proposed | Nothing is read when the connection has no calendar, its calendar differs from the last synchronized one, Google reports it gone or refuses it because another client made it; any other failure fails the synchronization. | — | R5 gap |
| CGTW-02.b | proposed | The fields read are the title, all-day, start, end, location, notes and the updated time, cut to the lengths in DEF-01 (Event fields read from Google); the notes lose the CalendarStream mark and a leading meeting-link line (CGOW-03.h). | — | R5 gap |
| CGTW-02.c | proposed | Events deleted in Google are recorded in History as msg:googleDeletedInGoogleList ({names} up to the number in DEF-01 (Removed events listed in one History entry), then " ..."), each with Restore (EVT-04). | — | R5 gap |
| CGTW-02.d | proposed | An event deleted in Google while its Restore is pending is not treated as a deletion. | — | R5 gap |
| CGTW-02.e | proposed | An event added in Google that does not repeat is copied to the first local calendar the connection includes, with a generated identifier (cs-, sixteen hexadecimal digits, @calendar_stream) and no color, deleted from Google and written back by the next synchronization. | — | R5 gap |
| CGTW-02.f | proposed | An added event that repeats, or one added to a connection with no local calendar, is left in Google and said once; the last number in DEF-01 (Events added in Google remembered as left alone) are remembered. | — | R5 gap |
| CGTW-02.g | proposed | Applying Google's changes records History msg:googleNameText ({name} the connection, {text} each change), rebuilds the rules and sources the changes touched and saves the state. | — | R5 gap |
