# Requirements: settings

☰ Settings, preferences, updates, public address. Issues against this feature (kept in the issues database): I2
(auto-update toggle, built beta.46), I25. I22 was closed Nov 17: the Developer decided to keep the separate pop-ups, so SET-06 stands as written.

| ID | status | statement | test | was |
|---|---|---|---|---|
| SET-01 | planned | Settings lets the Developer select another release (a build), including one typed by hand, for a temporary release made to solve one user's problem. Deferred: needs a change to the updater container's protocol. | — | F24.1 |
| SET-02 | planned | Settings can show an alternate port, and write it to `.env`; a change takes effect when the container is recreated. Deferred with SET-01. | — | F24.3 |
| SET-03 | planned | The update channel is selectable: Stable, Beta or Other. Deferred with SET-01. | — | F24.4, F54 |
| SET-04 | open | Changing or adding a domain, with Google Calendar API Sync already configured, pops up a notice pointing at that module's assist box, since the API always becomes unhealthy. | — | F56 |
| SET-05 | built | In Full mode, the page's modules (Calendar, Sources, Feeds, All Rules, Event Templates, History) are hidden elsewhere and listed above Settings under a Configure heading. | — | F65 |
| SET-06 | built | Settings has two headings, User (Login, Updates, Theme, each its own item) and Site Admin (Domains, Google API, more as added); every item opens as a pop-up. | — | F65 |
| SET-07 | built | The Settings pop-up stays centered with a dimmed background and a 130×34 px joined Cancel \| Save pair, as theme.md §6 says. | — | F65 |
| SET-47 |  | Settings has a Time Zones item with two choices: Follow System Time Zone (the zone of the device in use, so a phone and a PC may differ) or Fixed Time Zone (chosen with the same time zone picker as the calendar). After installation, the first sign-in follows the system time zone. The choice (Follow System or Fixed, and the fixed zone) is stored on the device, like the other view settings (Developer, Nov 17: for now, to stay consistent). The calendar's own time zone picker only changes the view temporarily and does not change this setting. (Developer, Nov 17) | — | Developer |
| SET-48 |  | Settings has a Search item, alongside Time Zones, to change how many search results each feature shows at first and in each step of "more" (default six). Stored on the device like the other view settings. (Developer, Nov 17) | — | Developer |
| SET-58 |  | Settings > Theme has a time notation choice, local to the device like the time format (TIM-10): 12-hour as "12:00 PM" or "12:00 pm"; 24-hour as "1200" or "12:00". The four choices are spelled out in the setting's (?) help, in the form HH:MM PM. (Developer, Nov 17) | — | Developer, Nov 17 |
| SET-59 |  | Settings > Site Admin has a Default time zone item, like Domains. It is stored in the database, and the database value overrides the installation's TZ setting (DEP-27). (Developer, Nov 17) | — | Developer, Nov 17 |
| SET-08 | proposed | An initial environment public address is imported once and shown as the saved public address; clearing it does not reimport it on the next initialization. An empty initial value also records that import is complete. | — | S15-01, S15-09, S25-12 |
| SET-09 | proposed | Without a public address, setup reports Not set yet and directs the user to Public address settings; the subscription page warns that the address is missing. | — | S15-02, S15-10 |
| SET-10 | proposed | A bare public host becomes an HTTPS address, with lowercase scheme/host, no trailing slash and no default port; a supplied path is preserved. | — | S15-03, S23-05, S23-06, S23-13 |
| SET-11 | proposed | The saved public address is used in feed links and Google callback addresses. Once set, setup no longer reports it as unset. | — | S15-04, S15-05 |
| SET-12 | proposed | Public addresses using FTP, queries, embedded credentials or malformed non-URLs are refused. | — | S15-06 |
| SET-13 | proposed | Clearing the public address removes the saved effective address. Legacy HTTP private-IP and localhost installer defaults are treated as unset. | — | S15-08, S23-01, S23-16 |
| SET-14 | proposed (?) | When opened through a host different from the configured public host, the page warns and identifies both hosts; it omits that warning for the configured host or the checked LAN-IP access. Is LAN-IP suppression intended for all private network addresses? | — | S24-01, S24-08, S24-09 |
| SET-15 | proposed | Administrator email is trimmed when saved; malformed addresses are refused and an empty value clears it. | — | S25-03, S25-04, S25-07 |
| SET-16 | proposed | Before the first destination is configured, setup suggests a public address from the request; after it is set, that initial setup field is no longer offered. | — | S26-31, S26-34 |
| SET-17 | proposed | Update checks offer hourly, weekly, monthly or never, with weekly initially selected. Unsupported frequencies are refused. | — | S22-01, S22-09 |
| SET-18 | proposed | Stable installations check stable releases rather than a newer beta; beta installations check beta releases and can advance to the resulting stable release. A pinned non-beta release selects stable, while a pinned beta selects beta. | — | S22-03, S22-07, S22-08, S30-04, S30-06, S30-07, S30-08 |
| SET-19 | proposed (?) | Versions compare numeric beta sequence numbers in order and place a release after its beta. Unknown installed versions or the checked unrecognized version forms do not produce a newer-version result. Which complete version grammar should be supported? | — | S30-01, S30-02, S30-03 |
| SET-20 | proposed | When no newer release is available, Updates reports Up to date; otherwise it offers the newer version and links to the running and available releases. | — | S22-04, S22-05 |
| SET-21 | proposed | Changing update channel clears the previous channel’s check result. | — | S22-06 |
| SET-22 | proposed (?) | Never disables automatic checks. Hourly checks become due between the checked 30- and 61-minute points, and monthly checks between 29 and 31 days. What exact schedule and meaning of monthly should be promised? | — | S22-10, S22-11, S22-12, S25-11 |
| SET-23 | proposed | Updates reports Not checked before a check and shows its next scheduled check time. An hourly check fifty minutes old schedules the next check about ten minutes later. | — | S25-10, S59-05 |
| SET-24 | proposed | A failed update check preserves the last offered version and reports the failure; a stable channel receiving an invalid beta offer also preserves its last stable offer and reports an error. | — | S22-13, S30-09 |
| SET-25 | proposed (?) | A manual update check does not clear the stored version already marked as logged. Is this marker intended to suppress repeated update notices? | — | S22-15 |
| SET-26 | proposed | Update now is available when the updater service is ready and an update is offered; an unavailable updater leaves installer guidance rather than a runnable update action. | — | S32-01, S32-02, S32-03, S32-13, S37-25, S37-26, S42-01, S42-02, S47-01 |
| SET-27 | proposed | Update now requests the offered app image through the configured updater using its authorization token; it does not request unrelated images. | — | S32-04 |
| SET-28 | proposed | Starting an update records an activity message naming its target version. | — | S32-05 |
| SET-29 | proposed | Updater token rejection reports update failure and its reason. | — | S32-07, S32-11, S47-05 |
| SET-30 | proposed | An exact pinned image version does not offer Update now, and a direct update request is refused. | — | S32-08 |
| SET-31 | proposed | A running update reports Downloading; once the running version changes, the page identifies the new release and removes the obsolete update offer. | — | S32-09, S32-10, S42-04, S42-05, S42-06, S47-02, S47-03, S47-04 |
| SET-32 | proposed | Automatic updating can be enabled or disabled, but cannot be enabled through the offered control without a ready updater. Repeated installation checks do not request the same pending update twice. | — | S38-08, S38-10, S38-11, S38-12 |
| SET-33 | proposed | Saving a public address or update frequency persists the choice. | — | S38-17, S38-18 |
| SET-34 | proposed | Each Check now request performs a new version check, reports whether an update was found, and retains the running-version information. A failed check reports Couldn’t check and its cause. | — | S42-03, S42-07, S43-04, S43-05, S43-06, S43-07, S43-08, S43-09, S67-33 |
| SET-35 | proposed | Extra public addresses are validated individually; blank extras are omitted and invalid extras identify their field. | — | S51-14, S51-15 |
| SET-36 | proposed (?) | A pending update exposes its target version, but an update marker older than sixteen minutes or belonging to a different starting version is no longer effective. What is the exact expiry boundary? | — | S59-01, S59-02, S59-03, S59-04 |
| SET-37 | proposed (?) | While an observed update loses contact with the app, progress changes from Downloading to Restarting; once contact returns, the page reloads after a settling delay. What delay should be required beyond the checked timing samples? | — | S59-24, S59-25, S59-26, S59-27 |
| SET-38 | proposed | Domains can be saved independently of Login settings, and an invalid main address identifies the main-address field. | — | S64-12, S64-13 |
| SET-39 | proposed | A custom PNG logo can be uploaded and displayed; without one the custom-logo address is unavailable. Invalid favicon bytes and the checked script-bearing SVG are refused. This evidence is not a complete image-sanitization guarantee. | — | S64-15, S64-16, S64-17, S64-18 |
| SET-40 | proposed (?) | Animation intensity and duration preferences are saved; the checked settings 150 and 50 yield factors 1.5 and 0.5. Intensity 500 is refused. What complete ranges and units should users be promised? | — | S64-19, S64-21 |
| SET-41 | proposed | Resetting the logo also clears the checked animation overrides and removes the custom image. | — | S64-20 |
| SET-42 | proposed | Module grips default to the left; choosing right saves that preference, and choosing left removes the override. | — | S65-26, S65-27, S65-29 |
| SET-43 | proposed | Removing or clearing public-address rows leaves one main address field, with its value cleared when removed; removing the extra row leaves the main address row. Shared row controls are not specified here. | — | S67-18, S67-20, S67-22 |
| SET-44 | proposed | Changing the public address warns about the Google callback configuration. Existing SET-04 owns the assist-box requirement; Google owns callback validation. | — | S67-25 |
| SET-45 | proposed | Effective public addresses are deduplicated, with the main address first and valid extras afterward. | — | S77-18 |
| SET-46 | proposed | Reopening Updates reflects the current saved auto-update preference, including changes made by another client. A refused auto-update save leaves the prior value in effect. | — | S81-09, S81-10 |

