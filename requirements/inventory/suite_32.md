# Suite 32: Updater requests and browser progress

Source: [`tests/suite_32.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8098; local fake updater HTTP server 8112; Chromium at 1300×800. A temporary fixture bearer-token file and patched installed version drive acceptance/rejection paths. A stored update offer is seeded; background loops are patched. Updating module version variables simulates restart; no container/image is installed.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S32-01 | settings | The updater probe sets ready when the local fake service answers /livez. | [L37](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L37) |
| S32-02 | settings | The page renders a ready update slot with the patched from/to versions and Update now text. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L39) |
| S32-03 | settings | With the updater ready, the page omits Updater: running and the older installer-update instruction. | [L40](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L40) |
| S32-04 | settings | Async Update now returns 200 with the offered version and POSTs /v1/update with only the app image, async=true and the fixture bearer token. | [L43](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L43) |
| S32-05 | settings | The page includes the activity message announcing the requested version update. | [L45](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L45) |
| S32-06 | account | An Update now request with a wrong CSRF token returns 400 or 403. | [L46](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L46) |
| S32-07 | settings | If the fake updater rejects the changed token file, the route returns 502 with token-refusal detail. | [L49](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L49) |
| S32-08 | settings | For a pinned exact image version, the page omits the update slot and Update now returns 400. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L53) |
| S32-09 | settings | After clicking Update now, the browser slot has downloading state, Downloading text and a visible progress-bar element. | [L66](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L66) |
| S32-10 | settings | After simulating a new installed version, the update slot/new-version notice disappear and version text/link/footer name the new version. | [L69](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L69) |
| S32-11 | settings | A rejected browser update sets failed state and a tooltip containing the token-refusal reason. | [L75](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L75) |
| S32-12 | shell | No browser pageerror events are collected during the sampled update interactions. | [L76](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L76) |
| S32-13 | settings | After the fake updater is stopped and probed, ready is false, the slot is absent and installer guidance is shown. | [L81](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_32.py#L81) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- The fake updater validates request path, image query and fixture bearer token; it does not pull an image or restart containers. Row 10 changes version variables to simulate the restarted service.
- Row 09 checks a visible bar, not that its pixels animate. Row 11 checks failed state/tooltip, not the exact failure icon or label promised in the legacy label.
- Timing checks sample fixed waits; screenshots are temporary captures without comparisons.
- Overlaps: suites 22/30 offered versions; suite 38 auto-install behavior; suite 39 cache/version assets.
