# Orchestration board (Nov 19)

The author of the requirements orchestrates and checks; it does not do the other steps. Product Owner = the repository owner, who decides. This file is the memory of what is next, who does it, and how incoming work is checked. Update it when a step changes.

## Roles

- **Product Owner**: decides; answers `build_rules/open-questions.md`; blanks the status of agreed rows; rewrites `build_rules/` as Scrum; launches the other agents.
- **Author (this agent)**: keeps the requirement files consistent; parses and corrects work that comes in; runs the turns of a review; never builds the app and never plays the Coder.
- **Coder**: a separate Dart and Flutter developer; reads only `requirements/` and reports gaps; later builds stories.
- **Contributor** (for example ChatGPT): produces drafts, scans or stories as pull requests; the author checks them with the list below before they merge.

## Steps

| # | Step | Owner | Input | Output | The author checks | State |
|---|---|---|---|---|---|---|
| 1 | Review slice 1 (Account, Calendar filter, Print, Calendar, common UI, theme) | Coder, then author at REVIEW 2 and 4 | issue #85, commit 51f7354 | findings; fixes in commits | each finding: Accepted, Rejected or Partly, with a reason or a fix commit | issue open, waiting for REVIEW 1 |
| 2 | Review the other slices: Sources + Feeds; Google; Settings + Shell + Events; Rules + History + Search + Event templates; Deployment + Diagnostics + Documentation | Coder, author | a new issue per slice, same first post as #85 | findings; fixes | as step 1 | after step 1 shows the kinds of gap |
| 3 | Answer the open questions and review each feature file | Product Owner | `build_rules/open-questions.md`, `requirements/*.md` | answers; approvals (a deleted `proposed`) | apply each answer: update the row, remove the question, record in `oldkey.md` if an ID changes | waiting |
| 4 | Rewrite `build_rules/` as Scrum (stories, sprints, epics, backlog; per-story tests) | Product Owner (or a Contributor) | the old build rules, `requirements/README.md` | new process files | no agent named; terms as `requirements/README.md`; story = named requirement IDs; tests per the testing decisions in `layer-map.md` | not started |
| 5 | Retire legacy: `build_rules/theme.md`, old build, test, review and deploy files, `theme-map.md`, the evidence column, `oracle-coverage-notes.md` | Product Owner decides; author removes | agreement | files removed | nothing referenced is lost | after steps 1 to 4 |
| 6 | Port, story by story | Coders | requirements + stories | Dart code, tests naming the requirement IDs | each story's tests pass; touched requirements retested | after step 4 |

## Checking incoming work (a pull request or a draft)

1. `tests/tools/req_check.sh` reports no errors (it runs on GitHub as "Requirements").
2. It follows the rules in `requirements/README.md` (rules 1 and 2 are the laws).
3. No history or oracle wording in a statement, no agent or tool named, Scrum terms, the Product Owner as the decider.
4. New or changed IDs have a row in `oldkey.md`; no reference to an ID that does not exist.
5. A rule found in more than one place is merged, not copied. A question goes in `open-questions.md` after looking in the other requirements, the code and https://docs.flutter.dev/ and https://dart.dev/.
6. Say clearly what was not checked.
