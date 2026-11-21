# Sprint: ocean

Launched by the Product Owner's message "start", after the deliverable "using dart/flutter, generate a locally hosted website with an ocean scene". Re-started 2026-11-21 01:46 after the usage readings below.

## Sprint Backlog
- Story 1: OCN-01 to OCN-07 (`WORKING.d/ocean/requirements.md`). Folder `WORKING.d/ocean`. Branch `sprint/ocean`, worktree `../CalendarStream-ocean`.

## Ready check (Or-09), passed 2026-11-21 01:46
- OCN-01 backlog, OCN-02 backlog, OCN-03 backlog, OCN-04 backlog, OCN-05 backlog, OCN-06 backlog, OCN-07 backlog before launch; now `planned` (Or-24.b). Test cells: five name `test/ocean_test.dart`, two say `see OCN-01`; none is `—`. No `(?)` row; no open question blocks it. "Simulate three jobs" ran before the rows were shown. Size is small.

## Usage (Or-15), 2026-11-21 01:46
- Before (the Product Owner's reading, given when asked): 5h 27%, 7d 77%.
- Estimate: about 17 changed files at 1.3 session % per file (`SCRUM.d/usage.md` rule of thumb, no finished story of this project yet): 22 session %, range 18 to 26 (plus or minus 20%, Or-15.b). Projected after-reading: 5h 49% (45 to 53). Under the 70% stop line (Or-10.a); fits the window (Or-15.c). The 7-day reading has no stop line; the Product Owner decides.

## Split (Or-16), 2026-11-21 01:49, at the Product Owner's direction
- Story 1 is now OCN-01, OCN-05, OCN-06, OCN-07 (the page served at localhost:8080 with the sky and the sea). OCN-02 (sun), OCN-03 and OCN-04 (waves) spill to the next sprint; their rows are back to `backlog`.
- New estimate: about 9 session % (7 to 11), projected after-reading 5h 36% (34 to 38). The Coder (tests) had finished all seven rows; the Tester runs only the four.

## Usage after (Or-15.a)
- After (the Product Owner's reading): 5h 33%, 7d 78%. Actual 6 session % against the estimate of 9 (first estimate 22). Recorded in `SCRUM.d/usage.md`.

## Review (Or-13.d)
- Story 1 (OCN-01, OCN-05, OCN-06, OCN-07): Tester ran `flutter test test/ocean_test.dart`, 5 tests, all passed (the same run also covers OCN-02 to OCN-04). The Orchestrator reran it once and got the same result. Not checked: the server on port 8080 and a real browser (the Tester did not run it; the Orchestrator served it once, got a 200 and the Product Owner viewed it; the server was later stopped for memory); `flutter analyze` (the Coder (build) says clean for its files, 7 info items in the test file); `req_check.sh` (not run on the Product Owner's instruction).
- Smoke result: not run; `tests/smoke.md` does not exist (Or-13.b).
- Product Owner: accept or reject pending.
- Usage: 6 session % actual (5h 27% to 33%; 7d 77% to 78%) against an estimate of 9; `SCRUM.d/usage.md`.

## Retrospective findings (Or-14.b), each ending as a fix, a Product Owner proposal, or a stated reason
Reviewer (cold, Or-14.a), 21 findings:
1. Issue defined twice: fixed (SCRUM.d points at `requirements/README.md`).
2. Laws 1 and 2 restated as `requirements/README.md` rules 1 and 2: fixed, removed at the Product Owner's earlier decision; the rules moved up by two (key in `WORKING.d/rules-key.md`) and the labels in `req_check.sh` were updated.
3. Status vocabulary repeated: stated reason; the definition is in `requirements/README.md`, the rows only use a status as a trigger.
4. Or-27, Or-07.c, Or-07.f restate `AGENTS.md`: stated reason; each cites the rule so a cold Orchestrator finds its limit in `SCRUM.d`; Or-07.c reworded to cite it.
5. Rv-01 and Or-14.a, Or-24 and Or-24.c, Or-05 and Or-05.d overlap: Or-24 fixed (points at Or-24.c); the others stated reason (two roles for one event; a list of fields and the values for them).
6. Cb-19 repeated the Scrum board clause: fixed.
7. "Also in" notes: one removed; the rest stated reason (the holding list is emptied by Product Owner decisions); the freeze line in `requirements/README.md`: proposal to the Product Owner.
8. Or-07.c "except": fixed. The claim that `AGENTS.md` allows fewer moves came from the session-start copy of `AGENTS.md` that a subagent receives (known); stated reason.
9. Cb-14 exception: fixed (split into Cb-14, Cb-14.a, Cb-14.b).
10. Parent test cell `—` against the test rule: fixed at the Product Owner's choice (option A): rule 11 covers a row with no sub-requirements, rule 11.a a row with sub-requirements; `req_check.sh` skips parents.
11. No `**Method:**` in `AGENTS.md`: proposal to the Product Owner; `SCRUM.d` rows state How by default.
12. `tests/README.md` rules without Test lines: proposal to the Product Owner.
13. Cb-14, 16, 17 tested by the wrong script: fixed (own review tests); Cb-12, 13, 15 scripts: issue, to be written.
14. `AGENTS.md` table says `tests/` holds the tests: pending the move to the Dart package layout (`WORKING.d/README.md`).
15. `UIC` against `UI`, `DEF` missing from the prefix list: proposal to the Product Owner.
16. Dangling "moved with the old app": proposal to the Product Owner (already in the `repo-review.md` list).
17. Permanent rules citing `WORKING.d/README.md`: stated reason; the holding lists are temporary.
18. CI described as existing: stated reason; `requirements.yml` runs `req_check.sh` on push; Dart CI is the open item.
19. Conflict note and first-person wording in the holding list: fixed (neutral wording).
20. Numbering gaps: renumber later with a key in `WORKING.d` (Product Owner's instruction); Or-09.b before Or-09.a: fixed; Or-10 several rules in one row: stated reason, one flow.
21. "dashboard" against "Scrum board": fixed in Or-04.e.

Orchestrator, this sprint:
22. Cb and Te did not load the skill their briefs named: fixed (Team-06 now reports the skills loaded).
23. First launch skipped the usage readings and estimate: fixed (Or-24.c).
24. Usage rate 1.3 % per file overestimated (0.35 observed): stated reason; the baseline has one imported data point; this sprint is the first of the project.
25. Ct did not commit until asked: Team-05 exists; stated reason, caught at Post-flight.
26. Orchestrator reran the Tester's tests: fixed (Or-02).
27. "Height 8 to 16" ambiguous (crest to trough or amplitude): proposal to the Product Owner for OCN-06.
28. The split mid-flight saved little because the Coder (build) had finished: stated reason; an estimate of 22 was four times too high.
29. `tests/smoke.md` missing: issue, to be written at the first sprint that needs it.
30. The server was stopped for memory (system low on memory, cause not measured): stated reason; start it again only when asked.
