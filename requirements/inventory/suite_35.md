# Suite 35: Fonts, icons, module geometry and sync feedback

Source: [`tests/suite_35.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8097; fake work.ics downloader with controllable delay/failure; Demo.ics upload. Static template/icon scans run first. Browser geometry/font checks loop over requested light/dark contexts at 1400×900, then separate interaction checks run and the page is resized to 390×900. Background loops patched.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S35-01 | shell | The static regex finds at least one named icon and every matched literal icon name exists in the vendored icon paths. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L31) |
| S35-02 | shell | Failure sentinel: requesting an unknown icon name without raising KeyError fails. | [L33](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L33) |
| S35-03 | shell | The unknown-icon request reaches the expected KeyError handler. | [L35](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L35) |
| S35-04 | shell | The check icon mask begins with the encoded SVG data-URL prefix and contains no literal less-than character. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L36) |
| S35-05 | shell | The scanned HTML template strings contain neither 999px nor border-radius:50%. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L38) |
| S35-06 | shell | The scanned templates contain none of the three sampled old SVG viewBox spellings. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L39) |
| S35-07 | shell | An anonymous request for the Sans font returns 200 with WOFF2 signature bytes. | [L57](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L57) |
| S35-08 | shell | Anonymous requests for the Mono font and font license return 200. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L58) |
| S35-09 | account | The sampled static parent-path request returns HTTP 404. | [L59](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L59) |
| S35-10 | shell | Page markup declares IBM Plex Sans, omits fonts.googleapis and includes its font variable. | [L60](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L60) |
| S35-11 | shell | The uid and url input markup includes class code. | [L61](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L61) |
| S35-12 | google | The client-ID input uses the sampled code-class markup or there is no client-ID field in the page. | [L62](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L62) |
| S35-13 | feeds | The subscription page includes the font name and copy-icon symbol/use markup rather than literal icon-name text. | [L64](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L64) |
| S35-14 | documentation | The footer contains the repository license/attribution link and its label. | [L66](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L66) |
| S35-15 | shell | The page omits Canceled and includes the Cancelled completion attribute. | [L67](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L67) |
| S35-16 | google | The status API google object has exactly connected, running, pending and error keys. | [L70](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L70) |
| S35-17 | google | Async Google Sync returns HTTP 200 and exactly JSON ok=true. | [L72](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L72) |
| S35-18 | shell | In each requested light/dark context, body font begins IBM Plex Sans and explicit Sans/Mono font-load requests succeed. | [L84](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L84) |
| S35-19 | sources | In each requested light/dark context, the username input's computed font begins IBM Plex Mono. | [L86](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L86) |
| S35-20 | shell | In each palette context, module header measurements are nonempty and all round to 50px. | [L88](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L88) |
| S35-21 | shell | In each palette context, status boxes are nonempty and all round to 132×50px. | [L90](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L90) |
| S35-22 | sources | In each palette context, at least one visible idle Sync Now exists and all sampled idle buttons have equal dimensions. | [L92](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L92) |
| S35-23 | sources | In each palette context, the Work module is folded, its Expand center lies near the bottom border and its divider pseudo-element is hidden. | [L97](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L97) |
| S35-24 | shell | In each palette context, the sampled destination help dot is raised relative to its heading and within 0–4px after its word. | [L102](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L102) |
| S35-25 | shell | In each palette context, no sampled visible control matches the computed numeric pill-radius predicate. | [L105](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L105) |
| S35-26 | shell | In each palette context, there are over twenty svg.mi nodes and every SVG matches the permitted grip/use/symbol structure. | [L106](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L106) |
| S35-27 | shell | No pageerror events are collected during either sampled palette load. | [L107](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L107) |
| S35-28 | sources | During delayed sync, the button state is syncing and both button and status chip say Syncing…. | [L118](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L118) |
| S35-29 | sources | After successful sync, the button is done/Synced with pulse-ok animation name and the chip says Healthy. | [L123](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L123) |
| S35-30 | sources | The syncing and done button dimensions round to the same width and height. | [L125](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L125) |
| S35-31 | sources | After a delay, the button returns to idle/Sync Now without a load event. | [L127](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L127) |
| S35-32 | sources | A fake download failure yields fail state, Failed text and pulse-warn animation name. | [L133](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L133) |
| S35-33 | sources | Expanded Work has a block divider, a 24px-high name input, a visible note input and a 50px header. | [L138](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L138) |
| S35-34 | sources | Editing the URL yields edit state with empty-text Cancel/Save controls, Cancel aria-label and a visible save SVG. | [L144](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L144) |
| S35-35 | sources | Inline Cancel restores the original URL and leaves the slot in ok or needs state. | [L148](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L148) |
| S35-36 | sources | The bottom Cancel control displays Cancelled after cancelling a typed name. | [L151](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L151) |
| S35-37 | shell | No pageerror events are collected during the sampled sync/edit interactions. | [L152](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L152) |
| S35-38 | shell | After resizing to 390px, document scroll width is at most 390px. | [L156](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_35.py#L156) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Static icon scanning only covers literal names matched in templates/main/routes; it does not establish every dynamically selected icon or prohibit every hand-drawn SVG. The banned viewBox/radius strings are specific source-spelling checks.
- Rows 02/03 are paired exception sentinel/success marker. Row 09 samples one normalized parent-path URL, not a complete path-traversal audit.
- Row 12 allows absence of the client field. Row 25 ignores percentage radius strings and samples only the selected visible elements, so it does not prove a blanket absence of pill/circle shapes.
- Row 26 expressly permits gripdots SVGs. Row 22 establishes equal idle sizes, not a particular corner shape.
- Row 33 measures the name field height and note visibility; it does not measure note height despite the legacy label saying both are 24px.
- Row 34 asserts Cancel's accessible name and a visible save SVG, not the Save control's accessible name. Animation checks read animationName, not rendered pulse color.
- Light/dark context checks are separate from the final sync/edit interactions; the phone check only asserts scroll width.
- Overlaps: suite 34 control styling; suite 31 responsive modules; suite 39 static asset serving/cache; suite 37 sync status box.
