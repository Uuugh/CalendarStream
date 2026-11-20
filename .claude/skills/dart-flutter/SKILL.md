---
name: dart-flutter
description: Use when writing, reviewing or testing Dart or Flutter code for CalendarStream, the port built from the requirements folder: widgets, themes, localization, state, tests, project layout.
---

# Dart and Flutter for CalendarStream

Rules for all Dart code (structure, testing) are in `packages/README.md`; read it and `requirements/README.md` first: its rules, and above all its two laws (no duplication, no exceptions), apply to code as they do to requirements. Sources for any Dart or Flutter question, before asking the Product Owner: https://docs.flutter.dev/ and https://dart.dev/.

## What to build, and from what

- The requirements are the spec. A feature's file adds only its specifics and points at a shared row; follow the pointer to see how the shared part is built (`common.md` UIC rows for components, `theme.md` THM rows for looks, `connections.md` and `plugins.md` for modules). Never copy a shared rule into a feature.
- Every widget, class and test cites the requirement IDs it implements, in a doc comment or the test name. A test says which IDs it verifies and whether one run covers them all or one run per ID.
- Messages: no user-visible text in code. Use the generated `AppLocalizations` from the ARB files (`requirements/messages/`, moved to `lib/l10n/` at the port). A requirement cites `msg:key`; the key is the getter's name. Missing translations are listed by `flutter gen-l10n`.
- Numbers (limits, defaults, durations) come from one constants class built from the `DEF-01` table; do not write a number in a widget.

## Layout (from AGENTS.md and build_rules/layer-map.md)

- Feature-first folders: `lib/features/<feature>/{data,domain,ui}`; a connection or plugin is a feature under `connections/` or `plugins/`. Domain code never imports storage, network or UI.
- One public class per file, named in `snake_case.dart`. A repository owns one kind of stored data; a service wraps one outside API and holds no state. Dependencies are passed in, never reached for.
- Every file starts with a header comment: what it holds, what it depends on, who uses it, what it reads or writes.

## Theme and components

- All colors, fonts, shapes and sizes come from `ThemeData` built from the THM rows: THM-01 is the `TextTheme`, THM-02 the `ColorScheme` plus a `ThemeExtension` for the status colors (ok, run, warn, bad), THM-03 the `IconThemeData`, THM-04 the shapes and component themes. A component takes its look from the theme by default (UIC-17); a feature supplies only content and behavior.
- A shared component (UIC-nn) is built once, in the shared UI folder, and every feature uses it. A section is a container that holds the connections with its capability (UIC-05, CON-01.c).

## Commands (run from the repository root)

- `flutter analyze` must be clean. `flutter test` must pass. `flutter gen-l10n` after changing an ARB file.
- `tests/tools/req_check.sh` checks the requirements folder; run it before and after any change to a requirement.

## Do not

- Follow the old process files in `build_rules/` (see `build_rules/README.md`; only the files it lists as live apply).
- Add a requirement during the freeze, or change a requirement to match the old Python app (the requirement wins).
- Name an agent or a tool in a requirement.

## Tests: where they live

- **Dart tests sit beside the code they test**, in each package's `test/` folder, which mirrors `lib/`: `packages/domain/test/<feature>/`, `server/test/`, `client/test/`, and `client/integration_test/` for the thin end-to-end set. Fakes and made-up data (Demo.ics; never real data) are in `packages/testing`. The layout is the plan in `build_rules/layer-map.md`; only `packages/domain` exists so far.
- **Never in `requirements/`**, and never in the Python `tests/` folder: that is the frozen old reference and is deleted when the port is done.
- **Every test names the requirement IDs it verifies** (in its name or a tag) and declares whether one run covers them all or it runs once per ID.
- **The requirement's `test` cell** lists the tests (path and name), or `see <ID>`, or `—` while there is none. A row passes only when all its tests pass; a test that cannot run marks its rows "not run", not "failed". A requirement that depends on time uses a clock the test controls.
- `req_check.sh` does not yet check the test cells against real tests; it will when Dart tests exist.
