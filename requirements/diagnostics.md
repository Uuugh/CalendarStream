# Requirements: diagnostics

Status, Report a problem, health, debug captures, the container log.

Dashboard.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| DIA-01 | proposed | The user can get the information needed to diagnose a problem. | — | — |
| DIA-01.a | proposed | Container log exposes the most recent log lines of the running app (the number in DEF-01), retrievable as plain text and copyable (DIA-01). | — | readme_gaps:72, changelog_gaps_601-900:34 |
| DIA-01.b | proposed | A Copy log button next to Container log copies the container log straight to the clipboard, with no new tab and no manual select-all. | — | F64.1 |
| DIA-01.c | proposed | Per-source Activity provides diagnostic details for the last download and makes the last received calendar file available for diagnosis. | — | changelog_gaps_1501-1800:21, changelog_gaps_2101-2336:26, changelog_gaps_1501-1800:21 |
| DIA-01.d | proposed | The last received calendar file of each downloaded connection is kept for Report a problem with the download record and these reply headers: content-type, content-length, content-disposition, etag, last-modified, server, date, cache-control and www-authenticate. | — | R4 gap |
| DIA-02 | proposed | The user can report a problem or suggest a feature, with a report they control. | — | — |
| DIA-02.a | proposed | The page offers Report a problem and Suggest a feature, allowing the user to describe a problem or idea; the report or suggestion is prefilled with the running CalendarStream version. | — | readme_gaps:78, changelog_gaps_1201-1500:32, changelog_gaps_1801-2100:25, changelog_gaps_1801-2100:25 |
| DIA-02.b | proposed | The user chooses independently whether a report includes History, each source’s last-download details, device and setup details, contact details and reply preference. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-02.c | proposed | Report preparation redacts private identifiers: usernames, links, stream names, email addresses and the public address; secret protection also follows ACC-05. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-02.d | proposed | Before sharing a report, the user can preview exactly the report content to be shared. | — | readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-02.e | proposed | A prepared report can be sent as a prefilled GitHub issue, copied, or downloaded as a file; copying and downloading need no GitHub account. | — | readme_gaps:78, changelog_gaps_1201-1500:32, readme_gaps:78, changelog_gaps_1201-1500:32, readme_gaps:78, changelog_gaps_1201-1500:32 |
| DIA-03 | proposed | Monitoring programs can read the app's status and health. | — | — |
| DIA-03.a | proposed | CalendarStream provides a status monitoring interface (GET /api/status) that identifies every connection and includes its synchronization status; access follows ACC-02. | — | readme_gaps:79, changelog_gaps_1501-1800:26 |
| DIA-03.b | proposed | CalendarStream provides a health monitoring interface (GET /healthz) that does not disclose database details; access follows ACC-01. | — | readme_gaps:79, changelog_gaps_1501-1800:36 |
| DIA-03.c | proposed | The status interface lists for each source its identifier, name, type, status, message, whether it is running, its attempt, success and change times, next check and event count. | — | R4 gap |
| DIA-04 | proposed | The Product Owner's working files and the Dashboard are served by the app, behind its login. | — | — |
| DIA-04.a | backlog | The Developer's private working files and Good \| Bad verdicts are served by the app itself, behind its login, and are never committed to the repository or published on a public page. | — | Developer, Nov 17 |
| DIA-04.b | backlog | The Dashboard is a live web page built from the GitHub issues and `requirements/*.md`; it is made after the port is complete. | — | Developer, Nov 17 |
| DIA-04.c | backlog | The Dashboard shows testing progress: the current and recent test runs, each shard's state, and pass or fail per requirement. | — | Developer, Nov 17 |
| DIA-01.e | proposed | A container log line reads "date time LEVEL source: message"; the app's own lines and the web server's access lines are kept; the level is info, and the per-request lines of the Google web library are left out. | — | R6 gap |
| DIA-01.f | proposed | The container log needs a signed-in user (ACC-02). | — | R6 gap |
| DIA-01.g | proposed | The first start without a login logs msg:firstTimeSetupLog ({code} the setup code of ACC-01), and the one-time unlock link is logged too. | — | R6 gap |
| DIA-01.h | proposed | A connection's download details say the final address, the HTTP status, the elapsed time with the decimals in DEF-01, the byte count, the client used with its version (and, for the browser-like client, the browser it imitates), the reply headers of DIA-01.d and, for CCS+, the list of attempts tried. | — | R6 gap |
| DIA-01.i | proposed | A new download replaces the connection's captured details and file, which are kept in the database across a restart: one pair per connection. | — | R6 gap |
| DIA-01.j | proposed | The debug view of a capture needs a signed-in user and accepts only the details or the file of a connection by its identifier; any other name is not found. | — | R6 gap |
| DIA-01.k | proposed | The file view shows the stored type of the reply; a calendar file is shown as Unicode plain text. | — | R6 gap |
| DIA-02.f | proposed | The report form has a title up to the length in DEF-01 with msg:reportTitlePlaceholder, the main text labelled msg:reportWhatHappened for a problem or msg:reportWhatWouldYouLike for a suggestion (the heading is msg:reportAProblem or msg:reportSuggestFeature), and an Include list. | — | R6 gap |
| DIA-02.g | proposed | The Include list offers msg:reportIncludeHistory ({n} the lines in DEF-01, ticked), one msg:reportIncludeSource ({name}) per connection ticked when its status is not Healthy and not Running, msg:reportIncludeDevice (ticked), msg:reportIncludeContact with a box msg:reportContactPlaceholder (not ticked) and msg:reportNotifyReplies (ticked). | — | R6 gap |
| DIA-02.h | proposed | The form says msg:reportPrivacyNote, has a fold msg:reportPreview with the exact report, says msg:reportNoGithub, and has the buttons msg:reportCopy (then msg:reportCopied), msg:reportDownload (a plain text file), msg:cancel and msg:reportOpenGithub. | — | R6 gap |
| DIA-02.i | proposed | The report text is "# " and the title (or the form's heading), a blank line, the description (or msg:reportNoDescription), then the sections Setup, Device, Contact and Logs, in that order, each when it has content. | — | R6 gap |
| DIA-02.j | proposed | Setup reads: the version, the image tag and channel (beta or stable), the server and the time zone; then each connection's type with its status word; then the destination types; then ", Google connected" when it is and ", updater on" when it is. | — | R6 gap |
| DIA-02.k | proposed | Device reads the browser's user agent, the screen and window sizes, and the browser language and the theme; Contact is the typed contact joined with " · " to the reply wish when ticked. | — | R6 gap |
| DIA-02.l | proposed | Logs is the History lines when ticked, then for each ticked connection its name, type and status followed by its download details or msg:reportNoDownloadDetails. | — | R6 gap |
| DIA-02.m | proposed | Opening the prefilled GitHub issue uses the problem or feature template with the title and fields; when the whole link would exceed the length in DEF-01, the log field is cut to the length in DEF-01, msg:reportTooLong is added and the whole report is copied to the clipboard. | — | R6 gap |
| DIA-02.n | proposed | The report data is fetched once per page load, when the form is first opened, and needs a signed-in user; the app sends nothing anywhere by itself. | — | R6 gap |
| DIA-02.o | proposed | The report data holds the newest History lines (the number in DEF-01) written as "date time level message" in English, and each connection's download details with private values redacted, cut to the length in DEF-01. | — | R6 gap |
| DIA-02.p | proposed | Redaction replaces any text that looks like an e-mail address with msg:redactedEmail, the value after password, secret, token, authorization or cookie (after a colon or an equals sign) with msg:redactedPrivate, and any unbroken run of letters, digits, underscores and hyphens of the length in DEF-01 with msg:redactedPrivate. | — | R6 gap |
| DIA-02.q | proposed | The listed private values of DIA-02.c (including the Google client ID) are replaced when they have the length in DEF-01 or more, the longest first. | — | R6 gap |
| DIA-02.r | proposed | Redaction is not applied to the Device section, the typed text or the contact. | — | R6 gap |
| DIA-03.d | proposed | The health interface checks only that the database answers; it answers success with ok true, or failure with msg:databaseUnavailable and a warning in the log, and it ignores sources, Google and the updater. | — | R6 gap |
| DIA-03.e | proposed | A call to the health interface is not a failed sign-in and is never locked out. | — | R6 gap |
| DIA-03.f | proposed | The status interface answers: version, updating, status, message, running, last attempt, last success, last change, last sign-in, last sign-in accepted, next run, events, sources, destinations and google (connected, running, pending, error). | — | R6 gap |
| DIA-03.g | proposed | Times in the status interface are ISO 8601 with their zone offset, and null when there is none. | — | R6 gap |
| DIA-03.h | proposed | The status words are starting, ok, auth_failed, blocked, error, paused, running, setup and internal. | — | R6 gap |
| DIA-03.i | proposed | A restart of a running connection resets its status to starting; a connection's status is saved after each run and restored at start. | — | R6 gap |
| DIA-03.j | proposed | The pages that need no sign-in are the health interface, the calendar feeds and the subscribe pages. | — | R6 gap |
