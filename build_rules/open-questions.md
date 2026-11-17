# Open questions for the Developer

Answer when convenient; none blocks the work already under way. Claude keeps going on everything that does not
depend on an answer. Mark an answer by editing the line or telling Claude. Started Nov 17.

## Q-M: merge delays (the real bottleneck)

Only the Developer can merge, and each inventory PR waited on that. Claude was refused when it tried to merge
unattended. Options:
1. **Auto-merge rule in GitHub (recommended).** A small GitHub Action merges a PR from `chatgpt/inventory-*` when the
   `suites` check is green, it changes only `requirements/inventory/`, and a Claude review comment exists. You keep control
   of the rule; nobody merges anything else.
2. Developer merges by hand (today): safe but waits whenever you are away.
3. Authorize Claude to merge those PRs, in writing in `2-build.md` (needs your decision; the safety layer may still ask).
Answer: ___

## Q-R: rules requirements (requirements/drafts/rules.md)

- **Q-R1** Layout measurements (pixels, offsets, opacity) in the inventory: leave to `theme.md` and the UI tests, not
  requirements? (Claude's default: yes.)
- **Q-R2** RUL-35 (migration of legacy tag colors): keep as a requirement for the Dart server, or drop it, if every
  install has already migrated? (Default: keep until you confirm no old data remains.)
- **Q-R3** RUL-42 (rule dialog fits a 390 px phone): keep? The Flutter client will have its own phone layout (Claude's
  default: keep, rewritten as "usable on a phone-width window").
- **Q-R4** Approve the 41 draft rows as `verified` in `requirements/rules.md`? Claude moves them after you say yes.

## Q-S: later steps

- **Q-S1** The inventory has about 1,700 rows. Claude drafts one feature per file under `requirements/drafts/`, in port
  order (rules, event_templates, events, calendar, sources, feeds, history, google, settings, account). Is that the order
  you want to review them in?
- **Q-S2** Suite 82 and the paused test overhaul (uncommitted in your working tree): finish, commit, or discard before the
  Python suites are frozen as the oracle?
- **Q-S3** Taichi / Ollama: address, local or hosted model, and whether Postgres is available there (needed before
  Claude can offload checks to it).
- **Q-S4** Dart toolchain: the Dart/Flutter SDK is not installed in this shell. Should Claude install it, or will you?
- **Q-S5** Baseline: Claude will run the full Python suites once in CI before freezing them. OK to push a branch for
  that?
