# Dashboard round 3 brief (the Product Owner's design; send to the dashboard agent when usage allows)

Limits: worktree `CalendarStream-dashboard`, branch `dashboard`, never write main, push only `dashboard`; load and use the
`dart-flutter` and `scrum` skills and name them in every subagent brief; port 8765 is the Orchestrator's, use 8766; first
`git merge main`. Approved: placement `SCRUM.d/dashboard`, dependencies `intl`, `flutter_localizations`, `flutter_lints`.

A. Layout. The page fits the window with no page scroll; every column and block area has its own vertical scrollbar;
nothing clips. TOP 2/5: a story board: a Backlog block, then a `+` that adds a story, an epic or a sprint (ask which, and
its name). Any block can be dragged anywhere (story into epic or sprint, epic into sprint, story between sprints).
BOTTOM 3/5: three columns: Requirements (filterable, drag up into a block), Issues (filterable, a `+ issue` that writes a
GitHub issue tied to a requirement through dropdowns), Agent progress.

B. Filters. Use the shared filter requirement UIC-21 (common.md) for feature, requirement and status in both the
requirement and the issue column. Reverse round 2's DSH-04 rewording.

C. Status is where things are. Statuses: `proposed`, `backlog`, `planned`, `done` (requirements/README.md). Anything with
status `backlog` or blank is already in the Backlog block. Dragging a `proposed` requirement into Backlog sets `backlog`
in its file; adding it to a story sets `planned` and records the membership in `SCRUM.d/sprint.md`; removing it sets
`backlog`; an Accept control on a story sets its requirements `done`. The server validates every change (a status moves
up; the only move down is `planned` to `backlog`) and edits only that row's status cell, atomically. An issue's status is
one of four GitHub labels (`proposed`, `backlog`, `planned`, `done`), created if missing.

D. Remove the Sprint Goal field and the Ready, Build, Test, Review and Done columns.

E. Agent progress column (bottom right). The server reads `*.progress` files in a folder given with `--progress <dir>` (file
name is the label, content `done/total`) and shows one simple bar per agent. AT THE TOP OF THIS COLUMN, the usage chart in
the format of the old dashboard's cost graph (`WORKING.d/CalendarStream.old/build_rules/dashboard.md`, "Cost graph", and
`build-costs.md`): two meters, the 5-hour session % and the 7-day weekly %, on a 0 to 100 scale; per sprint and story the
estimate range, the before and after readings and the actual, read from `SCRUM.d/usage.md` (written by the Orchestrator,
SCRUM.d/README.md step 11); the projected after-reading (before plus estimate) for the next planned sprint, with a mark where
it ends; a value over 100 (a window reset) is drawn as a triangle on the 100% line with the real number in its tooltip;
never plot an extrapolation as a dot; the slider is neutral gray, never the blue of the data. Usage and estimate also show
on each sprint and story block.

F. Requirements (`requirements/dashboard.md`, proposed rows, one rule per row, numbers in DEF-01, a Method and a Test for
each), the message keys in all six ARB files, tests with fakes (no real gh, no write to real requirement files), the
start command in `SCRUM.d/dashboard/README.md` running `flutter pub get`, `flutter gen-l10n`, `flutter build web`, then
the server; no Parts list in `SCRUM.d/README.md`.

G. Check: `flutter analyze`, `flutter test` (tests/dashboard), `req_check.sh` once at a time; own server on 8766, headless
Chrome screenshots at 1920x1080 and 1280x720, look at them and fix clipping. Commit messages: one plain sentence ending in
brackets with the IDs, issue or folder. Progress file `done/total` in the scratch folder. Final report: what changed, how to
start it, screenshots looked at, what was not checked, what is the Product Owner's to decide.

State when stopped: round 3 stopped at 94% usage; the worktree holds uncommitted `requirements/dashboard.md` and six `.arb`
edits; resume with "keep the output file and continue with what is not yet written".

H. Outline of requirements in the requirement column (added by the Product Owner after round 3 started). The Product Owner
left it to the Orchestrator to sort into a requirement and sub-requirements; write these as `proposed` rows in
`requirements/dashboard.md` with a Method and a Test each, one rule per row:
- DSH-11: the requirement column lists each requirement with its sub-requirements beneath it as an outline.
- DSH-11.a: a sub-requirement is indented from its requirement by the sub-requirement indent in DEF-01 (3 characters; add the
  DEF-01 row).
- DSH-11.b: a requirement that has sub-requirements shows a triangle; clicking it collapses or expands that requirement's
  sub-requirements; the triangle points right when collapsed and down when expanded; a requirement without sub-requirements
  shows no triangle.
- DSH-11.c: a switch above the column collapses every requirement or expands every requirement at once.
- DSH-11.d: when the page opens every requirement is collapsed (the Orchestrator's recommendation; the Product Owner can change it).
