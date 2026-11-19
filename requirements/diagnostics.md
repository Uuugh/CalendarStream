# Requirements: diagnostics

Status, Report a problem, health, debug captures, the container log. Issues against this feature: none open on the

Dashboard.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| DIA-01 | proposed | The user can get the information needed to diagnose a problem. | — | — |
| DIA-01.a | proposed | Container log exposes the most recent log lines of the running app (the number in DEF-01), retrievable as plain text and copyable (DIA-01). | — | readme_gaps:72, changelog_gaps_601-900:34 |
| DIA-01.b | built | A Copy log button next to Container log copies the container log straight to the clipboard, with no new tab and no manual select-all. | — | F64.1 |
| DIA-01.c | proposed | Per-source Activity provides diagnostic details for the last download and makes the last received calendar file available for diagnosis. | — | changelog_gaps_1501-1800:21, changelog_gaps_2101-2336:26, changelog_gaps_1501-1800:21 |
| DIA-02 | proposed | The user can report a problem or suggest a feature, with a report they control. | — | — |
| DIA-02.a | proposed | The page offers Report a problem and Suggest a feature, allowing the user to describe a problem or idea; the report or suggestion is prefilled with the running CalendarStream version. | — | readme_gaps:78, changelog_gaps_1201-1500:32, changelog_gaps_1801-2100:25, changelog_gaps_1801-2100:25 |
| DIA-02.b | proposed | The user chooses independently whether a report includes History, each source’s last-download details, device and setup details, contact details and reply preference. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-02.c | proposed | Report preparation redacts private identifiers: usernames, links, stream names, email addresses and the public address; secret protection also follows ACC-05. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-02.d | proposed | Before sharing a report, the user can preview exactly the report content to be shared. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-02.e | proposed | A prepared report can be sent as a prefilled GitHub issue, copied, or downloaded as a file; copying and downloading need no GitHub account. | — | readme_gaps:78, changelog_gaps_1201-1500:32, readme_gaps:78, changelog_gaps_1201-1500:32, readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-03 | proposed | Monitoring programs can read the app's status and health. | — | — |
| DIA-03.a | proposed | CalendarStream provides a status monitoring interface (GET /api/status) that identifies every connection and includes its synchronization status; access follows ACC-02. | — | readme_gaps:79, changelog_gaps_1501-1800:26 |
| DIA-03.b | proposed | CalendarStream provides a health monitoring interface (GET /healthz) that does not disclose database details; access follows ACC-01. | — | readme_gaps:79, changelog_gaps_1501-1800:36 |
| DIA-04 | proposed | The Product Owner's working files and the Dashboard are served by the app, behind its login. | — | — |
| DIA-04.a | backlog | The Developer's private working files and Good \| Bad verdicts are served by the app itself, behind its login, and are never committed to the repository or published on a public page. | — | Developer, Nov 17 |
| DIA-04.b | backlog | The Dashboard is a live web page built from the GitHub issues and `requirements/*.md`; it is made after the port is complete. | — | Developer, Nov 17 |
| DIA-04.c | backlog | The Dashboard shows testing progress: the current and recent test runs, each shard's state, and pass or fail per requirement. | — | Developer, Nov 17 |

