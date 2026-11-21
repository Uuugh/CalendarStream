# Scrum: roles, work and how agents are run

## Intro

Everything about how work is organized lives here, once. Rules of an area (requirements, Dart) are in that area's README.

A rule is one row: `ID | What | When acted | How tested`. The ID prefix is the role that acts. A sub-rule is ID.a, ID.b and inherits from its parent.

- A blank cell is missing and fails the check. `—` means none, stated. `^` means the parent's value; on a top-level row it means the default, stated once here: the agent does What as written (**how**), the Reviewer tests (**who tests**), per story after the Tester reports `pass` (**when tested**), by the Reviewer's checks Rv-02.a to Rv-02.c (**how tested**). A cell that differs states its own value.
- **When acted** names an event (defined below) or a condition; `^` on a top-level row means always.
- A parent rule is a flow ("runs the Review"); its sub-rules are its steps, in order.

## Definitions

### Roles

- **Product Owner (PO)**: *ROLE* the repository owner; decides. Human. Answers `requirements/open-questions.md`; agrees to rows (deletes `proposed`); launches work; decides which legacy files go; approves requirements; accepts or rejects each story at the Review. Owns the backlog and sets its priority: only the Product Owner sets the priority.
- **Orchestrator (Or)**: *ROLE* keeps the requirements consistent, briefs and checks the other agents, commits and pushes.
- **Coder (build) (Cb)**: *ROLE* implements a story's requirements.
- **Coder (tests) (Ct)**: *ROLE* builds the mirrored requirement tests from the requirements only.
- **Tester (Ts)**: *ROLE* produces a result per requirement (CI for scripted tests, an agent for the rest).
- **Reviewer (Rv)**: *ROLE* read-only; checks work against the rules of its area. The Orchestrator's subagent that tests the process and the rules (`AGENTS.md`, every README, `SCRUM.d/`) by following them cold; outside code development.
- **Team**: both Coders and the Tester.

### Work

- **Backlog**: requirements with status `backlog` (or blank) and open issues, waiting for a story.
- **Story**: names the requirement and sub-requirement IDs it will meet.
- **Epic**: a group of stories (usually one feature). A story that is split becomes an epic of the stories it was split into.
- **Defect**: a requirement an agent cannot act on (unclear, wrong, contradicting another, or missing table information). Its status is `defect`.
- **Issue**: a component not meeting a requirement. It lives in GitHub issues and names the requirement it breaks.
- **Sprint Backlog**: the story list in `SCRUM.d/sprint.md`.
- **Increment**: the sprint's last commit.
- **Size** of a story: its changed files (the rate is in `SCRUM.d/usage.md`).
- **Scratch folder**: the session's scratchpad directory, named in the session's environment.
- **Sprint**: the stories chosen to be built next. A sprint ends when its stories are done or at their review; it has no calendar length.
- **Ready**: a story is Ready when its requirements pass the review in `requirements/README.md` ("Simulate three jobs"), no open question blocks it, every row of it has status `backlog`, and no test cell of it is `—`.
- **Definition of done**: `tests/tools/req_check.sh` passes and the Tester reports `pass` for every requirement of the story, the README and docs the story affects are updated, and the Product Owner accepts it at the Review.

### Events

- **Pre-flight**, **Brief**, **Mid-flight**, **Post-flight**: the Orchestrator's named steps (Or-04, Or-05, Or-06, Or-07), in that order, around each agent it launches.
- **Refinement**: ongoing; breaking a deliverable the Product Owner states into requirements.
- **Review**: the end of a sprint.
- **Retrospective**: after the Review.

## Rules

### Orchestrator

