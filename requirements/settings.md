# Requirements: settings

☰ Settings, preferences, updates, public address. Issues against this feature (kept in the issues database): I2
(auto-update toggle, built beta.46), I25. I22 was closed Nov 17: the Developer decided to keep the separate pop-ups, so SET-06 stands as written.

| ID | status | statement | test | was |
|---|---|---|---|---|
| SET-01 | planned | Settings lets the Developer select another release (a build), including one typed by hand, for a temporary release made to solve one user's problem. Deferred: needs a change to the updater container's protocol. | — | F24.1 |
| SET-02 | planned | Settings can show an alternate port, and write it to `.env`; a change takes effect when the container is recreated. Deferred with SET-01. | — | F24.3 |
| SET-03 | planned | The update channel is selectable: Stable, Beta or Other. Deferred with SET-01. | — | F24.4, F54 |
| SET-04 | open | Changing or adding a domain or the public address, with Google Calendar API Sync already configured, pops up a notice pointing at that module's assist box, since the API always becomes unhealthy (GGL-46 gives the callback to authorize). | — | F56, S67-25 |
| SET-05 | built | In Full mode, the page's modules (Calendar, Sources, Feeds, All Rules, Event Templates, History) are hidden elsewhere and listed above Settings under a Configure heading. | — | F65 |
| SET-06 | built | Settings has two headings. **User** items are stored on the device (view preferences: Theme, Time Zones, time notation, Search) and can differ from device to device. **Site Admin** items are stored once in the database and are the same on every device and browser: Login, Domains, Google API, Updates (whether to check at all, automatic updating, how often), Default time zone, Backup and Restore, more as added. Every item opens as a pop-up. (Developer, Nov 17: admin settings are retained across devices, which is why they are in admin.) | — | F65 |
| SET-07 | built | The Settings pop-up follows the shared dialog rules (UI-01 to UI-03) and its Cancel \| Save pair looks as theme.md §6 says. | — | F65 |
| SET-47 |  | Settings has a Time Zones item with two choices: Follow System Time Zone (the zone of the device in use, so a phone and a PC may differ) or Fixed Time Zone (chosen with the same time zone picker as the calendar). After installation, the first sign-in follows the system time zone. The choice (Follow System or Fixed, and the fixed zone) is stored on the device, like the other view settings (Developer, Nov 17: for now, to stay consistent). The calendar's own time zone picker only changes the view temporarily and does not change this setting. (Developer, Nov 17) | — | Developer |
| SET-48 |  | Settings has a Search item, alongside Time Zones, to change how many search results each feature shows at first and in each step of "more" (default six). Stored on the device like the other view settings. (Developer, Nov 17) | — | Developer |
| SET-58 |  | Settings > Theme has a time notation choice, local to the device like the time format (TIM-10): 12-hour as "12:00 PM" or "12:00 pm"; 24-hour as "1200" or "12:00". The four choices are spelled out in the setting's (?) help, in the form HH:MM PM. (Developer, Nov 17) | — | Developer, Nov 17 |
| SET-59 |  | Settings > Site Admin has a Default time zone item, like Domains. It is stored in the database, and the database value overrides the installation's TZ setting (DEP-27). (Developer, Nov 17) | — | Developer, Nov 17 |
| SET-60 |  | Settings > Site Admin has Backup and Restore. A backup contains both the calendar data and the database, including the saved passwords and Google sign-in (still encrypted, so the same database password is needed to read them after a restore). Backup downloads as a file to the device in use; Restore takes that file and, because it replaces everything, asks first (UI-06). (Developer, Nov 17) | — | Developer, Nov 17; README Data and backups |
| SET-08 | proposed | A public address given at installation is saved once. After that the saved address is the only one used (DEP-28), so clearing it leaves it cleared. | — | S15-01, S15-09, S25-12 |
| SET-09 | proposed | Until a public address is set, setup reports Not set yet and points to Public address settings, the subscription page warns that the address is missing and, before the first destination is configured, setup suggests an address taken from the request. Once an address is set, none of these appear; a setup field can be filled from the address used to open the page. | — | S15-02, S15-10, S26-31, S26-34 |
| SET-10 | proposed | A bare public host becomes an HTTPS address, with lowercase scheme/host, no trailing slash and no default port; a supplied path is preserved. | — | S15-03, S23-05, S23-06, S23-13 |
| SET-11 | proposed | The saved public address is the one used in feed links; Google's callback address follows GGL-45. | — | S15-04, S15-05 |
| SET-12 | proposed | An address that uses FTP, has a query or embedded credentials, or is not a URL is not a valid public address (UI-19). | — | S15-06 |
| SET-13 | proposed | Clearing the public address removes it. An installer default that only works on the local machine or network (HTTP to a private IP address or localhost) is not a public address. | — | S15-08, S23-01, S23-16 |
| SET-14 | proposed | The page warns when it is opened through a host that is not a public host of the installation or one of the user's own networks (ACC-07), naming the host used and the configured host. | — | S24-01, S24-08, S24-09 |
| SET-15 | proposed | Administrator email is trimmed when saved, an empty value clears it, and a malformed address is not valid (UI-19). | — | S25-03, S25-04, S25-07 |
| SET-17 | proposed | Update checks run on the chosen schedule (hourly, weekly, monthly or never; the default and values are in DEF-01). Never turns automatic checks off. | — | S22-01, S22-09, S22-10, S22-11, S22-12, S25-11 |
| SET-18 | proposed | Stable installations check stable releases rather than a newer beta; beta installations check beta releases and can advance to the resulting stable release. A pinned non-beta release selects stable, while a pinned beta selects beta. | — | S22-03, S22-07, S22-08, S30-04, S30-06, S30-07, S30-08 |
| SET-19 | proposed | A version is major.minor.patch with an optional -beta.N (0.2.8-beta.46). A release is newer than its betas, and betas compare by their number. A version that does not follow this form, and an unknown installed version, cannot be compared, so it is not offered as newer. | — | S30-01, S30-02, S30-03 |
| SET-20 | proposed | A check, scheduled or Check now, reports Up to date when nothing newer is available; otherwise it offers the newer version with links to the running and available releases, and keeps the running-version information. A failed check, including an invalid offer, reports Couldn't check and its cause and keeps the last offered version. | — | S22-04, S22-05, S22-13, S30-09, S42-03, S42-07, S43-04, S43-05, S43-06, S43-07, S43-08, S43-09, S67-33 |
| SET-21 | proposed | Changing update channel clears the previous channel’s check result. | — | S22-06 |
| SET-23 | proposed | Updates reports Not checked before the first check and shows the next scheduled check time. | — | S25-10, S59-05 |
| SET-25 | proposed | An available version is announced in History once, however many times it is checked for. | — | S22-15 |
| SET-26 | proposed | Update now is offered only when an update is available, the updater service is ready and the installation is not pinned to an exact image version; otherwise the page shows installer guidance. Automatic updating, which the user can turn on or off, follows the same conditions, and a pending update is requested once. | — | S32-01, S32-02, S32-03, S32-08, S32-13, S37-25, S37-26, S38-08, S38-10, S38-11, S38-12, S42-01, S42-02, S47-01 |
| SET-27 | proposed | Update now requests the offered app image through the configured updater using its authorization token; it does not request unrelated images. | — | S32-04 |
| SET-28 | proposed | Starting an update records an activity message naming its target version. | — | S32-05 |
| SET-29 | proposed | An update that cannot reach the updater, or whose token the updater rejects, reports Update failed and the cause. | — | S32-07, S32-11, S47-05, changelog_gaps_1201-1500:35 |
| SET-31 | proposed | A running update reports Downloading; once the running version changes, the page identifies the new release and removes the obsolete update offer. | — | S32-09, S32-10, S42-04, S42-05, S42-06, S47-02, S47-03, S47-04 |
| SET-35 | proposed | Each extra public address is validated on its own; blank extras are left out and an invalid extra is not valid (UI-19). | — | S51-14, S51-15 |
| SET-36 | proposed | A running update is remembered for the time in DEF-01, and only for the version it started from; after that, or once the running version has changed, it is no longer shown as running. | — | S59-01, S59-02, S59-03, S59-04 |
| SET-37 | proposed | While an update is applying, every open client shows its progress, Downloading and then Restarting, including a client that did not start it; each reconnects when the app is back, refreshes after the time in DEF-01, and shows the new release with its Settings context kept (UI-13). | — | S59-24, S59-25, S59-26, S59-27, readme_gaps:77, changelog_gaps_301-600:41, changelog_gaps_901-1200:23 |
| SET-38 | proposed | Domains can be saved independently of Login settings. | — | S64-12, S64-13 |
| SET-39 | proposed | A custom PNG logo can be uploaded and shown; without one the default logo is used. An image that is not a valid PNG logo, or that can carry script, is not accepted. | — | S64-15, S64-16, S64-17, S64-18 |
| SET-40 | proposed | Animation intensity and animation duration are Theme settings; their defaults and ranges are in DEF-01, and Reset restores the defaults. | — | S64-19, S64-21 |
| SET-41 | proposed | Resetting the logo removes the custom image and restores the default logo. It does not change any other setting. | — | S64-20 |
| SET-42 | proposed | Module grips are on the left by default; the user may move them to the right. | — | S65-26, S65-27, S65-29 |
| SET-43 | proposed | Removing or clearing public-address rows leaves one main address field, with its value cleared when removed; removing the extra row leaves the main address row. | — | S67-18, S67-20, S67-22 |
| SET-45 | proposed | Effective public addresses are deduplicated, with the main address first and valid extras afterward. | — | S77-18 |
| SET-46 | proposed | Reopening Updates shows the current saved update-check frequency and auto-update preference, including a change made on another client. A change that fails to save leaves the previous value in effect and shows it. | — | S81-09, S81-10, changelog_gaps_1-300:15, changelog_gaps_1-300:18 |

