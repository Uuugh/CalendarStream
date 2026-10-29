# Deploy

Read when the Developer says Deploy. Steps a and b are a REVIEW (build_rules/review.md).

## Before starting

- Only start a Deploy if enough credits remain to complete it (steps a–f, including likely fix rounds).
  - Claude can't see the credit balance, so before step a it estimates the Deploy's cost (compared with a typical beta) and asks the Developer to confirm enough credits remain. No confirmation, no Deploy.
  - If credits run low during a Deploy, finish or undo the current step (never leave it half done), commit and push nothing unfinished, and report where it stopped and what remains.

## How the steps run

- At the start of a step, provide an estimated build time for "Total Time Remaining:" and "Time Remaining in &lt;Step Name&gt;:"
- Reviews (a, b) run once each, as build_rules/review.md says: the Reviewer's findings, Claude's reply, the
  Reviewer's answer, then the Developer's vote on anything still disputed. They don't restart.
  - Accepted findings and the Developer's votes are fixed; a change of code behavior is published as the next beta (like a plain "GO", e.g. beta.4 → beta.5), and the Developer tests that beta in step c. Comment, naming and docs fixes are made in place. The release (f) is made from the last beta.
  - A Developer F/I in step c is fixed as the next beta and returns to step a.
  - Number review findings #1, #2… within the deploy, for the CHANGELOG.
- Notify the Developer if stuck on a step for more than 5 minutes, or in a loop for more than 10 minutes.

## Steps

**a. Programming Review:** REVIEW a: the Reviewer reviews the code in a review issue, following build_rules/review.md (a. Programming Review).
- The Reviewer only receives the repo and the diff since the last stable release, not Claude's notes or conversation.
- `tests/run.sh` must pass; the Reviewer reads the suites that cover the diff.

**b. Security Review:** REVIEW b: the Reviewer reviews the code in a review issue, following build_rules/review.md (b. Security Review).
- The Reviewer only receives the repo and the diff since the last stable release, not Claude's notes or conversation.
- Claude runs all three scans and puts their results in the issue's first post: `pip-audit -r requirements.txt`, `bandit -r app`, and `trivy image` on the beta's image (`ghcr.io/uuugh/calendarstream:beta`).

**c. Testing**
- Developer validates and approves (APPROVE).

**d. Translations:**
- Update all translations.
- Translations are never updated between deployments, even if some languages show English words in beta.
- Run the automatic translation test (`tests/run.sh 17`; skipped before, since betas aren't translated).

**e. Documentation**
- Version history (CHANGELOG.md, also used for the GitHub release notes)
- Screenshots: if the page changed significantly, replace the README screenshots using the made-up demo schedule, never the Developer's real one.
- If the theme changed, redraw the CalendarStream Theme Rules picture (build_rules/theme.md).

**f. Release (tagged latest), only after Developer approval in step c**
- Drop the last beta's suffix (x.y.z-beta.N → x.y.z). The release is the approved code plus the translations (d) and documentation (e).
- Tag vx.y.z, publish the image as :x.y.z and :latest, and set STABLE to x.y.z.
- CHANGELOG.md: gather the version's beta entries under one x.y.z heading, with a sub-heading per beta (beta.1, beta.2…), since F/I/R numbers restart at each GO. This becomes the notes of its GitHub Release, published as Latest (not a pre-release).
- Report the release and the next GO's version (x.y.(z+1)-beta.1).
