# Slice 6 comparison (B = reverse/slice6.md vs A = history, diagnostics, deployment, documentation, common TIM+DEF)
B rows with the same behavior are grouped on one line. "A file" names are the likely home; some belong to files outside my slice (settings, accounts, connections, events, rules, google).

## GAP
### Topic 1 History
R6-01.a | line level is info, warn or error | history.md
R6-01.b | lines stored in English, translated only when shown; untranslated shown in English | history.md
R6-01.c | line for a non-CCS+ source is prefixed "<source name>: " | history.md
R6-01.d | every line also goes to the container log at the matching level | history.md
R6-01.e | if a line cannot be saved, log "Couldn't write activity log to the database: <reason>" and carry on | history.md
R6-01.f | a line's time is the moment recorded (database clock, with zone) | history.md
R6-02.a, .k | explicit Type kept; which actions carry which Type (calendar add/remove/empty/import/save/On-Off/default = Calendar; destination = Feed; rule ops = Rule; event ops = Event; Google deletions/account = Google; Settings lines = Settings) | history.md
R6-02.b-.j | untyped line gets Type from its leading words (Rule/Calendar/Feed/Event/Google/Settings/Update, else Sync); legacy inference, unneeded if every line carries a Type | history.md
R6-03.a | no-change download line "Schedule downloaded from CCS+|<host>: no changes"; status "Up to date: <n> events in feed (no changes)" | history.md
R6-03.c | republished identical schedule records "no changes" with the same status | history.md
R6-03.d | failure lines: 401 "Sign-in rejected: <reason>" (error), 403 "Blocked: <reason>", other "Download failed: <reason>", unexpected "Unexpected error: <Name>: <message>" | history.md
R6-03.e | refused hand upload records error "Upload rejected: <reason>" | history.md
R6-03.f | source status values auth_failed/blocked/error/internal; a feed only ever gets "error" | diagnostics.md / connections
R6-03.g | rejected sign-in count rises by 1, a success resets to 0 | connections
R6-03.i | with no CCS+ login saved a check only sets status "setup" ("Enter your CCS+ Username and Calendar Sync password..."), no History line | connections
R6-04, .a-.f | "Record changes" rule: History line "<calendar> changed <title>: time a->b; title; location" (only differing parts); removal line; moved occurrence of a repeating event counts as change; event note "Changed <date>: ..." (last 20 kept, appended to description); English notes for unsupported languages; time format "Oct 23 7:15am-9:30am" / "(all day)" | history.md / rules.md
R6-05, .a-.c | events a source stops sending are kept struck through and recorded ("United removed n event(s): ..." / "<cal>: gone from the feed: ..."); only non-hidden, ending today or later; max 200 kept per download; line names first 5 then " ..."; Type Event, restorable per event, no Undo button | history.md / events.md
R6-06.b | open History order: per-source status line, Google line, filter, table ("Nothing yet." if empty), footer, debug links | history.md
R6-06.c | source status line: Sign-in not yet/accepted/rejected + time, Last check, Schedule changed, Next check, n events, red "n rejected sign-ins in a row"; time today = clock only, else "short date, clock", none = "never" | history.md
R6-06.d | Google line (only when connected): error, "syncing...", last sync time or "not yet" | history.md
R6-07 | table lists the newest 300 lines, newest first (no DEF row) | history.md + DEF
R6-07.c | saved column order valid only if all four columns once, else default; bad save refused 400 "Unknown column order." | history.md
R6-07.d | Undo column header is screen-reader-only text | history.md
R6-07.e | line level colors the Event cell (info, warn, error each own color) | history.md
R6-08 | filter choices: Type menu "Every type" + the eight types; Words box; Time menu Any time / Last hour / Last 24 hours / Last 7 days / Last 30 days | history.md
R6-08.a | filtering acts on the loaded rows without reloading | history.md
R6-08.c | server-side filter (type, words, since, limit): words case-insensitive, % _ and backslash literal | history.md
R6-10.a | Unhealthy when a source status is auth_failed, blocked, error, internal or paused, or Google connected and last call failed; ok, running, starting, setup do not count | history.md
R6-20.a | each line has undo state "", "done" or "undone" | history.md
R6-20.c | undo/redo of a non-eligible line refused 400 "Newer changes come first: undo (or redo) the one with the arrow." | history.md
R6-20.d | line with no undo data refused 404 "That change can't be undone any more." | history.md
R6-20.f | undo/redo writes "Undone: <msg>" / "Redone: <msg>" to the container log only, no History line | history.md
R6-20.g | recording a new undoable change discards every "undone" line's data (redo chain cleared) | history.md
R6-21.b | per-source snapshot fields: name, color, tags, rule list, defaults, note, interval, download cache, status, counters, On/Off, plus CCS+ login and Calendar Sync link | history.md
R6-21.d | a change may name single events whose edit and added-event data are held | history.md
R6-21.e | restore is all-or-nothing in one transaction; settings absent from the snapshot are deleted | history.md
R6-21.f | after restore: checks start/stop per source, data of gone sources forgotten, statuses reread, calendars rebuilt | history.md
R6-22.a | a deleted event stays visible, struck through and greyed, labelled with where deleted (calendarstream, google, united, feed) | history.md / events.md
R6-22.d | undoing deletion of a source event removes its hidden mark (and edit record made only for the deletion) and re-writes it to Google | history.md
R6-23.c | saving the History count records "History remembers the last <n> changes for Undo" (Type Settings) and trims at once | history.md
R6-23.d | trimming keeps undo data of newest n lines that have any; older lose data and state; also runs after every recorded change; finishes deletions whose undo is gone | history.md
R6-24, .a, .b | at most 1000 History lines kept (counted by number gap, B "unsure"); page shows 300, problem report takes 60 | history.md + DEF
R6-25 | links/keys written safely: feed link host only; Calendar Sync link host+path; Google client first 12 chars + "..."; CCS+ line never has values; passwords/secrets/tokens never in History | history.md
R6-25.a | login lines name the user: Status-page login created for "<user>" / changed (user "<user>") | history.md
R6-26, .a-.i | exact wording of recorded lines: calendars, destinations, rules, events (incl. linked events), updates (Update available / Updating / Auto-update, warn when not started), sign-in protection (locked after 5 failed, 50-from-many warning, unlock link used), start-up old-secret-files import, public address moved from .env | history.md
### Topic 2 Diagnostics
R6-30.a | log line format "<date time> <LEVEL> <logger>: <message>"; app and web-server access lines kept | diagnostics.md
R6-30.b | log level info; per-request Google HTTP-library lines suppressed | diagnostics.md
R6-30.d | Container log needs the status-page sign-in | diagnostics.md
R6-30.e | first start without a login logs "First-time setup: open the status page and enter the setup code <CODE>"; one-time unlock link also logged | diagnostics.md
R6-31.a | response details JSON: effective URL, HTTP status, elapsed (2 decimals), bytes, client used ("curl <v>" / "curl_cffi <v>, as chrome"), kept headers (content-type, content-length, content-disposition, etag, last-modified, server, date, cache-control, www-authenticate), CCS+ "tried" list | diagnostics.md
R6-31.c | captures replaced by each new download, kept in database across restart, one pair per source | diagnostics.md
R6-31.d | /debug/<name> accepts only source, response, source:f<6 hex>, response:f<6 hex>; else 404; needs sign-in | diagnostics.md
R6-31.e | response doc shown with stored type, calendar file as text/plain UTF-8 | diagnostics.md
R6-32.a | report form: Title up to 120 chars; Include ticks and defaults (History last 60 lines ticked; a source's details ticked when its status is not ok/running; Device ticked; Contact unticked; Notify me of replies ticked) | diagnostics.md
R6-32.d | report layout: "# <title>", description or "(no description)", then ## Setup, ## Device, ## Contact, ## Logs in that order | diagnostics.md
R6-32.e | Setup line "CalendarStream <version> (<image tag>, <channel>), <server>, TZ <zone>"; Sources/Destinations lines; ", Google connected"; ", updater on" | diagnostics.md
R6-32.f | Device: Browser user agent, Screen and window size, Language and theme | diagnostics.md
R6-32.g | Contact joined " · " with "would like to be notified of replies" | diagnostics.md
R6-32.h | Logs: History lines then per ticked source "--- <name> (<type>): <status>" with download details or "(no download details)" | diagnostics.md
R6-32.j | GitHub link over 7000 chars: log field cut to first 1500 chars plus notice; whole report copied to clipboard | diagnostics.md
R6-32.k | report data fetched once per page load on first open; app itself sends nothing | diagnostics.md
R6-33, .a, .b | report data fields; activity = newest 60 lines "YYYY-MM-DD HH:MM:SS <level padded to 5> <message>" in English; source debug text redacted, cut to 6000 chars | diagnostics.md
R6-34, .b | any e-mail-looking text becomes "[e-mail]" | diagnostics.md
R6-34.c | value after password/secret/token/authorization/cookie (key: or =) replaced by "[private]" | diagnostics.md
R6-34.d | any run of 32+ letters/digits/_/- replaced by "[private]" | diagnostics.md
R6-34.a (part) | listed values replaced only when 3+ chars, longest first; list includes Google client ID (A's DIA-02.c list lacks it) | diagnostics.md
R6-34.e | redaction not applied to Device section, typed text or contact | diagnostics.md
R6-35 | report data needs sign-in | diagnostics.md
R6-36 | report form texts translated in the six languages | diagnostics.md
### Topic 3 Monitoring
R6-40.a | /healthz checks only that the database answers; ignores sources, Google, updater; 200 {"ok": true} else 503 "database unavailable" (warning logged) | diagnostics.md
R6-40.b | /healthz never counts as a failed sign-in and is never locked out | diagnostics.md
R6-40.c | container HEALTHCHECK calls /healthz on 8080 every 60 s, 5 s limit | deployment.md
R6-41.a | /api/status fields: version, updating, status, message, running, last_attempt, last_success, last_change, last_auth, last_auth_ok, next_run, events, sources, destinations, google | diagnostics.md
R6-41.c | times ISO 8601 with offset in server zone, null if never | diagnostics.md
R6-41.e | status words: starting, ok, auth_failed, blocked, error, paused, running, setup, internal | diagnostics.md
R6-41.g | google object: connected, running, pending, error | diagnostics.md
R6-41.h | restart while running resets that source's status to "starting" | diagnostics.md
R6-41.i | source status saved after each run and restored at start | diagnostics.md
R6-42 | no-sign-in pages: /healthz, calendar feeds, subscribe pages | diagnostics.md
R6-43 | updater /livez polled every 5 min with 3 s limit; Update now shown only while it answers 200 | deployment.md + DEF
### Topic 4 Deployment
R6-50.a | every installer question shows default in [ ], Enter accepts, later runs default to current settings, input read from terminal even when piped | deployment.md
R6-50.b | installer stops at first failure | deployment.md
R6-51 | previous install found in current folder (compose file naming calendar_stream) else ~/stacks/calendarstream; its .env gives defaults | deployment.md
R6-52 | subdomain slug: lower-case, runs of other chars -> "-", trim "-" and "."; empty -> "calendarstream" | deployment.md
R6-54.a, .b | folder path accepts "~" and relative, made absolute, trailing "/" dropped; created if missing | deployment.md
R6-58.a | default PORT 8080, or 8078 + stack number; STACK_NO is 2 or lowest free number | deployment.md
R6-58.b | container names <prefix><no>, <prefix>_db<no>, <prefix>_updater<no> (STACK_PREFIX default calendar_stream) | deployment.md
R6-59.a | answers written to .env (IMAGE_TAG, STACK_PREFIX, MNT_DOCKER, STACK_NO, PORT, COMPOSE_PROFILES), existing/commented line replaced, other lines kept | deployment.md
R6-59.c | UPDATER_TOKEN.txt: 40 random letters/digits, owner-readable, created even when updater declined (DB password file is 32) | deployment.md
R6-61 | stack = app + Postgres 18 alpine + optional updater (profile "updater", Watchtower fork) | deployment.md
R6-61.c | db health check pg_isready every 10 s, 5 s timeout, 6 retries, 30 s start | deployment.md
R6-61.e | DB_NAME (calendar_stream) / DB_USER (ccs) take effect only when the DB is first created | deployment.md
R6-62.a, .b | entrypoint starts as root, reads secret files (strips CR/LF), runs as PUID/PGID (defaults 1000/100) without extra groups; warns if a *_FILE is missing | deployment.md
R6-63.a | app listens on all addresses, port 8080 inside container | deployment.md
R6-63.b | public address is set on the page, not .env; old PUBLIC_URL/PUBLIC_BASE_URL read once and moved; http://<IPv4|localhost>:8080 counts as unset | deployment.md / settings
R6-63.c | public address normalisation (add https://, lower-case, drop default port and "/", refuse non-http(s), no host, params/query/fragment/userinfo/space, >300 chars) | settings
R6-64.b | app asks updater POST <UPDATER_URL>/v1/update (image=ghcr.io/uuugh/calendarstream, async=true, Bearer token, 15 s); 200/202/429 count as started | deployment.md
R6-64.c | updater error texts (not set up; couldn't reach; refused the token; answered HTTP n) | deployment.md
R6-64.d | install pinned to an exact version cannot be updated by the updater, only by the installer | deployment.md
R6-64.f | update check reads VERSION (beta) or STABLE file on main, 15 s, UA "CalendarStream/<v>"; stable never offers beta; failure text kept | settings (SET-05)
R6-64.g | channel is beta for tag "beta" or containing "-beta."; only strictly newer offered; a beta is older than its release | settings (SET-05)
R6-65, .a | .env defaults: TZ America/Chicago, IMAGE_TAG latest, COMPOSE_PROFILES empty, STACK_PREFIX calendar_stream, PORT 8080, PUID 1000, GUID 100, RESTART unless-stopped, MNT_DOCKER compose folder, FORWARDED_ALLOW_IPS 127.0.0.1, DB_NAME calendar_stream, DB_USER ccs | deployment.md
R6-65.c | CCS_CALENDAR_URL default https://ccsplus.ual.com/calendarsyncapi/api/Calendar/GetCalendar; a saved link overrides | deployment.md
R6-65.g | FEED_TOKEN legacy (pre-0.2.1 feeds): 24-byte URL-safe random made once; a typed stream name wins | deployment.md / DEP-05.c
R6-65.h | old login files (CCS_/GUI_ USERNAME/PASSWORD, *_FILE, /run/secrets) imported once; user name whitespace-trimmed; GUI name defaults "admin" | deployment.md / DEP-05.c
R6-65.i | DB_HOST (calendar_stream_db), DB_PORT 5432, DB_PASSWORD from secret file; warning when none; user/password percent-encoded | deployment.md
R6-67.a, .b | DB pool 1-4 connections; shutdown cancels loops and closes DB | deployment.md
R6-68 | release pipeline: beta built when VERSION changes after suites pass and image scan has no fixable High/Critical; tags v<VERSION>, <VERSION>, beta; latest moves when STABLE changes | deployment.md
### Topic 5 Shared blocks
R6-70.a | unknown TZ stops the app at start (B "unsure") | deployment.md
R6-71.b | choosing nothing/server zone clears display zone; invalid zone refused 400 "Unknown time zone." | common.md TIM
R6-71.c | invalid saved zone ignored, server zone used | common.md TIM
R6-71.d | zone list order: America/New_York, Chicago, Denver, Phoenix, Los_Angeles, Anchorage, Pacific/Honolulu, Pacific/Guam, UTC, Europe/London, Frankfurt, Asia/Tokyo, Hong_Kong, Australia/Sydney, then alphabetical | common.md TIM
R6-71.e | "Today" (calendar, event pages, print) is the day in the display zone | common.md TIM
R6-72.a | event form shows start/end in own zones with clock label | events.md
R6-72.b | typed times accepted: 9:30, 9.30, 9h30, 930, 21:30, 2130, 9 pm, 9:30pm, 9:30 p.m.; bare hour = :00; am/pm hour 1-12; empty = 00:00; else refused | events.md
R6-72.c | validation: end not after start 400 "The end has to be after the start."; "Check the dates and times."; "The event needs a title." | events.md
R6-72.g | Google sync starts at first day of current month (older not synced) | google.md
R6-73.a | source event with date-only start is all-day; no end = one day | calendars.md
R6-73.b | form shows all-day last day inclusive; last day before first refused 400 "The last day is before the first day." | events.md
R6-73.d | timed source event at exactly 00:00 with no end/duration (CCS+ RDO, HDO, VRDO) becomes one all-day | calendars.md
R6-73.e | no-end timed event not at midnight read with end = start, flagged "no end", rules decide length | calendars.md
R6-73.f | rule making timed event all-day: start date, max(1, round(days)) days, description gets "Start: HH:MM" or "Original time: ..." then old description, cut 2000 chars | rules.md
R6-73.g | description cut to 2000 chars, meeting link to 500 | DEF-01
R6-74.a | DEFAULT_EVENT_HOURS accepts decimals, "h" suffix, all-day words; invalid logs warning, uses 1 | deployment.md
R6-74.b | ALLDAY_24H false for 0/false/no/off | deployment.md
R6-74.d | no-end event that no rule changes still gets DEFAULT_EVENT_HOURS (or all-day) | rules.md
R6-74.e | CCS+ added via "+" can come with starter rules "Items without an end time" (60 min) and "24-hour events", per calendar, optional | rules.md
R6-75 | parser's legacy defaults (probably not applicable to the port) | n/a
R6-76.c | time with date: today = clock only; other day "Oct 19, 15:42" | common.md
R6-77, .a-.c | dates per language (day/short/month title patterns for en, es, fr, de, pt, nl); two-digit short day; month-grid weekday letters start Sunday; six languages (English, Espanol, Francais, Deutsch, Portugues pt-BR, Vlaams nl-BE); choice = saved else browser accept-language else English | settings (language)
R6-78 | untranslated text shown in English; catalog matching with {placeholders}, most specific wins, nested up to 4 levels | settings (language)
R6-80.a | calendar/destination name whitespace collapsed max 100; note max 300 | DEF-01
R6-80.b | tags max 30 per calendar, each max 40 | DEF-01
R6-80.c | event templates max 30; template/event title max 200, location max 200 | DEF-01
R6-80.d | hand event: title 200, location 200, notes 4000, meeting link 500 (http(s):// else 400 "Online Meeting is a link starting with https://") | DEF-01
R6-80.e | rules max 60; 3 bracket levels; condition text 200; pattern 100; title 80; emoji text 16; Notes text 1000; time offset and Move at most 10080 min either way; length at most 524160 min (12 conditions, 6 actions, 0.05 s already in A) | DEF-01
R6-80.f | rule test samples max 30 lines of 300 chars | DEF-01
R6-80.g | calendar search text cut to 100 chars; key hidden-kind list max 60 | DEF-01
R6-81.b | download waits 20 s to connect, 60 s total, with error texts | DEF-01
R6-81.c | calendar check: "BEGIN:VCALENDAR" in first 2000 bytes; web page quoted from first 4000 bytes; snippet 160 chars | DEF-01
R6-81.e | import/upload window 3650 days before and after today | DEF-01
R6-81.f | print: range at most 731 days; at most 24 monthly, 60 weekly, 62 daily pages | DEF-01
R6-82 (part) | after a failed scheduled run the next try is in 5 minutes | DEF-01
R6-82.a | checks start at app start and when a source is added; local calendars have none | connections
R6-82.c | browser-like client imitates newest known Chrome; feeds always downloaded with curl | connections
R6-83.a (part) | status-page user name 1-64 no whitespace/colon; CCS+ user name 2-64 [A-Za-z0-9._@-]; CCS+ password max 200; up to 50 remembered accepted logins | DEF-01 / accounts
R6-83 (part) | "known" cookie valid 400 days; own-address lookup at most every 10 minutes; trim rule for failed table (5000 unlocked dropped above 10000) | DEF-01
R6-83.b | Administrator e-mail max 254 (local part 64); public address max 300 | DEF-01
R6-84.b | alarm choices 0,5,10,15,30,60,120,1440,2880,10080 minutes; last 20 change notes kept per event | DEF-01 / events.md
R6-85 | retention: History 1000 lines; Beta Google traffic list 200 entries in memory | DEF-01
R6-86 | Google: at most 1500 writes per sync; full check and repair every 24 h; retry after failed sync 15 min; access token fresh 60 s; invite sign-ins 50 | DEF-01
R6-87 | update check connection limit 15 s; updater probe limit 3 s every 300 s | DEF-01
R6-89 | status-page password hashed with scrypt N=16384, r=8, p=1, 32-byte result, fresh 16-byte salt | accounts (ACC-05)
R6-90.a-.g | secret box: PBKDF2-SHA256 390000 rounds from DB password + random 16-byte salt, Fernet; record v1; sealing with no DB password fails; undecryptable = "can't be decrypted" (CCS+ password counts as unset, Google client secret empty, Google token error text); 8 cached keys; CCS+ login user clear + sealed password, blank keeps saved, max 200; secrets never shown again | accounts (ACC-05) / deployment.md
R6-98 | new source color default #1d4ed8 | DEF-01
R6-99 | identifiers: ccs; f+6 hex feed; l+6 hex local; a+6 hex extra Google account; added event "cs-"+16 hex+"@calendar_stream"; feed event "<source id>/<UID>[/<start>]" | connections / events.md

## DIFFERENT
R6-02 | HIS-02.a | Types: Calendar, Rule, Event, Sync, Feed, Google, Settings, Update | order Calendar, Feed, Rule, Event, Google, Settings, Update, Sync
R6-03.b | HIS-01.b | sync records how many events added and how many updated | "(3 new, 1 removed)" detail (new/removed, not added/updated)
R6-07.a | TIM-03 | times shown in the Local zone (device or Settings > Time Zones) | History time with seconds in server zone, not display zone
R6-21.a | HIS-03.b | undo covers rules, feeds, templates, import, merge, CCS+ removal, Hide | every snapshot always holds sources, default calendar, destinations, rules, templates, reminders, links, ignored conflicts
R6-23.a | HIS-04.a, UIC-19 | number outside 1-200 is not valid (field note) | a saved bad value silently falls back to 100; refused save is 400 "Between 1 and 200 changes."
R6-41.b | DIA-03.a | every connection identified with its own sync status | top-level legacy status fields come from CCS+ (else first source, else "starting")
R6-66 | DEP-01.g | backup and restore done from Settings > Site Admin | no backup/restore in the app; documented backup is a database dump
R6-70 | TIM-01, TIM-06, DEP-05.b | each event stored in UTC with its own zone; TZ only a default | one server zone (TZ, default America/Chicago) for all times read, kept, published, sent to Google
R6-70.b | TIM-01 | stored UTC + zone | ISO text with offset converted to server zone
R6-70.c | TIM-02, TIM-08 | zoned event keeps its zone; zone-less gets installation default | zoned converted to server zone; zone-less taken as server zone
R6-70.d | TIM-01 | status times not specified | stored ISO with offset, read back in server zone
R6-71.a | TIM-09 | only real zones offered; nonexistent zone -> default | valid = "UTC" or IANA name containing "/" not starting Etc/, SystemV/, posix/, right/
R6-72.d | TIM-06 | Google gets each event's recorded zone | Google gets text with server zone name
R6-72.e | TIM-07 | feeds carry each event's times with its zone | feed states server zone (X-WR-TIMEZONE), timed events in UTC, refresh and TTL 1 hour
R6-73 | TIM-04 | all-day = 24 h event local midnight to midnight in its zone, stored UTC | date-only start/end, exclusive end, no time, no zone
R6-76 | TIM-10 | until chosen: 12-hour if device in a US time zone, else 24-hour | "auto" = 12-hour for English, 24-hour for other five languages
R6-80 | DEF-01 Connections | at most 50 connections | at most 10 calendar sources; at most 20 destinations
R6-83 | DEF-01 Login failures in total; Unlock link valid | 25 failures within 15 min; unlock link 24 hours | 50 failures from all addresses in 15 min; unlock link 1 hour
R6-83.a | DEF-01 Password minimum rows | min length 11 (8 or more), min 1 capital, 1 lowercase, 1 number, 1 special | page password min 12, capital, number, symbol, no char 3+ times in a row

Limits table (B 5.4) against DEF-01:
- A states the same: 5 MB download; 5 redirects (CCS+); 5000 events per feed; sync 15-1440, default 60; History 1-200 default 100; container log 3000; 12 conditions; 6 actions; 0.05 s pattern; 5 min whole-day tolerance; 5 failures per address (15-min lock); 7-day trusted address; 30-day session; 10,000 failed addresses; 1,000 good addresses; Google consent 15 min, 20 pending, retry 5 attempts from 5 s doubling to 15 min, invite 7 days, instant-update 7 days, renewal 1 day, retry 6 h; 24 h fold; animation 0-200 % and 25-300 %; update schedule hourly/weekly/monthly (30 d)/never; running-update 15 min; DB retry 3 s up to 60 s; recurrence 1 year back, 2 years ahead; 2 rejected CCS+ sign-ins; logo/favicon 256 KB; longest reminder lead 1 week.
- A states differently: see DIFFERENT (R6-80 counts, R6-83 failures/unlock/passwords).
- A lacks: listed in GAP lines R6-80.a-.g, R6-81.b/.c/.e/.f, R6-82, R6-83 parts, R6-83.b, R6-84.b, R6-85, R6-86, R6-87, R6-88 (pool 1-4), R6-89, R6-90, R6-98, R6-61.c, R6-40.c.

## A-ONLY
HIS-01.c, .d | Google-change saved/kept and Google-origin deletion recorded (B defers to Google slice)
HIS-01.e | warning when a former Google client's calendar cannot be cleaned up
HIS-01.f | Google color-update failure recorded with operation, status, reasons
HIS-01.g | one unsigned-Google warning, resettable
HIS-01.h | unchanged repeating failure recorded once until it changes or clears
HIS-01.i | external removal/Google notification never becomes the current Undo entry
HIS-01.k | deferred remote cleanup (write budget) reported
HIS-01.l | completing Google API setup records which connections need sign-in/error/first sync
HIS-02.f | accepted sign-in shown as a check only
HIS-03.e | CCS+ removal forgets retained credentials once out of Undo history
HIS-04.b | Show secrets switch on every log view, masked by default, resets on page open
DIA-04, .a-.c | Developer working files and Dashboard served behind login; test-progress view
DEP-02.e | host-address lookup failures reported
DEP-02.g | pipe and ampersand answers kept literally
DEP-05.a | env values only starting values, database overrides (B only implicit)
DEP-05.b | installer sets installation time zone as default zone for zone-less imports
DEP-05.c | one-time Python-to-Dart migration tool
DOC-01, .a-.d, DOC-02, .a-.b, DOC-03, .a-.c | all documentation rows (B has none)
TIM-05, TIM-07 | rules independent of time zone; feeds carry zone (B contradicts 07, silent on 05)
TIM-10 (notation clause) | notation inside each format is a Theme setting
DEF-02, DEF-03 | list-limit rule; limits counted in grapheme clusters
DEF rows with no B counterpart | page refresh after update 15 s; Copied 1.8 s; Saved/Cancelled 3 s; Save pulse ~5 s; result held 2.4 s; good status word 2.4 s; working status 0.7/0.5 s; typing delay 300 ms; stream token 22 chars/128 bits/1-128; drag step 15 min; long-press 0.5 s; hour height; calendar key name 25; grid scroll start 7 am; search results 6; shortest template 5 min; reminders per event 5; networks trusted during global block; logo ratio; favicon ratio; image editor 512 px/10 MB; phone-width 700 px; password minimum rows (differ)

## Counts
B rows covered 88, different 19, gap 196 (total 303). By topic covered/different/gap: History 26/5/74, diagnostics 10/0/25, monitoring 4/1/11, deployment 28/1/32, shared blocks 20/12/54. A rows only-in-A: about 60 (history 11, diagnostics 4, deployment 5, documentation 12, common TIM/DEF about 28).
