# Scrum: roles, work and how agents are run

## Intro

Everything about how work is organized lives here, once. Rules of an area (requirements, Dart) are in that area's README.

A rule is one row: `ID | What | When acted | How tested`. The ID prefix is the role that acts. A sub-rule is ID.a, ID.b and inherits from its parent.

- A blank cell is missing and fails the check. `—` means none, stated. `^` means the parent's value; on a top-level row it means the default, stated once here: the agent does What as written (**how**), the Orchestrator tests a team's row at Post-flight (Or-07) and the Reviewer tests a process file when it changes (Rv-01) (**who tests**, **when tested**), by the row's own cell, or by Rv-02.a to Rv-02.c when it says `^` (**how tested**). A cell that differs states its own value.
- **When acted** names an event (defined below) or a condition; `^` on a top-level row means always.
- A parent rule is a flow ("runs the Review"); its sub-rules are its steps, in order.

## Definitions

### Roles

- **Product Owner (PO)**: *ROLE* the repository owner; decides. Human. Answers `SCRUM.d/defects.md`; agrees to rows (deletes `proposed`); launches work; decides which legacy files go; approves requirements; accepts or rejects each story at the Review. Owns the backlog and sets its priority: only the Product Owner sets the priority.
- **Orchestrator (Or)**: *ROLE* keeps the requirements consistent, briefs and checks the other agents, commits and pushes.
- **Coder (build) (Cb)**: *ROLE* implements a story's requirements.
- **Coder (tests) (Ct)**: *ROLE* builds the mirrored requirement tests from the requirements only.
- **Tester (Te)**: *ROLE* runs the tests Ct wrote and produces a result per requirement.
- **Reviewer (Rv)**: *ROLE* read-only; checks work against the rules of its area. The Orchestrator's subagent that tests the process and the rules (`AGENTS.md`, every README, `SCRUM.d/`) by following them cold; outside code development.
- **Team**: both Coders and the Tester.

### Work

- **Backlog**: requirements with status `backlog` (or blank) and open issues, waiting for a story.
- **Story**: names the requirement and sub-requirement IDs it will meet.
- **Epic**: a group of stories (usually one feature). A story that is split becomes an epic of the stories it was split into.
- **Defect**: a line an agent cannot act on (unclear, wrong, or missing information: a table cell, a name or a value), or a requirement that states more than one rule (`requirements/README.md`, rule 5). Or-02.e.b marks it.
- **Issue**: defined in `requirements/README.md`; it names the requirement it breaks.
- **Sprint Backlog**: the story list in `SCRUM.d/sprint.md`.
- **Increment**: the sprint's last commit.
- **Size** of a story: its changed files (the rate is in `SCRUM.d/usage.md`).
- **Scratch folder**: the session's scratchpad directory, named in the session's environment.
- **Sprint**: the stories chosen to be built next. A sprint ends with its Retrospective, after its stories are done or at their review; it has no calendar length.
- **Definition of done**: `tests/tools/req_check.sh` passes and the Tester reports `pass` for every requirement of the story, the README and docs the story affects are updated, and the Product Owner accepts it at the Review.

### Events

- **Pre-flight**, **Brief**, **Mid-flight**, **Post-flight**: the Orchestrator's named steps (Or-04, Or-05, Or-06, Or-07), in that order, around each agent it launches.
- **Refinement**: ongoing; breaking a deliverable the Product Owner states into requirements.
- **Review**: the last step of a sprint's work, before the Retrospective.
- **Retrospective**: after the Review.

## Rules

### Orchestrator

