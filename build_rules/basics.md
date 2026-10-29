# Basics: words, inputs and versions

Always loaded (imported by CLAUDE.md). These words have these meanings in every request.

## Definitions

- Developer = the human user
- Claude = the AI working on the project in the current session
- Author = whoever wrote the code being reviewed
- Reviewer = a separate AI, from another vendor than Claude (ChatGPT for now), running a review (build_rules/review.md)
- F#/f# = Feature Request
- I#/i# = Issue
- R#/r# = README file / Documentation
- ? = Developer has a question for Claude. This is not an input; the Developer wants Claude's suggestion. It might then become an input
- Sub-items are numbered F1.1, F1.2… Numbers start again with each GO.
- Software versioning (semver): Major.minor.patch[-beta.N]
  - Betas carry a suffix: 0.2.7-beta.1, 0.2.7-beta.2, …
  - Deploy releases the last beta without its suffix (0.2.7-beta.4 → 0.2.7) and tags it latest.
  - Documentation-only changes (README, CLAUDE.md, AGENTS.md, build_rules/) don't change the version.
- GO = Begin processing inputs, and set the new version (each one tagged beta). GO counts only in capitals, and GO
  with its options ends the message ("1 build. GO", "1 build. GO b FI"), so a "go" in ordinary words or dictation
  never starts a build. EOF is an alias that still works the same (EOF, EOF b, EOF m, EOF M).
  - Before any GO, Claude lists every waiting F, I and R, the ones this GO leaves too, so the Developer's
    messages keep the record if a session ends.
  - GO works on every waiting input. GO with F, I and/or R works on exactly those kinds (GO R: documentation and
    rules only); the rest stay listed and waiting. The options go in any order, with or without spaces, F/I/R in
    either case: GO b FI = GO FI b = GO F I b = GO b F I. (Only b, m and M choose the version, and m ≠ M.)
  - Only R (documentation): the version doesn't change.
  - Tidy Developer F/I/R before they're published in CHANGELOG.md: spelling, grammar and numbering.
  - Correct Developer dictation slips (e.g. "Texas" → "text is", "safe" → "Save", "subscription" → "subsection") and advise Developer which reading Claude took.
  - "GO" next beta of the same version (0.2.7-beta.1 → 0.2.7-beta.2);
    after a Deploy, starts the next patch (0.2.7 → 0.2.8-beta.1).
  - "GO b" starts the next patch (0.2.7-beta.3 → 0.2.8-beta.1).
  - "GO m" starts the next minor (0.2.8-beta.2 → 0.3.0-beta.1).
    Claude confirms the new version with the Developer before proceeding.
  - "GO M" starts the next major (0.3.1-beta.1 → 1.0.0-beta.1).
    Claude confirms the new version with the Developer before proceeding.
  - Before a beta is published (every GO):
    - `tests/run.sh` passes (suite 17, translations, waits for Deploy step d). New behavior gets tests in a new suite (the next number).
    - Anything on the page that changed follows build_rules/theme.md (look and interaction), checked
      by the theme suite (suite 44): each Clarification has a check there, added in the same beta.
    - `pip-audit -r requirements.txt` finds nothing; anything it finds is fixed in that beta, or reported to the Developer.
- Deploy/deploy = Start Deployment Instructions (build_rules/deploy.md)
- REVIEW = A review by the Reviewer (build_rules/review.md): REVIEW runs both (a Programming, b Security), REVIEW a
  or REVIEW b one. With a review issue open, REVIEW to Claude means "your turn: read the issue now"; the
  Developer sends REVIEW to the Reviewer (ChatGPT) to start its turn. Capitals only, ending the message, like GO.
- APPROVE = The Developer's sign-off wherever the rules ask for it: a rules change (Claude then moves the
  `review-rules` tag, build_rules/review.md), Deploy step c. Capitals only, ending the message, like GO.
- STOP/stop/s/WAIT/wait/w = Stop all work. No commit or push. No time / credits / tokens should be spent until the Developer says to continue.

## Ground rules

- Pull before editing, and keep the Developer's own edits.
- Never push half-finished or broken work.
- Never modify CCS+ (United's system): CalendarStream only reads it.
- Downloads identify themselves honestly: never disguise a client to get past United's bot protection.
- The Developer's real schedule (Calendar.ics), username and Google client secret never go into the repo, the tests, screenshots or messages. Use the made-up demo schedule (`tests/data/Demo.ics`, Username U123456).
