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

## Drafts and approval (Nov 17)

`requirements/drafts/` holds requirements that are only **proposed** (drafted by Claude or ChatGPT from the inventory, README and
CHANGELOG, not yet reviewed). When the Developer decides or approves a row it moves out of `drafts/` into `requirements/<feature>.md`
with status `planned` (approved, not built yet), keeping its ID and noting the date. A feature's approved requirements are therefore in
`requirements/<feature>.md`, and its still-unreviewed ones in `requirements/drafts/<feature>.md`.
