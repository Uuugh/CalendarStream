# Handoff: how we work and where everything is (written Nov 17-18 2026)

Read this first in a new conversation. Then `build_rules/layer-map.md` (the plan and the dated decisions), `requirements/README.md` and `build_rules/open-questions.md`.

## The rules of our conversation

1. **The Developer is one person, often dictating by voice.** Garbled text happens; when unclear, ask in plain words, one question at a time. Never guess a big decision.
2. **Questions go in two places:** asked in chat, one at a time, in plain words (what it is, my recommendation, a short answer); and filed in `build_rules/open-questions.md` with an `Answer:` line (the Developer may type the answer there). Remove a question once it is acted on and record the decision in `build_rules/layer-map.md`. Before asking, check whether a common rule already decides it (do not repeat a decision), and whether the code answers it (read the code).
3. **The Developer edits the files directly.** Always check `git status` and `git diff` for uncommitted changes in `requirements/` and `build_rules/` before editing; read them as instructions; never overwrite; commit them with your changes. **A blank status means the Developer agreed.** `proposed` and `planned` mean not yet agreed. Never reuse an ID.
4. **Requirements say what a feature does for the user.** One file per feature in `requirements/<feature>.md`; behavior shared by several features is written once in `requirements/common.md` (TIM time, UI components, CAP capabilities, DEF defaults and limits) and referenced. **No exceptions**: fix or add the general rule instead. Look and layout go to `build_rules/theme.md`. No pixel values (event lines, theme sizes). No web-page mechanics (UI-13: changes show at once). No Python-test wording ("sampled", "fixture"). No "is refused" rule for a control that cannot produce a bad value.
5. **Decisions that shaped the rules** (all in layer-map.md): UTC storage and per-event zones; Local zone from the device; the database overrides env (DEP-28); Site Admin settings are shared, User settings are per device (one user for now); layout zones left/center/right, stack then scale then clip (triple dot) or scroll (UI-14); anchors for badges (UI-15); one resize bar (UI-16); UI components separate from features (UI-17).
6. **Commit and push often.** Commit messages end with the Co-Authored-By line from the session. **Never merge pull requests by hand:** an Action merges ChatGPT's PRs after a clean `**Claude review, PR #N**` comment (run `gh workflow run "Inventory auto-merge"` after the comment; the schedule is unreliable).
7. **Style:** a timestamp line `---------- HHMM EST ----------` (EST = UTC-5, from `date -u -d '-5 hours' +%H%M`) at the top of the first reply after a break; commands in their own code block with nothing after them; be active, not passive; say plainly when something was not checked.
8. **Freeze:** no new features until the Python-to-Dart port is complete; the Python app (`app/`, `tests/`) is the running app and the oracle until step 5.
9. **Never put the Developer's real schedule, username or Google secret anywhere;** the Dashboard artifact is private; do not link it to other AIs.

## Where things are

- Plan, steps, decisions: `build_rules/layer-map.md` (steps 1 to 7). Processes: `build_rules/0-overview.md` to `5-deploy.md`.
- Requirements: `requirements/<feature>.md` (17 files; index in `requirements/README.md`). The inventory of the Python suites (evidence keys Sxx-NN): `requirements/inventory/`.
- Issues: GitHub issues (label `issue`, `feature:<name>`, titles "I22: ..."). The Dashboard is rebuilt after the port (DIA-02 to DIA-04).
- ChatGPT's queue and rules: `build_rules/gpt-tasks.md` (Task E, done; its `gaps_<feature>.md` files were folded in and deleted; branch `chatgpt/drafts-gaps-<feature>`).
- Dart code: `packages/domain` (Event, rule schema, text matching, regex legality). SDK: `C:\Users\rfrie\Development\sdks\flutter\bin\dart`. Parked test overhaul: branch `paused/test-parallel`.
- Memory notes for Claude: `C:\Users\rfrie\.claude\projects\C--Users-rfrie-Development-Projects-CalendarStream\memory\`.

## State and next steps

1. ChatGPT finishes Task E (feeds, history, rules, event_templates, diagnostics, documentation, search, calendar_filter). Claude reviews each PR; the Action merges.
3. The Developer reviews each feature file in order (calendar is done): answer the questions, blank the status of agreed rows. Remaining questions are in `build_rules/open-questions.md`.
4. Port (step 4) in `packages/domain`: rule conditions (days, times, lengths, dates), validation, actions; then the new Dart database and the Python migration tool (DEP-14); then the server features and client. Steps 5 (retire Python), 6 (analyze parallel testing, input: the parked branch), 7 (the Dashboard as a live page).
5. Timers are session-only: re-create the check in a new conversation if wanted (it reads the Developer's edits, answers, and ChatGPT's PRs).

## State when the second conversation ended (Nov 18, about 0020 EST)

- The review check is no longer needed (Task E complete). ChatGPT's limit is 4 open PRs (gpt-tasks.md); it has no task left in Task E.
- Task E is COMPLETE (16 of 16 merged, Nov 18, 0020 EST). No review check is needed any more. Folded into the feature files and `requirements/drafts/` deleted (Nov 18). Next: the Developer reviews each feature file in order.
- Done this conversation: FED-08, FED-25, FED-27, FED-30 answered; ACC-04 and ACC-26 (nothing refused for strength; strength bar and hint only); new common rows UI-18 (strength bar with recommendation hint) and UI-19 (invalid entry identified at its field); settings.md deduplicated (retired IDs listed in it); SET-41 is the logo only.
- Duplication review DONE Nov 18 (Claude): merged and retired rows are listed at the end of each feature file ("Retired IDs"); new common rows UI-19 (invalid entry), UI-20 (nearest palette color), DEF-01 rows for the limits that were in features; HIS-33 (repeated failure recorded once). Left for the Developer: see open-questions.md (20 questions). Open points from the review: the stream name and stream token in feeds look like one field (FED-08, FED-09, FED-25, FED-27); SRC-80 vs FED-30 (does an upgrade add Local to every feed); RUL-22 says "within a second" but DEF-01 has 0.05 seconds; SHL-27 vs SET-06 (section state shared or per device). `python` is not installed on this machine; use sed or the editor for edits.
