# Requirements (draft rewrite as definitions and rules)

## Intro

One file per feature: the checkable rules of behavior the app must meet. This is the spec for both the Python app (the reference) and the Dart port. 🟠 Defined in the old process notes (Inputs; moved with the old app); the plan is the old layer map (moved with the old app). (A cold agent cannot open "the old process notes" or "the old layer map".)

The aim is that the requirement files speak for themselves, so the build rules can stay short.

The Rules apply to every row in `requirements/`. A rule is one row: `ID | What | When acted | How tested`; the format and the cells `^`, `—` and blank are read as in `SCRUM.d/README.md` (Intro).

🟡 The prefix **Rw** of every ID below is chosen by the Orchestrator (the Product Owner gave no code for "any agent or person" who writes or changes a requirement). Every test cell that the original did not state is written as a review step and the row carries 🟡.

## Definitions

### Roles

- 🟡 **Requirement writer (Rw)**: the agent or person who writes or changes a row in `requirements/` ("any agent or person"; the Orchestrator and a slice agent are two). Not a ROLE in `SCRUM.d/README.md`.

### Terms

- **Feature**: an area of the app (Calendar, Sources, Account). One file: `requirements/<feature>.md`.
- 🔴 **Requirement**: one checkable rule of a feature's behavior with an ID (ACC-06), a status and a definitive statement of what to build. A requirement has a matching test (duplicates Rw-11). Other files link to the requirement, not to a sub-requirement (duplicates Rw-04).
- 🔴 **Sub-requirement**: one checkable rule that further clarifies a requirement, with a sub-ID (ACC-06.a), a status and a definitive statement of what to build. A sub-requirement has a matching sub-test (duplicates Rw-11.a).
- **Issue**: a component not meeting a requirement. It lives in GitHub issues, not here.
- 🟠 **Process**: how work is done here (the old process notes, moved with the old app). (No file to open.)
- **Question (?)**: a request for a suggestion; the Product Owner decides. A question is a row marked `(?)`, and it appears in `SCRUM.d/defects.md`.
- **Shared requirements** (`common.md`): behavior several features use, written once and referenced: time (TIM), shared UI (UI), what an origin allows (CAP), defaults and limits (DEF).
- 🔴 **Parent tests**: a requirement that has sub-requirements passes when all its sub-requirements pass; its own test cell may be `—` or name a test of the whole. (Rw-11.a says the same: Law 1.)
- **Test cell**: a list of tests, or `see <ID>` links to the tests of another requirement or sub-requirement, or `—` while there is none. A sub-test is simply the test the sub-requirement uses; it may be its own, its parent's, or another requirement's. A test says which requirements it verifies and how it runs when several call it (once, or once per requirement); failures are reported per requirement (🟠 the old layer map, moved with the old app: testing decisions).
- 🔴 **Evidence (temporary)**: the S keys pointing at the Python suites; deleted when the conversion ends. (The Line format below defines it again: Law 1.)
- **Oracle**: the existing Python app and its suites, used once as the reference for what the app does.
- **`oldkey.md`**: the record of old IDs to new IDs.
- **Stories, epics, sprints and the backlog** are defined in `SCRUM.d/README.md` ("the process rules").
- 🔴 A story names the requirement and sub-requirement IDs it will meet and is done when their tests pass (the Story is defined in `SCRUM.d/README.md`; the Product Owner removed "done when their tests pass" from definitions, see `WORKING.d/lessons.md`).
- **Number**: a limit, a default, a duration or a count; a number written as a word counts as a number.
- **Shared component**: an actionable component several features use (picker, filter, button, dropdown, strength bar, date range). **Look**: a color, font, padding, margin, corner, size or duration. **Shared capability**: a capability several features use (Print).
- **Growing thing**: anything that grows with use (a log, a list, a table of records).
- **Agreed row**: a row the Product Owner agreed (status `backlog` or blank).
- **Message key**: the name `msg:key` that cites a message the user sees; the wording and its translations live only in `messages/` (`app_en.arb` is the template).
- **Prefix**: a feature's prefix is three letters. A module in a subfolder adds that folder's letter before its three letters: C for `connections.d` (CGOW is Google one-way) and P for `plugins.d` (PGAP is the Google API plugin); a folder inside a folder adds its letter in turn.
- **Modules** come in two kinds, connections and plugins. `connections.md` and `plugins.md` hold what is common to every module of the kind (written once); each module is its own feature file in `connections.d/` or `plugins.d/`.
- **One file per feature (Nov 17)**: each feature has ONE file here, `requirements/<feature>.md`, with every requirement of that feature in the same table; the status vocabulary is under Line format. Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them (🔴 duplicates Rw-02 and Rw-03).
- **Reviewing a feature** means changing `proposed` rows to `backlog` (or editing or deleting them) in that one file. (The Product Owner does this; the Orchestrator never deletes `proposed`, Or-02.c.)
- **The freeze files**: these files hold what was already asked for.

