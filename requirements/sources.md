# Requirements: sources

Statuses: verified, built, open, planned (approved, not built yet) and proposed (drafted, not yet reviewed by the Developer).

| ID | status | statement | test | was |
|---|---|---|---|---|
| SRC-01 | proposed | Free/busy information from an imported calendar is preserved: events marked transparent remain free. | — | S13-01 |
| SRC-02 | proposed | The automatic-download interval is an admin setting kept in the database; the installation's value is only its starting value (DEP-28, DEF-01). | — | S14-04, S14-05, S14-11, S14-12, changelog_gaps_2101-2336:38 |
| SRC-03 | proposed | The next download is scheduled from the last attempt plus the configured interval; if that time has passed, changing the interval schedules an immediate download. | — | S14-06, S14-07 |
| SRC-04 | proposed | The download interval stays within the limits in DEF-01; a value outside them, or not a number, is not valid (UI-19). | — | S14-08, S14-09, readme_gaps:31, changelog_gaps_1801-2100:34 |
| SRC-05 | proposed | Changes to download settings or source credentials follow the shared form-security rules (ACC-09). | — | S14-10, S16-28 |
| SRC-06 | proposed | Existing CCS+ credentials can be imported from the legacy configuration, stored encrypted, and recorded as imported activity. | — | S16-02, S16-03 |
| SRC-07 | proposed | Saved CCS+ credentials are used for the next download. | — | S16-22, S16-24 |
| SRC-08 | proposed | The saved CCS+ password is protected (ACC-05); the page shows the saved username and explains how to keep its password. | — | S16-23, S16-25, S16-34 |
| SRC-09 | proposed | Changing the CCS+ username while leaving the password blank keeps the saved password. | — | S16-26 |
| SRC-10 | proposed | An invalid CCS+ username is refused with a username error. | — | S16-27, S28-13 |
| SRC-11 | proposed | Missing CCS+ credentials are reported as Setup needed rather than an error, and Sync now is unavailable until credentials are entered. | — | S18-01, S18-02, S18-06 |
| SRC-12 | proposed | CCS+ setup is available directly with the source when it needs configuration, rather than only in Settings. Successful credential saving returns to that source. | — | S16-20, S18-03, S18-04, S18-07, S27-01 |
| SRC-13 | proposed | CCS+ guidance distinguishes Calendar Sync credentials from CCS login credentials and explains enabling CCS+. | — | S18-05, S33-03 |
| SRC-14 | proposed | Rejected CCS+ credentials show a failure reason beside the credential fields; successful verification reports Validated. Editing the credentials removes stale validation or rejection feedback. | — | S18-08, S18-09, S19-19, S19-47, S19-48, S28-01, S28-08, S28-09, S28-10, S28-11 |
| SRC-15 | proposed | Calendar downloads, including a custom CCS+ site address, require HTTPS; a plain HTTP address is not valid. Clearing a custom CCS+ address removes the override. | — | S23-28, S26-07, S60-21, S27-02, S27-03, S27-04 |
| SRC-16 | proposed | A fresh installation starts with one Local calendar as the default, with no configured CCS+ source or destinations. | — | S26-01, S26-02, S36-19, S49-01, S63-12 |
| SRC-17 | proposed | One CCS+ source can be added; attempting to add a second is refused. | — | S26-05, S26-06 |
| SRC-18 | proposed | A webcal source address is saved as its equivalent HTTPS address with its chosen name; duplicate source addresses are refused. | — | S26-08, S26-09 |
| SRC-19 | proposed | Recurring source events expand into distinct occurrences while retaining source-qualified identities. Moving one recurrence preserves the occurrence identities and updates its changed title. | — | S26-10, S53-13 |
| SRC-20 | proposed | A successful feed download reports healthy status even when another source has no events. | — | S26-11 |
| SRC-21 | proposed | Removing a source removes its stored events and its membership from destinations, while keeping a combined Google destination. | — | S26-50, S26-51 |
| SRC-22 | proposed | Legacy migration creates the CCS+ source (destination scoping is in FED-12; the Google destination migration is in the google feature). | — | S26-64 |
| SRC-25 | proposed | Successful upload ends the source’s setup-needed configuration state. | — | S27-06 |
| SRC-26 | proposed | Credential saving reports saving/verification progress and a saved acknowledgement before successful validation. Shared save/cancel interaction follows SET-07; this rule specifies the verification outcome. | — | S28-05, S28-06, S28-07 |
| SRC-28 | proposed | A source can be renamed and given a note; saving updates its name and explanatory note, and clearing the note removes its content. | — | S18-17, S29-11, S33-05, S39-18, S44-16 |
| SRC-29 | proposed | Credentials are labeled Username rather than UID. | — | S31-05 |
| SRC-30 | proposed | Source presets identify the provider and offer provider-specific setup guidance, including Google secret-address guidance and the United Airlines CCS+ name. Choosing Apple selects the Apple preset. | — | S33-01, S33-02, S33-23 |
| SRC-31 | proposed | Sync Now updates a source in the background: it reports Syncing during work and Healthy on success, and keeps unrelated unsaved source edits. | — | S33-15, S33-18, S33-19, S35-28, S35-29, S35-31, S44-18 |
| SRC-34 | proposed | Local calendars do not offer Sync Now (CAP-06); the default calendar is identified (SRC-59). | — | S36-20, S36-23, S36-24, S49-02, S63-16 |
| SRC-35 | proposed | Additional Local calendars can be created; an unnamed one is named Local. | — | S36-22, S36-48 |
| SRC-36 | proposed | Removing the last Local calendar keeps that calendar and empties its events, rather than leaving no Local calendar; its feed and rule memberships are kept, and ensuring a Local calendar afterward does not create a duplicate. | — | S36-46, S36-47, S49-32, readme_gaps:63, changelog_gaps_601-900:39 |
| SRC-37 | proposed | Removing a source can preserve its events by creating a Local calendar with its prior color and destination memberships, or by merging into an existing Local calendar. The original source is removed. | — | S37-20, S37-21, S37-22, S49-28 |
| SRC-39 | proposed | Source color can be changed and saved; the new color is reflected immediately in its source display. | — | S38-15, S59-22 |
| SRC-40 | proposed | A source reports when it last synced (a download or an upload) or that a read, check or download failed. | — | S44-11, S27-05, S31-04, S31-19, S40-04, S35-32 |
| SRC-41 | proposed | Source calendars offer file import. | — | S18-15, S44-38 |
| SRC-42 | proposed (?) | If a future event disappears from a subsequent source upload, its deletion is retained with its title. How long should this retained deletion remain available? | — | S49-17 |
| SRC-43 | proposed | Importing with a date range (UI-23) excludes events outside it; completing import creates events from the included entries. | — | S49-21, S49-22 |
| SRC-44 | proposed | Importing an entry that conflicts with an existing event identifies the conflict; choosing merge preserves the incoming changed event and other included entries. | — | S49-23, S49-24 |
| SRC-45 | proposed | Calendar export downloads an ICS attachment containing its events. | — | S49-26 |
| SRC-46 | proposed | Calendar removal identifies its owned rules, and deleting the calendar removes those rules. | — | S49-27, S49-31 |
| SRC-47 | proposed | Removing CCS+ also removes its active saved login. | — | S49-33 |
| SRC-48 | proposed | A download keeps at most the number of events in DEF-01; the earliest events are kept, whatever the input order. | — | S53-14, changelog_gaps_601-900:22 |
| SRC-49 | proposed | A downloaded calendar retains calendar content and cache validators; a matching ETag can return an unchanged result rather than downloading the content again. | — | S60-05, S60-10 |
| SRC-50 | proposed | A wrong download password is reported as a credential rejection; upstream protection denial is reported as blocking, not as invalid credentials. A rejected password ends the download attempt at once, without trying another connection mode or spending a retry delay. | — | S60-11, S60-12, S60-25, S60-26, changelog_gaps_301-600:40 |
| SRC-51 | proposed | A successful HTTP response containing HTML instead of calendar data is refused; malformed calendar data is also refused. | — | S60-13, S77-08, S77-09 |
| SRC-52 | proposed | An HTTPS redirect on the same host can complete the download; a redirect to plain HTTP is refused, and a redirect loop is reported. | — | S60-14, S60-15, S60-16 |
| SRC-53 | proposed | A download larger than the size limit in DEF-01 is not accepted. | — | S60-17 |
| SRC-54 | proposed | Following a calendar redirect to a different host does not forward the source’s authorization credentials. | — | S60-18 |
| SRC-55 | proposed | A download that does not reply reports a timeout and explains the manual-upload alternative. | — | S60-19 |
| SRC-56 | proposed (?) | Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? | — | S60-22, S60-23, S60-24 |
| SRC-57 | proposed | A Local calendar can be selected as default; a read-only CCS+ calendar cannot (CAP-05). | — | S63-13, S63-14, S63-15, S66-04 |
| SRC-58 | proposed | A source can be turned off and back on, with its saved off state cleared when reenabled. | — | S63-20, S63-21, S63-23 |
| SRC-59 | proposed | A valid saved Local default calendar is used whatever the source order; if it no longer exists, the first Local calendar is used. With no sources, creating a Local calendar also makes it the default. | — | S77-13, S77-14, S77-15 |
| SRC-60 | proposed (?) | The user can add source calendars and outgoing feeds without an application-defined count limit. How does this promise relate to the one-CCS+ constraint SRC-17? | — | readme_gaps:20 |
| SRC-61 | proposed | Calendar links from Outlook, Microsoft 365 and iCloud can be downloaded as source calendars. | — | readme_gaps:21 |
| SRC-62 | proposed | A failed source download preserves the previously downloaded schedule. | — | readme_gaps:22, changelog_gaps_2101-2336:37 |
| SRC-63 | proposed (?) | A source download that unexpectedly returns an empty calendar preserves the previous schedule. How is an unexpected empty response distinguished from an intentionally emptied source? | — | readme_gaps:22, changelog_gaps_2101-2336:37 |
| SRC-65 | proposed | CCS+ downloading offers auto, browser, browser-patient and curl modes, initially auto. | — | readme_gaps:32, changelog_gaps_301-600:39 |
| SRC-66 | proposed | In auto mode, an unanswered or blocked CCS+ download tries the browser-like connection, retries with twice the wait, then tries curl. | — | readme_gaps:32, changelog_gaps_301-600:39 |
| SRC-67 | proposed | Browser-patient mode makes the number of CCS+ download attempts in DEF-01, each with its response allowance. | — | changelog_gaps_301-600:39 |
| SRC-68 | proposed | The download diagnostic record identifies the connection mode that answered and the modes previously attempted. | — | changelog_gaps_301-600:39 |
| SRC-69 | proposed | CCS+ import preserves the source event identifiers and details; event times follow TIM-01–TIM-06 and normalization follows RUL-29. | — | readme_gaps:37 |
| SRC-70 | proposed | When CCS+ full-day times are normalized, the original times remain available in the event notes. | — | readme_gaps:37 |
| SRC-71 | proposed | Upload & publish for CCS+ replaces the downloaded schedule with the uploaded schedule. | — | readme_gaps:38, changelog_gaps_601-900:36 |
| SRC-72 | proposed | After the number of rejected CCS+ sign-ins in DEF-01, automatic checks pause until the user corrects the credentials and requests Sync Now. | — | readme_gaps:39, changelog_gaps_2101-2336:37 |
| SRC-73 | proposed | The user can change source-calendar and outgoing-feed order, and the new order is saved immediately; shared interaction follows UI-13. | — | readme_gaps:59, changelog_gaps_1201-1500:15 |
| SRC-74 | proposed | When source events conflict, the earlier source in the saved source order has priority. | — | readme_gaps:60, changelog_gaps_301-600:27 |
| SRC-75 | proposed | Recurring source events are expanded over the period in DEF-01. | — | readme_gaps:61, changelog_gaps_1501-1800:24 |
| SRC-76 | proposed | When an imported event conflicts with an existing event, the user can discard the incoming copy. | — | readme_gaps:62, changelog_gaps_601-900:36 |
| SRC-77 | proposed | An import-conflict choice can be applied to all remaining conflicts in that import. | — | readme_gaps:62, changelog_gaps_601-900:36 |
| SRC-78 | proposed | When merging a calendar into another, the user can transfer its owned rules to the target or delete those rules. | — | readme_gaps:63, changelog_gaps_601-900:39 |
| SRC-80 | proposed (?) | An upgrade creates its initial Local calendar once. Is it then added to every existing feed, or does each feed decide which calendars it carries (FED-30)? | — | changelog_gaps_1201-1500:18 |
| SRC-81 | proposed | CCS+ setup guidance explains enabling trips as one event and the other calendar options, setting a dedicated Calendar Sync password, and completing the Accomplished checklist. | — | changelog_gaps_1201-1500:24 |
| SRC-82 | proposed | A CCS+ download follows no more redirects than DEF-01 allows; HTTPS and credential forwarding follow SRC-52 and SRC-54. | — | changelog_gaps_1501-1800:37, changelog_gaps_301-600:40 |
| SRC-83 | proposed | The source status event count counts the published feed events, with event visibility determined by CAP-02. | — | changelog_gaps_2101-2336:30 |
| SRC-84 | proposed | Calendar downloads keep sign-in credentials out of process command-line arguments; stored and displayed secret protection follows ACC-05. | — | changelog_gaps_2101-2336:31 |
| SRC-85 | proposed | Download failure feedback distinguishes failure to connect from a connected server that does not reply. | — | changelog_gaps_2101-2336:33 |
| SRC-87 | proposed | Turning a source off removes its events from published feeds while retaining its selected feed memberships for reenabling. | — | changelog_gaps_301-600:23 |
| SRC-89 | proposed | When a recurring source occurrence moves, its existing local edits remain attached using its original-start identity. | — | changelog_gaps_601-900:21 |
| SRC-91 | proposed | Future source events that disappear from a refreshed schedule remain available for restoration; SRC-42 retains the open retention-duration question. | — | changelog_gaps_601-900:35 |
| SRC-92 | proposed | Legacy source notes that merely repeat the source kind are treated as absent notes. | — | changelog_gaps_901-1200:24 |

