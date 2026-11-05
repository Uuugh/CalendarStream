#!/bin/bash
# Runs CalendarStream's test suites, each against a fresh database. Prints only the failures, then a
# summary; exits 1 if any suite failed.
#
#   tests/run.sh              every suite except 17 (translations: run in the Deploy, build_rules/5-deploy.md)
#   tests/run.sh 26 39        just these
#   tests/run.sh all          every suite, translations included
#
# Needs: Python with requirements.txt, Playwright with Chromium (pip install playwright; playwright
# install chromium), psql, and a Postgres the suites can create databases on. Where it is:
#   TEST_DB_HOST (127.0.0.1)  TEST_DB_PORT (5432)  TEST_DB_USER (ccs)  TEST_DB_PASSWORD (testpw)
# The user needs CREATEDB. Every suite uses its own database, csNN, dropped and made again each run.
#
# The clock: the made-up demo schedule (tests/data/Demo.ics) and several suites use dates in late October 2026,
# so the suites run with the clock fixed at 2026-10-30 12:00 (libfaketime, installed by tests/tools/setup.sh;
# it keeps running from then). That way those dates never lapse (R12). Set TEST_CLOCK to another moment
# ("@2026-11-20 12:00:00"), or TEST_CLOCK=real for the real clock.
cd "$(dirname "$0")"
export TEST_DB_HOST="${TEST_DB_HOST:-127.0.0.1}" TEST_DB_PORT="${TEST_DB_PORT:-5432}"
export TEST_DB_USER="${TEST_DB_USER:-ccs}" TEST_DB_PASSWORD="${TEST_DB_PASSWORD:-testpw}"
export PGPASSWORD="$TEST_DB_PASSWORD"
PSQL=(psql -q -h "$TEST_DB_HOST" -p "$TEST_DB_PORT" -U "$TEST_DB_USER")
TEST_CLOCK="${TEST_CLOCK-@2026-10-30 12:00:00}"
FAKE=()
if [ "$TEST_CLOCK" != real ] && [ -n "$TEST_CLOCK" ]; then
  if command -v faketime >/dev/null; then FAKE=(faketime -f "$TEST_CLOCK")
  else echo "warning: faketime is not installed (tests/tools/setup.sh installs it): running on the real clock" >&2; fi
fi
failed=0; ran=0
run() {   # run <suite number> <database> [argument]
  local n=$1 db=$2
  "${PSQL[@]}" -d postgres -c "DROP DATABASE IF EXISTS $db" -c "CREATE DATABASE $db" 2>&1 | grep -v NOTICE
  # Suites from before 0.2 expect an install that already had CCS+ (as an upgraded one does); 26 starts fresh.
  if [ "$n" != 26 ]; then
    "${PSQL[@]}" -d "$db" -c "CREATE TABLE kv (key text PRIMARY KEY, value jsonb NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()); INSERT INTO kv (key, value) VALUES ('sources', '[{\"id\": \"ccs\", \"type\": \"ccs\"}]'), ('destinations', '[\"feed\", \"google\"]')"
  fi
  local out; local F=("${FAKE[@]}"); [ "$n" = 45 ] && F=()   # 45 compares the database's own timestamps (real clock) with the program's
  out=$(timeout 600 "${F[@]}" python3 "suite_$n.py" "$db" "${@:3}" 2>&1)
  ran=$((ran + 1))
  if echo "$out" | grep -qE "^FAIL |Traceback"; then
    failed=$((failed + 1))
    echo "$out" | grep -E "^FAIL |Traceback|Error:" | head -8 | sed "s/^/suite $n ($db): /"; echo "$out" | grep -E "suite_[0-9]+.py\", line" | tail -2 | sed "s/^/suite $n at: /"
  fi
}
if [ "$1" = all ] || [ -z "$1" ]; then
  run 12 cs12; run 12 cs12b unconfigured; run 15 cs15 https://env.example.com; run 15 cs15b ''
  for f in suite_*.py; do
    n=${f#suite_}; n=${n%.py}
    case "$n" in 12|15) continue ;; 17) [ "$1" = all ] || continue ;; esac
    run "$n" "cs$n"
  done
else
  for n in "$@"; do run "$n" "cs$n"; done
fi
echo "$ran suite runs, $failed with failures"
[ "$failed" = 0 ]
