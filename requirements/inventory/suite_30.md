# Suite 30: Version ordering and beta/stable offers

Source: [`tests/suite_30.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient for integration checks, with background loops and HTTP client patched. Pure comparisons run first. Fake VERSION/STABLE responses and installed version 0.2.7-beta.1 drive channel/offer checks.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S30-01 | settings | Each adjacent pair in the sampled version sequence compares newer in one direction only, including beta.2 before beta.10 and betas before their release. | [L17](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L17) |
| S30-02 | settings | The samples 0.2.7-beta, 0.2.7.1 and an unknown installed version do not produce a newer-version result. | [L18](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L18) |
| S30-03 | settings | The sampled plain release is stable; its beta and x are not. | [L19](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L19) |
| S30-04 | settings | For beta and a pinned beta tag the channel is beta; latest, a pinned release and the empty tag select stable. | [L22](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L22) |
| S30-05 | shell | The footer shows the full beta version and links to its release tag. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L38) |
| S30-06 | settings | A beta install offers the newer 0.2.7-beta.2 and shows its available-version text. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L39) |
| S30-07 | settings | A beta install then offers the stable 0.2.7 release when VERSION names it. | [L41](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L41) |
| S30-08 | settings | A latest-channel install offers STABLE 0.2.7 while VERSION names 0.2.8-beta.1. | [L44](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L44) |
| S30-09 | settings | If STABLE subsequently names a beta, update info records an error and preserves the last offered stable version. | [L46](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_30.py#L46) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 01 compares adjacent pairs in a finite ordered list, not every semver pair. Row 02 checks three invalid comparisons, not all malformed versions.
- Row 04 is one call site across five image-tag cases. The empty string case does not remove IMAGE_TAG from the environment.
- Remote VERSION/STABLE data and the installed version are fake; this suite checks update decisions and markup, not published artifact identity.
- Overlaps: suite 22 channel selection and last-answer retention; suite 29 release-note links.
