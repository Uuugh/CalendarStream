# Changelog

Versions follow `0.0.x` until a new minor version is decided.
The newest release is also tagged `beta`; the last stable release is tagged `latest`.

## 0.0.1 — 2026-10-19 (beta)

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
