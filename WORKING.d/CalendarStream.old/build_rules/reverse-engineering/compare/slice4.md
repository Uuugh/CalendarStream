# Slice 4 comparison (B = reverse/slice4.md, A = requirements)

## GAP (B ID | behavior and values | A file)
R4-01.b | CCS+ source has fixed identifier "ccs" | ccs.md
R4-01.c | adding CCS+ lets the person choose which starter rules come with it, applied to CCS+ | ccs.md (+rules.md)
R4-02.a | Username trimmed, 2-64 chars of letter/digit/dot/underscore/@/hyphen; error "Enter your Username (letters and digits, e.g. U123456)." | ccs.md (CCCS-02.f gives no limits)
R4-02.c | one trailing CR/LF stripped from password, other whitespace kept | ccs.md
R4-02.e | blank password with none saved refused "Enter the Calendar Sync password too." | ccs.md
R4-02.f | password over 200 chars refused "That password is too long."; undecryptable stored password counts as not entered (R4-02.g) | ccs.md / common.md DEF-01
R4-02.i | saving credentials resets rejected-sign-in count to 0, forgets download validators, History "CCS+ Username and Calendar Sync password saved" | ccs.md
R4-02.j | after saving, Sync Now starts at once (page returns to CCS+ module ~1.5 s later when page reloads) | ccs.md
R4-03, R4-03.a, R4-03.b, R4-03.c | verify waits for a running download (up to 120 s), runs manual download, answers Validated/Failed; CCS+ ok only if last sign-in succeeded and status ok; link ok only if status ok; unknown kind "Unknown kind of login." | ccs.md / calendar_link.md
R4-04, R4-04.a, R4-04.b, R4-04.c, R4-04.d, R4-04.e | editable Calendar Sync link, default https://ccsplus.ual.com/calendarsyncapi/api/Calendar/GetCalendar; empty/default deletes saved; page wins over CCS_CALENDAR_URL; must be https with host ("The Calendar Sync link must start with https://"); change resets validators and count and downloads; reset action; History lines | ccs.md
R4-05 | CCS+ download sends HTTP Basic sign-in and Accept "text/calendar, */*;q=0.5" | ccs.md
R4-06.a, R4-06.b | validators stored only on accepted publish; 304 gives status ok, History info "Schedule downloaded from CCS+: no changes", message "Up to date: <n> events in feed (no changes)"; If-None-Match/If-Modified-Since sent only when not empty (R4-06) | connections.md (CON-06.g)
R4-07 | CCS_CLIENT setting case-insensitive, trimmed, unknown means auto | ccs.md
R4-07.a, R4-07.b | curl: one attempt with curl; browser: one attempt browser-like, normal timeout, no pause | ccs.md
R4-07.c, R4-07.d | browser-patient pauses 0/5/15 s before attempts; auto: browser (normal), browser (2x timeout) after 3 s pause, then curl | ccs.md (CCCS-03.b/.c lack pauses)
R4-07.e | normal CCS+ attempt timeout 60 s overall, 20 s connect | common.md DEF-01
R4-07.g, R4-07.h | last attempt's error reported when all fail; failed attempts logged as warnings ("no reply in <n> s"/"refused (HTTP 403)"); info "CCS+ download answered after <attempts>" | ccs.md
R4-08, R4-08.a, R4-08.b | browser-like client uses newest Chrome profile fingerprint; messages when curl_cffi or curl not installed | ccs.md
R4-09.a, R4-09.b, R4-09.c, R4-09.g, R4-09.e, R4-09.f, R4-09.d | exact error texts: 401 "CCS+ rejected the UID or Calendar Sync password (HTTP 401)..."; 403 "Access denied by <Akamai (United's bot protection)|Server|the server>, HTTP 403[, reference <id>]."; other >=400 "<who> answered HTTP <status>: <160 chars>"; non-calendar reply; silent hold text with <n> s; "Couldn't connect to <host> within 20 seconds..."; "Couldn't reach <host>: <reason>"; first 2,000 bytes must contain BEGIN:VCALENDAR | connections.md (CON-06 only states categories)
R4-09.h, R4-09.i, R4-09.j | exact texts for non-https, "redirected too many times", "sent more than 5 MB" | connections.md
R4-10, R4-10.a, R4-10.b | outcome statuses auth_failed/blocked/error/internal and History prefixes "Sign-in rejected:", "Blocked:", "Download failed:", "Unexpected error:"; count +1 per rejection, reset on success (304 counts as success), block/hold/other errors leave count | ccs.md / connections.md
R4-11 | pause message "Automatic downloads paused after <n> rejected sign-ins, to avoid locking your account..." status "paused" | ccs.md
R4-11.b, R4-11.c | successful sign-in or new credentials/link ends pause; header shows "Automatic checks paused" in place of next-check time | ccs.md
R4-12 | setup message "Enter your CCS+ Username and Calendar Sync password to start downloading the schedule."; status "setup" | ccs.md (CCCS-02.c lacks text)
R4-13 | interval default from SYNC_INTERVAL_MINUTES (old SCRAPE_INTERVAL_MINUTES), 60, min 15 | connections.md CON-05.a (installation starting value)
R4-14.a, R4-14.b, R4-14.c, R4-14.d | upload max 5 MB ("That file is too large for a schedule (over 5 MB)." 413); first 2,000 bytes need BEGIN:VCALENDAR ("That file isn't a calendar (.ics) file: ..."); accepted upload published as "uploaded by hand", forgets validators, records attempt time; rejected upload History "Upload rejected: <message>" | ccs.md
R4-15.a | event without a start is skipped | connections.md (CON-07)
R4-15.b | end is DTEND, else start + DURATION | connections.md / TIM
R4-15.e | all-day event with no end lasts one day | connections.md
R4-15.f | no title becomes "(no title)" | connections.md
R4-15.g | notes cut to 2,000 characters | connections.md / common.md DEF-01
R4-15.h | no UID: identifier from start and title | connections.md
R4-15.j | unzoned times taken in the display time zone | connections.md / TIM
R4-17, R4-17.a, R4-17.b | first download detail "first copy", later "<a> new, <r> removed", unchanged "no changes"; accepted download sets ok, last-success, last-change; message "<How>: <n> events in feed (<detail>)"; History "Schedule <how>: ..." with how = "downloaded from CCS+"/"uploaded by hand"/"downloaded from <host>" | connections.md CON-03
R4-18 | last raw download and download record kept for Report a problem, with listed headers (content-type, content-length, content-disposition, etag, last-modified, server, date, cache-control, www-authenticate) | ccs.md / diagnostics.md
R4-19.a | only kinds addable: local, CCS+, calendar link; other "Unknown kind of calendar source." | connections.md
R4-19.b | unknown preset stored as "other"; preset only changes help and description | calendar_link.md
R4-19.c | generated ids: "f"+6 hex (link), "l"+6 hex (local), never colliding | connections.md
R4-19.d | name cut to 100 chars after collapsing whitespace, note to 120 | common.md DEF-01 / connections.md
R4-19.e | adding writes History "Calendar source added: <name>" (undoable), builds feed and starts checks at once | connections.md
R4-20.a | address trimmed, https and host required; text "The feed link must start with https:// (or webcal://)." | calendar_link.md
R4-20.c, R4-20.d | link of existing link source editable (CCS+ refused "Use the Calendar Sync link field for CCS+."); change forgets validators, History "<name>: Feed link changed to <host>", manual download | calendar_link.md
R4-21 | link source default name is its host ("Calendar" if none); blank name returns to default | calendar_link.md
R4-22 | link downloaded with curl only, no sign-in, no retries, 60 s/20 s timeouts, same limits as CCS+ | calendar_link.md
R4-22.a, R4-22.b, R4-22.c, R4-22.d, R4-22.f | link error texts use host; 401 "<host> wants a login (HTTP 401). Use the calendar's public or secret .ics link..."; a link's status is only ok/error/internal (never auth_failed/blocked/paused); silent hold "Try again later."; History prefix "<name>: " | calendar_link.md
R4-23.d | repeating series with invalid rule skipped, not the whole file | connections.md
R4-23.e | events with STATUS CANCELLED skipped | connections.md
R4-23.f | duplicate identifier in one file: first wins | connections.md
R4-23.i | meeting link (first Zoom, Zoom Gov, Meet, Teams, Webex https link in properties/text) shown first in notes and as URL | events.md EVT-03
R4-24.a, R4-24.b | link History/messages start with source name; 304 text for links | calendar_link.md
R4-25, R4-25.a | removed-from-source events still ending today or later are kept struck through, max 200 per download; ended/hidden/rule-made not kept; History "United removed <n> event(s): ..." or "<name>: gone from the feed: ..." first 5 then " …", each restorable | connections.md CON-07.f
R4-26.a | events of different sources never merge/replace | connections.md
R4-30 | local calendar status always ok, empty message, no checks | local_calendar.md
R4-31 | local calendar named "Local" first time, "CalendarStream" later; placed first in list; becomes default | local_calendar.md
R4-31.a | new local name cut to 100 chars | local_calendar.md
R4-32.a, R4-32.b | non-local default refused "Only a CalendarStream calendar can be the default: the others are read-only."; History "Default calendar: <name>" undoable, no-op if already default | local_calendar.md
R4-33 | export holds events as now, edits included, without hidden and rule-made events | connections.md CON-08
R4-33.a, R4-33.b | export file name = name with chars other than letters/digits/space/./_/- removed + ".ics" ("calendar.ics" if empty); header has name, display time zone, color; same format as feed | connections.md CON-08
R4-34, R4-34.a, R4-34.d | import step 1: calendar must exist; 5 MB limit "That file is too large (over 5 MB)." 413; BEGIN:VCALENDAR check; "No events in that file between those dates." | local_calendar.md
R4-34.b, R4-34.c | From/To days YYYY-MM-DD years 2000-2100; unset = 3,650 days either side of today; swapped if To<From; recurring expanded, cancelled skipped, 5,000 limit | local_calendar.md (CLCL-02.b only says range)
R4-34.e | conflict = same identifier (without import prefix) as a non-rule-made, non-deleted event or previously imported; list shows title, day, time of both | local_calendar.md
R4-34.f | check returns token, event count, conflicts; token valid 30 minutes | local_calendar.md / common.md DEF-01
R4-35, R4-35.a | finish: no match adds, match "merge" replaces title/start/end/all-day/location/notes (stored as edit for source event), otherwise keep existing; added events have no color, new id "cs-<16 hex>@calendar_stream", remember file id for re-import | local_calendar.md
R4-35.b, R4-35.c, R4-35.d | token must be 16 lowercase hex, single use, <=30 min ("That import has expired; choose the file again."); calendar gone message; merge onto vanished original not counted | local_calendar.md
R4-35.e | History "Imported <file or Calendar.ics> into <calendar>: <n> added[, <m> merged][, <d> already there]" undoable | local_calendar.md
R4-36 | removal asks keep=delete (default) or keep=merge, and with merge rules=move or delete (default); "Unknown choice." | connections.md CON-04
R4-36.b | merged events: current state with edits, excluding hidden and rule-made; start/end kept, time-zone overrides cleared; reminders and links follow | connections.md CON-04
R4-36.c | rules only for removed calendar deleted (or moved to target); rules for several lose it; rules for all stay | connections.md CON-04.c/.d
R4-36.d, R4-36.e | removal stops checks, leaves every feed, deletes all stored settings; History "Calendar source removed: <name> (<n> events merged into <target>[, with its rules])" | connections.md CON-04
R4-36.h | removal offers a copy to download first | connections.md CON-04
R4-40.b, R4-40.c | unknown destination kind refused; when adding, no calendars given means every calendar chosen, kept in list order | feeds/generic_feed.md
R4-40.e | feed note cut to 300 chars, defaults to calendar's note | generic_feed.md
R4-40.f | feed Start/End day YYYY-MM-DD, "Check the date.", "The end is before the start." | generic_feed.md (CON-09.e)
R4-40.g | feed color #rrggbb lowercase, else "Choose the color in the color box." | generic_feed.md
R4-40.h | History for feed add/change/remove (`Destination "<name>": <calendars|no sources>`, `Destination added: Calendar Feed "<name>"`, `Destination removed: "<name>"`), undoable | generic_feed.md
R4-40.i | removing a feed also forgets its read times | generic_feed.md
R4-40.j | feeds reorderable; unknown "That isn't there (any more)." | generic_feed.md
R4-41.e | History `Stream name of "<name>" changed; links with the old name no longer work` | generic_feed.md
R4-41.f | only a Calendar Feed has a stream name | generic_feed.md
R4-41.g | stream names compared constant-time, case-sensitive | generic_feed.md
R4-42, R4-42.a | public base is main address, extra, or none (falls back to main, then address page was opened at); address entered when adding saved as main, logged, invalid refused with example | generic_feed.md (CFED-02.f)
R4-43 | five addresses: ".../calendar/<name>.ics", ".../subscribe/<name>", Google "https://calendar.google.com/calendar/r?cid=" + webcal feed address percent-encoded, webcal://, Outlook "https://outlook.live.com/calendar/0/addfromweb?" url+name | generic_feed.md (CFED-03.a)
R4-43.a | public only if https and not localhost/127.0.0.1/testserver, else subscription page warns | generic_feed.md
R4-44.a, R4-44.b, R4-44.c | subscription page in visitor's browser language; shows name, five links, help, "Last updated <date>, <time> · <n> events"; noindex | generic_feed.md
R4-45 | Off/On History `Destination "<name>" switched Off|On` (undoable) | generic_feed.md
R4-45.a | while Off: HTTP 503 "This calendar feed is switched off." Retry-After 3600; unknown still 404 | generic_feed.md (CFED-01.g)
R4-46, R4-46.a | feed serves events of its chosen non-Off calendars, not hidden, overlapping Start/End, sorted by start; calendar name = feed name; color = feed color, else single calendar's color, else none | generic_feed.md
R4-47 | ETag = first 32 hex of SHA-256 of body in quotes, Cache-Control no-cache, If-None-Match list match gives 304 with same headers | generic_feed.md (CFED-04.b)
R4-48 | ICS: VERSION 2.0, PRODID "-//calendar_stream//EN", X-WR-CALNAME and NAME, X-WR-TIMEZONE (display zone), refresh interval and TTL PT1H, content type "text/calendar; charset=utf-8" | generic_feed.md (CFED-04)
R4-48.a | event props: UID, DTSTAMP now UTC, TRANSP TRANSPARENT when free, SUMMARY, LOCATION/DESCRIPTION when not empty | generic_feed.md / connections.md CON-09
R4-48.d | X-CALENDAR-STREAM marker: added, rule, edited, source | generic_feed.md
R4-48.e | alarm detail: DISPLAY alarms, description = title, minutes digits only, duplicates removed, largest first | connections.md CON-09.b
R4-49, R4-49.a | last read classed "Google" if requester contains "google" (any case) else "other"; 304 counts, 503/404 do not; saved at most once per minute | generic_feed.md CFED-05
R4-49.b | chip "Read by Google" (good) / "Not read yet" (in progress); line "Last read by Google <when>" or "Last read <when>" | generic_feed.md CFED-05
R4-50 | status chip labels: ok Healthy, running Syncing…, starting Starting, setup Setup needed, paused Paused, auth_failed Sign-in rejected, blocked Blocked, error Error, internal Internal error; colors good/in-progress/warning/bad | connections.md CON-03
R4-50.a | status, times, counts persisted across restart; "running" restores as "starting" | connections.md CON-03
R4-50.d | source's section opens by itself when status not ok/running/starting or CCS+ lacks credentials | connections.md CON-03
R4-50.e | machine-readable status per source (id, name, type, status, message, running, times, next run, event count) | diagnostics.md / connections.md
R4-51.a | Sync Now waits ~0.5 s, answers still running; page follows status until done | connections.md CON-03.a
R4-52 | each non-local source checked once at start/add, then each interval after previous check ended | connections.md CON-05
R4-52.a | unexpected scheduled failure: next check in 5 minutes | connections.md CON-05
R4-52.d | for CCS+ a value equal to default removes saved value | connections.md CON-05
R4-52.e | saving interval wakes schedule, History "Checks every <n> min from now on" | connections.md CON-05
R4-52.f | interval field offers whole numbers in steps of 5, 15 to 1,440 | connections.md CON-05
R4-53.a | source switched Off keeps being downloaded (unsure) | connections.md CON-03.e
R4-53.b | Off/On of a calendar chosen in a Google destination requests full Google sync; History "Calendar <name> switched Off|On" undoable | connections.md CON-03 / google plugin
R4-54 | calendars reorder by drag/arrows, saved only if changed, unknown refused "That isn't there (any more)." | connections.md (CON-07.e only uses the order)
R4-55 | blank name returns to default; CCS+ default name CALENDAR_NAME "United CCS Schedule", not stored when equal | connections.md CON-02 / ccs.md
R4-55.a | note cut to 120 chars; with no note ever set, the preset/kind description is shown | connections.md CON-02
R4-55.b | History `<name> saved: name "<name>", color <#rrggbb|default color>` undoable; rebuilds feed | connections.md CON-02
R4-56, R4-56.a | color #rrggbb any case stored lowercase, else "Choose the color with the color picker."; "default color" deletes it; no color shows accent #3f51b5 and publishes none | connections.md CON-02.b
R4-56.b | event color precedence: own, rule's, calendar's, none | rules.md / events.md
R4-57, R4-57.a | any change of name/color/rules/events rebuilds from last downloaded copy without downloading; order: rule time changes, edits and added events, rule-made events, rule colors/emoji, reminders; hidden not counted | connections.md

