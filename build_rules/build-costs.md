# Build costs

What each BUILD cost, to predict the next one. Claude can't see the usage meters, so **actual** comes only from the
Developer's readings (2-build.md, Usage readings): the session % and the weekly % before and after a BUILD.
Claude fills a row at the end of each BUILD, asks for the after-reading in its report, and fills the actual when it
arrives. The Dashboard's cost graph draws these rows, and, to their right, each build PLAN recommends (numbered by build); the two
meters under it carry a numbered mark where each planned build should end (the session meter starts again from 0 for a
build planned after the session reset).

Read by PLAN (1-plan.md, point 5) for its estimates and by BUILD (2-build.md) for its estimate and projection.

## Builds

Estimate = what Claude said before building. Before / after = the Developer's readings (session % / weekly %).
Actual = after − before (a session reset in between makes the session actual unknown, "?"). A dash = never recorded.

| Build | Date | Model | Inputs | Files, lines (+/−) | Estimate session % | Estimate weekly % | Before s / w | After s / w | Actual session % | Actual weekly % | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| beta.26 (Theme) | Nov 3 | – | – | – | 37 | – | – | – | 26 | – | Estimate 37, the Developer saw about 26 |
| beta.27 (3 Rules + installer) | Nov 4 | Sonnet 5.5 | 9 | 34, +610/−143 | 37 | – | – | – | ? | ? | |
| beta.28 (4 Sources) | Nov 4 | – | 9 | 56, +637/−138 | 37 | – | – | – | ? | ? | |
| beta.29 (5 Calendar) | Nov 5 | – | 8 | 37, +924/−192 | 41 | – | – | – | ? | ? | |
| R (cost tracking, no version) | Nov 5 | Sonnet 5.5 | 3 R | docs, rules, Dashboard | 8 | 2 | 8 / 28 | 24 / 30 (Nov 5, 10:50 PM; also covers the TEST and PLAN of the next conversation) | ? | ? | First row with a weekly estimate; the reading is not a clean after-reading, so the actual stays unknown |
| R (split marks on the Dashboard, no version) | Nov 5 | Sonnet 5.5 | 1 R | docs, rules, Dashboard | 5 | 1 | 24 / 30 | 28 / 31 | 4 | 1 | Estimated at build time; the after-reading also covers the R1 follow-ups in the chat; ratio 0.8 |
| R (session/week zones, no version) | Nov 6 | Sonnet 5 | 1 R | Dashboard only (this row) | 3 | 1 | 59 / 36 | 84 / 40 | 25 | 4 | R1 actually built this time (session and week meters split into per-period zones), plus the legend's dash pattern, gauge padding, filling the window, removing the cost card's scrollbar, the zone-divider gap, the Est./Actual color and dash scheme, the hollow/filled dot swap, R3 (model on hover, widened hit area), merging builds 7/8 into one, and a card-padding cut — all asked for live in chat; ratio 8.3 (session) — a long run of small follow-up asks stacked onto one BUILD R, so this ratio isn't representative of a typical R; see this row's notes for how it broke down over the conversation |

## How to predict

1. Start from the nearest finished build by size (inputs and changed lines; a build that changes the page costs more
   than a rules or docs build, because of the suites and the before/after pictures).
2. Multiply by the observed ratio (actual ÷ estimate). Until there are 3 pairs the ratio is 0.7 (the one pair so far),
   low confidence.
