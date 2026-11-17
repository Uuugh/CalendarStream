# Suite 60: CCS download transports against local TLS

Source: [`tests/suite_60.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

No Postgres/app server/browser UI. A temporary self-signed TLS HTTP server stands in for CCS+, using Demo.ics, fixture Basic credentials and controlled hold/redirect/error responses. Requires OpenSSL, curl and the browser-like HTTP transport dependency. Trust is scoped to the fixture certificate via test session/curl settings; retry pauses are scaled to zero. Tests browser/curl, auto and browser-patient modes.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S60-01 | sources | With CCS_CLIENT absent, selected client is auto. | [L87](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L87) |
| S60-02 | sources | Mixed-case Browser in the environment selects browser. | [L88](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L88) |
| S60-03 | sources | An unknown environment client value falls back to auto. | [L89](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L89) |
| S60-04 | sources | An explicit curl argument selects curl. | [L90](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L90) |
| S60-05 | sources | For browser/curl, successful fixture download returns 200, calendar bytes, ETag and expected Last-Modified prefix. | [L95](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L95) |
| S60-06 | sources | For each transport, debug records one HTTP-200 attempt and a nonempty client description. | [L96](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L96) |
| S60-07 | sources | The first server request carries Authorization. | [L97](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L97) |
| S60-08 | sources | The browser transport user agent begins Mozilla/5.0 and includes Chrome. | [L98](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L98) |
| S60-09 | sources | The curl transport user agent begins curl/. | [L99](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L99) |
| S60-10 | sources | A matching ETag produces status 304 and not_modified=true. | [L101](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L101) |
| S60-11 | sources | The wrong fixture password raises AuthError with the expected credential-rejection text. | [L103](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L103) |
| S60-12 | sources | The simulated protection 403 raises BlockedError with Akamai/reference text. | [L105](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L105) |
| S60-13 | sources | An HTML success response raises SourceError saying it is not a calendar file. | [L107](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L107) |
| S60-14 | sources | Following the same-host redirect succeeds with 200. | [L108](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L108) |
| S60-15 | sources | An HTTPS-to-HTTP redirect raises SourceError requiring HTTPS. | [L110](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L110) |
| S60-16 | sources | A redirect loop raises SourceError with too-many-redirects wording. | [L112](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L112) |
| S60-17 | sources | The six-megabyte fixture raises SourceError with more-than-5MB wording. | [L114](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L114) |
| S60-18 | sources | Redirecting localhost to 127.0.0.1 returns Demo.ics and the destination echo sees no Authorization. | [L117](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L117) |
| S60-19 | sources | The silent hold raises NoReplyError with the sampled one-second timeout and manual-upload guidance. | [L119](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L119) |
| S60-20 | sources | Failure sentinel: a plain-HTTP download unexpectedly accepted by browser/curl/auto fails. | [L123](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L123) |
| S60-21 | sources | Each sampled plain-HTTP call raises SourceError requiring HTTPS. | [L124](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L124) |
| S60-22 | sources | A flaky auto download succeeds with debug attempts showing first browser timeout then browser HTTP 200. | [L129](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L129) |
| S60-23 | sources | A persistent auto hold raises NoReplyError after at least 3.5 seconds. | [L133](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L133) |
| S60-24 | sources | The browser-patient flaky fixture succeeds with three recorded attempts. | [L137](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L137) |
| S60-25 | sources | Auto download of the simulated protection denial raises BlockedError. | [L140](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L140) |
| S60-26 | sources | An auto wrong-password attempt raises AuthError in under three seconds. | [L142](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L142) |
| S60-27 | sources | A plain feed download remains curl with a curl user-agent/debug description despite CCS_CLIENT=browser. | [L147](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_60.py#L147) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 04 tests an explicit argument with the environment absent; it does not independently prove precedence over a conflicting environment value.
- Common transport rows repeat for browser/curl; their user-agent assertions are separate branches. Rows 20/21 pair a failure sentinel with SourceError checks across browser/curl/auto.
- The loop fixture proves rejection of an infinite redirect loop, not the exact allowed five-hop boundary. The oversized sample is six MiB, not the exact five-MB boundary.
- Cross-host credential removal is sampled with localhost versus 127.0.0.1 at the same server. No real United service is contacted. Certificate trust uses the local fixture, not production TLS policy testing.
- Retry row 23 checks type/elapsed lower bound, not an explicit complete client-attempt list. Wrong-password timing under three seconds does not by itself count attempts or establish real account-lockout behavior.
- Overlaps: suite 23 HTTPS input; suite 53 recurrence/installer; earlier source-error/credential checks.
