# tests: how requirements are tested

## Intro

A test verifies one or more requirements. Its test cell in the requirement row names it (what a test cell means is
defined in `requirements/README.md`). Who writes and who runs tests is defined in `SCRUM.d/README.md`.

A rule is one row: `ID | What | When acted | How tested`, read as in `SCRUM.d/README.md` (Intro). The ID prefix is the role that acts.
🟡 The IDs in this file (Ct-11 on, Te-11 on) and every cell marked "(proposed)" are chosen by the Orchestrator; the codes Ct and Te are the Product Owner's.

## Definitions

- 🟡 **Behavior**: one thing a requirement's statement says must hold.
- 🟡 **Uncovered**: a behavior that no test the row lists checks.
- **CI** (continuous integration): the GitHub workflow that runs our scripted checks on every push; it costs no agent usage.
- 🟡 **Result**: one of four words for a requirement ID in a run: `pass` (every listed test passed and no behavior is uncovered), `fail` (a listed test failed; the result gives the ID, what was expected and what was found), `not run` (a test could not start or crashed before its checks, or the row has status `defect`) or `uncovered` (a behavior of the row is uncovered).
- 🟡 **Precedence of results**: `fail`, then `not run`, then `uncovered`, then `pass`.
- **Test**: verifies one or more requirements; one test may verify several requirements.
- **Test cell**: the cell of a requirement row that names its test (meaning in `requirements/README.md`).
- **Cost of a test**: agent usage and time. A test that CI can run costs no agent usage, so it is cheaper than the same test an agent must run.
- **Methods, cheapest first** (a guide, not a limit; no method is required and none is banned):
  1. A static check or script on files (`tests/tools/req_check.sh` is one).
  2. A unit test of pure logic, with a clock the test controls and made-up data.
  3. An API test against a running server and a throwaway database.
  4. A comparison with stored expected output (made-up fixtures, or screenshots).
  5. A browser run by an agent, for layout and behavior nothing cheaper can check.
  6. A written procedure an agent follows, for a row no script can decide.
