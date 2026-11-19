# Requirements: print

Printing what the user sees. Print is its own feature, used by every section of the page; the feature being printed says what can be printed and supplies the details (which views, which orientation each gets).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| PRT-01 | proposed | Printing anything opens Print Preview, where the user chooses what to print, its theme and its orientation; the printed result shows what the user sees. | — | — |
| PRT-01.a | backlog | The print follows what the user sees: the Local or temporary time zone, the time format (TIM-10), the language and the active filter (UIC-21). | — | Developer, Nov 17 |
| PRT-01.b | proposed | The user's print choices (what to print, theme, orientation) are user settings (SET-01), and Print Preview opens with them; before any are saved, it starts with what is on screen. | — | S36-30, S36-52, S36-53, readme_gaps:52, changelog_gaps_1201-1500:16 |
| PRT-01.c | proposed | The orientation is one segmented choice in Print Preview: Auto, Landscape or Portrait. Auto is chosen from what is printed; the feature being printed says which orientation each kind of content gets (CAL-05.a). | — | S65-18..22 |
| PRT-01.d | backlog | Each print sheet fits one page of the paper: Letter for English, A4 otherwise. A day or page that would not fit gets smaller type, and whole titles wrap. | — | theme.md Clarifications (Print) |
| PRT-01.i | backlog | The paper's margins are 5 mm. | — | theme.md Clarifications (Print) |
| PRT-01.e | proposed | Printed titles wrap to show the complete title. | — | changelog_gaps_301-600:20 |
| PRT-01.f | backlog | A print honors the theme the user chose: Light prints on white paper and Dark on dark paper. | — | S36-32 |
| PRT-01.g | proposed | Print Preview opens as a dialog (UIC-01 to UIC-03), and a date range in it, where the content has one, is the shared control (UIC-23). | — | — |
| PRT-01.h | proposed | Every section of the page can be printed; each section says what is printed and its orientation (PRT-01.c). The print layout of All Rules, Event Templates and History is still to be designed. | — | Developer, Nov 19 |
| PRT-02 | proposed | The calendar prints pages of days, weeks and months from a date range, as the rows below say. | — | R2 gap |
| PRT-02.a | proposed | Week prints one page for each week, Sunday to Saturday, from the week that contains From until a week starts after To, up to the page limit in DEF-01. | — | R2 gap |
| PRT-02.b | proposed | 5-day prints the same weeks as Week, Monday to Friday, up to the page limit in DEF-01. | — | R2 gap |
| PRT-02.c | proposed | Day prints one page for each day from From through To, up to the page limit in DEF-01. | — | R2 gap |
| PRT-02.d | proposed | Print Preview has an Include weekends choice (msg:includeWeekends), on until changed; turned off, Week, Month and Itinerary leave out Saturday and Sunday, and Day and 5-day print as before. | — | R2 gap |
| PRT-02.e | proposed | Week, 5-day, Day and Itinerary pages show each event's location after " · " and, when there is more than one calendar, the calendar's name after " · "; Month pages show neither. | — | R2 gap |
| PRT-02.f | proposed | A Week or Month page's title is the calendar's title for that week or month; a Day page's title is the day's title (CAL-01.q). | — | R2 gap |
| PRT-02.g | proposed | A Day page with no events shows msg:noEvents. | — | R2 gap |
| PRT-02.h | proposed | A printed Month shades the days outside its month. | — | R2 gap |
| PRT-02.i | proposed | From starts as the 1st of the current month and To as the last day of From's month, in the displayed zone. | — | R2 gap |
| PRT-02.j | proposed | The range reaches at most the number of days in DEF-01 after From. | — | R2 gap |
| PRT-02.k | proposed | Print type scales with the sheet so the preview and the paper look alike; the heading is the heading size in DEF-01 times the base size. | — | R2 gap |
| PRT-02.l | proposed | The background colors of a print are printed exactly. | — | R2 gap |
| PRT-02.m | proposed | A printed event is tinted by its own color or its rule's color; an event from United's schedule without one by its calendar's color; an event added here or by a rule has the custom look (THM-10.b); a hidden event is struck through at the printed hidden opacity (THM-10.c). | — | R2 gap |
