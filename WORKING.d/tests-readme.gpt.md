tests: how requirements are tested
Intro
Its test cell in the requirement row names it (what a test cell means is defined in requirements/README.md). Who writes and who runs tests is defined in SCRUM.d/README.md.

How runs are split and what a run reports to the dashboard is the first open story in WORKING.d/README.md.
Definitions
- Test: A test verifies one or more requirements.
- 🟡 Behavior: one thing a requirement's statement says must hold.
- 🟡 Uncovered: a behavior that no test the row lists checks.
- CI (continuous integration): the GitHub workflow that runs our scripted checks on every push; it costs no agent usage.
- 🟡 Result: one of four words for a requirement ID in a run: pass (every listed test passed and no behavior is uncovered), fail (a listed test failed; the result gives the ID, what was expected and what was found), not run (a test could not start or crashed before its checks, or the row has status defect) or uncovered (a behavior of the row is uncovered).
- Methods, cheapest first (a guide, not a limit). A test that CI can run costs no agent usage, so it is cheaper than the same test an agent must run: methods 1 to 4 are scripts CI can run, methods 5 and 6 need an agent.
  1. A static check or script on files (tests/tools/req_check.sh is one).
  2. A unit test of pure logic, with a clock the test controls and made-up data.
  3. An API test against a running server and a throwaway database.
  4. A comparison with stored expected output (made-up fixtures, or screenshots).
  5. A browser run by an agent, for layout and behavior nothing cheaper can check.
  6. A written procedure an agent follows, for a row no script can decide.
- Smoke procedure: test/smoke.md, in the project's test/ folder, is the smoke procedure: a written procedure an agent follows at each Review, derived from the requirements.
- Made-up data: Demo.ics is a made-up schedule, work.ics a second made-up calendar.
Rules
For ^ on a top-level row, the Reviewer checks the named artifacts for the evidence specified in that row’s How tested cell. A sub-rule’s ^ refers to the corresponding cell in its parent.
ID    What    When acted    How tested
🟡 Ct-05    The rule. A requirement is tested by the cheapest method, in agent usage and in time, that still verifies it. No method is required and none is banned. Pick the cheapest one that can fail when the requirement is not met. Apply Ct-05.a through Ct-05.c in order.    The Coder (tests) starts work on a test for a requirement.    Review: for each test, name a cheaper method and show it would not verify the row; for each test an agent runs, show that CI cannot run it. Start at method 1 when evaluating the listed methods. The review records that method 1 is first when it is selected. 🟠 The source gives no way to rank two qualifying approaches when one uses less time and the other uses less agent usage.
Ct-05.a    Check the requirement for observable success and failure. Use the method guide in Definitions to evaluate test methods against those observations.    ^    ^
🟡 Ct-05.b    Share before you write. Before writing a new test, look for an existing test to share or modify, and do so when that is the cheaper way to verify the requirement; one test may verify several requirements. Use the requirement IDs and behaviors to search the existing tests.    A new test is proposed.    Review: for each new test, name the existing test it could have extended and show that extending it would have cost more. When the search finds zero candidates, review the search and its results.
Ct-05.c    Creating and merging tests. The Coder (tests) creates a test from the requirement alone, from its observable success and failure, and names it by the behavior and the requirement ID.    The method and the decision to write or reuse a test have been recorded.    Review: for each test, name the requirement it verifies. Check the test name for the behavior and requirement ID, and match its assertions to the requirement statement.
🟡 Ct-06    Shared helpers live in one place, and a test mocks external systems, not internal logic. Put common helper code in one shared location. Use the production implementation for internal logic.    The Coder (tests) writes or changes a helper or a mock.    Review the changed helpers for duplicate implementations and trace each mock to an external system boundary.
🟡 Ct-07    Two tests that verify the same row are merged into one. Keep checks for each behavior when combining the tests.    Two test declarations name the same requirement ID.    Review: for each pair, show they verify different rows. Compare the merged assertions with the original assertions for the row.
🟡 Ct-08    A test whose requirement is deleted is deleted. For a shared test, remove the deleted ID and its checks that serve zero remaining IDs. Delete the test when zero IDs remain.    A requirement ID named by an existing test is deleted.    Review the change for references to the deleted ID and check that every surviving ID retains its checks.
🟡 Ct-09    The tests a row with no sub-requirements lists together check every behavior of its statement. Match each behavior to a check in a test listed in the row.    The Coder (tests) creates or changes tests for a row whose list of sub-requirements is empty.    The Tester's result for the row names each uncovered behavior (Te-02). Review the behavior-to-check mapping against the row and its listed tests.
🟡 Ct-10    A test declares whether one run covers all its requirement IDs or runs once per ID. Record the declaration with the test.    The Coder (tests) creates a test or changes the IDs it covers.    Review: for each test, name its declaration. Compare the declared mode with how the test runs.
🟡 Ct-11    A requirement that depends on time is tested with a clock the test controls; no test waits real time. Advance the controlled clock to exercise the timing condition.    The Coder (tests) writes or changes a check for a behavior whose outcome depends on time.    Review: for each time-dependent requirement, show the controlled clock. Inspect the test for waits tied to elapsed real time.
🟡 Te-04    Results. Each run reports one result per requirement ID, with the command run, by this precedence: fail, then not run, then uncovered, then pass (Definitions). Any result names each uncovered behavior. Apply Te-04.a through Te-04.c in order.    A test run ends, or the test command fails to start.    Review: each result in a report is one of those four words, names the command, and names each uncovered behavior. Compare the reported IDs and selected results with the run records.
Te-04.a    For each requirement ID in the run, use Definitions to determine which result words apply to its own tests or status. Identify uncovered behaviors using the tests listed in the row.    ^    ^
🟡 Te-04.b    A row with sub-requirements is checked through them (Parent tests, requirements/README.md). A row with sub-requirements takes the first of these four words, in that order, that its own tests or its sub-requirements have, and names the sub-requirement that has it. Compare the direct sub-requirements’ results and the row’s own results using Te-04.    The row has at least one sub-requirement and their results have been determined.    Review the parent result against the applicable words in its own results and the results of its sub-requirements. Check that each named sub-requirement has the reported word.
Te-04.c    Write the report with one entry per requirement ID. Use the word selected in Te-04.a and Te-04.b by the precedence in Te-04. Include the command and uncovered behaviors as required by Te-04, and the failure details specified in Definitions for fail.    A result word has been selected for every requirement ID in the run.    ^
🟡 Te-05    Follow the smoke procedure in file order. Each step names the requirement IDs it exercises and is reported pass, fail or not run. Record one of those words against each step.    Each Review.    Review: each step names requirement IDs, and the Tester's smoke report follows the file. Compare the entries with the steps in test/smoke.md.


