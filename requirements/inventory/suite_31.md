# Suite 31: Source and destination layout at three widths

Source: [`tests/suite_31.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTP server on 8131; Chromium/Playwright at 1400, 900 and 390px, each 900px high. Demo.ics uploaded; public address seeded directly and another feed added. Background loops patched. No explicit browser palette is selected, so these checks do not establish both light and dark coverage.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S31-01 | feeds | Adding a feed with an empty name gives the last feed the CCS+ source's calendar name. | [L27](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L27) |
| S31-02 | feeds | The page contains the checked Label input markup with maxlength 100, accessible label and placeholder. | [L29](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L29) |
| S31-03 | calendar | The page contains the time-zone icon wrapper with the New York tooltip and the time-zone picker node. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L30) |
| S31-04 | sources | The page contains a Last synced source-status line. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L31) |
| S31-05 | sources | The page labels the credential Username and contains no span labeled UID. | [L32](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L32) |
| S31-06 | shell | Card section IDs occur as sources, destinations, rules, templates, activity, beta. | [L34](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L34) |
| S31-07 | shell | The page contains All Rules and Event Templates headings with help dots, and History, Undo & Logs text. | [L35](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L35) |
| S31-08 | feeds | The new destination has its section key, Configure aria-controls and a hidden Configure body. | [L37](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L37) |
| S31-09 | feeds | Opening that destination section returns HTTP 204 and the next page omits its hidden Configure marker. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L38) |
| S31-10 | settings | Saving the sampled malformed destination section key returns HTTP 400. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L39) |
| S31-11 | shell | At 1400, 900 and 390px, the page has no horizontal overflow and no collected pageerror events. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L48) |
| S31-12 | sources | At non-phone widths where the right box exists, its top is above the title box bottom and the two status lines share an x coordinate. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L58) |
| S31-13 | history | At 1400px, Activity and Calendar widths differ by less than two pixels. | [L61](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L61) |
| S31-14 | shell | At 1400px, Rules and Templates tops differ by less than two pixels and Templates is to the right. | [L63](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L63) |
| S31-15 | shell | At 1400px, the horizontal gap from Sources right edge to Destinations left edge rounds to 10px. | [L65](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L65) |
| S31-16 | sources | At 1400px with Configure open, the validation slot width rounds to 80px. | [L67](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L67) |
| S31-17 | settings | At 1400px, opening Settings yields one of the two accepted RGB background values. | [L70](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L70) |
| S31-18 | calendar | At 390px, the time-zone wrapper is visible and has the New York time-zone tooltip. | [L72](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L72) |
| S31-19 | sources | At 390px, the source status node text contains Last synced. | [L73](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_31.py#L73) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 11 repeats at three widths. The pageerror listener is installed before navigation, but absence of collected events does not prove all possible interactions are error-free.
- Row 12 runs only at 1400/900px and is skipped if the right header box is absent. It checks vertical overlap and status-line x alignment, not every position described in its historical label.
- Rows 13–17 run only at 1400px; rows 18–19 only at 390px. Row 19 uses text_content, not a visibility assertion.
- Row 16 measures 80px; it does not compare against another box to establish half-width. Row 17 accepts two specific background colors and does not establish dark-mode behavior.
- Header/icon and hint assertions inspect markup; they do not prove exact icon shape, accessible contrast or every input state.
- Overlaps: suite 22 Settings order; suite 19 source status/login; suite 26 view/section markup; suite 21 phone/browser controls.
