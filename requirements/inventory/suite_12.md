# Suite 12: Google connection and client setup

Source: [`tests/suite_12.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; FastAPI TestClient; local mock Google on port 8112. Default configured mode and `unconfigured` mode. `connect()` also checks the initial redirect. Background source loop is patched; the mock supplies OAuth and calendar responses.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S12-01 | google | Without a client, show the guided setup and omit the Google connect form. | [L48](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L48) |
| S12-02 | google | Without a client, refuse POST /google/connect with HTTP 400. | [L49](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L49) |
| S12-03 | google | Reject a malformed Google client ID with HTTP 400 and a client-ID error. | [L51](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L51) |
| S12-04 | google | Require a secret when saving a client for the first time. | [L53](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L53) |
| S12-05 | google | Reject a Google client form with an invalid CSRF token. | [L54](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L54) |
| S12-06 | google | Persist the submitted client ID without the submitted plaintext secret in the stored record. | [L57](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L57) |
| S12-07 | google | After saving a client, omit the plaintext secret, show keep-saved guidance and a connect control. | [L59](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L59) |
| S12-08 | google | A blank secret preserves the saved secret while updating the client ID. | [L62](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L62) |
| S12-09 | google | Removing the client clears configured state and the stored client record. | [L64](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L64) |
| S12-10 | google | The sampled recent log contains no fixture secret prefix. | [L66](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L66) |
| S12-11 | google | The configured page contains a connect control or the Ready client state. | [L69](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L69) |
| S12-12 | google | connect needs CSRF | [L70](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L70) |
| S12-13 | google | connect needs the status-page login | [L71](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L71) |
| S12-14 | google | callback needs the status-page login | [L72](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L72) |
| S12-15 | google | The consent URL supplies the public callback URI and prompt=consent. | [L75](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L75) |
| S12-16 | google | callback returns to Google Calendar sync in Settings (0.2.8-beta.4) | [L76](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L76) |
| S12-17 | google | After consent, connection state is true and the mock account email is reported. | [L78](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L78) |
| S12-18 | google | The returned calendar ID exists in the mock and its summary equals the app calendar name. | [L79](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L79) |
| S12-19 | google | The created mock calendar uses America/New_York. | [L81](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L81) |
| S12-20 | google | The stored refresh-token record has version 1 and contains no plaintext mock refresh token. | [L84](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L84) |
| S12-21 | google | the account is shown (beta.17: in its Google module) | [L86](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L86) |
| S12-22 | google | client can't change while connected | [L87](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L87) |
| S12-23 | google | Recent activity logs report connection as the mock account and calendar creation. | [L90](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L90) |
| S12-24 | google | Reusing the consent state reports expired or already used. | [L94](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L94) |
| S12-25 | google | After clearing cached access credentials, an API call refreshes access and retrieves the calendar. | [L101](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L101) |
| S12-26 | google | A 403 rateLimitExceeded followed by 503 is retried successfully with at least 2.5 seconds elapsed. | [L106](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L106) |
| S12-27 | google | Reconnecting the same account retains the calendar ID and does not create a second calendar. | [L111](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L111) |
| S12-28 | google | Disconnect without delete revokes access, clears connected state and retains the mock calendar. | [L115](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L115) |
| S12-29 | google | Disconnect without delete remembers the calendar ID. | [L116](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L116) |
| S12-30 | google | Reconnect after keeping the calendar reuses its ID. | [L118](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L118) |
| S12-31 | google | Disconnect with delete removes the mock calendar and forgets its ID. | [L122](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L122) |
| S12-32 | google | Recent activity logs report disconnection and calendar deletion. | [L124](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L124) |
| S12-33 | google | Consent without calendar permission leaves disconnected state and records a permission error. | [L129](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L129) |
| S12-34 | google | The page shows guidance to tick calendar permission after refused consent. | [L131](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L131) |
| S12-35 | google | An access_denied callback reports cancelled or refused sign-in. | [L136](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L136) |
| S12-36 | google | Successful subsequent consent clears the recorded error. | [L141](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L141) |
| S12-37 | google | A different mock account gets a different calendar ID and its own reported email. | [L145](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L145) |
| S12-38 | google | Failure sentinel: reaching the end of the revoked-token API call without AccessRevoked fails. | [L151](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L151) |
| S12-39 | google | Revoked refresh access raises AccessRevoked with Connect again guidance. | [L153](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L153) |
| S12-40 | google | Failure sentinel: decrypting with a different database password without AccessRevoked fails. | [L158](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L158) |
| S12-41 | google | Using a different database password raises AccessRevoked with DB_PASSWORD guidance. | [L160](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L160) |

## Direct assertions

- [L31](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L31): `r.status_code == 303` — setup/connection redirect guard; a failed prerequisite stops the subsequent checks.
- [L45](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_12.py#L45): `r.status_code == 303` — setup/connection redirect guard; a failed prerequisite stops the subsequent checks.

## Coverage limits and reconciliation notes

- Rows 01–10 run only in `unconfigured`; rows 11–41 run in the configured path. The unconfigured branch exits early.
- Rows 38 and 40 are deliberate `ok(False, ...)` exception-path sentinels, paired with rows 39 and 41, not behaviors to specify as unconditional failures.
- `ok()` here only prints PASS/FAIL; the harness scans output for FAIL. Running this file directly does not by itself provide a reliable failing exit code.
- Token/client encryption checks compare stored representations and absence of fixture plaintext; they are not a full cryptographic audit.
- Overlaps: suite 14 client validation; suite 13 sync lifecycle; suite 20 disconnect/watch cleanup.
