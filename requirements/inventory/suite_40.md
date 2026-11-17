# Suite 40: Rule colors, section headers, feed reads and Settings

Source: [`tests/suite_40.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8096; seed.demo; fake work.ics downloader and patched loops. A Google-Importer user-agent request seeds feed-read feedback. Chromium uses 1400×1000 for palette interaction; initial header/palette assertions inspect rendered source.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S40-01 | rules | The rendered RDO rule label contains Color, a Tomato swatch with the expected color and the Tomato name. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L30) |
| S40-02 | rules | The titled airport rule has the checked title attribute and visible title-plus-action separator markup. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L31) |
| S40-03 | rules / event_templates | Each sampled section header has a count box before its plus control and the section contains no sfoot class. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L36) |
| S40-04 | sources | The CCS+ header has Last synced time markup and the page omits Last check was. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L39) |
| S40-05 | feeds | After a Google-Importer feed request, its header says Last read by Google and omits All dates. | [L44](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L44) |
| S40-06 | google | The page has a client-ID copyField handler for either client field ID. | [L46](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L46) |
| S40-07 | settings | The Updates form has module header/status/name markup and Check now, while the page omits Updater: running. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L48) |
| S40-08 | shell | Page source includes the sampled Soft palette background and accent tokens. | [L51](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L51) |
| S40-09 | rules | The rule Color action has eleven palette buttons and no input[type=color]. | [L62](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L62) |
| S40-10 | rules | Selecting Peacock marks a palette control with aria-checked=true and Peacock title. | [L65](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L65) |
| S40-11 | rules | Saving that rule stores exactly its color action with hex #039be5. | [L68](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L68) |
| S40-12 | shell | No browser pageerror events are collected during the sampled interactions. | [L69](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_40.py#L69) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 03 is one call site over Rules and Templates. It checks markup order/absent footer, not top-right screen coordinates.
- Row 05 samples one feed reader user-agent and header text, not the complete reader-classification algorithm or horizontal position.
- Row 06 only asserts a copy handler exists, not clipboard contents. Row 08 checks two source tokens rather than every palette color or rendered contrast.
- Palette interaction checks exact saved action but do not exhaust all eleven color choices.
- Overlaps: suite 19 event colors; suite 35 source/feeds status; suite 38 count/plus modules; suite 33 rule rendering.