3. Give the estimate as a range (±20 %) and, once the Developer's before-reading is known, the projected after-reading:
   before + estimate. The weekly estimate is the session estimate × the observed weekly ÷ session ratio (not known
   yet; assume 0.25: a session is about a quarter of a week's allowance on this plan, to be corrected by the data).
4. After each BUILD, add the row, recompute the ratios here, and say in the report how far the last estimate was off.
5. Note the model (Sonnet, Opus…) and effort; costs are only compared within the same model.
| beta.31 (7 Calendar + carryover + F22 + R1) | Nov 6 | Sonnet 5 → 5.5 | 14 done, 6 deferred | 30, +210/−76 | 50 | 13 | 0 / 41 | 0 (new session) / 46 | ~30 (extrapolated) | 5 | Nov 6, 9:52 AM reading; the session reset in between, so the session actual is extrapolated from the weekly change at the observed ratio of about 6 session points per week point (b30 24/4, R3 25/4): 5 × 6 = about 30, range 25–31; estimate 50 / 13, so over by about 20 session points; R1's zones were already built in BUILD R |
| R (PLAN reads the Dashboard, no version) | Nov 6 | Sonnet 5.5 | 1 R | docs, rules, Dashboard | 3 | 1 | 11 / 47 | – | ? | ? | R4 and I11 to the roadmap; the before-reading is the one given at PLAN (11:17 AM); after-reading to be asked |
| R (start-of-BUILD box, handoff clone line, no version) | Nov 6 | Sonnet 5.5 | 2 R | docs, rules, Dashboard | 3 | 1 | 11 / 47 (last known; the Developer reports usage in the new conversation) | – | ? | ? | R5 and R6; after-reading to be asked |
| beta.32 (8 Fixes + Settings + Calendar + History + Setup) | Nov 6 | Sonnet 5 | 17 | 41, +590/−178 | 65 | 11 | 17 / 48 | 81 / 59 | 64 | 11 | Nov 6, 12:52 PM reading; estimate was 65/11, almost exact (64/11 actual); ratio 0.98 (session) / 1.0 (week) — the best estimate so far on this model |
| R (HANDOFF on request only, no version) | Nov 6 | Sonnet 5 | 1 R | docs, rules | 1 | 0 | 81 / 59 | 93 / 61 | 12 (blended) | 2 (blended) | R9; the 93/61 reading was taken at PLAN after R8/R9 and the Inputs-Status cleanup together (like beta.31's R1 row, this ratio isn't representative of R9 alone) |
| R (Dashboard updates after PLAN, before/after BUILD, no version) | Nov 6 | Sonnet 5 | 1 R | docs, rules, Dashboard | 1 | 0 | 81 / 59 | 93 / 61 | 12 (blended) | 2 (blended) | R8: 0-overview.md's Dashboard bullets say so explicitly; also added the "Inputs Status drops confirmed items entirely" rule, cleaned up Inputs Status (11 items removed), and fixed the stale "Every BUILD ends with it" HANDOFF tooltip; blended reading, see R9's row |
| R (Commands tooltips, no version) | Nov 6 | Sonnet 5 | 1 R | Dashboard only, no repo file | 1 | 0 | 93 / 61 | 95 / 61 | 2 | 0 | R10: every Commands-table (i) tooltip rewritten as a short bulleted list; Dashboard-only, no commit |
| beta.33 (9 Fixes + Settings + Calendar + Theme) | Nov 6 | Sonnet 5 | 23 | 47, +421/−152 | 65 (55–75 range) | 11 (9–13 range) | 7 / 63 | 22 / 83 | 15 raw / ~116 blended | 20 | 9:21 PM reading, blended across BUILD 9 + the post-build build-costs.md fix + review-rules troubleshooting (same week count); session reset mid-build so the raw 15 isn't comparable, extrapolated from the week delta (beta.32's own ~5.8:1 session:week ratio) instead; week (20) ran well past the estimate's top end (13) — PLAN's low-confidence flag for a 23-item mixed build was warranted; the F47 regression chain (12 suites) and the mandatory pixel-diff review were the two biggest unplanned costs |
| R (code structure rules R18, R19, no version) | Nov 7 | Sonnet 5.5 | 2 R | docs, rules (AGENTS.md) | 3 | 1 | 60 / 89 | – | ? | ? | Wording as shown on the Dashboard, plus the Developer's "Flutter is the model for structure"; after-reading: see the R20 row (one blended reading for both); the weekly meter was already at 89 % |
| R (checkpoints, R20, no version) | Nov 7 | Sonnet 5.5 | 1 R | docs, rules (2-build.md, 1-plan.md) | 2 | 0 | 60 / 89 | 63 / 90 (Nov 7, 12:13 AM; also covers R18/R19, the PLAN and the checkpoint discussion) | 3 (blended) | 1 (blended) | R20 with the Developer's additions: judgment sizing, red run doesn't stop the build, full suite on GitHub, Reviewer on risky checkpoints |
| F58 (Google modules, 10 checkpoints; beta.36) | Nov 7 | Sonnet 5.5 | 1 F + #9 2,3 | 9 code checkpoints + rules, +suites 68–75 | ? | ? | 63 / 90 | 0 / 92 (Nov 7, 6:30 AM; session had reset) | session: spans a reset, not measurable; week +2 | ? | Week reading only: the session was reset before this reading |
| F59 (Beta: Google Traffic) | Nov 7 | Sonnet 5 | 1 F | app/google/ (2 files) + routes + template + JS + CSS, +suites 68, 53, 76, fixes to 31/34/61 | ? | ? | 0 / 92 | 25 / 97 (Nov 7, 9:18 AM; session had reset) | session: spans a reset, not measurable; week +5 | 3 checkpoints + 2 fixes (R19 headers; a push before its Tests run, caught and rebuilt) |
| REVIEW of PR #13 (R18/R19 reorg) and PR #14 (theme/CSS), then merge (no version) | Nov 11 | Sonnet 5, then Fable 5.2 | 2 PRs | review only: 3 full local suite runs (PR #13 twice, both PRs combined), diffs, screenshots; merged both | ? | ? | 6 / 1 (5:25 PM) | 56 / 10 (6:22 PM, before the merge's Tests run finished) | 50 | 9 | No estimate was made. One full run was wasted (a second test started against the same database mid-run) and one was cut off by a 10-minute limit: about a third of this cost was avoidable |
| Build A (F47, F49, F63, I3, I22, F52/F57/I35, I38, F15.2, F58 checkpoint 10; F46/F48/F50 not reproducible; beta.40) | Nov 11–12 | Sonnet 5.5 | 8 built + 3 not-reproducible + F15 (1 of 9 parts) | 10 code checkpoints (incl. the GoogleSync composition rewrite) + CHANGELOG/VERSION | 30 | 5 | ? (no before-reading given this session) | 25 / 21 (Nov 12, session resets 6:00 AM, week resets Wed 5:00 PM) | ? | ? | Includes a self-corrected false alarm mid-build (a shallow clone misread as a rewound `main` — see the PR #13/#14 history check in the chat) and a Postgres-instance mixup (wrong default-port cluster vs. the dedicated test one) that cost time but no commits; no before-reading, so actual is unknown (dash) |
