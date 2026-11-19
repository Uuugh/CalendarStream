# Requirements: Event templates

Statuses: verified, built, open, planned (approved, not built yet) and proposed (drafted, not yet reviewed by the Developer).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| TPL-01 | proposed | An event template is a reusable event that the user saves once and uses for new events and for rules. | — | — |
| TPL-01.a | proposed | A template stores a title, a duration, a color, a location and notes, and a saved template keeps its duration, color and location exactly. | — | S26-14, S26-15 |
| TPL-01.b | proposed | A duration is accepted as `1:30`, `2`, `1.5`, `90m` or `1h15` (90, 120, 90, 90, 75 minutes); a duration that is not a time (`x`) is not valid (UI-19). | — | S26-16, S26-17 |
| TPL-01.c | proposed | Saving normalizes a template: an invalid ID is ignored, runs of spaces in the title collapse, a duration under five minutes is raised to five. | — | S77-17 |
| TPL-02 | proposed | Templates are listed in their own section and offered when the user adds an event. | — | — |
| TPL-02.a | proposed | Event Templates is a section listing the templates with their count and a way to add one (UI-05). | — | S44-32, S46-26, S38-01 |
| TPL-02.b | proposed | Choosing a template in the new-event editor fills the title, location and end time. | — | S57-25, S26-29 |
| TPL-02.c | proposed | A calendar's saved events do not offer a template picker (only new events do). | — | S57-01, S57-07 |

