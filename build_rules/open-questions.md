# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-S: later steps


## Q-R: approved rules rows that are really UI mechanics

- **Q-R5** Apply my proposed changes to RUL-37..43 (answer "approve", or name the rows to change)?
  - RUL-37 reword: "Each action asks for what it needs: minutes for Change length, a title or an event template for Add event, a color for Color." (palette part moves to UI-10)
  - RUL-38 drop (unmatched brackets are already refused by RUL-20; the rest is a control mechanic)
  - RUL-39 reword: "A rule shows which calendars it applies to: All, one calendar, or several (with the count)." (stripe is theme)
  - RUL-40 reword: "A rule shows its title (if any), what it does, and its color by name." (truncation/tooltip is theme)
  - RUL-41 reduce to: "How rules work is explained from the rule dialog." (section frame is UI-05)
  - RUL-42 drop (UI-01 covers dialogs at phone width)
  - RUL-43 reword: "An Emoji action lets the user find and choose any emoji by searching." (1000 count is implementation)
  Answer:

## Q-U: shared UI

- **Q-U1** UI-10 (color palette): rules show eleven colors and events twelve. Are they the same set (Google's eleven plus a
  default), or different palettes?
  Answer:

## Q-E: events

- **Q-E1** EVT-25 (Duplicate event) overlaps the planned EVT-01 (Duplicate icon next to Edit, copies to another
  calendar). Merge them into one requirement, or keep both (EVT-25 = duplicate within the calendar)?
  Answer:
