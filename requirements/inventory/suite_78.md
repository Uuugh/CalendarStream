# Suite 78: CSS guard failure branches

Source: [`tests/suite_78.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_78.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

No ok()/unittest assertions or direct assert statements. Imports tests/tools/csscheck.py, checks repository findings, then constructs duplicate/late-owner and valid print-media CSS fixtures in a temporary directory. Three explicit if/exit-one guards are the evidence rows. No app/database.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S78-01 | process | The repository's initial CSS ownership/duplicate check must produce no findings or the suite exits one. | [L12](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_78.py#L12) |
| S78-02 | process | The temporary duplicate/late-owner fixture must produce exactly three findings or the suite exits one. | [L20](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_78.py#L20) |
| S78-03 | process | The temporary base-plus-print-media fixture must produce no findings or the suite exits one. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_78.py#L24) |

## Direct assertions

No direct Python `assert` statements. See the setup section for the unittest/failure-guard evidence units.

## Coverage limits and reconciliation notes

- These rows map explicit failure guards, not ok() call sites. The duplicate fixture only asserts finding count three, not each finding's exact kind/message; valid media fixture proves the sampled override is accepted.
- The guard covers consolidated-component rules implemented by csscheck, not all CSS correctness or rendered appearance.
- Overlaps: suites 35/44 rendered theme; suite 75 process checks.
