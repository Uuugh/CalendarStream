# DRAFT gap triage: deployment

Not approved. Task E comparison at `d9ea06c9b4f288064b2bf9443fad33d01a40064a`. This file triages every README/CHANGELOG gap whose
first proposed owner is deployment. Where a row also names account, settings, security or shared data,
deployment takes the complete row for this pass under the queue's first-owner rule; the other feature
must not duplicate it. Gap reports are candidates, not authority to add behavior beyond their evidence.

DEP-01..13 in the deployment draft and DEP-14 in the approved-path file were checked. New IDs start
DEP-15 and remain proposed. Existing questions count as Covered statements, not answered questions.
No existing requirement, common file, gap report or source is edited. These installer/data behaviors do
not introduce feature-specific widget mechanics or exceptions to TIM/UI/CAP. No new common rule is needed.

## Outcomes

| gap (file and line) | outcome | ID or decision | proposed requirement or reason |
|---|---|---|---|
| [changelog_gaps_1-300.md:L29](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_1-300.md#L29) (source L259) | New | DEP-15 | DEP-03 covers prompts/defaults but not numbered-name/alternate-path/cancel handling for an occupied app folder. |
| [changelog_gaps_1501-1800.md:L16](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_1501-1800.md#L16) (source L1513) | New | DEP-16 | DEP-03 covers channels; exact beta-version selection is an additional accepted installer input. |
| [changelog_gaps_1501-1800.md:L32](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_1501-1800.md#L32) (source L1714) | New | DEP-17 | DEP-02 promises macOS support; a failed host-address lookup still needs an explicit user-visible failure/recovery rule. |
| [changelog_gaps_1501-1800.md:L38](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_1501-1800.md#L38) (source L1770) | New | DEP-18, DEP-19 | Owner-readable environment output and lossless special-character storage are separate uncovered guarantees. |
| [changelog_gaps_1801-2100.md:L26](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_1801-2100.md#L26) (source L1953) | New | DEP-20 | DEP-05 preserves configuration but does not define the defaults offered by rerun prompts. |
| [changelog_gaps_1801-2100.md:L28](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_1801-2100.md#L28) (source L1988) | New | DEP-21 | The stable/latest installer-input alias is not stated in DEP-03. |
| [changelog_gaps_2101-2336.md:L32](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_2101-2336.md#L32) (source L2273) | New | DEP-22 | DEP-09 is about installer reruns, not image refresh during direct deployment startup/recreation. |
| [changelog_gaps_2101-2336.md:L36](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_2101-2336.md#L36) (source L2304) | New | DEP-23 | DEP-02 host support does not explicitly specify amd64/arm64 prebuilt images. |
| [changelog_gaps_301-600.md:L33](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_301-600.md#L33) (source L389) | New | DEP-24 | DEP-04 covers second-install names/ports; the missing qualifier is updater enabled by default on a new install. The obsolete stack-folder default is not proposed. |
| [changelog_gaps_601-900.md:L24](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_601-900.md#L24) (source L678) | New | DEP-25 | DEP-05 downloads deployment files but does not guarantee that an exact selected release supplies its matching deployment definition. |
| [changelog_gaps_901-1200.md:L29](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/changelog_gaps_901-1200.md#L29) (source L1118) | New | DEP-26 (?) | DEP-05 starts the stack, but database-readiness retry/recovery is unspecified; retry budget remains a real question. |
| [readme_gaps.md:L23](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L23) (source L94) | Covered | DEP-02 | Already lists Linux, macOS Docker Desktop and Windows WSL. |
| [readme_gaps.md:L24](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L24) (source L103) | New | DEP-15 | DEP-03 covers prompt categories and defaults. The remaining occupied-folder alternatives are the same new rule as CHANGELOG L259, not a second requirement. |
| [readme_gaps.md:L25](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L25) (source L114) | Covered | DEP-04 | Already requires independent names/ports and saved allocation. |
| [readme_gaps.md:L26](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L26) (source L119) | Covered | DEP-05 | Already requires generated credentials, deployment download/start, printed address/setup code and preserved rerun settings/password. |
| [readme_gaps.md:L29](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L29) (source L153) | Covered | DEP-06 | Already applies configured user/group identity and restart policy. |
| [readme_gaps.md:L88](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L88) (source L490) | Covered | DEP-09 | Already installs the newest selected release while keeping settings. |
| [readme_gaps.md:L89](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L89) (source L500) | Covered | DEP-10 (?) | The whole updater/database/cleanup claim and its auto-update conflict are already proposed as an open question. This triage does not answer or duplicate it. |
| [readme_gaps.md:L90](https://github.com/Uuugh/CalendarStream/blob/d9ea06c9b4f288064b2bf9443fad33d01a40064a/requirements/drafts/readme_gaps.md#L90) (source L502) | Covered | DEP-11 | Already requires Docker-network isolation, generated token/socket access and removable updater with other data preserved. |

## Proposed requirements

| ID | status | statement | gap row |
|---|---|---|---|
| DEP-15 | proposed | When the chosen app folder already exists, the installer offers using it, choosing a numbered folder, choosing another path or cancelling. | [changelog_gaps_1-300.md:L29](changelog_gaps_1-300.md#L29), [readme_gaps.md:L24](readme_gaps.md#L24) |
| DEP-16 | proposed | The installer accepts an exact beta release identifier as the requested version. | [changelog_gaps_1501-1800.md:L16](changelog_gaps_1501-1800.md#L16) |
| DEP-17 | proposed | Host-address lookup failures are reported to the user rather than silently terminating installation. | [changelog_gaps_1501-1800.md:L32](changelog_gaps_1501-1800.md#L32) |
| DEP-18 | proposed | The installer writes the environment configuration with read access restricted to its owner. | [changelog_gaps_1501-1800.md:L38](changelog_gaps_1501-1800.md#L38) |
| DEP-19 | proposed | Installer answers containing pipe or ampersand characters are preserved literally in the saved configuration. | [changelog_gaps_1501-1800.md:L38](changelog_gaps_1501-1800.md#L38) |
| DEP-20 | proposed | On a rerun, installer questions offer the current saved settings as their defaults, including the data folder. | [changelog_gaps_1801-2100.md:L26](changelog_gaps_1801-2100.md#L26) |
| DEP-21 | proposed | The installer accepts stable and latest as names for the stable release channel. | [changelog_gaps_1801-2100.md:L28](changelog_gaps_1801-2100.md#L28) |
| DEP-22 | proposed | Starting or recreating the app deployment checks the selected image tag for an updated image before starting the app. | [changelog_gaps_2101-2336.md:L32](changelog_gaps_2101-2336.md#L32) |
| DEP-23 | proposed | Prebuilt app images run on amd64 and arm64 hosts without building the app locally. | [changelog_gaps_2101-2336.md:L36](changelog_gaps_2101-2336.md#L36) |
| DEP-24 | proposed | A new installation defaults to enabling the optional updater. | [changelog_gaps_301-600.md:L33](changelog_gaps_301-600.md#L33) |
| DEP-25 | proposed | Installing an exact release uses that release’s matching deployment definition. | [changelog_gaps_601-900.md:L24](changelog_gaps_601-900.md#L24) |
| DEP-26 | proposed (?) | Startup retries establishing a database connection while the database is not ready. What retry budget and terminal failure behavior should be required? | [changelog_gaps_901-1200.md:L29](changelog_gaps_901-1200.md#L29) |

## Coverage and remaining questions

All 19 deployment-first gap rows have exactly one outcome: 7 Covered and
12 New, yielding 12 distinct proposed rules after duplicate grouping.
No row in this owner set requires Superseded or Not a requirement. Historical defaults embedded in compound
rows are explained rather than promoted. DEP-10's updater policy and DEP-12's restore scope stay open in
their original rows; DEP-26 explicitly leaves the database startup retry budget for Developer review.
This is statement/evidence reconciliation, not implementation or runtime verification; no suites were run.