- Methods 1 to 4 are scripts CI can run; methods 5 and 6 need an agent.
- **Shared helpers** live in one place.
- **Layout**: tests sit in `test/<feature>/`, mirroring `requirements/<feature>.md`, in the Dart package layout (https://dart.dev/tools/pub/package-layout); thin end-to-end tests sit in `integration_test/`.
- 🟡 **Smoke procedure** (`test/smoke.md`, in the project's `test/` folder): a written procedure an agent follows at each Review, derived from the requirements.
- **Made-up data** lives in `tests/data/`, one dataset per kind, shared by all tests (`Demo.ics` is a made-up schedule, `work.ics` a second made-up calendar).

## Rules

### Coder (tests)

| ID | What | When acted | How tested |
|---|---|---|---|
| 🟠🟡 Ct-11 | Tests a requirement by the cheapest method, in agent usage and in time, that still verifies it: picks the cheapest one that can fail when the requirement is not met (methods 1 to 4 before 5 and 6, Definitions). Same rule as Ct-02 in `SCRUM.d/README.md` | Writing a test | review: for each test, name a cheaper method and show it would not verify the row; for each test an agent runs, show that CI cannot run it |
| 🟡 Ct-11.a | Captures the expected outputs of the old app once as made-up fixtures and compares by script (method 4), not by running the old app each time | Writing a test whose expected output comes from the old app | (proposed) review: no test runs the old app |
| 🟡 Ct-12 | Before writing a new test, looks for an existing test to share or modify, and does so when that is the cheaper way to verify the requirement | Before writing a new test | review: for each new test, name the existing test it could have extended and show that extending it would have cost more |
| 🟡 Ct-13 | Creates a test from the requirement alone, from its observable success and failure | Creating a test | review: for each test, name the requirement it verifies |
| 🟡 Ct-13.a | Names a test by the behavior and the requirement ID | Creating a test | ^ |
| 🟡 Ct-13.b | Mocks external systems, not internal logic | Creating a test | (proposed) review: no test mocks internal logic |
| 🟡 Ct-13.c | Merges two tests that verify the same row into one | Two tests verify the same row | review: and for each pair, show they verify different rows |
| 🟡 Ct-13.d | Deletes a test whose requirement is deleted | A requirement is deleted | (proposed) review: no test names a requirement that is not in `requirements/` |
| 🟡 Ct-14 | Writes the failing test of an issue first; the fix (Cb) follows | An issue is open | review: the commit that fixes an issue follows the commit of its failing test |
| 🟡 Ct-15 | Lists, for a row with no sub-requirements, tests that together check every behavior of its statement; a row with sub-requirements is checked through them (Parent tests, `requirements/README.md`) | Writing the tests of a row | the Tester's result for the row names each uncovered behavior (Te-02) |
| 🟡 Ct-16 | A test declares whether one run covers all its requirement IDs or runs once per ID | Writing a test | review: for each test, name its declaration |
| 🟡 Ct-16.a | A requirement that depends on time is tested with a clock the test controls; no test waits real time | Writing a test of a time-dependent requirement | review: for each time-dependent requirement, show the controlled clock |
| 🟡 Ct-17 | Puts tests in the Layout (Definitions) | Creating a test | (proposed) review: each test file sits in `test/<feature>/` or `integration_test/` |
| 🟡 Ct-17.a | Fakes and made-up data are never real data (`AGENTS.md`) | ^ | (proposed) review: the diff holds no real data (`AGENTS.md`) |
| 🟡 Ct-18 | Writes each step of the smoke procedure with the requirement IDs it exercises | Writing the smoke procedure | review: each step names requirement IDs |
| 🟡 Ct-19 | Uses the shared dataset in `tests/data/` and carries no copy of its own | Writing a test that needs data | review: a test that carries its own copy of data names the shared dataset it could have used |

### Tester

| ID | What | When acted | How tested |
|---|---|---|---|
| 🟡 Te-11 | Each run reports one result per requirement ID, with the command run, by the precedence of results (Definitions) | A run | review: each result in a report is one of those four words, names the command, and names each uncovered behavior |
| 🟡 Te-11.a | Any result names each uncovered behavior | A run | ^ |
| 🟡 Te-11.b | A row with sub-requirements takes the first of the four result words, in precedence order, that its own tests or its sub-requirements have, and names the sub-requirement that has it | A run | ^ |
| 🟡 Te-12 | Reports each step of the smoke procedure `pass`, `fail` or `not run` | A Review | review: the Tester's smoke report follows the file |

## Not yet placed

- 🟡 "How runs are split and what a run reports to the dashboard is the first open story in `WORKING.d/README.md`." No actor, not a definition: a pointer to an open item. Where it belongs is for the Product Owner.
- 🔴 Ct-11 repeats Ct-02 and Ct-02.a (and Te-11 repeats Te-01) in `SCRUM.d/README.md` (Law 1). This file owns them (`AGENTS.md`, folders); `SCRUM.d/README.md` should only link. Not edited here.
- 🟠 "the cheapest method" (Ct-11) is a judgment; its test cell makes it checkable only by a reviewer.
- 🟡 The actor of the unattributed sentences (Ct-13.c, Ct-13.d, Ct-14, Ct-17.a, the Fixtures rule Ct-11.a) is chosen as the Coder (tests); Ct-14's fix is by the Coder (build). The original names no actor.
- 🟡 The original "Test:" tail on the "Creating and merging tests" paragraph was split across Ct-13, Ct-13.c; the one on "A test declares..." across Ct-16, Ct-16.a; the smoke tail across Ct-18, Te-12; the Results tail across Te-11 to Te-11.b. Words kept; the joining "and" sits at the start of Ct-13.c's cell.
- 🟡 Heading names ("The rule", "Methods", "Share before you write", "Creating and merging tests", "Results", "Layout") are replaced by Definitions and role tables; the old section names are gone.
