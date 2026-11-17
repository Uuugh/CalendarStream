# Suite 74: Sync helpers and facade composition

Source: [`tests/suite_74.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure imports, facade objects with None collaborators and local helper values; no app/database/network operation. The facade write-limit constant is temporarily overridden/restored. Database argument unused.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S74-01 | google | The gsync facade exports identical event/body/window/result/color helper objects from sync. | [L12](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L12) |
| S74-02 | google | Facade Google directly inherits GoogleApi and is not a GoogleSync subclass. | [L16](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L16) |
| S74-03 | google | The API facade holds a GoogleSync instance whose api_client refers back to it. | [L18](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L18) |
| S74-04 | google | The sampled event ID is repeatable, differs for another UID and is alphanumeric. | [L20](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L20) |
| S74-05 | google | The two sampled event/calendar colors map to expected Google IDs. | [L21](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L21) |
| S74-06 | google | in_window is non-None and google_fields is callable. | [L22](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L22) |
| S74-07 | google | A fresh SyncResult is unchanged and produces a string summary. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L24) |
| S74-08 | google | Setting gsync.MAX_WRITES to seven makes a new facade instance expose seven. | [L27](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L27) |
| S74-09 | google | GoogleSync's class default write limit is 1500. | [L30](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_74.py#L30) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Stable/distinct event IDs are checked for two sample strings, not collision-freedom globally. Row 06 establishes presence/callability only, not window filtering or field conversion behavior.
- Composition/object-identity checks are compatibility/structure evidence rather than end-user requirements. The write-limit override tests object exposure, not a sync actually constrained to seven writes.
- Overlaps: suites 69/70 facade identity; suite 53 actual write-limit behavior.
