# Task queue for ChatGPT

ChatGPT works from this file, so the Developer does not have to start each task. Read it, take the first task not marked
done, and when its PR merges mark it done in a later PR. Rules for every task: branch from the latest `origin/main`;
branch name `chatgpt/<kind>-<what>`; the PR adds only the files the task names (never edit README.md or an existing
file unless the task says so); put notes in the PR description; keep at most 4 PRs open (raised from 2 by the Developer, Nov 18, so Task E can finish while Claude is offline); never merge (an Action merges a
PR only after Claude's clean review and a green `suites` check, and only for `chatgpt/inventory-*` PRs touching
`requirements/inventory/` and `chatgpt/drafts-*` PRs touching `requirements/drafts/`); stop and tell the Developer only if
blocked.

## Task B: draft requirements per feature (branch `chatgpt/drafts-<feature>`, one PR per feature)

Features, in this order: calendar, sources, feeds, history, google, settings, account, shell. (Claude has done rules and
event_templates and is doing events; do not touch those.)

For each feature, create ONE file `requirements/<feature>.md`:
1. Collect the rows of `requirements/inventory/suite_*.md` whose candidate feature includes the feature.
2. Group them into requirements. A requirement is one checkable rule of the feature's behavior, in the plain words of the
   app's user (not of the Python code). Merge duplicates and overlaps; keep each statement testable.
3. Format, as in `requirements/drafts/event_templates.md`: header (DRAFT, not approved), then a table
   `| ID | status | statement | evidence |` with IDs `<PREFIX>-NN` (CAL, SRC, FED, HIS, GGL, SET, ACC, SHL; continue after
   the highest number already in `requirements/<feature>.md`), status `proposed` (add `(?)` and a question when unsure),
   and evidence = inventory keys such as `S26-14`.
4. Leave out, and list at the end under "Not requirements": failure-sentinel rows, source-text checks (tests of the
   Python implementation), and pure pixel/layout measurements (those belong to `build_rules/theme.md`).
5. Do not invent behavior the inventory does not show. If a row is unclear, mark it `proposed (?)`.
6. Claude reviews each PR for coverage (every inventory row for the feature appears in a requirement or in "Not
   requirements") and wording, then the Action merges it. The Developer approves the drafts later, feature by feature.

Done: (none yet)

## Rule for every requirements draft: no UI mechanics, no duplication across features

A feature's requirement says what the feature does for the user ("Clicking a day opens the new-event dialog for that
date"). How dialogs, menus, sections, confirmations, info dots, pickers and phone layouts behave is shared UI and is
written ONCE in `requirements/common.md` (IDs `UI-NN`). A feature's requirement references it ("follows UI-02")
and never repeats it. If a row you are drafting is shared UI, add or reuse a `UI-NN` row instead (add it in your PR to
that file only if it is not there yet; otherwise reference the existing one). If the same behavior appears in two
features, write it once, in the owning feature or in common.md, and reference it from the other. (Developer, Nov 17.)

After the last feature draft merges, Claude runs a duplication review across all drafts before the Developer sees them
(layer-map.md, step 2). GPT: do not wait for it, and do not start a duplicate-removal pass yourself.

## Task C: README reconciliation (branch `chatgpt/drafts-readme`, one PR, file `requirements/drafts/readme_gaps.md`)

Start after Task B's last PR. Read README.md section by section (What it does; How it compares; Quick start; Settings;
How syncing works; The status page; Syncing straight to Google Calendar; Updating; Data and backups). For every claim
about what the app DOES (behavior a user can observe), check whether it is covered by a requirement in
`requirements/*.md` or `requirements/drafts/*.md`. List the claims that are NOT covered, as a table
`| README section/line | claim | closest requirement ID or none | proposed owning feature |`. Do not write new
requirements and do not edit README.md. Claude turns the confirmed gaps into requirements.

## Task D: CHANGELOG scan (later, same rules; split by version range, 300 lines per PR)

Same method on CHANGELOG.md: list behaviors a release says it added or fixed that no requirement covers.

Task D output (clarified Nov 17): one PR per 300-line chunk of CHANGELOG.md, newest first (lines 1-300, 301-600, ... 2,336).
Branch `chatgpt/drafts-changelog-<first>-<last>` (for example `chatgpt/drafts-changelog-1-300`); one new file
`requirements/drafts/changelog_gaps_<first>-<last>.md` in the same table format as `readme_gaps.md`
(`| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |`), anchors pinned to the
revision you read. Only new files; stop when the whole file is covered, then report that Task D is complete.

## No exceptions (Developer, Nov 17)

"Exceptions in general are very bad. Fix the requirement instead of adding an exception whenever you can." A requirement that says
"except", "unless", "never for X", "only for Y" usually means a general rule is missing. Before writing one, look for the general
rule (requirements/common.md: TIM time rules, UI interaction rules, CAP what an origin allows) and reference or extend it.
If no general rule fits, write one in common.md and reference it; list it in your PR description.

## Task E: gap triage into proposed requirements (starts after Task D; one PR per feature)

Task D is complete (README gaps: `requirements/drafts/readme_gaps.md`; CHANGELOG gaps: `requirements/drafts/changelog_gaps_*.md`, 8 files).
For each feature in this order: deployment, google, settings, sources, calendar, events, shell, account, feeds, history, rules, event_templates,
diagnostics, documentation, search, calendar_filter (a gap row's "proposed owning feature" column says which; if a row names two, take it for
the first and say so). Branch `chatgpt/drafts-gaps-<feature>`; ONE new file `requirements/drafts/gaps_<feature>.md`; never edit another file.

For every gap row owned by the feature, give it ONE outcome:
1. **Covered**: an existing requirement (`requirements/*.md` or `requirements/drafts/*.md`) already says it. Name the ID.
2. **Superseded**: a Developer decision replaced it (build_rules/layer-map.md: the time model TIM, Capabilities CAP, UI-NN, the filter and search
   split, default rules RUL-29, global Time Zones SET-47, ACC-16/17 numbers, "no exceptions"). Name the decision.
3. **New**: write a proposed requirement `| ID | proposed | statement | gap row |`. ID continues the feature's prefix after the highest number
   in `requirements/<feature>.md` (and the approved file). Rules for the statement: behavior only (no UI mechanics: those are UI-NN in
   common.md), no exception wording (extend or reference a common rule instead), no fixture wording, one checkable rule, `(?)` only for a
   real open question. If it restates another feature's rule, reference it instead.
4. **Not a requirement** (process, refactor, release note): say why in a few words.

Table columns: `| gap (file and line) | outcome | ID or decision | proposed requirement or reason |`. Claude reviews each PR for the
rules above and merges through the Action; the Developer approves the new requirements later with the rest of the drafts.
