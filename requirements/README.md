# Requirements

One file per feature: the checkable rules of behavior the app must meet.

This is the spec of the app.

## Definitions

- **Feature**: an area of the app (Calendar, Sources, Account).
- **Requirement**: one checkable rule of a feature's behavior with an ID (ACC-06), a status and a definitive statement of what to build.
- **Sub-requirement**: one checkable rule that further clarifies a requirement, with a sub-ID (ACC-06.a), a status and a definitive statement of what to build.
- **Issue**: a component not meeting a requirement.
- **Question (?)**: a request for a suggestion; the Product Owner decides.
- **Shared requirements** (`common.md`): behavior several features use, written once and referenced: time (TIM), shared UI (UI), what an origin allows (CAP), defaults and limits (DEF).
- **Parent tests**: the test cell of a requirement that has sub-requirements (rule 13).
- **Test cell**: a list of tests, or `see <ID>` links to the tests of another requirement or sub-requirement, or `—` while there is none.
  A sub-test is simply the test the sub-requirement uses; it may be its own, its parent's, or another requirement's.
- **Evidence (temporary)**: the S keys pointing at the old suites; deleted when the conversion ends.
- **`oldkey.md`**: the record of old IDs to new IDs.
- **Stories, epics, sprints and the backlog** are defined in the process rules.
  A story names the requirement and sub-requirement IDs it will meet and is done when their tests pass.

- **Row**: one line of a requirement table, in the columns `| ID | status | statement | test | evidence (temporary) |`.
  - **ID**: a feature prefix and a number (CAL-03).
    A requirement may have sub-requirements (ACC-06, ACC-06.a, ACC-06.b).
    The prefixes:
    - CAL calendar
    - SRC sources section
    - FDS feeds section
    - CLCL local calendar
    - CFED generic feed
    - CCCS ccs+
    - CLNK calendar link
    - RUL rules
    - TPL event_templates
    - EVT events
    - HIS history
    - CON connections (common)
    - CGOW google one-way
    - CGTW google two-way
    - PLG plugins (common)
    - PGAP google plugin
    - SET settings
    - ACC account
    - DIA diagnostics
    - DOC documentation
    - SHL shell
    - DEP deployment
    - SRH search
    - FLT calendar_filter
    - TIM time, UIC shared interface, CAP capabilities (all three in common.md)
    - PRT print
    - THM theme
  - **status**: `proposed` (drafted, not yet agreed), `backlog` (the Product Owner agreed: it is a Requirement, waiting for a story), `planned` (it is in a story) or `done` (its story was accepted at the Review).
    `SCRUM.d/sprint.md` records which story holds a planned requirement.
  - **test**: the test that verifies it (path and name), once one exists.
  - **evidence (temporary)**: the old-suite keys (and old Dashboard items) a row came from; deleted when the conversion ends.

## Rules for writing and changing requirements (any agent or person)

These apply to every row in `requirements/`.

- **M1** (who, how, when): Or applies the rule when a row is written or changed; PO approves the row (`SCRUM.d/README.md`).
- **TS** (script test): a check in `tests/tools/req_check.sh`, run by Te at every commit that changes a requirement file (`SCRUM.d/README.md`; CI fills the Te role once it exists).
- **TR** (review test): a review step, run by Re when a rule file changes (`SCRUM.d/README.md`); each names what the reviewer looks for.

Every rule links to M1 and to its tests, and a rule with no `[TS]` or `[TR]` test is not a rule (law 3 of `AGENTS.md`).

1. **Define every term** the first time a file uses it, or point to where it is defined.
   **Method:** M1.
   **Test:** [TR] a reader who knows only this folder can follow every term.
2. **Nothing you write names an agent or a tool.**
   Name a person by role, as `SCRUM.d/README.md` defines the roles.
   **Method:** M1.
   **Test:** [TS] `req_check.sh` lists any agent or tool name.
3. **Messages are keys.**
   A requirement never contains the wording of a message the user sees; it cites the message as `msg:key` and says when it is shown and what its placeholders hold.
   The wording and its translations live only in `messages/` (`app_en.arb` is the template).
   **Method:** M1.
   **Test:** [TS] `req_check.sh` reports a cited key missing from the template, a locale file that lacks a key the template has, and counts the keys no requirement cites yet.
4. **One file per feature.**
   One file: `requirements/<feature>.md`.
   **Method:** M1.
   **Test:** [TR] every feature has one file in `requirements/`, named for the feature.
5. **A row says what to build, once, in the user's words.**
   One checkable rule per row.
   No history, no test or script wording, no web-page mechanics, no "is refused" for a control that cannot produce a wrong value.
   A requirement's own statement is general; its sub-requirements hold the detail and the values.
   **Method:** M1.
   **Test:** [TS] `req_check.sh` lists history and script wording.
   [TR] the row holds one checkable rule.
6. **An agreed row has agreed sub-requirements.**
   A row the Product Owner agreed (status `backlog` or blank) can gain a `proposed` sub-requirement; the Product Owner reviews each such sub-requirement before it counts as agreed.
   **Method:** M1.
   **Test:** [TS] `req_check.sh` lists every agreed row that has a `proposed` sub-requirement.
   
7. **Issues are not recorded here.**
   It lives in GitHub issues, not here.
   **Method:** M1.
   **Test:** [TR] no row records a component that does not meet a requirement.
