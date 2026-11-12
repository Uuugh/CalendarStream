# 5. Deploy

Command: **DEPLOY**, twice: the first prepares the release and asks the Developer to test it; the second
releases it. Read when the Developer says DEPLOY.

## Before starting

- Only start a Deploy if enough credits remain to finish it, likely fix rounds included. Claude can't see the
  balance, so it estimates the Deploy's cost (compared with a typical beta) and asks the Developer to confirm.
  No confirmation, no Deploy.
- If credits run low during a Deploy, finish or undo the current part (never leave it half done), push nothing
  unfinished, and report where it stopped and what remains.
- Each part starts with an estimate: "Total time remaining:" and "Time remaining in <part>:". Claude tells the
  Developer if stuck on a part for more than 5 minutes, or in a loop for more than 10.

## The first DEPLOY: prepare

1. **Review the whole app** (4-review.md): the Developer passes the turns with REVIEW. Fixes go out as betas
   (like a plain BUILD, e.g. beta.4 → beta.5); comment, naming and docs fixes are made in place. Findings are
   numbered #1, #2… for the CHANGELOG.
2. **Translations:** update every language, then run the translation test (`tests/run.sh 17`). Translations are
   only ever updated here, even if betas show some English words.
   A translation too long for its place is abbreviated ("Sync" for "synchronisation"), and only then; a word that fits
   stays in full. The longest Status/Action words are checked against the 132 px button, and the Cancel | Save
   words ("Abbrechen", "Speichern", "Enregistrer") against their 65 px halves.
3. **Documentation:** CHANGELOG.md (also the GitHub release notes); the README screenshots if the page changed a
   lot (the made-up demo schedule, never the Developer's real one). (0.2.8-beta.33, R7: the Theme Rules pictures
   are no longer redrawn here or anywhere else - they stay as they are.)
4. Publish all that as the last beta, the **release candidate**, and ask the Developer to test it (with TEST, if
   they'd like Claude to follow along).

An F or I from the Developer's testing is fixed as the next beta and goes back to 1 (a review of just that
change), then 4.

## The second DEPLOY: release

The release is exactly the beta the Developer tested — meaning the same source, not the same image bytes.
(Decided, PR #15 BR02: dropping the suffix is itself a VERSION change, so `release.yml`'s `beta` job builds and
scans a fresh image for it, from a commit that differs from the tested beta only in that one-line VERSION edit
— it does not reuse or re-tag the exact image the Developer ran. "Exactly" is a same-source, same-behavior
promise, never a same-digest one. Every platform actually published is scanned before this image is pushed,
the same as any other beta — see `release.yml`, `beta`, BR01/BR02.)
- Drop its suffix (x.y.z-beta.N → x.y.z); tag `vx.y.z`; publish the image as `:x.y.z` and `:latest`; set STABLE
  to x.y.z.
- CHANGELOG.md: the version's beta entries under one x.y.z heading, a sub-heading per beta (F, I and R numbers
  restart at each BUILD). It becomes the notes of its GitHub Release, published as Latest (not a pre-release).
- Report the release and the next BUILD's version (x.y.(z+1)-beta.1).
