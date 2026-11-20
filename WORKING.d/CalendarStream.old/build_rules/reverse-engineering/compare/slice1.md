# Slice 1 comparison (B = reverse/slice1.md, A = account.md, settings.md, shell.md + common/theme/deployment pointers)

## GAP (B ID | behavior and values | A file)
R1-01.d | /welcome and /login show the version "vX.Y.Z" beside the name CalendarStream (also R1-62.c: version only in footer on main page) | shell.md
R1-02.b | A new setup code is generated on every start that finds no login; a new start replaces the earlier code; it lives in memory only, valid for that run | account.md (ACC-01)
R1-03.c | Welcome page title "Welcome · CalendarStream", intro "Welcome! First, create the login for this status page.", button "Create login" | account.md
R1-05.b | A correct setup code with an invalid user name/password is not counted as a failed attempt | account.md (ACC-06.b)
R1-05.c | Setup code is checked before user name/password; invalid name/password reported only when the code was right | account.md (ACC-01)
R1-07.c | Order of checks: user name, then password rules, then password match | account.md (ACC-01.d)
R1-07.f | Every password box has Show/Hide password button; box hidden again when the form is sent | common.md (UIC)
R1-08.a | Activity log (info) "Status-page login created for <user>" | account.md / history.md
R1-08.b | Form token renewed after the login is created (A has renewal only on change, ACC-03.c); R1-15.b same | account.md (ACC-03.c)
R1-08.c | Creating the login also marks the browser as known (cs_known) | account.md (ACC-07.c)
R1-09 | Sign-in page: fields User name (max 64, required) and Password, button "Sign in", title "Sign in · CalendarStream", focus on User name (Password when name kept after failure) | account.md
R1-09.a | Wrong sign-in re-shows form (400), keeps typed user name, message "That user name or password isn't right." never says which was wrong | account.md (ACC-02.b)
R1-09.d | Signed-in visitor opening /login is redirected to the next path | account.md (ACC-02)
R1-10.b | Unauthenticated non-page request (not GET/HTML, background) gets 401 "Sign in again (reload the page)." | account.md (ACC-02.a)
R1-11.b | Session cookie cs_session: not script-readable, SameSite lax, Secure when request is https (direct or via proxy) | account.md (ACC-02.d)
R1-11.c | Session signing key: random 32 bytes kept in the database, regenerated if missing or shorter than 64 hex chars | account.md (ACC-02.d)
R1-12 | Known-browser cookie cs_known valid 400 days from last successful sign-in, renewed each sign-in; also set by login creation and unlock link (A has no lifetime; not in DEF-01) | account.md (ACC-07.c) + common.md DEF-01
R1-13 | Basic credentials: correct pair counts as success, wrong pair as one failed attempt, none counts nothing (A only says Basic supported for status API) | account.md (ACC-02.c, ACC-06)
R1-18 | Old installs: page login imported once from pre-0.1.3 secret files (user admin default), info log, password not rule-checked (likely obsolete in the port) | deployment.md (DEP-05)
R1-20.b | Installer lower-cases subdomain and names, allows only letters, digits, . _ - | deployment.md (DEP-02.a)
R1-21.a | Defaults: port 8080, TZ America/Chicago, IMAGE_TAG latest, restart unless-stopped | deployment.md (DEP-01.d / DEP-05.b)
R1-22.a | The failed attempt that reaches the limit is itself answered 429 "Too many failed attempts. Try again later." | account.md (ACC-06.a)
R1-22.c | At lock start the counter resets to 0 and lock-until = now+15 min; later attempts are refused without counting and do not extend the lock | account.md (ACC-06.a/.d)
R1-22.d | History warning "Status page locked for <address> after 5 failed logins" ("setup codes" for setup code failures) | account.md / history.md (A has only the global-block warning, ACC-08.a)
R1-23.h | First-visit form lockout check does not use the known-browser exemption | account.md (ACC-07.d)
R1-25.c | Using an unlock link records info "Unlock link used from <address>: that browser can sign in again" | account.md (ACC-08.b)
R1-26 | Wrong current password in Settings counts as a failed attempt for the requester's address (also R1-26.a Basic) and gives field error "The current password isn't right." | account.md (ACC-03.a / ACC-06)
R1-26.a | Wrong Basic credentials count as a failure; none do not | account.md (ACC-06)
R1-31.d | Empty user name field in Settings keeps the current user name | account.md (ACC-03)
R1-32 | Domains has a "This page" button that fills the address the page is opened at; + only on last row; "Not set yet." text | settings.md (SET-04)
R1-32.e | After changing the main address while Google API sync is configured, page opens Settings with a prompt to fix Google's redirect address | settings.md (SET-04.d) / connections
R1-32.f | Legacy posts /settings/public-url and /settings/public-extra (extra logs info "More public addresses: ...") | settings.md (SET-04; likely drop)
R1-33.c | A saved public address that no longer normalizes is treated as not set | settings.md (SET-04)
R1-34.a | Admin email used in Google setup instructions as support contact and test user ("my Gmail address" when none); re-validated on every read; max 254 chars | settings.md (SET-06.d)
R1-35.b | Time zone picker lists "Common" group (14 named zones in fixed order), then "All time zones" (region/city only, excluding Etc/ SystemV/ posix/ right/), default marked ★ | calendar.md (CAL-02)
R1-35.c | Zone must be UTC or in the list else 400 "Unknown time zone."; choosing the default or empty clears the stored choice; invalid stored falls back to default | calendar.md / settings.md (SET-02)
R1-36.e | /brand/logo and /brand/favicon served without sign-in, private cache 1 day, CSP forbidding running anything, 404 when unset, fingerprint in link | settings.md (SET-06.e/.f)
R1-36.j | Successful look save records info "Look changed (logo, favicon, grips, animation)" | history.md / settings.md
R1-40.a | Newest version read from text files VERSION (beta) / STABLE (stable) in the project's GitHub repo; client name "CalendarStream/<version>" only | settings.md (SET-05)
R1-41 | Check timeout 15 s, follows redirects; success only on HTTP 200 with a valid version (stable channel must be stable) | settings.md (SET-05.d)
R1-43 | Background checker waits 30 s after start; between rounds waits until next due but at least 60 s and at most 1 h; round failure logged as warning, never stops | settings.md (SET-05.a)
R1-44.c | Page header shows "(v<new> is available)" linking to release notes, plus Update now button | settings.md (SET-05) / shell.md
R1-45 | Auto-update is off by default; disabled unless updater usable (or already on); logs "Auto-update on/off" | settings.md (SET-05.h) + common.md DEF-01
R1-47.a | Update progress polling: every 2 s, gives up after 15 minutes with failure; status polled once a minute while page shown; reload 0.8 s if restart never observed | settings.md (SET-05.n)
R1-48.a | App probes the updater at start and every 5 minutes (health answers 200 within 3 s) | settings.md (SET-05.h) / deployment.md
R1-60.e | Sign-in and first-visit pages follow the saved theme | shell.md (SHL-03)
R1-62 | Browser tab titles: "CalendarStream", "Sign in · CalendarStream", "Welcome · CalendarStream" | shell.md (SHL-01)
R1-62.b | Logo mark is 39 by 36 px | theme.md / shell.md
R1-62.c | Version not in title; shown in footer; on sign-in/first-visit pages as "vX.Y.Z" | shell.md (SHL-01.a)
R1-64 | Default icons: 32 px favicon, 192 px icon, Apple touch icon, each versioned in the URL; custom favicon replaces all | shell.md (SHL-01.b)

