# Requirements: Event templates

Statuses: verified, built, open, planned (approved, not built yet) and proposed (drafted, not yet reviewed by the Developer).

| ID | status | statement | test | was |
|---|---|---|---|---|
| TPL-01 | proposed | A template stores a title, a duration, a color and a location (and notes). A saved template keeps its duration, color and location exactly (45 minutes, gray, "Desk"). | — | S26-14, S26-15 |
| TPL-02 | proposed | A duration is accepted as `1:30`, `2`, `1.5`, `90m` or `1h15` (90, 120, 90, 90, 75 minutes); a duration that is not a time (`x`) is refused (400). | — | S26-16, S26-17 |
| TPL-03 | proposed | Saving normalizes a template: an invalid ID is ignored, runs of spaces in the title collapse, a duration under five minutes is raised to five. | — | S77-17 |
| TPL-04 | proposed | Event Templates is a section listing the templates with their count and a way to add one (UI-05). | — | S44-32, S46-26, S38-01 |
| TPL-05 | proposed | Choosing a template in the new-event editor fills the title, location and end time. | — | S57-25, S26-29 |
| TPL-06 | proposed | A rule's "Add event" action can use a template; naming a template that does not exist (with no title) is refused (400). | — | S26-26, S37-38 (also RUL-17, RUL-23) |
| TPL-07 | proposed | A calendar's saved events do not offer a template picker (only new events do). | — | S57-01, S57-07 |
