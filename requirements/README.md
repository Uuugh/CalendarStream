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

CAL calendar · SRC sources · FED feeds · RUL rules · TPL event_templates · EVT events · HIS history · GGL google ·
SET settings · ACC account · DIA diagnostics · DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · TIM time, UI shared interface, CAP capabilities (all three in common.md) · PRT print

Nothing new is added while the transition freeze lasts (build_rules/0-overview.md); these files hold what was already
asked for.

## One file per feature (Nov 17)

Each feature has ONE file here, `requirements/<feature>.md`, with every requirement of that feature in the same table. The status says
where it stands: `proposed` (drafted from the inventory, README or CHANGELOG, not yet reviewed by the Product Owner), `planned` (approved,
not built yet), `built`, `verified`, `open`. Reviewing a feature means changing `proposed` rows to `planned` (or editing or deleting
them) in that one file. Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them.

The scans of the README and CHANGELOG and ChatGPT's gap triage (Task E) were folded into these files as `proposed` rows on Nov 18 and the `requirements/drafts/` folder was deleted; the history is in git (commit before the deletion).

## Index (feature files, click to open)

| Feature | File | Requirements | Proposed (to review) |
|---|---|---|---|
| Calendar | [requirements/calendar.md](requirements/calendar.md) | 25 | 10 |
| Calendar filter | [requirements/calendar_filter.md](requirements/calendar_filter.md) | 5 | 0 |
| Print | [requirements/print.md](requirements/print.md) | 8 | 6 |
| Search | [requirements/search.md](requirements/search.md) | 9 | 5 |
| Events | [requirements/events.md](requirements/events.md) | 37 | 33 |
| Event templates | [requirements/event_templates.md](requirements/event_templates.md) | 6 | 6 |
| Rules | [requirements/rules.md](requirements/rules.md) | 58 | 16 |
| Sources | [requirements/sources.md](requirements/sources.md) | 81 | 81 |
| Feeds | [requirements/feeds.md](requirements/feeds.md) | 30 | 30 |
| History | [requirements/history.md](requirements/history.md) | 19 | 19 |
| Google | [requirements/google.md](requirements/google.md) | 92 | 87 |
| Settings | [requirements/settings.md](requirements/settings.md) | 43 | 31 |
| Account | [requirements/account.md](requirements/account.md) | 32 | 30 |
| Shell | [requirements/shell.md](requirements/shell.md) | 20 | 17 |
| Diagnostics | [requirements/diagnostics.md](requirements/diagnostics.md) | 13 | 9 |
| Deployment | [requirements/deployment.md](requirements/deployment.md) | 24 | 21 |
| Documentation | [requirements/documentation.md](requirements/documentation.md) | 9 | 9 |
| Common (time, shared UI, capabilities) | [requirements/common.md](requirements/common.md) | 36 | 19 |

## Checking a feature file

A feature file is not done when its rows are written. After organizing a feature into requirements and sub-requirements, go back over it:

1. **Duplication**: the same rule is not written twice, in this file or another; a number or limit lives only in DEF-01; a repeated detail is merged.
2. **Common elements**: behavior that other features also use (a filter, a picker, an invalid entry, a strength bar) is in `common.md` and referenced here, so this file adds only its own content.
3. **Simulate three jobs**, and fix what stops you:
   - **Coder**: every term is defined; every behavior and boundary is stated; time and size limits are stated; nothing has to be guessed.
   - **Tester**: every row has a visible pass or fail; one rule per row, so a failure says which; time can be controlled in a test.
   - **Reviewer**: the statement says what to build, with no history or Python-app notes; the code can be compared with it row by row.

The aim is that the requirement files speak for themselves, so the build rules can stay short.
