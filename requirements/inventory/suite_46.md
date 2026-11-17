# Suite 46: Search, event form layout and module controls

Source: [`tests/suite_46.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8115; seed.demo and fake work.ics download; patched loops. Connected state and updater offer/readiness are patched for markup checks. Chromium 1230×950 inspects search, embedded editor, Templates and update state markup.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S46-01 | google | With connected patched true, the Google header has next-push or instant-updates-off wording and tooltip markup. | [L34](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L34) |
| S46-02 | feeds | The sampled ordinary feed header contains no Next push text. | [L38](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L38) |
| S46-03 | google | The Google settings substring omits credtrash and has the checked Remove control/confirmation attribute. | [L40](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L40) |
| S46-04 | settings | Updates source markup has the checked label/select row structure and auto-update markup. | [L44](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L44) |
| S46-05 | google | Without the connected patch, settings still omits credtrash and has Remove or Not set up markup. | [L47](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L47) |
| S46-06 | google | Posting Remove returns 303 and leaves the Google client unconfigured. | [L49](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L49) |
| S46-07 | calendar | The union search page contains a numeric found-count string. | [L52](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L52) |
| S46-08 | calendar | The nonempty sampled result titles all contain Union. | [L54](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L54) |
| S46-09 | calendar | Adding source/date filters produces a smaller nonempty count of Union meetings and the sampled start date appears. | [L57](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L57) |
| S46-10 | calendar | A nonsense search query renders Nothing found. | [L58](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L58) |
| S46-11 | calendar | The calendar plus has the sampled top/right offsets and search lies after the zone control with near-aligned top positions. | [L70](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L70) |
| S46-12 | calendar | Typing union shows search, nonempty result events and only Union result summaries. | [L72](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L72) |
| S46-13 | calendar | The typed query remains union and its input keeps focus. | [L74](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L74) |
| S46-14 | calendar | Closing search hides the line and restores month day cells. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L76) |
| S46-15 | events | Calendar plus opens an event dialog with a date-bearing iframe URL. | [L78](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L78) |
| S46-16 | events | Location is below and aligned with Title; the Calendar label is below Location. | [L84](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L84) |
| S46-17 | events | The color picker has the sampled vertical proximity and horizontal separation from the Calendar label. | [L85](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L85) |
| S46-18 | events | Start/end date fields share a row, and time fields sit below with matching x coordinates. | [L86](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L86) |
| S46-19 | events | All-day is above the end date, and the different-end-zone checkbox lies between that date and end time. | [L90](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L90) |
| S46-20 | events | The sampled visible text/date/select fields are nonempty and all round to 34px high. | [L92](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L92) |
| S46-21 | events | Editor body omits times in and Last day text and has one map button. | [L94](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L94) |
| S46-22 | events | Checking All-day leaves the end label Ends. | [L96](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L96) |
| S46-23 | events | Typing a location updates the map href with its URL-encoded query. | [L98](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L98) |
| S46-24 | events | The editor button pair rounds to 130×34px. | [L100](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L100) |
| S46-25 | rules / event_templates | Each section plus satisfies the sampled top/right offsets and the section has no bottom footer. | [L107](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L107) |
| S46-26 | event_templates | Clicking Templates plus opens its dialog with one tag row. | [L109](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L109) |
| S46-27 | calendar | The sampled opened event's Close and icon rectangles meet the checked bottom/left/right and shared-or-above-row constraints. | [L120](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L120) |
| S46-28 | settings | With a newer offer/updater readiness patched, Settings Update now has four state spans and Update now text. | [L125](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L125) |
| S46-29 | shell | No browser pageerror events are collected during the sampled interactions. | [L127](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_46.py#L127) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Several labels describe a line/placement more strongly than source markup proves: row 04 does not measure one-row layout; row 03 checks confirmation markup, not a browser confirmation interaction.
- Search filtering samples counts/titles and one date string, not exact membership for every bound. Row 15 opens an editor, not a saved event.
- Row 20 samples visible text/date/select fields, excluding other types. Row 23 checks the map href, not opening an external map. Row 28 checks state spans, not actually performing an update.
- Row 25 repeats for Rules/Templates; geometry checks run only at one desktop width. No phone/dark browser loop.
- Overlaps: suite 44 popup/theme geometry; suite 47 update state; suite 49 all-date search.
