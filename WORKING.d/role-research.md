# Role research: vibe-coding rules mined for the AI roles

Sources: A = alguidelines.dev vibe-coding-rules (index page, plus its `al-testing` subpage; the other subpages are AL
syntax and were not read), B = agentkit.best "12 vibe coding rules", C = obviousworks `codex/AGENTS.md` (a template
with placeholders).

## Rules found

**A.** The index only says: rules are structured markdown an agent can parse; copy, adapt, configure the assistant.
`al-testing`: app code and test code in separate projects, tests never in the app folder, the app never references the
tests; generate tests only when asked; tests mirror the app's feature folders; unit-test all business logic; Given/When/Then
names; test-data factories; shared test utilities in one folder.

**B.** 1 write acceptance criteria (success, failure, exclusions); 2 persistent rules file; 3 simplest stack, approval for
new dependencies; 4 plan before changes, no edits until approved; 5 smallest testable step, verify, commit; 6 name the
allowed paths, protect named areas; 7 review the actual diff (unrelated edits, duplicates, config, credentials); 8 test
after every change, label each check honestly, never weaken a test to pass; 9 commit every working checkpoint; 10 revert
early in a failure loop and restart from verified context; 11 protect secrets and data; 12 review scaled to risk.
Extras: verify evidence, not the agent's confidence; labels Passed/Failed/Not run (reason)/Not applicable; fresh-session
handoff (objective, checkpoint, rules, verified errors, checked against the repo); pre-commit checklist.

**C.** Clarify before coding, ask when intent is unclear; simplest viable solution; security by default; design for
testability; no new dependencies without approval; atomic changes touching only the task's files; lint and test after
every change; review your own output for redundancy and simpler alternatives; when uncertain propose alternatives with
pros and cons and cite existing patterns; mock external dependencies, not internal logic; Arrange-Act-Assert;
conserve context (file-scoped commands, reference docs instead of pasting).

## Worth adopting, per role

- **Orchestrator.** State per brief what is out of scope and which paths the agent may write (B1, B6); the brief names the
  acceptance criteria as the requirement IDs (B1). Treat an agent's report as a claim and check it against the diff and
  the test output (B "evidence"). Stop an agent in a failure loop (several failed attempts or a growing diff), keep its
  diagnostics, and relaunch cold from the last verified commit (B10). A relaunch carries objective, checkpoint, rules and
  verified errors, checked against the repo (B handoff). Check the diff for unrelated edits, new dependencies and config
  changes (B7, C).
- **Coder (build).** Smallest testable step, then verify, then commit (B5, C). Touch only files the story needs (B6, C).
  Ask, or propose alternatives with pros and cons, when a requirement is unclear, and send the defect to the Orchestrator
  (C). Add no dependency without approval (B3, C). Never weaken or delete a test to make it pass (B8). Review your own diff
  for redundancy and a simpler way before reporting (C).
- **Coder (tests).** Keep test code apart from application code and mirror the feature folders (A). Name tests by the
  behavior and requirement ID (A Given/When/Then). Shared test data factories and utilities in one place (A). Mock
  external systems, not internal logic (C). Write from the requirement's observable success and failure (B1).
- **Tester.** Run the checks after every meaningful change in layers (analyze, tests, req_check) and report each honestly
  (B8). Report evidence: the command run and its output per requirement (B). Say what was not run and why (B).
- **Reviewer.** Review the actual diff, not the agent's summary (B7). Look for unrelated edits, duplicated code,
  dependency and config changes, and secrets (B7, B11). Scale depth to risk (B12).

## Already ours (do not repeat)

- Cold, one slice per agent, brief with allowed writes and progress file: `SCRUM.d/README.md` (Orchestrator 2, 7).
- Diff check after work, no status goes backwards, `req_check.sh`: `SCRUM.d/README.md` (Orchestrator 5), `AGENTS.md`.
- Persistent rules file: `AGENTS.md`; session handoff memory: `WORKING.d/README.md` (Orchestrator 1, 8).
- No secrets or real data: `AGENTS.md`. Push after each verified commit: `AGENTS.md`.
- Definition of done (analyze, test, req_check): `SCRUM.d/README.md`.
- Tests mirror the requirements, written without the implementation, result `pass`/`fail`/`not run`, cheapest method,
  share before you write: `tests/README.md` and `SCRUM.d/README.md` (Team).
- Reviewer read-only; the team never edits requirements, defects go to the Orchestrator: `SCRUM.d/README.md`.
- Ask only the Product Owner's decisions; no duplication; review wording tests: `AGENTS.md`.

## Conflicts or recommended against

- Plan approved before any edit (B4): conflicts with `AGENTS.md` (act without waiting for a permission already held).
  Keep the plan in the brief, not an approval step.
- "Not applicable" check label (B): `tests/README.md` has three results and a fourth is a new status; recommend against.
- "Generate tests only when asked" (A): ours always requires the Coder (tests); do not adopt.
- 85% coverage on critical paths (C): our measure is requirement rows tested, not coverage; recommend against.
- Commit after every checkpoint (B9) and conventional commit format (C): a commit-style rule is not ours and would
  need a Product Owner decision; commit cadence is already "push after each verified commit".
- Separate test project/folders with a dependency rule (A): our tests live in `tests/<feature>/`; Dart package layout is
  `packages/README.md`'s to decide, not ours.
- Risk tiers and production sign-off (B11, B12), security checklists, code-style and naming rules (A, C): not role
  responsibilities here (AL- and web-specific); skip.
- Source A's index page contains no rules of its own; weight it as the weakest source.
