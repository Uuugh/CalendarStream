# Requirements: print

Printing what the user sees. Print is its own feature, used by every section of the page; the feature being printed says what can be printed and supplies the details (which views, which orientation each gets).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| PRT-01 | proposed | Printing anything opens Print Preview, where the user chooses what to print, its theme and its orientation; the printed result shows what the user sees. | — | — |
| PRT-01.a | approved | The print follows what the user sees: the Local or temporary time zone, the time format (TIM-10), the language and the active filter (UI-21). (Developer, Nov 17) | — | Developer, Nov 17 |
| PRT-01.b | proposed | The user's print choices (what to print, theme, orientation) are user settings (SET-01), and Print Preview opens with them; before any are saved, it starts with what is on screen. | — | S36-30, S36-52, S36-53, readme_gaps:52, changelog_gaps_1201-1500:16 |
| PRT-01.c | proposed | The orientation is one segmented choice in Print Preview: Auto, Landscape or Portrait. Auto is chosen from what is printed; the feature being printed says which orientation each kind of content gets (CAL-05.a). | — | S65-18..22 |
| PRT-01.d | approved | Each print sheet fits one page of the paper: Letter for English, A4 otherwise. A day or page that would not fit gets smaller type, and whole titles wrap. | — | theme.md Clarifications (Print) |
| PRT-01.i | approved | The paper's margins are 5 mm. | — | theme.md Clarifications (Print) |
| PRT-01.e | proposed | Printed titles wrap to show the complete title. | — | changelog_gaps_301-600:20 |
| PRT-01.f | approved | A print honors the theme the user chose: Light prints on white paper and Dark on dark paper. | — | S36-32 |
| PRT-01.g | proposed | Print Preview opens as a dialog (UI-01 to UI-03), and a date range in it, where the content has one, is the shared control (UI-23). | — | — |
| PRT-01.h | planned | Every section of the page can be printed; each section says what is printed and its orientation (PRT-01.c). The print layout of All Rules, Event Templates and History is still to be designed. | — | Developer, Nov 19 |
