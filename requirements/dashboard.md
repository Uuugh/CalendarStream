# Requirements: dashboard

The Scrum dashboard: one app where the Product Owner and the team see the backlog, build the sprint by dragging, follow its progress and usage, and see what the agents are doing.

Terms. A **status** is one of `proposed`, `backlog`, `planned` or `done` (`requirements/README.md`, Line format); it says where a requirement or an issue is: not yet agreed, waiting for a story, in a story, or accepted. A **block** is a story, an epic or a sprint, with a name; blocks nest as DSH-06.c says. The **Backlog block** is the first block of the board and holds every requirement and issue whose status is `backlog`. A **story** names the requirements and issues it will meet. **Usage** is the agent work a story has used, and the **estimate** is the usage planned for it, both counted in **usage points**, the unit defined in DEF-01. A **feature** is the area of one requirements file; an issue's feature is named by its `feature:` label. The **server** is the program of DSH-13 that serves the web app and its data. A **progress file** is a file in the progress folder whose name is an agent's label and whose content is `done/total`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| DSH-01 | proposed | The dashboard is one app that runs as a web app and as a desktop app and shows the backlog, the sprint blocks, their usage and the agents' progress. | — | — |
| DSH-01.a | proposed | The dashboard changes only the sprint file, the status cell of a requirement row, the issues and labels of the issue tracker through the user's own signed-in access, and nothing else; it reads the progress files; no token or secret is in its code or in the repository. | — | — |
| DSH-01.b | proposed | When the issue tracker cannot be reached, the issue column says why (msg:dshTrackerUnreachable, with the reason as {reason}) and the rest of the dashboard keeps working. | — | — |
| DSH-01.c | proposed | A Reload control (msg:dshReload) reads the sprint file, the requirement files, the issues and the progress files again. | — | — |
| DSH-01.d | proposed | Every label, heading and note the dashboard shows is a cited message key (rule 14 of `requirements/README.md`) with translations in `requirements/messages/`; the rows below cite them. | — | — |
| DSH-01.e | proposed | The web app and the desktop app use the same data interface; the web app's implementation asks the server (DSH-13) and the desktop app's does what the server does, in its own process. | — | — |
| DSH-01.f | proposed | When the sprint file or the requirement files cannot be read, the page says why (msg:dshLoadFailed, with the reason as {reason}) in the places that need them and the other places keep working. | — | — |
| DSH-01.g | proposed | The dashboard's colors come from the theme built from the THM-02 colors, in light and dark; no widget names a color. | — | — |
| DSH-02 | proposed | The sprint file `SCRUM.d/sprint.md` holds the blocks, which requirements and issues each story holds, the review and the retrospective. | — | — |
| DSH-02.a | proposed | The file has a Blocks table, a Members table, a Review section and a Retrospective section. | — | — |
| DSH-02.b | proposed | A Blocks row has: block ID, kind (story, epic or sprint), name, parent block ID (blank at the top), assignee, estimate and usage. | — | — |
| DSH-02.c | proposed | A Members row has a story's block ID and one item: a requirement ID or an issue number written #N. | — | — |
| DSH-02.d | proposed | Every change made in the dashboard is written to the file at once, and the review and retrospective text is kept as it was. | — | — |
| DSH-02.e | proposed | When the file does not exist the sprint is empty, and the first change creates the file. | — | — |
| DSH-02.f | proposed | What the dashboard does not edit is written back as it was: text before the first table, other sections, headings inside the Review or Retrospective text, and a row it cannot read. | — | — |
| DSH-03 | proposed | The Requirements column lists the requirements read from the requirement files, each with its ID, status, statement and feature. | — | — |
| DSH-03.a | proposed | Every row of a feature file in `requirements/` is read, including the files in `connections.d` and `plugins.d`; the README, `oldkey.md` and `open-questions.md` hold no requirements. | — | — |
| DSH-03.b | proposed | A status is shown as a message (msg:dshStatusProposed, msg:dshStatusBacklog, msg:dshStatusPlanned, msg:dshStatusDone); a blank status counts as `backlog`. | — | — |
| DSH-03.c | proposed | The column's heading is msg:dshRequirements. | — | — |
| DSH-04 | proposed | The Requirements column and the Issues column each have the shared filter (UIC-21) for the feature, for the requirement and for the status. | — | — |
| DSH-04.a | proposed | The feature filter's choices are the features of what the column lists (msg:dshFilterFeature). | — | — |
| DSH-04.b | proposed | The requirement filter's choices are the requirement IDs of what the column lists (msg:dshFilterRequirement). | — | — |
| DSH-04.c | proposed | The status filter's choices are the four statuses (msg:dshFilterStatus). | — | — |
| DSH-04.d | proposed | An entry is listed when it meets all three filters, and the column shows how many entries are listed out of all (msg:dshShownOf, {shown} the entries listed, {total} all entries). | — | — |
| DSH-05 | proposed | The Issues column lists the open issues read from the issue tracker, each with its number, title, status, feature, requirement and assignee; its heading is msg:dshIssues. | — | — |
| DSH-05.a | proposed | An issue's status is the one of its labels `proposed`, `backlog`, `planned` or `done`; an issue with none counts as `backlog`. | — | — |
| DSH-05.b | proposed | An issue's feature is the name after `feature:` in its labels. | — | — |
| DSH-05.c | proposed | An issue's requirement is the ID on the line starting `Requirement:` in its description. | — | — |
| DSH-05.d | proposed | An issue without a feature or a requirement shows a dash in its place. | — | — |
| DSH-05.e | proposed | The issue list holds at most the number of issues in DEF-01, newest first, and says when more exist (msg:dshIssuesTruncated, with the number as {limit}). | — | — |
| DSH-06 | proposed | The board along the top shows the Backlog block, then the blocks of the sprint, then an add control. | — | — |
| DSH-06.a | proposed | The Backlog block (heading msg:dshBacklog) holds the requirements and the issues whose status is `backlog`. | — | — |
| DSH-06.b | proposed | The add control (msg:dshAddBlock) asks which kind of block (msg:dshBlockKind, msg:dshKindStory, msg:dshKindEpic, msg:dshKindSprint) and its name (msg:dshBlockName), and adds the block at the top of the board; its Cancel is msg:cancel and its Save is msg:dshSave. | — | — |
| DSH-06.c | proposed | A story can sit in an epic or in a sprint, an epic can sit in a sprint, and a sprint sits at the top of the board; a block is drawn inside the block it sits in. | — | — |
| DSH-06.d | proposed | A story holds the requirements and the issues that were dropped on it and shows each with its ID or number and title. | — | — |
| DSH-07 | proposed | The Product Owner and the team build the sprint by dragging and dropping. | — | — |
| DSH-07.a | proposed | A block can be dragged onto a block it may sit in (DSH-06.c) and then sits there, written to the sprint file (DSH-02.d). | — | — |
| DSH-07.b | proposed | A block can be dragged to the top of the board and then sits there if it may (DSH-06.c). | — | — |
| DSH-07.c | proposed | A requirement or an issue can be dropped only on the Backlog block or on a story. | — | — |
| DSH-07.d | proposed | Dropping a `proposed` requirement or issue on the Backlog block sets its status to `backlog`. | — | — |
| DSH-07.e | proposed | Dropping a requirement or an issue on a story sets its status to `planned` and records it in the story's Members rows. | — | — |
| DSH-07.f | proposed | Dropping a requirement or an issue that is in a story on the Backlog block removes it from the story's Members rows and sets its status to `backlog`. | — | — |
| DSH-07.g | proposed | A drop that would move a status down in any other way, or that is not allowed by DSH-07.c, changes nothing and says why (msg:dshMoveRefused, with the reason as {reason}). | — | — |
| DSH-07.h | proposed | Dropping something where it already is changes nothing. | — | — |
| DSH-08 | proposed | A story that sits in a sprint has an Accept control (msg:dshAccept). | — | — |
| DSH-08.a | proposed | Accept sets the status of every requirement and issue of the story to `done`. | — | — |
| DSH-08.b | proposed | A story that does not sit in a sprint has no Accept control. | — | — |
| DSH-09 | proposed | The Issues column has a New issue control (msg:dshNewIssue) that opens a form to enter an issue: a title, a description, and dropdowns for the feature, the requirement and the status. | — | — |
| DSH-09.a | proposed | The form's requirement dropdown lists the requirements of the chosen feature, and choosing another feature clears it. | — | — |
| DSH-09.b | proposed | The status dropdown offers the four statuses and nothing else, and starts as `backlog`. | — | — |
| DSH-09.c | proposed | The Save control (msg:dshSave) stays off until the title is filled; the form's labels are msg:dshIssueTitle, msg:dshIssueDescription, msg:dshFilterFeature, msg:dshFilterRequirement and msg:dshFilterStatus. | — | — |
| DSH-09.d | proposed | Saving creates one issue in the issue tracker with the label `issue`, its `feature:` label (DSH-05.b), its status label (DSH-05.a) and its `Requirement:` line (DSH-05.c). | — | — |
| DSH-09.e | proposed | When the issue cannot be created the form stays filled and says why (msg:dshIssueFailed, with the reason as {reason}). | — | — |
| DSH-09.f | proposed | The form has a Cancel control (msg:cancel) that closes it without creating an issue. | — | — |
| DSH-09.g | proposed | After saving, the new issue is listed in the Issues column. | — | — |
| DSH-10 | proposed | The dashboard shows usage against estimate on every story and sprint block. | — | — |
| DSH-10.a | proposed | A story's estimate and usage can be changed on its block and are written to the sprint file (DSH-02.d); labels msg:dshEstimate and msg:dshUsage. | — | — |
| DSH-10.b | proposed | A sprint or an epic shows the sum of the estimates and the sum of the usage of the stories it holds. | — | — |
| DSH-10.c | proposed | Each of these blocks shows its usage and estimate as a bar, in the warn color (THM-02.j) when usage is above the estimate. | — | — |
| DSH-11 | proposed | The page fits the window and every part of it scrolls on its own. | — | — |
| DSH-11.a | proposed | The page itself does not scroll: the board takes the share of the window's height in DEF-01 and the columns below it take the rest. | — | — |
| DSH-11.b | proposed | Each column, and each block's contents, has its own vertical scrollbar when its content is longer than its area. | — | — |
| DSH-11.c | proposed | Nothing is clipped or overflows at the window sizes in DEF-01. | — | — |
| DSH-12 | proposed | The Agent progress column (heading msg:dshAgentProgress) shows the usage chart (DSH-14) and then one bar for each progress file the server reads. | — | — |
| DSH-12.a | proposed | A bar shows the file's name as the label, the fraction `done/total` as the bar and the text `done/total`. | — | — |
| DSH-12.b | proposed | With no progress folder, or none with a progress file, the column is empty and says so (msg:dshNoProgress). | — | — |
| DSH-12.c | proposed | The bars are read again at the interval in DEF-01 and on Reload (DSH-01.c). | — | — |
| DSH-12.d | proposed | A progress file whose content is not `done/total` shows no bar. | — | — |
| DSH-13 | proposed | One command starts the server, which serves the web app and gives it the data over HTTP; the progress folder is given with `--progress <dir>`. | — | — |
| DSH-13.a | proposed | The server listens on the local machine only, on the port given with `--port` (it starts as the port in DEF-01), and answers only a request whose Host is that address or `localhost` and whose Origin, when present, matches it. | — | — |
| DSH-13.b | proposed | The server answers only these requests: read and write the sprint file, list the requirements, set a requirement's status, list the issues, create an issue, set an issue's status, list the progress, read the usage file; any other request is answered not found. | — | — |
| DSH-13.c | proposed | The server checks every status change: a status only moves up the order `proposed`, `backlog`, `planned`, `done`, and the only move down is `planned` to `backlog`; any other change is refused with its reason. | — | — |
| DSH-13.d | proposed | A requirement's status change edits only the status cell of that row in its file, and the file is replaced as a whole or not at all. | — | — |
| DSH-13.e | proposed | An issue's status change removes the other status labels and adds the new one, creating the label when it is missing, and leaves the issue's open or closed state as it is. | — | — |
| DSH-13.f | proposed | The server runs the issue tracker's commands with each argument passed separately and never through a shell, and holds no token or secret. | — | — |
| DSH-13.g | proposed | When the issue tracker's command fails, the server answers with its reason and its other answers keep working. | — | — |
| DSH-13.h | proposed | When the web app cannot reach the server it says so (msg:dshServerUnreachable, with the reason as {reason}). | — | — |
| DSH-14 | proposed | At the top of the Agent progress column a usage chart (heading msg:dshUsageChart) shows the readings of the 5-hour session and of the 7-day week against the estimates, read from `SCRUM.d/usage.md`. | — | — |
| DSH-14.a | proposed | The usage file has a Usage table whose rows are: block ID, estimate session %, estimate weekly %, before session %, before weekly %, after session % and after weekly %; a cell that is not known is a dash. | — | — |
| DSH-14.b | proposed | The chart has two meters, one for the session (msg:dshMeterSession) and one for the week (msg:dshMeterWeek), each on a scale from 0 to 100. | — | — |
| DSH-14.c | proposed | For each row with a before and an after reading, a meter draws a bar from the before reading to the after reading in the data color of the theme, and names the block. | — | — |
| DSH-14.d | proposed | For each row with an estimate, a meter draws the estimate as a lighter band from the before reading, as wide as the estimate plus and minus the share in DEF-01. | — | — |
| DSH-14.e | proposed | For the next planned sprint the meter draws the projected after reading, the before reading plus the estimate, as a band that ends in a mark; a projection is never drawn as a dot. | — | — |
| DSH-14.f | proposed | A value above 100 is drawn as a triangle on the 100 line with the real number in its tooltip. | — | — |
| DSH-14.g | proposed | When the usage file is missing or has no Usage table the chart is empty and says so (msg:dshNoUsage). | — | — |
