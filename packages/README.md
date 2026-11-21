# Dart code: definitions and rules for all Dart code (packages/, server/, client/, SCRUM.d/dashboard/)

The port is built from `requirements/`; the laws are in `AGENTS.md`. How to read a rule row: `SCRUM.d/README.md`. Tests are in `tests/README.md`.

## Definitions

- **Layer**: `data`, `domain` or `ui`, one folder per feature.
- **Repository**: the source of truth for one kind of stored data (caching, retry, persistence).
- **Service**: wraps one external API or data source.
- **Approved dependencies**: `intl`, `flutter_localizations` and `flutter_lints`, plus the Flutter SDK's own `flutter_test` (approved by the Product Owner).
- **Scrum board**: Dart code that lives in `SCRUM.d/dashboard/`, not in `packages/`, because it is the project's Scrum board (the Product Owner's decision).

## Rules (Coder (build); IDs continue `SCRUM.d/README.md`)

| ID | What | When acted | How tested |
|---|---|---|---|
| Cb-11 | A package follows the layout at https://dart.dev/tools/pub/package-layout (public code in `lib/`, implementation in `lib/src/`, tests in `test/`) | Writing Dart | review: each file in the diff sits in the folder the page names |
| Cb-12 | Never imports from another package's `lib/src` | Writing Dart | a script lists an import of another package's `lib/src` (to be written) |
| Cb-13 | Domain never imports storage, network or the page | Writing Dart | a script lists a `domain` file that imports them (to be written) |
| Cb-14 | One public class per file, named for it in `snake_case.dart`; a closed family a `sealed class` or an enum holds (an exception hierarchy, a set of states) shares one file; small private helpers stay in the file that uses them | Writing Dart | ^ |
| Cb-15 | Every file starts with a header comment: what it holds; depends on; used by; what it reads or writes (database, network, files, the clock) | Writing Dart | a script lists a `.dart` file with no header (to be written) |
| Cb-16 | What a file needs comes in through its constructor or arguments; no reading another module's globals | Writing Dart | ^ |
| Cb-17 | A Repository never reaches into another repository; combine data one layer up. A Service holds no state | Writing Dart | ^ |
| Cb-18 | Behavior that appears twice is one shared widget or function: search for an existing one before writing a new one, and extract a shared one when a second use appears (a filter, a list column, a row, a draggable block) | Writing Dart | review: the Reviewer names each pair of near-identical code and the shared one that replaces it |
| Cb-19 | No Dart code sits outside `packages/`, `server/`, `client/` and `SCRUM.d/dashboard/`; the Scrum board follows these rules | Writing Dart | review: no Dart code sits outside those folders |

## Not yet placed

- Intro: "Flutter's structure is the model: a file stands alone and says what it needs."
- "A module per responsibility. One responsibility per file, a small interface, dependencies passed in, and its own fast test that needs no app, database or browser unless that is what it tests." ("small" and "fast" are not checkable; one responsibility per file is Cb-14.)
- "Name a class for its role: `GoogleSyncService`, `CalendarSourceRepository`."
- Open story: "Define how Dart tests run in parallel and what a run reports" (inputs: branch `paused/test-parallel`, commit 85f404b, DIA-04.c). Also in `WORKING.d/README.md`.
- The Testing section moved to `tests/README.md` and `SCRUM.d/README.md`; the "Test cell" definition is in `requirements/README.md`.