| ID | What | When acted | How tested |
|---|---|---|---|
| Or-01 | Delegates work by two intents: protecting the Orchestrator's context and the Product Owner's usage on long work, and independence for work that needs a cold reader or no sight of the implementation | Always | ^ |
| Or-01.a | Work that needs a cold reader, or no sight of the implementation, is always delegated: the Reviewer (Rv-01), the Coder (tests), the Tester | Always | review: each such task was done by a launched agent |
| Or-01.b | Other work is delegated when doing it inline would cost more of the Orchestrator's context or of the usage than a brief and a check (filling a slice, a story's build, the port) | Always | review: each agent launched outside Or-01.a was sized (Or-15.b) against the cost of its brief and check |
| Or-01.c | Edits, fixes and discussion are done by the Orchestrator itself | Always | review: no agent was launched for an edit, a fix or a discussion |
| Or-02 | Changes a rule, a definition or a requirement only through Or-02.a to Or-02.f; a mark (🟡, 🟠, 🔴) goes inside the line's first cell, before the ID (at the start of a list item when it has no cell), and is removed when the Product Owner has answered | Always | ^ |
| Or-02.a | Before changing or removing any rule, looks up its ID in `WORKING.d/lessons.md` | A rule is to be changed or removed | review: each change to a rule cites the entry it read, or says there is none |
| Or-02.b | When a correction changes a rule, writes the entry in `WORKING.d/lessons.md` (one or two sentences) | A correction changes a rule | review: each correction-driven change has an entry |
| Or-02.c | Never deletes `proposed`; the Product Owner agrees to a row by deleting it | Always | `git diff` shows no `proposed` removed by the Orchestrator |
| Or-02.d | Raises a request of the Product Owner that would break a rule, a check or a Law, with what it would break; the Product Owner decides | A breaking request | review: for each breaking request, the conversation named what would break before the change |
| Or-02.e | Marks a line it questions, cannot act on, or finds bad, with one of three marks (Or-02.e.a to Or-02.e.c), and removes the mark when the Product Owner has answered | A line is questioned, unactionable or bad | review: no 🟡, 🟠 or 🔴 is left on a line whose question, rewrite or proposal was answered |
| Or-02.e.a | 🟡 A question about a written line (a definition, a rule, a requirement) is asked in the conversation | A question about a written line | review: each 🟡 has its question in the conversation |
| Or-02.e.b | 🟠 A line an agent cannot act on (a cold agent finds no answer, an ambiguity or a conflict) is rewritten by the Orchestrator, which asks only if the rewrite changes what the rule means. A requirement it cannot act on is marked by the status `defect`; the Orchestrator changes it, using the alternatives the agent proposed (Cb-05) when it gave them, and sets it to `proposed` for the Product Owner's review | Any agent, the Orchestrator included, cannot act on a line, or a row states more than one rule | review: each 🟠 has a recorded rewrite and any change of meaning was asked; no requirement an agent reported is left without `defect` or `proposed` |
| Or-02.e.c | 🔴 A line that breaks a Law or contradicts another line is flagged and its removal proposed to the Product Owner, who decides; never removed alone | A line is found that breaks a Law or contradicts another | `req_check.sh` lists identical statements (Law 1), exception wording (Law 2) and a rule with no test (Law 3); the review for what a script cannot find is run on request of the Product Owner; review: each 🔴 was proposed to the Product Owner |
| Or-02.f | Changes a blank status to `backlog` | A blank status is found | `git diff` shows no blank status after the Orchestrator's pass |
| Or-03 | Treats an agent's report as a claim and checks it against the diff and the test output; a Tester's report is checked by its named command and its one result per requirement ID, and the Orchestrator reruns a test only when the report lacks the command or a result | ^ | review: the post-flight record cites the diff and the test output for each agent report |
| 🟡 Or-03.a | When a Tester's result names an uncovered clause: a clause that can fail on its own, with the rest of the row passing, could be a requirement of its own, so the requirement states more than one rule and is a defect (Or-02.e.b) naming the clause; any other clause goes back to the Coder (tests) (Ct-03) | A Tester's report names an uncovered clause, after any `fail` of the row (Or-03.b) | review: each uncovered clause has a test added, or its requirement is `defect` or `proposed` and names it |
| 🟡 Or-03.b | A result `fail` goes back to the Coder (build), or to the Coder (tests) (Ct-02) when the Tester's result says the test is wrong | A Tester's report has a `fail` | review: each `fail` has a fix commit after the failing result |
| 🟡 Or-03.c | A result `not run` goes back to the Coder (tests) (Ct-02) when the test could not start, or to the Coder (build) when the code crashed it | A Tester's report has a `not run` | review: each `not run` has a later result that is not `not run` |
| Or-04 | Runs Pre-flight: the sub-rules in order, before launching any agent | Pre-flight | review: the first messages of the session show Or-04.a to Or-04.e done in order |
| Or-04.a | Reads `WORKING.d/README.md` (your memory) | Pre-flight | review: the first message states what `WORKING.d/README.md` held |
| Or-04.b | Runs `git status` and `git diff` | Pre-flight | review: the first message quotes `git status` before any edit |
| Or-04.c | Reads the `Answer:` lines in `SCRUM.d/defects.md` | Pre-flight | review: the first message names every non-blank `Answer:` line or says there is none |
| Or-04.d | Commits the Product Owner's uncommitted work first, in its own commit (any uncommitted change found at Pre-flight is the Product Owner's) | Pre-flight | `git log` shows the uncommitted change as its own commit before any other commit of the session |
| Or-04.e | Starts the Scrum board if `SCRUM.d/dashboard/` exists and it is not running (the start command is in its README) and gives the Product Owner its address | Pre-flight | review: the first message of the session names the address of a running Scrum board |
| Or-05 | Brief: one line each: role, slice, output file, what the agent may write, its progress file, the skills it must load and use (`dart-flutter` for Dart, `scrum` for Scrum files), and "read AGENTS.md and follow it"; Or-05.a to Or-05.d add to the brief | Brief | review: each brief holds every field the row lists |
| Or-05.a | For a slice of requirements the limit is "add rows and extend your own; never change the status of an existing row" | Brief | review: a slice agent's diff adds rows and changes no status |
| Or-05.b | Blind agents (reverse-engineering) must not read the requirements: give them the minimal row format inline | Brief | review: a blind agent's brief holds the row format and no path into `requirements/` |
| Or-05.c | Writes each brief's acceptance criteria as requirement IDs, and names what is out of scope and which paths the agent may write | Brief | review: each brief lists requirement IDs, what is out of scope and the paths the agent may write |
| Or-05.d | The brief names the sprint's branch and the team's worktree (Team-04) and its output file (in the scratch folder or a path the brief names) | Brief | review: each brief names a branch, a worktree and an output file |
| Or-06 | Does not edit files agents are reading | Mid-flight | review: no file an agent was reading changed between its launch and its report |
| Or-06.a | One agent at a time on files they share (`common.md`, `messages/`) | Mid-flight | review: no two agents ran at once on `common.md` or `messages/` |
| Or-07 | Runs Post-flight: the sub-rules in order, after each agent finishes | Post-flight | review: the post-flight record holds Or-07.a to Or-07.f |
| Or-07.a | Runs `git diff` against the commit before | Post-flight | the post-flight `git diff` |
| Or-07.b | Checks the agent loaded the skills its brief named | Post-flight | review: the record names the skills each agent loaded |
| Or-07.c | Reverts any status move that the status rule in `AGENTS.md` (Standing rules) does not allow | Post-flight | `git diff` shows no status move that rule does not allow |
| Or-07.e | In `WORKING.d/README.md` deletes the item the work finished (in the same commit as the work; git history is the trash) and adds anything newly awaiting action | Post-flight | review: the commit of the work also changes `WORKING.d/README.md` |
| Or-07.f | Pushes | Post-flight | `git log origin/<branch>` matches the local branch |
| Or-07.g | Edits the docs the Coder (build) reported as needing a change (Cb-07), in the same commit as the work | Post-flight | review: no doc named in a Coder report is left unchanged |
| Or-08 | Launches a team per story: both Coders and a Tester | Sprint | review: each story has a Coder (build), a Coder (tests) and a Tester in the record |
| Or-08.a | Launches Coder (build) and Coder (tests) together, and the Tester after both report; each writes only the paths its brief names (Or-05.c), so they do not collide | Sprint | review: the launch times in the record follow the order of the row |
| Or-09 | Before planning, checks that every row of a story has status `backlog`, that a row without sub-requirements has a test cell that is not `—`, and that no `(?)` row blocks it | Before planning | review: the check names each of the three conditions and its result for each row |
| Or-09.a | A story that fails Or-09 is not planned; reports to the Product Owner why (an open question, a `—` test cell, a `defect` row) | Before planning | review: a story with a `—` cell, an open question or a `defect` row has a message to the Product Owner and no launch |
| Or-10 | Progress bars: one simple bar per running agent, nothing else, in every message to the Product Owner until it finishes: label (the agent's role and the story it works on), 20-character bar, `done/total`, and `done` when finished. Do not poll or sleep; draw the bars when a notification arrives; Each agent writes `done/total` to its own progress file (in the session's scratch folder) after each unit | Until the agent finishes | review: every message to the Product Owner while an agent runs holds one bar per agent |
| 🟡 Or-10.a | When the Product Owner says stop, or the 5-hour or 7-day reading (`/usage`) reaches the warning level in `SCRUM.d/usage.md` (Levels) for a job the Product Owner has not permitted, tells every running agent to commit its work in progress and stop, and makes no launch or push until told | A stop message, or a reading at the warning level | review: after a stop message or such a reading every agent's work in progress is committed, no agent is running, and no launch or push follows |
| Or-10.d | Before starting a job, compares its projected after-reading of each window (Or-15.b) with the levels in `SCRUM.d/usage.md`; when it ends at or above the caution level, notifies the Product Owner, naming the job and its projected after-readings so the Product Owner can adjust priorities, and continues | Before starting a job | review: each job projected at or above the caution level was preceded by the notice in the conversation |
| 🟡 Or-10.e | When a job's projected after-reading of either window ends at or above the warning level, asks the Product Owner's permission and waits before starting | Before starting a job | review: no job projected at or above the warning level started without a Product Owner message permitting it |
| 🟡 Or-10.g | Before starting a job and after each agent finishes, reads the 5-hour and 7-day readings from the readings file named in `SCRUM.d/usage.md` (Levels) and applies Or-10.a and Or-10.d to Or-10.f to them; asks the Product Owner for a reading when the file is missing or stale | Before starting a job; after each agent finishes | review: the record shows a reading taken from a file whose `written_at` was within the stale limit before each launch and after each agent finished, or a request to the Product Owner |
| 🟡 Or-10.f | When a reading reaches the caution level while an agent runs, tells it to commit its work in progress at the end of its current unit | A reading at the caution level while an agent runs | review: each agent running at that time has a commit after the message |
| Or-10.b | Sets an alarm for the window's reset time (the status line shows it) that tells the Product Owner and asks for a usage reading | After a stop for usage | review: after a stop for usage an alarm exists for the reset time |
| Or-10.c | Relaunches when the Product Owner says so, with "keep the output file and continue with what is not yet written" | The Product Owner says so | review: a relaunch brief holds the quoted sentence |
| Or-11 | Before a session ends, updates `WORKING.d/README.md` and pushes it: nothing else survives into the next conversation | Before a session ends | `git status` is clean and `WORKING.d/README.md` is pushed at the end of the session |
| Or-12 | Stalled agent: stops an agent in a failure loop (several failed attempts or a growing diff) and keeps its diagnostics. Relaunches it cold from the last verified commit with the objective, the checkpoint, the rules and the verified errors, checked against the repo; or splits the story | An agent in a failure loop | review: a stalled agent's diagnostics are kept and its relaunch brief holds the objective, the checkpoint, the rules and the verified errors |
| Or-13 | Runs the Review: the sub-rules in order | Review | review: the Review holds Or-13.a to Or-13.e |
| Or-13.a | Runs the sprint's last commit as a user runs it, with the made-up data in `tests/data/` | Review | review: the Review names the commit it ran and the data folder |
| 🟡 Or-13.b | Has a Tester agent follow the smoke procedure (`test/smoke.md`) and report each step (`tests/README.md`, Layout); when the file does not exist, has the Coder (tests) write it first (Ct-04) | Review | review: at the Review the file exists and the smoke report has a result for each step |
| Or-13.c | Each failure becomes an issue that names the requirement it breaks | Review | review: every issue names a requirement ID |
| Or-13.d | Writes the Review in `SCRUM.d/sprint.md`: per story what passed, failed and was not checked, the smoke result, the Product Owner's accept or reject, and the usage it took | Review | the Review in `sprint.md` holds an accept or reject for every story |
| Or-13.e | Runs `req_check.sh` and sets each requirement of a story the Product Owner accepted to `done` only when it reports no errors (Definition of done) | Review | review: each accepted story's rows are `done` and no other story's rows are, and the record holds the output of `req_check.sh` |
| Or-14 | Runs the Retrospective: the sub-rules in order | Retrospective | review: the Retrospective holds Or-14.a to Or-14.c |
| Or-14.a | If a process file (`AGENTS.md`, a README, `SCRUM.d/`) changed during the sprint, the Reviewer (a cold agent) given only "read AGENTS.md and follow it" says who it is, where the rules, the tests and the open questions are, and what it reads next; each wrong answer is a finding | Retrospective | the Retrospective in `sprint.md` records that run for every sprint in which a process file changed |
| Or-14.b | Writes the findings in `SCRUM.d/sprint.md`; each ends as an issue, a fix or a stated reason | Retrospective | review: each finding in `sprint.md` ends as an issue, a fix or a stated reason |
| Or-14.c | Deletes `SCRUM.d/sprint.md` when the Retrospective is done (git history keeps it) | Retrospective | review: `sprint.md` is gone after the Retrospective |
| Or-14.d | Asks the Product Owner whether to start the next sprint (Or-20) | Retrospective | review: the question is the last message of the Retrospective |
| Or-15 | Records usage: the sub-rules in order | The start and the end of a sprint | review: `usage.md` holds both readings and the estimate for the sprint |
| Or-15.a | Asks the Product Owner for the 5-hour and 7-day usage readings (`/usage` or the status line) and records them in `SCRUM.d/usage.md`: for each sprint and story its estimate, the before and after readings and the actual (after minus before; a window reset in between makes the actual unknown) | The start and the end of a sprint | `usage.md` holds a before and an after reading for every finished sprint |
| Or-15.b | Estimates the next sprint from the nearest finished stories by size, multiplied by the ratio of actual to estimate seen so far, as a range of plus or minus 20% with the projected after-reading (before plus estimate) | The start of a sprint | each planned sprint shows its estimate range |
| Or-15.c | Splits stories until each ends below the warning level in `SCRUM.d/usage.md`, or the Product Owner permits it (Or-10.e) | The start of a sprint | review: each story's projected after-reading ends below the warning level, or the Product Owner permitted it |
| Or-15.d | When no split of a story ends below the warning level, or no estimate can be made, applies Or-10.e (no estimate is a reason to ask) and sets an alarm for the window's reset time (Or-10.b) | The start of a sprint | review: no job projected at or above the warning level, or without an estimate, started without a Product Owner message permitting it |
| Or-16 | Splits, spills over to the next sprint, or stops a story that misses done | ^ | review: each story that missed done is recorded in `sprint.md` as split, spilled over or stopped |
| Or-20 | Asks the Product Owner whether to start a sprint, at the start of a project and at the end of each Retrospective; never launches one, since the Product Owner's message is the only start of a sprint | The start of a project; the end of each Retrospective | review: each sprint was started by a Product Owner message that follows the Orchestrator's question |
| Or-22 | Never accepts a story; the Product Owner accepts or rejects each story at the Review | Review | review: no story is `done` without a Product Owner accept in `sprint.md` |
| Or-23 | Launches more than one team in a sprint only when the Product Owner directs it (one team by default), each on its own stories | Sprint | review: one team per story unless a Product Owner message directs more |
| Or-24 | Runs a sprint once the Product Owner launches it (Or-20), in this order: Pre-flight (Or-04), checks each story (Or-09), estimates and records the start usage (Or-15), plans from the Product Owner's priority (Or-25), launches each story's team (Or-08, Or-23), then the Review (Or-13) and the Retrospective (Or-14). The gate before any launch is Or-24.c | The Product Owner launches a sprint | review: the record shows Or-24.a to Or-24.c in the order of the row |
| Or-24.a | Writes `SCRUM.d/sprint.md`: the story IDs (a story that fixes an issue names it as `#N`) and the usage estimate | When the sprint is launched | review: `sprint.md` holds the story IDs and the estimate at the launch |
| Or-24.b | Sets the status of each requirement of a story to `planned` | When the sprint is launched | review: every requirement of a launched story is `planned` |
| Or-24.c | The gate: a launch message from the Product Owner does not agree to rows. No agent is launched until every story's check (Or-09) is written in `SCRUM.d/sprint.md` as passed, naming each requirement and its status, and the start usage readings the Product Owner gave when asked, and the estimate (Or-15), are written there too | Before the first launch of the sprint | review: `sprint.md` holds the passed Or-09 check naming each requirement and its status, the readings and the estimate, all dated before the first agent launch |
| Or-24.d | Creates one branch for the sprint from `main` when the sprint is launched; the sprint's work is pushed only to it and it merges to `main` after the Retrospective, when the Product Owner directs it | When the sprint is launched | review: `git log main` holds no commit from the sprint branch before the Retrospective is done and the Product Owner has directed the merge |
| Or-25 | Never sets or changes the priority of the backlog; plans a sprint from the Product Owner's priority | Planning a sprint | review: the stories of a sprint follow the Product Owner's priority |
| Or-26 | Turns a deliverable the Product Owner states into `proposed` rows in the right feature file, by launching a slice agent when it is large (Or-01); each row traces to the Product Owner's statement | Refinement | review: every new row traces to a Product Owner statement |
| Or-26.a | A value the Product Owner's statement does not give (a number, a name, a test) is written as a `(?)` row and asked in the conversation, never chosen. When the Product Owner asks "Questions?", asks them all before writing a row | Refinement | review: no new row holds a value that the Product Owner's statement or an answer in `SCRUM.d/defects.md` does not give |
| Or-27 | Asks the Product Owner only what the first Standing rule of `AGENTS.md` says is the Product Owner's to decide, and acts without asking on everything its rows assign | Always | review: every question to the Product Owner is a decision of theirs, and no action waited for a permission a row already gave (`AGENTS.md`, Standing rules) |