## DIFFERENT (B ID | A ID | A says | B says)
R1-06 | ACC-01.d | refuses a username containing a space | valid = 1-64 chars after trimming, no whitespace, no colon
R1-07 | ACC-04.a, DEF-01 | min length 11 default; per-class minimums (capitals, lowercase, numbers, special) all 1 by default, configurable in Site Admin | fixed: 12+ chars, capital, digit, symbol (non A-Z a-z 0-9 whitespace), no char 3+ times in a row; no lowercase rule; not configurable
R1-07.a | ACC-04.b | hint names unmet requirements (wording not fixed) | "The password needs: " + unmet rules with fixed texts, joined by "; "
R1-10 | ACC-02.f | not followed if starts with //, has backslash, tab, line break or other control character | followed only if starts with "/", not "//", no backslash, no character code 32 or lower (spaces too)
R1-23 | ACC-07.a, DEF-01 | global block at 25 failures within 15 minutes | 50 failed attempts within 15 minutes (also R1-24 trigger "exactly 50")
R1-23.c | ACC-07.b (backlog), DEF-01 | trusted during global block: 192.168.0.0/16, 10.10.0.0/16, loopback; judged from trusted-proxy address | all local nets 10/8, 172.16/12, 192.168/16, 127/8, 169.254/16, ::1, fc00::/7, fe80::/10; proxy headers not consulted
R1-23.d | ACC-07.b | CalendarStream's own public domain not blocked | not blocked when the address is one the public domains currently resolve to (lookup at most every 10 min)
R1-24 | ACC-08.a/.d | History warning with the unlock link, link valid 24 h (DEF-01) | link written to container log; "within an hour"
R1-25.a | ACC-08.d, DEF-01 | unlock link valid 24 hours, single use | valid 1 hour, single use
R1-30 | SET-06.b | Backup and Restore exists in Site Admin (backlog) | no backup or restore feature exists
R1-33.a | SET-04.e | invalid: FTP, query, embedded credentials, not a URL | also invalid: non-http(s) scheme, no host, params, fragment, whitespace, >300 chars, invalid port, single slash after scheme
R1-35.a | CAL-02.a, SET-02.a | calendar zone picker is a temporary view choice kept on the device | stored for all browsers (server), changes only the page calendar
R1-36 | SET-03, SET-06.e-g, UIC-37 | logo and favicon are Site Admin settings set with the image editor; Theme holds animation, grips, notation, long-press | Theme block holds Logo and Favicon file choosers, "Use CalendarStream's ..." ticks, grips, animation, one Save
R1-60 | SET-01.a, SHL-03.a | theme is a User (device) setting | theme stored on server, same for every browser
R1-61.c | SHL-02.d | language kept on the device | language stored on server, shared by all browsers
R1-61.e | TIM-10, SET-03.a | time format user setting on device; default 12-hour in US zone else 24-hour; four notation choices | clock 12/24/Automatic(by language) stored on server
R1-62.a | CAL-06.a, SHL-01.d | Full page sits in the calendar's right zone; title bar has logo mark and title | Full page button is in the page header between theme menu and Settings

