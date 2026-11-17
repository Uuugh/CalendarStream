# Suite 61: Theme headers, dirty controls and fold timing

Source: [`tests/suite_61.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8161; seed.demo; fake work.ics download; all background loops patched. Harness/setup/scripts are inspected as source; section timestamps are manipulated. Browser checks run light/dark at 1230×900, with a final desktop label-gap sample outside that loop. No phone loop.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S61-01 | process | Harness/setup source strings mention faketime and the fixed October 30 timestamp. | [L36](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L36) |
| S61-02 | rules / event_templates | Each sampled section's source markup orders status lines, count box then plus. | [L42](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L42) |
| S61-03 | rules / event_templates | Each sampled section has no sfoot markup. | [L43](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L43) |
| S61-04 | rules | The Rules status substring contains three sampled sline class occurrences. | [L44](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L44) |
| S61-05 | event_templates | The Templates status substring contains two sampled sline class occurrences. | [L45](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L45) |
| S61-06 | sources | The sampled Sources section has no slines class while expected source/rule nodes exist. | [L46](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L46) |
| S61-07 | shell | Title markup has light/dark logo marks and Calendar/Stream spans, without a version or link. | [L50](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L50) |
| S61-08 | shell | Footer markup includes copyright, current-version class and running version text. | [L52](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L52) |
| S61-09 | shell | The page has a favicon URL and five sampled logo assets return 200. | [L53](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L53) |
| S61-10 | shell | Page source includes the four expected light/dark logo-color token values. | [L55](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L55) |
| S61-11 | shell | Expand labels have exactly two Details exceptions and all others Configure, without old Edit Configuration text. | [L59](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L59) |
| S61-12 | rules | If a page-script URL exists, its text omits the sampled airplane placeholder; absence of the script URL passes. | [L60](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L60) |
| S61-13 | shell | Freshly observed open section state remains open. | [L64](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L64) |
| S61-14 | shell | After shifting Rules' open timestamp 25 hours back, Rules closes/persists closed while Templates stays open. | [L67](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L67) |
| S61-15 | shell | In both palettes, six sections have 1px top borders and no box shadow, and sampled CCS+ has 1px top border. | [L81](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L81) |
| S61-16 | shell | The three sampled section color tokens equal the expected Feed/Rules/Templates hex values. | [L82](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L82) |
| S61-17 | rules | Measured All Rules header orders title, lines, count and plus with its right offset within 11–15px. | [L89](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L89) |
| S61-18 | history | Activity preview text is left-aligned, ends before the status box and starts over 20px after the title. | [L90](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L90) |
| S61-19 | sources | Both source Cancel and Save controls are disabled initially. | [L94](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L94) |
| S61-20 | sources | Editing enables both controls, sets dirty=1 and selects pulse-run animation with iteration count five. | [L98](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L98) |
| S61-21 | sources | Cancelling puts the pair in cancelled state. | [L100](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L100) |
| S61-22 | sources | After the sampled cancellation wait, Save is disabled again. | [L102](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L102) |
| S61-23 | shell | Good status boxes keep visible words; if login marks exist, at least one is shrunk and sampled shrunk marks have accessible names. | [L108](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L108) |
| S61-24 | rules | The sampled rule grip has six circles, opacity 0.55 and sits left of the row. | [L115](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L115) |
| S61-25 | rules | Hovering the row leaves grip opacity above 0.4. | [L117](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L117) |
| S61-26 | rules | The trash icon has a nonempty computed color different from the Edit control color. | [L118](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L118) |
| S61-27 | shell | No browser pageerror events are collected in either palette context. | [L119](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L119) |
| S61-28 | sources | Sampled field-label row gaps are 1px or normal and at least one is 1px. | [L126](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_61.py#L126) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- The clock setup row checks source strings, not whether faketime is installed/active. Row 12 has a True fallback if the page script URL is absent and is not independent placeholder verification in that branch.
- Timestamp folding samples 25 hours rather than proving the exact 24-hour boundary. Rows 02/03 repeat for Rules/Templates; browser rows 15–27 repeat across light/dark.
- Row 06 examines Sources only, despite the old label mentioning Feeds too. Row 15 measures six section borders and one source module, not every module.
- Row 20 checks animation name/iteration configuration, not visually five pulses or exact duration. Row 22 checks Save only, not both pair controls. Row 23 permits zero login marks.
- The grip test counts six circles but not their two-column/three-row geometry. Trash color is compared to Edit color, not directly to a red token. Row 28 checks computed rowGap rather than actual label/field pixel separation.
- Overlaps: suite 44 broad theme; suite 59 section colors; suite 34 Cancel/save feedback; suite 58 History headers.
