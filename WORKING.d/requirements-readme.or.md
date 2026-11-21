# Requirements

## Intro

One file per feature: the checkable rules of behavior the app must meet. The aim is that the requirement files speak for themselves, so the build rules can stay short.

A rule is one row: `ID | What | When acted | How tested`; `^` is the parent's value. The ID prefix `Rq` is my choice for "the rules for writing and changing requirements (any agent or person)"; it is marked 🟡 below.

## Definitions

- **Feature**: an area of the app (Calendar, Sources, Account). One file: `requirements/<feature>.md`, with every requirement of that feature in the same table. Reviewing a feature means changing `proposed` rows to `backlog` (or editing or deleting them) in that one file.
- **Requirement**: one checkable rule of a feature's behavior with an ID (ACC-06), a status and a definitive statement of what to build. A requirement has a matching test. Other files link to the requirement, not to a sub-requirement.
- **Sub-requirement**: one checkable rule that further clarifies a requirement, with a sub-ID (ACC-06.a), a status and a definitive statement of what to build. A sub-requirement has a matching sub-test.
- **Issue**: a component not meeting a requirement. It lives in GitHub issues, not here.
- **Question (?)**: a request for a suggestion; the Product Owner decides.
- **Shared requirements** (`common.md`): behavior several features use, written once and referenced: time (TIM), shared UI (UI), what an origin allows (CAP), defaults and limits (DEF). Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them.
- **Module**: a feature that comes in one of two kinds, connections and plugins. `connections.md` and `plugins.md` hold what is common to every module of the kind (written once).
- **Parent tests**: a requirement that has sub-requirements passes when all its sub-requirements pass; its own test cell may be `—` or name a test of the whole.
- **Test cell**: a list of tests, or `see <ID>` links to the tests of another requirement or sub-requirement, or `—` while there is none. A sub-test is simply the test the sub-requirement uses; it may be its own, its parent's, or another requirement's. A test says which requirements it verifies and how it runs when several call it (once, or once per requirement); failures are reported per requirement.
- **Evidence (temporary)**: the S keys pointing at the Python suites; deleted when the conversion ends.
- **Oracle**: the existing Python app and its suites, used once as the reference for what the app does.
- **`oldkey.md`**: the record of old IDs to new IDs.
- **Stories, epics, sprints and the backlog** are defined in the process rules (`SCRUM.d/README.md`). A story names the requirement and sub-requirement IDs it will meet and is done when their tests pass; requirements never refer to a story.
- **Line format**: `| ID | status | statement | test | evidence (temporary) |`.
  - **ID**: a feature prefix and a number (CAL-03). A requirement may have sub-requirements (ACC-06, ACC-06.a, ACC-06.b); a link points at the requirement unless it means exactly one sub-requirement. When IDs change, `oldkey.md` records old to new.
  - **status**: `proposed` (drafted, not yet agreed), `backlog` (the Product Owner agreed: it is a Requirement, waiting for a story), `planned` (it is in a story), `done` (its story was accepted at the Review) or `defect` (an agent cannot act on it). A blank status is read as `backlog`. `SCRUM.d/sprint.md` records which story holds a planned requirement.
  - **test**: the test that verifies it (path and name), once one exists. `—` until the inventory of the Python suites (`requirements/inventory/`) has been matched to requirements.
  - **evidence (temporary)**: the Python-suite keys (and old Dashboard items) a row came from; deleted when the conversion ends.
- **Prefixes**: CAL calendar · SRC sources section · FDS feeds section · CLCL local calendar · CFED generic feed · CCCS ccs+ · CLNK calendar link · RUL rules · TPL event_templates · EVT events · HIS history · CON connections (common) · CGOW google one-way · CGTW google two-way · PLG plugins (common) · PGAP google plugin · SET settings · ACC account · DIA diagnostics · DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · TIM time, UIC shared interface, CAP capabilities (all three in common.md) · PRT print · THM theme.
- **Feature files** (click to open):