### Line format

- **Line**: `| ID | status | statement | test | evidence (temporary) |`
- **ID**: a feature prefix and a number (CAL-03). A requirement may have sub-requirements (ACC-06, ACC-06.a, ACC-06.b). 🔴 (A link points at the requirement unless it means exactly one sub-requirement; when IDs change, `oldkey.md` records old to new: both duplicate Rw-04.)
- **status**: one of the five below.
  - `proposed`: drafted, not yet agreed.
  - `backlog`: the Product Owner agreed; it is a Requirement, waiting for a story.
  - `planned`: it is in a story.
  - `done`: its story was accepted at the Review.
  - `defect`: an agent cannot act on it; the Orchestrator changes it and sets it to `proposed`.
- The Product Owner agrees to a row by deleting `proposed` (authority; its effect on agents is Or-02.c). A blank status is read as `backlog`.
- `SCRUM.d/sprint.md` records which story holds a planned requirement.
- **Order of status**: a status moves up the order of the list above (`proposed`, `backlog`, `planned`, `done`). The moves down are `planned` to `backlog`, when a requirement leaves its story, and `planned` to `defect`, when an agent cannot act on it; a `defect` row returns to `proposed` after the Orchestrator changes it. 🔴 (`defect` is last in the list but `AGENTS.md` names only `planned` to `backlog` as a move down; the sentence also repeats Or-02.e.b.)
- **test**: the test that verifies it (path and name), once one exists. `—` until the inventory of the Python suites (`requirements/inventory/`) has been matched to requirements.
- 🔴 **evidence (temporary)**: the Python-suite keys (and old Dashboard items) a row came from; deleted when the conversion ends.

### Prefixes

CAL calendar · SRC sources section · FDS feeds section · CLCL local calendar · CFED generic feed · CCCS ccs+ · CLNK calendar link · RUL rules · TPL event_templates · EVT events · HIS history · CON connections (common) · CGOW google one-way · CGTW google two-way · PLG plugins (common) · PGAP google plugin ·
SET settings · ACC account · DIA diagnostics · DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · TIM time, UIC shared interface, CAP capabilities (all three in common.md) · PRT print · THM theme

(🔴 The text says UIC and the rules say UI: two names for the shared interface.)

### Index (feature files, click to open)

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

### Requirement writer (rules for writing and changing requirements, any agent or person)

