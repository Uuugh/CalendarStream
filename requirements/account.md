# Requirements: account

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.
Terms used below (defined once):
- **Address**: the visitor's network address as reported by a trusted proxy (DEP-03).
- **Trusted network**: a network listed in ACC-07.b.
- **Known browser**: a browser holding the signed cookie issued at a successful sign-in (ACC-07.c).
- **Outside address**: an address that is not on a trusted network, not a known browser's, and has not signed in successfully recently (ACC-07.f).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| ACC-01 | proposed | A new installation is set up by creating the page login with the setup code; once it exists, setup is closed. | — | — |
| ACC-01.a | proposed | Before a page login exists, page and status requests lead to initial setup; feed and health endpoints remain accessible. | — | S16-05, S16-06, S16-07 |
| ACC-01.b | proposed | Initial setup requires its generated setup code, written as two groups of four hexadecimal characters. | — | S16-08, S16-09, S16-13 |
| ACC-01.g | proposed | The setup code is accepted in any letter case and with or without the dash between its groups. | — | S16-08, S16-09, S16-13 |
| ACC-01.h | proposed | An incorrect setup code creates no login. | — | S16-08, S16-09, S16-13 |
| ACC-01.c | proposed | Initial setup explains how to retrieve its setup code with a command that works independently of the chosen service name; incorrect-code guidance repeats that retrieval instruction (ACC-01.b, DEP-02). | — | changelog_gaps_1801-2100:27 |
| ACC-01.d | proposed | Initial setup refuses a mismatched password confirmation, a password that does not meet the password requirements (ACC-04) and a username containing a space. | — | S16-10, S16-11, S16-12 |
| ACC-01.e | proposed | After initial login creation, setup is closed and the creating user is signed in. | — | S16-15, S16-16 |
| ACC-02 | proposed | A person signs in to see or change anything on the page, and can sign out. | — | — |
| ACC-02.a | proposed | An unauthenticated page request goes to sign-in and does not expose destination content; a successful session can read the page. Any change to settings, including update settings, requires that signed-in session. | — | S16-17, S49-47, S49-51, S51-29, S22-14 |
| ACC-02.b | proposed | An incorrect login password is not accepted; a correct one establishes a session. | — | S49-48, S49-49, S49-50 |
| ACC-02.f | proposed | After sign-in the user goes to the page they asked for only when it is a path on this site. A destination that starts with //, contains a backslash, or contains a tab, line break or other control character (browsers drop those, so "/<tab>/other.site" would go to another site) is not followed; the user goes to the home page instead. The query and fragment of a followed destination are kept. | — | S49-48, S49-49, S49-50 |
| ACC-02.c | proposed | Signing out removes page access; subsequent page requests return to sign-in. Authenticated HTTP Basic remains supported for the status API. | — | S49-52, S49-53 |
| ACC-02.d | proposed | A successful page sign-in establishes a session valid for the time in DEF-01. | — | readme_gaps:73 |
| ACC-02.e | proposed | Login settings identify the saved username and the signed-in state. | — | S16-18, S19-50, S19-51, S28-12 |
| ACC-03 | proposed | The user can change the page login, and the change takes effect for every browser. | — | — |
| ACC-03.a | proposed | Changing credentials, including entering a replacement password, requires the correct current password and a matching new-password confirmation. A username change that fails for a wrong current password leaves the saved username unchanged and identifies the current-password error (UI-19). | — | S16-29, S16-30, S64-14 |
| ACC-03.b | proposed | After a credential change, the old credentials are refused and the new credentials are accepted. Changing only the username retains the existing password. | — | S16-31, S16-33 |
| ACC-03.c | proposed | Changing the login renews the form security token and invalidates the previous token. | — | S16-32 |
| ACC-03.d | proposed | Changing the page login invalidates all previously issued browser sessions. | — | readme_gaps:73, changelog_gaps_601-900:30 |
| ACC-04 | proposed | A new password must meet the password requirements, and the user sees how strong it is and which requirements it still misses. | — | — |
| ACC-04.a | proposed | A password is accepted only if it has at least the minimum length and at least the minimum number of capital letters, lowercase letters, numbers and special characters set in the password requirements (SET-06; the defaults and floors are in DEF-01). A character and a special character are as DEF-03 defines them. | — | S63-06, S63-07, S63-08 |
| ACC-04.b | proposed | The strength bar (UI-18) is shown when a password is created or changed, with a hint naming the requirements not yet met. Sign-in only verifies the saved password (ACC-02.b). | — | changelog_gaps_301-600:26 |
| ACC-04.d | proposed | The password requirements apply when a password is created or changed (initial setup, replacement), not to a password already saved; changing the requirements does not sign anyone out. | — | — |
| ACC-05 | proposed | Passwords, Google client secrets and notification tokens are protected: stored safely and never exposed. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.a | proposed | A sign-in password (page login, setup, replacement) is stored only as a one-way hash, never in plaintext. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.b | proposed | A credential the app must send on (the CCS+ password, Google client secret and tokens) is stored encrypted with a key from the database password; after the database password changes they cannot be read until entered again (GOW-01). | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.c | proposed | A secret is never written to a log. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.d | proposed | A secret is shown on a page only when a user who is authorized to see secrets turns on the Show secrets switch in History (HIS-04). | — | — |
| ACC-06 | proposed | Repeated failed sign-ins from one address lock that address for a time. | — | — |
| ACC-06.a | planned | After the number of failed sign-ins in DEF-01 from one address, further attempts from it are refused for the lock time in DEF-01. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-06.b | proposed | An incorrect initial-setup code counts toward the same per-address failure limit as an incorrect page login (ACC-06.a). | — | readme_gaps:35 |
| ACC-06.c | proposed | Concurrent failed sign-ins are all counted toward the applicable failure limits without causing internal errors (ACC-06, ACC-07). | — | changelog_gaps_1501-1800:31 |
| ACC-06.d | proposed | An address remains blocked until its lockout expires; recording failures from other addresses does not remove an active block early (ACC-06.a). | — | changelog_gaps_1501-1800:33 |
| ACC-06.e | proposed | Restarting CalendarStream clears the active sign-in lockout state. | — | readme_gaps:75 |
| ACC-06.f | proposed | A successful sign-in clears that address's failure count. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-06.g | proposed | Failure records are kept only while needed: at most the number in DEF-01 at once, forgetting addresses that are not locked out first. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07 | proposed | Many failed sign-ins across addresses start a global block that refuses new outside addresses, while trusted and known visitors keep access. | — | — |
| ACC-07.a | planned | The number of failed sign-ins from all addresses together within the window in DEF-01 starts a global block. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.h | proposed | A global block ends when the failures within that window fall below the number in DEF-01. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.e | planned | During a global block, an outside address is refused even with the right password. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.f | planned | An address that signed in successfully within the trusted-address period in DEF-01 is not an outside address. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.b | approved | During the global block, requests from the trusted networks in DEF-01 and from CalendarStream's own public domain are not blocked. An address is judged from what a trusted proxy reports (DEP-03). | — | S53-11, S53-12; Developer, Nov 17 |
| ACC-07.c | proposed | A successful login issues a signed known-browser cookie; a forged signature is refused. | — | S55-24, S55-25, S55-26 |
| ACC-07.d | proposed | A known browser can authenticate during the global block, but does not bypass a block applied specifically to its own address. A new browser remains blocked. | — | S55-29, S55-30, S55-31 |
| ACC-07.g | proposed | The record of addresses that signed in successfully keeps at most the number in DEF-01 (the oldest are forgotten first). | — |  |
| ACC-08 | proposed | When failed sign-ins lock the administrator out, a single-use recovery link restores access. | — | — |
| ACC-08.a | proposed | Reaching a global block records one recovery warning (HIS-01) pointing the administrator to the container log. | — | S53-09, S55-27 |
| ACC-08.d | proposed | The warning includes an unlock link that works once and is valid for the time in DEF-01. | — | S53-09, S55-27 |
| ACC-08.b | proposed | A fresh recovery link uses the configured public address, marks the visiting browser as known and directs it to login, allowing that browser to authenticate. | — | S55-32, S55-33, S55-34 |
| ACC-08.c | proposed | Recovery links are single-use, and an expired link is not accepted. | — | S55-35, S55-36 |
| ACC-09 | proposed | Changes to the page are accepted only from the page itself, and page responses carry basic browser protections. | — | — |
| ACC-09.a | proposed | Initial-setup and signed-in form tokens are distinct; a setup token cannot authorize a public-address change. Mismatched form tokens are refused. | — | S23-02, S23-03, S32-06, S77-23, S77-24, S77-25 |
| ACC-09.b | proposed | Cross-site form changes are refused and leave the saved value unchanged. | — | S23-23 |
| ACC-09.c | proposed | Page responses restrict framing to the same origin, prevent content-type sniffing and suppress referrer disclosure. | — | S23-25, S36-37 |

Future: a Users feature will decide which users may see secrets in the logs (log visibility permissions, HIS-04, GOW-01); until then the one signed-in user is authorized. (Developer, Nov 18)
