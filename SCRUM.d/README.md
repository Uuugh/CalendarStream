# Scrum: roles, work and how agents are run

<span style="color:#1f6feb">New text is blue.</span> <span style="color:#d29922"><s>Text to delete is amber and struck through.</s></span>
<span style="color:#1f6feb">Approve by making the text plain: remove the colour, or delete the amber text.</span>

Everything about how work is organized lives here, once. Rules of an area (requirements, Dart) are in that area's README.

## Roles

- **Product Owner**: the repository owner. Decides, answers `requirements/open-questions.md`, agrees to rows
  (deletes `proposed`), launches work, decides which legacy files go.
- **Orchestrator**: keeps the requirements consistent, briefs and checks the other agents, commits and pushes. Is also
  the **Author** for short work: edits, fixes and discussion are done by the Orchestrator itself. Never builds the app
  and never plays the Coder. <span style="color:#1f6feb">Treats an agent's report as a claim and checks it against the diff and the test output.</span>
  <span style="color:#1f6feb">Checks the diff for unrelated edits, new dependencies and configuration changes. Writes each brief's acceptance</span>
  <span style="color:#1f6feb">criteria as requirement IDs, and names what is out of scope and which paths the agent may write.</span>
- **Team**: the Orchestrator launches a team per story: two Coders and a Tester. **Coder (build)** implements the
  story's requirements. **Coder (tests)** builds the mirrored requirement tests in `tests/`, working from the
  requirements only, never the implementation. **Tester** runs the tests and reports a result per requirement; how to test is in `tests/README.md`. More than one team
  may work in a sprint only when the Product Owner directs it (one team by default), each on its own stories. A team
  reads the requirements and never edits them; a defect in one goes to the Orchestrator, who changes it as `proposed`; the Product Owner approves requirements.
  Until the port starts, a Coder is a read-only agent reviewing the requirements for what cannot be implemented.
  - <span style="color:#1f6feb">**Coder (build)** also: works in the smallest testable step, verifies, then commits; touches only the files the</span>
    <span style="color:#1f6feb">story needs; adds no dependency without the Product Owner's approval; does not weaken or delete a test to make it</span>
    <span style="color:#1f6feb">pass; reviews its own diff for redundancy and a simpler way before reporting. When a requirement is unclear it</span>
    <span style="color:#1f6feb">proposes alternatives with pros and cons and sends the defect to the Orchestrator.</span>
  - <span style="color:#1f6feb">**Coder (tests)** also: names each test by the behavior and the requirement ID; keeps shared test data and</span>
    <span style="color:#1f6feb">helpers in one place; mocks external systems, not internal logic; writes from the requirement's observable success</span>
    <span style="color:#1f6feb">and failure.</span>
  - <span style="color:#1f6feb">**Tester** also: runs the checks in layers (analysis, tests, `req_check.sh`) after every meaningful change and</span>
    <span style="color:#1f6feb">reports per requirement the command run and its output; says what was not run and why.</span>
- **Reviewer**: read-only; compares requirement files or code with the README rules of its area, row by row.
  <span style="color:#1f6feb">Reviews the actual diff, not the agent's summary: looks for unrelated edits, duplicated code, dependency and</span>
  <span style="color:#1f6feb">configuration changes and secrets, and scales its depth to the risk of the change.</span>

## Work

- **Backlog**: requirements agreed by the Product Owner (status `backlog` or blank) waiting for a sprint.
- **Story**: names the requirement and sub-requirement IDs it will meet; done when their tests pass. Requirements
  never refer to a story.
- **Epic**: a group of stories (usually one feature).
- **Sprint**: the stories chosen to be built next; the Dashboard (not yet built) will record the sprint and done.
  <span style="color:#1f6feb">A sprint ends when its stories are done or at their review; it has no calendar length.</span>
  <span style="color:#1f6feb">Its **Sprint Goal** is one sentence, written by the Orchestrator and agreed by the Product Owner.</span>
  <span style="color:#1f6feb">The sprint's story list and the retrospective's output live in `SCRUM.d/sprint.md`, deleted when the sprint is done.</span>
