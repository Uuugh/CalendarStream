# Changelog

Versions follow `0.0.x` until a new minor version is decided.
The newest release is also tagged `beta`; the last stable release is tagged `latest`.

## 0.0.2 — 2026-10-20 (beta)

Switched from reading the CCS website to United's official **CCS+ Calendar Sync** download.

- Downloads `Calendar.ics` from CCS+ Calendar Sync with your UID and Calendar Sync password
  (HTTP Basic), on a timer (`SYNC_INTERVAL_MINUTES`, default 60, minimum 15); uses ETags so
  unchanged schedules aren't re-downloaded
- Republishes United's events as-is (same IDs, times and details) under `CALENDAR_NAME`
- Events lasting exactly 24 h (or 48 h, 72 h…) become all-day events (`ALLDAY_24H`)
- Events with no end time follow `DEFAULT_EVENT_HOURS` (hours or `allday`)
- Clear statuses for rejected sign-ins (pauses after 2), Akamai blocks, and non-calendar answers;
  the previous feed is kept on any failure or a sudden empty calendar
- Status page: month view with ‹ › month navigation and event details; **Setup** checklist with
  a box for the CCS+ **Copy link** URL and the CCS+ steps; debug shows the response and download
- `docker-compose.yml` now uses the prebuilt image `ghcr.io/uuugh/calendar_stream:${IMAGE_TAG}`;
  no local build. GitHub Actions builds amd64/arm64 images tagged `0.0.x`, `beta`, and `latest`
  (when marked stable)
- Removed the headless browser (Playwright/Chromium), CCS website login and HTML parsing
- New settings: `CCS_CALENDAR_URL`, `SYNC_INTERVAL_MINUTES`, `ALLDAY_24H`, `IMAGE_TAG`.
  Removed: `CCS_URL`, `SCRAPE_INTERVAL_MINUTES` (still read as a fallback), `CCS_*_SELECTOR`
- Status-page forms are protected against cross-site requests

## 0.0.1 — 2026-10-19

First release as **Calendar Stream** (previously `ccs_calendar`).

- Logs in to United CCS with headless Chromium (Playwright), reusing the saved session
- Tolerant page loading (no longer waits for "networkidle", which timed out on CCS)
- Parses the schedule from the page's JSON data, falling back to HTML tables
- `DEFAULT_EVENT_HOURS`: hours, or `allday`, for items without an end time
- iCalendar feed for Google Calendar, plus a shareable subscribe page
- Status page: login results, sync history, upcoming events, debug captures, version
- Status-page lockout after 5 failed logins; copy buttons work over plain HTTP
- All data stored in Postgres (`calendar_stream_db`)
- Docker secrets for the CCS login, status-page login and database password
