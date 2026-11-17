# Suite 22: Update channels and check frequency

Source: [`tests/suite_22.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; source/Google/update loops patched. Fake HTTP client serves VERSION and STABLE; the installed updater version is patched to 0.1.19. The test switches IMAGE_TAG and remote fixture versions in sequence.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S22-01 | settings | Settings renders updates, weekly selected, and hourly/monthly/never options. | [L29](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L29) |
| S22-02 | settings | Settings groups are pagelogin, domains, updates, look, googlesync in that order. | [L32](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L32) |
| S22-03 | settings | For IMAGE_TAG=latest, the check fetches STABLE and offers no update when that stable version is older. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L36) |
| S22-04 | settings | With no newer stable, the page has no newver class and shows Stable versions, Up to date and Next check @. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L38) |
| S22-05 | settings | A newer stable is offered as 9.2.0 with available-version text and links for current and available releases. | [L42](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L42) |
| S22-06 | settings | Changing from stable to beta clears the update-info result for the previous channel. | [L45](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L45) |
| S22-07 | settings | For IMAGE_TAG=beta, the check fetches VERSION and offers 9.9.9 with Beta versions and release text. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L48) |
| S22-08 | settings | A pinned non-beta IMAGE_TAG is classified as stable. | [L50](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L50) |
| S22-09 | settings | Saving frequency yearly returns HTTP 400. | [L52](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L52) |
| S22-10 | settings | With frequency never, due remains false at the sampled time 400 days ahead. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L55) |
| S22-11 | settings | After an hourly check, due is false at 30 minutes and true at 61 minutes. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L58) |
| S22-12 | settings | For monthly frequency, due is false at 29 days and true at 31 days. | [L60](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L60) |
| S22-13 | settings | A connection failure retains the last available version and displays a failed-check message. | [L69](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L69) |
| S22-14 | account | Posting update settings without status-page authentication returns HTTP 401. | [L70](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L70) |
| S22-15 | settings | A manual check retains the stored logged-version marker for 9.9.9. | [L74](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_22.py#L74) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 11 and 12 sample either side of scheduling intervals; they do not prove the exact due-time boundaries. Row 10 samples 400 days ahead, not literally all future times.
- Row 02 only asserts group IDs/order; its historical label's admin-email placement claim is not checked.
- Fake release files and failures exercise update-check decisions, not live GitHub connectivity, image pulling or update installation.
- Overlaps: suite 30 beta/version semantics; suite 25 update status; suite 19 Settings group order.
