# Suite 16: First-run setup, page login and CCS+ credentials

Source: [`tests/suite_16.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; fake download records credentials and raises AuthError. `fresh` is the default; `import` supplies legacy environment credentials, checks import, then exits. The normal harness exercises fresh only: import needs an explicit isolated invocation.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S16-01 | account | old page login imported (hashed) | [L24](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L24) |
| S16-02 | account / sources | old CCS login imported (encrypted) | [L25](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L25) |
| S16-03 | account / sources | Legacy credential import records an Imported activity message. | [L26](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L26) |
| S16-04 | account | page password not stored in clear | [L27](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L27) |
| S16-05 | account | no login yet → /welcome | [L30](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L30) |
| S16-06 | account | Without an initial login, the status API also redirects with HTTP 303. | [L31](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L31) |
| S16-07 | account | feed and health stay open | [L32](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L32) |
| S16-08 | account | The generated setup code matches four hex digits, a dash and four hex digits. | [L36](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L36) |
| S16-09 | account | An incorrect setup code returns 400, reports the code error and creates no page login. | [L39](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L39) |
| S16-10 | account | Initial setup refuses the sampled short password with HTTP 400. | [L40](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L40) |
| S16-11 | account | Initial setup refuses mismatched password confirmation with HTTP 400. | [L41](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L41) |
| S16-12 | account | Initial setup refuses a username containing a space with HTTP 400. | [L42](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L42) |
| S16-13 | account | login created (code case/dash-insensitive) | [L44](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L44) |
| S16-14 | account | The stored page-login record does not contain the plaintext fixture password. | [L45](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L45) |
| S16-15 | account | welcome closed once a login exists | [L46](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L46) |
| S16-16 | account | the new login is signed in already (0.2.8-beta.15) | [L48](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L48) |
| S16-17 | account | page needs the login (the page goes to the sign-in page) | [L50](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L50) |
| S16-18 | account | Settings shows the saved username and Signed in status. | [L56](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L56) |
| S16-19 | account | Five repeated authenticated status requests complete in under one second in this test environment. | [L57](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L57) |
| S16-20 | sources | Setup open with the CCS+ form while not configured | [L58](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L58) |
| S16-21 | sources | Coverage gap: the intended status-message check is unconditionally true because of `or True`. | [L59](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L59) |
| S16-22 | sources | Saving CCS+ credentials returns 303 and retrieves the submitted username/password. | [L64](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L64) |
| S16-23 | sources | The stored CCS+ login record does not contain its plaintext fixture password. | [L65](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L65) |
| S16-24 | sources | Saving CCS+ credentials causes the fake download to receive them. | [L66](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L66) |
| S16-25 | sources | The page omits the plaintext CCS+ password, displays keep-saved guidance and the saved username. | [L68](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L68) |
| S16-26 | sources | Saving a new CCS+ username with a blank password retains the old password. | [L70](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L70) |
| S16-27 | sources | Saving the sampled invalid CCS+ UID returns HTTP 400. | [L71](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L71) |
| S16-28 | sources | Saving CCS+ credentials with an invalid CSRF token returns HTTP 400. | [L72](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L72) |
| S16-29 | account | Changing page credentials with an incorrect current password returns HTTP 400. | [L75](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L75) |
| S16-30 | account | Changing page credentials with mismatched confirmation returns HTTP 400. | [L76](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L76) |
| S16-31 | account | After changing credentials, the old credentials return 401 and the new credentials return 200. | [L78](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L78) |
| S16-32 | account | changing the login renews the form token; the old one is refused | [L82](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L82) |
| S16-33 | account | Changing only the username keeps the existing password and permits the renamed login. | [L85](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L85) |
| S16-34 | account / sources | Sampled logs contain none of the setup, CCS+ or replacement fixture passwords. | [L87](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_16.py#L87) |

## Coverage limits and reconciliation notes

- Rows 01–04 run only in `import`; all remaining rows run in `fresh`. `tests/run.sh` does not separately run import mode.
- Row 21 cannot fail (`... or True`), so it supplies no status-message coverage. Do not turn it into a verified requirement.
- Row 19 measures a performance threshold under the suite’s environment, not a cross-platform service guarantee.
- Hash/encryption checks largely use absence of fixture plaintext, not cryptographic algorithm verification.
- Row 20 checks for a form and absence of a legacy hidden-node spelling, not rendered browser visibility.
- Overlaps: suite 18 source login rendering; suite 19 password-edit UI.
