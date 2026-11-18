# Search gap triage

DRAFT — proposed, not approved. Task E comparison pinned to 459df21936152b337d866b9f214361592c66f141.

All nine input reports (README and eight CHANGELOG chunks) were checked. **Zero rows name search as their first proposed owner.** No new requirement or ID is proposed. Existing SRH-01–SRH-09 were read.

| gap (file and line) | outcome | ID or decision | proposed requirement or reason |
|---|---|---|---|

The empty table represents an empty owned-row set. Ownership stays with the original first owner even where a Developer decision later moved behavior to another feature. These cross-owner notes must not produce duplicate outcomes:

- [readme_gaps.md:48](https://github.com/Uuugh/CalendarStream/blob/459df21936152b337d866b9f214361592c66f141/requirements/drafts/readme_gaps.md#L48): Historical calendar search matching and day grouping: first owner calendar. The Calendar triage assigns Superseded, referencing global Search SRH-01, SRH-04 and SRH-08. Current results group by feature and populate live under SRH-09.
- [readme_gaps.md:49](https://github.com/Uuugh/CalendarStream/blob/459df21936152b337d866b9f214361592c66f141/requirements/drafts/readme_gaps.md#L49): Historical one-year search bounds: first owner calendar. The Calendar triage assigns Superseded; current SRH-03 owns date constraints and SRH-06 the unlimited forward search promise.
- [changelog_gaps_901-1200.md:14](https://github.com/Uuugh/CalendarStream/blob/459df21936152b337d866b9f214361592c66f141/requirements/drafts/changelog_gaps_901-1200.md#L14): Repeated calendar-search matching claim: first owner calendar, already reconciled by the Calendar triage.
- [changelog_gaps_901-1200.md:15](https://github.com/Uuugh/CalendarStream/blob/459df21936152b337d866b9f214361592c66f141/requirements/drafts/changelog_gaps_901-1200.md#L15): Repeated historical default search-window claim: first owner calendar, already reconciled by the Calendar triage.

## Coverage and validation

Exact first-owner filtering found zero rows across all nine reports; all cross-owner anchors and Markdown were checked. No IDs are allocated or reused. This report does not treat gap claims or evidence mappings as requirements and does not modify the current feature/common rules. No application suites were run locally for this documentation-only report.
