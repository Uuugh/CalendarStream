# Requirements: Google plugin (API client)

The Google plugin: the access to Google that every Google connection requires. Common plugin rules are in plugins.md.
Terms: the **API client** is the Google client the user creates once in Google Cloud.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| GAP-01 | proposed | The user sets up access to Google once, with their own Google client, and is guided through it. | — | — |
| GAP-01.a | proposed | A Google destination can be added only once the API client is set up and accepted; before that, connecting is unavailable and setup guidance is offered. | — | S12-01, S12-02, S39-01, S39-02, S51-01, S51-03, S39-16 |
| GAP-01.b | proposed | Client setup requires a well-formed client ID and an initial secret. Invalid or missing values are identified. | — | S12-03, S12-04, S48-01, S48-02 |
| GAP-01.c | proposed | Changing the Google client ID with the secret left blank keeps the previous secret; secrets are protected as in ACC-05. | — | S12-10, S14-18 |
| GAP-01.d | proposed | Removing the API client clears the configured and connected state and returns setup to Not set up. The Google accounts are disconnected with their remote calendars kept, and the page reports that destinations need their account connections restored after the client is set up again. | — | S12-09, S46-06, S48-17, S48-18, S54-14, changelog_gaps_601-900:L17, changelog_gaps_901-1200:L17 |
| GAP-01.e | proposed | The Google client cannot be changed while an account is connected, because the sign-in belongs to that client; the user disconnects first (removing the client disconnects its accounts, GAP-01). | — | S12-22 |
| GAP-01.f | proposed | Saved refresh credentials, the client secret and pending sign-in verifiers are protected as ACC-05 says. | — | S12-20, changelog_gaps_1-300:L23 |
| GAP-01.g | proposed | Client checking distinguishes accepted credentials, rejected secrets, unknown client IDs and an unreachable service; unreachable is not reported as invalid credentials. | — | S14-13, S14-15, S14-16, S14-17, S19-20, S19-22, S48-03, S48-04, S54-13 |
| GAP-01.h | proposed | Without an explicit public address, setup derives the callback from the request host; unsupported public IP/local-host addresses do not advertise an unusable callback and instead request public-address setup. Public-address rules: SET-04..SET-04. | — | S23-04, S23-17, S23-18 |
| GAP-01.i | proposed | A missing authorized redirect is reported separately from client acceptance and supplies the exact callback to authorize. Changing the public address invalidates stale address feedback. | — | S23-07, S23-08, S23-10, S23-11, S23-12, S23-22, S48-05, S48-06, S67-26 |
| GAP-01.j | proposed | Setup provides the callback address and ordered guidance through the Google project, API, consent screen and client, and for redirect mismatch, denied access and invalid client errors. It tells the user to publish the OAuth app or add the signing-in account as a test user, covers a deleted client and repeated reconnection from an app left in testing, and uses the saved support email or asks for the user's Gmail support email. | — | S24-02, S24-03, S24-05, S25-02, S25-05, changelog_gaps_1501-1800:L28, changelog_gaps_1501-1800:L29 |
| GAP-01.k | proposed | Guided Google setup confirms that the callback is authorized before continuing to consent. | — | changelog_gaps_601-900:L44 |
| GAP-01.l | proposed | Google setup provides a copyable assisted-setup request and a guided route through the required provider configuration. | — | changelog_gaps_901-1200:L21, readme_gaps:L85 |
| GAP-01.m | proposed | API setup completion, and its History message, identify each Google connection that needs sign-in, has a sync error or has not completed its first sync. | — | changelog_gaps_1-300:L22 |
| GAP-01.n | proposed | Repeating a Google setup submission does not create duplicate or orphan destinations. | — | changelog_gaps_1-300:L26 |
| GAP-02 | proposed | Failures of Google's service are retried and reported honestly, whichever connection is affected. | — | — |
| GAP-02.a | proposed | An expired access credential is refreshed and the call retried once; if that does not recover it, the next try is at the next scheduled synchronization and the page reports that timing. Revoked consent or a permission refusal requires reauthorization without an automatic retry. | — | S72-08, S72-09, S72-10, S72-11, S73-08, S12-25, changelog_gaps_1-300:L19 |
| GAP-02.b | proposed | Transient failures, including rate limits, are retried with a wait that starts at the first wait in DEF-01, doubles each attempt up to the longest wait, is randomized upward by the jitter in DEF-01, and stops after the number of attempts in DEF-01; a longer wait asked for by the server (Retry-After) is honored. | — | S72-12, S72-13, S72-14, S72-15, S72-16, S73-02, S73-05, S73-06, S12-26 |
| GAP-02.c | proposed | A missing calendar pauses recovery rather than retrying at once; an invalid event or a conflict does not make the account unhealthy. An unknown or unexpected failure is reported as unknown (degraded), never as success, and gets one automatic retry. | — | S72-17, S72-18, S72-19, S73-10, S68-12, S68-13 |
| GAP-02.d | proposed | Upstream Google refusals preserve Google’s explanation in diagnostic feedback. | — | changelog_gaps_601-900:L15, readme_gaps:L66 |
