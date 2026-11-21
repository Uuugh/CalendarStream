# Task for ChatGPT (self-contained: nothing outside this message is needed)

Rewrite the file under "FILE TO REWRITE" below as three sections: Intro, Definitions, Rules, plus a final section "Not yet placed". Write your answer to the file `WORKING.d/tests-readme.gpt2.md` in the connected workspace (repository Uuugh/CalendarStream): the rewritten file as markdown, then, under the heading "Choices", a list of at most 150 words naming every choice you had to make that these instructions did not settle. Write only that one file, and do not edit any other file or open a pull request. Do not add commentary.

## The three Laws every rule must obey
1. No duplication: say it once; a rule is written in one place and referenced everywhere else.
2. No exceptions: a rule holds for every case; a different case gets its own rule. Do not write "except", "unless", "never for" or "only when X is not".
3. Every rule has a method (who does it and how) and a test (a script check, or a review step that names what the reviewer looks for).

## Format
- A rule is one table row: `| ID | What | When acted | How tested |`. The ID prefix is the role code that acts. A sub-rule is ID.a, ID.b, and a sub-sub-rule ID.a.1 or ID.b.c; it inherits from its parent.
- A blank cell is missing. `—` means none, stated. `^` means the parent's value (on a top-level row, the default: the review described in "How tested" of the file).
- "When acted" names an event or an observable condition.
- Role codes: Or = Orchestrator, Cb = Coder (build), Ct = Coder (tests), Te = Tester, Rv = Reviewer (outside code development; tests the process files). Use only these codes.

## Method (the steps to follow, in order)
1. Before writing, read the whole file below, the existing rows in "Existing rows that overlap" below, and the "Citations" below. A cited heading is kept or its citation is noted.
2. Put every sentence of the original in Definitions, in a row or in "Not yet placed" with the reason; cut nothing. A word you add to What comes from the original; a word you add to When acted or How tested is marked 🟡 and "(proposed)". Define a term once, in Definitions; rules only use it; flag any term or code you must choose.
3. Sort each sentence: a definition goes to Definitions (a sentence that is both a definition and a rule is split); a rule whose paragraph names an actor is a row for that actor, and the ID prefix is that actor; a rule with no actor in its paragraph goes to "Not yet placed" 🟠 and you never guess the actor; a rule that repeats an existing row goes to "Not yet placed" 🔴; a "Test:" tail goes to How tested, the rest to What. A flow is one parent rule whose sub-rules are the steps in order.
4. Continue the existing IDs of the role; do not use an ID listed as removed (below).
5. For each rule ask what happens with an empty set, a tie and mixed results; write each case the original does not answer in "Not yet placed" as a 🟡 question, never as a new rule.
6. Before answering, scan for exception words (Law 2), compare with the existing rows (Law 1), and mark only what you added or could not place. Each rule must let an agent that has never seen the project decide yes or no without judgment.


## Marks (put them in the first cell of a row, or at the start of a list item)
- 🟡 a question or a choice you had to make.
- 🟠 a line an agent cannot act on (unclear, wrong, or missing information).
- 🔴 a line that breaks a Law or duplicates another line.

## Context you may use
- The file below belongs to a project where requirements are rows with an ID, a status (proposed, backlog, planned, done, defect), a statement and a test cell. A requirement's test cell names its tests. The roles are: the Coder (tests) writes tests from the requirements only; the Tester runs them and reports one result per requirement ID; the Orchestrator coordinates and routes results.
- The IDs for the rules you write continue the existing Ct (Coder (tests)) and Te (Tester) numbering at Ct-05 and Te-05 (Te-04 is a removed ID); mark that choice 🟡.

## Existing rows that overlap (Or = Orchestrator; these exist in another file and are not yours to rewrite)
- Ct-01: Works from the requirements only, never the implementation, in `test/` (the Dart package layout).
- Ct-02: Writes, for each requirement, the test that matches it, by the cheapest method, in agent usage and in time, that can still fail (the rule in `tests/README.md`).
- Ct-02.a: Uses an existing test when that is the cheaper way (`tests/README.md`, "Share before you write").
- Ct-03: Writes the test that the test cell of each requirement of the story names, and the test for any behavior reported uncovered.
- Ct-04: Writes `test/smoke.md` as `tests/README.md` (Layout) defines it; acted when the file is missing at the Review.
- Te-01: Runs the tests Ct wrote and produces one result per requirement, in the format of `tests/README.md` (Results).
- Te-02: Runs each test the way its test cell says it runs; the method was chosen by the Coder (tests), not by the Tester.
- Te-03: Writes only its results to its output file; does not change code or tests.
- `AGENTS.md`, Standing rules: "Never put real data or secrets anywhere (the real schedule, username, Google secret)."

