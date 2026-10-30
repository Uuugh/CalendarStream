# AGENTS.md

For any AI agent (or person) working on CalendarStream.

**CalendarStream** is a self-hosted Docker web app (FastAPI, Jinja2, Postgres) that downloads a United
Airlines CCS+ schedule and other `.ics` calendars, applies the user's rules and edits, and delivers the
result to Google Calendar (through the Calendar API) and to calendar feeds, with a status page to
manage it all. See README.md for what it does.

## Where things are

- `app/`: the app. `main.py` (shared state and orchestration), `routes/` (the status page's routes, by
  area), `calsync.py` (reading calendars, feeds), `rules.py` (the If/Then rules), `gsync.py` (Google),
  `store.py` (Postgres), `templates/` (pages, their partials, the page's script), `styles/` (the page's
  stylesheet, by area), `static/` (fonts, emoji). The code map below says which file holds what.
- `tests/`: the test suites and `run.sh`; `tests/tools/`: setup for a new machine or conversation, a demo
  server and screenshots (see tests/README.md).
- `docs/`: the README's screenshots.
- `build_rules/`: how work is done here:
  - `0-overview.md`: the steps and their commands (DASH, PLAN, BUILD, TEST, REVIEW, DEPLOY, STOP), who does
    what, the inputs (F, I, R, ?), ground rules. Read first.
  - `1-plan.md` … `5-deploy.md`: one file per step: Plan, Build, Test, Review, Deploy.
  - `theme.md`: how the page looks, with the CalendarStream Theme Rules picture beside it.
  - `roadmap.md`: what's planned.

## Code map (0.2.8-beta.20, F12)

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
| `events.py` | `/event`, `/event/…` (save, revert, restore, alarms, delete, done) |
| `history.py` | `/history/…` (undo, keep, container log) |
| `account.py` | `/welcome`, `/login`, `/unlock/{token}`, `/logout`, `/settings/login` |
| `settings.py` | `/settings/public-url`, `/settings/public-extra`, `/settings/admin-email`, `/settings/updates`, `/update/now` |
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
(dragging, refused fields, copy), `13-feeds`.

**`app/styles/NN-<what>.css`**: the page's stylesheet, sent as one file (`/assets/app.css`) in number order.
The order is the cascade's (a later rule wins a tie), so the parts are named for what they mostly hold and
never reordered: `01-base`, `02-topbar-settings`, `03-sections-editors`, `04-calendar`, `05-log-logins-forms`,
`06-sections-boxes`, `07-calendars-feeds`, `08-layout` (narrow boxes, rule lines, wide and narrow screens),
`09-spacing-print`, `10-calendar-module`, `11-modules` (the theme's modules, color box, status, Sync Now),
`12-handles`, `13-popups`, `14-rule-dialog`, `15-features` (Remove a calendar, Updates, Google API Sync,
search, import, date ranges, History…), `16-feeds`. A style for one area can live in more than one part:
grep `app/styles/` for its class. New styles go at the end of the part for their area, unless they must win
over a later part.

## Before you push

`tests/run.sh` passes, `pip-audit -r requirements.txt` finds nothing, and the Developer's real data
appears nowhere (build_rules/0-overview.md, Ground rules).
