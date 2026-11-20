# Slice 5 comparison (Google): B = reverse/slice5.md, A = requirements/connections.d/google_*.md, plugins*.md
A files: GO = connections.d/google_one_way.md, GT = google_two_way.md, PG = plugins.d/google_api.md. Note: DEF-01 (common.md) lacks the values A refers to for consent expiry (B 15 min), invitation expiry (B 7 days), instant-update lifetime (B 7 days).

## GAP
R5-01.a | client ID = 10-200 chars [A-Za-z0-9_.-] then exactly ".apps.googleusercontent.com", trimmed first | PG (PGAP-01.b)
R5-01.b | bad ID refused: "That doesn't look like a Google OAuth client ID (it ends in .apps.googleusercontent.com)." | PG
R5-01.c | secret trimmed; >200 chars or any whitespace refused "That doesn't look like a client secret." | PG
R5-01.d | blank secret with none saved refused "Enter the client secret too."; saved secret never shown again | PG
R5-01.e | undecryptable stored secret reads as blank, so client counts as not configured | PG
R5-01.f | client "configured" only when both ID and secret non-empty | PG
R5-01.g | saving a new client clears cached access token and the first account's shown error | PG
R5-01.h | History info line "Google OAuth client saved (<first 12 chars of ID before first period>...)" | PG
R5-02.d | client removal is the trash at the end of the credentials row and asks confirmation first | PG
R5-03.f | each check stores ok (yes/no/unknown), message, UTC time, callback address used, address-listed (yes/no/unknown) | PG
R5-03.g | all Google calls time out at 20 s total, 10 s connect | PG
R5-03.h | legacy 0.1.20 check "Google doesn't list ..." read as ok, redirect not ok (migration) | PG
R5-04.a | address check = the Connect request not followed: client_id, address, code, scopes, offline, forced consent, state "calendarstream-check", S256 | PG
R5-04.c | address check: "invalid_client/deleted_client/unauthorized_client" in answer = verdict unknown | PG
R5-04.d | address check: status 200/302/303 and location without "/signin/oauth/error" = listed | PG
R5-04.e | otherwise or unreachable = unknown; verdict saved with last check (ok and message kept) | PG
R5-05 | callback address = public address + "/google/callback", must be listed exactly | PG
R5-05.c | public host differs from page host (not localhost/127.0.0.1/IP) is reported as mismatch (typo guard) | PG
R5-06 | Connect = four ordered steps save, client, address, go in status boxes, stops at first failure naming the fix | PG (or CGOW-01)
R5-06.a | step save: typed ID differing / typed secret saved; not configured stops "Client ID and Client secret: from Google Cloud > Clients > CalendarStream..." | PG
R5-06.b | step client: not ok stops with "<message>: Google Cloud > Clients > CalendarStream > copy both again > Connect." and opens console.cloud.google.com/auth/clients; unknown offers retry | PG
R5-06.c | step address: unacceptable address stops "Settings > Public address: this page's https:// address > Save > Connect." | PG
R5-06.d | step address: not listed logs warn and stops "Address not on your client: ... + Add URI > <address> > Save > wait 5 min > Connect." with Copy and Open | PG
R5-06.e | step address passes on yes or unknown; "confirmed" only on yes | PG
R5-06.f | step go: info "Google Calendar API Sync is set up..." plus one line per unsynced Google destination (warn unless "not synced yet"); starts no sign-in | PG
R5-06.g | unknown step name refused 400 "Unknown step." | PG
R5-06.h | step status words "Saving...", "Checking...", "Checking address...", "Healthy" | PG
R5-05.a | callback acceptable only if https, host not bare IP and not .local, or host localhost/127.0.0.1 any scheme (A PGAP-01.h says only "unsupported public IP/local-host") | PG
R5-08.a | with API off, adding a destination / invite / Connect me refused 400 "Needs Google Calendar API Sync, which your admin turns on in Settings." | PG/GO
R5-09 | one client serves the whole install, up to 100 people while unverified; guide ends with Google error list and fixes | PG
R5-10.b | accounts in use = first account plus each destination's account, no duplicates, first first | GO
R5-10.c | destination from before account slots (account "") is on the first account | GO (legacy, may be deliberate)
R5-10.d | per account stores refresh token, email, connected time, last sync/result/error, per-destination calendars; first account keeps old storage names | GO (partly PG)
R5-11.b | state 24 random bytes, verifier 48 random bytes url-safe, verifier encrypted in DB | PG (PGAP-01.f is generic)
R5-11.c | sign-in valid 15 minutes (value missing in DEF-01); expired dropped first, oldest removed to make room | common.md DEF-01 / GO CGOW-01.c
R5-12 | Connect refused 400 "Save the Google OAuth client ID and secret first." or "Set the public address ... first." | GO
R5-13.a | unknown/expired/used state: "This Google sign-in has expired or was already used. Try Connect again." | GO
R5-13.b | code exchanged at oauth2.googleapis.com/token with authorization_code, same callback, PKCE verifier, client ID+secret | GO
R5-13.d | no refresh token returned fails "Google didn't send a lasting sign-in (refresh token). Try Connect again." | GO
R5-13.f | new email differs from stored email clears the account's stored details/calendars | GO
R5-13.g | success: token encrypted, client check saved ok+listed, access token cached to expiry-60 s (default 3600) | GO
R5-13.j | History info "Google Calendar connected as <email or 'your account'>" plus per destination "calendar created/found again" | GO
R5-13.l | failed sign-in stored as account last error and logged at error "Google: <message>" | GO
R5-13.n | callback needs page login except when state belongs to an invitation sign-in | GO
R5-14 | token request: transport failure "Couldn't reach Google (<type>)." transient; good only with HTTP 200 and an access token | PG
R5-14.b | token invalid_client/unauthorized_client text "Google rejected the OAuth client: check the client ID and secret..." | PG
R5-14.c | token redirect_uri_mismatch text "Google says the redirect URI isn't one of the client's authorised redirect URIs." | PG
R5-14.d | other token error "Google sign-in failed: <error or HTTP status>." | PG
R5-14.f | access token reused until 60 s before expiry; refresh via refresh_token grant; concurrent requests share one refresh | PG
R5-15.a | invite only for a Google destination, needs API on; token 24 random bytes, works once, lasts 7 days (value missing in DEF-01); one live invite per destination, new replaces old | GO
R5-15.b | History info "Google, <name>: invite made (works once, for 7 days)" / "invite withdrawn" | GO
R5-15.d | invite token 20-64 chars [A-Za-z0-9_-], live, destination exists and its account still equals invite's origin account, else 404 "This invite has been used, has expired, or was withdrawn. Ask for a new one." | GO
R5-15.e | invite page shows destination name and "Continue with Google"; Continue needs HMAC page token, mismatch 400 "This page has expired. Open the invite link again." | GO
R5-15.f | Continue fails 400 "CalendarStream can't sign anyone in to Google right now..." when API off or address unacceptable | GO
R5-15.g | invite sign-in state remembered 15 min, max 50 (oldest dropped); return needs no page login | GO
R5-15.h | invite return: cancel/error page "Google sign-in was cancelled. Open the invite link again to try once more." 400; success logs "Google, <name>: <email> connected through an invite", done page, full sync | GO
R5-16.a | "Back on the first account" sets destination to first account, logs it, requests full sync | GO
R5-17.a | disconnecting a destination on the first account gives it a new unconnected account; first account and others stay signed in | GO
R5-17.b | disconnect under sync lock: stop its notifications, disconnect without deleting calendar; revoke grant only when no other connected account shares the same Gmail (case-insensitive) | GO (A CGOW-01.k only says same-account)
R5-17.c | History "Google, <name>: <email> disconnected; <notes>", warn if notes else info | GO
R5-17.d | revoke posts refresh token to oauth2.googleapis.com/revoke; 200 and 400 fine; else note to remove at myaccount.google.com/permissions | GO
R5-17.g | Settings Disconnect for first account stops all channels, optional "Also delete these calendars in Google", wipes per-event state when deleting, History line | GO
R5-17.h | unconnected Google destination shows status "Invited" (invite exists) or "Not connected" | GO
R5-20.b | calendar fetch 404/410 = gone, make new; refusal containing "403" (other client) also new; other errors fail | GO
R5-20.g | stored calendar differs from last synced: drop all per-event state and full sync | GO
R5-21 | calendar color tried in order: RGB (backgroundColor, foreground #ffffff, colorRgbFormat), nearest of 24 colorIds, full replace of list entry; last accepted way first | GO
R5-21.a | the 24 calendar colors id->hex table and nearest = least squared RGB difference | GO
R5-21.b | full-replace way starts from Google's copy minus colorId/etag/kind, selected true hidden false, PUT colorRgbFormat true | GO
R5-21.c | only a Google refusal moves to next way; unreachable/busy/revoked stop at once; errors joined with "; " | GO
R5-21.f | History info "<who>: color set in Google Calendar" naming the way used and "; that way is kept" | GO
R5-22.d | switched-off destination skipped by every sync | GO
R5-23 | Google event id = lower base32hex of SHA-256 of UID, no padding; status confirmed; private props calendarstream=1 and uid (first 900 chars) | GO
R5-23.c | reminders: useDefault false, popup overrides earliest first, at most 5 | GO (A CGOW-03.d silent on max 5)
R5-23.f | the 11 Google event colors id/name/hex table, ties to first | GO (A defers to UIC-20)
R5-24.a | per-event SHA-256 of sorted-key JSON body stored with end, Google id, Google updated time | GO
R5-24.b | result classes: added, updated (content changed), repaired (copy deleted/changed by hand), unchanged | GO
R5-24.c | known event replaced at fixed id (404/410 falls back to insert); new inserted (409 falls back to replace, reviving deleted); never duplicates | GO
R5-24.f | at most 1500 Google writes per destination per sync, rest next sync, "(more at the next sync)" (A CGOW-04.h has no number) | GO
R5-24.g | summary "<n> added, <n> updated, <n> removed, <n> repaired" omitting zeros, "calendar renamed", "no changes" | GO
R5-24.h | History info "<who>: <summary>; notes" only when changed or notes | GO
R5-24.i | completed sync stores destination last sync time+count and account last sync/result, clears last error | GO
R5-24.j | legacy "held" deleted events skipped (pre beta.15) | GO (legacy)
R5-25.a | Google copy counts as changed when missing, cancelled, or updated time differs from last write (30 s tolerance when no stored time) | GO
R5-26 | Google job runs at start (full), on change wake-up, and at least every 24 h with full check | GO
R5-26.a | after wake-up wait 2 s to settle bursts | GO
R5-26.b | wait for next run never shorter than 60 s | GO
R5-26.d | unexpected exceptions logged and treated as failed run; loop continues | GO
R5-26.e | one sync/disconnect at a time (lock); run covers all destinations account by account; nothing when no client or no destinations | GO
R5-29.a | pull reads nothing when no calendar, calendar differs from last synced, 404/410, or 403 (other client); other errors fail sync | GT
R5-29.b | fields read: title 200 chars, all-day, start/end, location 200, notes (strip "Synced by CalendarStream" and leading meeting-link line, 4000 chars), updated | GT
R5-31 | Google deletions logged info "Deleted in Google Calendar: " up to 5 entries then " ..." each with Restore in History | GT
R5-31.a | events deleted in Google while a Restore is pending are not treated as deletions | GT
R5-32 | event added in Google: copied to first local calendar (uid cs-<16 hex>@calendar_stream, no color), deleted from Google, rewritten by next sync; non-repeating only | GT
R5-32.a | repeating event or destination with no local calendar left in Google and said once; last 500 remembered | GT
R5-33 | Google changes applied logged info "<who>: <line>", rules/sources rebuilt for touched sources, state saved | GT
R5-34 | sync error handling: failure text logged at error only if different from account's previous last error; unexpected "Google sync failed: <type>: <message>" | GO
R5-35 | Google call results: 200/201 body, 204 empty, 404/410 nothing when missing-ok | PG
R5-35.a | (as R5-35) status handling per call | PG
R5-35.b | API base https://www.googleapis.com/calendar/v3, calendar ids percent-encoded fully | PG
R5-36 | status API reports Google connected, running, pending, last sync failed | GO (or status area)
R5-36.a | Report-a-problem data includes Google connected; client ID, tokens, secrets, emails redacted | PG/GO
R5-36.b | destination status: Not connected/Invited; "Sync problem" (bad tone if "Google sync failed", else warn); Connected; Starting | GO
R5-40.b | channel = POST events/watch: id 16 random bytes hex, web_hook, address <public>/google/notify, token 32 random bytes, ttl 604800 s (7 days; DEF-01 lacks it) | GO
R5-40.c | stored channel: id, resourceId, encrypted token, address, calendar, expiry (Google ms else now+7 d), time tried, last notice kept | GO
R5-40.a | notify address empty when host localhost/127.0.0.1/.local (A only says HTTPS needed) | GO
R5-41.b | channels checked after each destination's sync, only if account connected and notify address exists | GO
R5-41.c | destination with no calendar records attempt but starts nothing | GO
R5-42 | start failure logged warn once "Google: instant updates aren't available (<error>); changes made in Google are checked daily instead" (not repeated when same error) | GO
R5-42.a | first success logs info "Google: instant updates turned on (changes made in Google are checked within seconds)" | GO
R5-43 | /google/notify no login; accepted when x-goog-channel-id and x-goog-channel-token match stored channel, constant-time compare, undecryptable token never matches | GO
R5-45 | page shows instant updates off ("needs a public https:// address"), off with stored error, on with last notice time, or "starts with the next sync" | GO
R5-45.a | status line "Next push instantaneous" / "Instant updates off" with tooltips | GO
R5-46 | notifications need valid certificate and proxy letting Google POST /google/notify without login | GO
R5-47 | destination re-key (migration from per-source calendars) moves calendar details, event state, channel | GO (migration)
R5-50.c | all 5 attempts retried: "Google Calendar is busy; CalendarStream will try again later." transient | PG
R5-50.d | 401: drop cached token and retry at once unless token was issued in last 60 s | PG (A PGAP-02.a covers retry once only)
R5-50.e | HTTP 409 raises Conflict at once, no retry | PG
R5-50.f | other failure text "Google Calendar refused <METHOD> <path>: HTTP <status> <reason>, "<message>"", message parts joined " . " max 300 chars, status carried, first 2000 chars of answer logged | PG (PGAP-02.d is generic)
R5-50.g | reason = first "reason" in Google's error list | PG
R5-51 | failures classified into kinds: token expired, consent revoked, rate limit, transient, permission, calendar missing, event invalid, conflict, unknown; first match wins | PG
R5-51.a | revoked->consent revoked; missing->calendar missing; conflict->conflict; non-Google error->unknown | PG
R5-51.b | status map: 401 token expired; 403 or "rejected the OAuth client" permission; 429 rate limit; 404/410 calendar missing; 409 conflict; 5xx/transient transient; 400 event invalid; else unknown | PG
R5-54 | per-account health fields: state (healthy/degraded/recovering/reauth required/paused), kind, reason, attempts, next retry (epoch s), last error (300 chars) and time | PG/GO
R5-54.a | on failure attempts +1 only when decision is retry; next retry = now + wait when retrying and wait non-zero | PG
R5-54.d | recovering/paused/reauth required set only by the decisions; health is per account | PG
R5-55.a | no second try inside a failed sync: call-level retries already happened | PG
R5-57 | user messages per condition (revoked, unreachable "Couldn't reach Google Calendar (<type>).", busy, refusal) | PG
R5-59 | every Google call recorded unredacted in memory for Beta Google traffic view (time, account, method, URL, headers, body, status, response first 20000 chars, ms) | new Beta feature file (not in slice A)
R5-59.a | /google/traffic returns recent entries newest first; /google/traffic/clear empties | same
R5-61 | History gets a line once per new problem, not at every retry | PG/GO
R5-18 | (Fix button) destination error containing "sign-in" shows status "Sign-in failed" with "Fix" restarting sign-in (A CGOW-01.l only "offers a way to reconnect") | GO

## DIFFERENT
R5-08 | PGAP-01.a | connecting unavailable until client set up and accepted | Google features on when client configured and last check not "not ok"; unknown/never-checked counts as on
R5-20 | CGOW-02.a | calendar uses the calendar's configured time zone | calendar time zone = the install's time zone; fixed description text "Kept up to date by CalendarStream..."
R5-20.f | CGOW-04.e (open question) | recreated with new mapping, interaction with paused recovery unresolved | missing calendar mid-sync: new calendar made, all event state dropped, everything rewritten, note shown (policy R5-52.e says "paused, not recreated without asking")
R5-22.b | CGOW-02.j | initial window starts first day of current month | window starts at destination's Start date, or 2000-01-01 when none; only events ending after window start written
R5-23.a | CGOW-03.a (backlog) | send each event's recorded time zone; all-day sent for stored zone | timed events always sent with the install's time zone name; all-day as date from stored text
R5-50.a | PGAP-02.b | one retry schedule: 5 s doubling to 15 min, 25% jitter, 5 attempts | call level: waits 1,2,4,8 s, no jitter, 5 attempts; separate recovery backoff 5 s x 2^n, jitter, cap 900 s (R5-53)
R5-50.b | PGAP-02.b | 429/5xx/rate limit retried with the DEF-01 schedule | same condition retried at 1,2,4,8 s for attempts 0-3
R5-55.b | PGAP-02.a | reauthorization required without automatic retry | reauth-required and paused states set no next-retry, so later scheduled syncs still try
R5-26.c | PGAP-02.a | after exhausted failure, next try at next scheduled sync | after failed sync next attempt within 15 minutes

## A-ONLY
CGOW-01.s | repeated setup submission creates no duplicate/orphan connections
CGOW-01.l | unsynced connection does not claim Last synced
CGOW-02.h | concurrent consent and sync reuse one calendar mapping (B 13.i only locks)
CGOW-03.g | color request that never reached Google is not remembered as refused (B 21.e partly)
CGOW-04.d | window advance/back-extension rules (open question)
CGOW-04.j | measurable latency target (open question)
CGOW-06.g | long saved health error shown in full or clipped per UIC-14
PGAP-01.h | callback derived from request host when no public address
PGAP-01.m | notice when domain/public address changes with client set up (F56)
PGAP-01.i | changing public address invalidates stale address feedback (B 05.b near)
PGAP-02.d | Google's explanation preserved in diagnostic feedback (B 50.f supports)
PLG-01 | plugin set up once, shared by all connections
CGTW-01.f / CGOW-04.k | one-way/two-way as source/feed definitions (structural; B 28 supports)
Counts: B covered 97, different 9, gap 131 (of 237); A-only 13
