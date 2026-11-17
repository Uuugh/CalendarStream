# Suite 65: Calendar carryover, print orientation and editor rows

Source: [`tests/suite_65.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8165; seed.demo; source/Google/update/updater loops patched. HTTP checks include print preference markup and a Chromium-generated Letter PDF inspected with pypdf. A separate 1230×900 browser checks full-page views, legend and editor row alignment; source CSS is also inspected.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S65-01 | events | The sampled editor IDs occur in the asserted date/All-day/time/end-zone sequence. | [L37](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L37) |
| S65-02 | events | The enddate template region contains end label followed by All-day control. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L39) |
| S65-03 | events | New-event Rule-link markup has no disabled attribute. | [L40](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L40) |
| S65-04 | events | The created custom event UID initially appears in its calendar page. | [L46](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L46) |
| S65-05 | events | After deletion, that custom event UID is absent from the page. | [L48](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L48) |
| S65-06 | history | The deleted custom event remains in stored events with a deletion marker. | [L49](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L49) |
| S65-07 | calendar | After deleting an imported event, its title still appears on its date page. | [L52](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L52) |
| S65-08 | calendar | Hiding CCS+ stores its source-hidden key. | [L56](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L56) |
| S65-09 | calendar | Posting the clear-hidden sentinel returns success and stores an empty hidden list. | [L57](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L57) |
| S65-10 | calendar | The full-page control appears in topbar markup before the Settings button. | [L62](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L62) |
| S65-11 | calendar | The sampled calendar-to-footer substring omits the full-page control ID. | [L63](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L63) |
| S65-12 | calendar | Full mode topbar includes the restore-squares icon and pressed=true markup. | [L64](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L64) |
| S65-13 | calendar | After leaving full mode, topbar source contains the fullscreen icon. | [L66](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L66) |
| S65-14 | calendar | Saving hour height 64 returns success and stores 64. | [L69](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L69) |
| S65-15 | calendar | Hour heights 500 and 10 each return 400. | [L70](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L70) |
| S65-16 | calendar | Week markup contains the hour handle, 64px variable and slider role. | [L73](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L73) |
| S65-17 | calendar | The calendar-header CSS contains the two checked tighter-gap declarations. | [L77](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L77) |
| S65-18 | calendar | For four sampled month orientation inputs, print markup has the expected land/port paper value. | [L82](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L82) |
| S65-19 | calendar | An explicit landscape day request has land paper markup. | [L83](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L83) |
| S65-20 | calendar | Saving portrait print preference returns success and stores port orientation. | [L84](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L84) |
| S65-21 | calendar | A later month print request without orientation uses portrait markup. | [L85](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L85) |
| S65-22 | calendar | Page markup contains the orientation toggle and print HTML contains the sampled 5mm landscape page rule. | [L87](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L87) |
| S65-23 | calendar | The generated portrait month PDF has one portrait page with no sampled cell vertical overflow. | [L95](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L95) |
| S65-24 | account | Page source includes the cancel/check icon variables. | [L99](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L99) |
| S65-25 | account | Calendar CSS includes the sampled page-login heading/status-box selectors. | [L100](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L100) |
| S65-26 | settings | Default page markup omits gripsright. | [L103](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L103) |
| S65-27 | settings | Saving right-side grips stores right and adds gripsright page markup. | [L105](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L105) |
| S65-28 | shell | The handle stylesheet contains the right-side module-handle selector. | [L106](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L106) |
| S65-29 | settings | Saving left-side grips removes the override and gripsright markup. | [L108](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L108) |
| S65-30 | calendar | In each of four full-page views, document scroll height/width fit the browser viewport. | [L120](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L120) |
| S65-31 | calendar | In full mode, calendar width is at least 1200px in the 1230px viewport. | [L122](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L122) |
| S65-32 | calendar | Clicking the CCS+ legend control off then on changes its pressed attribute false then true. | [L129](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L129) |
| S65-33 | calendar | Leaving full mode resets pressed=false and the fullscreen icon. | [L131](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L131) |
| S65-34 | events | All-day and Ends label tops are within four pixels. | [L136](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L136) |
| S65-35 | events | Different-end-zone and end-Time label tops are within four pixels. | [L137](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L137) |
| S65-36 | events | Editor row tops order end date, end time then start zone. | [L138](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L138) |
| S65-37 | events | Checking All-day leaves its label visible and hides end time. | [L140](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L140) |
| S65-38 | calendar | The open event has at least four icon tops whose rounded vertical spread is at most two pixels. | [L145](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L145) |
| S65-39 | shell | No browser pageerror events are collected during the sampled interactions. | [L146](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_65.py#L146) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Imported deletion row 07 checks title presence, not strike-through/Restore styling. Hour-bound validation samples 10/500, not exact 20/120 boundary acceptance.
- Orientation row 18 repeats four values. The PDF check covers one month/Letter portrait with DOM cell-overflow checks, not all paper/date/view combinations.
- CSS selectors/variables do not establish Administrator box geometry by themselves. Full-page row 30 repeats four views at one width; no phone/palette loop.
- Legend row 32 checks pressed attributes, not exact event membership. Editor Rule enabled is tested only by absent disabled markup. Row 37 checks end-time hiding, not every time field.
- Overlaps: suite 64 generated PDFs; suite 57 editor fields; suite 67 legend/menu/stretch controls.
