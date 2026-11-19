# Requirements: Event templates

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| TPL-01 | proposed | An event template is a reusable event that the user saves once and uses for new events and for rules. | — | — |
| TPL-01.a | proposed | A template stores a title, a duration, a color, a location and notes, and a saved template keeps its color and location exactly (its duration is normalized by TPL-01.c). | — | S26-14, S26-15 |
| TPL-01.b | proposed | A duration is accepted as hours and minutes in the forms 1:30, 2, 1.5, 90m and 1h15; a duration that is not a time is not valid (UIC-19). | — | S26-16, S26-17 |
| TPL-01.c | proposed | Saving normalizes a template: an invalid ID is ignored, runs of spaces in the title collapse, a duration under the shortest in DEF-01 is raised to it. | — | S77-17 |
| TPL-02 | proposed | Templates are listed in their own section and offered when the user adds an event. | — | — |
| TPL-02.a | proposed | Event Templates is a section (UIC-05) listing the templates. | — | S44-32, S46-26, S38-01 |
| TPL-02.b | proposed | Choosing a template in the new-event editor fills the title, location and end time. | — | S57-25, S26-29 |
| TPL-02.c | proposed | A calendar's saved events do not offer a template picker (only new events do). | — | S57-01, S57-07 |
| TPL-01.d | proposed | A duration is also accepted as h:m, 1h, a decimal with a comma (1,5) and 90min, with at most the hour digits in DEF-01; an empty duration means the default in DEF-01. | — | R3 gap |
| TPL-01.e | proposed | A duration that is not a time is not valid (UIC-19) and shows msg:templateCheckLength ({title} the template's title); an all-day template keeps the default length in DEF-01. | — | R3 gap |
| TPL-01.f | proposed | When stored templates are read back, the title, location and notes are cut to their lengths in DEF-01, a length outside its range becomes the default, and a color that is not a palette color (THM-09) is dropped. | — | R3 gap |
| TPL-01.g | proposed | A template keeps notes; the page does not offer to edit them. | — | R3 gap |
| TPL-02.d | proposed | The Event Templates header has the + of UIC-24, the counts msg:templateAllDayCount and msg:templateTimedCount ({n}), msg:templateCountOne or msg:templateCount ({n}), and when empty msg:noTemplatesYet. | — | R3 gap |
| TPL-02.e | proposed | A template row has a Title field (placeholder msg:templateTitlePlaceholder), a choice of msg:timed or msg:allDay, a Length, a Location, a color or msg:templateCalendarColor, a delete button and a + that adds a row. | — | R3 gap |
| TPL-02.f | proposed | The + opens a dialog titled msg:addEventTemplate whose defaults are Timed, the default length in DEF-01 and no color; saving without a title is not valid (UIC-19) and shows msg:templateGiveTitle. | — | R3 gap |
| TPL-02.g | proposed | At most the number of templates in DEF-01 are kept; one more is not valid (UIC-19) and shows msg:templatesLimit ({n} the limit); rows with an empty title are dropped when saved. | — | R3 gap |
| TPL-02.h | proposed | Removing a template makes the rules that use it stop adding events and leaves the rules; History records the save as msg:templatesSaved ({n} the number of templates). | — | R3 gap |
