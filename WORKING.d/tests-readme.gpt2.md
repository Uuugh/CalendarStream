# tests: how requirements are tested

## Intro

The requirement row’s test cell names its tests. See [requirements/README.md](../requirements/README.md) for the meaning of a test cell and [SCRUM.d/README.md](../SCRUM.d/README.md) for who writes and runs tests.

## Definitions

- **Test** — verifies one or more requirements.
- **Behavior** — one thing a requirement’s statement says must hold.
- **Uncovered** — a behavior that no test listed in the row checks.
- **CI** (continuous integration) — the GitHub workflow that runs scripted checks on every push at no agent usage cost.
- **Result** — one of four words for a requirement ID in a run.
  - `pass` — every listed test passed and no behavior is uncovered.
  - `fail` — a listed test failed. The result gives the ID, what was expected and what was found.
  - `not run` — a test could not start or crashed before its checks, or the row has status `defect`.
  - `uncovered` — a behavior of the row is uncovered.
- **Smoke procedure** — the written procedure in `test/smoke.md` in the project’s `test/` folder.
- **How tested** — a named review step in the last column. 🟡 (proposed) For a default review, the Reviewer checks the item named by that column. Here, `^` inherits the parent value, or the default review on a top-level row, and `—` means none stated.

## Rules

The ID prefix names who acts. Ct is the Coder (tests) and Te is the Tester.

### Creating and merging tests

| ID | What | When acted | How tested |
| --- | --- | --- | --- |
| 🟡 Ct-05 | The Coder (tests) creates a test from the requirement’s observable success and failure, and names it by the behavior and the requirement ID. | 🟡 (proposed) When the Coder (tests) creates a test. | Review: for each test, name the requirement it verifies. 🟡 (proposed) Check that the name identifies the behavior and requirement ID and that the test checks the observable success and failure named in the requirement. |
| Ct-06 | Shared helpers live in one place. | 🟡 (proposed) When two or more tests use the same helper. | 🟡 (proposed) Review: for each shared helper, check that its callers use one definition. |
| Ct-07 | A test mocks external systems. | 🟡 (proposed) When a test calls an external system. | 🟡 (proposed) Review: inspect calls to external systems and check that each call uses a mock. |
| Ct-08 | Two tests that verify the same row are merged into one. | Two tests verify the same row. | Review: for each pair, show they verify different rows. |
| Ct-09 | A test whose requirement is deleted is deleted. | A requirement is deleted. | 🟡 (proposed) Review: compare the deleted row’s test cell with the tests removed by the change and check that every named test was removed. |

### Layout

| ID | What | When acted | How tested |
| --- | --- | --- | --- |
| 🟡 Te-05 | The Tester’s smoke report follows the file. | At each Review. | Review: each step names requirement IDs. 🟡 (proposed) Match each report entry to its step and check its reported result against the smoke step format under Layout — remaining material. |

## Not yet placed

### The rule

- 🔴 Use the cheapest method, in agent usage and time, that still verifies the requirement and can fail when the requirement is unmet. Ct-02 already states this rule. Its source review asks the reviewer to name a cheaper method for each test and show that it would fail to verify the row, and to show that CI cannot run each agent-run test.
- 🟠 All methods are eligible. Methods 1–4 are scripts CI can run. Methods 5–6 need an agent. A CI-runnable test costs less than the same test run by an agent because CI costs no agent usage. The paragraph supplies no actor or decision procedure for comparing agent usage with elapsed time.
- 🟡 How is the cheapest method chosen when the candidate set is empty, methods tie, or one saves time and another saves agent usage?

### Methods, cheapest first (a guide, not a limit)

- 🟠 The source gives this ordered guide with no actor or pass/fail criteria for choosing a method.
  1. A static check or script on files, such as `tests/tools/req_check.sh`.
  2. A pure-logic unit test with a controlled clock and made-up data.
  3. An API test against a running server and throwaway database.
  4. Comparison with stored expected output such as made-up fixtures or screenshots.
  5. An agent-run browser check for layout and behavior that cheaper methods cannot check.
  6. An agent-followed written procedure for a row that no script can decide.
- 🟠 Capture the old app’s expected outputs once as made-up fixtures and compare by script using method 4. The old app runs at capture time. The paragraph names no actor or test.
- 🟡 What happens when no old-app output is available, candidate captures tie, or the captured outputs disagree?

### Share before you write

- 🔴 Before writing a new test, look for an existing one to share or modify and use it when that is cheaper. Ct-02.a states the reuse rule. The source review asks, for each new test, which existing test it could have extended and what makes extension cost more. This heading is cited by Ct-02.a.
- 🟡 What does the review record when there is no candidate to extend, extension and a new test cost the same, or an existing test covers only part of the requirement?

### Creating and merging tests

