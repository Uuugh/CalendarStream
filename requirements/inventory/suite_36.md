# Suite 36: Rule engine, Local, reminders, printing and event dialogs

Source: [`tests/suite_36.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure engine checks construct Event/Ruleset values with America/New_York. Integration checks need Postgres, app server 8098, seed.demo fixtures, fake work.ics download and patched loops. Chromium starts at 1400×900 and later resizes to 390×800. gsync.event_body is checked directly without a real Google call.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S36-01 | rules | The sampled text conditions match trimmed equality, substring, whole word, prefix, suffix and regex; reject RDOS as whole-word RDO and reject case-sensitive lowercase against uppercase. | [L34](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L34) |
| S36-02 | rules | The sampled A event matches A OR B AND C but not the bracketed (A OR B) AND C. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L38) |
| S36-03 | rules | Non-strict normalization clears the sampled unmatched opening bracket. | [L40](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L40) |
| S36-04 | rules | Failure sentinel: strict normalization accepting the unmatched bracket without RuleError fails. | [L42](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L42) |
| S36-05 | rules | Strict unmatched-bracket normalization reaches the RuleError handler. | [L44](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L44) |
| S36-06 | rules | Failure sentinel: strict acceptance of any sampled invalid regex, empty actions or incomplete date range without RuleError fails. | [L47](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L47) |
| S36-07 | rules | Each of those three invalid samples reaches the RuleError handler. | [L49](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L49) |
| S36-08 | rules | The Fri–Mon day range matches Friday and Sunday but not Wednesday. | [L52](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L52) |
| S36-09 | rules | The sampled day conditions cover multiple selected days, after Thursday and before Thursday. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L53) |
| S36-10 | rules | The overnight 22:00–06:00 range matches the 23:00 sample but not the daytime sample. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L55) |
| S36-11 | rules | A reversed date range and an after-date condition both match the sampled October 14 event. | [L57](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L57) |
| S36-12 | rules | Length conditions distinguish no-end from a normal event, recognize the near-whole-day sample and match a 60-minute duration. | [L60](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L60) |
| S36-13 | rules | Time changes make the near-whole-day sample all-day with original-time notes, shorten the normal sample to 30 minutes and give the unmatched no-end sample a two-hour end. | [L65](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L65) |
| S36-14 | rules | The higher color rule wins, the lower rule adds its emoji and a second finish pass does not duplicate that emoji. | [L69](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L69) |
| S36-15 | rules | The new-event action creates one rule-origin Prep event from 08:00 to 08:45, an hour before the sample event. | [L72](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L72) |
| S36-16 | rules | A calendar-specific rule's insertion position is zero in the sample list; an all-calendar rule's is at its end. | [L74](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L74) |
| S36-17 | rules | The sampled before/after moves produce the exact expected rule ID orders. | [L76](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L76) |
| S36-18 | rules | Migration preserves sampled rule IDs/order, scopes shared rules to all, maps starts to begins and keeps the 90-minute action. | [L80](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L80) |
| S36-19 | sources | The first source is Local, named Local, and belongs to both sampled feed destinations. | [L93](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L93) |
| S36-20 | sources | The Local header has the sole Default label and CalendarStream kind markup but no Sync Now or old events-added status text. | [L96](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L96) |
| S36-21 | events | Saving an event without a source returns 303 and assigns it to the initial Local source. | [L100](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L100) |
| S36-22 | sources | The page includes a Local source option or preset. | [L101](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L101) |
| S36-23 | sources | Moving Local after CCS+ puts CCS+ first while default_sid still identifies Local. | [L105](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L105) |
| S36-24 | sources | The next page has one Default label and its occurrence is after the Local module start. | [L107](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L107) |
| S36-25 | events | Saving reminders 15,60,7 returns 303 and stores only 15,60. | [L110](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L110) |
| S36-26 | feeds | The sampled Dentist feed block contains VALARM, 15-minute/hour triggers and DISPLAY action. | [L114](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L114) |
| S36-27 | google | Building the event body disables default reminders and includes overrides at 15 and 60 minutes. | [L116](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L116) |
| S36-28 | events | The page contains the reminder data attribute and Reminders for text. | [L118](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L118) |
| S36-29 | events | Posting no reminder choices stores an empty alarms string. | [L120](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L120) |
| S36-30 | calendar | Saving week/no-weekends/dark print preferences returns 200 or 204 and stores those values with auto orientation. | [L122](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L122) |
| S36-31 | calendar | The sampled default print output has dark theme, a five-column grid, one sheet and Dentist text. | [L124](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L124) |
| S36-32 | calendar | The two-month print request yields two sheets, seven-column markup and light theme. | [L126](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L126) |
| S36-33 | calendar | The sampled itinerary output includes Dentist and an aday class. | [L128](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L128) |
| S36-34 | calendar | The sampled 5day print request includes five-column grid markup. | [L130](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L130) |
| S36-35 | events | The embedded editor includes embed class and hidden embed=1 field. | [L133](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L133) |
| S36-36 | events | Embedded save redirects to /event/done, whose response contains the event-saved message name. | [L136](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L136) |
| S36-37 | account | The sampled page response has SAMEORIGIN and frame-ancestors self framing headers. | [L138](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L138) |
| S36-38 | rules | The new source-specific rule sits after only same-source rules and before a rule with another scope. | [L142](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L142) |
| S36-39 | rules | Moving the sampled rule before its neighbor returns 303 and yields the expected effective pair order. | [L144](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L144) |
| S36-40 | rules | Saving the malformed regex through the route returns 400. | [L145](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L145) |
| S36-41 | rules | Cloning creates exactly one unapplied Gym rule immediately after the original. | [L150](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L150) |
| S36-42 | rules | Embedded rule-dialog data includes the rule ID, text type, nonempty length operations and one calendar entry per source. | [L153](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L153) |
| S36-43 | history | The sampled Activity markup has its node, good status box and Healthy text. | [L155](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L155) |
| S36-44 | history | After setting CCS+ state to error, the sampled Activity markup contains Unhealthy. | [L158](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L158) |
| S36-45 | shell | The stylesheet contains the checked 22px list padding and absolute-position checkmark declarations. | [L161](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L161) |
| S36-46 | sources | Removing the last Local leaves its ID first and no undeleted events in it. | [L164](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L164) |
| S36-47 | sources | Calling ensure_local afterward leaves exactly that one Local source. | [L166](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L166) |
| S36-48 | sources | Adding another unnamed Local returns 303 and appends a local source named Local. | [L167](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L167) |
| S36-49 | events | Clicking an event bell opens the reminder popover. | [L183](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L183) |
| S36-50 | events | Clicking event Edit opens the event dialog with a UID-bearing iframe URL. | [L186](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L186) |
| S36-51 | events | Saving the changed title in the embedded editor closes the dialog and updates calendar text. | [L189](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L189) |
| S36-52 | calendar | Opening Print Preview selects the remembered week print view. | [L192](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L192) |
| S36-53 | calendar | Changing the preview to month changes its iframe URL to include view=month. | [L194](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L194) |
| S36-54 | shell | After opening the rule dialog, every help tooltip has no offsetParent. | [L198](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L198) |
| S36-55 | rules | The browser saves Sat/Sun days, color then emoji actions and apply=all. | [L206](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L206) |
| S36-56 | rules | At 390px, the rule dialog width rounds to 390px and its back control is visible. | [L211](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L211) |
| S36-57 | events | At phone width, the synthetic day click navigates to an event URL and displays Back. | [L214](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L214) |
| S36-58 | shell | No browser pageerror events are collected during the sampled interactions. | [L215](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_36.py#L215) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 04/05 and 06/07 pair failure sentinels with RuleError handlers. Row 05 is an `ok(True, ...)` handler marker and cannot fail on its own; do not count S36-05 as independently verifying a requirement. The surrounding exception path supplies the rejection evidence. The latter pair repeats for three invalid rules. Text/day/time/date predicates use finite fixture samples, not exhaustive operators/boundaries.
- Row 13 passes a two-hour no-end default directly to Ruleset; it does not establish environment-file loading. Row 18 tests a specific older migration fixture; later migration refinements also appear in suite 37.
- Row 24's global position check only says the sole Default label occurs after Local's start, not that it is structurally nested there. Row 27 builds a Google body locally; it does not send reminders to Google.
- Print rows 31–34 inspect HTML sheet/grid/text markers, not physical print geometry or each date cell. Row 34's five-column check does not verify weekday labels.
- Row 36 checks redirect/message markup; row 51 separately verifies browser dialog closing. Row 37 samples framing headers on one page rather than every route.
- Row 45 checks stylesheet declarations, not actual wrapped text. Row 46 proves retained Local source/event deletion state, not an explicit default_sid assertion.
- Phone row 56 checks dialog width/back visibility, not full viewport height. Row 57 uses a synthetic day click.
- Overlaps: suites 26/27 rule/template/source operations; suite 37 conflict/link rules; suite 19 event editing; suite 23 framing headers.