## DIFFERENT (B ID | A ID | A says | B says)
R4-19, R4-40.a | DEF-01 Connections, CON-01.d | at most 50 connections in total, + disabled at limit | 10 calendars and, separately, 20 destinations
R4-41, R4-41.a, R4-41.c | CFED-02.a, CFED-02.c, DEF-01 | generated token 22 chars, >=128 bits, any character allowed (percent-encoded), 1-128 chars | generated 32 chars (24 random bytes), only letters/digits/-/_, 1-128; invalid message "A stream name is up to 128 letters, digits, - or _..."
R4-52.e, R4-52.b | CON-05.c, CON-05.b | next download = last attempt + interval; if passed, immediate download; out-of-range value not valid | next = later of now and last+new interval (no immediate download on change); a saved out-of-range value counts as default; per-source interval
R4-13, R4-52.b | CON-05.a | interval is one admin setting in the database; env value only starting | interval is per source (CCS+ default from env setting, link default 60)
R4-19.f | CLCL-01.d | local calendar added to every feed only when created because none exists | any new local calendar, and the very first calendar, is added to every feed
R4-40.d | CFED-01.e | new feed name/note default to the selected source's and follow it until typed over | default computed at add time from top chosen non-local calendar, else top, else first non-local, else "CalendarStream"; does not follow
R4-48.b | CON-09.a | published event keeps its own time zone | timed events written in UTC, all-day as dates
R4-15.c, R4-15.d | CCCS-04.a/.b, RUL-06 | full-day normalization by RUL-06, originals kept in notes | parser turns a midnight event with no end into an all-day event; other no-end events get end = start and rules set length
R4-55.a | CON-02.c | a note merely repeating the kind is treated as no note | empty note stays empty; with no note ever set, the kind description is shown
R4-11.b | CCCS-03.f | pause lasts until credentials corrected and Sync Now requested | pause ends on any successful sign-in or new credentials/link (count reset)
R4-34.b | CLCL-02.b/UIC-23 | import range excludes events outside it (defaults per UIC-23) | defaults 3,650 days each side, From/To swapped
R4-07.c | CCCS-03.c | browser-patient: 3 attempts, 90 s each | same (1.5 x 60 s), plus pauses 0/5/15 s (see GAP)

