# Suite 23: Public URLs, Google client checks and security guards

Source: [`tests/suite_23.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; initially no page credentials. The test creates a fixture login, seeds encrypted mock client records and replaces the Google check HTTP client. Global login-limit checks patch client-IP extraction to use test headers and use documentation-range IPs. No live Google or CCS+ account is needed.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S23-01 | settings | The legacy installer HTTP private-IP default yields empty configured and effective public addresses. | [L17](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L17) |
| S23-02 | account | The welcome page token differs from the status-page CSRF token. | [L21](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L21) |
| S23-03 | account | A welcome-page token cannot submit the authenticated public-address form (HTTP 400). | [L24](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L24) |
| S23-04 | google | Without a configured public address, the page includes a Google callback URI using its request host. | [L26](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L26) |
| S23-05 | settings | Saving the sampled mixed-case bare host with a trailing slash produces lowercase HTTPS without a trailing slash. | [L28](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L28) |
| S23-06 | settings | URL normalization lowercases schemes/hosts and removes default HTTPS 443 and HTTP 80 ports in the two examples. | [L29](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L29) |
| S23-07 | google | A mocked redirect_uri_mismatch response yields client ok=true and redirect_ok=false. | [L44](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L44) |
| S23-08 | google | The page shows Address missing and the exact callback-addition guidance, without Check both values. | [L46](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L46) |
| S23-09 | google | The rendered page contains the copy-address and open-client controls; the open-client link is not hidden by the checked markup. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L48) |
| S23-10 | google | After changing public address, the previous address's Address missing result no longer appears. | [L52](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L52) |
| S23-11 | google | A mocked invalid_grant response yields client-check ok=true. | [L56](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L56) |
| S23-12 | google | After the accepted check, the page omits the old missing-address wording, shows Healthy and contains the client-ID field. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L58) |
| S23-13 | settings | URL normalization preserves the sampled /a path. | [L59](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L59) |
| S23-14 | settings | Failure sentinel: accepting either malformed-scheme or semicolon-path sample without ValueError fails. | [L61](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L61) |
| S23-15 | settings | The two invalid URL samples raising ValueError reach the paired success marker. | [L62](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L62) |
| S23-16 | settings | The legacy HTTP localhost installer default is treated as no public URL. | [L65](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L65) |
| S23-17 | google | For the configured HTTPS IP address, omit its callback URI and show public-address setup guidance. | [L70](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L70) |
| S23-18 | google | For the configured .local host, omit its callback URI from the page. | [L73](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L73) |
| S23-19 | account | Among 60 failed logins from distinct simulated addresses, the first 50 have no 429 and at least nine overall return 429. | [L80](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L80) |
| S23-20 | account | During the global-failure block, valid credentials from a seeded recently successful address return HTTP 200. | [L82](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L82) |
| S23-21 | account | During that block, valid credentials from a new simulated address return HTTP 429. | [L83](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L83) |
| S23-22 | google | A seeded legacy missing-redirect check is interpreted as client ok=true, redirect_ok=false with its saved redirect URI. | [L89](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L89) |
| S23-23 | account | A cross-site public-address form POST returns HTTP 403 and preserves the saved address. | [L93](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L93) |
| S23-24 | google | A cross-site Google notification request with an unknown channel receives HTTP 200. | [L94](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L94) |
| S23-25 | account | The sampled authenticated page response includes SAMEORIGIN, frame-ancestors self, nosniff and no-referrer headers. | [L96](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L96) |
| S23-26 | feeds | Requesting the sampled non-ASCII feed token returns HTTP 404. | [L98](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L98) |
| S23-27 | sources | Failure sentinel: accepting the sampled plain-HTTP download without SourceError fails. | [L102](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L102) |
| S23-28 | sources | The plain-HTTP download raises SourceError containing must start with https://. | [L104](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_23.py#L104) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 14/15 are a failure sentinel and its paired success marker inside a loop over two invalid URLs. Row 27/28 similarly pair the forbidden-download call with its expected exception. Neither success marker alone checks an error message beyond its stated predicate.
- Row 25 checks headers on one authenticated GET response, despite the label saying every page; it does not establish header coverage across routes.
- Row 19 asserts observed 429 counts at the sampled attempts. It does not independently prove an exact configured global threshold or block duration. The test patches IP extraction; it does not establish trust of real proxy headers.
- Row 24 only checks HTTP 200 on an unknown-channel notification; it does not prove a valid notification causes a sync.
- Row 11 checks ok only, not an explicit redirect_ok field. Row 12 checks markup and Healthy, not a subsequent connection.
- Plain-HTTP download rejection is a single transport-input example, not full redirect/SSRF coverage.
- Overlaps: suite 15 URL validation/import; suite 16 setup/CSRF/login; suites 12/14 client checks; suite 20 notification behavior.
