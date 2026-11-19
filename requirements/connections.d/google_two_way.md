# Requirements: Google two-way sync

A Google connection that also reads changes made in Google. It does everything Google one-way sync does (connections.d/google_one_way.md) and adds only what is here.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| GTW-01 | proposed | A change made in Google reaches CalendarStream as well, and the newer change wins. | — | — |
| GTW-01.f | proposed | Google two-way sync is both a source and a feed: it publishes events to Google and reads changes made there. | — | — |
| GTW-01.a | proposed | After a full check, edits to remote imported or custom events update the local edited title, location and start time without changing the original imported source record. | — | S45-05, S45-06, S45-07, S45-09, S53-06 |
| GTW-01.b | proposed | A handmade remote event is imported once as a local custom event, placed in a Local calendar that the destination includes; its remote identity is replaced by the mapped CalendarStream identity. | — | S45-10, S45-11, changelog_gaps_901-1200:L19 |
| GTW-01.c | proposed | In two-way synchronization, remote deletion hides or marks the corresponding local event deleted; restoring one clears its marker and restores that remote event without restoring other deleted events. Event restoration is owned by EVT-01. | — | S45-12, S45-19, S45-22, S45-23, S49-40 |
| GTW-01.d | proposed | Rule-generated events remain governed by the rule: remote title edits and deletions are corrected on synchronization. | — | S45-13, S45-14, S45-15 |
| GTW-01.e | proposed | When local and remote edits conflict, the newer change wins. | — | S45-16, S45-18, S53-05 |
