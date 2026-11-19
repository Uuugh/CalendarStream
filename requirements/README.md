# Requirements

One file per feature: the checkable rules of behavior the app must meet. This is the spec for both the Python app
(the reference) and the Dart port. Defined in `build_rules/0-overview.md` (Inputs); the plan is `build_rules/layer-map.md`.

## Definitions

- **Feature**: an area of the app (Calendar, Sources, Account). One file: `requirements/<feature>.md`.
- **Requirement**: one checkable rule of a feature's behavior with an ID (ACC-06), a status and a definitive statement of what to build. A requirement has a matching test. Other files link to the requirement, not to a sub-requirement.
- **Sub-requirement**: one checkable rule that further clarifies a requirement, with a sub-ID (ACC-06.a), a status and a definitive statement of what to build. A sub-requirement has a matching sub-test.
- **Issue**: a component not meeting a requirement. It lives in GitHub issues, not here.
- **Process**: how work is done here (`build_rules/`).
- **Question (?)**: a request for a suggestion; the Product Owner decides.
- **Shared requirements** (`common.md`): behavior several features use, written once and referenced: time (TIM), shared UI (UI), what an origin allows (CAP), defaults and limits (DEF).
- **Parent tests**: a requirement that has sub-requirements passes when all its sub-requirements pass; its own test cell may be `—` or name a test of the whole.
- **Test cell**: a list of tests, or `see <ID>` links to the tests of another requirement or sub-requirement, or `—` while there is none. A sub-test is simply the test the sub-requirement uses; it may be its own, its parent's, or another requirement's. A test says which requirements it verifies and how it runs when several call it (once, or once per requirement); failures are reported per requirement (`build_rules/layer-map.md`, testing decisions).
- **Evidence (temporary)**: the S keys pointing at the Python suites; deleted when the conversion ends.
- **Oracle**: the existing Python app and its suites, used once as the reference for what the app does.
- **`oldkey.md`**: the record of old IDs to new IDs.
- **Stories, epics, sprints and the backlog** are defined in the process rules. A story names the requirement and sub-requirement IDs it will meet and is done when their tests pass; requirements never refer to a story.

## Line format

`| ID | status | statement | test | evidence (temporary) |`

