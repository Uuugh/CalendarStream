# WORKING.d: the Orchestrator's memory

This is the Orchestrator's memory. If your brief or the Product Owner has not made you the Orchestrator, ignore this folder and file.

Everything here is temporary and holds no rules, so no check reads it. Delete an item when its work is done (git history keeps it). Keep this file under about 40 lines and list every file of this folder below.

## Work in progress and awaiting action

In order; Product Owner items first, then what the Orchestrator can do now, then what waits.

- [ ] The Product Owner reviews the `proposed` rows and answers `requirements/open-questions.md` (a blank status they leave means `backlog`); decides the three proposed rule changes (bucket B in `WORKING.d/CalendarStream.old/build_rules/coder-review-1.md`)
- [ ] Write the Test line for the 32 rules in `SCRUM.d`, `tests` and `packages` READMEs that `req_check.sh` lists as warnings (law 3), and trim the duplicates in `packages/README.md` Testing (its Location line also contradicts `tests/README.md`)
- [ ] Restore or delete the placeholders left when the old app moved (list: `WORKING.d/placeholders.md`)
- [ ] Open: still to fix from the first Coder review: about 30 undefined terms, statements pointing at the legacy theme file, README roles and the DEF prefix, `common.md` to the line format
- [ ] Cold-agent acceptance test of `AGENTS.md`: who am I, where are the rules, the tests and the open questions, what do I read next
- [ ] Story: define how test runs are split and run in parallel and what a run reports; inputs: the parked branch `paused/test-parallel` (commit 85f404b) and requirement DIA-04.c (see `tests/README.md`); CI fills the Tester role for scripted tests only once this report exists
- [ ] Decide Dart CI and release: what CI runs (analysis, tests, `req_check.sh`), whether a green run is part of done, a dependency check, and the release steps (gaps 2, 8, 12, 13, 33 in `WORKING.d/scrum-gaps.md`)
- [ ] Re-run the six Coder slices and compare with the baseline (about 390 of 900 rows could not be implemented); repeat the fix, check and review cycle until the count is acceptable
- [ ] First story, to test the Scrum process: the Scrum dashboard in Flutter/Dart; the Product Owner launches this sprint (brief given: backlog from unassigned requirements and GitHub issues with filters, drag and drop sprint building, issue entry with dropdowns, sprint progress, usage and estimate; samples bolt.new, zeda.io, monday.com agile dashboards, `Desktop/kanban-board-example.jpg`, `Desktop/Scrum-Master-Dashboard-for-Project-Management.png`; plan: branch `dashboard` in its own worktree, a pre-push guard keeps `main` untouched); then port story by story with the `dart-flutter` skill

## Files in this folder

- `move-plan.md`: how to move the live files into the new layout
- `placeholders.md`: plain-text stand-ins left when the old app moved, to restore or delete
- `CalendarStream.old/`: the retired Python app, frozen, an oracle only; delete it when the port is complete
- `scrum-gaps.md`: gaps found by comparing `SCRUM.d/` with the retired `build_rules/` (for decision; delete after)
- `repo-review.md`: the Reviewer agent's findings on the process files against the laws (for decision; delete after)
