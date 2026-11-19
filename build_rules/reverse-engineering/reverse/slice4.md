# Slice 4: sources, local calendars, feeds, source status (reverse-engineered)

Columns: | ID | statement | evidence (file:function) |

## 1. The CCS+ source

| ID | Statement | Evidence |
|---|---|---|
| R4-01 | CCS+ is a calendar source that can be added once. | routes/sources.py:add_source |
| R4-01.a | Adding CCS+ when it is already a source is refused with "CCS+ Calendar Sync is already a source." | routes/sources.py:add_source |
| R4-01.b | The CCS+ source always has the fixed identifier "ccs". | routes/sources.py:add_source; main.py:SID_RE |
| R4-01.c | When CCS+ is added, the person may choose which of its starter rules come with it; each chosen starter rule is added to the rule list, applying to CCS+. | routes/sources.py:add_source |
| R4-02 | CCS+ credentials are a Username (UID) and a Calendar Sync password, both kept by the app. | logins.py:Logins.save_ccs |
| R4-02.a | The Username is trimmed of surrounding whitespace and must be 2 to 64 characters, each a letter, digit, dot, underscore, at sign or hyphen. | logins.py:UID_RE, save_ccs |
| R4-02.b | An invalid Username is refused with "Enter your Username (letters and digits, e.g. U123456)." | logins.py:save_ccs |
| R4-02.c | A trailing line break (CR or LF) is removed from the password; other whitespace is kept. | logins.py:save_ccs |
| R4-02.d | A blank password keeps the saved password; it is never shown again. | logins.py:save_ccs |
| R4-02.e | A blank password when none is saved is refused with "Enter the Calendar Sync password too." | logins.py:save_ccs |
| R4-02.f | A password longer than 200 characters is refused with "That password is too long." | logins.py:save_ccs |
| R4-02.g | The password is stored encrypted, never in clear text; if it cannot be decrypted (the database password changed) it counts as not entered and must be entered again. | logins.py:ccs, save_ccs |
| R4-02.h | The CCS+ source counts as configured only when both the Username and the password are present. | logins.py:ccs_configured |
| R4-02.i | Saving the credentials resets the count of rejected sign-ins to 0, forgets the stored download validators (see R4-06), and writes the History line "CCS+ Username and Calendar Sync password saved". | routes/sources.py:set_ccs_login |
| R4-02.j | After saving credentials from a page that reloads, a Sync Now starts at once and the page returns to the CCS+ module after about 1.5 seconds. When saved in place by the page's script, the page asks for a verification instead (R4-03). | routes/sources.py:set_ccs_login |
| R4-02.k | Removing CCS+ deletes the saved credentials and the saved Calendar Sync link, and resets its status. Undo in History can bring them back. | routes/sources.py:remove_source |
| R4-02.l | Credentials are sent to the download program without appearing on any command line or in the address (a file-style config on standard input for curl). | calendars/downloads.py:_download_curl |
| R4-03 | After credentials are saved, the page can ask the app to verify them: the app waits for any running download of CCS+ to finish (up to 120 seconds), runs a manual download, waits again, and answers Validated or Failed with the status message. | routes/sources.py:verify, _wait_idle |
| R4-03.a | For CCS+, verification succeeds only when the last sign-in succeeded and the status is "ok". | routes/sources.py:verify |
| R4-03.b | For a calendar link source, verification succeeds only when the status is "ok". | routes/sources.py:verify |
| R4-03.c | A verification kind other than ccs, google or feed is refused with "Unknown kind of login." | routes/sources.py:verify |
| R4-04 | The Calendar Sync link (Site Address) of CCS+ defaults to https://ccsplus.ual.com/calendarsyncapi/api/Calendar/GetCalendar. | config.py:DEFAULT_CALENDAR_URL |
| R4-04.a | The link can be changed on the page and is saved; an empty value, or a value equal to the default, deletes the saved link and the default applies. A link set on the page wins over one in the environment settings (CCS_CALENDAR_URL). | routes/sources.py:set_ccs_login; services/calendar_sources.py:calendar_url |
| R4-04.b | A link that does not start with https:// or has no host is refused with "The Calendar Sync link must start with https://". | routes/sources.py:set_ccs_login, set_link |
| R4-04.c | Changing the link forgets the stored download validators (R4-06), resets the rejected-sign-in count to 0 and starts a download. | routes/sources.py:set_link, set_ccs_login |
| R4-04.d | A "reset" action deletes the saved link (back to the default), writes "Calendar Sync link reset to the default" to History, resets the rejected-sign-in count and starts a download. | routes/sources.py:set_link |
| R4-04.e | After saving a changed link, History says "Calendar Sync link set to <host><path>". | routes/sources.py:set_link |
| R4-05 | A CCS+ download sends the Username and password as HTTP Basic sign-in, and asks for the content type "text/calendar, */*;q=0.5". | calendars/downloads.py:_download_curl, _download_browser |
| R4-05.a | The sign-in is sent only to the host of the original address; after a redirect to another host it is not sent (browser-like client). | calendars/downloads.py:_download_browser |
| R4-06 | Conditional download: when a copy has already been downloaded, the download sends If-None-Match with the stored ETag and If-Modified-Since with the stored Last-Modified, each only when it is not empty. | calendars/downloads.py; services/source_jobs.py:run_once |
| R4-06.a | The validators are stored only when a download is accepted and published; they are used only while a downloaded copy exists. | services/source_jobs.py:run_once |
| R4-06.b | A "not modified" answer (HTTP 304) sets the status to ok, records "Schedule downloaded from CCS+: no changes" in History as information, sets the last detail to "no changes", and the message to "Up to date: <n> events in feed (no changes)". | services/source_jobs.py:run_once |
| R4-07 | The CCS+ client is chosen by the CCS_CLIENT setting: auto, browser, browser-patient or curl. An unset or unknown value means auto. The name is case-insensitive and trimmed. | calendars/downloads.py:ccs_client; calsync.py:CCS_CLIENTS |
| R4-07.a | "curl" makes one attempt with the curl program, normal timeout, no pause. | calsync.py:_PLANS |
| R4-07.b | "browser" makes one attempt with the browser-like client, normal timeout, no pause. | calsync.py:_PLANS |
| R4-07.c | "browser-patient" makes three attempts with the browser-like client, each with 1.5 times the normal timeout, pausing 0 seconds before the first, 5 seconds before the second and 15 seconds before the third. | calsync.py:_PLANS |
| R4-07.d | "auto" makes up to three attempts: browser-like with the normal timeout and no pause; browser-like with 2 times the timeout after a 3-second pause; then curl with the normal timeout and no pause. | calsync.py:_PLANS |
| R4-07.e | The normal timeout of a CCS+ attempt is 60 seconds overall and 20 seconds to connect. | calsync.py:download |
| R4-07.f | Only two failures trigger the next attempt: no reply in time and a refusal (HTTP 403). Any other outcome (success, 304, 401, other HTTP errors, other errors) ends the sequence at once. | calendars/downloads.py:download |
| R4-07.g | When all attempts fail, the error of the last attempt is reported. | calendars/downloads.py:download |
| R4-07.h | Each failed attempt is logged as a warning naming the client and the reason ("no reply in <n> s" or "refused (HTTP 403)"); when a later attempt answers, an information line "CCS+ download answered after <attempts>" is logged. | calendars/downloads.py:download |
| R4-07.i | The download record kept for Report a problem lists every attempt with its client and result and names the client that answered: "curl_cffi <version>, as chrome" for the browser-like client, or the curl version. | calendars/downloads.py:download, _download_browser, _download_curl |
| R4-08 | The browser-like client presents the connection (TLS and HTTP/2 fingerprint) of the newest Chrome profile available. | calsync.py:BROWSER_PROFILE; calendars/downloads.py:_download_browser |
| R4-08.a | If the browser-like client is not installed, that attempt fails with "The browser-like client (curl_cffi) isn't installed in this container." | calendars/downloads.py:_download_browser |
| R4-08.b | If curl is not installed, an attempt with curl fails with "curl isn't installed in this container (it's needed to download calendars)." | calendars/downloads.py:_download_curl |
| R4-09 | Download errors for CCS+ and their texts: | calendars/downloads.py:_finish and the transports |
| R4-09.a | HTTP 401 is a rejected sign-in: "CCS+ rejected the UID or Calendar Sync password (HTTP 401). Check both in the CCS+ Calendar Sync box (the Calendar Sync password, not your CCS login)." | calendars/downloads.py:_finish |
| R4-09.b | HTTP 403 is a block: "Access denied by <server>, HTTP 403" followed by ", reference <id>" when the reply contains "Reference #<id>", then a full stop. <server> is "Akamai (United's bot protection)" when the Server header contains "akamai" (any case), else the Server header value, else "the server". | calendars/downloads.py:_finish |
| R4-09.c | Any other status of 400 or higher is an error: "<who> answered HTTP <status>: <first 160 characters of the reply with tags removed, or 'no details'>". <who> is "CCS+". | calendars/downloads.py:_finish |
| R4-09.d | A successful reply whose first 2,000 bytes do not contain "BEGIN:VCALENDAR" is an error: "<who> answered, but not with a calendar file (<content type or 'unknown type'>): <first 160 characters of the reply>". | calendars/downloads.py:_finish |
| R4-09.e | Connected but no reply within the timeout (silent hold): "Connected to <host>, but it sent no reply within <n> seconds. United's bot protection may be holding the request; use Upload & publish in the CCS+ Calendar Sync box in the meantime." where <n> is the whole-second timeout of that attempt. | calendars/downloads.py:_no_reply |
| R4-09.f | Not connected within 20 seconds: "Couldn't connect to <host> within 20 seconds (network, DNS or firewall problem on this server)." | calendars/downloads.py |
| R4-09.g | Network failure: "Couldn't reach <host>: <reason>". | calendars/downloads.py |
| R4-09.h | A link that is not https, or a redirect to a non-https address: "The Calendar Sync link must start with https://, and may only redirect to https:// addresses (CalendarStream only downloads over https)." | calendars/downloads.py:_not_https |
| R4-09.i | More than 5 redirects: "<host> redirected too many times; check the Calendar Sync link." | calendars/downloads.py:_too_many_redirects |
| R4-09.j | A reply over 5 MB (5,242,880 bytes): "<host> sent more than 5 MB, which is too large for a schedule." | calendars/downloads.py:_too_large |
| R4-09.k | Redirect handling: up to 5 redirects (status 301, 302, 303, 307, 308 with a Location) are followed; the 6th redirect is an error (R4-09.i). | calendars/downloads.py; calsync.py:MAX_REDIRECTS |
| R4-10 | Outcome states of an automatic or manual CCS+ run: a rejected sign-in gives the status "auth_failed" (History error "Sign-in rejected: <message>"); a block gives "blocked" (History error "Blocked: <message>"); any other source error gives "error" (History error "Download failed: <message>"); an unexpected failure of the app itself gives "internal" with "<error type>: <message>" (History error "Unexpected error: ..."). | services/source_jobs.py:run_once |
| R4-10.a | Each rejected sign-in adds 1 to the rejected-sign-in count; a successful sign-in resets it to 0 and records the time of the last sign-in and whether it succeeded. A reply that is not a sign-in rejection (including 304) counts as a successful sign-in. | services/source_jobs.py:run_once |
| R4-10.b | A block, a silent hold or any other error does not change the rejected-sign-in count. | services/source_jobs.py:run_once |
| R4-11 | Pause after rejected sign-ins: when the count has reached 2, scheduled (automatic) runs do not download; the status becomes "paused" with the message "Automatic downloads paused after <n> rejected sign-ins, to avoid locking your account. Check the Username and Calendar Sync password in the CCS+ Calendar Sync box, then press Sync now." | services/source_jobs.py:run_once; main.py:MAX_AUTH_FAILURES |
| R4-11.a | Sync Now (a manual run) always downloads, even while paused. | services/source_jobs.py:run_once |
| R4-11.b | A successful sign-in or saving new credentials or a new link resets the count to 0, which ends the pause. | routes/sources.py; services/source_jobs.py |
| R4-11.c | While paused, the source header shows "Automatic checks paused" in place of the next-check time. | templates/index/sources.html |
| R4-12 | When CCS+ has no credentials yet, a run does not download: the status becomes "setup" with the message "Enter your CCS+ Username and Calendar Sync password to start downloading the schedule." and the Sync Now button is disabled. | services/source_jobs.py:run_once; templates/index/sources.html |
| R4-13 | The CCS+ schedule check interval is set per source in minutes; see R5-05 for the limits. The default for CCS+ is the SYNC_INTERVAL_MINUTES setting (older name SCRAPE_INTERVAL_MINUTES), default 60, never less than 15. | config.py:Settings.interval_minutes; services/source_jobs.py:interval_minutes |
| R4-14 | Upload (Manual Upload): a Calendar.ics downloaded by hand from CCS+ can be uploaded and replaces the schedule. | routes/sources.py:upload |
| R4-14.a | The file may be at most 5 MB (5,242,880 bytes); a larger file is refused with "That file is too large for a schedule (over 5 MB)." (status 413). | routes/sources.py:upload |
| R4-14.b | A file whose first 2,000 bytes do not contain "BEGIN:VCALENDAR" is refused with "That file isn't a calendar (.ics) file: <first 120 characters, or 'it's empty'>". | calendars/validation.py:check_calendar |
| R4-14.c | An accepted upload is published like a download (R4-15), with the wording "uploaded by hand", forgets the stored download validators, and records the attempt time. | routes/sources.py:upload |
| R4-14.d | A rejected upload writes "Upload rejected: <message>" to History as an error. | routes/sources.py:upload |
| R4-15 | Publishing a downloaded or uploaded CCS+ file reads its events and builds the feed: events keep United's IDs (UID), times and details. | services/publishing.py:apply_calendar; calendars/parsing.py:parse |
| R4-15.a | An event without a start time is skipped. | calendars/parsing.py:_event |
| R4-15.b | The end is DTEND, else start plus DURATION. | calendars/parsing.py:_event |
| R4-15.c | A timed event starting exactly at midnight (local time zone) with no end becomes an all-day event on that date (a day code such as RDO, HDO, VRDO). | calendars/parsing.py:_event |
| R4-15.d | Any other timed event with no end has no end recorded and its end equals its start; the rules decide its length (the defaults mode used when reading is "rules"). | calendars/parsing.py:_event; main.py:RULES_PARSE |
| R4-15.e | An all-day event with no end lasts one day. | calendars/parsing.py:_event |
| R4-15.f | An event with no title is titled "(no title)". | calendars/parsing.py:_event |
| R4-15.g | The notes (description) are cut to 2,000 characters. | calendars/parsing.py:_event |
| R4-15.h | An event with no UID gets an identifier made from its start and title. | calendars/parsing.py:_event |
| R4-15.i | An event whose TRANSP is TRANSPARENT (any case) is "free", otherwise "busy". | calendars/parsing.py:_event |
| R4-15.j | Times without a zone are taken in the display time zone (the TZ setting, default America/Chicago); published start and end of timed events are expressed in that zone. | calendars/parsing.py; config.py |
| R4-15.k | A file that cannot be read as a calendar is an error: "The calendar file from CCS+ couldn't be read: <reason>". | calendars/parsing.py:parse |
| R4-15.l | Events are sorted by start time. | calendars/parsing.py:parse |
| R4-16 | If a downloaded or uploaded file produces no events while the source already has events, it is rejected: status "error", message "The <how> calendar has no events. Keeping the previous feed (<n> events) in case this is a glitch.", a History warning, and the previous events stay. | services/publishing.py:apply_calendar |
| R4-17 | The first download of a source is recorded with the detail "first copy"; later changes are recorded as "<a> new, <r> removed", counting events by UID. An unchanged file gives the detail "no changes" and "Up to date: <n> events in feed (no changes)". | services/publishing.py:apply_calendar |
| R4-17.a | An accepted download sets the status to ok, the last-success time to now, and when the file differs from the previous one also the last-change time; the message is "<How, capitalised>: <n> events in feed (<detail>)" and History records "Schedule <how>: <n> events in feed (<detail>)". | services/publishing.py:apply_calendar |
| R4-17.b | <how> is "downloaded from CCS+", "uploaded by hand", or "downloaded from <host>" for links. | services/source_jobs.py; routes/sources.py |
| R4-18 | The last raw download and the last download record (address, status, seconds, bytes, client, selected headers) are kept for Report a problem; the headers kept are content-type, content-length, content-disposition, etag, last-modified, server, date, cache-control and www-authenticate. | services/source_jobs.py:run_once; calsync.py:_KEEP |

