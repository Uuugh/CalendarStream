# Suite 76: Traffic retention and serialization

Source: [`tests/suite_76.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_76.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure TrafficLog/TrafficEntry objects with a three-entry buffer and synthetic raw request-body text. No app/database/network. No real token or secret is used.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S76-01 | diagnostics | A new traffic log has no recent entries. | [L12](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_76.py#L12) |
| S76-02 | diagnostics | After five records with maxlen three, recent returns three. | [L16](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_76.py#L16) |
| S76-03 | diagnostics | Those retained entries are newest-first URLs x4,x3,x2. | [L17](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_76.py#L17) |
| S76-04 | diagnostics | Clear empties the recent-entry list. | [L19](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_76.py#L19) |
| S76-05 | diagnostics | Serializing the fixture entry preserves its account, raw fixture request-body text and millisecond duration. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_76.py#L24) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Serialization only asserts account/request_body/ms despite its legacy label saying everything. It does not independently compare every header/response field.
- Raw data preservation is demonstrated with fixture text only; this inventory contains no live credential data.
- Overlaps: suites 53/68 diagnostic traffic routes and authentication.
