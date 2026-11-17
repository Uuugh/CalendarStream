# Suite 69: Google shared errors, enums and immutable decision

Source: [`tests/suite_69.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure imports and object checks; no app, database or network operation. The accepted database argument is unused. Exception subclasses/enums/recovery decision and facade identity are compared directly.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S69-01 | google | AccessRevoked, CalendarMissing and Conflict subclass GoogleError. | [L13](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L13) |
| S69-02 | google | GoogleError preserves its supplied message string. | [L14](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L14) |
| S69-03 | google | The HealthState value set equals the five expected saved strings. | [L15](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L15) |
| S69-04 | google | Constructing paused yields the enum member and healthy compares equal to its string. | [L16](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L16) |
| S69-05 | google | FailureKind has exactly the nine expected saved strings. | [L17](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L17) |
| S69-06 | google | A RecoveryDecision keeps retry/state and defaults retry_after_seconds to zero. | [L20](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L20) |
| S69-07 | google | Failure sentinel: mutating the frozen decision without any exception fails. | [L22](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L22) |
| S69-08 | google | A caught exception after the mutation attempt reaches an unconditional success marker. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L24) |
| S69-09 | google | The gsync facade exposes identical Google error class objects. | [L26](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_69.py#L26) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 07/08 pair a failure sentinel with a broad exception-handler ok(True) marker. Any exception counts, not a specific frozen-dataclass exception; the marker is not standalone verification.
- Enum/value and facade identity checks are implementation/compatibility contracts rather than end-user feature requirements. No health transition behavior is exercised.
- Overlaps: suite 70 API facade; suite 71 readiness stage values; suite 68 health integration.
