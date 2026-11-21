# WORKING.d: Orchestrator memory

Read only if your brief or the Product Owner (PO) made you the Orchestrator. `README.md` is temporary and `lessons.md` is kept; holds no rules; no check reads it.
Delete an item when done (git history keeps it). Keep under 4,000 characters, one sentence per item, detail in a listed file.
`CalendarStream.old/` is not memory and holds no rules: the retired Python app, an oracle only.

## To do (order: PO, Orchestrator now, waiting)

- [ ] Next test sprint (the PO launches it): verify the Team-05 commit rule survives several interruptions of each agent (Coder (build), Coder (tests), Tester) and a broken requirement (Team-03.a, Or-02.e.b); record the result in the Review.
- [ ] Resume here: read `WORKING.d/rewrite-comparison.md` (three-way README rewrites, method additions, five Product Owner decisions, state).
- [ ] PO: review `proposed` rows; answer `SCRUM.d/defects.md` (blank status = `backlog`).
- [ ] Dashboard epic of 7 stories (`dashboard-brief.md` J, K): Orchestrator launches each story's Coder (build) and Coder (tests) itself, no sub-orchestrator; first the Reviewer on the whole repo (~25 session %); ask the PO for 5h and 7d readings first and after each story; stop agents at 70%; first window = the Reviewer plus the stories that fit the usage left, chosen by the Orchestrator from the estimates (smallest and most independent first); the PO only launches the sprint.
- [ ] Worktree `CalendarStream-dashboard` (branch `dashboard`): 43 uncommitted files; `flutter build web` fails ("Too few positional arguments: 2 required, 1 given"), fix first; port 8765 serves a stale build. Queued, unbuilt: collapse keeps top-level rows, `+` buttons, add popup (optional number, suggestions), missing sprint file shows an empty board.
- [ ] On dashboard merge (after PO acceptance): stays in `SCRUM.d/dashboard`; remove the Parts list the agent added to `SCRUM.d/README.md`; list `SCRUM.d/dashboard` in the `AGENTS.md` table of contents; start command runs `flutter gen-l10n`; delete `dashboard-brief.md` and `dashboard-review.md`; renames `default`, `{new}` accepted. Next sprint: new Scrum board features (PO picks), new Orchestrator conversation per sprint.
- [ ] Write the Test line for the 32 rules in the `SCRUM.d`, `tests`, `packages` READMEs that `req_check.sh` warns about; trim `packages/README.md` Testing (duplicates; its Location contradicts `tests/README.md`).
- [ ] Move to the Dart package layout (the project is one package): `tests/` to `test/`, `tests/tools/` to `tool/`, `tests/data/` to `test/data/`, `packages/`, `server/`, `client/` into `lib/src/` and `bin/`; fix links; PO to answer one pubspec or several; make the Cb-12, 13, 15 check scripts.
- [ ] Placeholders: restore or delete (`placeholders.md`).
- [ ] From the first Coder review: ~30 undefined terms, statements pointing at the legacy theme file, README roles and the DEF prefix, `common.md` to the line format.
- [ ] Define test-run split, parallel runs and run report (inputs: branch `paused/test-parallel` commit 85f404b, DIA-04.c); CI fills the Tester role only after it exists.
- [ ] Decide Dart CI and release: what CI runs (analysis, tests, `req_check.sh`), green run in done, dependency check, release steps.
- [ ] Re-run the six Coder slices (baseline ~390 of 900 rows unimplementable); repeat fix, check, review until acceptable.
- [ ] Retrospective after sprint 2 decides: `sprint.md` lifecycle vs blocks that outlive a sprint; smoke wording in step 9; Test lines for roles and Orchestrator steps; step 11 position; stalled-agent overlap with Definition of done; usage per model and role (gap 25).; cold test 2 findings: say that the Files below are in WORKING.d; order of pre-flight vs usage reading in step 1 and 11; the first Reviewer run needs a scope in SCRUM.d; the harness gives a subagent the session-start copy of AGENTS.md, so a cold test needs a fresh conversation to see current text

## Files

- `rules-method.md`: how definitions and rules are built (draft; the Product Owner places it)
- `rules-key.md`: old to new numbers of the requirements rules; fix the links, then delete
- `move-plan.md`: plan for moving files into the new layout
- `placeholders.md`: plain-text stand-ins left when the old app moved
- `repo-review.md`: Reviewer findings on the process files (decide, then delete)
- `dashboard-review.md`: Reviewer findings on the `dashboard` branch (decide, then delete)
- `dashboard-brief.md`: round 3 brief, epic, usage chart, samples
- `CalendarStream.old/`: see top; delete when the port is complete
