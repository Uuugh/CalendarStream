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
- `docs/`: screenshots and the CalendarStream Theme Rules picture.
- `build_rules/`: how work is done here:
  - `basics.md`: words (F, I, R, ?, EOF, STOP…), versions, ground rules. Read first.
  - `deploy.md`: the Deploy steps (a–f).
  - `review.md`: what Reviewers check (Deploy steps a and b).
  - `theme.md`: how the page looks.
  - `roadmap.md`: what's planned.

## Before you push

`tests/run.sh` passes, `pip-audit -r requirements.txt` finds nothing, and the Developer's real data
appears nowhere (build_rules/basics.md, Ground rules).