| ID | What | When acted | How tested |
|---|---|---|---|
| Or-01 | Subagents only for: filling a slice, a full review, the port, a story's team, the Reviewer (Rv-01). Short work (edits, fixes, discussion) is done by the Orchestrator itself | ^ | review: each agent the Orchestrator launched is on the list; one outside it is a finding |
| Or-02 | Treats an agent's report as a claim and checks it against the diff and the test output | ^ | review: the post-flight record cites the diff and the test output for each agent report |
| Or-04 | Runs Pre-flight: the sub-rules in order, before launching any agent | Pre-flight | review: the first messages of the session show Or-04.a to Or-04.e done in order |
| Or-04.a | Reads `WORKING.d/README.md` (your memory) | Pre-flight | review: the first message states what `WORKING.d/README.md` held |
| Or-04.b | Runs `git status` and `git diff` | Pre-flight | review: the first message quotes `git status` before any edit |
| Or-04.c | Reads the `Answer:` lines in `requirements/open-questions.md` | Pre-flight | review: the first message names every non-blank `Answer:` line or says there is none |
| Or-04.d | Commits the Product Owner's uncommitted work first, in its own commit (any uncommitted change found at Pre-flight is the Product Owner's) | Pre-flight | `git log` shows the uncommitted change as its own commit before any other commit of the session |
| Or-04.e | Starts the dashboard if `SCRUM.d/dashboard/` exists and it is not running (the start command is in its README) and gives the Product Owner its address | Pre-flight | review: the first message of the session names the address of a running dashboard |
| Or-05 | Brief: one line each: role, slice, output file, what the agent may write, its progress file, the skills it must load and use (`dart-flutter` for Dart, `scrum` for Scrum files), and "read AGENTS.md and follow it" | Brief | review: each brief holds every field the row lists |
| Or-05.a | For a slice of requirements the limit is "add rows and extend your own; never change the status of an existing row" | Brief | review: a slice agent's diff adds rows and changes no status |
| Or-05.b | Blind agents (reverse-engineering) must not read the requirements: give them the minimal row format inline | Brief | review: a blind agent's brief holds the row format and no path into `requirements/` |
| Or-05.c | Writes each brief's acceptance criteria as requirement IDs, and names what is out of scope and which paths the agent may write | Brief | review: each brief lists requirement IDs, what is out of scope and the paths the agent may write |
| Or-05.d | The brief names the agent's own branch and worktree (Team-04) and its output file (in the scratch folder or a path the brief names) | Brief | review: each brief names a branch, a worktree and an output file |
| Or-06 | Does not edit files agents are reading | Mid-flight | review: no file an agent was reading changed between its launch and its report |
| Or-06.a | One agent at a time on files they share (`common.md`, `messages/`) | Mid-flight | review: no two agents ran at once on `common.md` or `messages/` |
| Or-07 | Runs Post-flight: the sub-rules in order, after each agent finishes | Post-flight | review: the post-flight record holds Or-07.a to Or-07.f |
| Or-07.a | Runs `git diff` against the commit before | Post-flight | the post-flight `git diff` |
| Or-07.b | Checks the agent loaded the skills its brief named | Post-flight | review: the record names the skills each agent loaded |
| Or-07.c | Reverts any status that went backwards | Post-flight | `git diff` shows no status moving down the order except as `AGENTS.md` allows |
| Or-07.d | Runs `req_check.sh` | Post-flight | review: the record holds the output of `req_check.sh` |
| Or-07.e | In `WORKING.d/README.md` deletes the item the work finished (in the same commit as the work; git history is the trash) and adds anything newly awaiting action | Post-flight | review: the commit of the work also changes `WORKING.d/README.md` |
| Or-07.f | Pushes | Post-flight | `git log origin/<branch>` matches the local branch |
| Or-08 | Launches a team per story: both Coders and a Tester | Sprint | review: each story has a Coder (build), a Coder (tests) and a Tester in the record |
| Or-08.a | Launches Coder (build) and Coder (tests) together, and the Tester after both report | Sprint | review: the launch times in the record follow the order of the row |
| Or-09 | A story enters a sprint when it is Ready. The Orchestrator checks this before planning | Before planning | review: the check names the review it ran, no test cell of the story is `—`, no `(?)` row blocks it |
| Or-09.b | A story is small enough for one Post-flight check (about 1,000 changed lines); a larger story is split before it starts | Before planning | `git diff --stat` at post-flight; a story over that size was not split |
| Or-09.a | A story that is not Ready is not planned; reports to the Product Owner why (an open question, a `—` test cell, a `defect` row) | Before planning | review: a story with a `—` cell, an open question or a `defect` row has a message to the Product Owner and no launch |
| Or-10 | Progress bars: one simple bar per running agent, nothing else, in every message to the Product Owner until it finishes: label (the agent's role and the story it works on), 20-character bar, `done/total`, and `done` when finished. Do not poll or sleep; draw the bars when a notification arrives; Each agent writes `done/total` to its own progress file (in the session's scratch folder) after each unit | Until the agent finishes | review: every message to the Product Owner while an agent runs holds one bar per agent |
| Or-10.a | Stops every running agent when the Product Owner says stop or their 5-hour usage (`/usage`) passes about 70%, and makes no commit, push or launch until told. The 7-day reading has no stop line: the Product Owner decides from it | A stop message, or usage about 70% | review: after a stop message no agent is running and no commit follows |
| Or-10.b | Sets an alarm for the window's reset time (the status line shows it) that tells the Product Owner and asks for a usage reading | After a stop for usage | review: after a stop for usage an alarm exists for the reset time |
| Or-10.c | Relaunches when the Product Owner says so, with "keep the output file and continue with what is not yet written" | The Product Owner says so | review: a relaunch brief holds the quoted sentence |
| Or-11 | Before a session ends, updates `WORKING.d/README.md` and pushes it: nothing else survives into the next conversation | Before a session ends | `git status` is clean and `WORKING.d/README.md` is pushed at the end of the session |
| Or-12 | Stalled agent: stops an agent in a failure loop (several failed attempts or a growing diff) and keeps its diagnostics. Relaunches it cold from the last verified commit with the objective, the checkpoint, the rules and the verified errors, checked against the repo; or splits the story | An agent in a failure loop | review: a stalled agent's diagnostics are kept and its relaunch brief holds the objective, the checkpoint, the rules and the verified errors |
| Or-13 | Runs the Review: the sub-rules in order | Review | review: the Review holds Or-13.a to Or-13.e |
| Or-13.a | Runs the sprint's last commit as a user runs it, with the made-up data in `tests/data/` | Review | review: the Review names the commit it ran and the data folder |
| Or-13.b | Has a Tester agent follow the written smoke procedure (`tests/smoke.md`, created at the first sprint that needs it) and report pass, fail or not run per step | Review | review: the smoke report has pass, fail or not run per step |
| Or-13.c | Each failure becomes an issue that names the requirement it breaks | Review | review: every issue names a requirement ID |
| Or-13.d | Writes the Review in `SCRUM.d/sprint.md`: per story what passed, failed and was not checked, the smoke result, the Product Owner's accept or reject, and the usage it took | Review | the Review in `sprint.md` holds an accept or reject for every story |
| Or-13.e | Sets each requirement of a story the Product Owner accepted to `done` | Review | review: each accepted story's rows are `done` and no other story's rows are |
| Or-14 | Runs the Retrospective: the sub-rules in order | Retrospective | review: the Retrospective holds Or-14.a to Or-14.c |
| Or-14.a | Writes the findings in `SCRUM.d/sprint.md`; each ends as an issue, a fix or a stated reason | Retrospective | review: each finding in `sprint.md` ends as an issue, a fix or a stated reason |
| Or-14.b | If a process file (`AGENTS.md`, a README, `SCRUM.d/`) changed during the sprint, the Reviewer (a cold agent) given only "read AGENTS.md and follow it" says who it is, where the rules, the tests and the open questions are, and what it reads next; each wrong answer is a finding | Retrospective | the Retrospective in `sprint.md` records that run for every sprint in which a process file changed |
| Or-14.c | Deletes `SCRUM.d/sprint.md` when the Retrospective is done (git history keeps it) | Retrospective | review: `sprint.md` is gone after the Retrospective |
| Or-15 | Records usage: the sub-rules in order | The start and the end of a sprint | review: `usage.md` holds both readings and the estimate for the sprint |
| Or-15.a | Asks the Product Owner for the 5-hour and 7-day usage readings (`/usage` or the status line) and records them in `SCRUM.d/usage.md`: for each sprint and story its estimate, the before and after readings and the actual (after minus before; a window reset in between makes the actual unknown) | The start and the end of a sprint | `usage.md` holds a before and an after reading for every finished sprint |
| Or-15.b | Estimates the next sprint from the nearest finished stories by size, multiplied by the ratio of actual to estimate seen so far, as a range of plus or minus 20% with the projected after-reading (before plus estimate) | The start of a sprint | each planned sprint shows its estimate range |
| Or-15.c | Splits stories until each fits the usage left in the window | The start of a sprint | review: each story's estimate fits the usage left in the window |
| Or-16 | Splits, spills over to the next sprint, or stops a story that misses done | ^ | review: each story that missed done is recorded in `sprint.md` as split, spilled over or stopped |
| Or-17 | Sets a requirement's status to `defect` when an agent reports it cannot act on it; changes the requirement and sets it to `proposed` for the Product Owner's review | An agent (the Orchestrator included) finds a requirement it cannot act on | review: no row an agent reported is left without `defect` or `proposed` |
| Or-18 | Changes a blank status to `backlog` | A blank status is found | `git diff` shows no blank status after the Orchestrator's pass |
| Or-19 | Flags a rule that breaks a Law and proposes its removal and waits for the Product Owner's decision; never removes it alone | A rule is found that breaks a Law | `req_check.sh` lists identical statements (Law 1), exception wording (Law 2) and a rule with no test (Law 3); the review for what a script cannot find is run on request of the Product Owner |
| Or-20 | Never calls for or launches a sprint; waits for the Product Owner's message, which is the only start of a sprint | ^ | review: the sprint was launched by a Product Owner message |
| Or-21 | Never deletes `proposed`; the Product Owner agrees to a row by deleting it | ^ | `git diff` shows no `proposed` removed by the Orchestrator |
| Or-22 | Never accepts a story; the Product Owner accepts or rejects each story at the Review | Review | review: no story is `done` without a Product Owner accept in `sprint.md` |
| Or-23 | Launches more than one team in a sprint only when the Product Owner directs it (one team by default), each on its own stories | Sprint | review: one team per story unless a Product Owner message directs more |
| Or-24 | Runs a sprint once the Product Owner launches it (Or-20), in this order: Pre-flight (Or-04), checks each story is Ready (Or-09), estimates and records the start usage (Or-15), plans from the Product Owner's priority (Or-25), launches each story's team (Or-08, Or-23), then the Review (Or-13) and the Retrospective (Or-14). Launches no agent and makes no commit for the sprint until Or-09 passes for every story (Or-24.c) | The Product Owner launches a sprint | review: the record shows Or-24.a to Or-24.c in the order of the row |
| Or-24.a | Writes `SCRUM.d/sprint.md`: the story IDs (a story that fixes an issue names it as `#N`) and the usage estimate | When the sprint is launched | review: `sprint.md` holds the story IDs and the estimate at the launch |
| Or-24.b | Sets the status of each requirement of a story to `planned` | When the sprint is launched | review: every requirement of a launched story is `planned` |
| Or-24.c | The gate: a launch message from the Product Owner does not agree to rows. No agent is launched until every story's Ready check (Or-09) is written in `SCRUM.d/sprint.md` as passed, naming each requirement and its status | Before the first launch of the sprint | review: `sprint.md` holds the passed Ready check, and it is dated before the first agent launch |
| Or-25 | Never sets or changes the priority of the backlog; plans a sprint from the Product Owner's priority | Planning a sprint | review: the stories of a sprint follow the Product Owner's priority |
| Or-26 | Turns a deliverable the Product Owner states into `proposed` rows in the right feature file, by launching a slice agent when it is large (Or-01); runs "Simulate three jobs" (`requirements/README.md`) before showing the rows; each row traces to the Product Owner's statement | Refinement | review: every new row traces to a Product Owner statement |
| Or-26.a | A value the Product Owner's statement does not give (a number, a name, a test) is written as a `(?)` row and asked in the conversation, never chosen. When the Product Owner asks "Questions?", asks them all before writing a row | Refinement | review: no new row holds a value that the Product Owner's statement or an answer in `open-questions.md` does not give |

