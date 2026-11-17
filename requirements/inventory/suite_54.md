# Suite 54: Google reconnect, color refusal and settings

Source: [`tests/suite_54.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8124; Demo.ics; background loops patched. Per-module consent is followed through the mock. Color setter failure and client-check health states are injected; page markup is inspected without a browser.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S54-01 | google | The unconnected module header omits Last synced text. | [L49](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L49) |
| S54-02 | google | Completing mock module consent redirects 303 to that destination's fragment. | [L53](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L53) |
| S54-03 | google | The destination's stored section-open preference is true after consent. | [L54](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L54) |
| S54-04 | google | Its mapped calendar exists in the mock and the page contains Connected text. | [L58](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L58) |
| S54-05 | google | Two full syncs succeed even when the color setter raises the fixture AccessRevoked error. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L65) |
| S54-06 | google | Recent logs contain exactly one color-failure message and the module info has no last_error. | [L67](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L67) |
| S54-07 | google | Disconnecting the module makes its account unconnected. | [L72](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L72) |
| S54-08 | google | Reconnecting the same fixture account reuses its remote calendar ID without increasing calendar count. | [L77](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L77) |
| S54-09 | google | A seeded sign-in error renders Sign-in failed, Fix-control markup and its module connect form/action. | [L84](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L84) |
| S54-10 | google | Accepted client settings show Healthy/Reconnect and omit Sync Now, Last synced and Instant updates. | [L95](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L95) |
| S54-11 | google | The client-ID field exists with no readonly text in its sampled neighboring markup. | [L97](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L97) |
| S54-12 | google | Google settings has one Remove-button spelling, no credential trash and explanatory reconnect wording. | [L99](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L99) |
| S54-13 | google | A seeded rejected-client result shows Client rejected and Fix. | [L103](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L103) |
| S54-14 | google | Removing the client renders Not set up and Connect without Turn on wording. | [L106](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_54.py#L106) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Color refusal is injected as AccessRevoked; succeeding sync does not prove live Google accepts any color. Row 06 checks one recent message count and stored error absence, not all historical logging.
- Row 09 inspects Fix form markup, not clicking/re-authenticating via a browser. Row 11 only checks the client-ID field's nearby readonly text, not both credentials' actual edit/save capability.
- State/wording predicates are markup checks without ordering/geometry unless explicitly described.
- Overlaps: suites 48 client lifecycle; suites 55/56 real mock refusal/fallback methods; suite 46 Settings controls.
