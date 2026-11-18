# Requirements: diagnostics

Status, Report a problem, health, debug captures, the container log. Issues against this feature: none open on the
Dashboard.

| ID | status | statement | test | was |
|---|---|---|---|---|
| DIA-01 | built | A Copy log button next to Container log copies the container log straight to the clipboard, with no new tab and no manual select-all. | — | F64.1 |
| DIA-02 |  | The Developer's private working files and Good \| Bad verdicts are served by the app itself, behind its login, and are never committed to the repository or published on a public page. | — | Developer, Nov 17 |
| DIA-03 |  | The Dashboard is a live web page built from the GitHub issues and `requirements/*.md`; it is made after the port is complete. | — | Developer, Nov 17 |
| DIA-04 |  | The Dashboard shows testing progress: the current and recent test runs, each shard's state, and pass or fail per requirement. | — | Developer, Nov 17 |
| DIA-05 | proposed | Container log exposes the running app’s log output since startup, matching its container log; plain-text retrieval and copying follow HIS-14 and DIA-01. | — | readme_gaps:72, changelog_gaps_601-900:34 |
| DIA-06 | proposed | The page offers Report a problem and Suggest a feature, allowing the user to describe a problem or idea. | — | readme_gaps:78, changelog_gaps_1201-1500:32, changelog_gaps_1801-2100:25 |
| DIA-07 | proposed | The user chooses independently whether a report includes History, each source’s last-download details, device and setup details, contact details and reply preference. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-08 | proposed | Report preparation redacts private identifiers: usernames, links, stream names, email addresses and the public address; secret protection also follows ACC-11. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-09 | proposed | Before sharing a report, the user can preview exactly the report content to be shared. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-10 | proposed | A prepared report can open a prefilled GitHub issue. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-11 | proposed | A prepared report can be copied without a GitHub account. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-12 | proposed | A prepared report can be downloaded as a file without a GitHub account. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-13 | proposed | CalendarStream provides a status monitoring interface at GET /api/status; access follows ACC-20. | — | readme_gaps:79 |
| DIA-14 | proposed | CalendarStream provides a health monitoring interface at GET /healthz; access follows ACC-02. | — | readme_gaps:79 |
| DIA-15 | proposed | Per-source Activity provides diagnostic details and captures for the last download. | — | changelog_gaps_1501-1800:21, changelog_gaps_2101-2336:26 |
| DIA-16 | proposed | Per-source Activity makes the last received calendar file available for diagnosis. | — | changelog_gaps_1501-1800:21 |
| DIA-17 | proposed | The status monitoring response identifies every source and destination. | — | changelog_gaps_1501-1800:26 |
| DIA-18 | proposed | Health monitoring responses do not disclose database details. | — | changelog_gaps_1501-1800:36 |
| DIA-19 | proposed | A report or suggestion is prefilled with the running CalendarStream version. | — | changelog_gaps_1801-2100:25 |