### Coder (build)

| ID | What | When acted | How tested |
|---|---|---|---|
| Cb-01 | Works in the smallest testable step, verifies, then commits | ^ | review: the commits are small and each leaves its tests passing |
| Cb-02 | Touches only the files the story needs | ^ | `git diff --stat` shows only files the story needs |
| Cb-03 | Does not weaken or delete a test to make it pass | ^ | review: the diff deletes or weakens no assertion |
| Cb-04 | Reviews its own diff for redundancy and a simpler way before reporting | Before reporting | review: the report names what the self-review found |
| Cb-05 | When a requirement is unclear it proposes alternatives with pros and cons and sends the defect to the Orchestrator | A requirement is unclear | review: each unclear requirement has a report with alternatives and their pros and cons |
| Cb-06 | Builds as `packages/README.md` says | ^ | review: the diff follows Cb-11 to Cb-19 of `packages/README.md` |
| Cb-07 | Updates the affected docs in the same step as the code, searching them for the behaviors of the story's requirement IDs | With the code | review: the diff changes the docs that name the story's behaviors |
| Cb-08 | Adds no dependency without the Product Owner's approval (the approved list is in `packages/README.md`) | Adding a dependency | review: the diff adds no entry to a `pubspec.yaml` that the Product Owner has not approved |