### Coder (build)

| ID | What | When acted | How tested |
|---|---|---|---|
| Cb-01 | Works in the smallest testable step, verifies, then commits | ^ | review: the commits are small and each leaves its tests passing |
| Cb-02 | Touches only the files the story needs | ^ | `git diff --stat` shows only files the story needs |
| Cb-03 | Does not weaken or delete a test to make it pass | ^ | review: the diff deletes or weakens no assertion |
| Cb-04 | Reviews its own diff for redundancy and a simpler way before reporting | Before reporting | review: the report names what the self-review found |
| Cb-05 | When a requirement is unclear it proposes alternatives with pros and cons and sends the defect to the Orchestrator | A requirement is unclear | review: each unclear requirement has a report with alternatives and their pros and cons |
| Cb-06 | Builds as `packages/README.md` says | ^ | review: the diff follows Cb-11 to Cb-19 of `packages/README.md` |
| Cb-07 | Searches the docs for the behaviors of the story's requirement IDs and reports each doc that needs a change, in the same step as the code; the Orchestrator edits them (Or-07.g), since the rule files are not the team's to edit (Team-02) | With the code | review: the report names every doc that mentions the story's behaviors |
| Cb-08 | Adds no dependency without the Product Owner's approval (the approved list is in `packages/README.md`) | Adding a dependency | review: the diff adds no entry to a `pubspec.yaml` that the Product Owner has not approved |

