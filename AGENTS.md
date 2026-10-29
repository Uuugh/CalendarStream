# AGENTS.md

For any AI agent (or person) working on CalendarStream.

**CalendarStream** is a self-hosted Docker web app (FastAPI, Jinja2, Postgres) that downloads a United
Airlines CCS+ schedule and other `.ics` calendars, applies the user's rules and edits, and delivers the
result to Google Calendar (through the Calendar API) and to calendar feeds, with a status page to
manage it all. See README.md for what it does.

## Where things are

- `app/`: the app. `main.py` (routes and orchestration), `calsync.py` (reading calendars, feeds),
  `rules.py` (the If/Then rules), `gsync.py` (Google), `store.py` (Postgres), `templates/` (pages,
  `page.js`), `static/` (stylesheet, fonts).
- `tests/`: the test suites and `run.sh` (see tests/README.md).
- `docs/`: the README's screenshots.
- `build_rules/`: how work is done here:
  - `0-overview.md`: the steps and their commands (MENU, PLAN, BUILD, TEST, REVIEW, DEPLOY, STOP), who does
    what, the inputs (F, I, R, ?), ground rules. Read first.
  - `1-plan.md` … `5-deploy.md`: one file per step: Plan, Build, Test, Review, Deploy.
  - `theme.md`: how the page looks, with the CalendarStream Theme Rules picture beside it.
  - `roadmap.md`: what's planned.

## Before you push

`tests/run.sh` passes, `pip-audit -r requirements.txt` finds nothing, and the Developer's real data
appears nowhere (build_rules/0-overview.md, Ground rules).