## Notes from the draft

### Not requirements

These rows are accounted for without duplicating shared mechanics or promoting implementation details.

- S15-07: Shared change-security token enforcement; shared/account security owns this rather than another settings-specific rule.
- S19-49: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S19-52: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S19-53: Pixel positions, border/background colors and control dimensions belong to theme rules.
- S21-10: Pixel positions, border/background colors and control dimensions belong to theme rules.
- S22-02: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S23-14: Failure sentinel and paired exception-handler marker; not independent validation coverage.
- S23-15: Failure sentinel and paired exception-handler marker; not independent validation coverage.
- S31-10: Shared section-key validation, not a settings preference outcome; retained for shared UI review.
- S31-17: Pixel positions, border/background colors and control dimensions belong to theme rules.
- S37-24: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S38-09: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S38-19: Pixel positions, border/background colors and control dimensions belong to theme rules.
- S40-07: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S43-01: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S43-02: Pixel positions, border/background colors and control dimensions belong to theme rules.
- S43-03: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S44-19: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S44-20: Pixel positions, border/background colors and control dimensions belong to theme rules.
- S46-04: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S46-28: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S47-06: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S59-23: Control state spans, callbacks, shared feedback reset, button geometry and markup are UI/implementation mechanics. Actual check/update outcomes are specified above.
- S64-11: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S66-06: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S66-07: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S66-08: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S66-09: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S67-19: Shared add/remove-row control placement and notice dismissal; UI-02 governs layer dismissal. Domain data outcomes are specified above.
- S67-21: Shared add/remove-row control placement and notice dismissal; UI-02 governs layer dismissal. Domain data outcomes are specified above.
- S67-23: Shared add/remove-row control placement and notice dismissal; UI-02 governs layer dismissal. Domain data outcomes are specified above.
- S67-28: Shared add/remove-row control placement and notice dismissal; UI-02 governs layer dismissal. Domain data outcomes are specified above.
- S67-29: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S67-30: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S67-31: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S67-32: Settings grouping/form/heading markup; existing SET-06 owns organization. No duplicate mechanics or legacy-ID requirements are added.
- S80-01: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-02: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-03: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-04: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-05: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-06: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-07: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-08: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-09: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-10: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S80-11: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S81-01: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S81-02: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S81-04: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.
- S81-06: Shared Settings/Configure navigation, dialog IDs and form arrangement; existing SET-05/SET-06 and UI-01/UI-02 own these mechanics. Source-string absence is not a separate behavior requirement.

### Coverage and open questions

All 165 settings-candidate evidence rows are accounted for in 39 proposed requirements and
51 excluded/shared-owner mappings. Questions above preserve uncertainty about schedules, version
grammar, animation ranges and update observation timing. Image rejection examples do not establish
a comprehensive upload security policy. No application suites were run locally for this draft.
