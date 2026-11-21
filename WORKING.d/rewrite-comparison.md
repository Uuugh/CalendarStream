# Rewrite comparison and handoff (written 2026-11-21 for the next conversation)

## Files
- `requirements-readme.or.md` (Orchestrator) and `requirements-readme.sub.md` (cold sub-Claude): two rewrites of `requirements/README.md`.
- `tests-readme.or.md`, `tests-readme.sub.md`, `tests-readme.gpt.md`: three rewrites of `tests/README.md` (GPT's was pasted by the Product Owner; the brief is `gpt-brief.md`).
- The real READMEs are untouched. `lessons.md` holds the lessons; `rules-key.md` the old-to-new rule numbers.

## Result 1: requirements README (mine vs sub-Claude)
- Both near-lossless, same shape (Intro, Definitions, Rules, Not yet placed), same duplicates flagged (the freeze, the old-app pointers).
- The sub-Claude caught the "unless exactly one detail is meant" exception (Law 2) that I missed; it split into finer rows (to Rw-16). Mine dropped some retired-app fragments.
- Both invented a prefix for the rules (mine `Rq`, the sub-Claude `Rw` with a "Requirement writer" role), both marked 🟡.

## Result 2: tests README (three-way)
| | Mine | Sub-Claude | GPT |
|---|---|---|---|
| Size (original 5.2 KB) | 6.3 KB | 8.3 KB | 11 KB |
| Words missing | inflections | inflections | none |
| Words added | few | some, "(proposed)" | a lot (step lists, new Te-04.c, Te-05) |
| Sentence with no actor | guessed Ct, partly unmarked | guessed Ct, flagged 🟡 | Not yet placed 🟠 (followed the method) |
| Marks 🟡/🟠/🔴 | 5/2/5 | 30/2/1 | 20/8/1 |
| Duplicates with SCRUM.d | found 5 | found 1 | did not look |
| Format | table | table | tab-separated, redefined `^` |
None is shorter than the original; the only real shrink is settling which file owns the rules both files state.

## Method additions proposed (not yet applied)
1. An actor guess goes to "Not yet placed" unless the Product Owner decides (GPT's way).
2. Words added to the "What" cell must come from the source; words added to "When acted" or "How tested" are marked 🟡 and "(proposed)".
3. A rewrite is compared with the SCRUM.d rows it overlaps (Law 1), and its distinct words with the original's (missing words accounted for).
Decision table for a sentence: definition -> Definitions; rule with an actor -> a row; rule with no actor -> Not yet placed 🟠; rule that repeats a SCRUM.d row -> Not yet placed 🔴; both -> split; "Test:" tail -> How tested.

## Decisions waiting for the Product Owner
1. Which file owns the test rules: `tests/README.md` (SCRUM.d cites it) or `SCRUM.d` (tests README cites it)? Recommended: `tests/README.md`.
2. Numbering of rule IDs in an area README (continue SCRUM.d IDs, or new codes), and the prefix for the requirements rules (`Rq`, `Rw`, other).
3. Adopt the sub-Claude rewrite as the base for `requirements/README.md` (recommended), plus the Orchestrator's catches.
4. Approve or change the lines still marked 🟡 in `tests/README.md` (Definitions, Creating, Results, smoke paragraph) and `SCRUM.d/README.md` (Or-03.b and its routing table, Ct-02, Ct-04, Team-03.a, Or-13.b).
5. The 🔴 questions in `SCRUM.d/defects.md` (Q-P), and the marked coverage lines.

## State
- Usage: last readings 5h 37%, 7d 86% (7d at the Warning level, 85%). The status line writes `C:\Users\rfrie\.claude\usage-now.json`; Or-10.g reads it. Levels: Caution 70%, Warning 85%, in `SCRUM.d/usage.md`.
- Handoff to GPT: Codex rejected; GPT takes work by paste or by writing a named file in its connected workspace (repository Uuugh/CalendarStream); lesson in `lessons.md`.
- Shell: grep and sed cannot match the marks 🟡 🟠 🔴; use `LC_ALL=C` or awk (AGENTS.md, Environment).
- Next test sprint (the Product Owner launches it): verify the Team-05 commit rule through interruptions of each agent and a broken requirement.
