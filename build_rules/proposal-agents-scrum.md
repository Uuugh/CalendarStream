# Proposal for discussion: AGENTS.md, Scrum, MEMORY.md, area READMEs

**This is a proposal, not a decision.** Nothing here is in force until the Product Owner approves it. Comment on the pull request.

## A. Why

The orchestrator forgot standing rules across conversations. A status the Product Owner had blanked (meaning agreed) was reverted by a delegated agent. The orchestrator then told the Product Owner that nothing had been overwritten, having checked only committed history, not the working tree.

The rules existed, but they are spread over `requirements/README.md`, `build_rules/HANDOFF.md` and `build_rules/orchestration.md`. They are written for whoever edits, not for whoever delegates. There is no brief template, and there is no after-check for a status going backwards.

## B. The Product Owner's plan (as given Nov 19)

- `CLAUDE.md` is a pointer to `AGENTS.md` and `MEMORY.md`.
- `MEMORY.md` is a temporary checklist of work in progress or awaiting action. Items are deleted when done. It is not a rule file.
- `AGENTS.md` is where all agents get: the LAWS; a table of contents; the instruction to read an area's README before touching the area; and the Responsibilities (Scrum).
- Scrum is stored somewhere and referenced by `AGENTS.md`.
- Area READMEs (not the main git-home README) define the rules of their area.
- Everything about the Python app is temporary and goes when the transition ends.
- Before the conversation ends, a subagent replaces `build_rules` with Scrum roles, responsibilities and processes.

## C. The orchestrator's points

1. **MEMORY.md must live in the repository.** The memory kept outside git holds rules, and rules there are invisible to other machines, other agents and review. Recommendation: move today's three working notes (delegate to subagents; push after a verified commit; a blank status means backlog) into `AGENTS.md` / Scrum, and delete them from that outside memory.

2. **Python material is temporary.** This covers the code map, `tests/run.sh`, `pip-audit` and the "before you push" section. Recommendation: keep it in one clearly temporary part, or a section of `MEMORY.md` marked for deletion, never a permanent area README. Items that serve only the Python app are removed with it, but they stay until the port passes.

3. **The laws live once.** `AGENTS.md` holds them and `requirements/README.md` links to them. Open decision: are the laws only the two about requirements, or also "never revert the Product Owner's edits" and "the Product Owner decides"? Recommendation: the second, wider set.

4. **Scrum is stored in a `scrum/` folder at the root, with its own README.** It holds the roles (Product Owner, Orchestrator, Author, Coder, Tester, Reviewer), the responsibilities, the sprint steps and the definition of done. The orchestrator's pre-flight, brief template and post-flight are the Orchestrator's responsibilities there, not a second file:
   - Pre-flight: `git status` and `git diff`; commit the Product Owner's uncommitted work first.
   - Brief template: the standing rules go inside every brief.
   - Post-flight: read the diff for statuses that went backwards, run `req_check.sh`, push.

5. **A mechanical check.** `req_check.sh` fails when a row's status goes from backlog or blank back to proposed in the last commit.

6. **Testing.** The location and naming rules are already written once in `.claude/skills/dart-flutter/SKILL.md`, "Tests: where they live" (commit 980b5b9). A skill is read by only one tool and only when triggered. Recommendation: the rules move to `packages/README.md` (an area README) and the skill links to it. The controllable clock, per-requirement reporting and the definition of done (`flutter analyze`, `flutter test`, `req_check.sh`) are still only in `build_rules/layer-map.md` and move there too. The undecided part (how Dart tests run in parallel, what a run reports and where, the Dashboard) becomes the first backlog story. It is not invented now.

7. **Moving `build_rules` breaks references.** Affected: `tests/tools/req_check.sh` (reads `build_rules/open-questions.md`), `tests/run.sh`, `.github/workflows/*.yml`, `requirements/README.md` and `common.md`, the dart-flutter skill, `tests/README.md`. `open-questions.md` and `reverse-engineering/` need a live home.

8. **Order.**
   1. One agent drafts `AGENTS.md`, `scrum/` and `packages/README.md`.
   2. The orchestrator reviews.
   3. The Product Owner approves.
   4. A second agent moves the live files, fixes the references and retires the legacy files.
   5. The Product Owner approves again before merging.

## D. Questions for the earlier orchestrator

The one who wrote `HANDOFF.md` and the testing section:

1. What did you intend as the permanent home of the rules?
2. What in `layer-map.md` about testing is still wanted?
3. Any objection to points 1 to 8?
4. Anything we missed that a cold agent would need?