8. **Questions** are rows marked `(?)` and appear in `requirements/open-questions.md`.
   Look for the answer first in the other requirements, the decisions, the code of the running app, and the Flutter and Dart documentation (https://docs.flutter.dev/ and https://dart.dev/), and only then ask the Product Owner.
   **Method:** M1.
   **Test:** [TS] `req_check.sh` reports a `(?)` row with no question, and a question with no `(?)` row.
9. **Numbers live in DEF-01.**
   A limit, a default, a duration or a count appears only in the table in `common.md`, and a number written as a word counts as a number.
   A row says "the time in DEF-01".
   A default that is not a number (a view, a theme) is stated in the row of the control it belongs to.
   **Method:** M1.
   **Test:** [TS] `req_check.sh` lists numbers with units, and number words of two or more, outside DEF-01.
10. **Three homes for shared things.**
    An actionable component several features use (picker, filter, button, dropdown, strength bar, date range) is a UI row in `common.md`.
    A look (color, font, padding, margin, corner, size, duration) is a theme row (`theme.md`) and is used by default.
    A capability several features use (Print) is its own feature.
    **Method:** M1.
    **Test:** [TR] the row does not restate how a shared component works; it links to the UI row, the theme row or the feature that owns it.
11. **Features add only their specifics.**
    A feature row never restates how a shared component works.
    **Method:** M1.
    **Test:** [TR] follow the row's links and nothing is said twice.
12. **State limits.**
    Anything that grows with use (a log, a list, a table of records) has a limit in DEF-01 (DEF-02).
    **Method:** M1.
    **Test:** [TR] for each list that grows, find its limit in DEF-01.
13. **Every requirement has a test.**
    A row's test cell names the test or says `see <ID>`; `—` stays only until a test exists, and a row with status `planned` or `done` has a test.
    A requirement has a matching test.
    A sub-requirement has a matching sub-test.
    A requirement that has sub-requirements passes when all its sub-requirements pass; its own test cell may be `—` or name a test of the whole.
    `—` until the inventory of the old suites (`requirements/inventory/`) has been matched to requirements.
    **Method:** M1.
    **Test:** [TS] `req_check.sh` counts rows whose test cell is `—` and reports a `planned` or `done` row with `—` as an error.
14. **A test says what it verifies.**
    A test says which requirements it verifies and how it runs when several call it (once, or once per requirement); failures are reported per requirement.
    **Method:** M1.
    **Test:** [TR] each test names its requirements and whether one run covers them all or it runs once per requirement.
15. **Links point at the requirement,** not a sub-requirement, unless exactly one detail is meant.
    A link names an ID that exists today.
    When an ID changes, every reference is changed and `oldkey.md` gets a row.
    Other files link to the requirement, not to a sub-requirement.
    A link points at the requirement unless it means exactly one sub-requirement.
    When IDs change, `oldkey.md` records old to new.
    **Method:** M1.
    **Test:** [TS] `req_check.sh` reports a link to an ID that does not exist.
    [TR] `oldkey.md` has a row for every ID change.
16. **Requirements never refer to a story.**
    A story names the requirement IDs; the requirement never names the story.
    **Method:** M1.
    **Test:** [TR] no row names a story, an epic or a sprint.
17. **A row has five columns.**
    A row has the columns ID, status, statement, test and evidence, in that order.
    An ID is a feature prefix, a hyphen and a number; a sub-requirement adds a letter after a dot.
    **Method:** M1.
    **Test:** [TS] `req_check.sh` reports a row that does not have five columns and an ID that is used twice.
18. **A status moves up.**
    The Product Owner agrees to a row by deleting `proposed`; a blank status is read as `backlog` and the Orchestrator writes the word.
    A status moves up this order; the one move down is `planned` to `backlog`, when a requirement leaves its story.
    **Method:** M1.
    **Test:** [TS] `req_check.sh` reports a status that is not `proposed`, `backlog`, `planned` or `done`, and a status that moved down any way but `planned` to `backlog`.
    
19. **Prefixes.**
    A feature's prefix is three letters.
    A module in a subfolder adds that folder's letter before its three letters: C for `connections.d` (CGOW is Google one-way) and P for `plugins.d` (PGAP is the Google API plugin); a folder inside a folder adds its letter in turn.
    A new feature adds its prefix to the list under ID.
    **Method:** M1.
    **Test:** [TS] `req_check.sh` reports a row whose prefix does not match its folder.
    [TR] every prefix used in `requirements/` is in the list, and every listed prefix has a file.

## One file per feature (Nov 17)

Nothing new is added while the transition freeze lasts; these files hold what was already asked for.

Each feature has ONE file here, `requirements/<feature>.md`, with every requirement of that feature in the same table; the status vocabulary is under Definitions (Row).

Reviewing a feature means changing `proposed` rows to `backlog` (or editing or deleting them) in that one file.

Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them.

Modules come in two kinds, connections and plugins.
`connections.md` and `plugins.md` hold what is common to every module of the kind (written once); each module is its own feature file in `connections.d/` or `plugins.d/` and adds only its specifics, linking to the common file.

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

A feature file is not done when its rows are written.

After organizing a feature into requirements and sub-requirements, go back over it:

1. **The laws and rules**: every row obeys the laws in `AGENTS.md` and rules 9, 10 and 11 (numbers, shared homes, specifics only).
   Search the other files for the same rule in other words before accepting a row as new.
2. **Simulate three jobs**, and fix what stops you:
   - **Coder**: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed.
   - **Tester**: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test.
   - **Reviewer**: the statement says what to build, with no history; the code can be compared with it row by row.

The aim is that the requirement files speak for themselves, so the build rules can stay short.
