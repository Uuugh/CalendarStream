# Requirements: google

Google sign-in and 2-way sync, health and recovery. Issues against this feature
(kept in the issues database): I5, I41, I42, I47, I50.
Terms: the **API client** is the Google client the user creates once in Google Cloud; a **Google module** is a Google calendar destination with its own account; **one-way** sync sends changes to Google only, **two-way** also reads changes made in Google.


| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| GGL-01 | proposed | The user sets up access to Google once, with their own Google client, and is guided through it. | — | — |
| GGL-01.a | proposed | A Google destination can be added only once the API client is set up and accepted; before that, connecting is unavailable and setup guidance is offered. | — | S12-01, S12-02, S39-01, S39-02, S51-01, S51-03, S39-16 |
| GGL-01.b | proposed | Client setup requires a well-formed client ID and an initial secret. Invalid or missing values are identified. | — | S12-03, S12-04, S48-01, S48-02 |
| GGL-01.c | proposed | Changing the Google client ID with the secret left blank keeps the previous secret; secrets are protected as in ACC-05. | — | S12-10, S14-18 |
| GGL-01.d | proposed | Removing the API client clears the configured and connected state and returns setup to Not set up. The Google accounts are disconnected with their remote calendars kept, and the page reports that destinations need their account connections restored after the client is set up again. | — | S12-09, S46-06, S48-17, S48-18, S54-14, changelog_gaps_601-900:L17, changelog_gaps_901-1200:L17 |
| GGL-01.e | proposed | The Google client cannot be changed while an account is connected, because the sign-in belongs to that client; the user disconnects first (removing the client disconnects its accounts, GGL-01). | — | S12-22 |
| GGL-01.f | proposed | Saved refresh credentials, the client secret and pending sign-in verifiers are protected as ACC-05 says. | — | S12-20, changelog_gaps_1-300:L23 |
| GGL-01.g | proposed | Client checking distinguishes accepted credentials, rejected secrets, unknown client IDs and an unreachable service; unreachable is not reported as invalid credentials. | — | S14-13, S14-15, S14-16, S14-17, S19-20, S19-22, S48-03, S48-04, S54-13 |
| GGL-01.h | proposed | Without an explicit public address, setup derives the callback from the request host; unsupported public IP/local-host addresses do not advertise an unusable callback and instead request public-address setup. Public-address rules: SET-04..SET-04. | — | S23-04, S23-17, S23-18 |
| GGL-01.i | proposed | A missing authorized redirect is reported separately from client acceptance and supplies the exact callback to authorize. Changing the public address invalidates stale address feedback. | — | S23-07, S23-08, S23-10, S23-11, S23-12, S23-22, S48-05, S48-06, S67-26 |
| GGL-01.j | proposed | Setup provides the callback address and ordered guidance through the Google project, API, consent screen and client, and for redirect mismatch, denied access and invalid client errors. It tells the user to publish the OAuth app or add the signing-in account as a test user, covers a deleted client and repeated reconnection from an app left in testing, and uses the saved support email or asks for the user's Gmail support email. | — | S24-02, S24-03, S24-05, S25-02, S25-05, changelog_gaps_1501-1800:L28, changelog_gaps_1501-1800:L29 |
| GGL-01.k | proposed | Guided Google setup confirms that the callback is authorized before continuing to consent. | — | changelog_gaps_601-900:L44 |
| GGL-01.l | proposed | Google setup provides a copyable assisted-setup request and a guided route through the required provider configuration. | — | changelog_gaps_901-1200:L21, readme_gaps:L85 |
| GGL-01.m | proposed | API setup completion, and its History message, identify each Google module that needs sign-in, has a sync error or has not completed its first sync. | — | changelog_gaps_1-300:L22 |
| GGL-01.n | proposed | Repeating a Google setup submission does not create duplicate or orphan destinations. | — | changelog_gaps_1-300:L26 |
| GGL-02 | proposed | Each Google module signs in with its own Google account, and the user can invite someone else to sign in. | — | — |
| GGL-02.a | proposed | Google consent requests use the public callback address and request explicit consent. | — | S12-15 |
| GGL-02.b | proposed | Successful consent connects the selected account, identifies its email and clears an earlier sign-in error. | — | S12-17, S12-21, S20-01, S45-01, S48-07, S48-08, S48-23, S49-36, S51-22, S54-04 |
| GGL-02.c | proposed | A consent state is single-use, belongs to its account and expires after the time in DEF-01; an expired, unknown, reused or other-account state is not accepted. | — | S12-24, S70-11, S70-13, S70-14, S70-15, S70-16, S70-18, changelog_gaps_1-300:L23 |
| GGL-02.d | proposed | Refused calendar permission leaves the account disconnected and explains how to grant permission; cancelled sign-in reports cancellation. Successful later consent clears the error. | — | S12-33, S12-34, S12-35, S12-36, S24-07 |
| GGL-02.e | proposed | Different Google accounts receive separate account identities and calendar mappings. | — | S12-37, S49-43, S49-44 |
| GGL-02.f | proposed | Revoked sign-in requires connecting again. A credential that cannot be decrypted after changing the database password reports that configuration cause. | — | S12-39, S12-41, S55-23 |
| GGL-02.g | proposed | A new Google module starts with its own unconnected account; it does not silently use another module’s account or create a remote calendar before its own sign-in. | — | S51-24, S51-25, S51-26, S70-07, S70-08 |
| GGL-02.h | proposed | A module can invite another person to connect it: the invite identifies the module, and successful consent connects that invited account without changing another account’s assignment. | — | S51-27, S51-28, S51-31, S51-34, S51-35, S51-36, S51-38 |
| GGL-02.i | proposed | An invitation is single-use, can be withdrawn and expires after the time in DEF-01; a consumed, withdrawn, expired or invented link is not accepted. | — | S51-37, S51-39, S51-40, S51-41, changelog_gaps_601-900:L26, readme_gaps:L65 |
| GGL-02.j | proposed | Inviting a replacement account does not change the current module assignment while consent is pending; withdrawing it keeps the original assignment. | — | S51-42, S51-43 |
| GGL-02.k | proposed | Connect me can sign a new module into the user’s account. Removing a same-account module does not revoke access still used by another module; removing a separately invited account revokes its credentials. | — | S51-44, S51-45, S51-46, S51-47 |
| GGL-02.l | proposed | A module not yet synchronized does not claim Last synced; a failed sign-in offers a way to reconnect. | — | S54-01, S54-09 |
| GGL-02.m | proposed | Google sign-in requests offline access with an S256 challenge; pending sign-in requests are bounded (DEF-01) and persist across API instances using the same storage. | — | S70-09, S70-10 |
| GGL-02.n | proposed | Google sign-in accepts an account email only from a verified Google identity issued for this app's client. | — | S70-19 |
| GGL-02.o | proposed | Pending invitation consent remains usable across an app restart until it is consumed or expires. | — | changelog_gaps_1-300:L23 |
| GGL-02.p | proposed | Google authorization requests the app-created-calendar scope and email identity, limiting calendar access to calendars created by this app. | — | changelog_gaps_2101-2336:L21, readme_gaps:L80 |
| GGL-02.q | proposed | After module consent completes, the user returns to the destination involved in that consent. | — | changelog_gaps_601-900:L16 |
| GGL-03 | proposed | Connecting a module creates or reuses its Google calendar, which holds only what the module publishes. | — | — |
| GGL-03.a | proposed | Connection creates a calendar named for the destination, using the calendar’s configured time zone. | — | S12-18, S12-19, S26-43, S26-45 |
| GGL-03.b | proposed | Reconnecting the same account reuses its retained calendar rather than creating a duplicate, preserving its synchronized event set. | — | S12-27, S12-29, S12-30, S48-14, S48-15, S48-16, S54-08 |
| GGL-03.c | proposed | Disconnecting without deleting revokes access and clears connection while keeping the remote calendar and its remembered mapping. | — | S12-28, S48-11, S54-07 |
| GGL-03.d | proposed | Disconnecting with deletion removes the remote calendar, forgets its mapping and clears synchronization tracking. | — | S12-31, S13-37 |
| GGL-03.e | proposed | Removing a Google destination can keep its remote calendar while clearing its local mapping, or delete that remote calendar. | — | S26-53, S26-54, S49-46 |
| GGL-03.f | proposed | Connecting a different client creates a new mapping without repeatedly recreating it, leaving the unreachable former calendar for manual cleanup. History owns the cleanup warning under HIS-01. | — | S48-19, S48-20, S48-21, S48-24 |
| GGL-03.g | proposed | After first calendar creation, opening it waits for synchronization and then opens Google Calendar for the correct account. The setup action is no longer offered once shown; ordinary feeds do not support this action. | — | S55-01, S55-02, S55-03, S55-04, S55-05, S55-06, S55-07, S55-08, S55-38, S55-40 |
| GGL-03.h | proposed | Concurrent consent completion and synchronization reuse the same remote calendar mapping rather than creating duplicates. | — | changelog_gaps_1501-1800:L35 |
| GGL-03.i | proposed | Renaming a destination updates the existing Google calendar’s name. | — | S13-20, S26-48 |
| GGL-03.j | proposed | The initial default Google publication window starts on the first day of the current month. | — | changelog_gaps_2101-2336:L17 |
| GGL-03.k | proposed | A Google destination can be limited by a date range (UI-23). | — | changelog_gaps_1501-1800:L17, readme_gaps:L81 |
| GGL-03.l | proposed | Each Google destination publishes only its selected sources; a combined destination may include multiple sources. | — | S26-46 |
| GGL-03.m | proposed | Connecting requests a full synchronization; initial synchronization publishes eligible nonhidden events in the configured window. | — | S13-02, S13-03, S20-03, S26-44, S45-02, S45-03, S48-09, S48-10 |
| GGL-04 | proposed | The events published to Google keep their time, title, reminders and color as the app shows them. | — | — |
| GGL-04.a |  | Google sync follows the common time rules (TIM-01 to TIM-07): it reads the time zone of the Google calendar and of each incoming event and records it with the event, and it sends each event's recorded time zone. A stored all-day event is sent to Google as an all-day event for its stored time zone, so it shows on the right days in Google Calendar. (Developer, Nov 17) | — | Developer |
| GGL-04.b | proposed | The busy or free state of an event is kept when it is published. | — | S13-08, S13-09, S13-10, S13-18 |
| GGL-04.c | proposed | Google events retain source titles and indicate that CalendarStream synchronized them. | — | S13-06 |
| GGL-04.d | proposed | Published reminders disable Google defaults and use the event’s explicitly selected reminders, including fifteen-minute and one-hour choices. Reminder selection is owned by EVT-03. | — | S13-07, S36-27 |
| GGL-04.e | proposed | An event without a color rule does not force a Google event color. Color rules apply the corresponding Google color (UI-20). | — | S13-11, S13-19, S13-22, S26-47, S74-05 |
| GGL-04.f | proposed | The Google calendar follows its module’s selected calendar color when the upstream service accepts it. | — | S49-39, S56-02 |
| GGL-04.g | proposed | If a calendar color cannot be applied, the module explains that the color does not carry to Google; repeating the same color does not retry it, and selecting a different accepted color applies it and clears the note. A color request that could not reach Google is not remembered as refused. | — | S55-09, S55-15, S55-20, S55-21, S56-22, S56-23, S56-24, S56-26, S56-27, S56-29 |
| GGL-04.h | proposed | A meeting link appears before the notes in the Google description, and is not copied back into the notes when the event is read from Google. | — | S63-03, S63-04 |
| GGL-04.i | proposed | Hiding a local event removes its published Google copy. | — | S13-17 |
| GGL-05 | proposed | Google and CalendarStream are kept in step, and a change on either side reaches the other. | — | — |
| GGL-05.a | proposed | An unchanged normal or full synchronization performs no event writes; editing an event schedules synchronization and updates the remote event. | — | S13-12, S13-13, S13-14, S13-15, S13-16, S13-30 |
| GGL-05.b | proposed | A normal synchronization does not inspect Google’s event copy; full checks reconcile Google changes. | — | S13-23, S13-24, S45-04 |
| GGL-05.c | proposed | A full check removes obsolete CalendarStream-owned remote events while keeping handmade remote events eligible for import. | — | S13-25 |
| GGL-05.d | proposed (?) | Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? | — | S13-27, S13-28, S13-29 |
| GGL-05.e | proposed (?) | If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? | — | S13-31 |
| GGL-05.f | proposed | Sync Now requests a full check. | — | S13-34, S35-17 |
| GGL-05.g | proposed | After a full check, edits to remote imported or custom events update the local edited title, location and start time without changing the original imported source record. | — | S45-05, S45-06, S45-07, S45-09, S53-06 |
| GGL-05.h | proposed | A handmade remote event is imported once as a local custom event, placed in a Local calendar that the destination includes; its remote identity is replaced by the mapped CalendarStream identity. | — | S45-10, S45-11, changelog_gaps_901-1200:L19 |
| GGL-05.i | proposed | In two-way synchronization, remote deletion hides or marks the corresponding local event deleted; restoring one clears its marker and restores that remote event without restoring other deleted events. Event restoration is owned by EVT-01. | — | S45-12, S45-19, S45-22, S45-23, S49-40 |
| GGL-05.j | proposed | Rule-generated events remain governed by the rule: remote title edits and deletions are corrected on synchronization. | — | S45-13, S45-14, S45-15 |
| GGL-05.k | proposed | When local and remote edits conflict, the newer change wins. History records the winning outcome under HIS-01. | — | S45-16, S45-18, S53-05 |
| GGL-05.l | proposed | Google modules distinguish one-way and two-way synchronization; one-way sync restores a remote-deleted local event rather than hiding it locally. | — | S49-37, S49-38, S49-42, S49-45 |
| GGL-05.m | proposed | When a write budget prevents completing remote cleanup in one sync, remaining work continues at the next full sync. History reports the deferred work. | — | S53-07, S53-08 |
| GGL-05.n | proposed | Synchronization resumes after the database becomes available following a restart. | — | changelog_gaps_1501-1800:L35 |
| GGL-05.o | proposed (?) | Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? | — | changelog_gaps_1801-2100:L19, changelog_gaps_2101-2336:L16, changelog_gaps_901-1200:L18, readme_gaps:L27 |
| GGL-06 | proposed | Google tells the app about changes at once, so they do not wait for the next scheduled check. | — | — |
| GGL-06.a | proposed | Instant updates start with synchronization. Registering them uses the HTTPS public notification address and the selected calendar; they need HTTPS and have the lifetime in DEF-01. | — | S20-02, S20-04, S20-07 |
| GGL-06.b | proposed | Notifications with a wrong token or unknown channel are acknowledged and ignored; a channel sync message does not trigger a check. | — | S20-08, S20-09, S20-10, S23-24 |
| GGL-06.c | proposed | A valid change notification requests a full check without a page login; processing it records the last notice time and retains Google edits locally. | — | S20-11, S20-12, S20-13 |
| GGL-06.d | proposed | A change-notification watch is renewed the time in DEF-01 before it expires and the old one stopped; a fresh watch is reused, and a changed public address replaces the target rather than accumulating watches. | — | S20-14, S20-15, S20-16, changelog_gaps_1801-2100:L20 |
| GGL-06.e | proposed | Refused instant updates report the reason without preventing ordinary autosync; a refusal that repeats unchanged is recorded once (HIS-01), and a later successful retry clears the error. After a refusal the retry waits the time in DEF-01. | — | S20-17, S20-18, S20-19, S20-20 |
| GGL-06.f | proposed | Disconnecting stops the instant-update channel, and a notice that arrives late is still acknowledged. | — | S20-21, S20-22, S20-23 |
| GGL-07 | proposed | Failures are retried, and each account's health is shown clearly. | — | — |
| GGL-07.a | proposed | Revoked access is shown as an error rather than successful sync; a failure that repeats unchanged is recorded once (HIS-01). | — | S13-35, S13-36 |
| GGL-07.b | proposed | Disconnected modules remain Not connected and are skipped without turning the whole sync into an error. | — | S48-12, S48-13, S68-01, S68-02 |
| GGL-07.c | proposed | A color-update failure does not stop event synchronization or falsely report that sign-in was lost. A failure that repeats unchanged is recorded once (HIS-01); History owns diagnostic wording under HIS-01. | — | S54-05, S54-06, S55-11, S55-13, S55-18, S56-19, S56-21, S56-28 |
| GGL-07.d | proposed | A transient server failure degrades only the affected account and defers its next sync; a skipped degraded account does not fail the whole job. An explicit health reset permits syncing again. | — | S68-09, S68-10, S68-11, S73-03, S73-04, S73-09, S73-11 |
| GGL-07.e | proposed | Readiness distinguishes missing client, signed-out account, API error, not-yet-synced account and successful sync; a nonempty error overrides prior success, while an empty error does not. | — | S71-01, S71-02, S71-03, S71-04, S71-05, S71-06, S71-07 |
| GGL-07.f | proposed | An expired access credential is refreshed and the call retried once; if that does not recover it, the next try is at the next scheduled synchronization and the page reports that timing. Revoked consent or a permission refusal requires reauthorization without an automatic retry. | — | S72-08, S72-09, S72-10, S72-11, S73-08, S12-25, changelog_gaps_1-300:L19 |
| GGL-07.g | proposed | Transient failures, including rate limits, are retried with a wait that starts at the first wait in DEF-01, doubles each attempt up to the longest wait, is randomized upward by the jitter in DEF-01, and stops after the number of attempts in DEF-01; a longer wait asked for by the server (Retry-After) is honored. | — | S72-12, S72-13, S72-14, S72-15, S72-16, S73-02, S73-05, S73-06, S12-26 |
| GGL-07.h | proposed | A missing calendar pauses recovery rather than retrying at once; an invalid event or a conflict does not make the account unhealthy. An unknown or unexpected failure is reported as unknown (degraded), never as success, and gets one automatic retry. | — | S72-17, S72-18, S72-19, S73-10, S68-12, S68-13 |
| GGL-07.i | proposed | Successful recovery, or a new successful sign-in, restores the healthy state and clears the retry count, keeping the account's calendar mappings and settings. New accounts start healthy and eligible to sync. | — | S73-01, S73-07, changelog_gaps_1-300:L21 |
| GGL-07.j | proposed | A saved health error is shown in full; a line that is too long for its space follows the clipping rule (UI-14, UI-07). | — | S73-13 |
| GGL-07.k | proposed | Each account’s recorded health and retry deadline persist across an app restart. | — | changelog_gaps_1-300:L21 |
| GGL-07.l | proposed | Upstream Google refusals preserve Google’s explanation in diagnostic feedback. | — | changelog_gaps_601-900:L15, readme_gaps:L66 |

