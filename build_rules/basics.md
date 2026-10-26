# Basics: words, inputs and versions

Always loaded (imported by CLAUDE.md). These words have these meanings in every request.

## Definitions

- Developer = the human user
- Claude = the AI working on the project in the current session
- Author = whoever wrote the code being reviewed
- Reviewer = a separate AI agent running a review step
- F#/f# = Feature Request
- I#/i# = Issue
- R#/r# = README file / Documentation
- ? = Developer has a question for Claude. This is not an input; the Developer wants Claude's suggestion. It might then become an input
- Sub-items are numbered F1.1, F1.2… Numbers start again with each EOF.
- Software versioning (semver): Major.minor.patch[-beta.N]
  - Betas carry a suffix: 0.2.7-beta.1, 0.2.7-beta.2, …
  - Deploy releases the last beta without its suffix (0.2.7-beta.4 → 0.2.7) and tags it latest.
  - Documentation-only changes (README, CLAUDE.md, AGENTS.md, build_rules/) don't change the version.
- EOF = Begin processing inputs, and set the new version (each one tagged beta):
  - Tidy Developer F/I/R before they're published in CHANGELOG.md: spelling, grammar and numbering.
  - Correct Developer dictation slips (e.g. "Texas" → "text is", "safe" → "Save", "subscription" → "subsection") and advise Developer which reading Claude took.
  - "EOF" next beta of the same version (0.2.7-beta.1 → 0.2.7-beta.2);
    after a Deploy, starts the next patch (0.2.7 → 0.2.8-beta.1).
  - "EOF b" starts the next patch (0.2.7-beta.3 → 0.2.8-beta.1).
  - "EOF m" starts the next minor (0.2.8-beta.2 → 0.3.0-beta.1).
    Claude confirms the new version with the Developer before proceeding.
  - "EOF M" starts the next major (0.3.1-beta.1 → 1.0.0-beta.1).
    Claude confirms the new version with the Developer before proceeding.
  - Before a beta is published (every EOF):
    - `tests/run.sh` passes (suite 17, translations, waits for Deploy step d). New behavior gets tests in a new suite (the next number).
    - Anything on the page that changed follows build_rules/theme.md (look and interaction), checked
      by the theme suite (suite 44): each Clarification has a check there, added in the same beta.
    - `pip-audit -r requirements.txt` finds nothing; anything it finds is fixed in that beta, or reported to the Developer.
- Deploy/deploy = Start Deployment Instructions (build_rules/deploy.md)
- STOP/stop/s/WAIT/wait/w = Stop all work. No commit or push. No time / credits / tokens should be spent until the Developer says to continue.

## Ground rules

- Pull before editing, and keep the Developer's own edits.
- Never push half-finished or broken work.
- Never modify CCS+ (United's system): CalendarStream only reads it.
- Downloads identify themselves honestly: never disguise a client to get past United's bot protection.
- The Developer's real schedule (Calendar.ics), username and Google client secret never go into the repo, the tests, screenshots or messages. Use the made-up demo schedule (`tests/data/Demo.ics`, Username U123456).
