# Requirements

One file per feature: the checkable rules of behavior the app must meet. This is the spec for both the Python app
(the reference) and the Dart port. Defined in `build_rules/0-overview.md` (Inputs); the plan is `build_rules/layer-map.md`.

A requirement is one statement that a test can pass or fail. A feature is the area (a file here). An issue (I) is a
component not meeting a requirement and is kept in the issues database, not here.

## Line format

`| ID | status | statement | test | was |`

- **ID**: a feature prefix and a number, never reused (CAL-03).
- **status**:
  - `verified`: built, and the Developer said Good;
  - `built`: built, still waiting for the Developer's verdict;
  - `open`: built, but the Developer said Bad (the requirement is still right; the code does not meet it);
  - `planned`: not built.
- **test**: the test that verifies it (path and name), once one exists. `—` until the inventory of the Python suites
  (`requirements/inventory/`) has been matched to requirements.
- **was**: the old Dashboard item it came from, for the transition only.

Planned requirements stay in the same table with status `planned`.

## Prefixes

CAL calendar · SRC sources · FED feeds · RUL rules · TPL event_templates · EVT events · HIS history · GGL google ·
SET settings · ACC account · DIA diagnostics · DOC documentation · SHL shell · DEP deployment · SRH search · FLT calendar_filter · TIM time, UI shared interface, CAP capabilities (all three in common.md)

Nothing new is added while the transition freeze lasts (build_rules/0-overview.md); these files hold what was already
asked for.

## One file per feature (Nov 17)

Each feature has ONE file here, `requirements/<feature>.md`, with every requirement of that feature in the same table. The status says
where it stands: `proposed` (drafted from the inventory, README or CHANGELOG, not yet reviewed by the Developer), `planned` (approved,
not built yet), `built`, `verified`, `open`. Reviewing a feature means changing `proposed` rows to `planned` (or editing or deleting
them) in that one file. Shared rules (time TIM, shared interface UI, capabilities CAP) are in `common.md`; features reference them.

`requirements/drafts/` now only holds the scans of the README and CHANGELOG (`readme_gaps.md`, `changelog_gaps_*.md`) and ChatGPT's
Task E output (`gaps_<feature>.md`), which are inputs for Claude; they are not requirements.

## Index (feature files, click to open)

| Feature | File | Requirements | Proposed (to review) |
|---|---|---|---|
| Calendar | [requirements/calendar.md](requirements/calendar.md) | 35 | 22 |
| Calendar filter | [requirements/calendar_filter.md](requirements/calendar_filter.md) | 5 | 0 |
| Search | [requirements/search.md](requirements/search.md) | 8 | 5 |
| Events | [requirements/events.md](requirements/events.md) | 32 | 28 |
| Event templates | [requirements/event_templates.md](requirements/event_templates.md) | 7 | 7 |
| Rules | [requirements/rules.md](requirements/rules.md) | 42 | 0 |
| Sources | [requirements/sources.md](requirements/sources.md) | 59 | 59 |
| Feeds | [requirements/feeds.md](requirements/feeds.md) | 28 | 28 |
| History | [requirements/history.md](requirements/history.md) | 22 | 22 |
| Google | [requirements/google.md](requirements/google.md) | 84 | 79 |
| Settings | [requirements/settings.md](requirements/settings.md) | 48 | 39 |
| Account | [requirements/account.md](requirements/account.md) | 27 | 25 |
| Shell | [requirements/shell.md](requirements/shell.md) | 19 | 16 |
| Diagnostics | [requirements/diagnostics.md](requirements/diagnostics.md) | 4 | 0 |
| Deployment | [requirements/deployment.md](requirements/deployment.md) | 14 | 13 |
| Documentation | [requirements/documentation.md](requirements/documentation.md) | 10 | 10 |
| Common (time, shared UI, capabilities) | [requirements/common.md](requirements/common.md) | 27 | 18 |
