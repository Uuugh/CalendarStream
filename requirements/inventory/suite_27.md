# Suite 27: Source configuration and built-in rules

Source: [`tests/suite_27.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; background loops and run_once patched. Demo.ics is extended in memory with a synthetic SCK event spanning nearly 24 hours. The test edits and removes built-in rules around before/after stored event snapshots.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S27-01 | sources | The CCS+ Configure node is present and not marked hidden while setup is needed. | [L19](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L19) |
| S27-02 | sources | Saving credentials with a custom HTTPS site URL returns HTTP 303, stores that URL and configures CCS+ credentials. | [L21](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L21) |
| S27-03 | sources | Saving the sampled plain-HTTP site URL returns HTTP 400. | [L22](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L22) |
| S27-04 | sources | Saving an empty site URL removes the stored calendar_url override. | [L24](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L24) |
| S27-05 | sources | After uploading the fixture, page markup contains a Last synced time in the source status line. | [L28](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L28) |
| S27-06 | sources | After upload, the CCS+ Configure node is marked hidden. | [L29](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L29) |
| S27-07 | sources | The page includes the Expand/Close arrow markup, a good status box and Sync Now text. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L30) |
| S27-08 | rules | The page names Items without an end time and 24-hour events. | [L32](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L32) |
| S27-09 | rules | Changing the first built-in rule to length 120 returns HTTP 303 and saves that exact action. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L38) |
| S27-10 | rules | Deleting the 24-hour rule returns HTTP 303 and leaves one rule. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L39) |
| S27-11 | rules | The seeded SCK event is all-day before the rule removal and timed afterward. | [L42](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L42) |
| S27-12 | rules | Saving the sampled rule with no actions returns HTTP 400. | [L43](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L43) |
| S27-13 | rules | Changing the no-end rule action to allday persists that action target. | [L45](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_27.py#L45) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 04 only checks that the stored URL override is absent, not the effective fallback URL string.
- Rows 05–08 inspect markup/text rather than browser folding interactions or the absence of any other default rules.
- Row 09 checks the saved 120-minute action, not the resulting duration of every missing-end event. Row 13 similarly checks the action target, not rendered all-day event results.
- Row 11 compares the one seeded SCK event's all_day flags; it does not independently compare its exact before/after timestamps.
- Overlaps: suite 21 predefined-rule UI; suite 26 rule/template operations; suite 28 source verification controls.
