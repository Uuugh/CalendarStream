# Dashboard sprint review (branch `dashboard`, `git diff main...dashboard`, 7 commits, 77 files, cold, read-only)

Method: read the diff against requirements/README.md rules 1-15, packages/README.md, tests/README.md, dart-flutter skill,
AGENTS.md laws, SCRUM.d/README.md. Did not run req_check.sh, flutter analyze or flutter test.

## Findings, most serious first
1. **DSH-04.c / DSH-05.a / DSH-03.c (bug)** `ui/list_filter_bar.dart:68` shows All when the filter value is not among the
   choices, but `dashboard_page.dart:43-44` still applies it. With no `backlog` requirement (or no open issue) the dropdown
   says All while the list is empty/filtered. Fix: add the filter's current value to the choices, or start from All when
   absent; add a test.
2. **DSH-08.c (known gap, confirmed)** a new issue entered as closed is hidden by the default open filter
   (`dashboard_page.dart:44,87`); the row says it "appears in the issue list". Fix: after Save, set the issue status filter
   to All (or to the new issue's status); add a test (the existing test at new_issue_test.dart:281 only uses an open issue).
3. **DSH-08.b (known gap, confirmed)** the Status dropdown has a blank first item (`new_issue_dialog.dart:83`, used for
   status at :123); the row says it offers open and closed. Picking blank silently means open. Fix: no blank item for
   status; test at new_issue_test.dart:203 never checks for it.
4. **DSH-08.d / DSH-08.c** `issue_service.dart:42-50`: create then close are two calls. If close fails the issue exists but
   the form says it failed and stays filled; Save again makes a duplicate. Fix: create with the status in one step
   (or, on a close failure, report the number and keep the issue; add a test).
5. **DSH-09.c / DSH-06.c / THM-02 (known gap, confirmed)** `usage_colors.dart:10` uses `scheme.error`; THM-02.j `warn`
   (and ok/run/bad, THM-02.h-k) are the status tokens. No theme or ThemeExtension is built: `main.dart:20` uses the default
   MaterialApp, `stage_colors.dart` derives colors from the default scheme, and `assignee_colors.dart:10-21` hard-codes
   `Colors.*` (dart-flutter: all colors from ThemeData). Fix: a ThemeExtension with warn (or record a decision that THM
   is not built yet and cite it), assignee palette from the theme.
6. **DSH-01 / DSH-01.a (web)** the row says web and desktop. `main.dart:8-31` always uses `DiskFileAccess` and
   `ProcessCommandRunner` (dart:io); on web nothing can be read and the header comment promises an error that is not
   built (the page shows the raw exception via `Text('$_error')`, `dashboard_page.dart:154`). Fix: either the requirement
   says desktop first (Product Owner decision) or add a web path; no test covers DSH-01 itself (cell `—`).
7. **DSH-04 / rule 5 / UIC-21** the row says "built on the shared filter (UIC-21)". UIC-21 is a multi-select filter on the
   shared dropdown (UIC-12) with saved choices and an active indicator; `list_filter_bar.dart` is its own single-select
   filter and the shared UI folder has no UIC component yet. Fix: reword the row (the dashboard has its own filter and
   says so) or build on UIC-21; the Product Owner decides.
8. **DSH-02.c data loss** `sprint_repository.dart:34-47,72-97`: a `##` heading inside the Review or Retrospective text starts
   a new section and the lines under it are lost on the next save; text before the Goal line and a story row whose stage
   does not parse (`:51-52`) are also dropped, and `# Sprint` is rewritten. SCRUM.d/README.md:92,94 has the Orchestrator
   write free text into those sections. Fix: keep unknown sections and unparsed rows verbatim (or refuse to save); test it.
9. **DSH-01.d / rule 14** not every shown text is a key: requirement statuses show raw (`dashboard_page.dart:116,121`),
   raw error text (`:154`), the `-` and `|` joins (`:142`), and issue-form blank item. Fix: keys for the statuses; the
   status dropdown for requirements shows `backlog`/`proposed` untranslated. Also DSH-01.d, DSH-09.b have test `—`.
10. **Rule 13 / tests/README / skill** test cells name test files only, not test names; one file serves up to 20 rows so a
    failure does not name its row (see DSH-04.* all share two files). DSH-01.d and DSH-09.b are `—` with "Product Owner" in
    the evidence column (that column is for Python-suite keys, rule "Line format"). Fix: list `file: test name` per row;
    DSH-09.b is a definition, move it to Terms (rule 7) and DSH-01.d to a req_check count.
11. **Rules 3 and 7 in dashboard.md** DSH-04 "three filters", DSH-09.b "one percent of the 5-hour allowance" are numbers
    outside DEF-01 (req_check lists them); DSH-08.c, DSH-07.a, DSH-05.b hold several rules in one row (Save off, create,
    label, line, list). DSH-03.a names a file list in the row (ok), no history found. Fix: split rows; DEF-01 row for the allowance.
12. **Limits / DEF** `issue_service.dart:21` hard-codes `--limit 200` (rules 3, 9; dart-flutter: numbers from a constants
    class); the list silently truncates. Fix: a named constant plus a requirement or DEF-01 row, and say when truncated.
13. **Known gap: no Cancel in the New issue form** (`new_issue_dialog.dart:131-137`, only Save; escape/barrier dismiss
    works). Not a DSH row; `cancel` key exists. Fix: add a Cancel using msg:cancel if the Product Owner wants it.
14. **Tests** real-time waits in `dashboard_page_test.dart:55-58` (packages/README "no test waits real time"); the
    DSH-01.a "no token" check is a string search for words in arguments, not proof (acceptable, weak).

## Files touched outside SCRUM.d/dashboard, tests/dashboard, requirements/dashboard.md
- `.gitignore` +2 (un-ignore the data folder): needed, justified. - `SCRUM.d/README.md` (Sprint line, new Parts list):
  justified (law: folder README indexes parts), but its Sprint line is behind main (main edited neighbouring lines; merge check).
- `requirements/README.md` (DSH prefix, index): justified. - `requirements/open-questions.md` removes one trailing blank
  line: unrelated, harmless, revert it. - `requirements/messages/app_*.arb` x6: dsh keys justified, BUT unrelated edits to
  existing keys: `default` renamed `defaultLabel` and placeholder `{new}` renamed `{newValue}` in changePartTime/Title/Location
  (en, de, es, fr, nl, pt). Needed for gen-l10n to compile (Dart keywords) but it changes shared messages: check no
  requirement cites `msg:default` (grep found none) and that the Python app does not read the ARB (not checked). Product Owner to confirm.
- AGENTS.md table of contents not updated for `SCRUM.d/dashboard/` (a Dart app inside the process folder, outside
  `packages/`, `server/`, `client/`; packages/README.md assumes those homes): Product Owner decides placement.

## Dependencies added (needs Product Owner approval, packages/README)
SCRUM.d/dashboard/pubspec.yaml: flutter (sdk), flutter_localizations (sdk), `intl: any` (unpinned; pin it), dev flutter_test
(sdk), flutter_lints ^6.0.0. tests/dashboard/pubspec.yaml: flutter_test, path dependency on the app. Two pubspec.lock files committed.

## gh calls (`issue_service.dart`)
Argument lists, no shell: titles/bodies cannot inject commands (a title starting `-` is a separate argv element after
`--title`, safe). Reads `gh issue list --state all --limit 200 --json ...`; writes `issue create` (labels `issue` and
`feature:<x>` that must already exist, else create fails with the reason; unverified) and `issue close N`. N comes from
the URL gh prints (digits only). No token in code or tests; stderr is shown to the user as the reason (could echo paths).

## Per row
Implemented as written: DSH-02.a-d (except finding 8), 03, 03.a-c, 04.a/b/d, 05, 05.b/c, 06 to 06.d (colors: finding 5),
07.a-d, 08, 08.a, 08.d, 09, 09.a, 09.c (colour: finding 5), 09.d, 01.b, 01.c. Not as written: DSH-01 (6), 01.d (9), 04 (7),
04.c (1), 05.a (1), 08.b (3), 08.c (2, 4), 09.b (no test).
Layers: domain imports no data/ui; one public class per file (sealed DragPayload shares a file, allowed); headers present.
sprint.md read/write matches SCRUM.d/README.md:26 (a file that is deleted at the end reads as an empty sprint) except finding 8.

## Not checked
flutter analyze/test/gen-l10n runs; req_check.sh; the 94 tests passing; translation quality (es, fr, nl, pt); the web build;
that labels `issue` and `feature:*` exist in the tracker; Python app use of the renamed ARB keys; layout look; main's newer commits merging cleanly.