- **ID**: a feature prefix and a number (CAL-03). A requirement may have sub-requirements (ACC-06, ACC-06.a, ACC-06.b); a link points at the requirement unless it means exactly one sub-requirement. When IDs change, `oldkey.md` records old to new.
- **status** (the Product Owner's way, Nov 17): a **blank status means the Product Owner agreed**: it is a Requirement. `proposed` and `planned` mean
  not yet agreed; the Product Owner removes the word when they agree with a row. `verified` means a Dart test passes it. The older `built` and
  `open` came from the Python-era Dashboard and are treated like `planned` until reviewed.
- **test**: the test that verifies it (path and name), once one exists. `—` until the inventory of the Python suites
  (`requirements/inventory/`) has been matched to requirements.
- **evidence (temporary)**: the Python-suite keys (and old Dashboard items) a row came from; deleted when the conversion ends.

Planned requirements stay in the same table with status `planned`.

## Prefixes

CAL calendar · SRC sources section · FDS feeds section · LCL local calendar · FED generic feed · CCS ccs+ · LNK calendar link · RUL rules · TPL event_templates · EVT events · HIS history · CON connections (common) · GOW google one-way · GTW google two-way · PLG plugins (common) · GAP google plugin ·
SET settings · ACC account · DIA diagnostics · DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · TIM time, UI shared interface, CAP capabilities (all three in common.md) · PRT print · THM theme

Nothing new is added while the transition freeze lasts (build_rules/0-overview.md); these files hold what was already
asked for.

## One file per feature (Nov 17)

Each feature has ONE file here, `requirements/<feature>.md`, with every requirement of that feature in the same table. The status says

Modules come in two kinds, connections and plugins. `connections.md` and `plugins.md` hold what is common to every module of the kind (written once); each module is its own feature file in `connections.d/` or `plugins.d/` and adds only its specifics, linking to the common file.
where it stands: `proposed` (drafted from the inventory, README or CHANGELOG, not yet reviewed by the Product Owner), `planned` (approved,
not built yet), `built`, `verified`, `open`. Reviewing a feature means changing `proposed` rows to `planned` (or editing or deleting
them) in that one file. Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them.

The scans of the README and CHANGELOG and ChatGPT's gap triage (Task E) were folded into these files as `proposed` rows on Nov 18 and the `requirements/drafts/` folder was deleted; the history is in git (commit before the deletion).

## Index (feature files, click to open)

| Feature | File | Requirements | Proposed (to review) |
|---|---|---|---|
| Calendar | [requirements/calendar.md](requirements/calendar.md) | 30 | 15 |
| Calendar filter | [requirements/calendar_filter.md](requirements/calendar_filter.md) | 10 | 1 |
| Print | [requirements/print.md](requirements/print.md) | 10 | 5 |
| Theme | [requirements/theme.md](requirements/theme.md) | 61 | 9 |
| Search | [requirements/search.md](requirements/search.md) | 11 | 7 |
| Events | [requirements/events.md](requirements/events.md) | 46 | 39 |
| Event templates | [requirements/event_templates.md](requirements/event_templates.md) | 8 | 8 |
| Rules | [requirements/rules.md](requirements/rules.md) | 64 | 23 |
| History | [requirements/history.md](requirements/history.md) | 28 | 24 |
| Sources (section) | [requirements/sources.md](requirements/sources.md) | 2 | 1 |
| Feeds (section) | [requirements/feeds.md](requirements/feeds.md) | 2 | 1 |
| Connections (common) | [requirements/connections.md](requirements/connections.md) | 58 | 49 |
| Local calendar | [requirements/connections.d/local_calendar.md](requirements/connections.d/local_calendar.md) | 16 | 13 |
| Generic Feed | [requirements/connections.d/generic_feed.md](requirements/connections.d/generic_feed.md) | 28 | 23 |
| CCS+ | [requirements/connections.d/ccs.md](requirements/connections.d/ccs.md) | 30 | 25 |
| Calendar link | [requirements/connections.d/calendar_link.md](requirements/connections.d/calendar_link.md) | 5 | 4 |
| Google one-way sync | [requirements/connections.d/google_one_way.md](requirements/connections.d/google_one_way.md) | 71 | 65 |
| Google two-way sync | [requirements/connections.d/google_two_way.md](requirements/connections.d/google_two_way.md) | 7 | 6 |
| Plugins (common) | [requirements/plugins.md](requirements/plugins.md) | 1 | 0 |
| Google plugin (API client) | [requirements/plugins.d/google_api.md](requirements/plugins.d/google_api.md) | 20 | 18 |
| Settings | [requirements/settings.md](requirements/settings.md) | 55 | 39 |
| Account | [requirements/account.md](requirements/account.md) | 56 | 51 |
| Shell | [requirements/shell.md](requirements/shell.md) | 27 | 21 |
| Diagnostics | [requirements/diagnostics.md](requirements/diagnostics.md) | 17 | 13 |
| Deployment | [requirements/deployment.md](requirements/deployment.md) | 29 | 26 |
| Documentation | [requirements/documentation.md](requirements/documentation.md) | 12 | 12 |
| Common (time, shared UI, capabilities) | [requirements/common.md](requirements/common.md) | 76 | 36 |

## Checking a feature file

A feature file is not done when its rows are written. After organizing a feature into requirements and sub-requirements, go back over it:

1. **Duplication**: the same rule is not written twice, in this file or another; a number or limit lives only in DEF-01; a repeated detail is merged.
2. **Common elements**: behavior that other features also use (a filter, a picker, an invalid entry, a strength bar) is in `common.md` and referenced here, so this file adds only its own content.
3. **Simulate three jobs**, and fix what stops you:
   - **Coder**: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed.
   - **Tester**: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test.
   - **Reviewer**: the statement says what to build, with no history or Python-app notes; the code can be compared with it row by row.

The aim is that the requirement files speak for themselves, so the build rules can stay short.

## Rules for writing and changing requirements (any agent or person)

These apply to every row in `requirements/`. `tests/tools/req_check.sh` checks what a script can check; the rest is judgment, so read them.

1. **Law: no duplication. Say it once.** A rule is written in one place and referenced everywhere else. Before adding a row, search the folder for the same rule in other words.
2. **Law: no exceptions.** If a rule has an exception, the requirement is wrong: change it so it holds for every case, or give the different case its own requirement. A row never says "except", "never for" or "only when X is not". A new kind of thing (a connection, a component) follows the existing rules and does not get a special case.
3. **Numbers live in DEF-01.** A limit, a default, a duration or a count appears only in the table in `common.md`; a row says "the time in DEF-01". A default that is not a number (a view, a theme) is stated in the row of the control it belongs to.
4. **Three homes for shared things.** An actionable component several features use (picker, filter, button, dropdown, strength bar, date range) is a UI row in `common.md`. A look (color, font, padding, margin, corner, size, duration) is a theme row (`theme.md`) and is used by default. A capability several features use (Print) is its own feature. The user feature only adds details (which content, which order, which default).
5. **Features add only their specifics.** A feature row never restates how a shared component works.
6. **Links point at the requirement,** not a sub-requirement, unless exactly one detail is meant. A link names an ID that exists today; when an ID changes, every reference is changed and `oldkey.md` gets a row.
7. **A row says what to build, once, in the user's words.** One checkable rule per row. No history ("the Python app does…"), no test or script wording, no web-page mechanics, no "is refused" for a control that cannot produce a wrong value. A requirement's own statement is general; its sub-requirements hold the detail and the values.
8. **Define every term** the first time a file uses it, or point to where it is defined.
9. **State limits.** Anything that grows with use (a log, a list, a table of records) has a limit in DEF-01 (DEF-02).
10. **Questions** are rows marked `(?)` and appear in `build_rules/open-questions.md`. Look for the answer first in the other requirements, the decisions, the code of the running app, and the Flutter and Dart documentation (https://docs.flutter.dev/ and https://dart.dev/), and only then ask the Product Owner.
11. **Nothing you write names an agent or a tool.** Roles are the Product Owner, the developer and the tester.