Also retired (merged): SET-49, SET-55 and SET-57 into SET-37; SET-50 and SET-51 into SET-46; SET-52 into SET-29; SET-53 into SET-25; SET-54 into SET-09; SET-56 into SET-17.

Retired IDs (merged; numbers are never reused): SET-16 into SET-09; SET-22 into SET-17; SET-24 and SET-34 into SET-20; SET-30 and SET-32 into SET-26; SET-33 (persistence is SET-06 and UI-13); SET-44 into SET-04.

## Notes from the draft

### Not requirements

Evidence rows that belong elsewhere, by reason:

- **Belongs to theme.md (pixels, colors, dimensions):** S19-53, S21-10, S31-17, S38-19, S43-02, S44-20.
- **Settings grouping, headings and form markup (SET-06 owns organization):** S19-49, S19-52, S22-02, S37-24, S64-11, S66-06, S66-07, S66-08, S66-09, S67-29, S67-30, S67-31, S67-32.
- **Control state, callbacks and feedback reset (UI mechanics; the check and update outcomes are above):** S38-09, S40-07, S43-01, S43-03, S44-19, S46-04, S46-28, S47-06, S59-23.
- **Add/remove-row controls and notice dismissal (shared UI; UI-02 governs layers):** S67-19, S67-21, S67-23, S67-28.
- **Settings/Configure navigation and dialogs (SET-05, SET-06, UI-01, UI-02):** S80-01 to S80-11, S81-01, S81-02, S81-04, S81-06.
- **Shared security or validation:** S15-07 (change-security token, account security), S31-10 (section-key validation, shared UI).
- **Failure markers, not coverage:** S23-14, S23-15.
- **Saving persists the choice (SET-06, UI-13):** S38-17, S38-18.

### Coverage

All 165 settings-candidate evidence rows are in a requirement above or in the list above.