### Coder (tests)

| ID | What | When acted | How tested |
|---|---|---|---|
| Ct-01 | Works from the requirements only, never the implementation, in `test/` (the Dart package layout) | ^ | review: the test diff touches no implementation file and cites only requirements |
| Ct-02 | Creates the tests as `tests/README.md` says | ^ | review: each test follows `tests/README.md` |
| Ct-03 | Writes the test that the test cell of each requirement of the story names | Sprint | review: every test cell of the story names a test file that exists |

### Tester

| ID | What | When acted | How tested |
|---|---|---|---|
| Ts-01 | Produces one result per requirement, in the format of `tests/README.md` (Results) | ^ | review: the report has one result per requirement ID |
| Ts-02 | CI produces the result for scripted tests | ^ | the CI run reports the scripted tests per requirement |
| Ts-03 | A Tester agent produces the result for tests that need an agent and adds the CI run for the commit to its report, so the Orchestrator reads one combined result | ^ | review: the combined report holds the agent's results and the CI run for the commit |
| Ts-04 | `flutter analyze` is clean and `flutter test` passes, run by CI once it exists | ^ | CI reports `flutter analyze` and `flutter test` once CI exists |

### Reviewer

| ID | What | When acted | How tested |
|---|---|---|---|
| Rv-01 | Runs cold, given only `AGENTS.md` | A process file changed, or the Product Owner asks | review: the record shows a Reviewer run for every sprint in which a process file changed |
| Rv-02 | Checks the diff, not the agent's summary, against Rv-02.a to Rv-02.c, for a process file, a draft or an agent report | ^ | review: the report cites the diff, not the agent's summary |
| Rv-02.a | `tests/tools/req_check.sh` reports no errors | ^ | the Reviewer runs it and reports its output |
| Rv-02.b | The work follows the rules in the README of each area it touches (`requirements/README.md`, `tests/README.md`, `packages/README.md`) and the laws in `AGENTS.md` | ^ | the Reviewer names the rule or law each finding breaks (Rv-03) |
| Rv-02.c | Says clearly what was not checked | ^ | the report has a "not checked" list, which may say none |
| Rv-03 | Reports each finding with the rule or requirement ID it breaks, and its file and line | ^ | review: every finding has an ID, a file and a line |

