# Scrum: roles, work and how agents are run

Everything about how work is organized lives here, once. Rules of an area (requirements, Dart) are in that area's README.
## Definitions

- **Product Owner (PO)**, a role: the repository owner; decides. Human
- **Orchestrator (Or)**, a role: keeps the requirements consistent, briefs and checks the other agents, commits and pushes.
- **Coder (build) (Cb)**, a role: implements a story's requirements.
- **Coder (tests) (Ct)**, a role: builds the mirrored requirement tests from the requirements only.
- **Tester (Te)**, a role: produces a result per requirement (CI for scripted tests, an agent for the rest).
- **Reviewer (Re)**, a role: read-only; checks work against the rules of its area.
- **Team**: two Coders (build and tests) and one Tester.
- **Backlog**: requirements with status `backlog` (or blank) and open issues, waiting for a story.
- **Story**: names the requirement and sub-requirement IDs it will meet; done when their tests pass.
- **Epic**: a group of stories (usually one feature). A story that is split becomes an epic of the stories it was split into.
- **Defect**: a GitHub issue.
- **Sprint**: the stories chosen to be built next.
- **Ready**: the state of a story that may enter a sprint.
- **Definition of done**: the conditions a story meets to be accepted.

## Rules

Each row is one rule of engagement for one role. The ID is the role code and a number. A rule is a rule only if an agent told its role can act on it, a Tester can verify it, and the verification will happen. Blank cells are not yet answered.

Defaults for a blank Tester or How: the Tester is Re, who checks against rule Re-03; for Or rows Or-19 also runs a `git diff`. A step of the Orchestrator keeps its step number in the Rule cell.

