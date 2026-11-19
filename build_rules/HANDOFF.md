# Handoff: how we work and where everything is (written Nov 17-18 2026)

Read this first in a new conversation. Then `build_rules/layer-map.md` (the plan and the dated decisions), `requirements/README.md` and `build_rules/open-questions.md`.

## The rules of our conversation

1. **The Developer is one person, often dictating by voice.** Garbled text happens; when unclear, ask in plain words, one question at a time. Never guess a big decision.
2. **Questions go in two places:** asked in chat, one at a time, in plain words (what it is, my recommendation, a short answer); and filed in `build_rules/open-questions.md` with an `Answer:` line (the Developer may type the answer there). Remove a question once it is acted on and record the decision in `build_rules/layer-map.md`. Before asking, check whether a common rule already decides it (do not repeat a decision), and whether the code answers it (read the code).
3. **The Developer edits the files directly.** Always check `git status` and `git diff` for uncommitted changes in `requirements/` and `build_rules/` before editing; read them as instructions; never overwrite; commit them with your changes. **A blank status means the Developer agreed.** `proposed` and `planned` mean not yet agreed. Never reuse an ID.
4. **Requirements say what a feature does for the user.** One file per feature in `requirements/<feature>.md`; behavior shared by several features is written once in `requirements/common.md` (TIM time, UI components, CAP capabilities, DEF defaults and limits) and referenced. **No exceptions**: fix or add the general rule instead. Look and layout go to `build_rules/theme.md`. No pixel values (event lines, theme sizes). No web-page mechanics (UIC-13: changes show at once). No Python-test wording ("sampled", "fixture"). No "is refused" rule for a control that cannot produce a bad value.
5. **Decisions that shaped the rules** (all in layer-map.md): UTC storage and per-event zones; Local zone from the device; the database overrides env (DEP-28); Site Admin settings are shared, User settings are per device (one user for now); layout zones left/center/right, stack then scale then clip (triple dot) or scroll (UIC-14); anchors for badges (UIC-15); one resize bar (UIC-16); UI components separate from features (UIC-17).
6. **Commit and push often.** Commit messages end with the Co-Authored-By line from the session. **Never merge pull requests by hand:** an Action merges ChatGPT's PRs after a clean `**Claude review, PR #N**` comment (run `gh workflow run "Inventory auto-merge"` after the comment; the schedule is unreliable).
7. **Style:** a timestamp line `---------- HHMM EST ----------` (EST = UTC-5, from `date -u -d '-5 hours' +%H%M`) at the top of the first reply after a break; commands in their own code block with nothing after them; be active, not passive; say plainly when something was not checked.
8. **Freeze:** no new features until the Python-to-Dart port is complete; the Python app (`app/`, `tests/`) is the running app and the oracle until step 5.
9. **Never put the Developer's real schedule, username or Google secret anywhere;** the Dashboard artifact is private; do not link it to other AIs.

## Where things are

- Plan, steps, decisions: `build_rules/layer-map.md` (steps 1 to 7). Processes: `build_rules/0-overview.md` to `5-deploy.md`.
- Requirements: `requirements/<feature>.md` (index in `requirements/README.md`). The inventory of the Python suites (evidence keys Sxx-NN): `requirements/inventory/`.
- Issues: GitHub issues (label `issue`, `feature:<name>`, titles "I22: ..."). The Dashboard is rebuilt after the port (DIA-02 to DIA-04).
- ChatGPT's queue and rules: `build_rules/gpt-tasks.md` (Task E, done; its `gaps_<feature>.md` files were folded in and deleted; branch `chatgpt/drafts-gaps-<feature>`).
- Dart code: `packages/domain` (Event, rule schema, text matching, regex legality). SDK: `C:\Users\rfrie\Development\sdks\flutter\bin\dart`. Parked test overhaul: branch `paused/test-parallel`.
- Memory notes for Claude: `C:\Users\rfrie\.claude\projects\C--Users-rfrie-Development-Projects-CalendarStream\memory\`.

## State and next steps (Nov 19)

All process language is Scrum (Product Owner, story, epic, sprint, backlog) and nothing in the requirement files names an agent. `requirements/README.md` has the definitions and the ten rules for writing requirements (say it once, numbers only in DEF-01, shared things in their one home, no history); `tests/tools/req_check.sh` checks what a script can and runs on GitHub when `requirements/` changes (workflow "Requirements").

Done in the third conversation:
- Task E (ChatGPT's gap triage) was folded into the feature files; `requirements/drafts/` is deleted.
- Every feature file is organized into requirements with sub-requirements (ACC-06, ACC-06.a), duplicates merged, numbers moved to DEF-01 in `common.md`, shared things moved to `common.md` (UI-NN) and `theme.md` (THM-NN), and Print made its own feature (`print.md`, PRT). `requirements/oldkey.md` records every old ID to new ID (batches R0 to R23).
- `build_rules/theme.md` (legacy, kept only as the oracle) is converted into `requirements/theme.md` and the UI rows; `build_rules/theme-map.md` is empty of work except the note. The legacy file can go when the Product Owner agrees.
- The Python app's code answered most questions (limits such as retry delays, watch renewal, memory bounds); those values are in DEF-01 as proposed rows for the Product Owner to review.
- The Beta section was deleted; History has a Show secrets switch (HIS-04.b); passwords are enforced (ACC-04, SET-06.c).

Next:
1. **The Product Owner answers `build_rules/open-questions.md`** (10 questions) and reviews each feature file, blanking the status of the rows they agree.
2. **The coder review (orchestrated by the author, started Nov 19).** Issue #85 (slice 1: Account, Calendar filter, Print, Calendar, common UI, theme) is open with the Coder's instructions in its first post; the Product Owner launches a separate developer conversation and says "Do REVIEW 1" there, then passes the turns (the author acts at REVIEW 2 and REVIEW 4). After slice 1, the other slices follow. Originally: after the Product Owner is content, a developer who knows Flutter and Dart reads only `requirements/` (starting with its README) and lists every guess they had to make (undefined term, two readings, conflict, missing limit or default, untestable, duplicated, a rule that belongs in common or theme). Method: the REVIEW process adapted to Scrum terms, one issue as the channel, numbered turns.
3. The Product Owner rewrites `build_rules/` as Scrum (stories, sprints, epics, backlog) with per-story testing against the touched requirements; the old build, test, review and deploy files and `theme.md` retire.
4. Port in `packages/domain` and onward, story by story; the evidence column and `build_rules/oracle-coverage-notes.md` are deleted when the conversion ends.

Notes: `python` is not installed on this machine; use bash, sed, awk or the editor. A tool layer may halve backslashes in commands; test any sed that must match a literal backslash. The check script reports errors for duplicate IDs, missing parents, dangling references and malformed rows.
