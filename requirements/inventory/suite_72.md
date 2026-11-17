# Suite 72: Google failure classification and recovery decisions

Source: [`tests/suite_72.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure classifier/policy objects; no app/database/network. Fixed jitter lambdas make sampled backoffs deterministic. Database argument unused.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S72-01 | google | AccessRevoked, CalendarMissing and Conflict fixtures classify as consent-revoked, calendar-missing and conflict. | [L15](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L15) |
| S72-02 | google | Status 401 and 403 classify as token-expired and permission. | [L16](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L16) |
| S72-03 | google | Status 429 and 503 classify as rate-limit and transient. | [L17](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L17) |
| S72-04 | google | A transient-flagged GoogleError classifies as transient. | [L18](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L18) |
| S72-05 | google | The sampled 404,409,400 errors classify as calendar-missing, conflict and event-invalid. | [L19](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L19) |
| S72-06 | google | The sampled rejected-OAuth-client message classifies as permission. | [L20](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L20) |
| S72-07 | google | A ValueError and plain GoogleError both classify as unknown. | [L21](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L21) |
| S72-08 | google | An initial token-expired recovery decision retries in recovering state. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L24) |
| S72-09 | google | The next token-expired attempt does not retry and requires reauthorization. | [L26](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L26) |
| S72-10 | google | Revoked-consent recovery does not retry and requires reauthorization. | [L27](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L27) |
| S72-11 | google | Permission recovery does not retry and requires reauthorization. | [L28](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L28) |
| S72-12 | google | With zero jitter, the first two transient delays are five and ten seconds and the initial decision retries. | [L29](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L29) |
| S72-13 | google | A rate-limit decision honors a sampled longer Retry-After of 120 seconds. | [L30](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L30) |
| S72-14 | google | The sampled final allowed transient-attempt delay does not exceed MAX_DELAY. | [L31](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L31) |
| S72-15 | google | At MAX_ATTEMPTS, transient recovery does not retry and is degraded. | [L32](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L32) |
| S72-16 | google | With jitter fixed at one, the initial backoff is five seconds times 1.25. | [L33](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L33) |
| S72-17 | google | A missing-calendar decision does not retry and pauses. | [L35](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L35) |
| S72-18 | google | Event-invalid and conflict decisions do not retry and leave health healthy. | [L36](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L36) |
| S72-19 | google | Unknown failure retries at attempt zero but not attempt one. | [L37](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_72.py#L37) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Status samples include 503 and 404 but not every 5xx or 410 mentioned by labels. Class precedence is sampled, not exhaustively cross-combined with contradictory statuses.
- Policy decisions do not refresh tokens, recreate calendars or run scheduled syncs. Missing-calendar row checks paused/no-retry only. Backoff cap/jitter assertions use selected attempts and fixed jitter, not full distributions.
- Overlaps: suites 68/73 account-health integration and persistence; suite 71 readiness.