| ID | What | When acted | How tested |
|---|---|---|---|
| Rw-01 | **Numbers live in DEF-01.** A number appears only in the table in `common.md`; a row says "the time in DEF-01" | A row is written or changed | `req_check.sh` lists numbers with units, and number words of two or more, outside DEF-01 |
| 🟡 Rw-01.a | A default that is not a number (a view, a theme) is stated in the row of the control it belongs to | A row is written or changed | review: the default is in the row of its control |
| Rw-02 | **Three homes for shared things.** Puts each shared thing in its home, by Rw-02.a to Rw-02.c | A row is written or changed | review: the row does not restate how a shared component works; it links to the UI row, the theme row or the feature that owns it |
| Rw-02.a | A shared component is a UI row in `common.md` | A shared component is written | ^ |
| Rw-02.b | A look is a theme row (`theme.md`) and is used by default | A look is written | ^ |
| Rw-02.c | A shared capability is its own feature | A shared capability is written | ^ |
| 🔴 Rw-03 | **Features add only their specifics.** A feature row never restates how a shared component works (the Test is also the Test of Rw-02: Law 1) | A feature row is written or changed | review: follow the row's links and nothing is said twice |
| 🟡 Rw-03.a | A module's feature file (in `connections.d/` or `plugins.d/`) adds only its specifics, linking to the common file (`connections.md`, `plugins.md`) | A module file is written or changed | review: follow the module's links to the common file and nothing is said twice |
| 🔴 Rw-04 | **Links point at the requirement,** not a sub-requirement, unless exactly one detail is meant (an exception: Law 2) | A link is written | review: each link to a sub-requirement means exactly one detail |
| Rw-04.a | A link names an ID that exists today | A link is written | `req_check.sh` reports a link to an ID that does not exist |
| Rw-04.b | When an ID changes, changes every reference and gives `oldkey.md` a row | An ID changes | review: `oldkey.md` has a row for every ID change |
| Rw-05 | **A row says what to build, once, in the user's words**, by Rw-05.a to Rw-05.f. (The first words "A row says what to build, once, in the user's words" and "One checkable rule per row" say nearly the same.) | A row is written or changed | review: the row holds one checkable rule |
| Rw-05.a | One checkable rule per row | ^ | review: the row holds one checkable rule |
| Rw-05.b | No history ("the Python app does…") | ^ | `req_check.sh` lists history |
| Rw-05.c | No test or script wording | ^ | `req_check.sh` lists script wording |
| 🟠 Rw-05.d | No web-page mechanics (no closed list of what that is) | ^ | review: the row has no web-page mechanics |
| 🟠 Rw-05.e | No "is refused" for a control that cannot produce a wrong value (the agent must judge what a control can produce) | ^ | review: no row says "is refused" for such a control |
| 🟡 Rw-05.f | A requirement's own statement is general; its sub-requirements hold the detail and the values | ^ | review: the values are in the sub-requirements |
| 🟠 Rw-06 | **Define every term** the first time a file uses it, or point to where it is defined | A term is used the first time in a file | review: a reader who knows only this folder can follow every term |
| 🟠 Rw-07 | **State limits.** Anything that grows with use (a growing thing) has a limit in DEF-01 (DEF-02) (the pair "DEF-01 (DEF-02)" is unclear) | A growing thing is written | review: for each list that grows, find its limit in DEF-01 |
| Rw-08 | **Questions** are rows marked `(?)` (Questions, Definitions). Looks for the answer first in the other requirements, the decisions, the code of the running app, and the Flutter and Dart documentation (https://docs.flutter.dev/ and https://dart.dev/), and only then asks the Product Owner (🟠 "the decisions" names no file) | An answer is needed | review: the question to the Product Owner records where the answer was looked for |
| 🟡 Rw-08.a | Every `(?)` row has its question in `SCRUM.d/defects.md`, and every question there has its `(?)` row | A `(?)` row or a question is written | `req_check.sh` reports a `(?)` row with no question, and a question with no `(?)` row |
| Rw-09 | **Nothing you write names an agent or a tool.** | ^ | `req_check.sh` lists any agent or tool name |
| Rw-09.a | Names a person by role, as `SCRUM.d/README.md` defines the roles | A person is named | ^ |
| Rw-10 | **Prefixes.** Gives each row the prefix its folder defines (Prefix, Definitions) | A row is written | `req_check.sh` reports a row whose prefix does not match its folder |
| Rw-11 | **Every requirement has a test.** Gives a row with no sub-requirements a test, by Rw-11.a to Rw-11.c | A row is written or changed | `req_check.sh` counts rows whose test cell is `—` |
| 🟡 Rw-11.a | The test cell names the test or says `see <ID>` | A row with no sub-requirements is written | review: the test cell names a test or says `see <ID>` |
| 🟡 Rw-11.b | `—` stays only until a test exists | A row with no sub-requirements has `—` | `req_check.sh` counts rows whose test cell is `—` |
| Rw-11.c | A row with status `planned` or `done` has a test | A row is `planned` or `done` | `req_check.sh` reports a `planned` or `done` row with no sub-requirements and `—` as an error |
| 🔴 Rw-11.d | **A row with sub-requirements passes when all its sub-requirements pass;** its own test cell may be `—` or name a test of the whole (duplicates the definition Parent tests: Law 1; originally numbered 11.a) | A row has sub-requirements | `req_check.sh` skips the test-cell error of Rw-11 for a row that has sub-requirements; review: each sub-requirement of such a row has a test |
| Rw-12 | **Messages are keys.** A requirement never contains the wording of a message the user sees; it cites the message as `msg:key` and says when it is shown and what its placeholders hold | A message is cited | `req_check.sh` reports a cited key missing from the template |
| Rw-12.a | The wording and its translations live only in `messages/` (`app_en.arb` is the template) | A message is written | `req_check.sh` reports a locale file that lacks a key the template has |
| Rw-12.b | Counts the keys no requirement cites yet | ^ | `req_check.sh` counts the keys no requirement cites yet |
| 🟡 Rw-13 | **An agreed row has agreed sub-requirements.** Adds a sub-requirement to an agreed row as `proposed`; it does not count as agreed until the Product Owner reviews it (the Product Owner reviews each such sub-requirement: authority) | A sub-requirement is added to an agreed row | `req_check.sh` lists every agreed row that has a `proposed` sub-requirement |
| 🟡 Rw-14 | Never refers to a story in a requirement ("requirements never refer to a story") | A row is written | review: no requirement names a story |
| 🔴 Rw-15 | Adds nothing new while the transition freeze lasts (the old process overview, moved with the old app) (the freeze is owned by `AGENTS.md`: Law 1) | The transition freeze lasts | review: every new row traces to the old app or a Product Owner answer (`AGENTS.md`) |
| 🟡 Rw-16 | **Checks a feature file** after organizing it into requirements and sub-requirements: a feature file is not done when its rows are written; goes back over it by Rw-16.a and Rw-16.b | A feature is organized into requirements and sub-requirements | review: the check names Rw-16.a and Rw-16.b done |
| 🟡 Rw-16.a | **The laws and rules**: every row obeys rules 1 to 3 (numbers, shared homes, specifics only: Rw-01 to Rw-03) and the laws in `AGENTS.md`. Searches the other files for the same rule in other words before accepting a row as new | Rw-16 | review: each row checked against Rw-01 to Rw-03 and the laws; the search is named |
| 🟡 Rw-16.b | **Simulates three jobs**, and fixes what stops you (Rw-16.b.a to Rw-16.b.c) | Rw-16 | review: the three simulations are recorded |
| 🟠 Rw-16.b.a | **Coder**: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed ("nothing has to be guessed" is a judgment) | Rw-16.b | review: each of the listed points was checked |
| 🟡 Rw-16.b.b | **Tester**: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test | Rw-16.b | review: each of the listed points was checked |
| 🟡 Rw-16.b.c | **Reviewer**: the statement says what to build, with no history or Python-app notes; the code can be compared with it row by row | Rw-16.b | review: each of the listed points was checked |

## Not yet placed (existing statements I could not give a row)

- The scans of the README and CHANGELOG and the gap triage were folded into these files as `proposed` rows on Nov 18 and the `requirements/drafts/` folder was deleted; the history is in git (commit before the deletion). Reason: history, no actor, not a definition (and Rw-05.b forbids history in a row).
- "A blank status is read as `backlog` and the Orchestrator writes the word": the Orchestrator's half is Or-02.f (Law 1); the definition half is in the Line format above.
- "Nothing new is added while the transition freeze lasts ... these files hold what was already asked for": the first half is Rw-15 (duplicate of the freeze in `AGENTS.md`); the second half is under Terms.
- "The aim is that the requirement files speak for themselves, so the build rules can stay short": placed in the Intro as the file's aim; no rule can test it.
- The sentence "Reviewing a feature means changing `proposed` rows to `backlog` (or editing or deleting them)" gives the Product Owner's act; the Orchestrator's limit is Or-02.c. Is "deleting" a row there the Product Owner's only?
