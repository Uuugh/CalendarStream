# Changelog

Versions are numbered `0.0.x` until a new minor version is decided. Every release is tagged
`v0.0.x`; the newest is also tagged `beta`, and the last one marked stable is tagged `latest`
(set by the `STABLE` file). Each version lists what was **added**, **changed**, **fixed** and
**removed**. Feature requests are labelled F1, F2, …

**Stable (`latest`): 0.0.6 · Newest (`beta`): 0.0.6**

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
