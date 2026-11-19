# Requirements: calendar

Month, week, day and list views, the stretch bar, print. Issues against this feature (kept in the issues database): I43, I44, I49 (stretch), I35 and I46 (icon alignment).

Terms: the **Local time zone** is defined in TIM-03; an **event line** is one event's line height, with its padding and margins, defined in the theme; **Itinerary** is a printed list of events grouped by day.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CAL-01 | proposed | The calendar shows the user's events in the view the user chooses and lets them move to any date. | — | — |
| CAL-01.a |  | The calendar displays the events of its source calendars, as far as the Calendar filter (FLT-01) and event visibility (CAP-02) allow. | — | S26-12 |
| CAL-01.b |  | Month, Week, 5-day (Monday through Friday), Day and List can be selected from the shared dropdown (UI-12); the chosen view is indicated as selected. Week, 5-day and Day provide an hourly view. | — | S26-60, S64-01, S64-03, S67-35, S67-40, S33-16, S33-17 |
| CAL-01.c |  | Week view shows its date range and navigates backward and forward by one week. | — | S26-61 |
| CAL-01.d |  | Selecting a month and year navigates the calendar to that month and year; date selection follows UI-09. | — | S21-01, S21-02, S21-03 |
| CAL-01.e | proposed | Today returns the main calendar to the current month. | — | changelog_gaps_2101-2336:35 |
| CAL-01.f | proposed (?) | On a phone, the calendar initially uses List view before the user chooses a view. Should the initial choice follow available window space rather than device type under UI-14? | — | changelog_gaps_1501-1800:18 |
| CAL-01.g | proposed | A day cell shows how many of its visible events do not fit; event visibility follows CAP-02 and the Calendar filter. | — | changelog_gaps_301-600:15 |
| CAL-02 | proposed | The calendar shows times in the Local time zone (TIM-03), and the user can look at another zone for a while. | — | — |
| CAL-02.a |  | Selecting a time zone in the calendar's own picker shows event times in that zone as a temporary view change; the Time Zones setting (SET-47) is not changed. | — | S19-31; Developer, Nov 17 |
| CAL-03 | proposed | The user can move an event they may edit by pressing and dragging it. | — | — |
| CAL-03.a |  | A long-press-drag moves an event, for the events that can be edited (CAP-01). | — | F61 |
| CAL-03.b |  | In Week and Day the start snaps to the drag step in DEF-01. | — | — |
| CAL-03.c |  | In Month the event moves to the day it is dropped on and keeps its time. | — | — |
| CAL-03.d |  | The press must be held for the long-press time set in Settings > Theme (SET-62, DEF-01). | — | — |
| CAL-04 | proposed | The user can change how tall the calendar is, and Full page gives it the whole window. | — | — |
| CAL-04.a | planned | A Full page icon sits right of Print, in the calendar header's right zone; it hides every other section and becomes an Exit full page icon (the arrows-inward icon, not Back). Full page always resizes to the available window; that is its definition. | — | F15.4; S64-04, S65-10, S65-12, S65-13, S65-33, S67-41 |
| CAL-04.b |  | The calendar uses the shared resize bar (UI-16). Its height is measured in event lines, not pixels, changes by whole lines, is saved, and has no fixed pixel minimum or maximum. | — | Developer, Nov 17; S64-06, S79-06, S79-07, S79-08 |
| CAL-04.c |  | Collapse gives the fewest lines the view needs; Expand gives the most lines that fit the visible window. | — | — |
| CAL-04.d |  | The hour height in Week and Day is measured in event lines per hour, changed by whole lines and saved, within the limits in DEF-01, so a line of an event always fits. | — | Developer, Nov 17; S65-14, S65-15 |
| CAL-04.e | proposed | Full page also hides the page footer. | — | changelog_gaps_1-300:36 |
| CAL-05 | proposed | The user can print the calendar through Print Preview (UI-22). | — | — |
| CAL-05.a |  | Until the user chooses an orientation it is automatic: landscape for Month, Week and 5-day sheets, portrait for Day and Itinerary sheets (UI-22.c). | — | S65-18..22 |
| CAL-05.b | proposed | The views that can be printed are the calendar's views (CAL-01.b) and Itinerary, which lists events grouped by day. | — | S36-33, readme_gaps:53, changelog_gaps_1201-1500:16 |
| CAL-05.c |  | Printing two months produces a sheet for each month. | — | S36-32 |
| CAL-05.d | proposed | Print All sets the date range (UI-23) from the first event through the last event. | — | readme_gaps:52 |
| CAL-05.e | proposed | Printing one event uses Day view for that print and keeps the remembered print choices (EVT-03, UI-22.b). | — | changelog_gaps_301-600:43 |
| CAL-06 | proposed | The calendar header's right zone holds the view controls in a fixed order, and what the user chooses with them stays on the device until the user changes it. | — | — |
| CAL-06.a | proposed | The right zone holds, in this order: Time Zone, View, 12/24 clock, Print, Full page. Zone alignment and stacking follow UI-14; what each control does is in its own requirement (CAL-02.a, CAL-01.b, TIM-10, CAL-05, CAL-04). | — | theme.md 13c (to confirm) |
| CAL-06.b | proposed | The state of each right-zone control that holds one (the time zone, the view, the time format, Full page) is kept on the device until the user changes it (SET-06). A default is stated in the control's own requirement. | — | Developer, Nov 18 |

## Notes from the draft

### Shared UI and owning-feature references

These are evidence mappings, not duplicate CAL requirements. Shared behavior is defined once in
[common.md](common.md); event behavior is owned by [events.md](events.md) and the existing
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

### Not requirements

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

### Coverage and remaining questions

All 131 calendar-candidate inventory rows are accounted for in 38 proposed requirements,
11 owning-feature/shared-UI reference groups, or the 23 exclusions above. This is static evidence reconciliation; no suites were run locally.
Related event editing, source configuration and publishing behaviors remain with their owning feature drafts.
The questions in proposed rows require review; existing CAL-07/CAL-08 disagree about leaving Full page,
and the draft preserves the later asserted persistence rather than silently approving either statement.
