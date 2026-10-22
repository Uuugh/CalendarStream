# Changelog

Versions follow [semver](https://semver.org): `x.y.z-beta.N` for betas (from 0.2.7-beta.1) and
`x.y.z` for stable releases; versions before 0.2.7 are `0.y.z`. Planned: 0.2 more calendar sources
and destinations, 0.3 backups, 0.4 more users, 0.5 notifications, 0.6 theming. Every version is
tagged `v<version>`; the newest is also tagged `beta`. The last stable one (in the `STABLE` file) is
the `latest` image and the GitHub Release marked **Latest**; when a version is released, its betas'
entries are gathered under its heading. Each version lists what was **added**, **changed**,
**fixed** and **removed**. Labels refer to that beta's request list: F = feature request,
I = issue, # = review item, R = README; numbers start again with each beta.

**Stable (`latest`): 0.0.6 · Newest (`beta`): 0.2.7-beta.4**

## 0.2.7-beta.4 — 2026-10-22

### Fixed
- **I1** A source's header didn't fit on its two lines and overflowed. The last-download and
  check-interval lines now start at the same left edge, and switch to the short wording ("98 events
  @ 14:53", "Check every 15 min") whenever the long one wouldn't fit beside the title; this is
  measured on the page, so it also works in other languages.

### Changed
- **R1** README: every screenshot is shown in the light and the dark theme, side by side (and the
  add-event screenshot is new).

## 0.2.7-beta.3 — 2026-10-22

### Added
- **F1** Updates from the status page:
  - **F1.1** An optional updater container next to CalendarStream: Watchtower, with an HTTP "update
    now" endpoint protected by a secret token (`.secrets/UPDATER_TOKEN.txt`). It's reachable only
    inside the Docker network, never checks on its own, and only updates the CalendarStream
    container (not the database).
  - **F1.2** "(v… is available)" gets an **Update now** button that asks the updater to download
    the new image and restart. The button shows the progress like the ✓ Validated box does:
    **Update now** → **Downloading…** (with a moving bar; the updater doesn't report how far the
    download is) → **Restarting…** → gone once CalendarStream is running again, with the version at
    the top (and in the footer) showing the new one. If the updater refuses or isn't reachable, it
    says **✗ Update failed**, with the reason. Settings → Updates says whether the updater is
    running.
  - **F1.3** The installer asks whether to set it up (no by default; yes adds
    `COMPOSE_PROFILES=updater` to `.env`), and it works the same on Linux, macOS (Docker Desktop)
    and Windows (WSL).
  - **F1.4** The updater is [nicholas-fedor/watchtower](https://github.com/nicholas-fedor/watchtower),
    the maintained fork: the original containrrr/watchtower was archived in December 2025, and the
    fork releases every week or two (v1.23.2 on 2026-10-22).
- **R1** README: light and dark screenshots side by side (the calendar and a phone).

## 0.2.7-beta.2 — 2026-10-22

### Changed
- **F1** Settings:
  - **F1.1** Hard to see when opened: the Settings panel is now light blue (the blue of the Sync
    Now box), with each part on white.
- **F2** Calendar:
  - **F2.1** "Time Zone" before the time-zone menu; "TZ" when space is limited.
- **F3** Calendar Sources:
  - **F3.1** The last-download line no longer fit: when the box is narrow it shortens to
    "40 events @ 1:10pm (…)".
  - **F3.2** Likewise "Check for changes every 60 minutes" shortens to "Check every 60 min"; on a
    phone the status box sits beside the title.
  - **F3.3** "UID" is now "Username".
  - **F3.4** Every "✓ Validated" box is half as wide, in the same place; Save and Cancel share that
    width, and a failed check says "✗ Failed" (the reason shows under the boxes).
- **F4** Calendar Destinations:
  - **F4.1** Each destination's box, and the Google account's, has the same header as a source's
    (name, kind, its sources and dates, status) and folds the rest under **▸ Configure ◂**. The
    Google account opens by itself until it's connected; the others stay as you left them.
  - **F4.2** Add a destination: the Name's hint reads "How your calendar will be titled via stream"
    (left empty, it takes the first source's name).
- **F5** Rules:
  - **F5.1** The same section heading as Calendar Sources.
  - **F5.2** Renamed **Rule Templates**.
- **F6** Event Templates:
  - **F6.1** Its own section (it was a box inside Rules), with **+** in its heading.
  - **F6.2** Where Activity was: beside Rule Templates on a wide screen.
- **F7** Activity:
  - **F7.1** Renamed **Activities and Logs**.
  - **F7.2** Spans the full width.
- **F8** Layout:
  - **F8.1** Checked on a wide screen, a narrow one and a phone, with shorter words where needed
    (no sideways scrolling at any width).
  - **F8.2** Spacing: 10 px between sections, 5 px between the boxes in a section, 2 px between rows
    of fields.
- **R1** Fuller README screenshots: the calendar (light and dark), each section in use, the rule
  dialog, Settings and a phone (made-up demo schedule).

## 0.2.7-beta.1 — 2026-10-22

### Changed
- **F1** Version numbers follow [semver](https://semver.org): betas are `x.y.z-beta.N` (this is
  0.2.7-beta.1), and stable releases are `x.y.z` (every beta of 0.2.7 comes before 0.2.7 itself).
  - **F1.1** The full version shows at the top of the page (on its own line on phones) and in the
    footer, still linked to its release notes.
  - **F1.2** Check for updates: a beta install is offered newer betas and stable releases; a
    stable install only stable releases. An exact beta version in `IMAGE_TAG` (e.g.
    `0.2.7-beta.1`) follows beta.
  - **F1.3** The release build accepts `x.y.z-beta.N`. Only an `x.y.z` can become `latest`; a
    release changes `VERSION` and `STABLE` together, and is built before it's marked latest.
  - **F1.4** The installer and `.env` accept an exact beta version.

## 0.2.6 — 2026-10-22

### Added
- **F1.2** The version number at the top links to its release notes on GitHub.
- **F3.1** Adding a calendar source: "Calendar feed (.ics link) — add any calendar with a link
  starting with `webcal://` or ending in `.ics`", with a **Title**, the **Link** and a **Note** (a
  short message shown next to the source's title).
- **F4** Each destination has a **Start** and **End** date (empty = no limit); it only gets the
  events between them.
- **F5.1** Predefined rules in the Rules section: **Items without an end time** and **24-hour
  events**. New sources start with both.

### Changed
- **F1.1** "(v0.2.0)" next to the version reads "(v0.2.0 is available)".
- **F2** The page's layout:
  - **F2.1** **▸ Configure ◂** uses the same rotating arrows as the other collapsible parts.
    - **F2.1.1** Equal, smaller spacing above and below it.
  - **F2.2** No more **(edit)** links: opening Configure turns a source's color, title and note
    into fields.
  - **F2.3** **✓ Validated** is a rounded box like **Healthy**.
    - **F2.3.1** **Save** and **Cancel** together are the same size as that box.
  - **F2.4** Every section except the Calendar has the same kind of heading as Calendar Sources.
    - **F2.4.1** The sections are Calendar, Calendar Sources, Calendar Destinations (the Google
      calendar boxes moved in here), Rules and Activity.
  - **F2.5** Wide screens: Calendar (opens on the calendar view unless another is chosen), then
    Calendar Sources | Calendar Destinations and Rules | Activity side by side, then the footer.
    Narrow screens and phones: one column, the Calendar opens on the List (itinerary) view unless
    another is chosen, and the view and theme switches become one button each that steps through
    the choices.
- **F3.2** A source's Rules:
  - **F3.2.1** Each rule is a rounded box spanning the line.
  - **F3.2.2** Each line starts with a menu of the rules defined in the Rules section, ending with
    **Create a New Rule…**, which opens the same dialog as creating a rule in the Rules section.
- Rule templates are now simply **Rules**: every rule lives in the Rules section and sources pick
  from it. A source's own rules and the ticked rule templates of 0.2.5 are moved there, in the same
  order, with their settings. **Event templates** are a box inside Rules.

### Fixed
- **I1** "Add to Google Calendar" on Android: the calendar was added but never appeared. Google's
  Android app can't subscribe by link, and a linked calendar stays hidden on the phone until its
  **Sync** is turned on. The subscribe page (on Android and iPhone) and each feed's box now explain
  how: add it on calendar.google.com (desktop site), then in the app **Settings →** the calendar
  **→ Sync**; Google can take a few hours to load it.

## 0.2.5 — 2026-10-22

### Changed
- **F1** The page's sections, in order: **Calendar, Sources, Destinations, Rule templates, Event
  templates, Activity**.
  - **F1.1** **Rule templates** (new section): rules kept once, for any source. Each source's Rules
    (under Configure) has a subsection where it ticks the rule templates it uses, alongside its own
    rules; changing a template changes every source that ticks it. A source's own rules come first.
  - **F1.2** **Event templates** is its own section (it was a box at the end of Sources).

## 0.2.4 — 2026-10-22

### Changed
- **F1** The "✓ Validated" slot next to each login (CCS+, the Google client, a feed's Site Address, the
  status-page login):
  - **F1.1** When text is entered, ✓ Validated is replaced by **Save** and **Cancel**, side by side in
    the same space.
  - **F1.2** **Cancel** grows to fill the space, undoes the typing and fades back to ✓ Validated.
  - **F1.3** **Save** grows to fill the space and says **Saved**, then **Verifying…** (yellow) while
    CalendarStream checks the login, then **✓ Validated** (green) or **✗ Verification failed** (red,
    with the reason under the boxes). The page login is simply saved (your browser then asks for it).

## 0.2.3 — 2026-10-22

### Fixed
- The debug links (Response details, Last calendar file received) are back, in the Activity log
  for each source (0.2.2 had dropped them with the old source footer).

## 0.2.2 — 2026-10-22

### Changed
- **F1** Calendar Sources look like the mockups:
  - **F1.1** Each source's header: name (**(edit)**) and kind on the left; on the right, the last
    download ("Downloaded 98 events from feed @ 23:13. (0 new, 0 removed)") above the check
    interval (saved as soon as it's changed), then the status with **Sync Now** under it.
  - **F1.2** **> Configure <** under the header opens the rest; it's folded until opened (and
    remembered), unless something needs doing.
  - **F1.3** **Site Address** (the Calendar Sync link) sits with the UID and password and is saved
    with them; the hand upload is to its right. A feed source's Site Address is its link.
  - **F1.4** Two built-in rules end each source's Rules: **Items without an end time** (last a set
    time, or all day) and **24-hour events** (shown as all-day, or keep their times). They replace
    the ".env" note and override `DEFAULT_EVENT_HOURS` / `ALLDAY_24H` for that source.
  - **F1.5** One line at the bottom: How rules work, **Save** and **Remove**.

## 0.2.1 — 2026-10-21

### Changed
- **F1** Destinations are independent of sources (0.2.0 made a Google calendar and a feed for each
  source). There can be several Google calendars and several feeds; each has its own name and
  ticks the sources it gets, and every event keeps its source's colors and rules. One **Google
  account** box signs in for all the Google calendars. Removing a source takes it off every list;
  removing a Google destination keeps its calendar in Google unless "Also delete it in Google" is
  ticked. Installs from 0.2.0 and before keep their feed links and Google calendar.
- **F3.2** No more "33 events · times in" above the calendar.
- **F3.3** The calendar's time zone moved to the right: time zone, view, 12h / 24h.

### Added
- **F2.1** **Duplicate** and **Delete** icons at the bottom of an event's details and on the event
  page. Delete removes an event added here; a source's own event is hidden instead (its source
  would send it again).
- **F3.1** **Month / Week / Day / List** views, left of the 12h / 24h switch.
- **F4** The **PolyForm Noncommercial License 1.0.0** (`LICENSE.md`): free for non-commercial use, with
  credit to the author; see the README.

## 0.2.0 — 2026-10-21

Calendar sources and destinations: CalendarStream is no longer only for CCS+. An install from
before keeps what it had (CCS+ as its source; the feed, and Google Autosync if it was set up).

### Added
- **F1** The status page has two sections, **Calendar Sources** and **Calendar Destinations**, each
  with **+** in its corner. A new install starts with neither.
  - **F1.1** Sources: **United CCS+ Calendar Sync** (once) and **calendar feeds** (any `.ics` or
    `webcal://` link: another airline, work, school, sports). Each source has its own box: name and
    color (**(edit)**), status chip, check interval, **Sync now**, its login or link, its rules and
    a **Remove** button. Repeating events in feeds are shown from a year back to two years ahead.
  - **F1.2** Destinations: **Google Calendar Autosync**, with a Google calendar of its own for each
    source (removing a source deletes its calendar there), and **Calendar feed**, with a feed link
    and subscribe page for each source.
  - **F1.3** The CCS+ step-by-step help ("How to get a Calendar Sync link, ID and secret") is in the
    same box as the UID and Calendar Sync password.
  - **F1.4** Adding an event asks which calendar it goes in (with more than one source).
- **F2** The first destination asks for the public address (filled in with this page's address
  when it's https://), noting that it can be changed later in ☰ Settings.
- **F3** **Rules** replace Tag Colors (existing tags carry over as color rules). A rule matches a
  title as before; coloring is now one of its actions, so more can follow.
  - **F3.1** Each rule (and each template) has a bin icon to delete it.
  - **F3.2** **Add event**: a rule can add an event from a template some time before the start,
    after the start or after the end of each matching event, e.g. "Drive to the airport", 1:30
    long, 2:00 before each trip. These events follow their event; edit the rule or the template to
    change them.
  - **F3.3** **Event templates**: title, length (or all day), location and color, used by those
    rules and by **Start from a template** when adding an event by hand.
- **F4** **Stream names**: each feed's secret link part can be entered by hand (or taken from a
  pasted old link), so links from before a reinstall, or from a source removed by mistake, work
  again.

### Changed
- `/api/status` also lists each source and the destinations (its top-level fields stay CCS+'s).
- Google sign-in finds or makes a calendar for each source.

## 0.1.24 — 2026-10-21

### Added
- **F1** ☰ Settings → **Admin e-mail**: the administrator's address. The Google Calendar Autosync
  guide fills it in as the support and contact e-mail and as the test user.
- **F2.1** Every password box has an eye button to show what's being typed.
- **F2.2** Password boxes where you choose a password (status-page login, first visit, CCS+
  Calendar Sync password) show a strength bar along their bottom edge as you type (estimated in
  the browser; nothing is sent).

### Changed
- **F3.1** The public address is set only in ☰ Settings. `PUBLIC_URL` is gone from `.env` and the
  installer (which now asks three questions); an existing `PUBLIC_URL` is moved into Settings once,
  after which it can be deleted from `.env`.
- **F3.2** ☰ Settings → Updates reads, e.g., "Subscribed to beta versions (Up to date). Next check at
  10:19.", above **Check for updates** · Weekly · **Check now** on one line.

## 0.1.23 — 2026-10-21

The Autosync setup, reviewed for first-time users (after a real first setup ran into each of these).

### Changed
- The Google Calendar Autosync guide follows the order Google needs: "Before you start" (the public
  address must match the browser's address bar), then create the project, turn on the Calendar API,
  set up the sign-in screen, allow calendar access, **publish the app or add yourself as a test user
  (before creating the client)**, create the client with its Authorized redirect URI, copy both keys
  (Google shows the secret only once) and Connect. Each step ends with a ✓ checkpoint showing what
  you should see.
- Beside **Connect Google Calendar**: the exact address Google sends you back to, which Gmail account
  to use, and what to press on "Google hasn't verified this app" (**Continue**).
- The installer's public-address question and the README Quick start say the address needs
  `https://` and must be typed exactly as in the browser; the first-visit page says where to find the
  setup code.

### Added
- **If Google shows an error:** what to do about redirect_uri_mismatch, access_denied, "hasn't
  verified this app", invalid_client, deleted_client and being asked to connect again each week.
- A warning when the public address and the address the page is open at differ (e.g. a ccs/css
  typo), since Google always sends you back to the public address.

### Fixed
- A refused Google sign-in (403 access_denied) now explains the test-users fix instead of only
  "cancelled".

## 0.1.22 — 2026-10-21

Deploy review, rounds 3–4 (release candidate).

### Fixed
- The login limit across all addresses no longer locks out the owner: addresses that logged in
  successfully in the last 7 days are exempt (strangers' failures can't keep you out).
- Login-failure bookkeeping is thread-safe (two logins at once could cause an error).
- A Google client check saved by 0.1.20 shows correctly after upgrading (✓ Validated plus the
  missing redirect URI, instead of "Google rejected the client").
- The installer can't stop silently on macOS when looking up this computer's address.
- The 12h / 24h switch and the event pin keep their size again (0.1.18 had squashed the switch), and
  the calendar legend's "?" sits in its circle.

### Added
- README screenshots (from a made-up demo schedule).
- Translations for everything added since 0.1.18.

## 0.1.21 — 2026-10-21

Deploy review, second round.

### Security
- Forwarded headers (the visitor's address and https) are only believed from this computer unless
  `FORWARDED_ALLOW_IPS` names your reverse proxy (see `.env.default`); behind a proxy, set it and the
  Public address. A limit across all addresses (50 failed logins in 15 minutes) stops guessing from
  many made-up addresses, and addresses that are locked out are never forgotten early.

### Fixed
- When Google doesn't list the redirect URI, the Google box keeps **✓ Validated** (the ID and secret
  are right) and shows a separate red line with the exact address to add, a **Check again** button,
  and Connect waits; the result only counts for the address that was checked.
- The old installer default `http://localhost:8080` (macOS) also counts as not set; the installer
  finds this computer's address on macOS.
- **Check now** no longer makes the log announce the same update again.
- An https link that redirects to http gets an accurate message.
- The public address refuses typos such as `http:/example.com` and `…;params`; `.local` addresses
  aren't offered to Google.

## 0.1.20 — 2026-10-21

Deploy review fixes (programming, commenting, security).

### Fixed
- **Google sign-in (`redirect_uri_mismatch`):** the installer's default public address was
  `http://<this computer's IP>:8080`, which then replaced the address the page is opened at, so the
  redirect URI didn't match what's registered in Google Cloud. The installer now leaves it empty
  (Enter skips it, "-" clears it), and that old default in `.env` counts as not set.
- The client check now says when Google doesn't list the redirect URI (with the exact address to
  add) instead of showing ✓, and Connect stays off until it's fixed. The guide only shows a redirect
  URI Google can accept (https with a domain name).
- The public address is tidied the same way everywhere: lower-case scheme and host, default ports
  and a trailing slash dropped.
- The background loops (CCS+, Google) survive a database restart; finishing a Google sign-in can no
  longer race a sync (no duplicate calendars); "Update available" is logged once, not at every check.
- The Public address text no longer runs under the "This page" button in Settings.

### Security
- The login lockout can't be dodged with a made-up `X-Forwarded-For` as easily: forwarded headers
  were limited to proxies on private networks (0.1.21 tightens this further), and the failure list
  is bounded.
- The first-visit page has its own form token, the status page's token is renewed whenever the
  login is created or changed, and form posts from other websites are refused.
- Pages can't be framed, and send `nosniff` and `no-referrer`; `/healthz` no longer shows database
  details; non-ASCII tokens no longer cause errors.
- Downloads from CCS+ are https only (also after redirects), at most 5 redirects and 5 MB.
- The installer makes `.env` readable by you only and stores answers with `|` or `&` safely; the
  release workflow gives each job only the permissions it needs.

### Changed
- Comments, docstrings, README and `.env.default` brought up to date; unused CSS, scripts and code
  removed.

## 0.1.19 — 2026-10-21

### Added
- **F1** ☰ Settings → **Check for updates**: Hourly, Weekly (the default), Monthly or Never, plus
  **Check now**. It follows this install's release (`IMAGE_TAG`): a stable install is only told
  about stable versions, a beta install about the newest beta. A newer version shows in brackets
  next to the version at the top, linked to its release notes, and once in the activity log.

### Changed
- **F1 (tags)** Tag Colors shows only saved tags. With none, the box is just its header with **+**
  in the corner; **+** at the end of the last tag adds another. The Save line appears once there's
  something to save.
- **F2** The Google client guide is seven short steps, with its own "Create the OAuth client ID"
  step, and what to do when Google won't publish the app (stay in Testing and add yourself as a
  test user).
- **F3** **Sync now** is in the CCS+ Calendar Sync box (the schedule header keeps the status chip).
- `docker-compose.yml` passes `IMAGE_TAG` to the app.

### Fixed
- **I2** On the event page, only the All-day box and its words tick it (clicking elsewhere on the
  line did too); the same for the other check boxes there.

## 0.1.18 — 2026-10-20

The presentation review (#1–#11), except #4: logins stay on the dashboard.

### Changed
- **#1** One pattern for every section: the schedule card's header shows its status chip and
  **Sync now** on the right (folded or not), and each part of Status & setup is a box with a title,
  a one-line subtitle and a status chip. Activity log uses the same title style.
- **Logins:** the CCS+ login and the Google Autosync client (with Connect, Disconnect and the
  instant-updates line) live only on the dashboard, in their boxes. **☰ Settings** now holds only
  site settings: the status-page login and the public address.
- **#2** Tag Colors' explanation is folded behind "How tags match".
- **#3** "Check for changes every [60] minutes" is a labelled field; the `.env` facts are one line under it.
- **#5** Box titles have short subtitles instead of long bracketed descriptions.
- **#6** Autosync is the main path; **Subscribe to the feed** and **Share it** are folded under
  "Other ways to get the schedule".
- **#7** The feed's "read by Google" status is a chip, with "What to check" folded.
- **#8** One status chip (✓ good, ! warning, ✗ problem, ↻ working) everywhere.
- **#9** Two button styles (primary, secondary), all the same height; "Choose Calendar.ics…"
  replaces the browser's file box and shows the chosen file.
- **#10** The calendar's legend is one row, with its hint behind a "?".
- **#11** All step-by-step and help folds look the same.

## 0.1.17 — 2026-10-20

### Changed
- **F1** CCS+ Calendar Sync is laid out like Google Calendar Autosync: the step-by-step help is at
  the bottom of the box, now called "How to get a Calendar Sync link, ID and secret (step by step)".
- **F3.1** "Colour" is spelled "color" everywhere in English.
- **F4** The folded schedule header shows **Sync now** on the right.
- The release workflow no longer copies images from the old `calendar_stream` package (every
  version is under `calendarstream`; the old package is being removed).

## 0.1.16 — 2026-10-20

### Added
- **F2.2** A time-zone menu above the calendar ("times in …"): shows the calendar in any time zone.
  It only changes this page; the feed, Google and the server keep `TZ` from `.env`.
- **F2.3** Event times are one box each: type them ("9:30", "9:30pm", "21:30", "930") or pick from
  a list every 15 minutes (the end list shows the length). A **Time zone** menu, and **The end is
  in a different time zone** for events such as flights; lengths are kept in real hours across
  zones, and the event page remembers the zones used.
- The Subscribe box says when Google Calendar last read the feed, or that it hasn't yet, with
  what to check.

### Changed
- **F1.1, F1.2** In Settings and Status & setup, the CCS+ and Google client logins show
  **✓ Validated** to the right of the boxes; it turns into **Save & sync** / **Save** when a box is
  empty, being edited, or the check failed.
- **F1.3** The status-page login looks like the other logins: user name and password with
  **✓ Signed in**; typing a new password asks for the current one and shows **Save**.
- **F1.4** **Public address** is right under the status-page login, with **This page** inside the
  box, **Save** on the same line and the explanation underneath. Buttons are now always on the
  same line as their boxes.
- **F1.5** Time format is no longer in Settings; use the 12h / 24h switch above the calendar.

### Removed
- The hour / minute / am-pm menus on the event page (replaced by the time boxes).

## 0.1.15 — 2026-10-20

### Added
- **F3** Instant updates from Google (webhooks). With Autosync and a public `https://` address,
  CalendarStream asks Google to notify `/google/notify` whenever its calendar changes there; a
  change or deletion made by hand in Google is put back within seconds instead of at the daily
  check. Notifications are checked against a secret token, renewed every week, moved when the
  public address changes, and stopped on disconnect. If Google refuses them, Autosync carries on
  with the daily check and asks again 6 hours later. Settings and the Google section show whether
  they're on.
- **F1.1** Click the month and year above the calendar to jump to any month (‹ › change the year).
- **I1** A **12h / 24h** switch at the top right of the calendar (the same setting as ☰ → Time format).

### Changed
- **F2.1** Settings forms match the status page: labels above the boxes, boxes side by side
  (user name and current password; new password twice), buttons beside their notes.
- **F2.2** Each Settings section is in its own outlined block.

## 0.1.14 — 2026-10-20

### Changed
- **I1 (labels)** The CCS+ Calendar Sync login and the Google Autosync client have their labels
  outside the boxes, and the two boxes of each sit side by side on one line (UID and password;
  Client ID and Client secret), with the button at the end of the line.
- **F2** CCS+ Calendar Sync's contents are in a box, like the Google Calendar ones.
- **F1** In the Google Calendar boxes, the buttons (Connect, Add to Google Calendar, Open subscribe
  page) sit to the right of their explanation, so the section is shorter.
- **I1 (tags)** **Tag Colors** is now its own block, always visible right under the health bar,
  instead of inside (edit). (edit) keeps the calendar's name and default colour.

## 0.1.13 — 2026-10-20

### Changed
- **F1** The Google Calendar Autosync client form looks like the CCS+ Calendar Sync login: the
  Client ID and Client secret boxes are stacked full width and named by their placeholders, with
  the description and **Save** below them.

## 0.1.12 — 2026-10-20

### Changed
- **F1** Settings → Google Calendar Autosync is shorter: **Client ID** and **Client secret** each sit
  on one line with their box, and the description shares the last line with **Save**. The Google
  section of Status & setup uses the same layout.
- **I1, I2** The "Subscribe to the feed" note now says what Google does with a subscribed feed: it
  re-reads it on its own schedule, which can take up to 12 hours, and keeps the name it saw first.
  New events and a new name reach Google within minutes only with Autosync.

## 0.1.11 — 2026-10-20

### Added
- **F1.2** **Time format** in Settings: 12-hour (1:30pm), 24-hour (13:30, "military") or Automatic
  (12-hour in English, 24-hour in the other languages). It applies to the calendar, event details,
  the activity log and the event page.
- **F1.3** An event colour, bottom left on the event page: one of Google Calendar's 11 event colours,
  or the default (from a tag or the calendar). It wins over tags, on this page and in Autosync.

### Changed
- **F1.1** On the event page, changing the start (date or time) moves the end by the same amount,
  so the event keeps its length. Changing the end sets a new length.
- **F1.2** Times are picked from hour and minute menus (01–12 with am/pm, or 00–23) instead of the
  browser's time box, whose values ran on endlessly when scrolled.
- **F1.4** **Cancel** and **Save** are at the bottom right of the event page.
- **F2.1** Once Google accepts the client, the Client ID and Client secret fold away behind
  "✓ Validated: Client ID & Client secret" (click it to change them).
- **I2** "✓ Validated: CCS+ accepted the sign-in" now reads "✓ Validated: CCS+ sign-in".

## 0.1.10 — 2026-10-20

### Changed
- **F1.1** The setup checklist (UID, Calendar Sync password, link, CCS+ accepted the sign-in,
  schedule received) now sits just under the CCS+ login, above "CCS+ Calendar Sync · checks every".
- **F1.1.1** "How to turn on Calendar Sync in CCS+" sits to the right of the checklist (below it on
  phones), in a sub-block of their own with the Calendar Sync link box.
- **F1.1.2** That sub-block is only open while the UID or Calendar Sync password is missing, or the
  last update failed (sign-in rejected, blocked, error or paused); otherwise it's closed.
- The month view's hint mentions clicking an empty spot on a day to add an event.

### Fixed
- The calendar-name hint for Autosync (0.1.9) never showed; it now does when Google is connected.

## 0.1.9 — 2026-10-20

### Added
- **F1.3** The installer asks for the **public address** (default `http://<this computer's IP>:8080`);
  it may also be entered later in ☰ Settings.
- **I1.2** The CCS+ UID and Calendar Sync password are in the **Settings** menu (☰), with whether
  CCS+ accepted them.
- **F4** A footer with the version and links to **Report a problem** and **Suggest a feature**
  (GitHub issue forms; the bug form is filled in with the version).
- **F6.2** A pin (bottom right of an open event) keeps it open.
- **F6.3** Clicking an empty spot on a day opens **Add event** for that day.
- **F6.4** A line under **Add to Google Calendar** and **Open subscribe page** explaining each.
- The installer works on macOS (Docker Desktop) and on Windows inside WSL.

### Changed
- **F1.1** Running the installer again offers your current settings as the defaults.
- **F1.2** The installer's questions are now: release (stable or beta), the folder for
  `docker-compose.yml` and `.env`, then the config and data folder, which is always asked so you can
  confirm it.
- **I1.1** With no CCS+ login yet, the health bar shows **Setup needed** (not an error) and asks for
  it; nothing is downloaded until it's entered. The **CCS+ Calendar Sync** login now sits just under
  the health bar, always visible, with "✓ Validated: CCS+ accepted the sign-in" when it works, and
  the note "Your CCS+ UID and Calendar Sync password may be updated in Status & setup, or in
  Settings (☰)." Status & setup opens by itself until it's set up.
- **F2.1** The Settings Google section is now **Google Calendar Autosync**: Client ID, Client secret
  and a closed "How to get a client ID and secret (step by step)".
- **F3** Status & setup's Google section has three parts: **Autosync** (connected, or the client
  ID and secret with the same guide), **Subscribe to the feed** (the raw feed URL and **Add to Google
  Calendar**) and **Share it** (the shareable subscribe page and **Open subscribe page**).
- **F4** Copy buttons use the Bootstrap "copy" icon.
- **F5** The upload line is shorter: "Or upload **Calendar.ics** by hand."
- **F6.1** Clicking anywhere else closes an open event (unless it's pinned).
- **I2** The calendar-name hint says Autosync renames the Google calendar by itself; without
  Autosync, Google keeps the name it saw when you subscribed, so rename it in Google too.
- README: works on Linux, macOS or Windows (WSL); the installer's four questions in order.

## 0.1.8 — 2026-10-20

### Added
- **F1** A copy button next to the setup-code command on the first-visit page.

### Fixed
- **I1** The setup-code command named the service (`calendar_stream`), which is easy to mistype as
  `calendarstream` ("no such service"). It's now `docker compose logs | grep "setup code"`, run in
  the folder with `docker-compose.yml`, which needs no service name. The "wrong setup code" message
  says the same.

## 0.1.7 — 2026-10-20

### Changed
- **R1** The installer's release question now reads "Which release would you like to install,
  latest (stable) or beta [stable]:". Both `latest` and `stable` choose the stable release.

## 0.1.6 — 2026-10-20

### Added
- **F1** The installer asks which release to run: **stable** (the default) or **beta**. Pressing
  Enter on a later run keeps the current choice; it's saved in `.env` as `IMAGE_TAG`.

### Changed
- **R1.1** New README introduction, explaining why CalendarStream exists and its two ways of
  getting the schedule into Google.
- The README's Quick start lists the installer's three questions and defaults exactly, and stays short.

## 0.1.5 — 2026-10-20

### Added
- **F1** **Languages:** English, Español, Français, Deutsch, Português (Brasil) and Vlaams. Choose
  one with the new **globe** button, left of the theme switch, or **Automatic** to follow the
  browser; the choice is saved in the database. Everything on screen is translated: every page,
  menu, button, help text and guide, status messages, the activity log, error pages, and the
  month and day names. Event titles stay as United sends them. The shareable subscribe page uses
  each visitor's browser language.
- Errors from forms (e.g. a check interval below 15 minutes) are shown as a small page in your
  language with a **Go back** link, instead of raw JSON.

### Changed
- **F2.1** The installer's first question names what goes there: "Folder for docker-compose.yml
  and .env".
- **F2.2** The installer then asks for **CalendarStream's config and data folder** (the database
  and `.secrets/`, saved in `.env` as `MNT_DOCKER`). It defaults to the first folder and is only
  asked once.
- README: running the installer again is safe: it never overwrites an existing `.env` or the
  database password. The note about upgrading from 0.1.2 is gone.
- Two messages that still pointed at the old secret files and the old upload location now point
  at Setup and **Upload & publish**.

### Fixed
- On narrow screens the title could be squeezed under the header buttons; it now shortens neatly.

## 0.1.4 — 2026-10-20

### Added
- **`install.sh`**: installs or updates CalendarStream with one command
  (`bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)`). It
  downloads `docker-compose.yml` and `.env` (keeping an existing `.env`), creates a random database
  password once, starts the stack and shows the setup code.

### Changed
- **F1** `MNT_DOCKER` is optional. Without it, the installer asks for an installation folder, and the
  database and `.secrets/` live next to `docker-compose.yml`. Set it in `.env` (or before running the
  installer) to keep them elsewhere, e.g. `/mnt/SSD/docker`.
- The README is about a third as long, with a one-command quick start and a table of settings.

## 0.1.3 — 2026-10-20

The logins move into the app. Only `DB_PASSWORD.txt` stays on the server.

### Added
- **First visit:** CalendarStream asks you to create the status-page login. It first asks for a
  **setup code** printed in the container log (`docker compose logs calendar_stream | grep "setup code"`),
  so only someone with access to the server can claim a new install. The password is stored hashed.
- **Settings (☰) → Status-page login:** change the user name and password (needs the current one).
- **Setup:** boxes for your CCS+ **UID** and **Calendar Sync password**, with **Save & sync**. The
  password is stored encrypted and never shown again. Setup opens by itself until they're entered.
- Logins from the old secret files are imported once, if the old compose file still mounts them.

### Changed
- `docker-compose.yml` mounts only `DB_PASSWORD.txt`. `CCS_USER.txt`, `CCS_PASSWORD.txt`, `USER.txt`
  and `PASSWORD.txt` are no longer used and can be deleted (after the import, if you want it).
- `DB_PASSWORD` is also the key that encrypts the stored passwords (CCS+, Google), as it already was
  for Google.
- Messages about a rejected or missing CCS+ login point to Setup instead of the secret files.

## 0.1.2 — 2026-10-20

### Added
- **Settings (☰) → Public address**: the https:// address people use to reach the status page,
  used for the feed and subscribe links and Google's sign-in redirect. It overrides `PUBLIC_URL`
  in `.env`, which is now optional; **Reset** goes back to `.env`, and **This page** fills in the
  address the page is open at. "cal.example.com" is completed to "https://cal.example.com".

### Changed
- `.env.default` is shorter and clearer: only `MNT_DOCKER` is required, and every other setting is
  marked `# optional` with its default and what overrides it. The unused shared-host folders and the
  `CCS_*`/`GUI_*` login lines (the secret files replace them) are gone.
- Warnings about a missing public address point to Settings instead of `.env`.

## 0.1.1 — 2026-10-20

### Changed
- The image is now **`ghcr.io/uuugh/calendarstream`** (was `ghcr.io/uuugh/calendar_stream`), to match
  the repository's new name, `Uuugh/CalendarStream`. Every earlier version, `beta` and `latest` were
  copied to the new name, so any tag can be pulled from it. Update `docker-compose.yml` (`git pull`);
  the old name gets no new releases.

## 0.1.0 — 2026-10-20

First minor version: **Google Calendar sync** (0.0.12 and 0.0.13), plus the items below. A beta
until it passes the stable reviews and your approval.

### Added
- **F2.1.1** The check interval can be changed on the status page: type the minutes (15–1,440) and
  press **Save**. It's saved in the database (overriding `SYNC_INTERVAL_MINUTES`), and the next
  check moves to match.
- **F3.2** CalendarStream checks the Google client ID and secret with Google when they're saved,
  and shows ✓ accepted, ✗ rejected (unknown client ID or wrong secret) or ? (Google couldn't be
  reached). **Check again** repeats it. **Connect** is disabled while Google rejects them.

### Changed
- **F1** The theme switch is in the order Light, Dark, System.
- **F2.1** The line "CCS+ Calendar Sync · checks every … · items without an end time …" moved from
  under the title to just below the health bar.
- **F2.2** **Upload Calendar.ics** moved out of Setup to just below that line, in a smaller, more
  compact row (the full explanation is in its tooltip).
- **F3.1** In Settings → Google Calendar, the Client ID and Client secret boxes come first; the
  step-by-step guide is below them and starts closed.
- The release workflow keeps the image name `ghcr.io/uuugh/calendar_stream` even if the GitHub
  repository is renamed, so `docker-compose.yml` and the `latest`/`beta` tags keep working.

## 0.0.13 — 2026-10-20

Second beta of **Google Calendar sync** (planned for 0.1.0): the events are copied.

### Added
- **Event sync to Google.** Once connected, CalendarStream writes the schedule into its Google
  calendar and keeps it in step: within seconds of a download, upload or edit, sending only what
  changed. Covered: events from the first day of the current month onward (older ones are left
  alone in Google), edits, hidden events (removed from Google) and added events. No reminders.
  CCS+'s "free" items stay *free* in Google, the rest *busy*.
- **Tag colours in Google:** each tag uses the nearest Google event colour (Tomato, Basil, Peacock
  and so on). Events with no tag take the calendar's colour.
- **F2 (from 0.0.10):** renaming the calendar on the status page renames it in Google too.
- A daily check, and **Sync now** in the menu, compare Google's copy with the schedule and put back
  events changed or deleted there (events you added to that calendar yourself are kept). A calendar
  deleted in Google is made again.
- The menu shows the last sync and its result; the Activity log's status line shows Google's state,
  and the log records each sync that changed something (e.g. "Google: 3 added, 1 updated").
- **The Google OAuth client is entered in Settings (☰) → Google Calendar** (Client ID and Client
  secret), with a step-by-step guide for getting them in Google Cloud. The secret is stored
  encrypted with a key derived from `DB_PASSWORD` and never shown again. One client serves the
  whole app.

### Removed
- The `GOOGLE_CLIENT_ID.txt` and `GOOGLE_CLIENT_SECRET.txt` secrets from 0.0.12, and their lines in
  `docker-compose.yml` (now the same as in 0.0.11). Those files can be deleted.

## 0.0.12 — 2026-10-20

First beta of **Google Calendar sync** (planned for 0.1.0): connecting a Google account. Events
are copied in the next beta.

### Added
- **Settings (☰) → Google Calendar**: **Connect** signs in to Google and creates a calendar of
  CalendarStream's own, named like the feed; the menu then shows the connected account and
  calendar. **Disconnect** removes CalendarStream's access in Google, and can also delete the
  calendar. Connecting the same account again reuses the calendar.
- CalendarStream asks Google only for calendars it creates (`calendar.app.created`) and your
  e-mail address. The sign-in is stored encrypted with a key derived from `DB_PASSWORD`.
- Secrets `GOOGLE_CLIENT_ID.txt` and `GOOGLE_CLIENT_SECRET.txt` for the Google OAuth client, with
  set-up steps in the README. The menu shows the redirect URI to give Google.

### Changed
- `docker-compose.yml` mounts the two new secrets. **Create both files before recreating the
  stack**, even empty: Docker won't start a stack with a missing secret file.

## 0.0.11 — 2026-10-20

### Added
- **F1** Each tag row has a **match** setting: *Whole word* (default; "RDO" matches "RDO." but not
  "VRDO"), *Contains* (anywhere, even inside a word), *Starts with*, or *Exact title*; and an **Aa**
  button to match capitals exactly.

### Changed
- **F2.1** In **Setup: CCS+ Calendar Sync**, the box for the CCS+ **Copy link** URL comes first,
  directly under the title.
- **F2.2** Setup can be collapsed and starts closed, showing a one-line summary (e.g. "Schedule
  received · 97 events"). Whether it's open is saved in the database like the other sections.

## 0.0.10 — 2026-10-20

### Added
- A reminder under the calendar name in the editor: Google only reads the name when the calendar is
  first added, so a calendar already in Google Calendar has to be renamed there too (with the steps).

### Not done
- **F2** (rename the calendar in Google automatically) is skipped for now. It would need CalendarStream
  to connect to a Google account through the Google Calendar API.

## 0.0.9 — 2026-10-20

### Added
- **F1** Tag colours. In the Status & setup editor, each row has a tag, a colour, **×** to remove it
  and **+** (on the last row) to add another. An event whose title contains a tag as a whole word
  (ignoring capitals) uses that tag's colour in the month view, and the first matching tag wins.
  Other events use the default colour. Tags also appear in the colour key.
- **F1.3** A **Default** button next to the colour picker returns to the standard colours.

### Changed
- **F1.4** The Status & setup title now shows the calendar's name as text in the chosen colour,
  outlined when that colour would be hard to read on the background. A small **(edit)** next to
  it opens the editor (name, default colour, tag colours, **Save**).
- **F1.1** **Save** is right-aligned in the editor, next to **Cancel**.
- **F1.2** The name field stretches to fill the editor's width.

## 0.0.8 — 2026-10-20

### Added
- **F1** A colour picker next to **Save**. The colour tints United's events in the month view
  (timed lighter, all-day stronger) and is added to the feed as `X-APPLE-CALENDAR-COLOR`, which
  Apple Calendar uses. Google Calendar ignores feed colours, so Google subscribers choose their own.

### Changed
- **F2** The Activity log starts closed. Which sections are open is now saved in the database, so
  it's the same in every browser and after signing in again.
- The light / dark / system theme is also saved in the database, so every browser uses the same
  theme. Pages are drawn in the chosen theme from the start (no flash of the other theme).
- **F3** The calendar is now at the top of the page.
- **F4** The calendar's name, colour and **Save** are now the title of the Status & setup section.
  Clicking elsewhere in that title, or its arrow, opens or closes the section.

## 0.0.7 — 2026-10-20

### Added
- **F3** A **Settings** menu (☰) at the right of the title bar. It's empty for now.
- **F4** A **Light / System / Dark** theme switch just left of the Settings menu. The choice is
  remembered in this browser; **System** follows the device's setting. The event editor uses it too.
- **F5** Every section except the calendar can be collapsed by clicking its title. Each browser
  remembers which sections are open. A collapsed section still shows a summary: the status and
  latest message, or the latest activity-log entry.

### Changed
- **F1** The dashboard is reorganised:
  - **F1.1** The health bar, the Google Calendar feed and **Setup: CCS+ Calendar Sync** are now
    one section, **Status & setup**, in that order.
  - **F1.2** The activity log scrolls inside a window five rows tall.
  - **F1.3** The debug links (last download) are inside the Activity log section, below the log.
  - **F1.4** The Activity log title is at the top of its section, above the status line.
- **F2** The app is now called **CalendarStream** (one word).

## 0.0.6 — 2026-10-20

### Added
- **F1** A **Calendar Name** box next to the Google Calendar feed buttons. It sets the name Google
  shows for the calendar and is used by the feed and the subscribe page. It's saved in the
  database and overrides `CALENDAR_NAME`.
- **F3** Editing in the month view:
  - Click an event, then **Edit**, to change its title, all-day setting, start and end, location
    or notes, or to **hide it from Google Calendar**.
  - Edits to United's events are stored separately and re-applied after every download, so they
    survive syncs. ✎ marks an edited event; ⚠ marks one that United changed after your edit.
    **Revert to United's version** undoes an edit.
  - **+** on a day adds your own event (shown in purple), which can be edited or deleted later.
  - Nothing is ever changed in CCS+.
- A colour key under the month view.

### Changed
- **F2** "(Recommended)" now appears before the shareable subscribe page link.
- **F4** The sign-in, last check, schedule changed, next check and event count are condensed into
  one line at the top of the Activity log card. Today's times are shown without the date.
- **Add to Google Calendar** passes the feed as `webcal://`, the format Google's "Add calendar?"
  prompt expects.
- Status messages count the events in the feed (hidden events are excluded).

### Fixed
- **Add to Google Calendar** opened Google Calendar without offering to add the calendar.
- Two elements on the status page shared an `id`, which could break the **Copy** buttons.

## 0.0.5 — 2026-10-20

### Changed
- Downloads from CCS+ now use **curl**. curl identifies itself as curl; the UID and Calendar Sync
  password are passed to it privately, never on a command line.

### Fixed
- Automatic downloads never completed: United's Akamai protection held requests from Python's
  HTTP library (no reply for 60 s, or an immediate 403) but answers curl normally.
- Status messages said "ccs+" instead of "CCS+".

### Removed
- The `httpx` library (replaced by curl).

## 0.0.4 — 2026-10-20

### Changed
- `docker-compose.yml` sets `pull_policy: always` for the app, so `docker compose up -d` (including
  a recreate) checks for a newer image first.

### Fixed
- Recreating the stack didn't pick up a moved `beta` tag without a separate `docker compose pull`.

## 0.0.3 — 2026-10-20

### Added
- **Upload Calendar.ics** in Setup: publish a file downloaded by hand from the Calendar Sync link
  (United's own procedure for Google Calendar) when the automatic download can't get through.

### Changed
- Timeout errors say whether the connection failed or the server never replied.

### Fixed
- Day codes (RDO, HDO, VRDO, VHDO…), which CCS+ sends as a midnight start with no end, appeared as
  00:00–01:00 events. They're now all-day events.
- Full reserve and sick days, sent as 00:01–23:59:59, weren't treated as 24-hour events. The
  24-hour rule now allows up to 5 minutes either way (previously 1).
- Event details on the status page started with a blank line.

## 0.0.2 — 2026-10-20

### Added
- Downloads from United's official **CCS+ Calendar Sync** (`Calendar.ics`) with your UID and
  Calendar Sync password, on a timer (`SYNC_INTERVAL_MINUTES`, default 60, minimum 15). Unchanged
  schedules aren't downloaded again (ETag).
- Events lasting exactly 24 hours (or 48, 72…) become all-day events (`ALLDAY_24H`).
- A month view on the status page, with ‹ › navigation, **Today** and event details.
- **Setup**: a checklist, a box for the CCS+ **Copy link** URL, and the CCS+ steps.
- A prebuilt image `ghcr.io/uuugh/calendar_stream`, tagged `0.0.x`, `beta` and `latest`, for amd64
  and arm64; `docker-compose.yml` uses `image:` and needs no build.
- Settings `CCS_CALENDAR_URL`, `SYNC_INTERVAL_MINUTES`, `ALLDAY_24H` and `IMAGE_TAG`.
- Protection against cross-site form submissions on the status page.

### Changed
- United's events are republished as sent (same IDs, times and details) under `CALENDAR_NAME`.
- Clear statuses for a rejected sign-in (automatic checks pause after 2), an Akamai block, and an
  answer that isn't a calendar. The previous feed is kept after any failure or a sudden empty
  calendar.

### Fixed
- The schedule couldn't be read: the CCS website blocks automated browsers (Akamai "Access Denied").

### Removed
- The headless browser (Playwright/Chromium), CCS website login and HTML parsing.
- Settings `CCS_URL` and `CCS_*_SELECTOR` (`SCRAPE_INTERVAL_MINUTES` is still read as a fallback).

## 0.0.1 — 2026-10-19

First release as **Calendar Stream** (previously `ccs_calendar`).

### Added
- iCalendar feed for Google Calendar, plus a shareable subscribe page.
- Status page with login results, sync history, upcoming events, debug captures and the version.
- `DEFAULT_EVENT_HOURS`: a number of hours, or `allday`, for items without an end time.
- Status-page lockout after 5 failed logins.
- All data stored in Postgres (`calendar_stream_db`).
- Docker secrets for the CCS login, the status-page login and the database password.

### Fixed
- Pages that never go quiet timed out while loading ("networkidle").
- Copy buttons didn't work when the status page was opened over plain HTTP.
