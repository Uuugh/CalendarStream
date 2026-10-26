#!/bin/bash
# Runs CalendarStream's test suites, each against a fresh database. Prints only the failures, then a
# summary; exits 1 if any suite failed.
#
#   tests/run.sh              every suite except 17 (translations: run at Deploy, step d)
#   tests/run.sh 26 39        just these
#   tests/run.sh all          every suite, translations included
#
# Needs: Python with requirements.txt, Playwright with Chromium (pip install playwright; playwright
# install chromium), psql, and a Postgres the suites can create databases on. Where it is:
#   TEST_DB_HOST (127.0.0.1)  TEST_DB_PORT (5432)  TEST_DB_USER (ccs)  TEST_DB_PASSWORD (testpw)
# The user needs CREATEDB. Every suite uses its own database, csNN, dropped and made again each run.
cd "$(dirname "$0")"
export TEST_DB_HOST="${TEST_DB_HOST:-127.0.0.1}" TEST_DB_PORT="${TEST_DB_PORT:-5432}"
export TEST_DB_USER="${TEST_DB_USER:-ccs}" TEST_DB_PASSWORD="${TEST_DB_PASSWORD:-testpw}"
export PGPASSWORD="$TEST_DB_PASSWORD"
PSQL=(psql -q -h "$TEST_DB_HOST" -p "$TEST_DB_PORT" -U "$TEST_DB_USER")
failed=0; ran=0
run() {   # run <suite number> <database> [argument]
  local n=$1 db=$2
  "${PSQL[@]}" -d postgres -c "DROP DATABASE IF EXISTS $db" -c "CREATE DATABASE $db" 2>&1 | grep -v NOTICE
  # Suites from before 0.2 expect an install that already had CCS+ (as an upgraded one does); 26 starts fresh.
  if [ "$n" != 26 ]; then
    "${PSQL[@]}" -d "$db" -c "CREATE TABLE kv (key text PRIMARY KEY, value jsonb NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()); INSERT INTO kv (key, value) VALUES ('sources', '[{\"id\": \"ccs\", \"type\": \"ccs\"}]'), ('destinations', '[\"feed\", \"google\"]')"
  fi
  local out; out=$(timeout 600 python3 "suite_$n.py" "$db" "${@:3}" 2>&1)
  ran=$((ran + 1))
  if echo "$out" | grep -qE "^FAIL |Traceback"; then
    failed=$((failed + 1))
    echo "$out" | grep -E "^FAIL |Traceback|Error:" | head -8 | sed "s/^/suite $n ($db): /"
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
