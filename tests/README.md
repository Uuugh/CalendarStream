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

**Parallel (0.2.8-beta.47).** `run.sh` runs the suites `TEST_JOBS` at a time (default: the lower of 4 and your
cores; `TEST_JOBS=1` is the old one-by-one run). Each suite has its own database and its own ports, so they never
meet; `tools/ports.py` (checked by suite 82) fails if two suites ever share a port, so a new suite takes a port
nobody uses (8200 + its number is the habit). A suite's output prints when the run ends, in suite order. Suites 12
and 15 run twice and so run as one chain. Never two `run.sh` at once on the same Postgres: they share the databases.

To split a run over machines, `TEST_SHARD=2/4 tests/run.sh` runs the second quarter, balanced by the times in
`tests/timings.txt`. The GitHub Tests workflow does this with 4 shards. Refresh the times after the suites change a
lot: `TEST_TIMINGS=timings.txt tests/run.sh` (run from `tests/`) rewrites the file.

**Line endings.** Shell scripts must be LF, or bash stops with `$'\r': command not found`. `.gitattributes` says
`*.sh text eol=lf`, so a checkout on Windows gives LF; a clone inside WSL's own filesystem (`~/CalendarStream`, not
`/mnt/c/...`) is also much faster. Suite 82 fails if a `.sh` here has a CR.

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
- `shots.py DIR`: the standard set of whole-page screenshots of the demo (desktop and phone, light and dark, modules
  expanded, the ☰ menu), with times hidden. Take one before a change and one after, then
  `pixdiff.py BEFORE AFTER OUT`: compares them pixel by pixel and writes each changed area, before beside after,
  to OUT; only those are looked at (R15). Exit 0 = nothing changed.
- `shot.py [--phone] [--dark] [--url /path] out.png STEP...`: a screenshot of the demo after some steps
  (CLICK, FILL, WAIT, SHOT an element, or JavaScript); it prints the page's errors.
