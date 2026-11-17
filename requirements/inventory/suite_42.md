# Suite 42: Updates after redraw and simulated restart

Source: [`tests/suite_42.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8142; stand-in updater 8113; fake update checker and installed version; Chromium 1300×900. Background loops patched; temporary fixture token file. Version-variable changes simulate restart, not image installation.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S42-01 | settings | The local stand-in updater is reported ready. | [L41](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L41) |
| S42-02 | settings | Updates markup contains the idle Update now control and omits Upgrade wording. | [L43](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L43) |
| S42-03 | settings | After Check now, exactly one fake check has run, an update button appears and Updates says Update available. | [L54](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L54) |
| S42-04 | settings | Clicking Update after redraw sets the top slot downloading and disables the Settings update control in syncing state. | [L57](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L57) |
| S42-05 | settings | After simulating the new installed version, current-version text changes and the top update slot disappears. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L61) |
| S42-06 | settings | The Settings upgrade button disappears, Check now reappears and the new running version is displayed. | [L63](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L63) |
| S42-07 | settings | Clicking Check now again calls the fake checker a second time and retains the running version and Check now control. | [L66](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L66) |
| S42-08 | shell | No browser pageerror events are collected during the sampled interactions. | [L67](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_42.py#L67) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Version variables simulate a restarted container. The fake updater accepts the sampled path without testing authentication here; suite 32 separately checks bearer authorization.
- Fixed sleeps and count/state checks do not establish exact transition timings or real installation success. The browser test does not directly record reload events.
- Overlaps: suites 32/47 updater progress; suite 43 repeated checks; suite 38 in-place Settings.
