# Changelog

Versions are numbered `0.y.z`; the minor version (`y`) only changes when it's decided (0.1.0 was the
first). Every release is tagged `v<version>`; the newest is also tagged `beta`. The last one marked stable (in the `STABLE` file) is
the `latest` image and the GitHub Release marked **Latest**. Each version lists what was **added**, **changed**, **fixed** and
**removed**. Feature requests are labelled F1, F2, …

**Stable (`latest`): 0.0.6 · Newest (`beta`): 0.1.8**

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
