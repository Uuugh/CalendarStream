# Requirements: Google plugin (API client)

The Google plugin: the access to Google that every Google connection requires. Common plugin rules are in plugins.md.
Terms: the **API client** is the Google client the user creates once in Google Cloud.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| PGAP-01 | proposed | The user sets up access to Google once, with their own Google client, and is guided through it. | — | — |
| PGAP-01.a | proposed | Until the API client is set up and accepted (CON-01.b), connecting is unavailable and setup guidance is offered. | — | S12-01, S12-02, S39-01, S39-02, S51-01, S51-03, S39-16 |
| PGAP-01.b | proposed | Client setup requires a well-formed client ID and an initial secret. Invalid or missing values are identified. | — | S12-03, S12-04, S48-01, S48-02 |
| PGAP-01.c | proposed | Changing the Google client ID with the secret left blank keeps the previous secret; secrets are protected as in ACC-05. | — | S12-10, S14-18 |
| PGAP-01.d | proposed | Removing the API client clears the configured and connected state and returns setup to Not set up; its effect on Google connections is CGOW-01.r. | — | S12-09, S46-06, S48-17, S48-18, S54-14, changelog_gaps_601-900:L17, changelog_gaps_901-1200:L17 |
| PGAP-01.e | proposed | The Google client cannot be changed while an account is connected, because the sign-in belongs to that client; the user disconnects first (removing the client disconnects its accounts, PGAP-01.d). | — | S12-22 |
| PGAP-01.f | proposed | Saved refresh credentials, the client secret and pending sign-in verifiers are protected as ACC-05 says. | — | S12-20, changelog_gaps_1-300:L23 |
| PGAP-01.g | proposed | Client checking distinguishes accepted credentials, rejected secrets, unknown client IDs and an unreachable service; unreachable is not reported as invalid credentials. | — | S14-13, S14-15, S14-16, S14-17, S19-20, S19-22, S48-03, S48-04, S54-13 |
| PGAP-01.h | proposed | Without an explicit public address, setup derives the callback from the request host; unsupported public IP/local-host addresses do not advertise an unusable callback and instead request public-address setup. Public-address rules: SET-04. | — | S23-04, S23-17, S23-18 |
| PGAP-01.i | proposed | A missing authorized redirect is reported separately from client acceptance and supplies the exact callback to authorize. Changing the public address invalidates stale address feedback. | — | S23-07, S23-08, S23-10, S23-11, S23-12, S23-22, S48-05, S48-06, S67-26 |
| PGAP-01.j | proposed | Setup provides the callback address and ordered guidance through the Google project, API, consent screen and client, and for redirect mismatch, denied access and invalid client errors. It tells the user to publish the OAuth app or add the signing-in account as a test user, covers a deleted client and repeated reconnection from an app left in testing, and uses the saved support email or asks for the user's Gmail support email. | — | S24-02, S24-03, S24-05, S25-02, S25-05, changelog_gaps_1501-1800:L28, changelog_gaps_1501-1800:L29 |
| PGAP-01.k | proposed | Guided Google setup confirms that the callback is authorized before continuing to consent. | — | changelog_gaps_601-900:L44 |
| PGAP-01.l | proposed | Google setup provides a copyable assisted-setup request and a guided route through the required provider configuration. | — | changelog_gaps_901-1200:L21, readme_gaps:L85 |
| PGAP-01.m | proposed | Changing or adding a domain or the public address, with the API client already set up, shows a notice pointing at the Google plugin's setup guidance, since the API always becomes unhealthy. | — | F56, S67-25 |
| PGAP-02 | proposed | Failures of Google's service are retried and reported honestly, whichever connection is affected. | — | — |
| PGAP-02.a | proposed | An expired access credential is refreshed and the call retried once; if that does not recover it, the next try is at the next scheduled synchronization and the page reports that timing. Revoked consent or a permission refusal requires reauthorization without an automatic retry. | — | S72-08, S72-09, S72-10, S72-11, S73-08, S12-25, changelog_gaps_1-300:L19 |
| PGAP-02.b | proposed | Transient failures, including rate limits, are retried with a wait that starts at the first wait in DEF-01, doubles each attempt up to the longest wait, is randomized upward by the jitter in DEF-01, and stops after the number of attempts in DEF-01; a longer wait asked for by the server (Retry-After) is honored. | — | S72-12, S72-13, S72-14, S72-15, S72-16, S73-02, S73-05, S73-06, S12-26 |
| PGAP-02.c | proposed | A missing calendar pauses recovery rather than retrying at once; an invalid event or a conflict does not make the account unhealthy. An unknown or unexpected failure is reported as unknown (degraded), never as success, and gets one automatic retry. | — | S72-17, S72-18, S72-19, S73-10, S68-12, S68-13 |
| PGAP-02.d | proposed | Upstream Google refusals preserve Google’s explanation in diagnostic feedback. | — | changelog_gaps_601-900:L15, readme_gaps:L66 |
| PGAP-01.n | proposed | A client ID is trimmed before it is checked; it is valid when it has the length and characters in DEF-01 (Google client ID); any other value is refused with msg:thatDoesnTLookLike. | — | R5 gap |
| PGAP-01.o | proposed | A client secret is trimmed; one longer than the length in DEF-01 or containing whitespace is refused with msg:thatDoesnTLookLike2. | — | R5 gap |
| PGAP-01.p | proposed | A blank secret is refused with msg:enterTheClientSecretToo when none is saved; a saved secret is never shown again. | — | R5 gap |
| PGAP-01.q | proposed | A saved secret that cannot be decrypted reads as blank. | — | R5 gap |
| PGAP-01.r | proposed | The API client counts as configured when both its ID and its secret are not empty. | — | R5 gap |
| PGAP-01.s | proposed | Saving a new client clears the cached access credential and the error shown on the first account. | — | R5 gap |
| PGAP-01.t | proposed | Saving a client records History msg:googleOauthClientSavedShort, where {id} is the start of the client ID before its first period, cut to the length in DEF-01 (Client ID characters shown in History). | — | R5 gap |
| PGAP-01.u | proposed | Removing the client is the trash icon at the end of the credentials row and asks first (UIC-31). | — | R5 gap |
| PGAP-01.v | proposed | Adding a Google connection, making an invitation and pressing Connect while the API client is not set up are refused with msg:googleNeedsApiSync. | — | R5 gap |
| PGAP-01.w | proposed | One client serves the whole installation; the setup guide says how many people can sign in through it while the app is unverified (DEF-01) and ends with Google's error list and what fixes each. | — | R5 gap |
| PGAP-01.x | proposed | Report a problem says whether Google is connected and leaves out the client ID, credentials and secrets (DIA-02.c, ACC-05). | — | R5 gap |
| PGAP-02.e | proposed | A refusal for an expired access credential drops the cached one and retries at once when the credential was issued longer ago than the margin in DEF-01 (Google access credential margin). | — | R5 gap |
| PGAP-02.f | proposed | When every attempt fails, the user is told msg:googleCalendarIsBusyCalendarstream and the failure counts as transient. | — | R5 gap |
| PGAP-02.g | proposed | A conflict answer is reported at once and is not retried. | — | R5 gap |
| PGAP-02.h | proposed | Any other refusal is reported as msg:googleCalendarAnsweredTo ({code} the status, {reason} the first reason in Google's error list, {request} the method and path); Google's message parts are joined and cut to the length in DEF-01, the status is carried with the failure and the start of Google's answer, to the length in DEF-01, is logged. | — | R5 gap |
| PGAP-02.i | proposed | Every call to Google gives up after the time limits in DEF-01 (Google call time limits). | — | R5 gap |
| PGAP-02.j | proposed | A call that cannot reach Google is reported as msg:couldnTReachGoogleCalendar ({error} the kind of failure); revoked consent as msg:googleNoLongerAcceptsCalendarstream2. | — | R5 gap |
| PGAP-02.k | proposed | A failure is classified as one kind: token expired, consent revoked, rate limit, transient, permission, calendar missing, event invalid, conflict or unknown; the first matching rule wins. | — | R5 gap |
| PGAP-02.l | proposed | Classification rules: revoked consent is consent revoked; a missing calendar is calendar missing; a conflict is conflict; an error that is not Google's is unknown; otherwise by Google's status: 401 token expired, 403 or a rejected client permission, 429 rate limit, 404 or 410 calendar missing, 409 conflict, 5xx or a transient failure transient, 400 event invalid, anything else unknown. | — | R5 gap |
| PGAP-02.m | proposed | A failed synchronization is not tried a second time inside the same run, because the calls were already retried. | — | R5 gap |
| PGAP-02.n | proposed | History gets one line for each new problem, not one at every retry. | — | R5 gap |
| PGAP-03 | proposed | Setup checks the client and the callback address with Google and remembers each answer. | — | R5 gap |
| PGAP-03.a | proposed | Each check stores whether it passed (yes, no or unknown), its message, its time (UTC), the callback address used and whether Google lists that address (yes, no or unknown). | — | R5 gap |
| PGAP-03.b | proposed | The address check sends Google a sign-in request that it does not follow, carrying the client ID, the callback address, offline access, forced consent and an S256 challenge. | — | R5 gap |
| PGAP-03.c | proposed | An answer that names an invalid, deleted or unauthorized client gives the verdict unknown. | — | R5 gap |
| PGAP-03.d | proposed | An answer that succeeds or redirects to anywhere but Google's sign-in error page gives the verdict listed; any other answer, or no answer, gives unknown. | — | R5 gap |
| PGAP-03.e | proposed | The verdict is saved with the last check, keeping that check's result and message. | — | R5 gap |
| PGAP-03.f | proposed | The callback address is the public address followed by /google/callback and must be listed exactly in the client's authorized redirect addresses. | — | R5 gap |
| PGAP-03.g | proposed | A callback address is acceptable when it is https with a host that is not a bare IP address and does not end in .local, or when its host is localhost or 127.0.0.1 with any scheme. | — | R5 gap |
| PGAP-03.h | proposed | A public address whose host differs from the host the page is open at, other than localhost, 127.0.0.1 or an IP address, is reported with msg:yourPublicAddressIsBut ({public}, {here}), to catch typing mistakes. | — | R5 gap |
| PGAP-04 | proposed | Connect runs four steps in order, shows each in its status box and stops at the first that fails, naming the fix. | — | R5 gap |
| PGAP-04.a | proposed | The steps are save, client, address and go; their working words are msg:googleStepSaving, msg:googleStepChecking and msg:googleStepCheckingAddress, and a finished step shows msg:healthy (UIC-28). | — | R5 gap |
| PGAP-04.b | proposed | Step save stores a typed client ID that differs from the saved one and any typed secret (PGAP-01.n); when the client is still not configured it stops with msg:googleClientValuesNeeded and shows the guide. | — | R5 gap |
| PGAP-04.c | proposed | Step client stops with msg:googleClientFix ({message} the check's message) and opens Google Cloud's client page when the client is not accepted; when the verdict is unknown it stops showing the check's message, or msg:googleCouldntCheckClient, and offers to try again. | — | R5 gap |
| PGAP-04.d | proposed | Step address stops with msg:googlePublicAddressFix when the callback address is not acceptable (PGAP-03.g). | — | R5 gap |
| PGAP-04.e | proposed | When Google does not list the callback address, step address records a warning in History with msg:googleRedirectNotListed ({uri}) and stops with msg:googleAddressNotOnClient ({uri}), offering Copy and Open. | — | R5 gap |
| PGAP-04.f | proposed | Step address passes when the verdict is listed or unknown; it is confirmed when the verdict is listed. | — | R5 gap |
| PGAP-04.g | proposed | Step go records History msg:googleApiSyncSetUp and one line (msg:googleNameText, {text} the readiness text of CGOW-06.e) for each Google connection that is not working, as a warning when it has synced before and as information when it has not; it starts no sign-in. | — | R5 gap |
| PGAP-04.h | proposed | A step name that is not one of the four is refused with msg:googleUnknownStep. | — | R5 gap |
| PGAP-05 | proposed | The access credential is obtained, kept and renewed so that every call to Google can use it. | — | R5 gap |
| PGAP-05.a | proposed | A credential request that cannot reach Google fails as transient with msg:couldnTReachGoogle ({error}); it succeeds when Google answers success with an access credential. | — | R5 gap |
| PGAP-05.b | proposed | When Google rejects the client the failure reads msg:googleRejectedTheOauthClient; when it says the redirect address is not authorized, msg:googleSaysTheRedirectUri; any other error reads msg:googleSignInFailed ({error} Google's error or the status). | — | R5 gap |
| PGAP-05.c | proposed | An access credential is reused until the margin in DEF-01 before it expires and then renewed with the refresh credential; simultaneous requests share one renewal. | — | R5 gap |
