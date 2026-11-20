# WORKING.d: the Orchestrator's memory

This is the Orchestrator's memory. If your brief or the Product Owner has not made you the Orchestrator, ignore this folder and file.

Everything here is temporary and holds no rules. Delete an item when its work is done (git history keeps it). Keep this file under about 40 lines and list every file of this folder below.

## Work in progress and awaiting action

In order; Product Owner items first, then what the Orchestrator can do now, then what waits.

- [ ] The Product Owner reviews the `proposed` rows and answers `requirements/open-questions.md` (a blank status they leave means `backlog`); decides the three proposed rule changes (bucket B in `WORKING.d/CalendarStream.old/build_rules/coder-review-1.md`)
- [ ] The Product Owner reads `WORKING.d/scrum-research.md` and decides five points (sprint end rule, Sprint Goal, where the sprint list and retrospective live, a Ready check, how much Review is shown); then a subagent writes them into `SCRUM.d/`. Scrum is resolved before any coding.
- [ ] Read `WORKING.d/role-research.md` (two vibe-coding rule pages mined for agent role responsibilities, written by the scrum agent), then put what fits into the role entries of `SCRUM.d/README.md`; delete the file
- [ ] Add the checks to `tests/tools/req_check.sh`: status regression, every folder README lists its parts, links in `AGENTS.md`, `SCRUM.d/`, `packages/README.md` and this file resolve, this file under its size limit with no ticked item (the Orchestrator makes this change; see `WORKING.d/move-plan.md`)
- [ ] Restore or delete the placeholders left when the old app moved (list: `WORKING.d/placeholders.md`)
- [ ] Open: still to fix from the first Coder review: about 30 undefined terms, statements pointing at the legacy theme file, README roles and the DEF prefix, `common.md` to the line format
- [ ] Cold-agent acceptance test of `AGENTS.md`: who am I, where are the rules, the tests and the open questions, what do I read next
- [ ] Story: define how test runs are split and run in parallel and what a run reports; inputs: the parked branch `paused/test-parallel` (commit 85f404b) and requirement DIA-04.c (see `tests/README.md`)
- [ ] Re-run the six Coder slices and compare with the baseline (about 390 of 900 rows could not be implemented); repeat the fix, check and review cycle until the count is acceptable
- [ ] Port, story by story, with the `dart-flutter` skill (after Scrum is resolved)
- [ ] Later: the dashboard will probably be GitHub Projects

## Files in this folder

- `move-plan.md`: how to move the live files into the new layout
- `placeholders.md`: plain-text stand-ins left when the old app moved, to restore or delete
- `CalendarStream.old/`: the retired Python app, frozen, an oracle only; delete it when the port is complete
- `role-research.md`: (being written) rules from two vibe-coding pages that could define agent role responsibilities (for discussion; delete after)
- `scrum-research.md`: online sources on Scrum for agent teams, options per Scrum part and gaps in `SCRUM.d/` (for discussion; delete after)
