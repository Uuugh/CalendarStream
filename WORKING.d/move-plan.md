# Move plan (temporary; delete when the move is done)

Procedure for moving the live files into the new layout. It is a one-time procedure, so it lives here and not in `SCRUM.d/`.

1. Work on a branch and a pull request, not on main. Tag the commit before the move. Use `git mv` so history follows.
2. Run no Coder or Reviewer agents during the move (they read the repository).
3. Moves and reference fixes are separate commits, each followed by `tests/tools/req_check.sh`.
4. The Orchestrator, not the mover, changes `req_check.sh`, so the checker is not changed by the agent it checks.
5. The Product Owner approves between the drafting and the moving.

## Moves
- `build_rules/open-questions.md` to `requirements/open-questions.md`; add it to the exclusions in `req_check.sh` (next to `README.md` and `oldkey.md`). `requirements.yml` already covers `requirements/**`.
- To `WORKING.d/`: the Python reference taken out of the old `AGENTS.md` (code map, `tests/run.sh`, `pip-audit`, "Before you push": see git history of `AGENTS.md`), `build_rules/reverse-engineering/`, `coder-review-1.md`, `review-findings-1.md`, and the rest of `layer-map.md` once its decided parts (testing rules, target layout) are in `packages/README.md`.
- Keep `build_rules/2-build.md` and `5-deploy.md` until the Python app is no longer released with them.

## References to fix
`tests/tools/req_check.sh` (open-questions path, the "Rules:" line), `tests/run.sh`, `tests/README.md`, `.github/workflows/tests.yml` (`paths-ignore`), `release.yml`, the dart-flutter skill (drop its Layout, Tests and Do-not sections; `packages/README.md` and `AGENTS.md` cover them), and `requirements/` (`README.md`, `common.md`).

## Edits to `requirements/README.md`
- Rules 1 and 2 become numbered stubs linking to `AGENTS.md`, so rule numbers and `oldkey.md` do not shift.
- Replace "defined in the process rules" (stories, epics, sprints) with a link to `SCRUM.d/README.md`.
- Replace "Process: build_rules/" and the `build_rules/0-overview.md` pointers.
- Add: run `tests/tools/req_check.sh` before and after changing any row (it was in the old `AGENTS.md`).
- Rule 12 stays with its number and Test line; reword it to begin "In `requirements/`, a `.d` folder (see `AGENTS.md`)" and keep the C and P letters; line 63 ("Modules come in two kinds...") shrinks to a link to the `.d` definition in `AGENTS.md`.

## New check in `req_check.sh`
Compare the working tree and the range since the merge-base with the base branch (CI: the pull request base; locally `origin/main`). Raising a status (`proposed` to `backlog`) is fine; lowering one (`backlog` or blank to `proposed`) is an error unless the ID is named on a `Status-reset:` line in a commit message in the range. A removed row is a warning (merges are recorded in `oldkey.md`).

## Acceptance test
A cold agent with the one-line prompt "read AGENTS.md" answers where the rules, the tests and the open questions are.
