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
