# Scrum: roles, work and how agents are run

Everything about how work is organized lives here, once. Rules of an area (requirements, Dart) are in that area's README.

## Roles

- **Product Owner**: the repository owner; decides. Human
- **Orchestrator**: keeps the requirements consistent, briefs and checks the other agents, commits and pushes; also the
  **Author** of short work.
- **Coder (build)**: implements a story's requirements.
- **Coder (tests)**: builds the mirrored requirement tests from the requirements only.
- **Tester**: produces a result per requirement (CI for scripted tests, an agent for the rest).
- **Reviewer**: read-only; checks work against the rules of its area.

The Orchestrator launches a team per story: both Coders and a Tester.

## Work

- **Backlog**: requirements agreed by the Product Owner (status `backlog` or blank) waiting for a sprint.
- **Story**: names the requirement and sub-requirement IDs it will meet; done when their tests pass. Requirements
  never refer to a story. Small enough for one Reviewer run (about 1,000 changed lines); a larger story is split before it starts. **Test:** `git diff --stat` at post-flight; a story over that size was not split.
- **Epic**: a group of stories (usually one feature). A story that is split becomes an epic of the stories it was split into.
- **Defect**: a GitHub issue that names the requirement it breaks; a story fixes it by naming the issue as `#N`. **Test:** review: every defect issue names a requirement ID.
- **Sprint**: the stories chosen to be built next; the Dashboard (not yet built) will record the sprint and done.
  Only the Product Owner launches a sprint. A sprint ends when its stories are done or at their review; it has no calendar length.
  Its **Sprint Goal** is one sentence, written by the Orchestrator and agreed by the Product Owner.
  The sprint's story list and the retrospective's output live in `SCRUM.d/sprint.md`, deleted when the sprint is done. **Test:** review: the sprint was launched by a Product Owner message, and `sprint.md` names a goal.
