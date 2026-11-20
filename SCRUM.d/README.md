# Scrum: roles, work and how agents are run

Everything about how work is organized lives here, once. Rules of an area (requirements, Dart) are in that area's README.

## Roles

- **Product Owner**: the repository owner. Decides, answers `requirements/open-questions.md`, agrees to rows
  (deletes `proposed`), launches work, decides which legacy files go.
- **Orchestrator**: keeps the requirements consistent, briefs and checks the other agents, commits and pushes. Is also
  the **Author** for short work: edits, fixes and discussion are done by the Orchestrator itself. Never builds the app
  and never plays the Coder.
- **Team**: the Orchestrator launches a team per story: two Coders and a Tester. **Coder (build)** implements the
  story's requirements. **Coder (tests)** builds the mirrored requirement tests in `tests/`, working from the
  requirements only, never the implementation. **Tester** runs the tests and reports a result per requirement (`tests/README.md`). Before a new test is written, the Tester and the Coder (tests) look for an existing test to share or modify, and do so when it is the more efficient way to verify the requirement; one test may verify several requirements. More than one team
  may work in a sprint only when the Product Owner directs it (one team by default), each on its own stories. A team
  reads the requirements and never edits them; a defect in one goes to the Orchestrator, who changes it as `proposed`; the Product Owner approves requirements.
  Until the port starts, a Coder is a read-only agent reviewing the requirements for what cannot be implemented.
- **Reviewer**: read-only; compares requirement files or code with the README rules of its area, row by row.

## Work

- **Backlog**: requirements agreed by the Product Owner (status `backlog` or blank) waiting for a sprint.
- **Story**: names the requirement and sub-requirement IDs it will meet; done when their tests pass. Requirements
  never refer to a story.
- **Epic**: a group of stories (usually one feature).
- **Sprint**: the stories chosen to be built next; the Dashboard (not yet built) will record the sprint and done.
- **Definition of done**: `flutter analyze` is clean, `flutter test` passes and `tests/tools/req_check.sh` passes. Until
  Dart tests exist for a requirement, done means `req_check.sh` passes. At the end of a story, its items are gone from `WORKING.d/README.md` and no file in `WORKING.d/` is unlisted there.

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

## Checking incoming work (a pull request, a draft or an agent report)

1. `tests/tools/req_check.sh` reports no errors.
2. It follows the rules in `requirements/README.md` (and the two laws in `AGENTS.md`).
3. No history or Python-app wording, no agent or tool named, no Scrum terms inside requirements.
4. New or changed IDs have a row in `requirements/oldkey.md`; no reference to an ID that does not exist; user-visible wording is a cited message key.
5. A rule found in more than one place is merged, not copied. A question goes in `open-questions.md` only after
   looking in the other requirements, the Python app and https://docs.flutter.dev/ and https://dart.dev/.
6. Say clearly what was not checked.
