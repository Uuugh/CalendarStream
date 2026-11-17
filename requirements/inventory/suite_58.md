# Suite 58: Event links, History and feed defaults

Source: [`tests/suite_58.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8158; seed.demo; fake work.ics download; patched loops. Synthetic fixed UIDs drive picker/navigation assertions. Chromium 1400×900 briefly resizes to 900px. HTTP markup/storage checks precede browser geometry/dialog interactions; pageerror and console errors collected.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S58-01 | events | New-event Calendar-label markup contains an info dot and the fixture explanation of downstream-only edits. | [L40](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L40) |
| S58-02 | events | The new editor omits the old Changes here only affect footer and muted-foot markup. | [L42](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L42) |
| S58-03 | events | An imported-event footer includes edit-persistence/upstream-safety explanation and omits the new-event info-dot/footer pattern. | [L45](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L45) |
| S58-04 | events | A saved custom event omits Added on this page and includes the Calendar info dot. | [L51](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L51) |
| S58-05 | events | Link markup uses a hidden empty target field and hidden picked button instead of a select. | [L55](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L55) |
| S58-06 | events | The link Remove control is SVG-only with title/aria-label and appears after the Rule choice. | [L57](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L57) |
| S58-07 | events | The picker endpoint returns a month fragment with previous/next month attributes and Today control, not a full HTML page. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L61) |
| S58-08 | events | The current event is rendered with disabled-self class and its title. | [L63](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L63) |
| S58-09 | events | The current UID is not selectable, while another fixture UID has the expected title/date label. | [L64](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L64) |
| S58-10 | events | Rule-generated events have disabled markup and no selectable rule UID buttons. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L65) |
| S58-11 | events | Picker source contains no event-add URL, data-add or edit-tool markup. | [L67](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L67) |
| S58-12 | events | The next-month picker request returns 200 and its page text names November. | [L68](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L68) |
| S58-13 | events | A linked editor renders the target value, picked title/date button, active Event segment and unhidden link panel. | [L73](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L73) |
| S58-14 | events | The link-mode add editor has pick-now=1. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L76) |
| S58-15 | feeds | Add-feed markup has the old-link guidance and an initial stream token of at least twenty word/hyphen characters. | [L83](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L83) |
| S58-16 | feeds | Source metadata contains the fixture note and Label/data-default markup. | [L85](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L85) |
| S58-17 | feeds | Adding an empty label/note feed increments destination count and inherits its selected source's name/note. | [L89](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L89) |
| S58-18 | feeds | Explicit feed label/note values are preserved. | [L93](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L93) |
| S58-19 | history | Default History retention is 100 in constants/effective value and the input has the sampled 1–200 bounds/value. | [L96](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L96) |
| S58-20 | history | Saving retention 37 changes effective state and rendered value. | [L98](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L98) |
| S58-21 | history | Table header column IDs are time, type, event, undo in order. | [L104](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L104) |
| S58-22 | rules | The All-calendars badge has transparent background and accent-colored text/top border. | [L117](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L117) |
| S58-23 | history | Folded Activity shows three left-aligned preview lines before its status box, while explicitly opened Activity hides them. | [L126](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L126) |
| S58-24 | events | Calendar Delete asks the sampled question/subnote with No/Yes text and approximately 130px pair width. | [L133](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L133) |
| S58-25 | events | Cancelling Delete leaves the custom event undeleted. | [L136](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L136) |
| S58-26 | calendar | At 900px, event body padding is 6px and right icon inset matches Close inset within 2px and is at most 9px. | [L143](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L143) |
| S58-27 | events | Removing a link in the editor hides both pick/panel and clears its target field. | [L149](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L149) |
| S58-28 | events | Event linking opens the small calendar on the edited event's month. | [L151](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L151) |
| S58-29 | events | Next navigation changes the picker heading to November. | [L153](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L153) |
| S58-30 | events | Picking the fixture event closes the picker, sets target/label and shows the link panel. | [L156](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L156) |
| S58-31 | events | Clicking the picked label reopens the picker. | [L159](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L159) |
| S58-32 | events | Escape hides the picker while the outer event dialog stays open. | [L161](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L161) |
| S58-33 | events | Saving persists the newly picked target UID. | [L163](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L163) |
| S58-34 | events | The Calendar info tooltip opens below its icon. | [L168](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L168) |
| S58-35 | events | Embedded Delete confirmation uses the same sampled question/subnote and No/Yes text. | [L171](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L171) |
| S58-36 | events | Confirming Delete sets the stored event deletion marker. | [L174](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L174) |
| S58-37 | feeds | New-feed label/note placeholders match the first selected nonlocal source's fixture name/note. | [L179](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L179) |
| S58-38 | feeds | Unchecking that source changes the label placeholder. | [L181](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L181) |
| S58-39 | feeds | The stream title aligns horizontally above the stream input. | [L183](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L183) |
| S58-40 | shell | No pageerror or collected console-error events occur in the sampled paths. | [L184](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_58.py#L184) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Picker restrictions are asserted in rendered fragment/button markup, not through attempted unauthorized link-save calls. Row 13 checks panel visibility/target, not independently every link-option value.
- Feed defaults use one selected nonlocal source; they do not exhaust multi-source ordering. Row 19's min/max are input attributes, not endpoint bound-validation tests.
- Preview visibility is forced by changing Activity classes; it does not persist an open preference. Delete/tooltip geometry uses sampled widths/paths, not every viewport.
- Row 38 verifies a placeholder changed, not its exact replacement value. Row 33 separately checks actual link persistence after Save.
- Overlaps: suite 57 editor/link cancel; suite 49 History retention/Delete; suite 51 feed add flow; suite 61 folded header styling.
