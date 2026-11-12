# 2. Build

Command: **BUILD** `[F|f I|i R|r] [b m M]` (GO and EOF are aliases). Read when the Developer says BUILD. Claude first checks its model (0-overview.md, Conversations).

## The start-of-BUILD box

BUILD opens with one short rounded box (the style of the app's status boxes), two lines:
- **Model:** "Model: Sonnet 5.5" (green) when it is the model; "Model: Sonnet 5.5 not selected. (Optional)" (white/neutral,
  not amber — it's optional, not missing) otherwise. The Developer sets Medium effort (Claude can't see it) and switches
  models; Claude never does.
- **Usage:** "Usage: 11% / 47%" (green, the Developer's session % / weekly %) once a reading is given; "Usage: Missing"
  (amber) until then.
The repo is not part of the box; a handoff tells Claude to clone it when it is not on disk.

## Usage readings

Claude can't see the usage meters, so the Developer's readings are the only actual costs.
- **Before a BUILD:** the Developer gives the reading in the new conversation (always); unless the BUILD message or the conversation already gives a current reading, Claude asks for the
  current session % and weekly % (one short question) and waits. With none given, it says so and goes on, and the
  Dashboard marks that build's actual as unknown.
- **After a BUILD:** Claude's report ends by asking for the same two readings, and the next BUILD's "before" is not asked
  for again if it was given then.
- Claude records each build in build-costs.md (estimate session and weekly, model, size, readings) and on the
  Dashboard's cost graph, with its projection for each planned build (1-plan.md, point 5); the estimate comes from build-costs.md, How to predict.

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
- A page change meets ui_ux.md §5: keyboard, visible focus, labels, contrast and reduced motion, in light and dark
  and on a phone. Checks suite 44 can make are added in the same beta.
- A change to the page is compared before and after, pixel by pixel (`tests/tools/shots.py` before and after,
  then `tests/tools/pixdiff.py`): Claude looks only at the areas it reports, and every one is either the intended
  change or fixed. A change meant to leave the look alone (such as a split of the files) reports nothing.
- `pip-audit -r requirements.txt` finds nothing; anything it finds is fixed in that beta, or reported to the
  Developer.
- The release workflow's trivy scan of the image finds no fixable High or Critical vulnerability (it stops the
  beta before anything is published); the rest of its report is read and passed on in Claude's report.
- CHANGELOG.md has the beta's entry (its F, I and R, tidied); README.md matches what changed.
- The Developer's real data appears nowhere (0-overview.md, Ground rules).
- **One commit ships it** (0.2.8-beta.33): the image is built only when `VERSION` changes, so the commit that bumps
  `VERSION` must be the commit with all the code. A code commit pushed after it is never built (beta.33 shipped
  without most of its items that way). Run every test and fix first, bump `VERSION` last, and push once. If code
  must change after the bump, bump to the next beta. After pushing, check the workflow's run was for the HEAD commit
  (`gh run list --workflow=release.yml`) and say so in the report.

## Checkpoints (R20)

A build is a series of **checkpoint commits**, so progress is easy to resume.

- A checkpoint is one finished step that stands alone, sized by Claude's judgment, never leaving the app
  half-changed (no dead code, no half-moved functions, no failing test).
- Before it is committed: the suites that touch the changed code pass locally (the full suite is run by the Tests
  workflow on GitHub for each push, not locally); a new module has its own fast test (R18) and its dependency
  header (R19); no real data is in it.
- Its message names the build and step ("F58 2/10: models.py + test"). It is pushed at once, and the build's
  progress line on the Dashboard (done, next, left) is updated and republished.
- Its message's body (or, for a one-line checkpoint, a trailer) lists the files it touched, and names any new
  function or class — not every helper, just what another reader would look for to find the change. When one F,
  I or R is finished by more than one checkpoint, its Dashboard line (0-overview.md, The Dashboard) gathers this
  list across all of them, so the Dashboard shows what the code actually did, not only what was asked.
- Checkpoints don't change `VERSION`, so no image is built. The last one waits for a green Tests run on GitHub for
  its commit (the full suites, pip-audit), adds the CHANGELOG entry, bumps `VERSION` last ("One commit ships it",
  above) and records the cost.
- BUILD runs through as many checkpoints as it can without asking the Developer anything. It stops only for a
  decision that can't be undone and could go either way, or the usage limit. A usage limit can cut in mid-step;
  since a checkpoint is committed only when finished and green, that costs at most the step in progress.
- A red Tests run on GitHub doesn't stop the build: fixing it is the next checkpoint. Claude carries on with the
  next checkpoint while the previous one's run is in progress, unless the next depends on it. Never two local
  test runs at once (they share the suites' databases).
- For a risky build (the Google modules, anything that touches stored data or sign-in) the Reviewer reads each
  checkpoint's diff and Tests run when the Developer sends it REVIEW; it reads only and never changes code, and
  Claude checks everything it posts.
- BUILD said again continues from the progress line, in a new conversation if needed (the HANDOFF names it).

## Handing BUILD to another AI (R24)

Sometimes the Developer wants a different AI (ChatGPT, say) to build instead of Claude — asked for as
**BUILD (ChatGPT)** (or naming whichever AI; 0-overview.md, Commands). Unlike handing TEST to another AI
(3-test.md), this is real building: code is written, committed and pushed to the repo, under exactly the same
discipline as any build in this file — nothing is relaxed because another AI is doing it.

- **Never point it at the Dashboard link.** The Dashboard artifact is private to the Developer; another AI has
  no way to sign in as them, so a fetch of it returns a page shell with no real content (confirmed Nov 12, same
  failure mode seen handing TEST to ChatGPT: a 404 on what it called the Dashboard's "content API", falling back
  to inferring from the repo and old issue text).
- **Paste the content instead.** The handoff carries, as plain text, the actual Inputs Status items it's meant to
  build (or the relevant slice) — generated fresh from the live Dashboard, not a link to it.
- **Scope it.** Name the specific F/I/R items to build (e.g. "Build D: F65, I22, F47/I45 — not F24.1"), the same
  way a BUILD option (F, I or R) narrows Claude's own build.
- **Access.** The Developer gives the assigned AI whatever its role needs (push access to the repo to build;
  read/comment access to review) — there's no existing mechanism for granting this, so Claude asks the Developer
  how before using this handoff the first time.
- **Checkpoints, the before-publish checklist, the release gate and the Ground rules all apply exactly as they
  do to Claude's own build** (Checkpoints, above; R18–R23; the Developer's real data appears nowhere).
- **For a risky build** (the Google modules, anything touching stored data or sign-in), the Reviewer for that
  build's checkpoints is whichever AI isn't building it — if ChatGPT builds, Claude reads each checkpoint's diff
  and Tests run when the Developer sends it REVIEW, read-only, same as Checkpoints above.
- **The Dashboard stays Claude's to keep** (0-overview.md, The Dashboard): another AI can't publish to it, so
  Claude updates it from the repo's own history (checkpoint commits, CHANGELOG, VERSION) the next time it's asked
  for DASH, PLAN or REVIEW — not assumed finished until checked against the actual commits.
- The other AI reports back in plain text what it did, same shape as After, below.

## After

Commit and push; the release workflow tags `v<version>` and publishes the `beta` image. Claude reports what came
out, the readings it took, anything still waiting, and how many lines have changed since the `reviewed` branch (a
prompt for a REVIEW, which starts only when the Developer says it: 4-review.md, Chunks).

HANDOFF (step 1.1) is given only when the Developer asks for it, at any time — by name, or by saying they're
starting a new conversation. BUILD's own report does not end with one unprompted; the Developer asks separately.

When it is given, it is Claude's last message in the conversation (R17: one message, with no separate "New
conversation…" line before it): the message to paste as the new conversation's first, in one block. It names the
repo (Uuugh/CalendarStream) and says it is not on disk and must be cloned from GitHub (add_repo) before `tests/tools/setup.sh` and the version now current (an R-only build keeps it); the Dashboard's link; "Read
CLAUDE.md, run tests/tools/setup.sh, read the Dashboard"; the next command from "Waiting on"; and anything in
flight (a review turn, a release still running, a fix waiting for something from the Developer). Never the
Developer's real data.
