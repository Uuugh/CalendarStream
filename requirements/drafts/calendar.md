# DRAFT requirements: calendar (for the Developer's review)

Not approved. Derived from every inventory row whose candidate feature includes `calendar`,
using the merged inventory at `93444563b74f520dc0fd1fe8e1f8d7d9e4b834a2`.
IDs continue after CAL-15 in `requirements/calendar.md`; they do not change existing requirement statuses.
Evidence keys link conceptually to `requirements/inventory/suite_NN.md`, which retains pinned source anchors,
fixture setup and coverage limits. These are proposed rules, not claims of new runtime verification.

Compound rows may support both behavior and presentation. The statements retain only the user behavior;
pixel dimensions and implementation details are not promoted to requirements. Uncertain generalizations
remain questions. Questions explicitly identify uncertain generalization or conflicting existing requirements.

| ID | status | statement | evidence |
|---|---|---|---|
| CAL-19 | proposed | Local time: the calendar shows event times in the Local time zone, set in Settings > Time Zones (SET-47): the zone of the device in use, or a fixed zone. Existing events are viewed with the offset of that zone, while each event keeps, unchanged in the database, the time zone it was created in until the user edits it with Edit Event. (Developer, Nov 17) | S19-01 |
| CAL-20 | proposed | Automatic time format uses 12-hour times when the page language is English. | S19-02 |
| CAL-21 | proposed | Choosing 24-hour format saves it and displays 24-hour event times. Choosing 12-hour format saves that choice again. | S19-03, S19-04, S21-08, S21-09, S79-12, S79-13 |
| CAL-22 | proposed | The selected time format is indicated as 12 or 24 hours. | S21-05, S21-07, S66-16, S79-10, S79-11 |
| CAL-23 | proposed | An unknown time-format choice is refused. | S19-09 |
| CAL-24 | proposed | An unknown display time zone is refused. | S19-30 |
| CAL-25 | proposed | Selecting a Local time zone shows event times in that zone (see CAL-19). | S19-31 |
| CAL-27 | proposed | Selecting a month and year navigates the calendar to that month and year; date selection follows UI-09. | S21-01, S21-02, S21-03 |
| CAL-30 | proposed | The calendar displays its source calendars’ events. | S26-12 |
| CAL-33 | proposed | Month, Week, Day and List can be selected; the choice is saved and indicated as selected. Week and Day provide an hourly view. | S26-60, S64-01, S64-03, S67-35, S67-40, S33-16, S33-17 |
| CAL-34 | proposed | Week view shows its date range and navigates backward and forward by one week. | S26-61 |
| CAL-35 | proposed (?) | The sampled week header omits the redundant “times in” and event-count wording. Is this omission intended for every view? | S26-62 |
| CAL-37 | proposed (?) | The key omits separate Timed, All-day and Added here color labels in the sampled views. Should this apply to every key variant? | S34-04, S45-25 |
| CAL-38 | proposed | Changing a source name updates its name in the calendar key. | S34-16 |
| CAL-39 | proposed | Saving print preferences remembers the selected view, weekend choice, theme and automatic orientation. | S36-30 |
| CAL-40 | proposed | Week printing with weekends off includes five days and uses the saved print theme. | S36-31, S36-34 |
| CAL-41 | proposed | Printing two months produces a sheet for each month and honors the requested weekend and theme choices. | S36-32 |
| CAL-42 | proposed | Itinerary printing includes events grouped by day. | S36-33 |
| CAL-43 | proposed | Print Preview opens with the remembered print view; choosing Month updates its preview to Month. | S36-52, S36-53 |
| CAL-45 | proposed | Changing a source's color updates it wherever it is shown (the calendar key and the destination source choices). | S38-16 |
| CAL-47 | proposed | Search displays a result count and events matching the query; a query with no matches displays Nothing found. | S46-07, S46-08, S46-10, S46-12 |
| CAL-48 | proposed | Search can narrow results by source and date; the sampled filters reduce the nonempty result set. | S46-09 |
| CAL-49 | proposed | Search keeps the typed query while its results update. | S46-13 |
| CAL-50 | proposed | Leaving search restores the month calendar. | S46-14 |
| CAL-51 | proposed | Search without date bounds can find an event 700 days ahead. | S49-35 |
| CAL-53 | proposed | The calendar can be viewed Full page and returned to normal view. Shared navigation follows UI-02. | S64-04, S65-10, S65-12, S65-13, S65-33, S67-41 |
| CAL-54 | proposed | Calendar-key hidden choices are saved and kept when leaving Full page (the Developer, Nov 17: CAL-07 and CAL-08 are reconciled to this). | S64-05, S64-07, S65-08 |
| CAL-55 | proposed | View All is absent when nothing is dimmed, appears after dimming a calendar, restores it, and disappears again after restoration. Clearing hidden choices saves an empty selection. | S65-09, S67-52, S67-53, S67-54, S67-55 |
| CAL-56 | proposed | Calendar-key visibility choices can be changed in both normal and Full page modes. | S65-32, S67-42 |
| CAL-57 | proposed (?) REWORK BY DEVELOPER | The calendar stretch amount is saved for the sampled negative values -300 and -120; -301 is refused, and a request for 1500 is limited to at most 1200. Are the complete accepted range and clamping rules intended to be specified beyond these samples? | S64-06, S79-06, S79-07, S79-08 |
| CAL-58 | proposed | The calendar height and Week-view hour height can be adjusted. | S67-50, S79-01, S79-02, S65-16 |
| CAL-59 | proposed (?) REWORK BY DEVELOPER | An hour height of 64 is saved; heights 10 and 500 are refused. What is the complete accepted hour-height range? | S65-14, S65-15 |
| CAL-60 | proposed | For the sampled month print requests, automatic or unspecified orientation selects landscape; explicit portrait or landscape is honored. Day printing also honors explicit landscape. | S65-18, S65-19 |
| CAL-61 | proposed | Print orientation can be chosen and saved; a later request without an orientation uses the saved portrait preference. | S65-20, S65-21, S65-22 |
| CAL-62 | proposed (?) | For Letter and A4, the sampled month print produces one landscape PDF page and the sampled day print starts with a portrait PDF page; the sampled Letter week print has at least two pages. Are these pagination expectations specific to the fixture content? | S64-08, S64-09, S64-10 |
| CAL-63 | proposed (?) | The sampled portrait month print produces one portrait PDF page. Is single-page output required only for this fixture size? | S65-23 |