## Citations
Other files cite these headings of the file below: "Share before you write", "Results", "Layout". Removed ID: Te-04.

## FILE TO REWRITE
# tests: how requirements are tested

A test verifies one or more requirements. Its test cell in the requirement row names it (what a test cell means is
defined in `requirements/README.md`). Who writes and who runs tests is defined in `SCRUM.d/README.md`.

## Definitions

- 🟡 **Behavior**: one thing a requirement's statement says must hold.
- 🟡 **Uncovered**: a behavior that no test the row lists checks.
- **CI** (continuous integration): the GitHub workflow that runs our scripted checks on every push; it costs no agent usage.
- 🟡 **Result**: one of four words for a requirement ID in a run: `pass` (every listed test passed and no behavior is uncovered), `fail` (a listed test failed; the result gives the ID, what was expected and what was found), `not run` (a test could not start or crashed before its checks, or the row has status `defect`) or `uncovered` (a behavior of the row is uncovered).

## The rule

**A requirement is tested by the cheapest method, in agent usage and in time, that still verifies it.** No method is
required and none is banned. Pick the cheapest one that can fail when the requirement is not met. A test that CI can run
costs no agent usage, so it is cheaper than the same test an agent must run: methods 1 to 4 are scripts CI can run,
methods 5 and 6 need an agent. **Test:** review: for each test, name a cheaper method and show it would not verify the
row; for each test an agent runs, show that CI cannot run it.

## Methods, cheapest first (a guide, not a limit)

1. A static check or script on files (`tests/tools/req_check.sh` is one).
2. A unit test of pure logic, with a clock the test controls and made-up data.
3. An API test against a running server and a throwaway database.
4. A comparison with stored expected output (made-up fixtures, or screenshots).
5. A browser run by an agent, for layout and behavior nothing cheaper can check.
6. A written procedure an agent follows, for a row no script can decide.

Expected outputs of the old app are captured once as made-up fixtures and compared by script (method 4), not by
running the old app each time.

## Share before you write

Before writing a new test, look for an existing test to share or modify, and do so when that is the cheaper way to
verify the requirement; one test may verify several requirements. **Test:** review: for each new test, name the existing
test it could have extended and show that extending it would have cost more.

## Creating and merging tests

The Coder (tests) creates a test from the requirement alone, from its observable success and failure, and names it by the
behavior and the requirement ID. Shared helpers live in one place, and a test mocks external systems, not internal logic. Two tests
that verify the same row are merged into one. A test whose requirement is deleted is deleted. **Test:** review: for each
test, name the requirement it verifies, and for each pair, show they verify different rows.

An issue gets a failing test first; the fix follows. **Test:** review: the commit that fixes an issue follows the commit of
its failing test.

🟡 The tests a row with no sub-requirements lists together check every behavior of its statement; a row with sub-requirements is checked through them (Parent tests, `requirements/README.md`). **Test:** the Tester's result for the row names each uncovered behavior (Te-02).

A test declares whether one run covers all its requirement IDs or runs once per ID. A requirement that depends on time is
tested with a clock the test controls; no test waits real time. **Test:** review: for each test, name its declaration; for
each time-dependent requirement, show the controlled clock.

## Results

🟡 Each run reports one result per requirement ID, with the command run, by this precedence: `fail`, then `not run`, then `uncovered`, then `pass` (Definitions). Any result names each uncovered behavior. A row with sub-requirements takes the first of these four words, in that order, that its own tests or its sub-requirements have, and names the sub-requirement that has it. **Test:** review: each result in a report is one of those four words, names the command, and names each uncovered behavior.

## Layout

Tests sit in `test/<feature>/`, mirroring `requirements/<feature>.md`, in the Dart package layout
(https://dart.dev/tools/pub/package-layout); thin end-to-end tests sit in `integration_test/`. Fakes and made-up data are never real data
(`AGENTS.md`). How runs are split and what a run reports to the dashboard is the first open story in `WORKING.d/README.md`.

🟡 `test/smoke.md`, in the project's `test/` folder, is the smoke procedure: a written procedure an agent follows at each Review, derived from the requirements; each step names the requirement IDs it exercises and is reported `pass`, `fail` or `not run`. **Test:** review: each step names requirement IDs, and the Tester's smoke report follows the file.

Made-up data lives in `tests/data/`, one dataset per kind, shared by all tests (`Demo.ics` is a made-up schedule, `work.ics` a
second made-up calendar). **Test:** review: a test that carries its own copy of data names the shared dataset it could have used.
