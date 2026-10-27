# CalendarStream Dart core — migration work in progress

This is an isolated, platform-independent Dart package, **not** an
installable server or Docker image. The existing Python app remains intact.

Implemented:
- Immutable event model, Python-compatible edit fingerprint and alarm ordering.
- RFC 5545 feed output: hidden events, exclusive all-day dates, UTC times,
  escaped text, UTF-8 folding, reminders and event markers.
- HTTPS source URL and credential-forwarding policy helpers (no downloader).

Run with Dart SDK 3.5+:

```sh
cd dart/calendarstream_core
dart pub get
dart analyze
dart test
```

Still missing: ICS parsing and recurrence, rules, Google API, Postgres,
scheduling, server endpoints, Flutter UI, Docker image and benchmarks.