## Shared UI and owning-feature references

These are evidence mappings, not duplicate CAL requirements. Shared behavior is defined once in
[shared_ui.md](shared_ui.md); event behavior is owned by [events.md](events.md) and the existing
[events requirements](../events.md). Removed draft IDs remain reserved for review continuity.

- Former CAL-16: S18-19, S18-20, S18-21 → UI-01 and UI-02 (event details/dialog lifetime). The click-outside persistence observation is retained as an open shared-dialog question, rather than restated here.
- Former CAL-17: S18-22 → EVT-04 (new event for a selected day).
- Former CAL-18: S18-18 → UI-02 (Close), EVT-19 (reminders) and EVT-04 (Add event). Old pin replacement is presentation history.
- Former CAL-28: S21-04 → UI-09 (date selection). Outside-click dismissal is an open shared-picker question; it is not a second calendar rule.
- Former CAL-29: S21-06, S21-22, S64-02 → UI-07 (explanatory help). Calendar/Key grouping is presentation; no new help mechanic is defined here.
- Former CAL-31: S26-57, S39-20 → Events owns event tools; see EVT-23 and UI-02. Editor/Delete availability evidence is retained for its review.
- Former CAL-32: S39-21 → Events owns generated-event tools; see EVT-07. Copy-only availability is retained as an events coverage question, not duplicated here.
- Former CAL-44: S37-16 → EVT-30 (saved event link).
- Former CAL-46: S44-42, S45-21, S50-02, S65-07 → EVT-21 and EVT-22 (deletion/restoration). The imported-event tombstone/deletion-note observations remain evidence for events reconciliation; these references do not claim those drafts already specify every detail.
- Former CAL-52: S57-32, S57-39 → Existing planned EVT-03 (event printing); UI-01 and UI-02 govern dialog layers. No implementation or approval status is inferred.
- Former CAL-64: S67-36, S67-37, S67-39 → Shared menu mechanics. Open/choose/dismiss evidence is retained for shared UI review; UI-02 covers layer dismissal, but a general menu rule is still an open shared-UI question.

Other shared-UI observations retained in the table evidence (not separate calendar rules): CAL-22’s
switch/tooltip mechanics, CAL-27’s selection mechanics, CAL-49’s keyboard focus, and CAL-53/CAL-56’s
pressed-state mechanics belong to shared UI. CAL-58 retains only height adjustment, not the widget type.
Shared UI does not yet explicitly state every one of these mechanics; Claude can reconcile them in its
shared-UI ownership review. This PR changes only calendar.md, as scoped by the Developer.

## Not requirements

These rows are accounted for but do not independently establish a user-facing requirement.
Pure geometry and appearance decisions belong to `build_rules/theme.md`.

- S34-05: Print-button/CSS media-block presence only; does not execute printing.
- S34-06: Computed color equality is a theme assertion.
- S39-12: Python event-tool template/placeholder structure, not an exercised user action.
- S44-25: Pixel alignment belongs to theme rules; presence of a Link tool is also observed, but this compound geometry row does not exercise linking.
- S44-44: Today-cell shadow thickness is a theme measurement.
- S45-24: Class/color-variable implementation check; it does not compare rendered user behavior.
- S46-11: Control offsets and alignment are theme measurements.
- S46-27: Event-control rectangle alignment is a theme measurement.
- S58-26: Padding and icon inset are theme measurements.
- S62-14: Source-string checks for hide/deletion labels do not execute behavior.
- S65-11: Absence of an ID in a page substring is an implementation-placement check.
- S65-17: CSS source declarations, not runtime behavior.
- S65-30: Viewport scroll dimensions are layout measurements.
- S65-31: Calendar width threshold is a layout measurement.
- S65-38: Rounded icon top-coordinate spread is a layout measurement.
- S66-24: Touch handler strings in source do not prove swipe behavior.
- S67-34: Control IDs and absence of an obsolete native picker are implementation structure.
- S67-38: Icon x-coordinate equality is a layout measurement.
- S67-51: Legend separator gap is a pixel measurement.
- S79-03: Grip-dot class and circle count specify visual implementation.
- S79-04: Element type and obsolete spelling are implementation structure.
- S79-05: Absent CSS selector spelling does not prove grip independence.
- S79-09: Absent obsolete control ID is implementation structure.

## Coverage and remaining questions

All 131 calendar-candidate inventory rows are accounted for in 38 proposed requirements,
11 owning-feature/shared-UI reference groups, or the 23 exclusions above. This is static evidence reconciliation; no suites were run locally.
Related event editing, source configuration and publishing behaviors remain with their owning feature drafts.
The questions in proposed rows require review; existing CAL-07/CAL-08 disagree about leaving Full page,
and the draft preserves the later asserted persistence rather than silently approving either statement.
