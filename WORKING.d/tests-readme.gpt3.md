# tests: how requirements are tested

## Definitions

- **Test.** A test verifies one or more requirements. The [test cell](../requirements/README.md#definitions) in the requirement row names it. [SCRUM.d/README.md](../SCRUM.d/README.md) defines who writes and who runs tests and when.
- **Behavior.** One thing a requirement's statement says must hold.
- **Uncovered.** A behavior that no test the row lists checks.
- **CI** (continuous integration). The GitHub workflow that runs our scripted checks on every push. It costs no agent usage.
- **Result.** One of four words for a requirement ID in a run.
  - `pass` — every listed test passed and no behavior is uncovered.
  - `fail` — a listed test failed. The result gives the ID, what was expected and what was found.
  - `not run` — a test could not start or crashed before its checks, or the row has status `defect`.
  - `uncovered` — a behavior of the row is uncovered.

### Methods, cheapest first (a guide, not a limit)

No method is required and none is banned. Methods 1 to 4 are scripts CI can run. Methods 5 and 6 need an agent. A test that CI can run is cheaper than the same test an agent must run.

1. A static check or script on files (`tests/tools/req_check.sh` is one).
2. A unit test of pure logic, with a clock the test controls and made-up data.
3. An API test against a running server and a throwaway database.
4. A comparison with stored expected output (made-up fixtures, or screenshots).
5. A browser run by an agent, for layout and behavior nothing cheaper can check.
6. A written procedure an agent follows, for a row no script can decide.

### Layout

- Tests sit in `test/<feature>/`, mirroring `requirements/<feature>.md`, in the [Dart package layout](https://dart.dev/tools/pub/package-layout). Thin end-to-end tests sit in `integration_test/`.
- **Smoke procedure.** `test/smoke.md`, in the project's `test/` folder, is a written procedure derived from the requirements. Each step names the requirement IDs it exercises. Its report gives each step `pass`, `fail` or `not run`.
- **Made-up data.** The datasets live in `tests/data/`. `Demo.ics` is a made-up schedule and `work.ics` a second made-up calendar.

## Rules

Read the role prefixes and `^` as defined in [SCRUM.d/README.md](../SCRUM.d/README.md#intro).

### The rule

| ID | What | When acted | How tested |
| --- | --- | --- | --- |
| Ct-05 | Pick the cheapest method, in agent usage and in time, that verifies the requirement and can fail when the requirement is unmet. | ^ | Review: for each test, name a cheaper method and show it would not verify the row. For each test an agent runs, show that CI cannot run it. |

### Share before you write

| ID | What | When acted | How tested |
| --- | --- | --- | --- |
| Ct-06 | Look for an existing test to share or modify, and do so when that is the cheaper way to verify the requirement. | Before writing a new test. | Review: for each new test, name the existing test it could have extended and show that extending it would have cost more. |

### Creating and merging tests

| ID | What | When acted | How tested |
| --- | --- | --- | --- |
| Ct-07 | Create a test from the requirement alone, from its observable success and failure, and name it by the behavior and the requirement ID. | 🟡 (proposed) When creating a test. | Review: for each test, name the requirement it verifies. 🟡 (proposed) Match its checks and name to the observable behavior and ID in that requirement. |
| Ct-08 | Shared helpers live in one place. | ^ | 🟡 (proposed) Review: trace each shared helper's callers to one definition. |
| Ct-09 | A test mocks external systems and exercises its internal logic. | ^ | 🟡 (proposed) Review: inspect the test doubles and check that each stands in for an external system, and inspect any calls to external systems for mocks. |
| Ct-10 | Two tests that verify the same row are merged into one. | Two tests verify the same row. | Review: for each pair, show they verify different rows. |
| Ct-11 | A test whose requirement is deleted is deleted. | A requirement is deleted. | 🟡 (proposed) Review: match tests in the deleted requirement's test cell to test deletions in the diff. |

### Results

| ID | What | When acted | How tested |
| --- | --- | --- | --- |
| Te-05 | Each run reports one result per requirement ID, with the command run, by this precedence: `fail`, then `not run`, then `uncovered`, then `pass`. Any result names each uncovered behavior. | 🟡 (proposed) When reporting a run. | Review: each result in a report is one of those four words, names the command, and names each uncovered behavior. 🟡 (proposed) Check that each requirement ID appears once and its word is the first applicable one in the stated order. |
| Te-06 | A row with sub-requirements takes the first of the four words, in the order in Te-05, that its own tests or its sub-requirements have, and names the sub-requirement that has it. | A row with sub-requirements. | 🟡 (proposed) Review: compare the reported word with the words for the row's own tests and its sub-requirements, and match the named sub-requirement to that word. |
| Te-07 | The Tester's smoke report follows the file defined in Layout. | At each Review. | Review: each step names requirement IDs, and the Tester's smoke report follows the file. 🟡 (proposed) Match the reported steps and their words to Layout. |

## Not yet placed

- 🟠 **Old-app output.** Expected outputs of the old app are captured once as made-up fixtures and compared by script (method 4). Capture is the old-app run for those expected outputs. No actor or test is stated.
- 🟠 **Failing test before a fix.** An issue gets a failing test first. The fix follows. Review: the commit that fixes an issue follows the commit of its failing test. No actor is stated.
- 🟠 **Behavior coverage.** The tests a row with no sub-requirements lists together check every behavior of its statement. A row with sub-requirements is checked through them ([Parent tests](../requirements/README.md#definitions)). The Tester's result for the row names each uncovered behavior (Te-02). The Tester supplies the coverage evidence. No actor is stated for making the tests cover every behavior. Rule 11.a of the requirements README owns the parent pass condition.
- 🟠 **Run declaration.** A test declares whether one run covers all its requirement IDs or runs once per ID. Review: for each test, name its declaration. No actor is stated in the paragraph. Compare the Test cell definition in the requirements README.
- 🟠 **Time.** A requirement that depends on time is tested with a clock the test controls. Tests use the controlled clock in place of real-time waits. Review: for each time-dependent requirement, show the controlled clock. No actor is stated in the paragraph.
- 🔴 **Made-up data.** The source restriction on real data in fakes and made-up data repeats [AGENTS.md](../AGENTS.md#standing-rules), which owns the standing rule. This reference carries the restriction.
- 🟠 **Run splitting and dashboard report.** How runs are split and what a run reports to the dashboard is the first open story in [WORKING.d/README.md](README.md). The source gives a pointer.
- 🟠 **Made-up data sharing.** One dataset per kind is shared by all tests. Review: a test that carries its own copy of data names the shared dataset it could have used. No actor is stated for sharing, and dataset kind is undefined.

### Questions from the source rules

- 🟡 **Ct-05.** What does the review record when no method verifies the row or no cheaper method exists, which method wins a cost tie, and how are lower time and lower agent usage compared when they favor different methods?
- 🟡 **Ct-06.** What does the review record when no existing test can be extended, extending and writing cost the same, or different existing tests cover different parts?
- 🟡 **Old-app output.** What is compared when there is no capture, several captures qualify equally, or captured outputs disagree?
- 🟡 **Ct-08.** What does the review record when there are no shared helpers, which copy is retained when two definitions match, and what happens when helpers share only some logic?
- 🟡 **Ct-10.** What does the review record with no pairs, which test is retained when both qualify equally, and what happens when two tests share a row and also verify different rows?
- 🟡 **Ct-11.** What is deleted when the test cell names no tests, two references name the same test, or a test also verifies a retained row?
- 🟡 **Failing test before a fix.** How does review handle no failing-test commit, the failing test and fix in the same commit, or several tests whose results differ before the fix?
- 🟡 **Behavior coverage.** What happens when no tests are listed, multiple tests check the same behavior, or the tests cover some behaviors and leave others uncovered?
- 🟡 **Run declaration.** What declaration applies with zero IDs, when either run arrangement works, or when one run covers some IDs and separate runs are needed for the rest?
- 🟡 **Te-05.** What word is reported when there are no listed tests or uncovered behaviors, and which command and failure details are recorded when several tests have the same highest-priority word? Te-05 supplies the precedence for different words.
- 🟡 **Te-06.** What is reported when the row and its sub-requirements have no result words, which sub-requirement is named when several have the highest-priority word, and what is named when the row's own tests alone have that word?
- 🟡 **Smoke procedure.** What is reported when there are no steps, when steps exercise identical IDs, or when one step exercises several IDs with different outcomes?
- 🟡 **Made-up data sharing.** What happens when there is no shared dataset of the kind, multiple datasets match equally, or the shared dataset supplies only some of the needed data?

### Ownership and citations

The Product Owner assigned the method and report rules to `tests/README.md`. The existing Scrum rows supply the roles and events. Ct-01 overlaps Ct-07 and Layout. Ct-02 points to The rule and overlaps Ct-05. Ct-02.a cites Share before you write and overlaps Ct-06. Ct-03 assigns work named by the requirement's test cell and reported uncovered behaviors. Ct-04 and Or-13.b cite Layout for the smoke procedure. Te-01 cites Results and overlaps Te-05. Te-02 overlaps the reporting evidence in Results and the uncovered-behavior check. Te-03 governs the Tester's output file. Or-03 and Or-03.b check and route reported results. Those source rows remain in place for this draft. Te-04 is recorded as removed.

Rv-02.b, the Scrum note for removed Te-04, `AGENTS.md`, `packages/README.md` and `tests/tools/req_check.sh` reference the README as a file. The historical notes and rewrites in `WORKING.d` refer to the original rules and headings. The cited headings are retained.

## Choices

- Used Ct-05 through Ct-11 and Te-05 through Te-07. Used Ct-02, Ct-02.a, Te-01 and Or-13.b with Ct-04 as explicit actor evidence for their cited sections.
- Read the lessons on README rewrites and result reporting. No lesson is keyed to the affected Ct or Te IDs.
- Treated method descriptions, Dart locations and smoke step format as definitions. Kept smoke execution and missing-file routing with Scrum.
- Preserved the parent result precedence while leaving the parent pass condition with requirements rule 11.a.
- Kept proposed checks and unresolved edge cases visible. Existing source marks are represented by the corresponding questions and placement notes in this draft.
- Read internal logic as the logic under test. Split the dataset directory from the unassigned sharing rule.
