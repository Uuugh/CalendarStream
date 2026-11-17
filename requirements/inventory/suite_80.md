# Suite 80: Full-page Settings markup

Source: [`tests/suite_80.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres-backed HTTPS TestClient and patched source/Google/update loops. Compares normal/full-mode rendered Settings markup and form IDs; restores full mode afterward. No browser despite slide-out/dialog labels.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S80-01 | settings | Normal Settings markup has no slide-out class or shared Configure popup ID. | [L28](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L28) |
| S80-02 | settings | Normal markup has page-login/domain forms and exactly one login-form ID. | [L29](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L29) |
| S80-03 | settings | After enabling full mode, Settings markup has the settingsnav menu class. | [L34](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L34) |
| S80-04 | settings | The full-page navigation includes each of Configure, User and Site Admin group labels. | [L36](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L36) |
| S80-05 | settings | Each of five Configure keys has a data-configure navigation marker. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L38) |
| S80-06 | settings | Each of five setting keys has a data-setting navigation marker. | [L40](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L40) |
| S80-07 | settings | Each of those setting keys has its own setting-dialog ID. | [L41](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L41) |
| S80-08 | settings | The shared Configure popup and body IDs exist. | [L42](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L42) |
| S80-09 | settings | Login, Domains and Theme form IDs each occur exactly once. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L44) |
| S80-10 | settings | The full-page markup contains username/main-address/logo field names. | [L45](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L45) |
| S80-11 | settings | The sampled pre-sections substring has no sortable text, or the sections marker is absent. | [L47](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_80.py#L47) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Navigation-marker rows repeat over three/five labels. Markup IDs do not prove sections move correctly or dialogs open; suite 81 separately tests those paths.
- Row 10 only checks field names exist, not exact layout equivalence. Row 11 can pass if the sections marker is absent and is not independent evidence in that branch.
- The historical docstring downplays the database, but the suite imports the full app with Postgres-backed settings.
- Overlaps: suite 81 browser Settings; suites 64/67 normal Settings forms/order.
