# Orchestration board (updated Nov 19)

The orchestrator (the author of the requirements) keeps the requirement files consistent, runs and checks the other agents, and does not build the app. Product Owner = the repository owner, who decides. This file is the memory of what is next and how incoming work is checked; update it when a step changes.

## Roles

- **Product Owner**: decides; answers `build_rules/open-questions.md`; agrees to rows (deletes `proposed`); launches the agents; decides which legacy files go.
- **Orchestrator (author)**: edits the requirements, parses every agent report against `requirements/README.md`, fixes what is wrong in the one owning row, records ID changes in `requirements/oldkey.md`, passes only real decisions to the Product Owner. Never plays the Coder.
- **Coder** (a read-only agent now, builders later): reads only `requirements/` and reports what it cannot implement; later builds stories.
- **Reviewer** (read-only agent): checks requirement files against the README rules.
- **Contributor**: a person or agent that produces drafts as pull requests; checked with the list below.

How agents are run: cold (no conversation context), read-only, one slice each, a progress file per agent in the scratch folder, shown to the Product Owner as simple progress bars. Prompts are minimal: the role, the repository path and "read AGENTS.md and follow it". The Product Owner reports usage (`/usage`); pause the agents at about 70%.

## Steps and their state

| # | Step | State |
|---|---|---|
| 0 | Reorganize the requirements: features, modules (`connections.d`, `plugins.d`), shared UI and theme, two laws and 14 rules each with a test, `req_check.sh`, `oldkey.md` (R0 to R39), message catalog (`requirements/messages/`) | done |
| 1 | Coder review of every file by six slices, run 1 (baseline: about 390 of 900 rows cannot be implemented, `coder-review-1.md`) | done |
| 2 | Fix what that review found (bucket A in `coder-review-1.md`): contradictions are fixed; still to do: about 30 undefined terms, statements that point at the legacy theme file (port the badge and popover values into THM rows), README roles (Author, Coder, Product Owner) and the DEF prefix, `common.md` to the line format | partly done |
| 3 | Reverse-engineer the Python app with six blind agents and compare with ours (data in `build_rules/reverse-engineering/`: 1,410 rows; about 484 covered, 102 different, 793 gaps, 180 only in ours) | done |
| 4 | Fill the gaps from `reverse-engineering/compare/slice1..6.md`, one slice at a time: numbers into DEF-01, user-visible wording as `msg:key` rows citing the catalog, behaviors as rows. Slice 1 (account, settings, shell) is filled (Nov 19: 31 rows, 11 message keys, 16 DEF-01 rows; its A-only rows and the differences wait for the Product Owner); next is slice 2. The Product Owner confirms the roughly 100 differences first (ours wins; the big ones are listed in `HANDOFF.md`) | slice 1 done; slice 2 next |
| 5 | Re-run the six Coder slices; compare with the baseline; repeat 2 to 5 until the count is acceptable | not started |
| 6 | The Product Owner answers `open-questions.md` and agrees to rows (`proposed` to `backlog`); decides the three proposed rule changes (bucket B in `coder-review-1.md`) | waiting on the Product Owner |
| 7 | Rewrite the process as Scrum (stories, epics, sprints, backlog; the Dashboard records sprint and done; per-story tests) | not started (Product Owner) |
| 8 | Retire the legacy files listed in `build_rules/README.md` | not started (Product Owner decides) |
| 9 | Port, story by story, with the `dart-flutter` skill (`.claude/skills/dart-flutter/`) | after 7 |

Later ideas not yet requirements: a Users feature that decides who may see secrets in logs (until then the one signed-in user is authorized); Outlook and Apple connections; the CCS+ pause and per-source download interval if the Product Owner wants the old app's behavior.

## Checking incoming work (a pull request, a draft or an agent report)

1. `tests/tools/req_check.sh` reports no errors (it runs on GitHub as "Requirements").
2. It follows the rules in `requirements/README.md` (rules 1 and 2 are the laws).
3. No history or oracle wording, no agent or tool named, Scrum terms, the Product Owner as the decider.
4. New or changed IDs have a row in `oldkey.md`; no reference to an ID that does not exist; user-visible wording is a cited message key, not text.
5. A rule found in more than one place is merged, not copied. A question goes in `open-questions.md` only after looking in the other requirements, the Python app (rule 10) and https://docs.flutter.dev/ and https://dart.dev/.
6. Read `open-questions.md` for answers before editing anything. Say clearly what was not checked.
