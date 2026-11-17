# Suite 59: Update observations, event colors and section styling

Source: [`tests/suite_59.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8159; seed.demo; fake work.ics download. Source/Google/update/updater loops patched. Stored update timestamps are manipulated. Chromium 1400×900 tests event UI and light/dark styling, then intercepts /api/status and shortens RESTART_WAIT to four seconds to test observer/reload flow.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S59-01 | settings | Initial status API updating value is empty. | [L36](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L36) |
| S59-02 | settings | Marking an update makes the status API return its target version. | [L38](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L38) |
| S59-03 | settings | An update marker timestamped sixteen minutes ago is no longer effective. | [L40](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L40) |
| S59-04 | settings | An update marker whose from version differs from the running version is no longer effective. | [L42](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L42) |
| S59-05 | settings | For an hourly check fifty minutes old, next_check is between nine and eleven minutes ahead. | [L46](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L46) |
| S59-06 | process | The updater-job source contains the checked bounded sleep expression. | [L48](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L48) |
| S59-07 | feeds | Feed-removal confirmation markup contains the question and a newline before its link-stops-working note. | [L52](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L52) |
| S59-08 | events | The editor omits the old grid2 ticks line and old end-zone sentence. | [L57](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L57) |
| S59-09 | events | End-date label markup places All-day after Ends and before the date field. | [L59](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L59) |
| S59-10 | events | End-time label markup places the different-zone checkbox after Time and before its field. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L61) |
| S59-11 | events | The page has timed/tzdiff markup and orders start-zone before end-zone input. | [L62](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L62) |
| S59-12 | events | Choosing another source updates the default displayed color to that source's color. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L76) |
| S59-13 | events | The palette's default-color data value follows that selected source. | [L78](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L78) |
| S59-14 | events | An explicitly picked color survives a later source selection and differs from the new source color. | [L82](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L82) |
| S59-15 | events | All-day sits beside the Ends label on its row above the date field. | [L87](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L87) |
| S59-16 | events | The different-end-zone choice sits beside its Time label above the time field. | [L90](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L90) |
| S59-17 | events | Checking the different-zone option shows its zone box below/aligned with the end-time column. | [L94](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L94) |
| S59-18 | events | Checking All-day preserves its checkbox position and hides both time fields and tzdiff. | [L97](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L97) |
| S59-19 | shell | In each requested palette, the six section border colors are distinct and all measured border widths are 1px. | [L115](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L115) |
| S59-20 | shell | In each palette, all sampled section background colors are identical. | [L116](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L116) |
| S59-21 | shell | In each palette, the nonempty module set has a color token, gradient background and border color different from section colors. | [L117](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L117) |
| S59-22 | sources | Choosing a source palette color immediately updates its inline module-color variable. | [L126](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L126) |
| S59-23 | settings | With updater readiness true, the top bar has its can-update attribute. | [L132](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L132) |
| S59-24 | settings | Starting the observer flow with intercepted status responses shows Downloading in the top bar. | [L141](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L141) |
| S59-25 | settings | Aborting those status responses subsequently shows Restarting. | [L143](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L143) |
| S59-26 | settings | After restored status responses, the page marker survives the initial 1.5-second wait. | [L146](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L146) |
| S59-27 | settings | The browser later reloads and at least 1.2 seconds elapsed since the measured marker time. | [L148](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L148) |
| S59-28 | shell | No collected page/console errors occur, excluding the explicitly ignored failed-resource console text. | [L150](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_59.py#L150) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Marker expiry samples sixteen minutes, not the precise fifteen-minute boundary. The from-version mismatch check does not simulate running the named target version specifically.
- Row 06 is a source-string check; updater loops are patched, so scheduling is not exercised autonomously. Row 17 checks zone geometry, not absence of an End time zone label.
- Row 21 checks color-token/gradient presence and section-color inequality, not equality of every module border to its intended own color. Row 22 checks immediate inline state rather than save persistence.
- Reload behavior is driven via updateNow(true), intercepted status responses and a shortened four-second wait. The assertion's measured lower bound is 1.2 seconds, not a fifteen-second production timing guarantee.
- Overlaps: suites 42/47 updater state; suites 57/58 event layout; suites 44/61 themes.