Not yet placed
- 🟠 “Its test cell in the requirement row names it” is retained in the Intro. The first “Its” refers to the requirement’s test cell, and “it” refers to the test.
- 🟠 “Expected outputs of the old app are captured once as made-up fixtures and compared by script (method 4), not by running the old app each time.” The sentence supplies a method but gives no actor for capturing the fixtures or comparing them.
- 🟠 “An issue gets a failing test first; the fix follows. Test: review: the commit that fixes an issue follows the commit of its failing test.” The sequence crosses writing tests and fixing code. The sentence gives no actor responsible for enforcing the commit order.
- 🟠 Layout. “Tests sit in test/<feature>/, mirroring requirements/<feature>.md, in the Dart package layout (https://dart.dev/tools/pub/package-layout); thin end-to-end tests sit in integration_test/.” The sentence gives no actor. It also supplies no observable criterion for “thin.”
- 🟠 “Fakes and made-up data are never real data (AGENTS.md).” The constraint gives no actor or review evidence for establishing the origin of the data.
- 🟠 “Made-up data lives in tests/data/, one dataset per kind, shared by all tests (Demo.ics is a made-up schedule, work.ics a second made-up calendar). Test: review: a test that carries its own copy of data names the shared dataset it could have used.” The placement and sharing instruction gives no actor. “Kind” has no defined criterion, and the review describes what a private copy names while the preceding sentence calls for sharing.
- 🟠 Te-04.b gives no reporting instruction for a parent whose own tests supply the selected word and whose sub-requirements have other results. It also gives no tie rule for several sub-requirements with the selected word.
- 🔴 The original pass definition and the requirement that every run report one of four words leave a row with no listed tests and no behaviors open to interpretation. The brief supplies no explicit result for that case.
Choices
- 🟡 Continued numbering at Ct-05 and Te-04. Used Ct for test authoring and maintenance, Te for reporting and smoke execution, and Rv for review checks.
- 🟡 Kept the methods in Definitions and grouped method selection and reporting into ordered flows.
- 🟡 Added review evidence for the first method, searches with zero reuse candidates, naming and assertions, mocks, merged checks, declarations, and clocks.
- 🟡 Read test deletion per requirement ID so a shared test survives for its remaining IDs.
- 🟡 Used direct sub-requirements for aggregation and left the reporting gaps open.
- 🟡 Kept “Review,” “Dart package layout,” and “external systems” as source terms.
