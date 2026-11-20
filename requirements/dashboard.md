# Requirements: dashboard

The Scrum dashboard: one app where the Product Owner and the team see the backlog, build a sprint, follow its progress and compare agent usage with the estimate.

Terms. A **backlog item** is a requirement whose status is `backlog` (a blank status counts as `backlog`) or an issue, that no story of the sprint names. A **sprint** is the stories chosen to be built next, kept in `SCRUM.d/sprint.md`. A **story** names the requirement and issue IDs it will meet, and has a **stage**: Backlog, Ready, Build, Test, Review or Done, in that order. **Usage** is the agent work a story has used, and the **estimate** is the usage planned for it, both counted in **usage points**, the unit defined in DEF-01. A **feature** is the area of one requirements file; an issue's feature is named by its `feature:` label. The **server** is the program of DSH-10 that serves the web app and its data.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| DSH-01 | proposed | The dashboard is one app that runs as a web app and as a desktop app and shows the backlog, the sprint, its progress and its usage. | — | — |
| DSH-01.a | proposed | The dashboard reads and writes only the sprint file and the requirement files in the repository, and reads and writes issues in the issue tracker through the user's own signed-in access; no token or secret is in its code or in the repository. | — | — |
| DSH-01.b | proposed | When the issue tracker cannot be reached, the issue list says why (msg:dshTrackerUnreachable, with the reason as {reason}) and the rest of the dashboard keeps working. | — | — |
| DSH-01.c | proposed | A Reload control (msg:dshReload) reads the sprint file, the requirement files and the issues again. | — | — |
| DSH-01.d | proposed | Every label, heading and note the dashboard shows is a cited message key (rule 14 of `requirements/README.md`) with translations in `requirements/messages/`; the rows below cite them. | — | — |
| DSH-01.e | proposed | The web app and the desktop app get the sprint, the requirements and the issues through the same data interface; the web app's implementation asks the server (DSH-10) and the desktop app's reads the files and runs the issue tracker's commands itself. | — | — |
| DSH-01.f | proposed | When the sprint file or the requirement files cannot be read, the page says why (msg:dshLoadFailed, with the reason as {reason}) and the other lists keep working. | — | — |
| DSH-01.g | proposed | The dashboard's colors come from the theme built from the THM-02 colors, in light and dark; no widget names a color. | — | — |
| DSH-02 | proposed | The sprint file `SCRUM.d/sprint.md` holds the sprint: its goal, its stories, its review and its retrospective. | — | — |
| DSH-02.a | proposed | The file has a Goal line, a Stories table, a Review section and a Retrospective section. | — | — |
| DSH-02.b | proposed | A Stories row has: story ID, title, items (requirement and issue IDs, comma separated), stage, assignee, estimate and usage. | — | — |
| DSH-02.c | proposed | Every change made in the dashboard is written to the file at once, and the goal, review and retrospective text is kept as it was. | — | — |
| DSH-02.d | proposed | When the file does not exist the sprint is empty, and the first change creates the file. | — | — |
| DSH-02.e | proposed | What the dashboard does not edit is written back as it was: text before the Goal line, other sections, headings inside the Review or Retrospective text, and a story row it cannot read. | — | — |
| DSH-03 | proposed | The backlog lists requirements (heading msg:dshRequirements) read from the requirement files, each with its ID, status, statement and feature. | — | — |
| DSH-03.a | proposed | Every row of a feature file in `requirements/` is read, including the files in `connections.d` and `plugins.d`; the README, `oldkey.md` and `open-questions.md` hold no requirements. | — | — |
| DSH-03.b | proposed | A requirement named by a story of the sprint is not in the backlog. | — | — |
| DSH-03.c | proposed | The status filter starts as `backlog`, so a requirement not yet agreed (`proposed`) is listed when the filter selects it. | — | — |
| DSH-03.d | proposed | A requirement's status is shown as a message (msg:dshStatusBacklog, msg:dshStatusProposed). | — | — |
| DSH-04 | proposed | The requirement list and the issue list each have filters by feature, by requirement ID and by status; they are the dashboard's own single-choice filters, not the shared filter (UIC-21). | — | — |
| DSH-04.a | proposed | The feature filter is a dropdown of the features, with All as its start (msg:dshFilterFeature, msg:dshAll). | — | — |
| DSH-04.b | proposed | The requirement filter is a text box that keeps the entries whose requirement ID contains the text, ignoring case (msg:dshFilterRequirement). | — | — |
| DSH-04.c | proposed | The status filter is a dropdown of the statuses of what is listed, with All as its start (msg:dshFilterStatus, msg:dshAll). | — | — |
| DSH-04.d | proposed | The filters combine (an entry must meet all of them) and a list shows how many of its entries are shown out of all (msg:dshShownOf, {shown} the entries shown, {total} all entries). | — | — |
| DSH-04.e | proposed | A filter always shows the value that is applied: a value that no entry has is still offered and shown, and can be changed. | — | — |
| DSH-05 | proposed | The backlog lists issues (heading msg:dshIssues) read from the issue tracker, each with its number, title, status, feature, requirement and assignee. | — | — |
| DSH-05.a | proposed | An issue's status is open or closed (msg:dshStatusOpen, msg:dshStatusClosed), and its status filter starts as open. | — | — |
| DSH-05.b | proposed | An issue's feature is the name after `feature:` in its labels. | — | — |
| DSH-05.c | proposed | An issue named by a story of the sprint (its number written #N in the story's items) is not in the backlog. | — | — |
| DSH-05.d | proposed | An issue's requirement is the ID on the line starting `Requirement:` in its description. | — | — |
| DSH-05.e | proposed | An issue without a feature or a requirement shows a dash in its place. | — | — |
| DSH-05.f | proposed | The issue list holds at most the number of issues in DEF-01, newest first, and says when more exist (msg:dshIssuesTruncated, with the number as {limit}). | — | — |
| DSH-06 | proposed | The sprint board shows the sprint's goal (msg:dshSprintGoal) and one column for each stage, in order, holding the sprint's stories as cards. | — | — |
| DSH-06.a | proposed | A column header shows the stage name and `n / total` (msg:dshColumnCount; the stage names are msg:dshBacklog, msg:dshReady, msg:dshBuild, msg:dshTest, msg:dshReview and msg:dshDone): n is the number of cards in the column and total is the number of cards in the sprint. | — | — |
| DSH-06.b | proposed | A card shows the story ID, its estimate, its title and the assignee's dot. | — | — |
| DSH-06.c | proposed | Each column has its own color, taken from the theme (THM-02), and its cards carry it. | — | — |
| DSH-06.d | proposed | An assignee's dot has one color for that assignee on every card, shows the assignee's name when pointed at, and is empty when the story has no assignee (msg:dshNoAssignee). | — | — |
| DSH-07 | proposed | The Product Owner and the team build the sprint by dragging and dropping. | — | — |
| DSH-07.a | proposed | Dropping a backlog item on a board column adds a story with the item's ID as the story ID and title, and the stage of that column. | — | — |
| DSH-07.b | proposed | Dropping a card on another column sets its stage to that column. | — | — |
| DSH-07.c | proposed | Dropping a card on the backlog list removes the story from the sprint and the item returns to the backlog. | — | — |
| DSH-07.d | proposed | Dropping a card on the column it is in changes nothing. | — | — |
| DSH-08 | proposed | An issue can be entered in the dashboard with a form (msg:dshNewIssue, msg:dshIssueTitle, msg:dshIssueDescription, msg:dshFilterFeature, msg:dshFilterRequirement, msg:dshFilterStatus): a title, a description, and dropdowns for the feature, the requirement and the status. | — | — |
| DSH-08.a | proposed | The requirement dropdown lists the requirements of the chosen feature, and choosing another feature clears it. | — | — |
| DSH-08.b | proposed | The status dropdown offers open and closed and nothing else, and starts as open. | — | — |
| DSH-08.c | proposed | The Save control (msg:dshSave) stays off until the title is filled. | — | — |
| DSH-08.d | proposed | When the issue cannot be created the form stays filled and says why (msg:dshIssueFailed, with the reason as {reason}). | — | — |
| DSH-08.e | proposed | Saving creates the issue in the issue tracker with its `feature:` label (DSH-05.b) and its `Requirement:` line (DSH-05.d). | — | — |
| DSH-08.f | proposed | After saving, the issue list shows the new issue whatever its status. | — | — |
| DSH-08.g | proposed | An issue is created once: when a step after the creation fails, the form says that the issue exists and gives its number (msg:dshIssuePartial, with the number as {number} and the reason as {reason}), and saving again does not create another. | — | — |
| DSH-08.h | proposed | The form has a Cancel control (msg:cancel) that closes it without creating an issue. | — | — |
| DSH-09 | proposed | The dashboard shows each story's usage against its estimate and the sprint's total. | — | — |
| DSH-09.a | proposed | A story's estimate and usage can be changed on its card and are written to the sprint file (DSH-02.c); labels msg:dshEstimate and msg:dshUsage. | — | — |
| DSH-09.c | proposed | A usage panel (msg:dshUsagePanel) lists each story with its usage and estimate as a bar; the bar is in the warn color (THM-02.j) when usage is above the estimate. | — | — |
| DSH-09.d | proposed | The panel's sprint line adds up the estimates and the usage of all the stories (msg:dshSprintTotal). | — | — |
| DSH-10 | proposed | One command starts the server, which serves the web app and gives it the sprint file, the requirement files and the issues over HTTP. | — | — |
| DSH-10.a | proposed | The server listens on the local machine only, at the address and port in DEF-01. | — | — |
| DSH-10.b | proposed | The server answers only these requests: read the sprint file, write the sprint file, list the requirements, list the issues, create an issue; any other request is answered not found. | — | — |
| DSH-10.c | proposed | The server runs the issue tracker's commands with each argument passed separately and never through a shell, and holds no token or secret. | — | — |
| DSH-10.d | proposed | When the issue tracker's command fails, the server answers with its reason and its other answers keep working. | — | — |
| DSH-10.e | proposed | When the web app cannot reach the server it says so (msg:dshServerUnreachable, with the reason as {reason}). | — | — |