| ID | Rule | When | Where | Tester | How |
|---|---|---|---|---|---|
| PO-01 | Answers `requirements/open-questions.md` | | `open-questions.md` (`Answer:` lines) | | |
| PO-02 | Agrees to a row by deleting `proposed` | | requirement file | | |
| PO-03 | Launches work | | | | |
| PO-04 | Decides which legacy files go | | | | |
| PO-05 | Approves requirements | | | | |
| PO-06 | Directs more than one team in a sprint (one team by default, each on its own stories) | when the PO directs it | | | |
| PO-07 | Launches a sprint; only the PO does | | | Re | review: the sprint was launched by a PO message |
| PO-08 | Accepts or rejects each story | at the Review | `sprint.md` | | |
| Or-01 | Records the sprint and each requirement's status; the sprint's story list and the retrospective's output live in `SCRUM.d/sprint.md`, which is deleted when the sprint is done | | `SCRUM.d/sprint.md`, the requirement row | | |
| Or-02 | Ends a sprint | its stories are done, or at their review | `sprint.md` | | |
| Or-03 | Bounds no sprint by a date | | `sprint.md` | | |
| Or-04 | Launches a team per story | | | | |
| Or-05 | Checks that a story is ready: its requirements pass the review in `requirements/README.md` ("Simulate three jobs") and no open question blocks it | before planning | | Re | review: the check names the review it ran, no test cell of the story is `—`, no `(?)` row blocks it |
| Or-06 | Splits a story over about 1,000 changed lines | before the story starts | | | `git diff --stat` at post-flight |
| Or-07 | Requires a defect to name the requirement it breaks; a story fixes it by naming the issue as `#N` | | GitHub issue | Re | review: every defect issue names a requirement ID |
| Or-08 | Sets a requirement `planned` when it is in a story and `done` once its story is accepted at the Review | | requirement row | | |
| Or-09 | Allows no requirement to refer to a story | | `requirements/` | | |
| Or-10 | Splits, spills over to the next sprint or stops a story that misses done. Done means: `req_check.sh` passes, Te reports `pass` for every requirement, Re reports no finding, the README and docs are updated, the PO accepts | when a story misses done | `sprint.md` | | the Te report per requirement and the Re report (naming any doc the diff makes out of date) are recorded in `sprint.md`; `req_check.sh` reports a dead link or missing picture in the project `README.md` |
| Or-11 | Never builds the app and never plays the Coder | | | | |
| Or-12 | Does short work (edits, fixes, discussion) itself | | | | |
| Or-13 | Treats an agent's report as a claim and checks it against the diff and the test output | | | | |
| Or-14 | Writes each brief's acceptance criteria as requirement IDs and names what is out of scope and which paths the agent may write | | the brief | | |
| Or-15 | Step 1, Pre-flight | session start | | | |
| Or-15.a | Reads `WORKING.d/README.md` (your memory) | | | | |
| Or-15.b | Runs `git status` and `git diff` | | | | |
| Or-15.c | Reads the `Answer:` lines in `requirements/open-questions.md` | | | | |
| Or-15.d | Commits the PO's uncommitted work first, in its own commit | | | | |
| Or-15.e | Starts the dashboard if `SCRUM.d/dashboard/` exists and it is not running (the start command is in its README) and gives the PO its address | | | Re | review: the first message of the session names the address of a running dashboard |
| Or-16 | Step 2, Brief: one line each: role, slice, output file, what the agent may write, its progress file, the skills it must load and use (`dart-flutter` for Dart, `scrum` for Scrum files), and "read AGENTS.md and follow it"; for a slice of requirements the limit is "add rows and extend your own; never change the status of an existing row"; blind agents (reverse-engineering) must not read the requirements and get the minimal row format inline | launching an agent | the brief | | |
| Or-17 | Step 3, Subagents only for long tasks, so the Orchestrator retains its context: filling a slice, a full review, the port; short work is done by the Orchestrator | | | | |
| Or-18 | Step 4, Mid-flight: does not edit files agents are reading; one agent at a time on files they share | while agents run | `common.md`, `messages/` | | |
| Or-19 | Step 5, Post-flight: `git diff` against the commit before; checks the agent loaded the skills its brief named; reverts any status that went backwards; runs `req_check.sh`; deletes the item the work finished in `WORKING.d/README.md` in the same commit (git history is the trash) and adds anything newly awaiting action; pushes | after an agent finishes | `WORKING.d/README.md` | | |
| Or-20 | Step 6, Progress bars: one simple bar per running agent, nothing else: label (the agent's role and the story it works on), 20-character bar, `done/total`, and `done` when finished; each agent writes `done/total` to its own progress file (in the session's scratch folder) after each unit; does not poll or sleep, draws the bars when a notification arrives | every message to the PO until the agent finishes | message to the PO; the progress file | | |
| Or-21 | Step 6, Stop: stops every running agent, makes no commit, push or launch until told, sets an alarm for the window's reset time (the status line shows it) that tells the PO and asks for a usage reading, and relaunches when the PO says so with "keep the output file and continue with what is not yet written" | the PO says stop, or 5-hour usage (`/usage`) passes about 70% | | Re | review: after a stop message no agent is running and no commit follows, and after a stop for usage an alarm exists for the reset time |
| Or-22 | Step 7, Before a session ends: updates `WORKING.d/README.md` and pushes it; nothing else survives into the next conversation | before a session ends | `WORKING.d/README.md` | | |
| Or-23 | Step 8, Stalled agent: stops an agent in a failure loop and keeps its diagnostics; relaunches it cold from the last verified commit with the objective, the checkpoint, the rules and the verified errors, checked against the repo; or splits the story | several failed attempts or a growing diff | | | |
| Or-24 | Step 9, Review: runs the sprint's last commit as a user runs it, with the made-up data in `tests/data/`; has a Tester agent follow the written smoke procedure (`tests/smoke.md`, created at the first sprint that needs it) and report pass, fail or not run per step; the PO tries the increment and accepts or rejects each story; each failure becomes a defect issue; writes the Review in `SCRUM.d/sprint.md`: per story what passed, failed and was not checked, the smoke result, the PO's accept or reject, and the usage it took | end of a sprint | `sprint.md`, `tests/smoke.md`, `tests/data/` | | the Review in `sprint.md` holds an accept or reject for every story |
| Or-25 | Step 10, Retrospective: writes the findings; each ends as an issue, a fix or a stated reason; if a process file (`AGENTS.md`, a README, `SCRUM.d/`) changed during the sprint, a cold agent given only "read AGENTS.md and follow it" says who it is, where the rules, the tests and the open questions are, and what it reads next; each wrong answer is a finding | after the Review | `sprint.md` | | the Retrospective in `sprint.md` records that run for every sprint in which a process file changed |
| Or-26 | Step 11, Usage: asks the PO for the 5-hour and 7-day usage readings (`/usage` or the status line) and records them in `SCRUM.d/usage.md`: for each sprint and story its estimate, the before and after readings and the actual (after minus before; a window reset in between makes the actual unknown); estimates the next sprint from the nearest finished stories by size, multiplied by the ratio of actual to estimate seen so far, as a range of plus or minus 20% with the projected after-reading (before plus estimate); splits stories until each fits the usage left in the window | start and end of a sprint | `usage.md` | | `usage.md` holds a before and an after reading for every finished sprint, and each planned sprint shows its estimate range |
| Cb-01 | Works in the smallest testable step, verifies, then commits | | | | |
| Cb-02 | Touches only the files the story needs | | | | |
| Cb-03 | Does not weaken or delete a test to make it pass | | | | |
| Cb-04 | Reviews its own diff for redundancy and a simpler way | before reporting | | | |
| Cb-05 | Proposes alternatives with pros and cons and sends the defect to Or | a requirement is unclear | | | |
| Cb-06 | Builds as `packages/README.md` says | | | | |
| Cb-07 | Updates the affected docs, searching them for the behaviors of the story's requirement IDs | in the same step as the code | | | |
| Ct-01 | Works from the requirements only, never the implementation | | `tests/` | | |
| Ct-02 | Creates the tests as `tests/README.md` says | | | | |
| Te-01 | Produces one result per requirement, in the format of `tests/README.md` (Results): CI produces it for scripted tests; a Tester agent produces it for tests that need an agent and adds the CI run for the commit to its report, so Or reads one combined result | | | | |
| Te-02 | `flutter analyze` is clean and `flutter test` passes, run by CI once it exists | | | | |
| Tm-01 | Cb, Ct and Te read the requirements and the rule files (`AGENTS.md`, every README, `SCRUM.d/`) and never edit them; a defect in one goes to Or, who changes a requirement as `proposed` | | | | a team diff touches no requirement or rule file |
| Tm-02 | Cb, Ct and Te work on their own branch in their own worktree and push only that branch | | | | `git log main` holds no commit by a team member that the PO did not direct to merge |
| Re-01 | Runs once per story, cold | after Te reports `pass` | | | |
| Re-02 | Checks the diff, not the agent's summary, against the list in Re-03, and reports each finding with the rule or requirement ID it breaks, and its file and line | | | | |
| Re-03 | The checking list (a story, a pull request, a draft or an agent report): 1. `tests/tools/req_check.sh` reports no errors. 2. The work follows the rules in the README of each area it touches (`requirements/README.md`, `tests/README.md`, `packages/README.md`) and the laws in `AGENTS.md`. 3. Say clearly what was not checked | | | | |