- <span style="color:#1f6feb">**Ready**: a story enters a sprint when its terms are defined, its tests are named and no open question blocks it;</span>
  <span style="color:#1f6feb">the Orchestrator checks this before planning.</span>
- <span style="color:#d29922"><s>**Definition of done**: `flutter analyze` is clean, `flutter test` passes and `tests/tools/req_check.sh` passes. Until
  Dart tests exist for a requirement, done means `req_check.sh` passes.</s></span> <span style="color:#1f6feb">**Definition of done**: `tests/tools/req_check.sh`</span>
  <span style="color:#1f6feb">passes and the Tester reports `pass` for every requirement of the story. The Product Owner approves the Dart</span>
  <span style="color:#1f6feb">commands (static analysis and tests) that are added to this list once Dart tests exist for the requirement.</span>
  <span style="color:#1f6feb">A story that misses done is split, spilled over to the next sprint or stopped by the Orchestrator.</span>
  At the end of a story, its items are gone from `WORKING.d/README.md` and no file in `WORKING.d/` is unlisted there.

## Orchestrator's responsibilities

1. **Pre-flight.** Read `WORKING.d/README.md` (your memory); run `git status` and `git diff`; read the `Answer:` lines in `requirements/open-questions.md`; commit the
   Product Owner's uncommitted work first, in its own commit.
2. **Brief.** One line each: role, slice, output file, what the agent may write, its progress file, and "read
   AGENTS.md and follow it". For a slice of requirements the limit is "add rows and extend your own; never change the
   status of an existing row". Blind agents (reverse-engineering) must not read the requirements: give them the minimal
   row format inline.
3. **Subagents only for long tasks**: filling a slice, a full review, the port. Short work is done by the Orchestrator.
4. **Mid-flight.** Do not edit files agents are reading. One agent at a time on files they share (`common.md`, `messages/`).
5. **Post-flight.** `git diff` against the commit before; revert any status that went backwards; run `req_check.sh`; in `WORKING.d/README.md` delete the item the work finished (in the same commit as the work; git history is the trash) and add anything newly awaiting action; push.
6. **Progress bars.** One simple bar per running agent, nothing else, in every message to the Product Owner until it
   finishes: label, 20-character bar, `done/total`, and `done` when finished. Each agent writes `done/total` to its own
   progress file (in the session's scratch folder) after each unit. Do not poll or sleep; draw the bars when a
   notification arrives. Pause the agents (stop them) when the Product Owner's 5-hour usage (`/usage`) passes about 70%; relaunch later
   with "keep the output file and continue with what is not yet written".
7. **How agents are run**: cold (no conversation context), read-only for reviews, one slice each.
8. **Before a session ends**, update `WORKING.d/README.md` and push it: nothing else survives into the next conversation.
9. <span style="color:#1f6feb">**Stalled agent.** Stop an agent in a failure loop (several failed attempts or a growing diff) and keep its</span>
   <span style="color:#1f6feb">diagnostics. Relaunch it cold from the last verified commit with the objective, the checkpoint, the rules and the</span>
   <span style="color:#1f6feb">verified errors, checked against the repo; or split the story.</span>
10. <span style="color:#1f6feb">**Review.** At the end of a sprint write a short Review in `SCRUM.d/sprint.md`: per story what passed, failed and</span>
    <span style="color:#1f6feb">was not checked, and the usage it took.</span>
11. <span style="color:#1f6feb">**Retrospective.** Write the findings in `SCRUM.d/sprint.md`; each ends as an issue, a fix or a stated reason.</span>

## Checking incoming work (a pull request, a draft or an agent report)

1. `tests/tools/req_check.sh` reports no errors.
2. It follows the rules in `requirements/README.md` (and the two laws in `AGENTS.md`).
3. No history or Python-app wording, no agent or tool named, no Scrum terms inside requirements.
4. New or changed IDs have a row in `requirements/oldkey.md`; no reference to an ID that does not exist; user-visible wording is a cited message key.
5. A rule found in more than one place is merged, not copied. A question goes in `open-questions.md` only after
   looking in the other requirements, the Python app and https://docs.flutter.dev/ and https://dart.dev/.
6. Say clearly what was not checked.