(Also noted, not a row: B's Settings order Login, Domains, Updates, Theme, Google vs A SET-01.d Updates, Login & password, Domains, Theme last.)

## A-ONLY (A ID | one phrase)
ACC-04.d | requirements apply only on create/change, never sign anyone out
ACC-05.b | CCS+/Google credentials stored encrypted with key from database password
ACC-05.c | a secret is never written to a log
ACC-05.d | Show secrets switch in History
ACC-06.c | concurrent failures all counted without internal errors
ACC-06.d | block not removed early by failures from other addresses
SET-01.c | Settings pop-up follows shared dialog rules, Cancel | Save
SET-02.a | Time Zones setting: follow system or fixed zone
SET-02.b | Search results count setting
SET-03.a | time notation choice
SET-03.b | Long-press time
SET-04.g | warning when page opened through a non-public host
SET-04.j | removing public-address rows leaves one main field
SET-06.a | Default time zone in Site Admin
SET-06.b | Backup and Restore
SET-06.c | Password requirements setting
SET-07.a | pick another release by hand
SET-07.b | alternate port written to .env
SET-07.c | update stream Stable/Beta/by hand
SHL-01.c | logo files free of artifacts
SHL-02.f | inserted values in translations escaped
SHL-02.g | subscription page / Google setup-error guide follow browser language
SHL-02.h | localized form-error page with back link
SHL-05.a | no external resource providers (Google Fonts)
SHL-05.d | API requests keep JSON errors

## Counts
B rows: covered 121, different 17, gap 50 (total 188); A rows only-in-A: 25
