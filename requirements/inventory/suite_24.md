# Suite 24: Google setup guide and public-address warnings

Source: [`tests/suite_24.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; a synthetic configured public host differs from the request host. Main loops patched; Google client credentials are fixture values saved directly. Requests vary the request host and Accept-Language.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S24-01 | settings | A configured public host differing from the request host displays both hosts and the mismatch warning. | [L18](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L18) |
| S24-02 | google | The page includes the configured public callback URI in a value attribute for copying. | [L19](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L19) |
| S24-03 | google | All nine sampled guide step headings exist in order: First, Project, Calendar API, Sign-in screen, Calendar access, Let yourself in, Client, Keys, Connect. | [L23](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L23) |
| S24-04 | google | The guide substring contains at least five checkmark-space occurrences. | [L24](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L24) |
| S24-05 | google | The guide includes error guidance naming redirect_uri_mismatch, access_denied and invalid_client. | [L25](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L25) |
| S24-06 | google | An access_denied callback returns one of HTTP 302, 303 or 307. | [L27](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L27) |
| S24-07 | google | The next page after access_denied includes Test users guidance. | [L29](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L29) |
| S24-08 | settings | The public-address mismatch warning is absent when opened using the configured public host. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L30) |
| S24-09 | settings | The mismatch warning is absent when opened using the sampled HTTP LAN IP address. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L31) |
| S24-10 | shell | A Spanish browser-language request includes the translated Google-error guide heading. | [L33](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_24.py#L33) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- The guide checks use substring presence/order, not actual navigation through Google Cloud or successful project/API/client setup.
- Row 04 counts checkmark strings; it does not test completion tracking. Row 06 checks only an allowed redirect status, not its Location target.
- Row 10 samples one Spanish guide heading; it is not a complete translation audit.
- Request-host checks simulate matching and LAN requests inside TestClient; no public DNS resolution is exercised.
- Overlaps: suite 23 callback/address guidance; suite 17 translation samples; suite 25 support/contact guide text.
