# Dart packages: rules for all Dart code (packages/, server/, client/)

The port is built from `requirements/`; the laws are in `AGENTS.md`. Flutter's structure is the model: a file
stands alone and says what it needs.

## Structure (P18, P19, P26)

- **A module per responsibility.** One responsibility per file, a small interface, dependencies passed in, and its own
  fast test that needs no app, database or browser unless that is what it tests.
- **One public class per file** (P19), named for it in `snake_case.dart`. A closed family a `sealed class` or an enum
  holds (an exception hierarchy, a set of states) shares one file. Small private helpers stay in the file that uses them.
- **Layers** (`data`, `domain`, `ui`), one folder per feature: domain never imports storage, network or the page.
- **Within `data`** (P26): a **Repository** is the source of truth for one kind of stored data (caching, retry,
  persistence) and never reaches into another repository; combine data one layer up. A **Service** wraps one external
  API or data source and holds no state.
- **Name a class for its role**: `GoogleSyncService`, `CalendarSourceRepository`.
- **Every file starts with a header comment:** what it holds; depends on; used by; what it reads or writes (database, network, files, the clock).
- **No hidden dependencies:** no reading another module's globals; what a file needs comes in through its constructor or arguments.

## Dependencies

Add no dependency without the Product Owner's approval. **Test:** review: the diff adds no entry to a `pubspec.yaml` that the
Product Owner has not approved.

Approved by the Product Owner: `intl`, `flutter_localizations` and `flutter_lints`, plus the Flutter SDK's own `flutter_test`.

## Testing

- **Location:** tests sit beside the code, in each package's `test/` folder, mirroring `lib/`: `packages/domain/test/<feature>/`,
  `server/test/`, `client/test/`, `client/integration_test/` (thin end-to-end). Fakes and made-up data are in
  `packages/testing`. Never in `requirements/` or the Python `tests/` folder.
- **Names:** every test names the requirement IDs it verifies (in its name or a tag).
- **Once or once per ID:** a test declares whether one run covers all its IDs or it runs once per ID.
- **Per-requirement reporting:** a shared test reports a result for each requirement it verifies; a failure names the ID, expected and found.
- **Not run is not failed:** a test that cannot run (it crashes before its checks) marks its rows "not run".
- **Time:** a requirement that depends on time is tested with a clock the test controls; no test waits real time.
- **Test cell** (in a requirement row): a list of tests (path and name), `see <ID>`, or `—` while there is none. A row
  passes only when all its tests pass.

## Open stories

- **Define how Dart tests run in parallel and what a run reports.** Inputs: the parked branch `paused/test-parallel`
  (commit 85f404b) and requirement DIA-04.c.
