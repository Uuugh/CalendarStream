# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in
layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file
(or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-S: later steps

- **Q-S1** The inventory has about 1,700 rows. Claude drafts one feature at a time in port order (rules done; next
  event_templates, events, calendar, sources, feeds, history, google, settings, account) and asks you to approve each.
  Is that the order you want?
  Answer:
- **Q-S2** Suite 82 and the paused test overhaul (uncommitted in your working tree): finish, commit, or discard before
  the Python suites are frozen as the oracle?
  Answer:
- **Q-S3** Taichi / Ollama: address, local or hosted model, and whether Postgres is available there (needed before
  Claude can offload checks to it).
  Answer:
- **Q-S4** Dart toolchain: the Dart/Flutter SDK is not installed in this shell. Should Claude install it, or will you?
  Answer:
- **Q-S5** Baseline: Claude will run the full Python suites once in CI before freezing them. OK to push a branch for
  that?
  Answer:
