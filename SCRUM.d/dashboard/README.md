# SCRUM.d/dashboard: the Scrum dashboard

A Flutter/Dart app that shows the backlog, builds the sprint by dragging and shows usage and agent progress. Its
requirements are `requirements/dashboard.md` (DSH); its tests are `tests/dashboard/`. Rules for its code are in
`packages/README.md`.

## Start it (web, with the local server)

From the repository root, one command:

```
cd SCRUM.d/dashboard && flutter pub get && flutter gen-l10n && flutter build web && dart run bin/dashboard_server.dart --progress <dir>
```

Then open the address it prints (`http://127.0.0.1:8765/`). `--progress <dir>` is the folder of the agents' `*.progress`
files (file name is the label, content `done/total`); leave it out for an empty Agent progress column. `--port <n>` picks
another port. `lib/l10n/` is generated from `requirements/messages/` and git-ignored, which is why `flutter gen-l10n`
comes before the build.

## Parts

- `bin/dashboard_server.dart`: starts the server (DSH-13).
- `lib/features/dashboard/`: `domain/` (blocks, statuses, usage), `data/` (files, issue tracker, server client),
  `server/` (the local server), `ui/` (the page).
- `lib/theme/`: the theme built from THM-02.