- 🔴 The Coder (tests) works from the requirement alone. Ct-01 already states the input restriction.
- 🟠 The source also excludes mocks of internal logic. Ct-07 preserves the affirmative external-system rule. The source gives no inventory that lets a newcomer classify every dependency as external or internal.
- 🟠 Give an issue a failing test before its fix. Source review: check that the fix commit follows the failing-test commit. The paragraph names no actor.
- 🟠 For a row with no sub-requirements, its listed tests together check every behavior. A row with sub-requirements is checked through them. See “Parent tests” in [requirements/README.md](../requirements/README.md). The source names the Tester as the source of evidence that each uncovered behavior is reported, but names no actor for establishing coverage. Its reference to Te-02 points to the test execution method.
- 🟠 A test declares whether one run covers all its requirement IDs or it runs once per ID. For a time-dependent requirement, use the clock the test controls and avoid real-time waits. Source review: find each test’s declaration and the controlled clock for each time-dependent requirement. The paragraph names no actor.
- 🟡 Ct-05 — What counts as a valid test name or observation when a requirement lists no observable behavior, two tests target the same behavior and ID, or the test covers several behaviors or IDs?
- 🟡 Ct-06 — Does review pass with zero shared helpers, which definition is retained when copies are equivalent, and how are helpers with shared and distinct behavior handled?
- 🟡 Ct-07 — Does review pass when there are no external dependencies, how is a dependency spanning both boundaries classified, and how are tests that mix live calls and mocks classified?
- 🟡 Ct-08 — Does review pass when there are no pairs, which test is the merge base when both qualify, and what happens when a pair shares one row but each also verifies a different row?
- 🟡 Ct-09 — What happens when the deleted row lists no tests, several test names identify the same test, or a listed test also verifies a retained row?
- 🟡 What happens when an issue has no failing-test commit, the test and fix share a commit, or several tests produce mixed results before the fix?
- 🟡 What coverage is required for a row with no listed tests, several tests that each cover the same behavior, or a parent whose tests and sub-requirements cover different behaviors?
- 🟡 What declaration is valid for zero IDs, when either run arrangement works, or when a single run covers some IDs and the remainder need separate runs?

### Results

- 🔴 Each run reports one result per requirement ID. Te-01 states the one-result rule and cites this heading for the format.
- 🟠 Include the command run and every uncovered behavior. Use this precedence: `fail`, `not run`, `uncovered`, `pass`. A row with sub-requirements takes the first word by that order present in its own tests or its sub-requirements and names the sub-requirement that has it. Source review: check the result word, command, and uncovered behaviors for every report entry. The paragraph names no actor, and the source review does not check the precedence or the named sub-requirement.
- 🟡 What is the result with zero tests and zero sub-requirements, which sub-requirement is named when results tie, and what is named when the parent’s own test supplies the highest-priority result and its sub-requirements have lower-priority results?

### Layout — remaining material

- 🟠 Tests go in `test/<feature>/`, mirroring `requirements/<feature>.md`, using the [Dart package layout](https://dart.dev/tools/pub/package-layout). Thin end-to-end tests go in `integration_test/`. The paragraph names no actor and gives no criterion for “thin.”
- 🔴 Fakes and made-up data contain no real data. The standing rule in `AGENTS.md` already covers this.
- 🟠 Run splitting and dashboard reporting are the first open story in [WORKING.d/README.md](README.md). This is a pointer with no prescribed action.
- 🟠 Derive the smoke procedure from the requirements and have an agent follow it at each Review. Each step names the requirement IDs it exercises and is reported as `pass`, `fail` or `not run`. Ct-04 writes the file when missing and cites “Layout.” The paragraph does not assign a role code to the agent following the procedure or specify who maintains the step-to-ID mapping.
- 🟠 One made-up dataset per kind lives in `tests/data/` and is shared by all tests. `Demo.ics` is a made-up schedule and `work.ics` a second made-up calendar. Source review: for a test with its own copy, name the shared dataset it could have used. The paragraph names no actor or criterion for determining dataset kind.
- 🟡 Te-05 — What does a report contain when the procedure has no steps, how are equivalent or repeated steps matched, and what is recorded when a step exercises multiple IDs with mixed outcomes?
- 🟡 What layout applies without a matching feature file, when two feature files match equally, or when a test spans features or combines unit and end-to-end checks?
- 🟡 For test data, what happens when there is no shared dataset, two datasets match equally, or one shared dataset supplies only part of the required data?

## Choices

- 🟡 Started the new rows at Ct-05 and Te-05 and left removed Te-04 unused.
- 🟡 Applied the Coder (tests) actor across its paragraph and used the named Tester for smoke reporting. Kept the Results details unplaced under the paragraph-local actor rule despite Te-01’s citation.
- 🟡 Split smoke procedure identity, reporting, and steps by placement. Kept the cited headings and recorded the existing references where they matter.
- 🟡 Treated external mocks as a separate clause and flagged the missing boundary criterion. Kept both fixture examples without assigning them dataset kinds.
- 🟡 Used separate rows for independent test-creation duties and proposed review checks where the original review did not cover them. Used explicit review cells and labeled the default review as proposed.
