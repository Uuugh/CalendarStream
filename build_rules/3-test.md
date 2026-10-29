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
