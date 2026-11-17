# Suite 33: Source presets, shared rules, reports and in-place updates

Source: [`tests/suite_33.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8096; Chromium at 1400×900. Demo.ics and work.ics are synthetic; fake download delays 1.5 seconds and background loops are patched. Stored event snapshots are mutated via two fixture feeds to test Record changes. Browser load/pageerror events are collected.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S33-01 | sources | The Google source stores preset=google and the page contains its kind label and secret-address/enable help headings. | [L34](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L34) |
| S33-02 | sources | The CCS+ source kind label names United Airlines CCS+ and its sampled header has no Note label before a note is written. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L36) |
| S33-03 | sources | The page contains How to enable CCS+ and Accomplished help headings. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L38) |
| S33-04 | sources | CCS+ markup orders Automatic Upload, interval control, Manual Upload and Rules. | [L41](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L41) |
| S33-05 | sources | Saving an empty source note leaves no Note label in its sampled header substring. | [L43](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L43) |
| S33-06 | rules | The newly saved shared rule is effective on both chosen calendars. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L48) |
| S33-07 | rules | The page contains a shared striped-scope badge and 2 calendars text. | [L50](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L50) |
| S33-08 | rules | Changing that rule's Apply to list to CCS+ removes it from the other source's effective rules. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L53) |
| S33-09 | rules | The resulting page contains a one-calendar local badge and This calendar text. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L55) |
| S33-10 | rules | Cloning the rule increases the total rule count by one. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L58) |
| S33-11 | rules | A Record changes rule persists the changes action and makes the source ruleset report records_changes. | [L61](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L61) |
| S33-12 | rules | After changing fixture event time, stored change notes and annotated events exist; the first annotated description contains Changed and time. | [L68](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L68) |
| S33-13 | history | The rendered page contains the Family changed activity message. | [L69](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L69) |
| S33-14 | diagnostics | Report data has the current version and excludes the fixture CCS+ username and private feed-token substring. | [L73](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L73) |
| S33-15 | sources | Async Sync Now returns HTTP 200 with JSON ok=true. | [L76](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L76) |
| S33-16 | calendar | Selecting Week renders one hourview, records no load event and does not add view= to the URL. | [L86](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L86) |
| S33-17 | calendar | Selecting List renders one agenda and records no load event. | [L88](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L88) |
| S33-18 | sources | During the fake sync, the source status chip says Syncing… and no load event is recorded. | [L95](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L95) |
| S33-19 | sources | After sync, the chip says Healthy, no load event is recorded and another unsaved source-name value remains typed. | [L97](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L97) |
| S33-20 | sources | Cancel restores Family as the source name and hides its Configure body. | [L101](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L101) |
| S33-21 | rules | Editing a source rule opens the rule dialog with Change rule title and visible Remove control. | [L107](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L107) |
| S33-22 | rules | Saving the edited rule title updates stored rules and source rule text without a load event. | [L109](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L109) |
| S33-23 | sources | Choosing the Apple preset sets the visible preset heading and hidden preset value to Apple/apple. | [L112](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L112) |
| S33-24 | rules / event_templates | Rule and template bodies are hidden and the All Rules header has one plus control. | [L115](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L115) |
| S33-25 | diagnostics | The problem preview contains the typed description and current version but omits the fixture CCS+ username. | [L120](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L120) |
| S33-26 | shell | No browser pageerror events are collected during the sampled interactions. | [L121](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_33.py#L121) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 12 asserts at least one annotated event and selected description words, not every recorded event field. Report privacy rows 14/25 exclude particular fixture substrings, not every possible secret or personal field.
- Row 15 checks response status/JSON only, not response latency or browser reload. Rows 16–19 separately inspect browser load events.
- Row 07 proves a badge occurrence somewhere in the page, not every rule line. Row 10 proves a count increase, not all clone fields.
- Row 24 checks two hidden bodies and one header plus control; it does not prove all folding interactions or both header controls.
- Overlaps: suite 34 in-place save; suite 36 rule cloning; suite 38 source color/sections; suite 18 preset/help layout.