## A-ONLY (A ID | one phrase)
SRC-01, SRC-01.a | Sources section container and its border color
FDS-01, FDS-01.a | Feeds section container and its border color
CON-01, CON-01.a, CON-01.c | connection module concept, source/feed/both
CON-01.b | plugin required (Google)
CON-02.d, CON-02.e | kind fixed in header; module look/Expand/Close
CON-03.c | healthy even when another source empty
CON-03.d | event count follows CAP-02 visibility
CON-03.g | exact status-line wording rules ("Last read", no "Last check was successful")
CON-05.d | form-security rules for settings
CON-06.l | retry budget open question
CON-07.d | transparent events stay free (B R4-15.i covers; counted covered) - not A-only
CON-09.c | meeting address first line of notes (partly B R4-48.c)
CCCS-01.c, CLNK-01.d, CLCL-01.f, CFED-01.i | role rows (is a source / feed)
CCCS-02.a | guidance Calendar Sync vs CCS login
CCCS-02.b | setup shown with the source, return after save
CCCS-02.d | credentials labeled Username
CCCS-02.i | stale validation feedback removed on edit
CCCS-02.j | save/verify progress and saved acknowledgement
CCCS-02.k | setup guidance (trips as one event, Accomplished checklist)
CCCS-02.l | credential import from old config (open question)
CCCS-04.b | original times in notes after normalization
CCCS-05.b | upload ends setup-needed state
CLNK-01.b | Outlook/Microsoft 365/iCloud links
CLNK-01.c | Apple preset selection, United CCS+ name preset, Google secret-address guidance
CLCL-01.a | fresh install starts with one Local, no CCS+/destinations
CLCL-02.d, CLCL-02.e | discard incoming copy; apply choice to all remaining conflicts
CLCL-03.b | valid saved default wins over source order (B R4-32.c is similar)
CFED-01.c | no special Local rule for feed membership
CFED-02.a | token strength shown as UIC-18 hint
CFED-02.b | replaced token stops working
CFED-03.b | sharing via copy, device share, email/SMS
CFED-03.c | provider subscription guidance (12 hours, name, color)
CFED-05.b | ordinary feed shows reads not next-push schedule

## COUNT
B rows total 236: covered 58, different 11, gap 167; A rows only-in-A: 33 lines (some lines list several IDs)
