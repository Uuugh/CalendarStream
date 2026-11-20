# Requirements

One file per feature: the checkable rules of behavior the app must meet. This is the spec for both the Python app
(the reference) and the Dart port. Defined in the old process notes (Inputs; moved with the old app); the plan is the old layer map (moved with the old app).

## Rules for writing and changing requirements (any agent or person)

These apply to every row in `requirements/`.

1. **Law: no duplication. Say it once.** A rule is written in one place and referenced everywhere else. Before adding a row, search the folder for the same rule in other words. **Test:** `req_check.sh` lists identical statements; review: name the one row that owns the rule, and every other row only links to it.
2. **Law: no exceptions.** If a rule has an exception, the requirement is wrong: change it so it holds for every case, or give the different case its own requirement. A row never says "except", "never for" or "only when X is not". A new kind of thing (a connection, a component) follows the existing rules and does not get a special case. **Test:** `req_check.sh` lists exception wording (a condition that says when something happens is fine; an exception to another rule is not); review: would the rule hold unchanged for the next new connection or component?
3. **Numbers live in DEF-01.** A limit, a default, a duration or a count appears only in the table in `common.md`; a row says "the time in DEF-01". A default that is not a number (a view, a theme) is stated in the row of the control it belongs to. **Test:** `req_check.sh` lists numbers with units outside DEF-01.
4. **Three homes for shared things.** An actionable component several features use (picker, filter, button, dropdown, strength bar, date range) is a UI row in `common.md`. A look (color, font, padding, margin, corner, size, duration) is a theme row (`theme.md`) and is used by default. A capability several features use (Print) is its own feature. **Test:** review: the row does not restate how a shared component works; it links to the UI row, the theme row or the feature that owns it.
5. **Features add only their specifics.** A feature row never restates how a shared component works. **Test:** review: follow the row's links and nothing is said twice.
6. **Links point at the requirement,** not a sub-requirement, unless exactly one detail is meant. A link names an ID that exists today; when an ID changes, every reference is changed and `oldkey.md` gets a row. **Test:** `req_check.sh` reports a link to an ID that does not exist; review: `oldkey.md` has a row for every ID change.
7. **A row says what to build, once, in the user's words.** One checkable rule per row. No history ("the Python app does…"), no test or script wording, no web-page mechanics, no "is refused" for a control that cannot produce a wrong value. A requirement's own statement is general; its sub-requirements hold the detail and the values. **Test:** `req_check.sh` lists history and script wording; review: the row holds one checkable rule.
8. **Define every term** the first time a file uses it, or point to where it is defined. **Test:** review: a reader who knows only this folder can follow every term.
9. **State limits.** Anything that grows with use (a log, a list, a table of records) has a limit in DEF-01 (DEF-02). **Test:** review: for each list that grows, find its limit in DEF-01.
10. **Questions** are rows marked `(?)` and appear in `requirements/open-questions.md`. Look for the answer first in the other requirements, the decisions, the code of the running app, and the Flutter and Dart documentation (https://docs.flutter.dev/ and https://dart.dev/), and only then ask the Product Owner. **Test:** `req_check.sh` reports a `(?)` row with no question, and a question with no `(?)` row.
11. **Nothing you write names an agent or a tool.** Name a person by role, as `SCRUM.d/README.md` defines the roles. **Test:** `req_check.sh` lists any agent or tool name.
12. **Prefixes.** A feature's prefix is three letters. A module in a subfolder adds that folder's letter before its three letters: C for `connections.d` (CGOW is Google one-way) and P for `plugins.d` (PGAP is the Google API plugin); a folder inside a folder adds its letter in turn. **Test:** `req_check.sh` reports a row whose prefix does not match its folder.
13. **Every requirement has a test.** A row's test cell names the test or says `see <ID>`; `—` stays only until a test exists. **Test:** `req_check.sh` counts rows whose test cell is `—`.
14. **Messages are keys.** A requirement never contains the wording of a message the user sees; it cites the message as `msg:key` and says when it is shown and what its placeholders hold. The wording and its translations live only in `messages/` (`app_en.arb` is the template). **Test:** `req_check.sh` reports a cited key missing from the template, a locale file that lacks a key the template has, and counts the keys no requirement cites yet.

## Definitions

- **Feature**: an area of the app (Calendar, Sources, Account). One file: `requirements/<feature>.md`.
- **Requirement**: one checkable rule of a feature's behavior with an ID (ACC-06), a status and a definitive statement of what to build. A requirement has a matching test. Other files link to the requirement, not to a sub-requirement.
- **Sub-requirement**: one checkable rule that further clarifies a requirement, with a sub-ID (ACC-06.a), a status and a definitive statement of what to build. A sub-requirement has a matching sub-test.
- **Issue**: a component not meeting a requirement. It lives in GitHub issues, not here.
- **Process**: how work is done here (the old process notes, moved with the old app).
- **Question (?)**: a request for a suggestion; the Product Owner decides.
- **Shared requirements** (`common.md`): behavior several features use, written once and referenced: time (TIM), shared UI (UI), what an origin allows (CAP), defaults and limits (DEF).
- **Parent tests**: a requirement that has sub-requirements passes when all its sub-requirements pass; its own test cell may be `—` or name a test of the whole.
- **Test cell**: a list of tests, or `see <ID>` links to the tests of another requirement or sub-requirement, or `—` while there is none. A sub-test is simply the test the sub-requirement uses; it may be its own, its parent's, or another requirement's. A test says which requirements it verifies and how it runs when several call it (once, or once per requirement); failures are reported per requirement (the old layer map, moved with the old app: testing decisions).
- **Evidence (temporary)**: the S keys pointing at the Python suites; deleted when the conversion ends.
- **Oracle**: the existing Python app and its suites, used once as the reference for what the app does.
- **`oldkey.md`**: the record of old IDs to new IDs.
- **Stories, epics, sprints and the backlog** are defined in the process rules. A story names the requirement and sub-requirement IDs it will meet and is done when their tests pass; requirements never refer to a story.

## Line format

`| ID | status | statement | test | evidence (temporary) |`

- **ID**: a feature prefix and a number (CAL-03). A requirement may have sub-requirements (ACC-06, ACC-06.a, ACC-06.b); a link points at the requirement unless it means exactly one sub-requirement. When IDs change, `oldkey.md` records old to new.
- **status**: `proposed` (drafted, not yet agreed) or `backlog` (the Product Owner agreed: it is a Requirement, waiting for a sprint). The Product Owner agrees to a row by deleting `proposed`; a blank status is read as `backlog` and the Author writes the word. With Scrum the Dashboard records what follows: the sprint a requirement is built in, and done when its test passes.
- **test**: the test that verifies it (path and name), once one exists. `—` until the inventory of the Python suites
  (`requirements/inventory/`) has been matched to requirements.
- **evidence (temporary)**: the Python-suite keys (and old Dashboard items) a row came from; deleted when the conversion ends.

## Prefixes

CAL calendar · SRC sources section · FDS feeds section · CLCL local calendar · CFED generic feed · CCCS ccs+ · CLNK calendar link · RUL rules · TPL event_templates · EVT events · HIS history · CON connections (common) · CGOW google one-way · CGTW google two-way · PLG plugins (common) · PGAP google plugin ·
SET settings · ACC account · DIA diagnostics · DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · TIM time, UIC shared interface, CAP capabilities (all three in common.md) · PRT print · THM theme

Nothing new is added while the transition freeze lasts (the old process overview, moved with the old app); these files hold what was already
asked for.

## One file per feature (Nov 17)

Each feature has ONE file here, `requirements/<feature>.md`, with every requirement of that feature in the same table; the status vocabulary is under Line format. Reviewing a feature means changing `proposed` rows to `backlog` (or editing or deleting them) in that one file. Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them.

Modules come in two kinds, connections and plugins. `connections.md` and `plugins.md` hold what is common to every module of the kind (written once); each module is its own feature file in `connections.d/` or `plugins.d/` and adds only its specifics, linking to the common file.

The scans of the README and CHANGELOG and the gap triage were folded into these files as `proposed` rows on Nov 18 and the `requirements/drafts/` folder was deleted; the history is in git (commit before the deletion).

## Index (feature files, click to open)

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

## Checking a feature file

A feature file is not done when its rows are written. After organizing a feature into requirements and sub-requirements, go back over it:

1. **The laws and rules**: every row obeys rules 1 to 5 (the laws, numbers, shared homes, specifics only). Search the other files for the same rule in other words before accepting a row as new.
2. **Simulate three jobs**, and fix what stops you:
   - **Coder**: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed.
   - **Tester**: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test.
   - **Reviewer**: the statement says what to build, with no history or Python-app notes; the code can be compared with it row by row.

The aim is that the requirement files speak for themselves, so the build rules can stay short.

