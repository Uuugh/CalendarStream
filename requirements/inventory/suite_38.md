# Suite 38: Section counts, color persistence, settings and auto-update

Source: [`tests/suite_38.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8094; seed.demo and fake work.ics download; patched background loops. The test toggles updater readiness, seeds an update offer and substitutes a fake update method. Chromium uses 1400×1000, tracking pageerror/load events. No real image installation occurs.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S38-01 | rules / event_templates | The rendered green count boxes show the current rule count and two templates. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L31) |
| S38-02 | shell | The page contains at least two long Expand to Configure labels. | [L33](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L33) |
| S38-03 | rules | The All Rules header substring has no old toggle/peek class and has a help dot immediately after the heading text. | [L35](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L35) |
| S38-04 | rules | How rules work is absent from the rules body and occurs after the rule dialog footer markup. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L36) |
| S38-05 | rules | Page badge markup includes all, the sampled single-calendar color and no none badge. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L39) |
| S38-06 | rules | The shared-rule page includes the exact two-color repeating-gradient string for the fixture sources. | [L42](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L42) |
| S38-07 | rules | Adding the duplicate produces a run-class rule count box with the sampled digit-to-check title. | [L47](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L47) |
| S38-08 | settings | Without a ready updater, auto-update checkbox markup has value 1 and disabled. | [L49](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L49) |
| S38-09 | settings | With updater ready, the update form includes checkbox onchange markup and orders Check now before the auto-update wrapper. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L53) |
| S38-10 | settings | Submitting auto=1 enables auto_update and renders the Auto-update on message. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L55) |
| S38-11 | settings | Submitting the auto form without auto disables auto_update. | [L57](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L57) |
| S38-12 | settings | Two auto_install calls invoke the fake updater once and render the announced target version message. | [L64](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L64) |
| S38-13 | rules / event_templates / history | For each sampled section, title click leaves the body hidden and its Expand control then unhides it. | [L79](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L79) |
| S38-14 | history | The Activity latest text is left-aligned and its rectangle ends before the status-box left edge. | [L83](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L83) |
| S38-15 | sources | Each of two successive source color choices persists the selected calendar color. | [L90](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L90) |
| S38-16 | calendar / feeds | The final color appears in legend and destination source-pick markup without a load event. | [L91](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L91) |
| S38-17 | settings | Saving the public address updates stored state and feed markup without a load event, leaving Settings visible. | [L96](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L96) |
| S38-18 | settings | Choosing monthly persists that frequency without a load event, leaving Settings visible. | [L99](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L99) |
| S38-19 | settings | The frequency menu is within 1px of 34px high, its status box within 1px of 132×50px and Check now stays at least 10px inside the Settings group right edge. | [L103](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L103) |
| S38-20 | shell | No browser pageerror events are collected during the sampled interactions. | [L105](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_38.py#L105) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Badge/count rows inspect markup classes and specific gradient text, not actual rendered colors. Row 05 does not independently inspect the all-calendar badge's white fill.
- Row 12 asserts one fake updater invocation and log text across two calls, not a real installation or long-term retry behavior.
- Row 13 is repeated for Rules, Templates and Activity. Row 15 repeats two colors. Row 16 checks legend and destination picks, not rule badges despite its legacy label.
- Row 19 measures control/status geometry and one right edge only; it does not prove every element is contained.
- Overlaps: suite 32 updater UI; suite 34 retained typing/save; suite 37 conflict warnings; suite 31 Settings geometry.
