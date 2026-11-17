# Suite 56: Google calendar-color fallback methods

Source: [`tests/suite_56.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8125; Demo.ics; patched loops/API readiness. The mock selectively refuses RGB/colorId/GET/PUT paths. Captured calls, payloads, module info and logs are inspected. Unreachable behavior is injected by replacing API/color methods. No browser.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S56-01 | google | The calendar-color table has 24 entries and the two sampled nearest-color lookups return IDs 16 and 3. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L65) |
| S56-02 | google | An accepted RGB recolor succeeds and updates the mock calendar background color. | [L69](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L69) |
| S56-03 | history | The selected recent color message ends with the RGB-method-kept wording. | [L70](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L70) |
| S56-04 | google | Calendar info stores color_way=rgb. | [L71](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L71) |
| S56-05 | history | A subsequent color message uses the shorter sampled calendar-color wording. | [L73](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L73) |
| S56-06 | google | Recolor succeeds when the mock rejects RGB but allows a fallback. | [L77](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L77) |
| S56-07 | google | The resulting calendar uses the nearest colorId and has no backgroundColor. | [L79](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L79) |
| S56-08 | history | The selected log names the nearest calendar color and method retention without a failure phrase. | [L80](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L80) |
| S56-09 | google | Calendar info stores color_way=colorId and the module omits a palette note. | [L82](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L82) |
| S56-10 | google | The next color uses one PATCH and sets its nearest colorId. | [L84](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L84) |
| S56-11 | history | That subsequent message names nearest colors without repeating the method-kept phrase. | [L86](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L86) |
| S56-12 | google | Recolor succeeds when RGB and colorId are rejected. | [L89](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L89) |
| S56-13 | google | One PUT sets the requested mock background color. | [L91](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L91) |
| S56-14 | google | The captured PUT retains sampled default reminders and selected=true while omitting colorId and etag. | [L92](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L92) |
| S56-15 | history | The selected log says the full-entry update method is kept. | [L94](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L94) |
| S56-16 | google | Calendar info stores color_way=put. | [L95](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L95) |
| S56-17 | google | If fetching the entry fails, the fallback PUT still has requested background, selected=true and hidden=false. | [L99](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L99) |
| S56-18 | google | That saved PUT method is attempted without PATCH calls. | [L101](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L101) |
| S56-19 | google | Sync succeeds even when every color method is refused. | [L104](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L104) |
| S56-20 | history | The selected refusal message identifies all methods and contains the sampled upstream status/reasons and expected reason repetition count. | [L106](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L106) |
| S56-21 | google | The module info has no last_error after color refusal. | [L109](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L109) |
| S56-22 | google | The module renders the color-does-not-carry palette note. | [L110](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L110) |
| S56-23 | google | Repeating the refused color sends neither PATCH nor PUT even after mock acceptance is restored. | [L112](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L112) |
| S56-24 | google | Selecting a different accepted color updates its background and removes the palette note. | [L114](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L114) |
| S56-25 | google | Failure sentinel: the injected unreachable color call unexpectedly succeeding fails. | [L122](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L122) |
| S56-26 | google | The unreachable color call raises GoogleError containing Couldn't reach. | [L124](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L124) |
| S56-27 | google | That unreachable color is not recorded as color_tried. | [L126](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L126) |
| S56-28 | google | Sync still succeeds when its color setter is replaced with an unreachable error. | [L130](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L130) |
| S56-29 | google | The count of sampled color-refusal messages does not increase and color_tried remains different from the unreachable color. | [L131](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_56.py#L131) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Method/log assertions use finite color/refusal sequences. Statements saying once generally inspect the selected latest message rather than global uniqueness counts.
- Row 14 checks preservation of selected/defaultReminders fields and omission of colorId/etag, not every entry property. Row 17 checks the fallback payload's color/selected/hidden fields.
- Row 25 is an expected-failure sentinel. Row 26 checks exception text, not an explicit no-other-method call count. Row 29 leaves the color unmarked for retry but does not execute the subsequent successful retry.
- This suite uses Google's 24 calendar colors, distinct from the eleven event colors tested elsewhere.
- Overlaps: suites 54/55 refused color handling; suites 19/40 event palette; suite 49 module colors.
