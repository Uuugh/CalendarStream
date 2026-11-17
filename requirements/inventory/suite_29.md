# Suite 29: Destination date ranges, legacy rules and labels

Source: [`tests/suite_29.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; background loops and run_once patched. Demo.ics supplies the initial feed. Directly seeded legacy tags/templates/subscriptions/defaults are migrated; a synthetic change-title rule exercises the I24 label regression.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S29-01 | shell | The rendered version links to its corresponding release tag. | [L19](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L19) |
| S29-02 | feeds | Saving the sampled date range returns HTTP 303, stores its start date and reduces the feed event count to a nonzero subset. | [L25](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L25) |
| S29-03 | feeds | Saving an end date before the start date returns HTTP 400. | [L26](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L26) |
| S29-04 | feeds | Clearing both destination dates restores the original feed event count. | [L28](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L28) |
| S29-05 | feeds | The page includes start/end inputs and rangeall markup. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L30) |
| S29-06 | rules | Legacy rule migration yields three CCS+-scoped rules: RDO color, VAC color and a 120-minute no-end action, in that order. | [L40](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L40) |
| S29-07 | rules | After migration, legacy calendar_tags and defaults records are absent. | [L42](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L42) |
| S29-08 | rules | A change-title-to-text action produces the exact human label Every event → Change Title to “Reserve”. | [L47](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L47) |
| S29-09 | rules | The page returns HTTP 200 with that change-title rule saved. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L48) |
| S29-10 | rules | The rendered page contains Tomato and the expected source-use badge naming the CCS+ calendar. | [L51](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L51) |
| S29-11 | sources | Saving a source title and note changes the calendar name and renders the submitted note in the checked tooltip markup. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_29.py#L55) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 02 proves a smaller nonempty feed count and the saved start date. It does not check every included event against exact start/end boundaries, nor the stored end value independently.
- Row 06 checks migrated rule order, color labels, action and CCS+ applicability, not the resulting all-day state of all events. Row 07 only checks removal of calendar_tags and defaults, not every seeded legacy key.
- Row 10 asserts one expected badge plus Tomato text; it does not prove all rules have correct source-use badges.
- Row 11 checks resulting name/tooltip state; it does not assert the save response status.
- Overlaps: suite 26 source/destination migration; suite 27 built-in defaults; suite 19 rule labeling and source names.