### Coder (tests)

| ID | What | When acted | How tested |
|---|---|---|---|
| Ct-01 | Works from the requirements only, never the implementation, in `test/` (the Dart package layout) | ^ | review: the test diff touches no implementation file and cites only requirements |
| 🟡 Ct-02 | Writes, for each requirement, the test that matches it, by the cheapest method, in agent usage and in time, that can still fail (the rule in `tests/README.md`; a script is run by the Tester, or by CI when a workflow in `.github/workflows/` runs it) | ^ | review: for each test, name a cheaper method and show it would not verify the row (`tests/README.md`) |
| Ct-02.a | Uses an existing test when that is the cheaper way (`tests/README.md`, "Share before you write") | ^ | review: for each new test, name the existing test it could have extended and show that extending it would have cost more |
| Ct-03 | Writes the test that the test cell of each requirement of the story names, and the test for any clause reported uncovered (Or-03.a) | Sprint | review: every test cell of the story names a test file that exists |
| 🟡 Ct-04 | Writes `test/smoke.md` as `tests/README.md` (Layout) defines it | The file is missing at the Review (Or-13.b) | the file exists and each step names requirement IDs (`tests/README.md`, Layout) |

### Tester

| ID | What | When acted | How tested |
|---|---|---|---|
| Te-01 | Runs the tests Ct wrote and produces one result per requirement, in the format of `tests/README.md` (Results) | ^ | review: the report has one result per requirement ID |
| Te-02 | Runs each test the way its test cell says it runs (a script, CI, or a written procedure); the method was chosen by the Coder (tests) (Ct-02), not by the Tester | ^ | review: each result names the test, how it was run, what it checked and each uncovered clause; a `fail` says whether the test or the code is wrong |
| Te-03 | Writes only its results to its output file; does not change code or tests | ^ | `git diff` of the sprint branch shows no change by the Tester to code or tests |

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
| Team-03 | A defect in a requirement (or a flaw in a rule file) goes to the Orchestrator (Or-02.e.b) | ^ | review: each reported defect reached the Orchestrator and Or-02.e.b ran |
| 🟡 Team-03.a | The reporting agent reports each name or value it needed and the row does not give, skips the part of its work that needs it, and continues with the rest | An agent needs a name or value the row does not give | review: the report lists each such name or value, and none appears in the agent's diff |
| Team-04 | Work on the sprint's branch in the team's one worktree and push only that branch | ^ | `git log main` holds no commit by a team member that the Product Owner did not direct to merge |
| Team-05 | Commit your own work to the sprint's branch after each unit of work, before reporting, and when the Orchestrator says stop, with the requirement IDs in the commit message (`AGENTS.md`) | ^ | review: the sprint branch has a commit by each team member that names requirement IDs |
| Team-06 | Report to the Orchestrator: what you did, the files you read (Team-01), any defect (Team-03), any doc that needs a change (Cb-07), and the skills you loaded (Or-05) | ^ | review: each report holds those five |

