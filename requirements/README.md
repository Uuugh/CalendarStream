# Requirements

One file per feature: the checkable rules of behavior the app must meet. This is the spec for both the Python app
(the reference) and the Dart port. Defined in `build_rules/0-overview.md` (Inputs); the plan is `build_rules/layer-map.md`.

A requirement is one statement that a test can pass or fail. A feature is the area (a file here). An issue (I) is a
component not meeting a requirement and is kept in the issues database, not here.

## Line format

`| ID | status | statement | test | was |`

- **ID**: a feature prefix and a number (CAL-03). Related rules are grouped under one parent ID with sub-requirements (ACC-06, ACC-06.a, ACC-06.b); a reference points at the parent unless it means exactly one detail. When IDs change, `oldkey.md` records old to new.
- **status** (the Developer's way, Nov 17): a **blank status means the Developer agreed**: it is a Requirement. `proposed` and `planned` mean
  not yet agreed; the Developer removes the word when they agree with a row. `verified` means a Dart test passes it. The older `built` and
  `open` came from the Python-era Dashboard and are treated like `planned` until reviewed.
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

The scans of the README and CHANGELOG and ChatGPT's gap triage (Task E) were folded into these files as `proposed` rows on Nov 18 and the `requirements/drafts/` folder was deleted; the history is in git (commit before the deletion).

## Index (feature files, click to open)

| Feature | File | Requirements | Proposed (to review) |
|---|---|---|---|
| Calendar | [requirements/calendar.md](requirements/calendar.md) | 25 | 10 |
| Calendar filter | [requirements/calendar_filter.md](requirements/calendar_filter.md) | 5 | 0 |
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
