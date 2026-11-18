# DRAFT requirements: search (for the Developer's review)

Not approved. New top-bar feature (Developer, Nov 17): Search moves out of the calendar to the top bar, to the left of the language
control, and searches all features. Prefix SRH. Replaces CAL-47 to CAL-51 and the search position in CAL-03.

| ID | status | statement | evidence |
|---|---|---|---|
| SRH-01 | proposed | Search is in the top bar, left of the language control. It finds the words typed in the names, titles and text of events, rules, calendars, feeds, event templates and History, and shows which feature each result belongs to; choosing a result opens it. | Developer |
| SRH-02 | proposed | Search shows a result count and the items matching the query; a query with no matches shows "Nothing found". | S46-07, S46-08, S46-10, S46-12 |
| SRH-03 | proposed | Event results can be narrowed by calendar and by date; the From and To date fields show hints in the date's format. | S46-09 |
| SRH-04 | proposed | Search keeps the typed query while its results update (UI-13). | S46-13 |
| SRH-05 | proposed | Closing search returns to what was showing before. | S46-14 |
| SRH-06 | proposed | Search finds an event however far ahead it is (an event 700 days ahead is found without date limits). | S49-35 |
| SRH-07 | proposed | Search looks at everything: it ignores the Calendar filter (Developer, Nov 17). | Developer |
| SRH-08 | proposed | Results are grouped by feature, calendar events first. Each feature shows its first six results; the user can ask for more in steps of the same size. The size (six by default) is a setting (SET-48). (Developer, Nov 17) | Developer |
