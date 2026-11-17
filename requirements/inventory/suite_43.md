# Suite 43: Repeated check-update feedback

Source: [`tests/suite_43.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8102; fake checker persists configurable current/newer/error answers; installed version patched. Chromium 1300×900; loops patched; repeated fixed waits sample status transitions. No real GitHub check.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S43-01 | settings | Updates markup has an idle syncnow/checknow control and includes Checking and failed-check feedback strings. | [L29](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L29) |
| S43-02 | settings | At rest, the sampled Check now button height is below 26px. | [L39](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L39) |
| S43-03 | settings | On each of two clicks, the button has syncing state, Checking text and height exceeding status-box height minus 10px. | [L43](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L43) |
| S43-04 | settings | Each click subsequently reaches done state with Up to date text. | [L46](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L46) |
| S43-05 | settings | After each rest delay, fake-check count equals click count, button state is idle and the status shows running version plus Last checked text. | [L49](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L49) |
| S43-06 | settings | A newer fake version yields found state and normalized Update found text. | [L54](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L54) |
| S43-07 | settings | After its feedback delay, Updates says Update available and both Settings upgrade and top new-version controls appear. | [L56](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L56) |
| S43-08 | settings | A fake check failure yields fail state and Couldn't check feedback. | [L62](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L62) |
| S43-09 | settings | After failure feedback, ConnectError appears in Updates and Check now returns to idle. | [L64](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L64) |
| S43-10 | shell | No browser pageerror events are collected during the sampled interactions. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_43.py#L65) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 03–05 repeat for two clicks. Color words in legacy labels are not checked as computed colors; height is checked without full-width coverage.
- The temporary screenshot is not compared. Timing is sampled using waits, not an exact animation-duration contract.
- Overlaps: suite 42 redraw/reuse; suite 44 status-button theme; suite 22 check semantics.
