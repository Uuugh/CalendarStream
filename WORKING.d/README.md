# WORKING.d: the Orchestrator's memory

This is the Orchestrator's memory. If your brief or the Product Owner has not made you the Orchestrator, ignore this folder and file.

Everything here is temporary and holds no rules, so no check reads it. Delete an item when its work is done (git history keeps it). Keep this file under about 40 lines and list every file of this folder below.

## Work in progress and awaiting action

In order; Product Owner items first, then what the Orchestrator can do now, then what waits.

- [ ] The Product Owner reviews the `proposed` rows and answers `requirements/open-questions.md` (a blank status they leave means `backlog`); decides the three proposed rule changes (bucket B in `WORKING.d/CalendarStream.old/build_rules/coder-review-1.md`)
- [ ] Write the Test line for the 32 rules in `SCRUM.d`, `tests` and `packages` READMEs that `req_check.sh` lists as warnings (law 3), and trim the duplicates in `packages/README.md` Testing (its Location line also contradicts `tests/README.md`)
- [ ] Restore or delete the placeholders left when the old app moved (list: `WORKING.d/placeholders.md`)
- [ ] Open: still to fix from the first Coder review: about 30 undefined terms, statements pointing at the legacy theme file, README roles and the DEF prefix, `common.md` to the line format
- [ ] At the first Retrospective compare agent usage per model and per role, then decide which model suits which role (gap 25)
- [ ] Story: define how test runs are split and run in parallel and what a run reports; inputs: the parked branch `paused/test-parallel` (commit 85f404b) and requirement DIA-04.c (see `tests/README.md`); CI fills the Tester role for scripted tests only once this report exists
- [ ] Decide Dart CI and release: what CI runs (analysis, tests, `req_check.sh`), whether a green run is part of done, a dependency check, and the release steps (gaps 2, 8, 12, 13, 33 in `WORKING.d/scrum-gaps.md`)
- [ ] Re-run the six Coder slices and compare with the baseline (about 390 of 900 rows could not be implemented); repeat the fix, check and review cycle until the count is acceptable
- [ ] First story, to test the Scrum process: the Scrum dashboard in Flutter/Dart; the Product Owner launches this sprint (brief given: backlog from unassigned requirements and GitHub issues with filters, drag and drop sprint building, issue entry with dropdowns, sprint progress, usage and estimate; samples bolt.new, zeda.io, monday.com agile dashboards, `Desktop/kanban-board-example.jpg`, `Desktop/Scrum-Master-Dashboard-for-Project-Management.png`; plan: branch `dashboard` in its own worktree, a pre-push guard keeps `main` untouched); then port story by story with the `dart-flutter` skill; merge it when the process test is done and the Product Owner has accepted the stories: it stays under `SCRUM.d/dashboard` (approved); on merge remove the Parts list the agent added to `SCRUM.d/README.md`, list `SCRUM.d/dashboard` in the `AGENTS.md` table of contents, make the start command run `flutter gen-l10n`,; the shared message-key renames (`default`, `{new}`) are accepted
- [ ] The Product Owner directed: when the dashboard sprint is complete, reviewed (Reviewer, usage after-reading, acceptance) and merged, launch a new sprint with a new sub-orchestrator on new Scrum board features (the Product Owner picks which) and use it to test the process: usage readings at start and end (step 11), Coder (tests) from the requirements only, CI as Tester once it exists, the Reviewer on code and the laws, the cold-agent test of the process files
- [ ] At the Retrospective after sprint 2, decide from what ran: the lifecycle of `SCRUM.d/sprint.md` against the board's blocks that outlive a sprint; the smoke wording in step 9 (CI for scripted steps); the branch and worktree in the brief; a Test line for the roles and Orchestrator steps that lack one and the blanket Test under Responsibilities; the position of step 11; the overlap of the stalled-agent rule with the Definition of done (the Product Owner's decision: only fixes 3 and 4 of the Nov 20 review were applied before sprint 2)
- [ ] The Product Owner starts a fresh conversation at 18:21 (after the window reset at 18:20) with the Orchestrator role and gives the 5h and 7d readings; there is no sub-orchestrator: the Orchestrator launches each story's Coder (build) and Coder (tests) itself from the epic in `WORKING.d/dashboard-brief.md` section J, and first runs the Reviewer on the whole repository (process files, requirements rules, the dashboard code) at about 20 to 30 session %
- [ ] Dashboard round 3 (redesign) was stopped a second time at 83% of the 5-hour usage on 2026-11-20 14:25 (progress 4/7); the worktree `CalendarStream-dashboard` holds 43 uncommitted changed files after commits 0d56593 and a9ea4dc, plus fixes queued but unbuilt: collapse keeps top-level rows visible, the `+` buttons and add popup with an optional number and suggestions, the 404-on-sprint-file fix; relaunch with the brief in `WORKING.d/dashboard-brief.md`, "keep the output file and continue with what is not yet written"; `flutter build web` fails in the worktree ("Too few positional arguments: 2 required, 1 given", a call out of step with a changed signature): fix this first at relaunch, and the page served on port 8765 is a stale build until then

## Files in this folder

- `move-plan.md`: how to move the live files into the new layout
- `placeholders.md`: plain-text stand-ins left when the old app moved, to restore or delete
- `CalendarStream.old/`: the retired Python app, frozen, an oracle only; delete it when the port is complete
- `repo-review.md`: the Reviewer agent's findings on the process files against the laws (for decision; delete after)
- `dashboard-review.md`: the Reviewer agent's findings on the `dashboard` branch (for decision; delete after)
- `dashboard-brief.md`: the full round 3 brief for the dashboard agent, including the usage chart (delete when the dashboard merges)
