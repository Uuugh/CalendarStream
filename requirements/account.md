# Requirements: account

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
| ACC-01.d | proposed | Initial setup refuses a mismatched password confirmation, a password that does not meet the password requirements (ACC-04) and a user name that is empty, longer than the length in DEF-01 or contains a space, a colon or other whitespace (msg:chooseAUserNameWithout). | — | S16-10, S16-11, S16-12 |
| ACC-01.e | proposed | After initial login creation, setup is closed and the creating user is signed in. | — | S16-15, S16-16 |
| ACC-01.i | proposed | A setup code is generated each time the app starts and finds no page login; a new start replaces the earlier code; the code is kept in memory only and is valid for that run. | — | R1 gap |
| ACC-01.j | proposed | Initial setup checks the setup code first; a problem with the user name or password is reported after a correct code. The user name is checked first, then the password requirements, then the password confirmation. | — | R1 gap |
| ACC-01.k | proposed | The initial-setup page has the title, intro and button of msg:welcome, msg:welcomeFirstCreateTheLogin and msg:createLogin; its fields are Setup code, User name, Password and Password again. | — | R1 gap |
| ACC-01.l | proposed | Creating the login records a History entry msg:statusPageLoginCreatedFor ({user} is the new user name), renews the form security token (ACC-03.c) and marks the browser as known (ACC-07.c). | — | R1 gap |
| ACC-02 | proposed | A person signs in to see or change anything on the page, and can sign out. | — | — |
| ACC-02.a | proposed | An unauthenticated page request goes to sign-in and does not expose destination content; a successful session can read the page. Any change to settings, including update settings, requires that signed-in session. | — | S16-17, S49-47, S49-51, S51-29, S22-14 |
| ACC-02.b | proposed | An incorrect login password is not accepted; a correct one establishes a session. | — | S49-48, S49-49, S49-50 |
| ACC-02.g | proposed | The sign-in page has a User name field (length limit in DEF-01), a Password field with Show/Hide (UIC-38) and a button msg:signInAction; the cursor starts in User name, or in Password after a failed sign-in that kept the user name. | — | R1 gap |
| ACC-02.h | proposed | A wrong sign-in shows the form again with the typed user name kept and the message msg:signInWrong, which never says whether the user name or the password was wrong. | — | R1 gap |
| ACC-02.i | proposed | A signed-in visitor who opens the sign-in page goes to the page they asked for (ACC-02.f). | — | R1 gap |
| ACC-02.j | proposed | An unauthenticated request that is not a page request (a background request from the page) is answered 401 with msg:signInAgainReloadThePage. | — | R1 gap |
| ACC-02.f | proposed | After sign-in the user goes to the page they asked for only when it is a path on this site. A destination that starts with //, contains a backslash, or contains a tab, line break or other control character (browsers drop those, so "/<tab>/other.site" would go to another site) is not followed; the user goes to the home page instead. The query and fragment of a followed destination are kept. | — | S49-48, S49-49, S49-50 |
| ACC-02.c | proposed | Signing out removes page access; subsequent page requests return to sign-in. Authenticated HTTP Basic remains supported for the status API. | — | S49-52, S49-53 |
| ACC-02.d | proposed | A successful page sign-in establishes a session valid for the time in DEF-01. | — | readme_gaps:73 |
| ACC-02.k | proposed | The session cookie cannot be read by the page script, is sent only to this site (SameSite lax) and is marked secure when the request arrived over HTTPS, directly or through a trusted proxy. | — | R1 gap |
| ACC-02.l | proposed | Sessions are signed with a random key of the size in DEF-01 kept in the database; a missing or too-short key is replaced by a new one. | — | R1 gap |
| ACC-02.m | proposed | HTTP Basic credentials count as a sign-in: a correct pair succeeds, a wrong pair is one failed sign-in (ACC-06), and a request with none counts nothing. | — | R1 gap |
| ACC-02.e | proposed | Login settings identify the saved username and the signed-in state. | — | S16-18, S19-50, S19-51, S28-12 |
| ACC-03 | proposed | The user can change the page login, and the change takes effect for every browser. | — | — |
| ACC-03.a | proposed | Changing credentials, including entering a replacement password, requires the correct current password and a matching new-password confirmation. A username change that fails for a wrong current password leaves the saved username unchanged and identifies the current-password error (UIC-19). | — | S16-29, S16-30, S64-14 |
| ACC-03.b | proposed | After a credential change, the old credentials are refused and the new credentials are accepted. Changing only the username retains the existing password. | — | S16-31, S16-33 |
| ACC-03.c | proposed | Creating or changing the login renews the form security token and invalidates the previous token. | — | S16-32 |
| ACC-03.e | proposed | A wrong current password in Settings is one failed sign-in for the requester's address (ACC-06) and shows the field message msg:theCurrentPasswordIsnT (UIC-19). | — | R1 gap |
| ACC-03.f | proposed | An empty user name field in Login settings keeps the current user name. | — | R1 gap |
| ACC-03.d | proposed | Changing the page login invalidates all previously issued browser sessions. | — | readme_gaps:73, changelog_gaps_601-900:30 |
| ACC-04 | proposed | A new password must meet the password requirements, and the user sees how strong it is and which requirements it still misses. | — | — |
| ACC-04.a | proposed | A password is accepted only if it has at least the minimum length and at least the minimum number of capital letters, lowercase letters, numbers and special characters set in the password requirements (SET-06; the defaults and floors are in DEF-01). A character and a special character are as DEF-03 defines them. | — | S63-06, S63-07, S63-08 |
| ACC-04.b | backlog | The strength bar (UIC-18) is shown when a password is created or changed, with the hint msg:passwordNeeds, whose {rules} names the requirements not yet met, joined by semicolons. Sign-in only verifies the saved password (ACC-02.b). | — | changelog_gaps_301-600:26 |
| ACC-04.d | proposed | The password requirements apply when a password is created or changed (initial setup, replacement), not to a password already saved; changing the requirements does not sign anyone out. | — | — |
| ACC-05 | proposed | Passwords, Google client secrets and notification tokens are protected: stored safely and never exposed. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.a | proposed | A sign-in password (page login, setup, replacement) is stored only as a one-way hash, never in plaintext. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.b | proposed | A credential the app must send on (the CCS+ password, Google client secret and tokens) is stored encrypted with a key from the database password; after the database password changes they cannot be read until entered again (CGOW-01). | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.c | proposed | A secret is never written to a log. | — | S16-34, S16-23, S16-25, S12-06, S12-07, S12-08, S70-02, S70-03, S70-04, S20-05 |
| ACC-05.d | proposed | A secret is shown on a page only when a user who is authorized to see secrets turns on the Show secrets switch in History (HIS-04). | — | — |
| ACC-06 | proposed | Repeated failed sign-ins from one address lock that address for a time. | — | — |
| ACC-06.a | proposed | After the number of failed sign-ins in DEF-01 from one address, further attempts from it are refused for the lock time in DEF-01. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-06.h | proposed | The failed sign-in that reaches the limit is itself refused with msg:tooManyFailedAttemptsTry. | — | R1 gap |
| ACC-06.i | proposed | When a lock starts, the address's failure count resets to 0 and the lock lasts the time in DEF-01; later attempts during the lock are refused without being counted and do not extend the lock. | — | R1 gap |
| ACC-06.j | proposed | Starting a lock records one History warning, msg:statusPageLockedForAfter for sign-ins or msg:statusPageLockedForAfter2 for setup codes ({ip} is the address, {n} the limit). | — | R1 gap |
| ACC-06.k | proposed | A correct setup code with an invalid user name or password is not counted as a failed attempt. | — | R1 gap |
| ACC-06.b | proposed | An incorrect initial-setup code counts toward the same per-address failure limit as an incorrect page login (ACC-06.a). | — | readme_gaps:35 |
| ACC-06.c | proposed | Concurrent failed sign-ins are all counted toward the applicable failure limits without causing internal errors (ACC-06, ACC-07). | — | changelog_gaps_1501-1800:31 |
| ACC-06.d | proposed | An address remains blocked until its lockout expires; recording failures from other addresses does not remove an active block early (ACC-06.a). | — | changelog_gaps_1501-1800:33 |
| ACC-06.e | proposed | Restarting CalendarStream clears the active sign-in lockout state. | — | readme_gaps:75 |
| ACC-06.f | proposed | A successful sign-in clears that address's failure count. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-06.g | proposed | Failure records are kept only while needed: at most the number in DEF-01 at once, forgetting addresses that are not locked out first. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07 | proposed | Many failed sign-ins across addresses start a global block that refuses new outside addresses, while trusted and known visitors keep access. | — | — |
| ACC-07.a | proposed | The number of failed sign-ins from all addresses together within the window in DEF-01 starts a global block. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.h | proposed | A global block ends when the failures within that window fall below the number in DEF-01. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.e | proposed | During a global block, an outside address is refused even with the right password. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.f | proposed | An address that signed in successfully within the trusted-address period in DEF-01 is not an outside address. | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-07.b | backlog | During the global block, requests from the trusted networks in DEF-01 and from CalendarStream's own public domain are not blocked. An address is judged from what a trusted proxy reports (DEP-03). | — | S53-11, S53-12; Developer, Nov 17 |
| ACC-07.c | proposed | A successful sign-in, a login creation and a recovery link each issue a signed known-browser cookie valid for the time in DEF-01 from the last sign-in, renewed at each sign-in; a forged signature is refused. | — | S55-24, S55-25, S55-26 |
| ACC-07.d | proposed | A known browser can authenticate during the global block, but does not bypass a block applied specifically to its own address. A new browser remains blocked. | — | S55-29, S55-30, S55-31 |
| ACC-07.i | proposed | The initial-setup form is refused during a global block for every browser, known or not. | — | R1 gap |
| ACC-07.g | proposed | The record of addresses that signed in successfully keeps at most the number in DEF-01 (the oldest are forgotten first). | — |  |
| ACC-08 | proposed | When failed sign-ins lock the administrator out, a single-use recovery link restores access. | — | — |
| ACC-08.a | proposed | Reaching a global block records one recovery warning (HIS-01) pointing the administrator to the container log. | — | S53-09, S55-27 |
| ACC-08.d | proposed | The warning includes an unlock link that works once and is valid for the time in DEF-01. | — | S53-09, S55-27 |
| ACC-08.b | proposed | A fresh recovery link uses the configured public address, marks the visiting browser as known and directs it to login, allowing that browser to authenticate. | — | S55-32, S55-33, S55-34 |
| ACC-08.e | proposed | Using a recovery link records a History entry msg:unlockLinkUsedFrom ({ip} is the visitor's address). | — | R1 gap |
| ACC-08.c | proposed | Recovery links are single-use, and an expired link is not accepted. | — | S55-35, S55-36 |
| ACC-09 | proposed | Changes to the page are accepted only from the page itself, and page responses carry basic browser protections. | — | — |
| ACC-09.a | proposed | Initial-setup and signed-in form tokens are distinct; a setup token cannot authorize a public-address change. Mismatched form tokens are refused. | — | S23-02, S23-03, S32-06, S77-23, S77-24, S77-25 |
| ACC-09.b | proposed | Cross-site form changes are refused and leave the saved value unchanged. | — | S23-23 |
| ACC-09.c | proposed | Page responses restrict framing to the same origin, prevent content-type sniffing and suppress referrer disclosure. | — | S23-25, S36-37 |
| ACC-05.e | proposed | A page password is hashed with scrypt using the cost, block size, parallelism, result length and fresh random salt length in DEF-01 (Password hashing). | — | R6 gap |
| ACC-05.f | proposed | Encrypted credentials use a key derived from the database password and a random salt with the rounds in DEF-01 (Secret encryption); sealing with no database password fails. | — | R6 gap |
| ACC-05.g | proposed | A credential that cannot be decrypted reads as not set: a CCS+ password counts as unset, a Google client secret is empty, and a Google token reports an error text saying it cannot be decrypted. | — | R6 gap |
| ACC-05.h | proposed | A saved secret is never shown again; leaving its field blank keeps the saved one. | — | R6 gap |