## Notes from the draft

### Not requirements

Implementation-only observations, sentinels and shared-owner evidence are accounted for individually.
A reference identifies ownership; it does not assert that every shared mechanic is already approved.

- S12-05: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-11: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S12-12: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-13: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-14: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-16: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S12-23: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S12-32: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S12-38: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S12-40: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S13-04: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S13-05: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-21: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-26: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-32: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-33: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S14-14: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S18-10: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S19-21: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S20-06: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S23-09: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S24-04: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S24-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S25-01: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S25-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S26-49: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S35-12: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S35-16: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S39-13: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S39-17: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S39-22: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S40-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S46-01: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S46-03: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S46-05: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S47-07: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S47-08: Pixel offsets belong to build_rules/theme.md.
- S48-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S50-01: Shared deletion-confirmation wording (UI-06), not another calendar-deletion rule.
- S51-02: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S51-04: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S51-23: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S51-30: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S51-32: Internal sign-in/invite map bookkeeping; single-use consent/invite outcomes are specified above.
- S51-33: Internal sign-in/invite map bookkeeping; single-use consent/invite outcomes are specified above.
- S51-48: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-02: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-03: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-10: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-11: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-12: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S55-14: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S55-16: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S55-17: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S55-19: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S55-22: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S56-01: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S56-04: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S56-16: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S56-25: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S67-24: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S67-27: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S68-06: Setup endpoint result encoding; client configuration behavior is specified above.
- S69-01: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-02: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-03: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-04: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-05: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-06: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-07: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S69-08: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S69-09: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S70-01: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S70-05: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S70-06: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S70-12: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S70-17: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S70-20: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S70-21: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S72-01: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-02: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-03: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-04: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-05: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-06: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-07: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S73-12: Always-true or True predicate; cannot independently verify secret/token storage.
- S74-01: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-02: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-03: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-04: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-06: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-07: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-08: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-09: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S77-28: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S77-29: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S77-30: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.

### Coverage and open questions

All 400 Google-candidate rows are accounted for in 80 proposed requirements and
98 excluded/shared-owner mappings. Questions above preserve gaps in token protection, retry/renewal
thresholds, color/description handling and conflicting historical client/calendar recovery behavior.
Historical tests use finite samples and permissive predicates; they do not establish full OAuth validation,
exact production timing, or live-service availability. No application suites were run locally.
