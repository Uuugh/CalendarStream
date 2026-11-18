# DRAFT requirements: calendar_filter (for the Developer's review)

Not approved. New feature (Developer, Nov 17): the Calendar filter replaces the calendar key and every rule about hiding and showing
events on the calendar. Prefix FLT. It uses the shared multi-select dropdown (UI-12) and the show-at-once rule (UI-13). Replaces
CAL-06, CAL-07, CAL-08, CAL-10, CAL-37, CAL-38, CAL-45 (key part), CAL-54, CAL-55 and CAL-56.

| ID | status | statement | evidence |
|---|---|---|---|
| FLT-01 | proposed | The Calendar filter is one filter icon with a dropdown (UI-12). It lists every calendar with its color and the event states (Edited, Changed by the source since the edit, Hidden from Google, Deleted); choosing items shows only those events. It changes only what the calendar shows: nothing changes in Sources, Feeds, Rules or the other sections. | S34-04, S45-25 |
| FLT-02 | proposed | Select all shows everything and Select none shows nothing (UI-12); the filter shows when it is active. | S65-09, S67-52, S67-53, S67-54, S67-55 |
| FLT-03 | proposed | The filter choices are saved and kept, including when leaving Full page. | S64-05, S64-07, S65-08 |
| FLT-04 | proposed | The filter applies in every view and mode (Month, Week, Day, List, Full page) and Print follows it: what the user chooses to see is what is printed (Developer, Nov 17). | S65-32, S67-42 |
| FLT-05 | proposed | A calendar's name and color in the filter follow its source: renaming it or changing its color shows at once (UI-13). | S34-16, S38-16 |

Not requirements: the old Timed, All-day and Added here color labels are gone (build_rules/theme.md); layout of the old key (columns of
three, the View All eye button) is replaced by the dropdown.
