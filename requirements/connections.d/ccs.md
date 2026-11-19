# Requirements: CCS+

The CCS+ connection: the user's own United Airlines schedule, downloaded with their own sign-in (read only; CalendarStream never changes CCS+). Download rules every downloaded connection shares are in `connections.md`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CCCS-01 | proposed | There is one CCS+ connection: the user's own United Airlines schedule. | — | — |
| CCCS-01.c | proposed | CCS+ is a source. | — | — |
| CCCS-01.a | proposed | One CCS+ source can be added; attempting to add a second is refused. | — | S26-05, S26-06 |
| CCCS-01.b | proposed | Removing CCS+ also removes its active saved login. | — | S49-33 |
| CCCS-02 | proposed | The user signs in to CCS+ with their own credentials, which the app keeps safe, so it can read their schedule. | — | — |
| CCCS-02.a | proposed | CCS+ guidance distinguishes Calendar Sync credentials from CCS login credentials and explains enabling CCS+. | — | S18-05, S33-03 |
| CCCS-02.b | proposed | CCS+ setup is available directly with the source when it needs configuration, rather than only in Settings. Successful credential saving returns to that source. | — | S16-20, S18-03, S18-04, S18-07, S27-01 |
| CCCS-02.c | proposed | Missing CCS+ credentials are reported as Setup needed rather than an error, and Sync now is unavailable until credentials are entered. | — | S18-01, S18-02, S18-06 |
| CCCS-02.d | proposed | Credentials are labeled Username. | — | S31-05 |
| CCCS-02.e | proposed | Changing the CCS+ username while leaving the password blank keeps the saved password. | — | S16-26 |
| CCCS-02.f | proposed | An invalid CCS+ username is refused with a username error. | — | S16-27, S28-13 |
| CCCS-02.g | proposed | The saved CCS+ password is protected (ACC-05); the page shows the saved username and explains how to keep its password. | — | S16-23, S16-25, S16-34 |
| CCCS-02.h | proposed | Saved CCS+ credentials are used for the next download. | — | S16-22, S16-24 |
| CCCS-02.i | proposed | Rejected CCS+ credentials show a failure reason beside the credential fields; successful verification reports Validated. Editing the credentials removes stale validation or rejection feedback. | — | S18-08, S18-09, S19-19, S19-47, S19-48, S28-01, S28-08, S28-09, S28-10, S28-11 |
| CCCS-02.j | proposed | Credential saving reports saving/verification progress and a saved acknowledgement before successful validation. Shared save/cancel interaction follows SET-01; this rule specifies the verification outcome. | — | S28-05, S28-06, S28-07 |
| CCCS-02.k | proposed | CCS+ setup guidance explains enabling trips as one event and the other calendar options, setting a dedicated Calendar Sync password, and completing the Accomplished checklist. | — | changelog_gaps_1201-1500:24 |
| CCCS-02.l | proposed (?) | Existing CCS+ credentials can be imported from the old configuration, stored encrypted, and recorded as imported activity. Is this still needed after the port, given that the migration tool (DEP-05) copies the saved credentials? | — | S16-02, S16-03 |
| CCCS-03 | proposed | CCS+ is downloaded with a browser-like connection when the site's protection requires it. | — | — |
| CCCS-03.a | proposed | CCS+ downloading offers auto, browser, browser-patient and curl modes, initially auto. | — | readme_gaps:32, changelog_gaps_301-600:39 |
| CCCS-03.b | proposed | In auto mode, an unanswered or blocked CCS+ download tries the browser-like connection, retries with twice the wait, then tries curl. | — | readme_gaps:32, changelog_gaps_301-600:39 |
| CCCS-03.c | proposed | Browser-patient mode makes the number of CCS+ download attempts in DEF-01, each with its response allowance. | — | changelog_gaps_301-600:39 |
| CCCS-03.d | proposed | A CCS+ download follows no more redirects than DEF-01 allows; HTTPS and credential forwarding follow CON-06 and CON-06. | — | changelog_gaps_1501-1800:37, changelog_gaps_301-600:40 |
| CCCS-03.e | proposed | The download diagnostic record identifies the connection mode that answered and the modes previously attempted. | — | changelog_gaps_301-600:39 |
| CCCS-03.f | proposed | After the number of rejected CCS+ sign-ins in DEF-01, automatic checks pause until the user corrects the credentials and requests Sync Now. | — | readme_gaps:39, changelog_gaps_2101-2336:37 |
| CCCS-03.g | proposed | CCS+ is downloaded over HTTPS. | — | S23-28, S60-21 |
| CCCS-04 | proposed | A CCS+ import keeps its source identifiers and its full-day times. | — | — |
| CCCS-04.a | proposed | CCS+ import preserves the source event identifiers and details; event times follow TIM-01–TIM-06 and normalization follows RUL-06. | — | readme_gaps:37 |
| CCCS-04.b | proposed | When CCS+ full-day times are normalized, the original times remain available in the event notes. | — | readme_gaps:37 |
| CCCS-05 | proposed | The user can upload a CCS+ schedule instead of downloading it. | — | — |
| CCCS-05.a | proposed | Upload & publish for CCS+ replaces the downloaded schedule with the uploaded schedule. | — | readme_gaps:38, changelog_gaps_601-900:36 |
| CCCS-05.b | proposed | Successful upload ends the source’s setup-needed configuration state. | — | S27-06 |
