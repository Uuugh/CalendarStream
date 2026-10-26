# CalendarStream tests

Each `suite_NN.py` is a script that tests one version's changes (and keeps testing them later):
it starts CalendarStream against its own database, with a mock Google and made-up calendars, and
prints `PASS …` / `FAIL …` lines. Most also drive a real browser (Playwright, Chromium) to check
the page: layouts, in-place saving, pop-ups, phone widths, light and dark.

```bash
tests/run.sh            # every suite except 17 (translations, run at Deploy step d)
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
