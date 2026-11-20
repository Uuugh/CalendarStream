# Requirements

The spec of the app: one file per feature, each holding the checkable rules of behavior the app must meet.

## Definitions

- **Feature**: an area of the app (Calendar, Sources, Account), written as one file, `requirements/<feature>.md`, with every
  requirement of the feature in one table. Connections and plugins are two kinds of module: `connections.md` and
  `plugins.md` hold what is common to every module of the kind, written once; each module is a feature file in
  `connections.d/` or `plugins.d/` that adds only its specifics and links to the common file.
- **Shared requirements** (`common.md`): behavior several features use, written once and referenced: time (TIM), shared UI
  (UIC), what an origin allows (CAP), defaults and limits (DEF).
- **Requirement**: one checkable rule of a feature's behavior, with an ID (ACC-06), a status and a statement of what to
  build. It has a test.
- **Sub-requirement**: one checkable rule that clarifies a requirement, with a sub-ID (ACC-06.a), a status, a statement and a
  test.
- **Test cell**: the tests that verify a row (path and name), `see <ID>` to use the tests of another requirement or
  sub-requirement, or `—` while there is none. Any test may serve any row. A requirement with sub-requirements passes when
  all its sub-requirements pass, and its own test cell may be `—` or name a test of the whole.
- **Question (?)**: a request for a suggestion; the Product Owner decides.
- **`oldkey.md`**: the record of old IDs to new IDs.

## Line format

`| ID | status | statement | test | evidence (temporary) |`

- **ID**: a feature prefix and a number (CAL-03); a sub-requirement adds a letter (ACC-06.a). A feature's prefix is three
  letters; a module in a subfolder adds that folder's letter before its three letters: C for `connections.d` (CGOW is Google
  one-way) and P for `plugins.d` (PGAP is the Google API plugin); a folder inside a folder adds its letter in turn.
  The prefixes: CAL calendar · SRC sources section · FDS feeds section · CLCL local calendar · CFED generic feed · CCCS ccs+ ·
  CLNK calendar link · RUL rules · TPL event_templates · EVT events · HIS history · CON connections (common) · CGOW google
  one-way · CGTW google two-way · PLG plugins (common) · PGAP google plugin · SET settings · ACC account · DIA diagnostics ·
  DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · PRT print · THM theme · TIM time, UIC
  shared interface and CAP capabilities (all three in `common.md`).
- **status**: `proposed` (drafted, waiting for the Product Owner's review), `backlog` (approved by the Product Owner,
  waiting for a story), `planned` (in a story) or `done` (its story was accepted at the Review). The Product Owner approves a
  row by deleting `proposed`; a blank status is read as `backlog` and the Author writes the word. `SCRUM.d/sprint.md`
  records which story holds a planned requirement. A status moves up this order; the one move down is `planned` to
  `backlog`, when a requirement leaves its story.
- **statement**: what to build, as the rules below require.
- **test**: the test cell.
- **evidence (temporary)**: the old-suite keys a row came from; deleted when the port is complete.

## Rules for writing and changing requirements (any agent or person)

These apply to every row in `requirements/`.

1. **No duplication (law 1 of `AGENTS.md`).** Before adding a row, search the folder for the same rule in other words. **Test:** `req_check.sh` lists identical statements; review: name the one row that owns the rule, and every other row only links to it.
2. **No exceptions (law 2 of `AGENTS.md`).** A row never says "except", "never for" or "only when X is not"; a new kind of thing (a connection, a component) follows the existing rules. **Test:** `req_check.sh` lists exception wording (a condition that says when something happens is fine); review: would the rule hold unchanged for the next new connection or component?
3. **Numbers live in DEF-01.** A limit, a default, a duration or a count appears only in the table in `common.md`, and a number written as a word counts as a number; a row says "the time in DEF-01". A default that is not a number (a view, a theme) is stated in the row of the control it belongs to. **Test:** `req_check.sh` lists numbers with units, and number words of two or more, outside DEF-01.
4. **Three homes for shared things.** An actionable component several features use (picker, filter, button, dropdown, strength bar, date range) is a UI row in `common.md`. A look (color, font, padding, margin, corner, size, duration) is a theme row (`theme.md`) and is used by default. A capability several features use (Print) is its own feature. **Test:** review: the row does not restate how a shared component works; it links to the UI row, the theme row or the feature that owns it.
5. **Features add only their specifics.** A feature row never restates how a shared component works. **Test:** review: follow the row's links and nothing is said twice.
6. **Links point at the requirement,** not a sub-requirement, unless exactly one detail is meant. A link names an ID that exists today; when an ID changes, every reference is changed and `oldkey.md` gets a row. **Test:** `req_check.sh` reports a link to an ID that does not exist; review: `oldkey.md` has a row for every ID change.
7. **A row says what to build, once, in the user's words.** One checkable rule per row. No history, no test or script wording, no web-page mechanics, no "is refused" for a control that cannot produce a wrong value. A requirement's own statement is general; its sub-requirements hold the detail and the values. **Test:** `req_check.sh` lists history and script wording; review: the row holds one checkable rule.
8. **Define every term** the first time a file uses it, or point to where it is defined. **Test:** review: a reader who knows only this folder can follow every term.
9. **State limits.** Anything that grows with use (a log, a list, a table of records) has a limit in DEF-01 (DEF-02). **Test:** review: for each list that grows, find its limit in DEF-01.
10. **Questions** are rows marked `(?)` and appear in `requirements/open-questions.md`. Look for the answer first in the other requirements, the decisions, the code of the running app, and the Flutter and Dart documentation (https://docs.flutter.dev/ and https://dart.dev/), and only then ask the Product Owner. **Test:** `req_check.sh` reports a `(?)` row with no question, and a question with no `(?)` row.
11. **Nothing you write names an agent or a tool.** Name a person by role, as `SCRUM.d/README.md` defines the roles. **Test:** `req_check.sh` lists any agent or tool name.
12. **Prefixes follow the folder.** A row's prefix is its feature's prefix as the Line format gives it. **Test:** `req_check.sh` reports a row whose prefix does not match its folder.
13. **Every requirement has a test.** A row's test cell names the test or says `see <ID>`; `—` stays only until a test exists, and a row with status `planned` or `done` has a test. **Test:** `req_check.sh` counts rows whose test cell is `—` and reports a `planned` or `done` row with `—` as an error.
14. **Messages are keys.** A requirement never contains the wording of a message the user sees; it cites the message as `msg:key` and says when it is shown and what its placeholders hold. The wording and its translations live only in `messages/` (`app_en.arb` is the template). **Test:** `req_check.sh` reports a cited key missing from the template, a locale file that lacks a key the template has, and counts the keys no requirement cites yet.
15. **A new sub-requirement starts `proposed`.** A sub-requirement added under a `backlog` or blank requirement has status `proposed`, and the Product Owner reviews it before a story names it. **Test:** `req_check.sh` lists every `backlog` or blank requirement that has a `proposed` sub-requirement.

## Checking a feature file

A feature file is not done when its rows are written. After organizing a feature into requirements and sub-requirements, go back over it:

1. **The laws and rules**: every row obeys rules 1 to 5 (the laws, numbers, shared homes, specifics only). Search the other files for the same rule in other words before accepting a row as new.
2. **Simulate three jobs**, and fix what stops you:
   - **Coder**: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed.
   - **Tester**: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test.
   - **Reviewer**: the statement says what to build, with no history; the code can be compared with it row by row.

The aim is that the requirement files speak for themselves, so the build rules can stay short.
