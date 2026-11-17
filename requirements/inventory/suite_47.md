# Suite 47: Shared updater state and Google settings

Source: [`tests/suite_47.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8119; stand-in updater 8118; temporary fixture token file; patched installed version and loops. Chromium 1230×900 starts updates from each of two controls. Connected Google/client state is seeded for the final settings checks.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S47-01 | settings | The fake updater service is reported ready. | [L39](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L39) |
| S47-02 | settings | Whether started from Settings or the top bar, both copies simultaneously show Downloading with downloading/syncing state. | [L50](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L50) |
| S47-03 | settings | After a simulated version change, polling observes both controls done with Updated text. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L61) |
| S47-04 | settings | After the delay, the current-version text names the new version and the Settings update button is absent. | [L63](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L63) |
| S47-05 | settings | Token rejection sets top failed and Settings fail state, both with Update failed text. | [L70](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L70) |
| S47-06 | settings | After its delay, top returns ready and Settings returns idle. | [L73](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L73) |
| S47-07 | google | With connected/client records patched, Google settings has no Configure line or credtrash, shows Remove and has no confirmation checkbox. | [L80](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L80) |
| S47-08 | google | The Remove row/button satisfy the sampled at-most-14px left/bottom offsets. | [L84](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L84) |
| S47-09 | shell | No browser pageerror events are collected during the sampled interactions. | [L85](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_47.py#L85) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 02–04 repeat for each initiating control. Version variables simulate restart and fake HTTP simulates updater acceptance/rejection; no image installation is tested.
- Updated state is polled through a finite window. Row 04 checks final version/button presence, not a direct reload-event assertion.
- Row 07 seeds connected/client state instead of real sign-in. Row 08 checks upper bounds only and not exact bottom-left alignment.
- Overlaps: suites 32/42 updater control reuse; suite 46 Google credential layout.
