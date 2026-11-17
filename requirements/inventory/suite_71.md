# Suite 71: Google readiness stages

Source: [`tests/suite_71.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure Readiness.of calls with configured/authorized/error/last_sync fixture values; no app/database/network. The database argument is unused. A default synced New York-style timestamp is overridden for individual scenarios.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S71-01 | google | Without a configured client, readiness is NO_CLIENT for the sampled unconfigured/unauthorized combination. | [L11](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L11) |
| S71-02 | google | An unauthorized configured account is NOT_SIGNED_IN with Connect me guidance. | [L12](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L12) |
| S71-03 | google | An authorized account with an error is API_ERROR and includes the error text. | [L13](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L13) |
| S71-04 | google | An authorized error-free account without last_sync is NOT_SYNCED and not working. | [L14](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L14) |
| S71-05 | google | The default authorized/synced/error-free fixture is SYNCED and working. | [L15](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L15) |
| S71-06 | google | A nonempty error overrides a previous good sync and gives API_ERROR. | [L16](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L16) |
| S71-07 | google | An empty error string is treated as no error and yields SYNCED. | [L17](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_71.py#L17) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- The NO_CLIENT case explicitly sets both configured and authorized false; it does not exhaust every combination implied by the old whatever-else label.
- Working is checked for the SYNCED and NOT_SYNCED samples, not every stage. API error cases are string fixtures, not network/error classification tests.
- These are finite decision-table examples rather than proof of all readiness combinations or UI labels.
- Overlaps: suite 68 integration health; suite 69 state enums; suite 54 status wording.
