# 2. Build

Command: **BUILD** `[F|f I|i R|r] [b m M]` (GO and EOF are aliases). Read when the Developer says BUILD.

## What BUILD builds

- **BUILD**: every waiting input. **BUILD** with F, I and/or R: exactly those kinds; the rest stay waiting.
- Options go in any order, with or without spaces: BUILD b FI = BUILD FI b = BUILD F I b = BUILD b F I. Only b, m and M
  choose the version, and m ≠ M.
- **R only: no new version; the new rules take effect at the next REVIEW.** Every BUILD puts its R changes into
  effect: Claude moves the `review-rules` branch to that commit (4-review.md).

## Versions (semver: Major.minor.patch[-beta.N])

| Command | Version |
|---|---|
| BUILD | the next beta of the same version (0.2.7-beta.1 → 0.2.7-beta.2); after a Deploy, the next patch (0.2.7 → 0.2.8-beta.1) |
| BUILD b | the next patch (0.2.7-beta.3 → 0.2.8-beta.1) |
| BUILD m | the next minor (0.2.8-beta.2 → 0.3.0-beta.1); Claude confirms the version first |
| BUILD M | the next major (0.3.1-beta.1 → 1.0.0-beta.1); Claude confirms the version first |

Documentation-only changes (README, CLAUDE.md, AGENTS.md, build_rules/) don't change the version.

## Before a beta is published

- `tests/run.sh` passes (suite 17, translations, waits for the Deploy). New behavior gets tests in a new suite
  (the next number).
- Anything on the page that changed follows theme.md (look and interaction), checked by the theme suite
  (suite 44): each Clarification has a check there, added in the same beta.
- `pip-audit -r requirements.txt` finds nothing; anything it finds is fixed in that beta, or reported to the
  Developer.
- The release workflow's trivy scan of the image finds no fixable High or Critical vulnerability (it stops the
  beta before anything is published); the rest of its report is read and passed on in Claude's report.
- CHANGELOG.md has the beta's entry (its F, I and R, tidied); README.md matches what changed.
- The Developer's real data appears nowhere (0-overview.md, Ground rules).

## After

Commit and push; the release workflow tags `v<version>` and publishes the `beta` image. Claude reports what came
out, the readings it took, and anything still waiting.

Then the handoff, as Claude's last two messages in the conversation:

1. "New conversation CalendarStream v<version>": the version now current (an R-only build keeps it).
2. The message to paste as the new conversation's first, in one block: the repo (Uuugh/CalendarStream) and
   version; the Dashboard's link; "Read CLAUDE.md, run tests/tools/setup.sh, read the Dashboard"; the next
   command from "Waiting on"; and anything in flight (a review turn, a release still running, a fix waiting for
   something from the Developer). Never the Developer's real data.