- **Ready**: a story enters a sprint when its requirements pass the review in `requirements/README.md` ("Simulate three
  jobs") and no open question blocks it; the Orchestrator checks this before planning. **Test:** review: the check names the
  review it ran, no test cell of the story is `—`, no `(?)` row blocks it.
- **Definition of done**: `tests/tools/req_check.sh`
  passes and the Tester reports `pass` for every requirement of the story, and the Reviewer reports no finding against a rule or a requirement, and the Product Owner accepts it at the Review. The Product Owner approves the Dart
  commands (static analysis and tests) that are added to this list once Dart tests exist for the requirement.
  A story that misses done is split, spilled over to the next sprint or stopped by the Orchestrator.
  **Test:** the Tester's report per requirement and the Reviewer's report are recorded in `sprint.md`.

## Responsibilities

**Test:** the Reviewer's list under "Checking work" for every role; for the Orchestrator also its post-flight `git diff`.

### Product Owner
Decides; answers `requirements/open-questions.md`; agrees to rows (deletes `proposed`); launches work; decides which
legacy files go; approves requirements. More than one team works in a sprint only when the Product Owner directs it
(one team by default), each on its own stories.

### Team (both Coders and the Tester)
Read the requirements and the rule files (`AGENTS.md`, every README, `SCRUM.d/`) and never edit them. A defect in one goes to
the Orchestrator, who changes a requirement as `proposed`. Work on your own branch in your own worktree and push only that
branch. **Test:** a team diff touches no requirement or rule file, and `git log main` holds no commit by a team member that
the Product Owner did not direct to merge.

### Coder (build)
Works in the smallest testable step, verifies, then commits; touches only the files the story needs; does not weaken or
delete a test to make it pass; reviews its own diff for
redundancy and a simpler way before reporting. When a requirement is unclear it proposes alternatives with pros and
cons and sends the defect to the Orchestrator. Until the port starts, a Coder is a read-only agent reviewing the
requirements for what cannot be implemented. Builds as `packages/README.md` says.

### Coder (tests)
Works from the requirements only, never the implementation, in `tests/`. Creates the tests as `tests/README.md` says.

### Tester
Produces one result per requirement, in the format of `tests/README.md` (Results). CI produces it for scripted tests; a
Tester agent produces it for tests that need an agent and adds the CI run for the commit to its report, so the
Orchestrator reads one combined result.

### Reviewer
Runs once per story, cold, after the Tester reports `pass`. Checks the diff, not the agent's summary, against the list
under "Checking work" below, and reports each finding with the rule or requirement ID it breaks, and its file and line.

### Orchestrator
Never builds the app and never plays the Coder. Short work (edits, fixes, discussion) is done by the Orchestrator itself.
Treats an agent's report as a claim and checks it against the diff and the test output. Writes each brief's acceptance
criteria as requirement IDs, and names what is out of scope and which paths the agent may write.

1. **Pre-flight.** Read `WORKING.d/README.md` (your memory); run `git status` and `git diff`; read the `Answer:` lines in `requirements/open-questions.md`; commit the
   Product Owner's uncommitted work first, in its own commit.
2. **Brief.** One line each: role, slice, output file, what the agent may write, its progress file, the skills it must
   load and use (`dart-flutter` for Dart, `scrum` for Scrum files), and "read AGENTS.md and follow it". For a slice of
   requirements the limit is "add rows and extend your own; never change the
   status of an existing row". Blind agents (reverse-engineering) must not read the requirements: give them the minimal
   row format inline.
3. **Subagents only for long tasks**: filling a slice, a full review, the port. Short work is done by the Orchestrator.
4. **Mid-flight.** Do not edit files agents are reading. One agent at a time on files they share (`common.md`, `messages/`).
5. **Post-flight.** `git diff` against the commit before; check the agent loaded the skills its brief named; revert any status that went backwards; run `req_check.sh`; in `WORKING.d/README.md` delete the item the work finished (in the same commit as the work; git history is the trash) and add anything newly awaiting action; push.
6. **Progress bars.** One simple bar per running agent, nothing else, in every message to the Product Owner until it
   finishes: label, 20-character bar, `done/total`, and `done` when finished. Each agent writes `done/total` to its own
   progress file (in the session's scratch folder) after each unit. Do not poll or sleep; draw the bars when a
   notification arrives. Pause the agents (stop them) when the Product Owner's 5-hour usage (`/usage`) passes about 70%; relaunch later
   with "keep the output file and continue with what is not yet written".
7. **Before a session ends**, update `WORKING.d/README.md` and push it: nothing else survives into the next conversation.
8. **Stalled agent.** Stop an agent in a failure loop (several failed attempts or a growing diff) and keep its
   diagnostics. Relaunch it cold from the last verified commit with the objective, the checkpoint, the rules and the
   verified errors, checked against the repo; or split the story.
9. **Review.** At the end of a sprint: run the sprint's last commit as a user runs it, with the made-up data in `tests/data/`;
   have a Tester agent follow the written smoke procedure (`tests/smoke.md`, created at the first sprint that needs it) and
   report pass, fail or not run per step; the Product Owner tries the increment and accepts or rejects each story. Each
   failure becomes a defect issue. Write the Review in `SCRUM.d/sprint.md`: per story what passed, failed and was not
   checked, the smoke result, the Product Owner's accept or reject, and the usage it took. **Test:** the Review in `sprint.md`
   holds an accept or reject for every story.
10. **Retrospective.** Write the findings in `SCRUM.d/sprint.md`; each ends as an issue, a fix or a stated reason.

## Checking work (a story, a pull request, a draft or an agent report)

1. `tests/tools/req_check.sh` reports no errors.
2. The work follows the rules in the README of each area it touches (`requirements/README.md`, `tests/README.md`,
   `packages/README.md`) and the laws in `AGENTS.md`.
3. Say clearly what was not checked.
