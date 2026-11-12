# 3. Test

Command: **TEST**. Optional, after a BUILD. Read when the Developer says TEST.

TEST is a partnership: the Developer tries the beta in a browser and Claude follows along, so problems are
found and talked through together. (REVIEW is the other kind of check, done without the Developer: the two
agents take turns, and the Developer joins only to decide.)

## How it runs

- The Developer tests a **demo copy**: a second CalendarStream on their computer, on the beta, with the made-up
  demo schedule (Calendars › United Airlines CCS+ › Manual Upload of `tests/data/Demo.ics`). Claude gives the setup commands the first time.
- The Developer opens it in a browser Claude can reach: the Claude desktop app's built-in browser, or Claude in
  Chrome. (This chat must be open in the desktop app on that computer.)
- The first TEST starts it: Claude finds the tab and says what it can see.
- Each TEST after that means "look now": Claude takes a screenshot of the tab and reads its console errors and
  network requests, says what it sees, and asks what the Developer expected when it isn't clear.
- Claude never clicks or types in the Developer's tab unless asked to.
- Problems found become I items, each with the steps to reproduce and what was expected. Claude reproduces them
  on the demo copy before fixing; the fixes come with the next BUILD.
- The test ends when the Developer says what passed, or gives the next command.

## The Developer's data

The demo copy keeps the real schedule, username and Google client out of what Claude sees (0-overview.md,
Ground rules). If the Developer ever tests the live CalendarStream instead, Claude copies nothing from it into
an issue, a test, a commit or a message, and reproduces problems with the demo schedule.

## Handing TEST to another AI

Sometimes the Developer wants a different AI (ChatGPT, say) to test instead of testing together — asked for as
**HANDOFF FOR CHATGPT TEST** (or naming whichever AI). This is not the REVIEW flow: no GitHub issues or comments,
nothing merged, pushed or deployed from it, Rich has final say.

- **Never point it at the Dashboard link.** The Dashboard artifact is private to the Developer; another AI has no
  way to sign in as them, so a fetch of it returns a page shell with no real content (confirmed Nov 12: a ChatGPT
  TEST pass got a 404 on what it called the Dashboard's "content API" and fell back to inferring what's finished
  from the repo and old GitHub issue text — stale and incomplete next to the actual Inputs Status).
- **Paste the content instead.** The handoff message itself carries, as plain text, the actual current Inputs
  Status items it's meant to test (or the relevant slice of them) — generated fresh from the live Dashboard, not a
  link to it.
- **Scope it.** Name the specific F/I/R items to test rather than "test everything claimed finished" — a vague
  scope is exactly what produces thin, inferred coverage.
- **Ask for a plain-text report back**, not GitHub issues or comments (this isn't REVIEW).
- Findings that come back are recorded into Inputs Status as new, un-built items (dashboard.md, "New inputs are
  only recorded until PLAN or BUILD") — Claude does not build from them on its own, and notes where a finding only
  confirms something already built versus resolves an open Bad report.
