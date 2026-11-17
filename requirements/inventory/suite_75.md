# Suite 75: Dependency-map freshness and Google module headers

Source: [`tests/suite_75.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_75.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Runs tests/tools/deps.py --check as a subprocess and reads app/google Python source headers, skipping __init__.py. No app/database/network. This is process/structure evidence.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S75-01 | process | Running deps.py --check returns zero for the tracked dependency map. | [L11](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_75.py#L11) |
| S75-02 | process | Each non-init Python file in app/google has all five required header-label strings in its first triple-quoted section. | [L18](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_75.py#L18) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 02 repeats once per non-init Google file at runtime; call-site counts are not file counts. Header checks only search five label strings in the first triple-quoted segment, not truth/completeness of documented dependencies.
- The dependency tool exit result is meaningful freshness evidence but not a full architecture review.
- Overlaps: suite 77 AST/header boundaries across more folders.