Retired IDs (merged or dropped; numbers are never reused): SRC-23 into SRC-15; SRC-64 into SRC-04; SRC-86 into SRC-02; SRC-24 and SRC-32 into SRC-40; SRC-79 into SRC-36; SRC-88 into SRC-50; SRC-90 into SRC-48; SRC-33 (same as SRC-28); SRC-27 and SRC-38 (a control that cannot give a wrong value needs no rule).

## Notes from the draft

### Not requirements

These mappings account for evidence without defining duplicate UI or implementation requirements.

- S14-02: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S14-03: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S16-21: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S19-24: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S21-12: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S21-24: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S23-27: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S26-13: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S27-07: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S28-02: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S28-03: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S28-04: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S31-12: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S31-16: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S33-04: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S33-20: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-09: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S34-10: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-11: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-12: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-14: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-19: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S34-20: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S34-21: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S34-22: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-19: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-22: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-23: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-30: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-33: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-34: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S35-35: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S35-36: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S37-28: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S37-29: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S37-30: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S37-31: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S37-32: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S37-48: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S37-49: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S41-01: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S41-02: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S44-08: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S44-29: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S44-30: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S44-31: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S44-34: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S44-43: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S49-03: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S49-20: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S53-17: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S60-01: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-02: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-03: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-04: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-06: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-07: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-08: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-09: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-20: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S60-27: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S61-06: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S61-19: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-20: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-21: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-22: Shared save/cancel mechanics; see SET-07 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-28: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S63-19: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S63-29: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S66-02: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S66-03: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S66-05: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S77-19: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-20: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-21: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-26: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-27: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S81-03: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S81-05: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.

### Coverage and open questions

All 227 source-candidate rows are accounted for: 60 proposed requirements and
79 excluded/shared-owner evidence mappings. No application suites were run locally.
Questions above preserve uncertainty about retention and automatic retries. The import conflict policy,
complete validation ranges and source-removal dialog defaults require Developer review beyond the finite
examples in the oracle; these drafts do not silently add broader guarantees.
