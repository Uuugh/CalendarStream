# Suite 28: Credential save, cancel and verification UI

Source: [`tests/suite_28.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTP server on 8093; Chromium/Playwright at 1100×900 in light mode. Fake download waits 1.2 seconds, returns Demo.ics for accepted fixture passwords and raises AuthError for wrong. Background loops patched. Browser pageerror events are collected.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S28-01 | sources | After fake successful verification, the browser source slot starts in state ok. | [L37](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L37) |
| S28-02 | sources | Typing the source password changes the slot to edit and shows Save and Cancel controls. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L39) |
| S28-03 | sources | Clicking Cancel puts the source slot in cancel state. | [L40](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L40) |
| S28-04 | sources | After the cancellation delay, the slot returns to ok and the typed password is cleared. | [L41](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L41) |
| S28-05 | sources | Clicking Save after editing puts the slot in saving or verifying state. | [L43](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L43) |
| S28-06 | sources | Polling the save control observes Saved text. | [L47](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L47) |
| S28-07 | sources | Polling the slot observes verifying state with Verifying… text. | [L52](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L52) |
| S28-08 | sources | The final polled state is valid and its message contains Validated. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L53) |
| S28-09 | sources | After redraw and reopening Configure if needed, the source slot is again ok. | [L56](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L56) |
| S28-10 | sources | A fake rejected password results in failed state, Failed message and exactly one reason-note element. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L58) |
| S28-11 | sources | Typing the username after rejection changes the slot to edit and removes the reason-note element. | [L59](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L59) |
| S28-12 | account | Typing a new page password shows the Cancel control and current-password field. | [L61](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L61) |
| S28-13 | sources | An async credential save with a malformed username returns HTTP 400 and a JSON detail containing Username. | [L63](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L63) |
| S28-14 | sources | An async verify request with kind=nope returns HTTP 400. | [L65](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L65) |
| S28-15 | shell | No browser pageerror events were collected during the sampled interactions. | [L68](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_28.py#L68) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Save/cancel/verification assertions are observations at fixed sleeps and polling windows; they do not prove exact transition timing or all race conditions.
- Row 10 checks failed state, Failed text and one note node; it does not assert the specific rejection reason's text. Row 11 checks edit state and note removal, not both button visibilities again.
- Row 12 asserts Cancel and the current-password field are visible; it does not assert Save visibility or required validation despite the label's wording.
- Rows 13/14 are HTTP checks made through a separate client, not browser assertions that an error appears under fields.
- The screenshot helper is a no-op. No screenshot comparison or dark/phone assertion is made.
- Overlaps: suite 19 source/password edit UI; suite 16 credential validation; suite 27 Configure state.
