# Requirements: account

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | was |
|---|---|---|---|---|
| ACC-16 | planned | Sign-in failures are limited: 5 failures from one address lock that address for 15 minutes; 25 failures from all addresses together within 15 minutes start a global block, during which a new outside address is refused even with the right password. An address that signed in successfully in the last 7 days can still authenticate. (The Developer, Nov 17; the Python app uses 50 together, so this changes it.) | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-17 |  | During the global block, requests from the networks 192.168.0.0 and 10.10.0.0 (taken as the /16 ranges) and from loopback, and from CalendarStream's own public domain, are not blocked. An address is judged from what a trusted proxy reports (DEP-07). | — | S53-11, S53-12; Developer, Nov 17 |
| ACC-01 | proposed | A legacy page login is imported with a hashed password; saved page passwords are not stored in plaintext. | — | S16-01, S16-04, S16-14 |
| ACC-02 | proposed | Before a page login exists, page and status requests lead to initial setup; feed and health endpoints remain accessible. | — | S16-05, S16-06, S16-07 |
| ACC-03 | proposed | Initial setup requires its generated code, formatted as two groups of four hexadecimal characters. Code entry ignores case and the separating dash; an incorrect code is refused without creating a login. | — | S16-08, S16-09, S16-13 |
| ACC-04 | proposed | Initial setup refuses a mismatched confirmation and a username containing a space. A weak or short password is never refused; its strength is shown as in UI-18. | — | S16-10, S16-11, S16-12 |
| ACC-05 | proposed | After initial login creation, setup is closed and the creating user is signed in. | — | S16-15, S16-16 |
| ACC-06 | proposed | An unauthenticated page request goes to sign-in and does not expose destination content. A successful session can read the page. | — | S16-17, S49-47, S49-51, S51-29 |
| ACC-07 | proposed | Login settings identify the saved username and signed-in state; entering a replacement password requires the current password. | — | S16-18, S19-50, S19-51, S28-12 |
| ACC-08 | proposed | Changing credentials requires the correct current password and matching new-password confirmation. A refused username change leaves the saved username unchanged and identifies the current-password error. | — | S16-29, S16-30, S64-14 |
| ACC-09 | proposed | After a credential change, the old credentials are refused and the new credentials are accepted. Changing only the username retains the existing password. | — | S16-31, S16-33 |
| ACC-10 | proposed | Changing the login renews the form security token and invalidates the previous token. | — | S16-32 |
| ACC-11 | proposed | Passwords (page login, setup, CCS+, replacement), Google client secrets and notification tokens are stored protected, never shown on a page and never written to the logs. Other features refer to this rule. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-12 | proposed | Changing update settings requires page authentication. This is shared change authorization; other features should reference this rule rather than repeat it. | — | S22-14 |
| ACC-13 | proposed | Initial-setup and signed-in form tokens are distinct; a setup token cannot authorize a public-address change. Mismatched form tokens are refused. | — | S23-02, S23-03, S32-06, S77-23, S77-24, S77-25 |
| ACC-14 | proposed | Cross-site form changes are refused and leave the saved value unchanged. | — | S23-23 |
| ACC-15 | proposed | Page responses restrict framing to the same origin, prevent content-type sniffing and suppress referrer disclosure. | — | S23-25, S36-37 |
| ACC-18 | proposed | An incorrect login password is refused. Successful login establishes a session and redirects to a safe local destination. | — | S49-48, S49-49 |
| ACC-19 | proposed | Post-login navigation rejects protocol-relative external destinations and hidden-tab redirect tricks, while preserving the checked local query and fragment. | — | S49-50 |
| ACC-20 | proposed | Signing out removes page access; subsequent page requests return to sign-in. Authenticated HTTP Basic remains supported for the status API. | — | S49-52, S49-53 |
| ACC-21 | proposed | Reaching the global login-failure limit records one recovery warning directing the administrator to the container log. The warning includes an unlock link and explains that it is valid for 24 hours (the Python app uses one hour). History owns presentation of recovery guidance under HIS-16. | — | S53-09, S55-27 |
| ACC-22 | proposed | A successful login issues a signed known-browser cookie; a forged signature is refused. | — | S55-24, S55-25, S55-26 |
| ACC-23 | proposed | A known browser can authenticate during the global block, but does not bypass a block applied specifically to its own address. A new browser remains blocked. | — | S55-29, S55-30, S55-31 |
| ACC-24 | proposed | A fresh recovery link uses the configured public address, marks the visiting browser as known and directs it to login, allowing that browser to authenticate. | — | S55-32, S55-33, S55-34 |
| ACC-25 | proposed | Recovery links are single-use and expired links are refused. The oracle checks an already-expired link, not the precise one-hour expiry boundary. | — | S55-35, S55-36 |
| ACC-26 | proposed | A page password is never refused for its strength. The UI-18 hint recommends at least twelve characters, a capital letter, a number and a symbol, and no character repeated three or more times consecutively (doubled letters are fine). | — | S63-06, S63-07, S63-08 |
| ACC-27 | proposed | Anonymous users cannot read Google traffic diagnostics. Diagnostic content belongs to the existing Google/diagnostics requirements. | — | S68-17 |

## Notes from the draft

### Not requirements

The following observations are excluded or mapped to another owner rather than duplicated.

- S16-02: Legacy CCS+ credential import and its activity record are owned by sources (SRC-06), not a second account requirement.
- S16-03: Legacy CCS+ credential import and its activity record are owned by sources (SRC-06), not a second account requirement.
- S16-19: Environment-specific performance sample for five authenticated requests; does not establish a portable latency requirement.
- S21-11: Field alignment is a theme measurement; User name wording is a shared field-label observation, not a separate login capability.
- S35-09: Static parent-path request rejection belongs to shared asset-serving security; one sampled path does not establish the complete traversal policy.
- S39-09: Authenticated-page compression header policy belongs to shared HTTP security, not credential behavior; retained for shared review.
- S55-39: No window.opener in a new tab is shared external-navigation security, not an account-specific rule.
- S63-09: Failure sentinel and unconditional exception-handler success marker; not independent password validation evidence.
- S63-10: Failure sentinel and unconditional exception-handler success marker; not independent password validation evidence.
- S64-11: Settings form structure and signed-in/out wording are mapped to existing SET-06 and account signed-in state above, not duplicated UI mechanics.
- S65-24: Icon variables and CSS-selector source checks are Python presentation implementation details.
- S65-25: Icon variables and CSS-selector source checks are Python presentation implementation details.
- S81-07: Settings dialog navigation and field visibility are shared mechanics (SET-06, UI-01/UI-02), not new account behavior.
- S81-08: Settings dialog navigation and field visibility are shared mechanics (SET-06, UI-01/UI-02), not new account behavior.

### Coverage and open questions

All 81 account-candidate rows are accounted for in 27 proposed requirements and
14 excluded/shared-owner mappings. The exact block budget, reset interval, trusted-address
policy and expiry boundary remain questions; finite security samples are not comprehensive audits.
No real credentials or schedules are included. No application suites were run locally.