### Team (both Coders and the Tester)

| ID | What | When acted | How tested |
|---|---|---|---|
| Team-01 | Read the requirements and the rule files (`AGENTS.md`, every README, `SCRUM.d/`) | ^ | review: each team member's report names the files it read |
| Team-02 | Never edit the requirements or the rule files | ^ | a team diff touches no requirement or rule file |
| Team-03 | A defect in a requirement (or a flaw in a rule file) goes to the Orchestrator (Or-17) | ^ | review: each reported defect reached the Orchestrator and Or-17 ran |
| Team-04 | Work on your own branch in your own worktree and push only that branch | ^ | `git log main` holds no commit by a team member that the Product Owner did not direct to merge |

### Not yet placed (existing statements I could not give a row)

- "Requirements never refer to a story." Also in `requirements/README.md`.
- Conflict for the Product Owner: Or-07.d runs `req_check.sh` at every Post-flight, but you told me to run it only when you ask.
- Or-09.b: "small enough for one Reviewer run" became "small enough for one Post-flight check" after the Reviewer was moved outside code development.
- "The Dashboard records the sprint in `SCRUM.d/sprint.md` and each requirement's status." (The Dashboard is not a role.)
- Old wording of the Reviewer, removed because the Product Owner corrected that the Reviewer is outside code development: "Runs once per story, cold, after the Tester reports `pass`" (Rv-01), "the Reviewer after the Tester reports `pass` (Rv-01)" (Or-08.a), and "the Reviewer reports no finding against a rule or a requirement" (Definition of done).
- Retrospective timing ("after the Review") is not stated in the original file; to confirm.
- Removed from definitions because rules and the status list in `requirements/README.md` already say them: "A requirement in a story has status `planned`, and `done` once its story is accepted at the Review" (Or-24.b, Or-13.e) and "done when their tests pass" (Definition of done).
- "A story that misses done is split, spilled over to the next sprint or stopped by the Orchestrator" is Or-16; its **Test** line is below.
- **Test** of the Definition of done: the Tester's report per requirement and the Reviewer's report, which names any doc the diff makes out of date, are recorded in `sprint.md`; `req_check.sh` reports a dead link or missing picture in the project `README.md`. (Who records is not stated.)
- "Never builds the app and never plays the Coder" (Orchestrator). Possibly redundant with the Coder definition.
- "also the **Author** of short work" (Orchestrator). Replaced by Or-01; term removed.