### Not yet placed (existing statements I could not give a row)

- Old Or-07.d "Runs `req_check.sh`" (a Post-flight step): moved into Or-13.e, so it runs once per story at the Definition of done and not after every agent.
- Removed at the Product Owner's decision as redundant and costly: the definition **Ready** ("a story is Ready when its requirements pass the review in `requirements/README.md` ("Simulate three jobs"), no open question blocks it, every row of it has status `backlog`, and no test cell of a row of it without sub-requirements is `—`"); Or-09 now lists the three conditions it checks.
- Old Or-01: "Subagents only for: filling a slice, a full review, the port, a story's team, the Reviewer (Rv-01). Short work (edits, fixes, discussion) is done by the Orchestrator itself" (rewritten as Or-01 and its sub-rules; "a full review" is the Reviewer, Or-01.a).
- Removed Or-09.b at the Product Owner's decision (Or-15.c's usage fit is the single size limit): "Small enough for one Reviewer run (about 1,000 changed lines); a larger story is split before it starts." **Test:** `git diff --stat` at post-flight; a story over that size was not split.
- "The Dashboard records the sprint in `SCRUM.d/sprint.md` and each requirement's status." (The Dashboard is not a role.)
- Old Team-04 wording, replaced by one sprint branch (the article "Branching Strategy on Scrum Software Development" uses a branch per sprint): "Work on your own branch in your own worktree and push only that branch".
- Removed from the Tester definition: "(CI for scripted tests, an agent for the rest)"; CI is a tool, and Ct chooses the method.
- Removed Te-04: "`flutter analyze` is clean and `flutter test` passes, run by CI once it exists". CI is a method defined in `tests/README.md`; what it runs is the open item "Decide Dart CI and release" in `WORKING.d/README.md`.
- Removed Te-03: "A Tester agent produces the result for tests that need an agent and adds the CI run for the commit to its report, so the Orchestrator reads one combined result" (Te-01 and Te-02 already give one result per requirement however a test ran).
- Old wording of the Reviewer, removed because the Product Owner corrected that the Reviewer is outside code development: "Runs once per story, cold, after the Tester reports `pass`" (Rv-01), "the Reviewer after the Tester reports `pass` (Rv-01)" (Or-08.a), and "the Reviewer reports no finding against a rule or a requirement" (Definition of done).
- `req_check.sh` patterns match a row as `^\| ID`, so a row marked 🟡 or 🟠 in its first cell is skipped until the patterns allow an optional marker before the ID; a check that lists every mark left is also still to be written.
- Retrospective timing ("after the Review") is not stated in the original file; to confirm.
- Removed from definitions because rules and the status list in `requirements/README.md` already say them: "A requirement in a story has status `planned`, and `done` once its story is accepted at the Review" (Or-24.b, Or-13.e) and "done when their tests pass" (Definition of done).
- "A story that misses done is split, spilled over to the next sprint or stopped by the Orchestrator" is Or-16; its **Test** line is below.
- **Test** of the Definition of done: the Tester's report per requirement and the Reviewer's report, which names any doc the diff makes out of date, are recorded in `sprint.md`; `req_check.sh` reports a dead link or missing picture in the project `README.md`. (Who records is not stated.)
- "Never builds the app and never plays the Coder" (Orchestrator). Possibly redundant with the Coder definition.
- "also the **Author** of short work" (Orchestrator). Replaced by Or-01; term removed.
