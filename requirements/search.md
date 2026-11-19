# Requirements: search

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| SRH-01 | proposed | Search finds the user's data across the page and shows what it finds as it arrives. | — | — |
| SRH-01.a | backlog | Search is in the top bar, left of the language control. It finds the words typed in the names, titles and text of events, rules, calendars, feeds, event templates and History, and shows which feature each result belongs to; clicking a result takes the user there. | — | Developer |
| SRH-01.b | backlog | Search looks at everything: it ignores the Calendar filter. | — | Developer |
| SRH-01.c | proposed | Search finds an event however far ahead it is, with no date limit of its own; recurring events are searched over the expansion period in DEF-01. | — | S49-35 |
| SRH-01.d | proposed | Search shows a result count and the items matching the query; a query with no matches shows "Nothing found". | — | S46-07, S46-08, S46-10, S46-12 |
| SRH-01.e | proposed | Event results can be narrowed by calendar and by a date range (UIC-23). | — | S46-09 |
| SRH-01.f | proposed | Search keeps the typed query while its results update (UIC-13). | — | S46-13 |
| SRH-01.g | proposed | Closing search returns to what was showing before. | — | S46-14 |
| SRH-02 | proposed | Results are grouped by feature, and the user can ask for more. | — | — |
| SRH-02.a | backlog | Results are grouped by feature, calendar events first. Each feature shows its first results, the number in DEF-01; the user can ask for more in steps of the same size. The size is set in SET-02. | — | Developer |
| SRH-02.b | backlog | Results show as they populate: the list fills in while the user types and as each feature answers, calendar events first (SRH-02), without waiting for all features to finish (UIC-13). | — | Developer, Nov 17 |

