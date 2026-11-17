# Suite 68: Unsigned Google accounts, health and traffic routes

Source: [`tests/suite_68.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8168; loops patched and API readiness forced true. A fresh unsigned module drives warning counts. Health errors and a fake ValueError-raising account are injected. Traffic contains a synthetic bearer header; an anonymous TestClient checks access.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S68-01 | google | The newly added Google module's account is not connected. | [L37](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L37) |
| S68-02 | google | A full sync with that signed-out module returns true. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L38) |
| S68-03 | history | Recent logs contain exactly one not-signed-in/unsynced warning for it. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L39) |
| S68-04 | history | Two additional syncs leave that warning count at one. | [L41](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L41) |
| S68-05 | history | Discarding its remembered-warning key and syncing again raises that count to two. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L44) |
| S68-06 | google | The last API setup step returns 200 with ok=true. | [L47](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L47) |
| S68-07 | history | Recent logs say API Sync is set up and needs per-module sign-in, without is ready wording. | [L49](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L49) |
| S68-08 | history | Recent logs name the signed-out module. | [L51](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L51) |
| S68-09 | google | Injecting a 503 GoogleError marks the first account degraded and disallows immediate sync. | [L57](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L57) |
| S68-10 | google | The next full sync returns true while that account is degraded. | [L58](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L58) |
| S68-11 | google | Explicit health reset permits sync and marks the account healthy. | [L60](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L60) |
| S68-12 | google | A fake account whose sync raises ValueError makes _sync_account return false. | [L69](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L69) |
| S68-13 | google | That account's recorded failure kind is unknown and state degraded. | [L72](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L72) |
| S68-14 | diagnostics | The authenticated traffic endpoint returns 200 with the exact fixture Bearer header unredacted. | [L79](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L79) |
| S68-15 | diagnostics | Clearing traffic returns 200/ok and empties recorded entries. | [L82](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L82) |
| S68-16 | diagnostics | The page includes the betacopy control ID. | [L84](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L84) |
| S68-17 | account | An anonymous traffic request returns 401 or 403. | [L88](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_68.py#L88) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Warning reset row 05 manually discards the remembered flag; it does not sign in and lose consent. Row 11 calls health.reset directly, not an actual new sign-in.
- Degraded-account row 10 checks return true but does not count remote calls to independently prove no request hammering. Unexpected error coverage uses one synthetic ValueError.
- Traffic checks intentionally use a fixture bearer string; no real token is reproduced here. Row 16 checks control ID, not adjacency or clipboard behavior. Anonymous access samples one route.
- Overlaps: suite 53 diagnostic traffic; suites 54/55 sign-in/error health; suite 71 readiness decision stages.
