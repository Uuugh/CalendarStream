# Suite 14: Download interval, layout and Google client validation

Source: [`tests/suite_14.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; mock Google on 8114, stopped to simulate an unreachable service. Background loops patched; environment interval 60 minutes.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S14-01 | shell | Theme choices appear in light, dark, system order. | [L29](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L29) |
| S14-02 | sources | 0.2.2: last download, interval (header) → upload (Configure) → destinations | [L31](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L31) |
| S14-03 | sources | upload only once; old line under the title gone | [L33](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L33) |
| S14-04 | sources | With a 60-minute environment interval, the interval field displays 60. | [L34](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L34) |
| S14-05 | sources | Saving 30 minutes returns 303, persists the interval and wakes the source loop. | [L37](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L37) |
| S14-06 | sources | The next run is last attempt plus 30 minutes, within two seconds. | [L38](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L38) |
| S14-07 | sources | When last attempt is 100 minutes ago, changing to 45 minutes schedules an immediate run. | [L41](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L41) |
| S14-08 | sources | below 15 refused | [L42](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L42) |
| S14-09 | sources | not a number refused | [L43](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L43) |
| S14-10 | sources | needs CSRF | [L44](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L44) |
| S14-11 | sources | Returning to 60 minutes deletes the stored override and uses the environment interval. | [L46](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L46) |
| S14-12 | sources | After reset, the rendered interval field again displays 60. | [L47](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L47) |
| S14-13 | google | The mock accepts the saved client and the page shows acceptance feedback. | [L53](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L53) |
| S14-14 | google | form above the guide; guide closed (beta.17: Ready shows no guide) | [L54](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L54) |
| S14-15 | google | wrong secret → rejected, said under the row (beta.14: Connect stops there) | [L58](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L58) |
| S14-16 | google | An unknown mock client ID produces an unknown-client message. | [L60](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L60) |
| S14-17 | google | Google unreachable → unknown, not failed | [L65](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L65) |
| S14-18 | google | Sampled recent logs do not contain the fixture client secret. | [L66](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_14.py#L66) |

## Coverage limits and reconciliation notes

- Rows 04 and 12 both check the displayed 60-minute interval, before and after changing/resetting it.
- The sampled lower-bound rejection is 5 minutes; this suite does not exhaust all values below 15 or assert the 1440 upper bound.
- Client checks use a local mock, not Google’s production endpoint.
- Overlaps: suite 12 client setup and secret handling; suite 18 source layout; suite 21 theme/control placement.
