# DRAFT requirements: event_templates (for the Developer's review)

Not approved. From the `event_templates` rows of `requirements/inventory/` (suites 12-71) plus rows that use a
template picker. An event template is an event not assigned to a date: title, duration, color, location, notes. Only
17 inventory rows are about it, so the feature is small. "Template" in the inventory also means Python HTML templates;
those rows (S35, S39-05, S44-39, S62-12/14/15/16/17, S63-25, S66-19, S67-04) test the Python implementation and are not
requirements.

| ID | status | statement | evidence |
|---|---|---|---|
| TPL-01 | proposed | A template stores a title, a duration, a color and a location (and notes). A saved template keeps its duration, color and location exactly (45 minutes, gray, "Desk"). | S26-14, S26-15 |
| TPL-02 | proposed | A duration is accepted as `1:30`, `2`, `1.5`, `90m` or `1h15` (90, 120, 90, 90, 75 minutes); a duration that is not a time (`x`) is refused (400). | S26-16, S26-17 |
| TPL-03 | proposed | Saving normalizes a template: an invalid ID is ignored, runs of spaces in the title collapse, a duration under five minutes is raised to five. | S77-17 |
| TPL-04 | proposed | The Event Templates section has a count box and a plus; the plus opens a dialog (one tag row to start); the section behavior is UI-05. | S44-32, S46-26, S38-01, S38-13 |
| TPL-05 | proposed | Choosing a template in the new-event editor fills the title, location and end time and closes the template menu. | S57-25, S26-29 |
| TPL-06 | proposed | A rule's "Add event" action can use a template; naming a template that does not exist (with no title) is refused (400). | S26-26, S37-38 (also RUL-17, RUL-23) |
| TPL-07 | proposed | A calendar's saved events do not offer a template picker (only new events do). | S57-01, S57-07 |

Counted elsewhere: the section frame, count box and expand behavior are shared with Rules (RUL-41) and belong to the
shell's section component. The color of the Templates section header is a theme token (S61-16).
