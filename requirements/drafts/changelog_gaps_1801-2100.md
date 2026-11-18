# DRAFT CHANGELOG behavior gaps: lines 1801–2100

Candidate gaps only. CHANGELOG and requirement comparison are pinned at
`c3c0598ea7aab4f0bf586969d1bd2dcb12df0107`. Compared user-visible claims against statement rows in `requirements/*.md` and
`requirements/drafts/*.md`, including deployment/documentation and current Developer decisions.
Existing planned/proposed statements count as coverage; prior gap reports and excluded evidence do not.
Closest IDs identify partial coverage, not new requirements or approved behavior.

This range begins inside 0.1.18 and ends inside 0.1.0's Changed section. The next chunk continues that
release. Superseded setup locations, pin/outside-click behavior, public-address reset defaults, tag-color
layout and single-account arrangements are historical alternatives, not current guarantees.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L1817](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1817) | 0.1.18 | The chosen upload file name is displayed by the custom file field. Generic source import does not specify filename feedback. | SRC-41 | shared UI / sources |
| [L1835](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1835) | 0.1.16 | Changing the display time zone affects this page only; Google/server retain the configured zone. FED-03 covers feeds and CAL-19 preserves event zones but the full server/Google isolation is not explicit. | CAL-19, CAL-25, FED-03 | calendar / google |
| [L1837](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1837) | 0.1.16 | Typed event times accept 9:30, 9:30pm, 21:30 and 930, and suggestions appear every fifteen minutes. EVT-10/12 cover other samples and duration suggestions, not the complete accepted forms/list interval. | EVT-10, EVT-12 | events / shared UI |
| [L1839](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1839) | 0.1.16 | Event durations are preserved in real elapsed hours across different start/end zones. EVT-11/13 cover duration moves and separate zones without expressly defining elapsed-time semantics. | EVT-11, EVT-13 | events |
| [L1863](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1863) | 0.1.15 | Instant Google notices reconcile changes within seconds rather than waiting for a daily full check; otherwise the daily check continues. Earlier one-way overwrite policy is later superseded for two-way modules. | GGL-41, GGL-59, DEP-08 | google |
| [L1864](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1864) | 0.1.15 | Watch registration is renewed weekly and refused registration retried after exactly six hours. GGL-38/42/43 record lifetime and samples but leave renewal/retry thresholds open. | GGL-38, GGL-42 (?), GGL-43 (?) | google |
| [L1901](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1901) | 0.1.12 | Subscription guidance explains that Google can delay reads up to twelve hours and retain its initially read calendar name, unlike direct synchronization. FED-01’s generic instructions do not require these caveats. | FED-01, GGL-30 | feeds / documentation |
| [L1908](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1908) | 0.1.11 | Automatic clock mode uses 24-hour time for non-English languages and applies to event details, activity and editor as well as calendar. CAL-20 states English automatic behavior only. | CAL-20, CAL-21, EVT-10 | calendar / shell |
| [L1915](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1915) | 0.1.11 | Editing an event’s end establishes the duration used for subsequent start changes. EVT-11 preserves duration on start movement but does not state how manual end changes update that remembered duration. | EVT-11 | events |
| [L1931](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1931) | 0.1.10 | Setup guidance automatically opens for missing credentials or failed/blocked/paused source updates and closes after success. SRC-12/UI-05 do not specify every needs-attention trigger. | SRC-12, UI-05 | sources / shared UI |
| [L1945](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1945) | 0.1.9 | The footer’s Report/Suggest links open issue forms populated with the running version. Existing documentation and copy-log requirements do not define these app links/prefill. | SHL-11, DIA-01 | diagnostics / shell |
| [L1953](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1953) | 0.1.9 | Installer reruns offer the actual current settings as prompt defaults, including confirming the data path. DEP-05 preserves settings without explicitly specifying defaults shown to the user. | DEP-03, DEP-05 | deployment |
| [L1977](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1977) | 0.1.8 | The first-visit page offers a copyable, service-name-independent command to find the setup code, and wrong-code guidance repeats that command. ACC-03 requires a code but does not define obtaining it. | ACC-03, DEP-05 | account / documentation |
| [L1988](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L1988) | 0.1.7 | Installer treats latest and stable as equivalent stable-release choices. Channel selection is covered without the command-input alias. | DEP-03, SET-18 | deployment |
| [L2005](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L2005) | 0.1.5 | Language selection is saved durably and covers every screen/guide/error/month/day string, including Brazilian Portuguese. SHL-04/05 cover selected samples but not the blanket completeness or regional-language promise. | SHL-04, SHL-05 | shell |
| [L2011](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L2011) | 0.1.5 | Browser form errors show a localized error page with Go back, while API-style errors remain JSON. SHL-06/10 omit the browser error-page navigation contract. | SHL-06, SHL-10 | shell / shared UI |
| [L2053](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L2053) | 0.1.3 | Legacy page/CCS+ secret-file imports run once, so later restarts cannot overwrite changed stored credentials from lingering old files. Import content is specified without an explicit once-only guarantee. | ACC-01, SRC-06 | account / sources |
| [L2058](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L2058) | 0.1.3 | DB_PASSWORD supplies the encryption key for stored CCS+/Google secrets. Secret protection and changed-password errors do not fully define key derivation/credential portability. | SRC-07, GGL-07, GGL-22, DEP-12 (?) | shared security / deployment |
| [L2067](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L2067) | 0.1.2 | This page fills the public-address field from the current request. SET-16 covers initial setup prefilling, not the reusable Settings action. Historical Reset-to-environment is superseded by once-only import/clearing. | SET-16, SET-08 | settings / shared UI |
| [L2090](https://github.com/Uuugh/CalendarStream/blob/c3c0598ea7aab4f0bf586969d1bd2dcb12df0107/CHANGELOG.md#L2090) | 0.1.0 | Source intervals are bounded above at 1,440 minutes as well as below at fifteen. SRC-04 states only the minimum and SHL-06 translated guidance is not a validation rule. | SRC-04, SHL-06 | sources |

## Coverage and exclusions

- 0.1.18: UI-05/07, SRC-12/24/31, FED-02 and SET-06 cover sections, help, source setup/sync and read
  status. Chosen-filename feedback remains above. Old Google-on-dashboard, tag-color folds, legend rows,
  icons, spacing and typography are superseded or theme-only.
- 0.1.17: SRC-13 and SRC-31 cover CCS+ guidance and sync; spelling/placement and package-release renaming
  do not establish additional app behavior requirements.
- 0.1.16: CAL-19..25, EVT-10..13, ACC-07 and FED-02 cover zone/clock/editor/login/read basics.
  Page-only zone isolation, accepted time forms/list intervals and real-duration semantics remain qualifiers.
  Old time-format Settings location/hour-menu replacement and field arrangement are historical/theme.
- 0.1.15: GGL-38..44, DEP-08 and CAL-21/27 cover watch lifecycle, HTTPS, month selection and clock choice.
  Precise latency/daily cadence and renewal/retry times remain open; old unconditional overwrite behavior is
  only applicable to one-way after two-way was introduced. Field/block geometry is theme.
- 0.1.14/13: login/client box arrangements and Tag Colors placement are later superseded and visual, not
  new current functionality.
- 0.1.12: provider subscription delay/name guidance remains above; client form row layout is theme/history.
- 0.1.11: EVT-10/11/13/16/17 and CAL-20/21 cover clock, duration, zones and event colors. Generic automatic
  non-English formatting and end-edit duration semantics remain unspecified. Old hour-menu, client-fold and
  button-position descriptions are superseded visual arrangements.
- 0.1.10: SRC-13, EVT-04 and GGL-30 cover setup help, day creation and calendar renaming. Auto-expansion
  triggers remain above; explanatory label position/old checklist layout are theme.
- 0.1.9: DEP-02/03/05, SRC-11/12, EVT-04, FED-01 and GGL-30 cover install hosts/defaults, setup and core
  subscription/navigation. Actual rerun prompt defaults and report links remain qualifiers. Installer-set
  public address, pinned-event outside-click and older dashboard/account layouts were later replaced.
- 0.1.8: setup-code command/copy guidance remains above, beyond requiring a correct code.
- 0.1.7/6: DEP-03/05 and SET-18 cover release choice/preservation; stable/latest alias is not explicit.
  README editorial changes are documentation, not app behavior gaps.
- 0.1.5: SHL-04..10 and DEP-03/05 cover localization and persistent install basics. Table rows isolate
  completeness, localized browser-error navigation and once-only import guarantees. The old data-path default/
  ask-once wording is later superseded; shortening the title is presentation.
- 0.1.4: DEP-03/05 cover one-command install, download, password/start/setup code and configurable paths;
  no duplicate deployment gap is inferred from historical defaults. README length is not app behavior.
- 0.1.3: ACC-01..09 and SRC-06/07/12 cover initial login/change/import/protected CCS+ credentials; the
  once-only import and explicit database-key contract remain above. Mount/file cleanup is implementation
  supporting those behaviors, not an additional user rule.
- 0.1.2: SET-08..13/16 cover address use, import, normalization and missing guidance. A reusable This page
  action is not specified; old Reset-to-environment and mandatory-MNT requirements are superseded.
- 0.1.1: image/repository namespace migration and published-tag copying are release compatibility context,
  not a new app behavior requirement.
- 0.1.0 partial: SRC-02..04 and GGL-37/46 cover interval saving/scheduling and accepted/rejected/unreachable
  client checks. Exact interval upper bound remains above. Remaining Changed items continue at line 2101.

Claude confirms gap validity/ownership. No existing file, README, CHANGELOG or source code was changed.
No application suites were run locally for this documentation comparison.
