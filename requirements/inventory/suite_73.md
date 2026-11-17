# Suite 73: Google account health with a fake clock

Source: [`tests/suite_73.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Dictionary storage and mutable numeric clock; no app/database/network. Injected errors and explicit time changes exercise recorded state, retry permission, reset and truncation. Database argument unused.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S73-01 | google | A new account is healthy and may sync. | [L19](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L19) |
| S73-02 | google | A 503 decision records degraded/transient, attempt one and next_retry=1005 on the fake clock. | [L22](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L22) |
| S73-03 | google | The account may not sync during that initial backoff. | [L23](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L23) |
| S73-04 | google | Moving the clock to 1006 permits sync. | [L25](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L25) |
| S73-05 | google | A repeated 503 records attempt two and a ten-second later retry. | [L27](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L27) |
| S73-06 | google | Changing to rate-limit resets attempts and records the 120-second Retry-After. | [L29](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L29) |
| S73-07 | google | record_success restores healthy/sync-permitted state and zero attempts. | [L31](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L31) |
| S73-08 | google | Revoked consent on another account returns no-retry/reauth-required but is not timer-blocked by may_sync. | [L33](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L33) |
| S73-09 | google | The first account remains healthy after that other-account failure. | [L34](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L34) |
| S73-10 | google | A missing calendar marks the second account paused. | [L36](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L36) |
| S73-11 | google | Explicit reset makes it healthy and removes its stored health entry. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L38) |
| S73-12 | google | Coverage gap: the storage-token predicate has or True and cannot fail. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L39) |
| S73-13 | google | Recording a thousand-character error truncates saved last_error to exactly 300 characters. | [L41](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_73.py#L41) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 12 is unconditionally true because of or True; it proves neither token exclusion nor the text-length claim. Row 13 independently checks length 300 for one long error.
- Reset is called directly, not via an actual new sign-in. The missing-calendar case checks the affected account's state without reasserting other-account state afterward.
- Fake time samples before/after retry, not every exact boundary; policy/health behavior uses dictionary storage instead of database persistence.
- Overlaps: suite 72 decisions; suite 68 injected integration failures.
