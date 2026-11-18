# Settings gap triage

DRAFT — proposed, not approved. Task E; sources and requirement statements compared at 7d20930563e29c090ed7a5ed5d76de8b180cdf34.

All ten rows whose first proposed owner is settings are assigned once below. For compound owners, settings owns this triage; the later named features must not duplicate it. Existing approved, planned and proposed statements count as coverage. Gap reports themselves do not.

| gap (file and line) | outcome | ID or decision | proposed requirement or reason |
|---|---|---|---|
| [readme_gaps.md:77](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/readme_gaps.md#L77) | New | SET-49 | Reload timing is part of update completion, not general dialog mechanics. SET-37 remains the broader progress rule. The trailing Google removal wording belongs to existing GGL-08; it adds no settings proposal. |
| [changelog_gaps_1-300.md:15](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1-300.md#L15) | New | SET-50 | Extend saved-state freshness to update-check frequency; SET-46 already covers auto-update. |
| [changelog_gaps_1-300.md:18](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1-300.md#L18) | New | SET-51 | Extend refused-save behavior to frequency; SET-46 already covers auto-update. |
| [changelog_gaps_1-300.md:24](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1-300.md#L24) | Covered | UI-13, SET-04, GGL-46 | Immediate presentation of changed settings follows UI-13; the callback warning and stale Google feedback are already owned by SET-04 and GGL-46. |
| [changelog_gaps_1201-1500.md:35](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1201-1500.md#L35) | New | SET-52 | Describe an accepted update action failing to reach its updater, rather than duplicating token rejection in SET-29. |
| [changelog_gaps_1501-1800.md:34](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1501-1800.md#L34) | New | SET-53 | Resolve the notification-suppression behavior left open by SET-25; History is the output, not a second owner. |
| [changelog_gaps_1801-2100.md:33](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1801-2100.md#L33) | New | SET-54 | The reusable public-address suggestion is additional to initial setup SET-16. The old environment reset is superseded by SET-08 and SET-13. |
| [changelog_gaps_301-600.md:41](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_301-600.md#L41) | New | SET-49, SET-55, SET-56 | Reuse the same completion delay as the README row; additionally capture cross-page update observation and due-time scheduling. SET-22 retains its separate interval-boundary question. |
| [changelog_gaps_901-1200.md:23](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_901-1200.md#L23) | New | SET-57 | Preserve the settings context across update completion; shared dialog mechanics remain UI-01/UI-02. |
| [changelog_gaps_901-1200.md:31](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_901-1200.md#L31) | Covered | SET-26 | Installer guidance when the updater is unavailable already supplies the manual update route. A separate version-specific action is presentation detail, not another behavior requirement. |

## Proposed requirements

| ID | status | statement | gap row |
|---|---|---|---|
| SET-49 | proposed | Every open page refreshes fifteen seconds after an app update enters Restarting. | [readme_gaps.md:77](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/readme_gaps.md#L77) |
| SET-50 | proposed | Reopening Updates shows the current saved update-check frequency, including changes made by another client. | [changelog_gaps_1-300.md:15](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1-300.md#L15) |
| SET-51 | proposed | A refused update-check frequency change leaves the prior saved frequency in effect and shows that effective value. | [changelog_gaps_1-300.md:18](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1-300.md#L18) |
| SET-52 | proposed | An update that cannot reach the updater reports Update failed and the cause. | [changelog_gaps_1201-1500.md:35](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1201-1500.md#L35) |
| SET-53 | proposed | Repeated update checks announce an available version in History once for that version. | [changelog_gaps_1501-1800.md:34](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1501-1800.md#L34) |
| SET-54 | proposed | Public-address settings can fill the address from the request used to open the page. | [changelog_gaps_1801-2100.md:33](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_1801-2100.md#L33) |
| SET-55 | proposed | Every open page shows an app update in progress, including an update started from another page. | [changelog_gaps_301-600.md:41](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_301-600.md#L41) |
| SET-56 | proposed | Automatic update checks run when the selected checking interval becomes due. | [changelog_gaps_301-600.md:41](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_301-600.md#L41) |
| SET-57 | proposed | After an update completes, the page uses the new release assets and preserves the open Settings context. | [changelog_gaps_901-1200.md:23](https://github.com/Uuugh/CalendarStream/blob/7d20930563e29c090ed7a5ed5d76de8b180cdf34/requirements/drafts/changelog_gaps_901-1200.md#L23) |

## Coverage and questions

Ten owned gap rows: eight New outcomes and two Covered outcomes; nine distinct proposed requirements, SET-49–SET-57, after existing SET-48. The cross-page update row also supports SET-49. No additional common UI rule is introduced. Historical environment-reset and Google-removal fragments are accounted for in their outcomes rather than revived. SET-22 and SET-37 remain existing broader questions; the explicit historical fifteen-second claim is proposed for review here. No application suites were run locally for this documentation-only change.