| Feature | File |
|---|---|
| Calendar | [requirements/calendar.md](calendar.md) |
| Calendar filter | [requirements/calendar_filter.md](calendar_filter.md) |
| Print | [requirements/print.md](print.md) |
| Theme | [requirements/theme.md](theme.md) |
| Search | [requirements/search.md](search.md) |
| Events | [requirements/events.md](events.md) |
| Event templates | [requirements/event_templates.md](event_templates.md) |
| Rules | [requirements/rules.md](rules.md) |
| History | [requirements/history.md](history.md) |
| Sources (section) | [requirements/sources.md](sources.md) |
| Feeds (section) | [requirements/feeds.md](feeds.md) |
| Connections (common) | [requirements/connections.md](connections.md) |
| Local calendar | [requirements/connections.d/local_calendar.md](connections.d/local_calendar.md) |
| Generic Feed | [requirements/connections.d/generic_feed.md](connections.d/generic_feed.md) |
| CCS+ | [requirements/connections.d/ccs.md](connections.d/ccs.md) |
| Calendar link | [requirements/connections.d/calendar_link.md](connections.d/calendar_link.md) |
| Google one-way sync | [requirements/connections.d/google_one_way.md](connections.d/google_one_way.md) |
| Google two-way sync | [requirements/connections.d/google_two_way.md](connections.d/google_two_way.md) |
| Plugins (common) | [requirements/plugins.md](plugins.md) |
| Google plugin (API client) | [requirements/plugins.d/google_api.md](plugins.d/google_api.md) |
| Settings | [requirements/settings.md](settings.md) |
| Account | [requirements/account.md](account.md) |
| Shell | [requirements/shell.md](shell.md) |
| Diagnostics | [requirements/diagnostics.md](diagnostics.md) |
| Deployment | [requirements/deployment.md](deployment.md) |
| Documentation | [requirements/documentation.md](documentation.md) |
| Common (time, shared UI, capabilities) | [requirements/common.md](common.md) |

## Rules

These apply to every row in `requirements/`.

