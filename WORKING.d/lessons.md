# Lessons (the Orchestrator's, kept)

Keyed by rule ID, one or two sentences each. Read the entry before changing or removing a rule (Or-02.a); add one when a correction changes a rule (Or-02.b).

- **Or-01**: Two intents, not one task list: protect the Orchestrator's context and the Product Owner's usage on long work, and independence for work that must not see the answer (the Reviewer, Ct, Te). A task list hides both and invites exceptions.
- **Or-03**: Accept a Tester's report that names the command and one result per requirement. Rerunning the tests duplicates the Tester and spends usage (ocean sprint).
- **Or-15.d, Or-24.c**: The first launch skipped the usage readings and the estimate. The gate now needs the Ready check, the readings and the estimate written before any launch, and a story that cannot fit the window is reported, not launched.
- **Or-02.e**: The marks are ordered by severity: yellow a question, amber an agent cannot act on the line (the Orchestrator rewrites it), red a Law break (the Product Owner decides). A mark sits in the first cell so the table row still parses.
- **Rv-01**: The Reviewer is outside code development. It tests the process files cold and runs when a process file changed; it is not a per-story code reviewer.
- **Old Or-09.b (removed)**: the 1,000-line story size came from the old per-story Reviewer. The usage fit (Or-15.c), estimated before launch, is the single size limit.
- **Requirements rules 11 and 11.a**: a parent row passes through its sub-requirements, so its test cell may be `—`; the check skips parents.
- **Cb-14, Cb-14.a, Cb-14.b**: one public class per file, the closed family and the private helpers are separate rules so none is written as an exception (Law 2).
- **Or-20, Or-14.d**: starting a sprint is the Product Owner's decision. The Orchestrator asks at the start of a project and after each Retrospective and never launches one (a gate, unlike Scrum's immediate next sprint).
- **Sprint end**: a sprint ends with its Retrospective (Scrum Guide 2020: "The Sprint Retrospective concludes the Sprint").
- **Terms**: "sub" applies to anything (a sub-rule, a subagent); never define a "sub-orchestrator".
- **Defect and issue**: a defect is a requirement an agent cannot act on (status `defect`); an issue is code that does not meet a requirement.
