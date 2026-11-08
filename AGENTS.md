# AGENTS.md

For any AI agent (or person) working on CalendarStream.

**CalendarStream** is a self-hosted Docker web app (FastAPI, Jinja2, Postgres) that downloads a United
Airlines CCS+ schedule and other `.ics` calendars, applies the user's rules and edits, and delivers the
result to Google Calendar (through the Calendar API) and to calendar feeds, with a status page to
manage it all. See README.md for what it does.

## Where things are

- `app/`: the app. `main.py` (shared state and orchestration), `routes/` (the status page's routes, by
  area), `calsync.py` (reading calendars, feeds; the downloads: `curl`, and CCS+'s browser-like client, `CCS_CLIENT`), `rules.py` (the If/Then rules), `gsync.py` (Google),
  `store.py` (Postgres), `templates/` (pages, their partials, the page's script), `styles/` (the page's
  stylesheet, by area), `static/` (fonts, emoji). The code map below says which file holds what.
- `tests/`: the test suites and `run.sh`; `tests/tools/`: setup for a new machine or conversation, a demo
  server and screenshots (see tests/README.md).
- `docs/`: `screenshots/` (the README's pictures) and `development/`, the Developer's own scratch work: kept on the
  Developer's machine (its contents are in `.gitignore`), never read for the app or the build.
- `build_rules/`: how work is done here:
  - `0-overview.md`: the steps and their commands (DASH, PLAN, BUILD, TEST, REVIEW, DEPLOY, STOP), who does
    what, the inputs (F, I, R, ?), ground rules. Read first.
  - `1-plan.md` … `5-deploy.md`: one file per step: Plan, Build, Test, Review, Deploy.
  - `theme.md`: how the page looks, with the CalendarStream Theme Rules picture beside it.
  - `ui_ux.md`: usability and accessibility of the page (WCAG 2.2 AA, ARIA, keyboard, focus, motion); theme.md decides exact looks.
  - `roadmap.md`: what's planned.
  - `low-findings.md`: Low review findings waiting for their code to change.
  - `build-costs.md`: what each BUILD cost, to predict the next.

## Code map (0.2.8-beta.20, F12; 0.2.8-beta.21; 0.2.8-beta.26; 0.2.8-beta.28; 0.2.8-beta.29)

Read only the part you need. Each file's first lines say what it holds.

**`app/main.py`**: everything shared, in sections headed `# --- …` (grep for them): logging, the store, the
Google accounts; calendar sources and destinations; rules and their migration; event templates; History, Undo
and Logs; Google Calendar sync and two-way sync; publishing calendars, linked and deleted events; the
background loops and start-up; the app, its middleware and error page; the status-page login (lock-outs,
known browsers, sessions, the form token); links and addresses; the month view; helpers the routes of more
than one area use; the admin e-mail; Google invites. It imports `app/routes/` last.

**`app/routes/<area>.py`**: the routes, one file per area, each with the helpers only it uses. They take
shared things from `main` by name; anything the tests replace on `main` (`download`, `run_once`, `api_on`,
`_client_ip`, `__version__`, `CSRF_TOKEN`…) they read as `core.<name>` so the replacement is seen.

| File | Routes |
|---|---|
| `page.py` | `/` and its views, `/assets/app.css` and the page script, `/ui/…` (sections, language, clock, view, time zone, theme, print choices), `/print` |
| `sources.py` | `/run`, `/verify`, `/sources/…` (add, move, remove, import, export, link), `/setup/ccs`, `/setup/interval`, `/setup/link`, `/setup/upload`, `/feed/name`, `/feed/tags` |
| `destinations.py` | `/destinations/…`, `/feed/stream`, `/subscribe/{token}`, `/calendar/{token}.ics` |
| `rules.py` | `/rules/…`, `/templates`, `/templates/add` |
| `events.py` | `/event`, `/event/…` (save, hide, revert, restore, alarms, delete, done, pick: Link to › Event's small calendar, `event-pick.html`) |
| `history.py` | `/history/…` (undo, keep, container log) |
| `account.py` | `/welcome`, `/login`, `/unlock/{token}`, `/logout`, `/settings/login` |
| `settings.py` | `/settings/administrator`, `/settings/look`, `/brand/{kind}`, `/settings/public-url`, `/settings/public-extra`, `/settings/admin-email`, `/settings/updates`, `/update/now` |
| `google.py` | `/google/…`, `/invite/{token}` |
| `status.py` | `/api/status`, `/report/data`, `/debug/{name}`, `/healthz` |

**`app/templates/index.html`**: the status page's frame: its head, the macros and values every part uses, and
one `{% include %}` per part, in page order. The parts, in `app/templates/index/`: `topbar.html` (title bar,
language, theme; it includes `settings.html`, the ☰ menu), `calendar.html`, `sources.html` (Calendars),
`feeds.html`, `rules.html` (All Rules), `templates.html` (Event Templates), `history.html`, and the pop-ups:
`report-dialog.html`, `rule-dialog.html`, `sources-dialogs.html` (remove a calendar, import conflicts),
`templates-dialog.html`, `calendar-dialogs.html` (event, Print Preview, reminders). A part sees the macros and
`{% set %}` values above its include; what a part sets stays inside it.

**`app/templates/page.js`**: the page's script, made once per language from `app/templates/js/NN-<what>.js` in
number order. The order is the script's own (listeners run in the order they were added), so a part is never
reordered: `01-base` (texts, pop-up questions, copy, login fields), `02-calendar`, `03-topbar-settings`
(preferences, (?), updates, Google setup, menus, language, theme), `04-modules` (sections, modules, colors,
Sync Now), `05-report` (Report a problem; + Add a calendar's presets), `06-rules` (the rule dialog, emoji),
`07-saving` (rows, + menus, asking first, saving in place, Cancel | Save), `08-events`, `09-remove-import`,
`10-fields` (History's filter, file and date fields, pop-ups), `11-reminders-print`, `12-handles-checks`
(dragging, refused fields, copy), `13-feeds`, `14-status-fold` (the ✓ shrink of good status words, the 24-hour fold), `15-field-notes` (0.2.8-beta.28: the note under a field while typing), `16-beta-traffic` (F59: the Beta: Google Traffic section's poll and expandable rows).

**`app/styles/NN-<what>.css`**: source modules are concatenated in filename order into one gzip-capable
`/assets/app.css` response; a source file is not a browser request. Preserve order while migrating components,
but do not append historical overrides to win the cascade. Each component owns its base, states, responsive
rules and print behavior. Shared values are tokens in `app/templates/_theme.html`.

The first consolidation establishes these owners:

| File | Owns |
|---|---|
| `19-calendar-header.css` | Calendar header, title/caret, navigation, compact/wrapped layout, responsive and print rules |
| `13-dropdowns.css` | Month, view and language menu panels and their contents |
| `19-calendar.css` | Hourly grid, key/legend (including its 5 px top margin), stretch/full-page behavior, existing settings styles |
| `07-calendars-feeds.css` | Base source-picker row, including its 1 px label spacing; `16-feeds.css` owns the feed-specific grid variant |
| `09-spacing-print.css` | Shared print visibility only; component print geometry remains with its owner |
| `13-popups.css` | Modal dialog geometry, backdrop, motion and phone full-screen behavior |
| `17-spacing.css` | Cross-component flow spacing using shared tokens; not a final override layer |

Other source modules retain their current ordering and responsibilities while future components are migrated.
For a component above, update its owner instead of adding a later override. Add exceptions in its owner's
state/media block, document any design exception in `build_rules/theme.md`, and check the rendered result.
`python3 tests/tools/csscheck.py` checks ownership and duplicate declarations in the consolidated components;
`tests/suite_44.py` checks the rendered theme in both palettes and widths. `tests/tools/theme_shots.py DIR`
captures the page, open modules, menus/dialogs, all calendar views, full-page and print mockups from the demo.

## How code is structured (R18, R19)

The Developer ports this app to Dart, as a Flutter app, one file at a time, so Flutter's structure is the model
and a file must stand alone and say what it needs.

- **A module per responsibility.** New code is a module: one responsibility per file, a small interface, its
  dependencies passed in (never reached for in `main.py`), and its own fast test that needs no app, Postgres or
  browser unless that is what it tests. `main.py` gets no new sections; code a build changes moves out of it when
  practical.
- **One class per file** (R19), named for it in `snake_case` (Flutter's one public class per file). Loose
  functions are grouped into a class or a small module first. Small private helpers stay in the file that uses them. One exception, as in Dart: a closed family that a Dart `sealed class` or an enum would hold (an exception hierarchy, a set of states) shares one file.
- **Layers, as in a Flutter feature** (`data`, `domain`, `ui`): calendar and rule logic (`domain`) never imports
  storage, network or the page (`data`, `ui`). Each feature (rules, calendars, Google, store) is one folder.
- **Every file starts with a header** (a module docstring): what it holds; **Depends on** (other files of the app, by
  path); **Used by**; what it reads or writes (database, network, files, the clock); **Dart note** (the class or
  interface it becomes, its layer, and anything Dart does differently).
- **No hidden dependencies:** no imports inside functions, no reading another module's globals, no `core.<name>`
  lookups in a new file; what a file needs comes in through its constructor or arguments.
- `build_rules/dependencies.md` maps who depends on whom, so the next file to port is one whose prerequisites are
  done; it is rebuilt when a file moves (the first one is made when the first split is built).
- Existing code is split this way when a build touches it (a plan says which areas, in which order); a split changes
  no behavior and keeps the suites green.

## Before you push

`tests/run.sh` passes, `pip-audit -r requirements.txt` finds nothing, and the Developer's real data
appears nowhere (build_rules/0-overview.md, Ground rules).
