# Dart / Flutter migration of CalendarStream

Baseline: `0.2.8-beta.4`, commit `6d1044c9d9b3635be3367d5a0e34dc967150fa6a`.
Work only on `flutter-migration-v0.2.8-beta.4`. Preserve `main`, its image tags,
the existing Python application and all user data.

## Architecture

Use **Dart for the backend and shared calendar logic** and **Flutter Web for
the interactive client**. Flutter alone does not replace FastAPI, scheduled
jobs, Google OAuth callbacks, Postgres or iCalendar feed endpoints.

- `dart/calendarstream_core`: platform-independent event model, parsing,
  recurrence, ICS output, edits, rules and sync planning.
- `dart/calendarstream_server` (later): HTTP endpoints, login/CSRF,
  encrypted secrets, Postgres, CCS+ downloader, Google API and jobs.
- `flutter_app` (later): responsive Flutter Web status page.
- Separate test Docker image and Compose override; never repoint `:beta`
  or `:latest` without approval.

## Feature parity checklist

| Area | Reference implementation | Required validation |
| --- | --- | --- |
| CCS+ and generic HTTPS sources | `app/calsync.py` | Auth, redirect limits, max size, timeouts, 304/errors |
| ICS events and feeds | `app/calsync.py` | Dates, time zones, 24-hour tolerance, recurrence and cancellations |
| Edits and custom events | `app/calsync.py`, `app/store.py` | Stable IDs, stale edits, hide/free/color/reminders |
| Rules and templates | `app/rules.py` | Conditions, grouping, priority, actions and generated events |
| Google Calendar | `app/gsync.py` | OAuth, encrypted tokens, event mapping, retries and sync state |
| Persistence | `app/store.py` | Schema compatibility, transactions, backups and rollback |
| Authentication | `app/logins.py`, `app/main.py` | Session, lockout, CSRF and feed token boundaries |
| Web interface | `app/templates/`, `app/static/` | All controls, responsive views, editing, feedback |
| Localization | `app/locales/*.json` | All locales and keys |
| Docker and installer | `Dockerfile`, `docker-compose.yml` | Linux, macOS and Windows WSL, health and upgrade |

## Theme fidelity

Follow `build_rules/theme.md` and both Theme Rules reference images.
IBM Plex Sans for text, IBM Plex Mono for exact/copyable content, Material
Symbols icons only; 8px controls, 12px sections/modules, 50px module headers,
34px controls and 5px gaps. Reuse every light/dark color token in
`app/templates/_theme.html`. Preserve system/light/dark behavior and
responsive layouts. Compare screenshots using the fictional
`tests/data/Demo.ics` and never the Developer's real schedule.

## Milestones

1. **Core foundation:** event model, ICS output, source policy and tests.
2. **Calendar parity:** parser, recurrence, time zones, edits and rules with
   differential fixtures against Python.
3. **Server parity:** Postgres, downloads, secrets, Google, scheduled sync,
   feeds and authenticated endpoints with integration tests.
4. **Flutter UI:** all screens, translations, theme fidelity, mobile and
   end-to-end browser tests.
5. **Docker test image:** multi-stage build, isolated test stack, backup and
   rollback, separate tag, verified registry publication.
6. **Verification:** original `tests/run.sh` and equivalent Dart/Flutter
   tests, security audit, benchmarking and user acceptance.

## Performance and security evaluation

Use identical synthetic calendars, Google mock, database version, hardware
and workloads. Record container compressed/uncompressed size, cold startup,
idle/peak RSS, CPU time, p50/p95 API latency, feed generation throughput,
browser startup and client CPU/memory, with sample counts and commands.
Compare OWASP ASVS/Top 10, credential handling, redirect boundaries,
encryption, CSRF and dependencies. Do not substitute guesses for results.

**Status:** The branch is a migration workspace, not a published Docker
image. A Docker tag will be supplied only after a real build and verification.

## Upstream changes after the migration baseline

As of 2026-10-27, `main` has advanced through `0.2.8-beta.14`
(13 commits beyond the `beta.4` baseline). These changes include
**two-way Google Calendar sync** (introduced in `beta.10`), additional
theme rules, event colors, and changes to the settings and update UI.
Do not silently omit them from the parity target.

The migration remains anchored at the Developer-requested `beta.4`
commit. Before claiming feature parity, review and integrate the newer
upstream changes on the migration branch with explicit regression tests.
Do not merge or modify `main` as part of that process.
