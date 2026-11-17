# Suite 79: Calendar stretch controls and clock badge

Source: [`tests/suite_79.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; seed.demo; source/Google/update loops patched. Markup and stored route values are checked for stretch and clock controls. Calendar CSS is read directly; no browser.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S79-01 | calendar | The page contains the stretch-bar wrapper and collapse/expand IDs. | [L30](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L30) |
| S79-02 | calendar | Stretch-handle markup has the calstretch class/ID and a slider role somewhere in the page. | [L31](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L31) |
| S79-03 | calendar | The sampled stretch markup has gripdots class and at least twelve circle elements. | [L33](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L33) |
| S79-04 | calendar | The stretch node has the expected nonbutton markup and omits the old stretch-button spelling. | [L34](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L34) |
| S79-05 | calendar | Calendar CSS omits the sampled right-grip stretch-selector spelling. | [L35](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L35) |
| S79-06 | calendar | Stretch -300 returns success and persists -300. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L38) |
| S79-07 | calendar | Stretch -301 returns 400. | [L40](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L40) |
| S79-08 | calendar | Stretch -120 returns success and persists -120. | [L41](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L41) |
| S79-09 | calendar | The page omits the old clockswitch ID. | [L46](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L46) |
| S79-10 | calendar | The clock ID exists with switch role in its sampled neighboring markup. | [L47](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L47) |
| S79-11 | calendar | Clock-number markup exists and the nearby text shows default 12. | [L49](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L49) |
| S79-12 | calendar | Posting 24-hour format returns an allowed success status. | [L50](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L50) |
| S79-13 | calendar | The next page has checked=true and nearby clock number 24. | [L52](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_79.py#L52) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Markup presence does not prove visual centering, arrow operation or drag interaction. Slider-role row searches page-wide, and circle count is at least twelve rather than exactly twelve/two rows of six.
- Stretch tests prove -300 and -120 acceptance with -301 rejection, not every interior value or upper bound. Clock tests inspect nearby markup and saved response, not hollow-icon pixels or physical click behavior.
- Overlaps: suites 64/65 stretch/full-mode; suite 21 browser clock switching.
