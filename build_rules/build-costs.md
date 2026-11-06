# Build costs

What each BUILD cost, to predict the next one. Claude can't see the usage meters, so **actual** comes only from the
Developer's readings (2-build.md, Usage readings): the session % and the weekly % before and after a BUILD.
Claude fills a row at the end of each BUILD, asks for the after-reading in its report, and fills the actual when it
arrives. The Dashboard's cost graph draws these rows.

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
| R (cost tracking, no version) | Nov 5 | Sonnet 5.5 | 3 R | docs, rules, Dashboard | 8 | 2 | 8 / 28 | ? / ? | ? | ? | First row with a weekly estimate |

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
