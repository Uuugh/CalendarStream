# CalendarStream tests

Each `suite_NN.py` is a script that tests one version's changes (and keeps testing them later):
it starts CalendarStream against its own database, with a mock Google and made-up calendars, and
prints `PASS …` / `FAIL …` lines. Most also drive a real browser (Playwright, Chromium) to check
the page: layouts, in-place saving, pop-ups, phone widths, light and dark.

```bash
tests/run.sh            # every suite except 17 (translations, run in the Deploy: build_rules/5-deploy.md)
tests/run.sh 26 39      # some suites
tests/run.sh all        # all of them
```

`run.sh` prints only the failures and a summary, and exits 1 if anything failed. It needs a
Postgres it can create databases on (`TEST_DB_HOST`, `TEST_DB_PORT`, `TEST_DB_USER`,
`TEST_DB_PASSWORD`; defaults 127.0.0.1, 5432, ccs, testpw), `psql`, the packages in
`requirements.txt`, and Playwright with Chromium.

- `data/Demo.ics`, `data/work.ics`: the made-up schedule (Username U123456) and a made-up work
  calendar. Never put a real schedule here.
- `seed.py`: fills an install with the demo schedule, a work calendar, rules and feeds.
- `mockgoogle.py`: a stand-in for Google's sign-in and Calendar API.
- New suites take the next number; a suite's first lines say which version and requests it covers.

## Tools (tests/tools)

- `setup.sh`: gets a machine ready (a new cloud session, or any Debian/Ubuntu box): a Postgres just for the
  tests on port 55432 (ccs / testpw), the app's packages, Playwright's Chromium. Safe to run again. Then
  `export TEST_DB_PORT=55432`.
- `one.sh NN`: one suite, printing everything but the PASS lines (run.sh prints only failures).
- `demo.sh`: (re)starts `demo.py`, a demo CalendarStream on http://127.0.0.1:8177 (t / password1) filled by
  `seed.py`, for looking at the page. Restart it after changing the page.
- `shot.py [--phone] [--dark] [--url /path] out.png STEP...`: a screenshot of the demo after some steps
  (CLICK, FILL, WAIT, SHOT an element, or JavaScript); it prints the page's errors.