## 2. Calendar links and uploaded files as sources

| ID | Statement | Evidence |
|---|---|---|
| R4-19 | At most 10 calendars (sources of every kind together) can exist; adding an 11th is refused with "Up to 10 calendars can be added." | routes/sources.py:add_source |
| R4-19.a | The kinds of source that can be added are: a CalendarStream (local) calendar, CCS+ (once, R4-01), and a calendar link ("ics"). Any other kind is refused with "Unknown kind of calendar source." | routes/sources.py:add_source |
| R4-19.b | A calendar link has one of three presets, Google Calendar, Apple Calendar or Calendar feed ("other"); an unknown preset is stored as "other". The preset only changes the help and description shown. | routes/sources.py:add_source; main.py:SOURCE_PRESETS |
| R4-19.c | A calendar link source gets a generated identifier of the form "f" followed by 6 lower-case hexadecimal digits; a local calendar gets "l" followed by 6 hexadecimal digits; neither collides with an existing identifier. | routes/sources.py:add_source; services/calendar_sources.py:new_local; main.py:SID_RE |
| R4-19.d | A name entered when adding is cut to 100 characters after collapsing runs of whitespace to one space; a note is cut to 120 characters the same way. | routes/sources.py:add_source |
| R4-19.e | Adding a source writes the History line "Calendar source added: <name>" (type Calendar, undoable), builds its feed and starts its checks (R4-52) at once. | routes/sources.py:add_source |
| R4-19.f | When the added source is the first calendar of all, or is a local calendar, it is also added to every feed (R4-40); other new sources are in no feed until chosen. | routes/sources.py:add_source |
| R4-20 | A calendar link is entered as an address; "webcal://" (any case) at the start is the same as "https://". | routes/sources.py:_feed_link |
| R4-20.a | The address is trimmed; it must then use https and have a host, else it is refused with "The feed link must start with https:// (or webcal://)." | routes/sources.py:_feed_link |
| R4-20.b | Adding a link equal to an address already used by another source is refused with "That feed is already a source." (comparison is on the exact text after webcal conversion). | routes/sources.py:add_source |
| R4-20.c | Changing the link of an existing calendar link source follows the same address rules (R4-20, R4-20.a); CCS+ is refused with "Use the Calendar Sync link field for CCS+." | routes/sources.py:set_source_url |
| R4-20.d | After a change of link, the stored download validators of that source are forgotten, History records "<name>: Feed link changed to <host>", and a manual download starts. When saved in place by the page's script, the page asks for a verification instead (R4-03.b). | routes/sources.py:set_source_url |
| R4-21 | A calendar link source's default name is the host of its address ("Calendar" when none); a name set on the page replaces it, and a blank name goes back to the default. | services/calendar_sources.py:calendar_name; routes/sources.py:set_tags |
| R4-22 | A link source is downloaded with the curl program only (never the browser-like client), with no sign-in, with the same Accept, conditional-read, https-only, 5-redirect and 5 MB limits as CCS+ (R4-05, R4-06, R4-09.h to R4-09.k), a 60-second overall timeout and a 20-second connect timeout, and no retries. | calsync.py:download; calendars/downloads.py:download |
| R4-22.a | The error texts that name the source use the link's host in place of "CCS+" ("<host> answered HTTP <status>: ...", "<host> answered, but not with a calendar file (...)"). | calendars/downloads.py:_finish |
| R4-22.b | HTTP 401 on a link: "<host> wants a login (HTTP 401). Use the calendar's public or secret .ics link, which works without one." Its History line is "<name>: Download failed: ..." and its status is "error" (a link source never becomes auth_failed, blocked or paused). | calendars/downloads.py:_finish; services/source_jobs.py:run_feed |
| R4-22.c | HTTP 403 on a link: "Access denied by <server>, HTTP 403..." as R4-09.b; the status is "error". | services/source_jobs.py:run_feed |
| R4-22.d | A silent hold on a link says "Connected to <host>, but it sent no reply within <n> seconds. Try again later." | calendars/downloads.py:_no_reply |
| R4-22.e | A link that is not https, or redirects to a non-https address, is refused with "The feed link must start with https://, and may only redirect to https:// addresses (CalendarStream only downloads over https)."; more than 5 redirects gives "<host> redirected too many times; check the feed link." | calendars/downloads.py:_not_https, _too_many_redirects |
| R4-22.f | Any other unexpected failure of the app itself gives the status "internal" with "<error type>: <message>" and History "<name>: Unexpected error: ...". | services/source_jobs.py:run_feed |
| R4-22.g | A download that fails keeps the previously published events; nothing is removed on failure. | services/source_jobs.py:run_feed |
| R4-23 | A downloaded link file is read with the same rules as R4-15 (start required, end from DTEND or DURATION, no title becomes "(no title)", notes cut to 2,000 characters, TRANSPARENT is free, unzoned times in the display time zone), with these differences: | calendars/parsing.py:parse_feed |
| R4-23.a | Each event's identifier is "<source id>/<UID>", so sources cannot collide with each other or with CCS+; an event with no UID gets an identifier made from its start and title. | calendars/parsing.py:parse_feed |
| R4-23.b | Repeating events (repeat rule, extra dates or an individually moved occurrence) are expanded into occurrences; an occurrence's identifier also ends with "/<its original start>", so an occurrence the feed moves keeps its edits. | calendars/parsing.py:parse_feed |
| R4-23.c | Only occurrences from 365 days before today to 730 days after today are kept. | services/publishing.py:feed_window |
| R4-23.d | A repeating series with an invalid rule is skipped without failing the whole file. | calendars/parsing.py:parse_feed |
| R4-23.e | Events whose STATUS is CANCELLED (any case) are skipped. | calendars/parsing.py:parse_feed |
| R4-23.f | An event whose identifier was already seen in the same file is skipped (first wins). | calendars/parsing.py:parse_feed |
| R4-23.g | At most 5,000 events are kept from one link; the events are sorted by start first and the earliest 5,000 are kept. | calendars/parsing.py:parse_feed; calsync.py:MAX_FEED_EVENTS |
| R4-23.h | A file that cannot be read is an error: "The calendar file couldn't be read: <reason>". | calendars/parsing.py:parse_feed |
| R4-23.i | Events carry an online meeting link (the first Zoom, Zoom Gov, Google Meet, Teams (microsoft.com or live.com) or Webex https link found in the event's properties and text); it is shown first in the published notes and as the event's URL. | calendars/meeting.py; calendars/feed.py:_write_fields |
| R4-24 | The same acceptance rules as R4-16 and R4-17 apply to a link: an empty file when events exist is refused and the previous events stay; the first copy is "first copy"; later changes "<a> new, <r> removed"; an unchanged file "no changes". | services/publishing.py:apply_calendar |
| R4-24.a | A link's History lines and messages use "downloaded from <host>" and start with the source's name ("<name>: Schedule downloaded from <host>: 12 events in feed (first copy)"). | services/source_jobs.py:run_feed; services/state.py:record |
| R4-24.b | A "not modified" answer sets the status to ok, the detail to "no changes" and the message to "Up to date: <n> events in feed (no changes)". | services/source_jobs.py:run_feed |
| R4-25 | Events a source no longer has (taken out of a downloaded file) that still end today or later are kept in that calendar, struck through, as events added to it, at most 200 per download. Events that ended before today are not kept; hidden and rule-made events are not kept. | services/deletions.py:keep_removed |
| R4-25.a | The History line is "United removed <n> event(s): "<title>" (<date>), ..." for CCS+, or "<name>: gone from the feed: <n> event(s): ..." for a link, listing the first 5 and ending with " …" when there are more; each can be restored. | services/deletions.py:keep_removed |
| R4-26 | The order of the calendars on the page is their priority when events or rules conflict (earlier wins); it no longer decides the default calendar. | main.py (header comment); routes/sources.py:move_source |
| R4-26.a | Events of different sources never merge or replace each other; each keeps its own identifier and appears in the feeds that include its source. | calendars/parsing.py:parse_feed; services/google_sync.py:dest_events |
| R4-26.b | unsure: how two sources' events are shown when they overlap in time is decided by the rules (color, emoji, time: the higher rule wins); the calendar order is the rule priority "its own ones first, unless moved". | routes/page.py:source_view; routes/sources.py:move_source |
| R4-27 | An uploaded file (for CCS+, R4-14) is the only upload kind of source; a link source cannot be uploaded to. | routes/sources.py:upload |
| R4-27.a | An uploaded file for import into a calendar is described in R4-34 and R4-35. | routes/sources.py:import_check |

## 3. Local calendars (CalendarStream calendars)

| ID | Statement | Evidence |
|---|---|---|
| R4-30 | A local calendar has events added by hand (and imported), nothing to download and no schedule: it is always status "ok" with an empty message, and no checks run for it. | routes/page.py:source_view; services/source_jobs.py:start_source |
| R4-31 | There is always at least one local calendar. When none exists (new install or the last one removed) one is made, placed first in the list and in every feed, named "Local" (the first time) or "CalendarStream" (when one was made before), and becomes the default calendar. | services/calendar_sources.py:ensure_local |
| R4-31.a | A new local calendar is created from the Add calendar choice "local"; its name is cut to 100 characters after collapsing whitespace, and a blank name gives "Local". | routes/sources.py:add_source |
| R4-32 | The default calendar is the local calendar events added on the page go to unless another is chosen. | services/calendar_sources.py:default_sid |
| R4-32.a | Only a local calendar can be made the default; any other is refused with "Only a CalendarStream calendar can be the default: the others are read-only." | routes/sources.py:default_source |
| R4-32.b | Making a calendar the default writes History "Default calendar: <name>" (undoable) and changes nothing when it already is the default. | routes/sources.py:default_source |
| R4-32.c | When the stored default is missing or no longer a local calendar, the first local calendar is the default (position in the list otherwise does not matter); with no local calendar, the first source. | services/calendar_sources.py:default_sid, ensure_local |
| R4-33 | Export: a calendar can be downloaded as a .ics file holding its events as they are now, edits included, without hidden events and without events made by rules. | routes/sources.py:export_source |
| R4-33.a | The file name is the calendar's name with every character other than letters, digits, space, dot, underscore and hyphen removed and trimmed, plus ".ics"; "calendar.ics" when nothing is left. | routes/sources.py:export_source |
| R4-33.b | The exported file has the calendar's name, display time zone and color (R4-56) in its header and is the same format as a published feed (R4-48). | routes/sources.py:export_source |
| R4-34 | Import, step 1 (check): a .ics file is read and the events of it that already exist in the chosen calendar are listed. The calendar must exist, else "That calendar source doesn't exist (any more)." | routes/sources.py:import_check |
| R4-34.a | The file may be at most 5 MB (5,242,880 bytes), else "That file is too large (over 5 MB)." (status 413). A file whose first 2,000 bytes lack "BEGIN:VCALENDAR" is refused as in R4-14.b. | routes/sources.py:import_check |
| R4-34.b | A From and a To day may be given (format YYYY-MM-DD, years 2000 to 2100); an empty or invalid one is treated as not given. Not given means 3,650 days before today (From) and 3,650 days after today (To). If To is before From they are swapped. | routes/sources.py:import_check; calendars/view_helpers.py:_opt_day |
| R4-34.c | Only events whose start date lies between From and To inclusive are imported; repeating events are expanded into occurrences within that range, and the file is read as in R4-23 (cancelled skipped, 5,000-event limit). | routes/sources.py:import_check |
| R4-34.d | When no event is left, the import is refused with "No events in that file between those dates." | routes/sources.py:import_check |
| R4-34.e | An imported event matches one already in the calendar when its identifier (without the import prefix) equals the identifier of an existing event of that calendar that is not rule-made and not deleted, or of an event previously imported from the same identifier. Matching events are conflicts; the answer lists, for each, the title and day (plus the time HH:MM when not all-day) of the existing and of the file's version. | routes/sources.py:import_check, _import_key, _when |
| R4-34.f | The step answers with a token, the number of events, and the conflicts; the token is valid for 30 minutes. | routes/sources.py:import_check; IMPORT_KEEP |
| R4-35 | Import, step 2 (finish): for each event in the file, a new event is added to the calendar when there is no match; for a match, the choice is "merge" (the file's title, start, end, all-day, location and notes replace the existing event's; for a source event this is stored as an edit) or anything else, which keeps the existing event and drops the file's copy. | routes/sources.py:import_finish |
| R4-35.a | Added events are events of that calendar with no color, a new identifier "cs-<16 hex digits>@calendar_stream", and remember the file's identifier so a later re-import matches them. | routes/sources.py:import_finish |
| R4-35.b | A token that is not 16 lower-case hexadecimal digits, unknown or older than 30 minutes is refused with "That import has expired; choose the file again."; a token can be used once. | routes/sources.py:import_finish |
| R4-35.c | If the calendar no longer exists: "That calendar isn't here any more." | routes/sources.py:import_finish |
| R4-35.d | A merge onto a source event whose original is no longer available changes nothing and is not counted. | routes/sources.py:import_finish |
| R4-35.e | History records (undoable) "Imported <file name, or Calendar.ics> into <calendar>: <n> added" followed by ", <m> merged" when m > 0 and ", <d> already there" when d > 0. | routes/sources.py:import_finish |
| R4-36 | Removing a calendar asks what to do with its events: delete them (keep=delete, the default) or merge them into another calendar (keep=merge); and, with a merge, whether its own rules move with them (rules=move) or are deleted (rules=delete, default). Any other value is refused with "Unknown choice." | routes/sources.py:remove_source |
| R4-36.a | A merge target is an existing calendar other than the one removed, or "new" (a new local calendar with the same name and color, put where the removed one was, and in every feed the removed one was in); otherwise "Choose the calendar to merge its events into." | routes/sources.py:remove_source |
| R4-36.b | Merged events are the calendar's events as they are now (edits included), except hidden and rule-made ones; each becomes an added event of the target with start and end kept, time-zone overrides cleared; an added event keeps its identifier, any other gets a new one; reminders and links follow each event. | routes/sources.py:copy_events |
| R4-36.c | Rules that apply only to the removed calendar are deleted, or, with rules=move and a merge, now apply to the target; rules applying to several calendars lose the removed one; rules applying to all stay. | routes/sources.py:remove_source |
| R4-36.d | A removed calendar's checks stop, it leaves every feed, and all its stored settings are deleted (name, color, tags, rule subscriptions, defaults, note, interval, validators, status, feed reads, Off). | routes/sources.py:remove_source; main.py:SOURCE_BASES |
| R4-36.e | The History line is "Calendar source removed: <name>" followed by " (<n> events merged into <target>" and ", with its rules" when they moved, ")" when merged; the removal can be undone in History. | routes/sources.py:remove_source |
| R4-36.f | The last local calendar cannot be removed: it is emptied instead (events merged or deleted as chosen, its own rules deleted unless moved) and stays in every feed and rule; History: "Emptied <name> (<n> events merged into <target>)" or "(its events deleted)". | routes/sources.py:remove_source; services/calendar_sources.py:last_local |
| R4-36.g | After removing any calendar, a local calendar is made again if none is left (R4-31). | routes/sources.py:remove_source |
| R4-36.h | Before removing, the page offers a copy of the calendar to download first (R4-33). | routes/sources.py:export_source (docstring) |

## 4. Feeds (Calendar Feed destinations)

| ID | Statement | Evidence |
|---|---|---|
| R4-40 | A feed (destination of the type Calendar Feed) publishes the events of the calendars chosen for it as a .ics address any calendar application can subscribe to. | routes/destinations.py:calendar |
| R4-40.a | At most 20 destinations (feeds and Google modules together) can exist; a 21st is refused with "Up to 20 destinations can be added." | routes/destinations.py:add_destination |
| R4-40.b | An unknown kind is refused with "Unknown kind of destination." | routes/destinations.py:add_destination |
| R4-40.c | When adding, the calendars given are those chosen, kept in the order of the calendar list and ignoring unknown ones; when none are given at all, every calendar is chosen. | routes/destinations.py:add_destination |
| R4-40.d | The feed's name is cut to 100 characters after collapsing whitespace; when left empty it is the name of the top chosen calendar that comes from somewhere (not a local one), else the top chosen calendar, else the first non-local calendar, else "CalendarStream". | routes/destinations.py:add_destination, top_named_calendar; services/calendar_sources.py:first_named_calendar |
| R4-40.e | The feed's note is cut to 300 characters; when left empty it is that calendar's note (cut to 300). | routes/destinations.py:add_destination |
| R4-40.f | A feed may have a Start day and an End day (YYYY-MM-DD); an empty one means no limit. An unreadable day is refused with "Check the date." naming that field; an End before the Start is refused with "The end is before the start." | routes/destinations.py:_dest_dates |
| R4-40.g | A feed has its own color (#rrggbb, stored lower-case); anything else is refused with "Choose the color in the color box." | routes/destinations.py:update_destination |
| R4-40.h | Changing a feed's name (kept when the new one is blank), note, chosen calendars, dates and color writes History `Destination "<name>": <calendar names, or "no sources">`; adding writes `Destination added: Calendar Feed "<name>"` (undoable). | routes/destinations.py:update_destination, add_destination |
| R4-40.i | Removing a feed makes its links and subscription page stop working, forgets its read times, and writes `Destination removed: "<name>"`. | routes/destinations.py:remove_destination |
| R4-40.j | The order of the feeds can be changed by moving one above or below another; an unknown feed is refused with "That isn't there (any more)." | routes/destinations.py:move_destination; item_order.py:_moved |
| R4-41 | The stream name is the secret part of a feed's addresses: 1 to 128 characters, each a letter, digit, hyphen or underscore. | routes/destinations.py:STREAM_RE |
| R4-41.a | When a new feed has no stream name entered, a random one of 32 characters is made (24 random bytes in URL-safe text). | routes/destinations.py:add_destination |
| R4-41.b | A stream name may be typed or a whole old feed or subscribe address may be pasted; the name is taken from after "/calendar/" or "/subscribe/", without a ".ics" ending or trailing slash. The input is trimmed first. | routes/destinations.py:_stream_value |
| R4-41.c | An invalid name is refused with "A stream name is up to 128 letters, digits, - or _ (or paste a whole old feed link)." | routes/destinations.py:_stream_value, set_stream |
| R4-41.d | A name already used by another feed is refused with "Another feed already uses that stream name." | routes/destinations.py:_stream_value |
| R4-41.e | Changing the stream name writes History `Stream name of "<name>" changed; links with the old name no longer work`; an unchanged or empty stream value changes nothing. | routes/destinations.py:update_destination, set_stream |
| R4-41.f | Only a Calendar Feed has a stream name; otherwise "Only calendar feeds have a stream name." | routes/destinations.py:set_stream |
| R4-41.g | Stream names are compared in constant time and exactly (case-sensitive). | routes/destinations.py:dest_for_token |
| R4-42 | A feed has a public address base: one of the known public addresses (the main one from Settings, then the extra ones), or none. Any other value is stored as none, meaning the main public address, else the address the page was opened at (without trailing slash). | routes/destinations.py:add_destination, update_destination; services/addresses.py |
| R4-42.a | A public address entered when adding a feed is normalised, saved as the main public address, and logged "Public address set to <address>"; an invalid one is refused with "Enter the address people use to reach this page, e.g. https://cal.example.com". | routes/destinations.py:add_destination |
| R4-43 | A feed has five addresses made from its stream name and base: the feed address "<base>/calendar/<name>.ics"; the subscription page "<base>/subscribe/<name>"; an Add-to-Google link "https://calendar.google.com/calendar/r?cid=" followed by the feed address with its scheme replaced by "webcal://" and fully percent-encoded; a "webcal://" address of the feed; and an Outlook link "https://outlook.live.com/calendar/0/addfromweb?" with parameters url (the feed address) and name (the feed's name, "CalendarStream" when empty). | services/addresses.py:feed_url, subscribe_links |
| R4-43.a | The address counts as public only when it starts with https:// and does not contain "localhost", "127.0.0.1" or "testserver"; otherwise the subscription page warns that Google cannot load it and points to the public address setting. | services/addresses.py:subscribe_links; templates/subscribe.html |
| R4-44 | The subscription page needs no sign-in; the stream name is the only protection. An unknown stream name answers 404. | routes/destinations.py:subscribe |
| R4-44.a | It is shown in the visitor's browser language, not the page owner's. | routes/destinations.py:subscribe |
| R4-44.b | It shows the feed's name, the five links (R4-43), step-by-step help, and, when at least one of the feed's calendars has been synced, "Last updated <date>, <time> · <n> events", where the time is the latest last-success time of the feed's calendars and n counts the visible (non-hidden) events of the feed. | routes/destinations.py:subscribe; templates/subscribe.html |
| R4-44.c | The page asks search engines not to index it. | templates/subscribe.html |
| R4-44.d | unsure: the page is still served when the feed is switched Off (only the .ics address is blocked). | routes/destinations.py:subscribe |
| R4-45 | On and Off: a feed can be switched Off and On; the choice and its chosen calendars are kept. History: `Destination "<name>" switched Off` or `... On` (undoable). | routes/destinations.py:power_destination |
| R4-45.a | While Off, the feed address answers "unavailable" (HTTP 503, "This calendar feed is switched off.", Retry-After 3600 seconds) so subscribers' applications keep their last copy; an unknown stream name still answers 404. | routes/destinations.py:calendar |
| R4-46 | The feed address serves a calendar of the feed's events: those of its chosen calendars that are not switched Off, hidden ones left out, whose day span overlaps the feed's Start and End days inclusive, sorted by start time. | services/google_sync.py:dest_events; calendars/feed.py:build_feed |
| R4-46.a | The calendar name is the feed's name; the color is the feed's own color, else, when the feed has exactly one calendar, that calendar's color, else none. | routes/destinations.py:calendar |
| R4-47 | Conditional reads: the answer carries an entity tag (the first 32 hexadecimal digits of the SHA-256 of the body, in double quotes) and "Cache-Control: no-cache". When the request's If-None-Match lists (comma-separated, trimmed) that exact tag, the answer is 304 with no body and the same headers. | routes/destinations.py:calendar |
| R4-47.a | unsure: every calendar built carries a new DTSTAMP (the current time), so the tag changes on every request and a 304 is only possible if the clock second and content are identical; the intent is that an unchanged feed answers 304. | routes/destinations.py:calendar; calendars/feed.py:build_feed |
| R4-48 | Published calendar format: version 2.0, product id "-//calendar_stream//EN"; calendar properties name (X-WR-CALNAME and NAME), time zone (X-WR-TIMEZONE, the display time zone), refresh interval and published TTL of 1 hour (PT1H), and, when a color is given, X-APPLE-CALENDAR-COLOR in upper case. The content type is "text/calendar; charset=utf-8". | calendars/feed.py:build_feed, _calendar_props; routes/destinations.py:calendar |
| R4-48.a | Each event has its identifier (UID), a DTSTAMP of the current time in UTC, TRANSP TRANSPARENT when free, SUMMARY, LOCATION when not empty, and DESCRIPTION when not empty. | calendars/feed.py:build_feed, _write_fields |
| R4-48.b | Timed events are written with start and end in UTC (so the file is valid whatever zones the source defined); all-day events are written as dates, the end being the exclusive end day. | calendars/feed.py:_write_times |
| R4-48.c | An event with an online meeting link has it as its URL and as the first line of its DESCRIPTION, followed by a blank line and the notes. | calendars/feed.py:_write_fields, notes_with_meeting |
| R4-48.d | Each event has a marker property X-CALENDAR-STREAM: "added" (added on the page), "rule" (made by a rule), "edited" (a source event changed on the page) or "source". | calendars/feed.py:build_feed |
| R4-48.e | Reminders: each reminder of an event (minutes before the start; duplicates removed; digits only; earliest-to-latest order, largest first) is written as a DISPLAY alarm whose description is the event's title and whose trigger is that many minutes before the start. | calendars/feed.py:_write_alarms; calendars/event.py:alarm_minutes |
| R4-49 | Last read: each fetch of a feed address (including those answered 304, not including the 503 or 404 answers) is noted as "Google" when the requester's identification contains "google" (any case), else "other". | routes/destinations.py:note_feed_read |
| R4-49.a | The time of the last read of each kind is saved at most once per minute (a fetch within 1 minute of the saved time writes nothing). | routes/destinations.py:note_feed_read |
| R4-49.b | The feed's status chip shows "Read by Google" (good) when it was read by Google, else "Not read yet" (in progress); the line under the title shows "Last read by Google <when>", else "Last read <when>" for another reader, else is empty. | templates/index/feeds.html; routes/page.py:feed_reads |
| R4-49.c | Reads belong to the feed; removing the feed deletes them. | routes/destinations.py:remove_destination |

## 5. Source status, Sync Now, schedule, Off, ordering and colors

| ID | Statement | Evidence |
|---|---|---|
| R4-50 | Each source has a status, shown as a chip with a label: ok "Healthy" (good colour), running "Syncing…", starting "Starting", setup "Setup needed", paused "Paused" (these four in the in-progress colour), auth_failed "Sign-in rejected", blocked "Blocked", error "Error" (these three in the warning colour), internal "Internal error" (the bad colour). A status not in this list is shown as its own name in the warning colour. | templates/index.html; templates/index/sources.html |
| R4-50.a | A source's status, message, last attempt, last success, last change, last sign-in time and result, rejected-sign-in count, event count and last detail are saved and restored after a restart; a status "running" restored from a stopped app becomes "starting". | services/state.py:State.save, load |
| R4-50.b | The line under the title says "Last synced <when>" when the status is ok or running and a success is recorded; "Sync failed <when>" (bad text colour) when there was an attempt but the status is otherwise; the status message when there is nothing yet; empty for a local calendar. <when> is the last success time (ok, running) or the last attempt time. | routes/page.py:source_view; templates/index/sources.html |
| R4-50.c | The right-hand line says "Next check @ <when>" unless the status is paused or setup; for paused it says "Automatic checks paused"; otherwise empty. | templates/index/sources.html |
| R4-50.d | A source's section on the page opens by itself when its status is not ok, running or starting, or when CCS+ has no credentials. | routes/page.py:source_view |
| R4-50.e | The machine-readable status lists for each source: id, name, type, status, message, running, last attempt, last success, last change, next run (ISO times or null) and event count; the top-level fields are CCS+'s (or the first source's). | routes/status.py:api_status |
| R4-51 | Sync Now downloads one source immediately (manual run), even while automatic checks are paused. It does nothing if that source is already downloading. | routes/sources.py:run_now; services/source_jobs.py:run_once |
| R4-51.a | Sync Now waits about 0.5 seconds, then answers whether the source is still running; the page follows the source's status until it ends and then updates in place. | routes/sources.py:run_now |
| R4-51.b | An unknown source is refused with "That calendar source doesn't exist (any more)." | routes/sources.py:run_now; services/route_helpers.py:_sid |
| R4-51.c | A local calendar has no Sync Now; a source with no configured sign-in (CCS+) has it disabled (R4-12). | templates/index/sources.html |
| R4-52 | Schedule: each non-local source is checked once when started (at app start or when added) and then every interval; the next check is the end of the interval after the previous check ended. | services/source_jobs.py:loop, start_source |
| R4-52.a | If a scheduled check fails unexpectedly (for example the database is unavailable) the next check is in 5 minutes. | services/source_jobs.py:loop |
| R4-52.b | A source's interval is in whole minutes, 15 to 1,440 inclusive; the default is 60 for a link source and the CCS+ default (R4-13) for CCS+. A saved value outside the range counts as the default. | services/source_jobs.py:interval_minutes; main.py:MIN_INTERVAL, MAX_INTERVAL |
| R4-52.c | A value that is not a whole number is refused with "Enter a number of minutes."; a number out of range with "Choose between 15 and 1440 minutes." | routes/sources.py:set_interval |
| R4-52.d | For CCS+ a value equal to the default removes the saved value; otherwise it is saved. | routes/sources.py:set_interval |
| R4-52.e | Saving a new interval sets the next check to the later of now and (last attempt + new interval), wakes the schedule, and writes History "Checks every <n> min from now on". | routes/sources.py:set_interval |
| R4-52.f | The field offers whole numbers in steps of 5 minutes, from 15 to 1,440. | templates/index/sources.html |
| R4-52.g | Scheduled runs of a link source are never paused (only CCS+ pauses, R4-11). | services/source_jobs.py:run_feed |
| R4-53 | Turning a source Off: the On | Off switch marks the calendar unavailable; its events leave every feed (which keep it selected, shown greyed, so On restores it). History "Calendar <name> switched Off" or "... switched On" (undoable). Any value other than "1" means Off. | routes/sources.py:power_source; services/google_sync.py:dest_events |
| R4-53.a | A source switched Off keeps being downloaded on its schedule (unsure: the code does not stop its checks). | routes/sources.py:power_source; services/source_jobs.py |
| R4-53.b | When Off or On changes a calendar that is chosen in a Google destination, a full Google sync is requested. | routes/sources.py:power_source |
| R4-54 | The order of the calendars is changed by moving one above or below another (drag or up/down arrows); the new order is saved only if it differs; an unknown calendar is refused with "That isn't there (any more)." | routes/sources.py:move_source; item_order.py:_moved |
| R4-55 | The name and note of a calendar are edited in its header; a blank name returns to the default (R4-21; CCS+: the CALENDAR_NAME setting, default "United CCS Schedule"). A name equal to that CCS+ default is not stored. | routes/sources.py:set_tags, _source_name_color; config.py |
| R4-55.a | The note is cut to 120 characters after collapsing whitespace; an empty note stays empty (it is not replaced by the kind of calendar); with no note ever set, the note shown is a description of the kind of calendar (preset). | routes/sources.py:_source_name_color; routes/page.py:source_view |
| R4-55.b | Saving writes History "<name> saved: name "<name>", color <#rrggbb> | default color" (undoable) and rebuilds the calendar's feed. | routes/sources.py:set_tags |
| R4-56 | The color of a calendar is #rrggbb (6 hexadecimal digits, any case, stored and used lower-case); anything else is refused with "Choose the color with the color picker." A "default color" choice deletes the saved color. | routes/sources.py:_source_name_color; main.py:COLOR_RE |
| R4-56.a | A calendar with no color is shown with the accent #3f51b5 and publishes no color. | templates/index/sources.html; calendars/feed.py:_calendar_props |
| R4-56.b | An event's color is its own color, else the color its rules give it, else its calendar's color, else none. | services/google_sync.py:event_colorer |
| R4-57 | Every change of a source's name, color, rules or events rebuilds that source's published events from its last downloaded copy, without downloading again. | services/publishing.py:rebuild, publish |
| R4-57.a | Building a source's events from its last copy applies, in order: the rules' time changes, the edits and added events of that calendar, the events its rules make, its rules' colors and emoji, then the reminders; hidden events are counted out of the calendar's event count. | services/publishing.py:publish |
