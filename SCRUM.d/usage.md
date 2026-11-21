# Usage

The Product Owner's readings of the 5-hour session % and the 7-day weekly % (`/usage` or the status line), taken by the
Orchestrator at the start and end of each sprint (`SCRUM.d/README.md`, Or-15). The dashboard reads this file.

Estimate = what the Orchestrator said before the work. Before and after = the readings (session % / weekly %). Actual =
after minus before; a window reset in between makes the session actual unknown (`?`). A dash = never recorded.

| Sprint | Story or round | Date | Model | Estimate session % | Before s / w | After s / w | Actual session % | Notes |
|---|---|---|---|---|---|---|---|---|
| dashboard | rounds 1 and 2, with the process-rule work of the same conversation | Nov 20 | Sonnet 5.5 | – | 11 / 43 | 94 / 54 | 83 | No reading was taken at the sprint start, only when the Product Owner sent one mid-conversation (11 / 43); the 94 / 54 reading came at the stop of round 3; the conversation also covered the gap walk and the rule changes, so this is not the dashboard's cost alone |
| dashboard | round 3 (redesign, outline, plus buttons, collapse fix), stopped unfinished | Nov 20 | Sonnet 5.5 | – | 25 / 58 | 83 / 66 | 58 | Before-reading at 13:22; after-reading at 14:25 when the Product Owner reported 83 / 66 and the Orchestrator stopped the agents (the 70% line had been passed without a reading); 58 points of the 5-hour window and 8 of the week for an unfinished round, including the Orchestrator's own work in the conversation |
| dashboard | round 3 remainder, Review and your acceptance (planned) | Nov 20 | Sonnet 5.5 | 60 (45–80) | – | – | – | Estimate made at 14:50 from the old baseline rate (about 35 changed files at 1.3 session % per file, plus the Reviewer run and the Orchestrator's own work); weekly about 8 |

## Baseline from the old dashboard (low confidence)

Imported from the retired Python app's `build-costs.md`: builds with a measured session actual. It is a different task type and
different models (Sonnet 5 and 5.5), so use it only until this project has three finished pairs of its own (Or-15). Estimate and
actual are the session % of the 5-hour window.

| Build | Files, lines (+/−) | Items | Estimate session % | Actual session % | Notes |
|---|---|---|---|---|---|
| beta.31 (calendar items) | 30, +210/−76 | 14 | 50 | about 30 | extrapolated across a reset |
| beta.32 (fixes, settings, calendar, history, setup) | 41, +590/−178 | 17 | 65 | 64 | estimate almost exact |
| beta.33 (fixes, settings, calendar, theme) | 47, +421/−152 | 23 | 65 (55–75) | 15 raw, about 116 blended | the blended figure includes work around the build |
| rules and docs changes (6 rows) | docs only | 1 each | 1–3 | 2, 4, 12 (blended), 25 | the 25 included a dashboard rebuild |

Rate seen: about 1 to 1.6 session % per changed file in a code build (beta.31 1.0; beta.32 1.6). Round 3 of the new dashboard
cost 58 session % for at least 43 changed files, about 1.3 per file, which agrees. Rule of thumb until more data exists: a code
story costs about 1.3 session % per changed file, within plus or minus 30%; the estimate range is Or-15.b.
