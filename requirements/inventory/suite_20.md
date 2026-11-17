# Suite 20: Google change notifications

Source: [`tests/suite_20.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; mock Google on 8120; Demo.ics. Background loops patched. Directly mutates mock channels, events and stored timestamps to exercise renewal/retry. Default public address is a synthetic HTTPS host.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S20-01 | google | Mock Google consent results in connected state. | [L37](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L37) |
| S20-02 | google | before the first sync: off, starts with the next sync (in the tooltip) | [L39](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L39) |
| S20-03 | google | The initial full Google sync returns success. | [L40](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L40) |
| S20-04 | google | The watch uses the expected HTTPS notify URL, calendar ID and TTL 604800. | [L43](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L43) |
| S20-05 | google | Stored watch info has a token and does not contain the mock plaintext token; see limitation below. | [L44](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L44) |
| S20-06 | google | logged: instant updates turned on | [L45](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L45) |
| S20-07 | google | page: instant updates on (beta.18: in the module's header) | [L47](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L47) |
| S20-08 | google | wrong token: answered, ignored | [L53](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L53) |
| S20-09 | google | unknown channel: answered, ignored | [L54](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L54) |
| S20-10 | google | 'sync' message: no check | [L55](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L55) |
| S20-11 | google | change notice: full check requested (no login needed) | [L56](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L56) |
| S20-12 | google | After a valid notice and full sync, the remote edited title remains in Google and is saved locally. | [L60](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L60) |
| S20-13 | google | After processing a valid notice, watch info records last_notice and the page shows Last notice from Google. | [L62](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L62) |
| S20-14 | google | With expiry set two hours ahead, ensure_watch replaces the channel and stops the old channel. | [L68](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L68) |
| S20-15 | google | A subsequent ensure_watch on the fresh channel leaves its ID unchanged. | [L70](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L70) |
| S20-16 | google | Changing the public address replaces the watch target URL and leaves one mock channel. | [L74](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L74) |
| S20-17 | google | Two refused-watch attempts produce one unavailable-instant-updates warning. | [L80](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L80) |
| S20-18 | google | page: off, with the reason (in the tooltip) | [L82](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L82) |
| S20-19 | google | Normal autosync still succeeds when Google refuses watch registration. | [L83](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L83) |
| S20-20 | google | With the last attempt set seven hours ago, retry obtains a channel and clears its error. | [L87](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L87) |
| S20-21 | google | http:// address: off, needs https | [L90](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L90) |
| S20-22 | google | disconnect stops the channel | [L95](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L95) |
| S20-23 | google | late notices after disconnect: answered | [L96](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_20.py#L96) |

## Coverage limits and reconciliation notes

- Row 05 checks presence of a stored token and absence of plaintext, not decryptability or a cryptographic algorithm.
- Row 14 samples an expiry two hours ahead, rather than proving the exact one-day renewal boundary claimed in its label.
- Row 20 samples a seven-hour-old attempt, rather than proving the precise six-hour retry boundary.
- Row 08 checks wrong-token rejection and row 09 unknown-channel rejection; neither substitutes for an exhaustive notification-authentication audit.
- Row 12 verifies local and remote titles; it does not explicitly assert that CCS+ was untouched despite that phrase in the label.
- Row 23 only asserts HTTP 200 for a late notification after disconnect, not every possible downstream side effect.
- Overlaps: suite 12 disconnect lifecycle; suite 13 full-check synchronization; suite 15 public address settings.
