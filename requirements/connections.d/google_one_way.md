# Requirements: Google one-way sync

A Google connection: a Google calendar destination with its own account that CalendarStream publishes to. Common connection rules are in connections.md; the Google plugin is plugins.d/google_api.md.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CGOW-01 | proposed | Each Google connection signs in with its own Google account, and the user can invite someone else to sign in. | — | — |
| CGOW-01.a | proposed | Google consent requests use the public callback address and request explicit consent. | — | S12-15 |
| CGOW-01.b | proposed | Successful consent connects the selected account, identifies its email and clears an earlier sign-in error. | — | S12-17, S12-21, S20-01, S45-01, S48-07, S48-08, S48-23, S49-36, S51-22, S54-04 |
| CGOW-01.c | proposed | A consent state is single-use, belongs to its account and expires after the time in DEF-01; an expired, unknown, reused or other-account state is not accepted. | — | S12-24, S70-11, S70-13, S70-14, S70-15, S70-16, S70-18, changelog_gaps_1-300:L23 |
| CGOW-01.d | proposed | Refused calendar permission leaves the account disconnected and explains how to grant permission; cancelled sign-in reports cancellation. Successful later consent clears the error. | — | S12-33, S12-34, S12-35, S12-36, S24-07 |
| CGOW-01.e | proposed | Different Google accounts receive separate account identities and calendar mappings. | — | S12-37, S49-43, S49-44 |
| CGOW-01.f | proposed | Revoked sign-in requires connecting again. A credential that cannot be decrypted after changing the database password reports that configuration cause. | — | S12-39, S12-41, S55-23 |
| CGOW-01.g | proposed | A new Google connection starts with its own unconnected account; it does not silently use another connection’s account or create a remote calendar before its own sign-in. | — | S51-24, S51-25, S51-26, S70-07, S70-08 |
| CGOW-01.h | proposed | A connection can invite another person to connect it: the invite identifies the connection, and successful consent connects that invited account without changing another account’s assignment. | — | S51-27, S51-28, S51-31, S51-34, S51-35, S51-36, S51-38 |
| CGOW-01.i | proposed | An invitation is single-use, can be withdrawn and expires after the time in DEF-01; a consumed, withdrawn, expired or invented link is not accepted. | — | S51-37, S51-39, S51-40, S51-41, changelog_gaps_601-900:L26, readme_gaps:L65 |
| CGOW-01.j | proposed | Inviting a replacement account does not change the current connection assignment while consent is pending; withdrawing it keeps the original assignment. | — | S51-42, S51-43 |
| CGOW-01.k | proposed | Connect me can sign a new connection into the user’s account. Removing a same-account connection does not revoke access still used by another connection; removing a separately invited account revokes its credentials. | — | S51-44, S51-45, S51-46, S51-47 |
| CGOW-01.l | proposed | A connection not yet synchronized does not claim Last synced; a failed sign-in offers a way to reconnect. | — | S54-01, S54-09 |
| CGOW-01.m | proposed | Google sign-in requests offline access with an S256 challenge; pending sign-in requests are bounded (DEF-01) and persist across API instances using the same storage. | — | S70-09, S70-10 |
| CGOW-01.n | proposed | Google sign-in accepts an account email only from a verified Google identity issued for this app's client. | — | S70-19 |
| CGOW-01.o | proposed | Pending invitation consent remains usable across an app restart until it is consumed or expires. | — | changelog_gaps_1-300:L23 |
| CGOW-01.p | proposed | Google authorization requests the app-created-calendar scope and email identity, limiting calendar access to calendars created by this app. | — | changelog_gaps_2101-2336:L21, readme_gaps:L80 |
| CGOW-01.q | proposed | After connection consent completes, the user returns to the destination involved in that consent. | — | changelog_gaps_601-900:L16 |
| CGOW-01.r | proposed | When the API client is removed (PGAP-01.d), the Google accounts are disconnected with their remote calendars kept, and the page reports that each Google connection needs its account restored after the client is set up again. | — | S12-09, S46-06, S48-17, S48-18, S54-14 |
| CGOW-01.s | proposed | Repeating a Google setup submission does not create duplicate or orphan connections. | — | changelog_gaps_1-300:L26 |
| CGOW-02 | proposed | Connecting a connection creates or reuses its Google calendar, which holds only what the connection publishes. | — | — |
| CGOW-02.a | proposed | Connection creates a calendar named for the destination, using the calendar’s configured time zone. | — | S12-18, S12-19, S26-43, S26-45 |
| CGOW-02.b | proposed | Reconnecting the same account reuses its retained calendar rather than creating a duplicate, preserving its synchronized event set. | — | S12-27, S12-29, S12-30, S48-14, S48-15, S48-16, S54-08 |
| CGOW-02.c | proposed | Disconnecting without deleting revokes access and clears connection while keeping the remote calendar and its remembered mapping. | — | S12-28, S48-11, S54-07 |
| CGOW-02.d | proposed | Disconnecting with deletion removes the remote calendar, forgets its mapping and clears synchronization tracking. | — | S12-31, S13-37 |
| CGOW-02.e | proposed | Removing a Google destination can keep its remote calendar while clearing its local mapping, or delete that remote calendar. | — | S26-53, S26-54, S49-46 |
| CGOW-02.f | proposed | Connecting a different client creates a new mapping without repeatedly recreating it, leaving the unreachable former calendar for manual cleanup. | — | S48-19, S48-20, S48-21, S48-24 |
| CGOW-02.g | proposed | After first calendar creation, opening it waits for synchronization and then opens Google Calendar for the correct account. The setup action is no longer offered once shown; ordinary feeds do not support this action. | — | S55-01, S55-02, S55-03, S55-04, S55-05, S55-06, S55-07, S55-08, S55-38, S55-40 |
| CGOW-02.h | proposed | Concurrent consent completion and synchronization reuse the same remote calendar mapping rather than creating duplicates. | — | changelog_gaps_1501-1800:L35 |
| CGOW-02.i | proposed | Renaming a destination updates the existing Google calendar’s name. | — | S13-20, S26-48 |
| CGOW-02.j | proposed | The initial default Google publication window starts on the first day of the current month. | — | changelog_gaps_2101-2336:L17 |
| CGOW-02.l | proposed | Each Google destination publishes only its selected sources; a combined destination may include multiple sources. | — | S26-46 |
| CGOW-02.m | proposed | Connecting requests a full synchronization; initial synchronization publishes eligible nonhidden events in the configured window. | — | S13-02, S13-03, S20-03, S26-44, S45-02, S45-03, S48-09, S48-10 |
| CGOW-03 | proposed | The events published to Google keep their time, title, reminders and color as the app shows them. | — | — |
| CGOW-03.a | backlog | Google sync follows the common time rules (TIM-01 to TIM-07): it reads the time zone of the Google calendar and of each incoming event and records it with the event, and it sends each event's recorded time zone. A stored all-day event is sent to Google as an all-day event for its stored time zone, so it shows on the right days in Google Calendar. | — | Developer |
| CGOW-03.b | proposed | The busy or free state of an event is kept when it is published. | — | S13-08, S13-09, S13-10, S13-18 |
| CGOW-03.c | proposed | Google events retain source titles and indicate that CalendarStream synchronized them. | — | S13-06 |
| CGOW-03.d | proposed | A Google event carries the reminders of CON-09.b with Google's default reminders disabled. | — | S13-07, S36-27 |
| CGOW-03.e | proposed | An event without a color rule does not force a Google event color. Color rules apply the corresponding Google color (UIC-20). | — | S13-11, S13-19, S13-22, S26-47, S74-05 |
| CGOW-03.f | proposed | The Google calendar follows its connection’s selected calendar color when the upstream service accepts it. | — | S49-39, S56-02 |
| CGOW-03.g | proposed | If a calendar color cannot be applied, the connection explains that the color does not carry to Google; repeating the same color does not retry it, and selecting a different accepted color applies it and clears the note. A color request that could not reach Google is not remembered as refused. | — | S55-09, S55-15, S55-20, S55-21, S56-22, S56-23, S56-24, S56-26, S56-27, S56-29 |
| CGOW-03.h | proposed | A meeting link appears before the notes in the Google description (CON-09.c), and is not copied back into the notes when the event is read from Google. | — | S63-03, S63-04 |
| CGOW-04 | proposed | Events published to Google are kept in step with CalendarStream: a change made here reaches Google. | — | — |
| CGOW-04.k | proposed | Google one-way sync is a feed: it publishes events to Google and does not read them back. | — | — |
| CGOW-04.a | proposed | An unchanged normal or full synchronization performs no event writes; editing an event schedules synchronization and updates the remote event. | — | S13-12, S13-13, S13-14, S13-15, S13-16, S13-30 |
| CGOW-04.b | proposed | A normal synchronization does not inspect Google’s event copy; full checks reconcile Google changes. | — | S13-23, S13-24, S45-04 |
| CGOW-04.c | proposed | A full check removes obsolete CalendarStream-owned remote events while keeping handmade remote events eligible for import. | — | S13-25 |
| CGOW-04.d | proposed (?) | Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? | — | S13-27, S13-28, S13-29 |
| CGOW-04.e | proposed (?) | If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? | — | S13-31 |
| CGOW-04.f | proposed | Sync Now requests a full check. | — | S13-34, S35-17 |
| CGOW-04.g | proposed | One-way sync restores a remote-deleted local event rather than hiding it locally; two-way sync is CGTW-01. | — | S49-37, S49-38, S49-42, S49-45 |
| CGOW-04.h | proposed | When a write budget prevents completing remote cleanup in one sync, remaining work continues at the next full sync. | — | S53-07, S53-08 |
| CGOW-04.i | proposed | Synchronization resumes after the database becomes available following a restart. | — | changelog_gaps_1501-1800:L35 |
| CGOW-04.j | proposed (?) | Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? | — | changelog_gaps_1801-2100:L19, changelog_gaps_2101-2336:L16, changelog_gaps_901-1200:L18, readme_gaps:L27 |
| CGOW-05 | proposed | Google tells the app about changes at once, so they do not wait for the next scheduled check. | — | — |
| CGOW-05.a | proposed | Instant updates start with synchronization. Registering them uses the HTTPS public notification address and the selected calendar; they need HTTPS and have the lifetime in DEF-01. | — | S20-02, S20-04, S20-07 |
| CGOW-05.b | proposed | Notifications with a wrong token or unknown channel are acknowledged and ignored; a channel sync message does not trigger a check. | — | S20-08, S20-09, S20-10, S23-24 |
| CGOW-05.c | proposed | A valid change notification requests a full check without a page login; processing it records the last notice time and retains Google edits locally. | — | S20-11, S20-12, S20-13 |
| CGOW-05.d | proposed | A change-notification watch is renewed the time in DEF-01 before it expires and the old one stopped; a fresh watch is reused, and a changed public address replaces the target rather than accumulating watches. | — | S20-14, S20-15, S20-16, changelog_gaps_1801-2100:L20 |
| CGOW-05.e | proposed | Refused instant updates report the reason without preventing ordinary autosync; a later successful retry clears the error. After a refusal the retry waits the time in DEF-01. | — | S20-17, S20-18, S20-19, S20-20 |
| CGOW-05.f | proposed | Disconnecting stops the instant-update channel, and a notice that arrives late is still acknowledged. | — | S20-21, S20-22, S20-23 |
| CGOW-06 | proposed | Each account's health is shown clearly, and a failure never turns into a false success. | — | — |
| CGOW-06.a | proposed | Revoked access is shown as an error rather than successful sync. | — | S13-35, S13-36 |
| CGOW-06.b | proposed | Disconnected connections remain Not connected and are skipped without turning the whole sync into an error. | — | S48-12, S48-13, S68-01, S68-02 |
| CGOW-06.c | proposed | A color-update failure does not stop event synchronization or falsely report that sign-in was lost. | — | S54-05, S54-06, S55-11, S55-13, S55-18, S56-19, S56-21, S56-28 |
| CGOW-06.d | proposed | A transient server failure degrades only the affected account and defers its next sync; a skipped degraded account does not fail the whole job. An explicit health reset permits syncing again. | — | S68-09, S68-10, S68-11, S73-03, S73-04, S73-09, S73-11 |
| CGOW-06.e | proposed | Readiness distinguishes missing client, signed-out account, API error, not-yet-synced account and successful sync; a nonempty error overrides prior success, while an empty error does not. | — | S71-01, S71-02, S71-03, S71-04, S71-05, S71-06, S71-07 |
| CGOW-06.f | proposed | Successful recovery, or a new successful sign-in, restores the healthy state and clears the retry count, keeping the account's calendar mappings and settings. New accounts start healthy and eligible to sync. | — | S73-01, S73-07, changelog_gaps_1-300:L21 |
| CGOW-06.g | proposed | A saved health error is shown in full; a line that is too long for its space follows the clipping rule (UIC-14, UIC-07). | — | S73-13 |
| CGOW-06.h | proposed | Each account’s recorded health and retry deadline persist across an app restart. | — | changelog_gaps_1-300:L21 |

