# Suite 48: Google setup steps and client lifecycle

Source: [`tests/suite_48.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8120; Demo.ics. Loops patched. The connect helper runs save/client/address/go steps then mock consent, stopping on failure. Mock authorized-redirect/client data drives missing-address and replacement-client scenarios. No browser interaction.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S48-01 | google | An empty save step returns ok=false with client-ID/secret guidance. | [L58](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L58) |
| S48-02 | google | A malformed client ID returns ok=false with its shape-error message. | [L60](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L60) |
| S48-03 | google | Saving a well-shaped client ID with the fixture wrong secret initially returns ok=true. | [L62](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L62) |
| S48-04 | google | The client-check step then returns ok=false with secret-rejection message and an open-client fix link. | [L64](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L64) |
| S48-05 | google | Missing authorized callback causes connect to stop at address step, with the exact URI in its message/copy fix and an open fix. | [L67](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L67) |
| S48-06 | google | Settings renders Address missing, warn class and data-address=0 without the sampled old Google bold label. | [L71](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L71) |
| S48-07 | google | After authorizing the callback in the mock, connect succeeds and account state is connected. | [L75](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L75) |
| S48-08 | google | The stored client-check result records redirect_ok=true. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L76) |
| S48-09 | google | The first full sync returns success. | [L77](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L77) |
| S48-10 | google | One owned mock calendar exists with more than five active events and a nonempty local calendar mapping. | [L80](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L80) |
| S48-11 | google | Disconnect clears connected state while retaining the mapped remote calendar ID. | [L84](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L84) |
| S48-12 | google | The disconnected destination header says Not connected with run status class. | [L87](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L87) |
| S48-13 | google | A full sync while disconnected returns success without a last_error. | [L88](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L88) |
| S48-14 | google | Reconnect with the same client and blank secret succeeds. | [L90](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L90) |
| S48-15 | google | After reconnect sync, the mapped calendar ID is unchanged and owned-calendar count remains one. | [L92](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L92) |
| S48-16 | google | Its active remote event count matches the pre-disconnect count. | [L93](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L93) |
| S48-17 | google | Removing the client leaves both connected and configured false. | [L97](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L97) |
| S48-18 | google | The next page contains Not set up and no Traceback text. | [L99](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L99) |
| S48-19 | google | Connecting another fixture client succeeds with that new client ID. | [L102](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L102) |
| S48-20 | google | The new client's full sync returns success. | [L103](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L103) |
| S48-21 | google | The new mapping differs from the old ID, while two owned calendars and the old remote calendar remain. | [L106](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L106) |
| S48-22 | history | Recent logs warn that the prior client's calendar is unreachable and should be deleted manually. | [L107](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L107) |
| S48-23 | google | After new-client setup, account info has no last_error. | [L108](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L108) |
| S48-24 | google | Another full sync retains the new mapping and the count of two calendars. | [L110](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_48.py#L110) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- The mock checks authorized redirect lists, not live Google client configuration. Row 06 asserts data-address=0, not a named guide step's visual checkbox.
- Calendar/event count comparisons do not prove every event identity or field is unchanged. Row 13 explicitly calls a sync function; background loops are patched, so autonomous scheduling is not exercised.
- The old remote calendar intentionally remains when the client changes. Row 22 samples log wording, not actual manual deletion.
- Overlaps: suites 12/14/23 client checks; suite 51 per-module invitations/accounts; suite 45 two-way sync.
