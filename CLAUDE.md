# CLAUDE.md

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
  - Documentation-only changes (README, CLAUDE.md) don't change the version.
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
- Deploy/deploy = Start Deployment Instructions
- STOP/stop/s/WAIT/wait/w = Stop all work. No commit or push. No time / credits / tokens should be spent until the Developer says to continue.

## Deployment Instructions

- Only start a Deploy if enough credits remain to complete it (steps a–f, including likely fix rounds).
  - Claude can't see the credit balance, so before step a it estimates the Deploy's cost (compared with a typical beta) and asks the Developer to confirm enough credits remain. No confirmation, no Deploy.
  - If credits run low during a Deploy, finish or undo the current step (never leave it half done), commit and push nothing unfinished, and report where it stopped and what remains.
- At the start of a step, provide an estimated build time for "Total Time Remaining:" and "Time Remaining in &lt;Step Name&gt;:"
- If a step produces a finding (a # item or a Developer F/I), then return to step a until the code can flow to the end without a finding.
  - Only changes to code behavior restart at a; comment, naming and docs fixes are made and re-checked in place.
  - Each round of fixes is published as the next beta (like a plain "EOF", e.g. beta.4 → beta.5), and the Developer tests that beta in step c. The release (f) is made from the last beta.
  - Number review findings #1, #2… within the deploy, for the CHANGELOG.
- Notify the Developer if stuck on a step for more than 5 minutes, or in a loop for more than 10 minutes.
- Steps:

**a. Programming Review:** A Reviewer performs a code review.
- The Reviewer only receives the repo and the diff since the last stable release, not Claude's notes or conversation.
- Design: Is the code well-designed and appropriate for CalendarStream, a self-hosted Docker web app that may later become a standalone app? The app runs in a Linux container; the installer and Docker setup must work on Linux, macOS (Docker Desktop) and Windows (WSL). New code shouldn't add needless ties to Docker, Postgres or the web page: keep the calendar logic separate from where it runs and how it's shown.
- Functionality: Does the code behave as the author likely intended? Is the way the code behaves good for its users?
- Complexity: Could the code be made simpler? Would another programmer be able to easily understand and use this code when they come across it in the future?
- Tests: Does the code have correct and well-designed automated tests?
- Naming: Did the author choose clear names for variables, classes, methods, etc.?
- Comments: Are the comments clear and useful?
- Style: Does the code follow our style guides? PEP 8 and PEP 257 (Python), Google HTML/CSS and JavaScript style guides; ruff runs automatically.
- Documentation: Did the author also update relevant documentation?

**b. Security Review:** A Reviewer performs a code review.
- OWASP ASVS and Top 10; automated scans: pip-audit, bandit, trivy
- The Reviewer only receives the repo and the diff since the last latest, not main agents notes or conversation.

**c. Testing**
- Developer validates and approves.

**d. Translations:**
- Update all translations.
- Translations are never updated between deployments, even if some languages show English words in beta.
- Run the automatic translation test (skipped before, since betas aren't translated)

**e. Documentation**
- Version history (CHANGELOG.md, also used for the GitHub release notes)
- Screenshots: if the page changed significantly, replace the README screenshots using the made-up demo schedule, never the Developer's real one.

**f. Release (tagged latest), only after Developer approval in step c**
- Drop the last beta's suffix (x.y.z-beta.N → x.y.z). The release is the approved code plus the translations (d) and documentation (e).
- Tag vx.y.z, publish the image as :x.y.z and :latest, and set STABLE to x.y.z.
- CHANGELOG.md: gather the version's beta entries under one x.y.z heading, with a sub-heading per beta (beta.1, beta.2…), since F/I/R numbers restart at each EOF. This becomes the notes of its GitHub Release, published as Latest (not a pre-release).
- Report the release and the next EOF's version (x.y.(z+1)-beta.1).

## Roadmap (Subject to change)

0.2 = more sources and destinations

0.3 Backups

0.4 Additional Users
- Login via authentik.
- Each new login is a new user. The new user will need to add their own calendars unless a calendar has been shared with them
- Add share calendar with other users toggle to the top right of status and setup
- build the login on OpenID Connect in general, with authentik as the tested provider, so Authelia, Keycloak or Google logins also work.
- keep the built-in login as a fallback admin, so a broken authentik doesn't lock you out. And today's data should belong to whoever logs in first.
- put the share switch on each source and destination rather than one page-wide toggle. Sharing is per calendar, and you may want to share your schedule but not a personal feed.

0.5 Notifications
- triggers  are defined in rules say the may be resued
  - trip added, changed or dropped
  - failed sync, a sign-in rejected
  - settings allows options for (Apprise library): email, ntfy, Pushover, Telegram and others

0.6 Theming