| ID | What | When acted | How tested |
|---|---|---|---|
| 🟡 Rq-01 | Numbers live in DEF-01: a limit, a default, a duration or a count appears only in the table in `common.md`, and a number written as a word counts as a number; a row says "the time in DEF-01" | Writing a row | `req_check.sh` lists numbers with units, and number words of two or more, outside DEF-01 |
| Rq-01.a | A default that is not a number (a view, a theme) is stated in the row of the control it belongs to | Writing a row | review: each non-number default is in the row of its control |
| Rq-02 | A shared thing has one of three homes. An actionable component several features use (picker, filter, button, dropdown, strength bar, date range) is a UI row in `common.md` | Writing a row | review: the row does not restate how a shared component works; it links to the UI row, the theme row or the feature that owns it |
| Rq-02.a | A look (color, font, padding, margin, corner, size, duration) is a theme row (`theme.md`) and is used by default | Writing a row | ^ |
| Rq-02.b | A capability several features use (Print) is its own feature | Writing a row | ^ |
| Rq-03 | A feature row adds only its specifics; it never restates how a shared component works | Writing a row | review: follow the row's links and nothing is said twice |
| Rq-04 | A link points at the requirement, not a sub-requirement, unless exactly one detail is meant | Writing a link | review: each link to a sub-requirement means exactly one detail |
| Rq-04.a | A link names an ID that exists today; when an ID changes, every reference is changed and `oldkey.md` gets a row | An ID changes | `req_check.sh` reports a link to an ID that does not exist; review: `oldkey.md` has a row for every ID change |
| Rq-05 | A row says what to build, once, in the user's words: one checkable rule per row | Writing a row | review: the row holds one checkable rule |
| Rq-05.a | A row has no history ("the Python app does…"), no test or script wording, no web-page mechanics, no "is refused" for a control that cannot produce a wrong value | Writing a row | `req_check.sh` lists history and script wording |
| Rq-05.b | A requirement's own statement is general; its sub-requirements hold the detail and the values | Writing a row | review: each value is in a sub-requirement |
| Rq-06 | Defines every term the first time a file uses it, or points to where it is defined | Writing any line | review: a reader who knows only this folder can follow every term |
| Rq-07 | Anything that grows with use (a log, a list, a table of records) has a limit in DEF-01 (DEF-02) | Writing a row | review: for each list that grows, find its limit in DEF-01 |
| Rq-08 | Questions are rows marked `(?)` and appear in `SCRUM.d/defects.md` | A question | `req_check.sh` reports a `(?)` row with no question, and a question with no `(?)` row |
| Rq-08.a | Look for the answer first in the other requirements, the decisions, the code of the running app, and the Flutter and Dart documentation (https://docs.flutter.dev/ and https://dart.dev/), and only then ask the Product Owner | Before asking | review: each question shows where the answer was looked for |
| Rq-09 | Nothing you write names an agent or a tool; name a person by role, as `SCRUM.d/README.md` defines the roles | Writing any line | `req_check.sh` lists any agent or tool name |
| Rq-10 | A feature's prefix is three letters | Naming a feature | `req_check.sh` reports a row whose prefix does not match its folder |
| Rq-10.a | A module in a subfolder adds that folder's letter before its three letters: C for `connections.d` (CGOW is Google one-way) and P for `plugins.d` (PGAP is the Google API plugin); a folder inside a folder adds its letter in turn | Naming a module | ^ |
| Rq-11 | A row with no sub-requirements: its test cell names the test or says `see <ID>`; `—` stays only until a test exists, and a row with status `planned` or `done` has a test | Writing a row | `req_check.sh` counts rows whose test cell is `—` and reports a `planned` or `done` row with no sub-requirements and `—` as an error |
| Rq-12 | A requirement never contains the wording of a message the user sees; it cites the message as `msg:key` and says when it is shown and what its placeholders hold | Writing a row | `req_check.sh` reports a cited key missing from the template, a locale file that lacks a key the template has, and counts the keys no requirement cites yet |
| Rq-12.a | The wording and its translations live only in `messages/` (`app_en.arb` is the template) | Writing a message | ^ |
| Rq-13 | A row the Product Owner agreed (status `backlog` or blank) can gain a `proposed` sub-requirement; the Product Owner reviews each such sub-requirement before it counts as agreed | A sub-requirement is added to an agreed row | `req_check.sh` lists every agreed row that has a `proposed` sub-requirement |
| Rq-14 | A feature file is not done when its rows are written; after organizing a feature into requirements and sub-requirements, go back over it | After organizing a feature | review: Rq-14.a and Rq-14.b were done |
| Rq-14.a | Every row obeys rules Rq-01 to Rq-03 (numbers, shared homes, specifics only) and the laws in `AGENTS.md`; search the other files for the same rule in other words before accepting a row as new | After organizing a feature | review: the search for the same rule is named |
| Rq-14.b | Simulate three jobs, and fix what stops you (Rq-14.b.a to Rq-14.b.c) | After organizing a feature | review: each job's check was done |
| Rq-14.b.a | Coder: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed | After organizing a feature | review: a reader acting as the Coder needs to guess nothing |
| Rq-14.b.b | Tester: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test | After organizing a feature | review: a reader acting as the Tester can name the pass or fail of each row |
| 🟠 Rq-14.b.c | Reviewer: the statement says what to build, with no history or Python-app notes; the code can be compared with it row by row | After organizing a feature | review: a reader acting as the Reviewer finds no history or Python-app note |
| 🔴 Rq-15 | Status moves up the order proposed, backlog, planned, done; the moves down are `planned` to `backlog`, when a requirement leaves its story, and `planned` to `defect`, when an agent cannot act on it; a `defect` row returns to `proposed` after the Orchestrator changes it | A status changes | `git diff` shows no move the rule does not allow (the same rule is in `AGENTS.md`, Standing rules) |
| Rq-16 | A module is its own feature file in `connections.d/` or `plugins.d/` and adds only its specifics, linking to the common file | Writing a module | review: the module row links to the common file and does not restate it |

## Not yet placed

- 🔴 "Nothing new is added while the transition freeze lasts; these files hold what was already asked for." (the same freeze is in `AGENTS.md`.)
- 🔴 "This is the spec for both the Python app (the reference) and the Dart port." (`AGENTS.md` says requirements win over the Python app.)
- 🟠 "Defined in the old process notes (Inputs; moved with the old app); the plan is the old layer map (moved with the old app)." and "**Process**: how work is done here (the old process notes, moved with the old app)." (the notes are no longer in the repository.)
- 🔴 "The scans of the README and CHANGELOG and the gap triage were folded into these files as `proposed` rows on Nov 18 and the `requirements/drafts/` folder was deleted; the history is in git." (history; breaks Rq-05.a.)
- 🔴 The status rules "The Product Owner agrees to a row by deleting `proposed`; a blank status is read as `backlog` and the Orchestrator writes the word." (these are `SCRUM.d/README.md` Or-02.c and Or-02.f.)
- 🔴 The statement "Parent tests" and the old rule 11.a ("A row with sub-requirements passes when all its sub-requirements pass; its own test cell may be `—` or name a test of the whole") say the same thing; it stands once, as the definition above.
- 🟠 "Reviewer: the code can be compared with it row by row" (Rq-14.b.c): the Reviewer is outside code development.
