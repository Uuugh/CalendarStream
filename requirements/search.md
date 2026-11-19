# Requirements: search

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | was |
|---|---|---|---|---|
| SRH-01 |  | Search is in the top bar, left of the language control. It finds the words typed in the names, titles and text of events, rules, calendars, feeds, event templates and History, and shows which feature each result belongs to; clicking a result takes the user there. | — | Developer |
| SRH-07 |  | Search looks at everything: it ignores the Calendar filter (Developer, Nov 17). | — | Developer |
| SRH-08 |  | Results are grouped by feature, calendar events first. Each feature shows its first six results; the user can ask for more in steps of the same size. The size (six by default) is a setting (SET-02). (Developer, Nov 17) | — | Developer |
| SRH-09 |  | Results show as they populate: the list fills in while the user types and as each feature answers, calendar events first (SRH-08), without waiting for all features to finish (UI-13). (Developer, Nov 17) | — | Developer, Nov 17 |
| SRH-02 | proposed | Search shows a result count and the items matching the query; a query with no matches shows "Nothing found". | — | S46-07, S46-08, S46-10, S46-12 |
| SRH-03 | proposed | Event results can be narrowed by calendar and by a date range (UI-23). | — | S46-09 |
| SRH-04 | proposed | Search keeps the typed query while its results update (UI-13). | — | S46-13 |
| SRH-05 | proposed | Closing search returns to what was showing before. | — | S46-14 |
| SRH-06 | proposed | Search finds an event however far ahead it is (an event 700 days ahead is found without date limits). | — | S49-35 |
