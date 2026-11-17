# Suite 34: Help, saving, handles and component dimensions

Source: [`tests/suite_34.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8095; Chromium at 1400×900. Demo.ics is uploaded and a feed added; successful source-auth state is seeded. Background loops patched. The browser records load/pageerror events and measures sampled DOM elements/computed styles.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S34-01 | shell | The page has the source-section icon markup, Calendars/Feeds text and exactly six section-icon class occurrences. | [L26](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L26) |
| S34-02 | shell | The page uses Expand to Configure and short Expand markup, without the older configuration-expansion phrase. | [L27](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L27) |
| S34-03 | shell | The page contains help-dot markup and What other apps get guidance, without the sampled double-escaped class text. | [L28](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L28) |
| S34-04 | calendar | The sampled legend substring omits Timed and All-day labels. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L30) |
| S34-05 | calendar | The page contains a print-button class and the stylesheet contains an @media print block. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L31) |
| S34-06 | calendar | The first sampled noncustom timed and all-day events have identical computed background colors. | [L42](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L42) |
| S34-07 | shell | Clicking the destination help dot makes its help tooltip visible. | [L46](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L46) |
| S34-08 | shell | Moving the pointer away and pressing Escape hides that help tooltip. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L48) |
| S34-09 | sources | The source Cancel/Save pair rounds to 130×34px with each button 65px wide. | [L52](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L52) |
| S34-10 | sources | Cancel restores the original source name, displays Cancelled and expands the Cancel button beyond 65px. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L55) |
| S34-11 | sources | After the cancellation delay, the Configure body is hidden. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L58) |
| S34-12 | sources | After another sampled delay, the pair state is idle and its text contains Cancel. | [L60](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L60) |
| S34-13 | sources | Saving the new source name persists it without a load event. | [L66](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L66) |
| S34-14 | sources | The saved pair has state saved and its Save button text is Saved. | [L67](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L67) |
| S34-15 | feeds | Saving the source leaves a typed but unsaved destination name unchanged. | [L68](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L68) |
| S34-16 | calendar | The legend displays the updated source name. | [L69](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L69) |
| S34-17 | rules | The first rule handle has up, grip and down controls. | [L76](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L76) |
| S34-18 | rules | Clicking down reverses the first two rules in stored and displayed order without a load event. | [L78](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L78) |
| S34-19 | sources | The number of source module handles equals the number of sources. | [L80](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L80) |
| S34-20 | sources / rules | Visible source text inputs have a nonempty height set of 34px; every sampled rule line is 34px tall with 8px top-left radius. | [L85](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L85) |
| S34-21 | sources | The sampled source spacing values are 5,5,5,5,2,5px and the help-guide height rounds to 32px. | [L90](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L90) |
| S34-22 | sources | The source footer has a solid top border. | [L92](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L92) |
| S34-23 | rules | Saving a SIM condition through the rule dialog persists it and displays it in All Rules without a load event. | [L96](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L96) |
| S34-24 | shell | No browser pageerror events are collected during the sampled interactions. | [L97](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_34.py#L97) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 06 compares the first matched noncustom timed/all-day backgrounds only, not all calendars or events.
- Row 05 asserts Print markup and a print media block; it does not print or compare output. Row 20 requires a nonempty input-height set, but its all() over rule lines can pass on an empty list.
- Row 21 checks computed spacing and one guide height; it does not assert the label's claimed internal 5px/9px padding.
- Row 15 proves one other typed field is kept, not that every unrelated DOM subtree is untouched.
- Waits establish observed cancellation/saved feedback states, not exact animation-duration guarantees.
- Overlaps: suite 35 module/sync geometry; suite 33 preserved typing; suite 36 rule movement; suite 41 handle layout.
