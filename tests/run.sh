#!/bin/bash
# Runs CalendarStream's test suites, each against a fresh database, several at a time. Prints only the
# failures (in suite order), then a summary; exits 1 if any suite failed.
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
# In parallel (0.2.8-beta.47): suites run TEST_JOBS at a time (default: the lower of 4 and the number of
# cores; TEST_JOBS=1 is the old one-by-one run). Every suite has its own database AND its own ports (tests/
# tools/ports.py checks that no two suites share one), so they never meet. A suite's output is printed when
# the whole run is done, in suite order, so a run reads the same however many jobs it used. Suites 12 and 15
# run twice (two databases, one port), so each runs as one chain, one run after the other.
#
# Splitting the run over several machines (the GitHub workflow does this):
#   TEST_SHARD=2/4            this machine runs shard 2 of 4: tools/shard.py splits the suites by their
#                             recorded time (tests/timings.txt) so the shards take about as long as each other
#   TEST_TIMINGS=path         write each suite's time (seconds) to this file, to refresh tests/timings.txt
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
if [ -z "${TEST_JOBS:-}" ]; then
  TEST_JOBS=$(nproc 2>/dev/null || echo 2); [ "$TEST_JOBS" -gt 4 ] && TEST_JOBS=4
fi
OUT=$(mktemp -d); trap 'rm -rf "$OUT"' EXIT

run() {   # run <suite number> <database> [argument]: writes its failures to stdout, and R / F lines to $OUT/<unit>.count
  local n=$1 db=$2 dberr tries=0
  # (0.2.8-beta.34, review #8 findings 1, 3) a database that can't be made stops this suite as a failure, and so does
  # any suite that exits nonzero or times out (124) without printing FAIL or a Traceback.
  # (0.2.8-beta.47) CREATE DATABASE copies template1 and Postgres refuses two copies at the very same moment, which
  # parallel suites now meet; it is tried again a few times before it counts as a failure.
  until dberr=$("${PSQL[@]}" -d postgres -c "DROP DATABASE IF EXISTS $db" -c "CREATE DATABASE $db" 2>&1); do
    tries=$((tries + 1)); [ $tries -ge 5 ] && break; sleep 1
  done
  echo R >> "$CNT"
  if [ $tries -ge 5 ]; then
    echo F >> "$CNT"; echo "suite $n ($db): FAIL database not made: $(echo "$dberr" | grep -v NOTICE | head -2 | tr '\n' ' ')"; return
  fi
  # Suites from before 0.2 expect an install that already had CCS+ (as an upgraded one does); 26 starts fresh.
  if [ "$n" != 26 ]; then
    if ! seederr=$("${PSQL[@]}" -d "$db" -c "CREATE TABLE kv (key text PRIMARY KEY, value jsonb NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()); INSERT INTO kv (key, value) VALUES ('sources', '[{\"id\": \"ccs\", \"type\": \"ccs\"}]'), ('destinations', '[\"feed\", \"google\"]')" 2>&1); then
      echo F >> "$CNT"; echo "suite $n ($db): FAIL database not seeded: $(echo "$seederr" | head -2 | tr '\n' ' ')"; return
    fi
  fi
  local out; local F=("${FAKE[@]}"); [ "$n" = 45 ] && F=()   # 45 compares the database's own timestamps (real clock) with the program's
  out=$(timeout -k 5 "${TEST_SUITE_TIMEOUT:-600}" "${F[@]}" python3 "suite_$n.py" "$db" "${@:3}" 2>&1); rc=$?
  pkill -f "python3 suite_$n.py $db" 2>/dev/null   # nothing of this suite outlives it (a timeout kills only the wrapper)
  if [ $rc -ne 0 ] || echo "$out" | grep -qE "^FAIL |Traceback"; then
    echo F >> "$CNT"
    [ $rc -ne 0 ] && echo "suite $n ($db): FAIL exit status $rc$([ $rc = 124 ] && echo ' (timed out)')"
    echo "$out" | grep -E "^FAIL |Traceback|Error:" | head -8 | sed "s/^/suite $n ($db): /"; echo "$out" | grep -E "suite_[0-9]+.py\", line" | tail -2 | sed "s/^/suite $n at: /"
  fi
}

chain() {   # chain <unit>: the unit's runs one after the other (12 and 15 run twice); its output and time go to $OUT
  local unit=$1 start=$SECONDS CNT="$OUT/$1.count"; : > "$CNT"
  case "$unit" in
    12) run 12 cs12; run 12 cs12b unconfigured ;;
    15) run 15 cs15 https://env.example.com; run 15 cs15b '' ;;
    *)  run "$unit" "cs$unit" ;;
  esac > "$OUT/$unit.out" 2>&1
  echo "$unit $((SECONDS - start))" > "$OUT/$unit.time"
}

# The units (a suite number each), in the order their output prints.
UNITS=()
if [ "$1" = all ] || [ -z "$1" ]; then
  UNITS=(12 15)
  for f in suite_*.py; do
    n=${f#suite_}; n=${n%.py}
    case "$n" in 12|15) continue ;; 17) [ "$1" = all ] || continue ;; esac
    UNITS+=("$n")
  done
else
  UNITS=("$@")
fi
if [ -n "${TEST_SHARD:-}" ]; then   # a share of them, by recorded time
  mine=$(python3 tools/shard.py "$TEST_SHARD" timings.txt "${UNITS[@]}") || { echo "bad TEST_SHARD=$TEST_SHARD" >&2; exit 2; }
  LAUNCH=($mine)          # longest first: the tail of the run is short suites
  PRINT=()
  for u in "${UNITS[@]}"; do for m in "${LAUNCH[@]}"; do [ "$u" = "$m" ] && PRINT+=("$u"); done; done
else
  LAUNCH=("${UNITS[@]}"); PRINT=("${UNITS[@]}")
  if [ -s timings.txt ] && [ "$TEST_JOBS" -gt 1 ]; then LAUNCH=($(python3 tools/shard.py 1/1 timings.txt "${UNITS[@]}")); fi
fi

for u in "${LAUNCH[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge "$TEST_JOBS" ]; do wait -n 2>/dev/null || sleep 0.2; done
  chain "$u" &
done
wait

ran=0; failed=0
for u in "${PRINT[@]}"; do
  cat "$OUT/$u.out" 2>/dev/null
  ran=$((ran + $(grep -c '^R' "$OUT/$u.count" 2>/dev/null))); failed=$((failed + $(grep -c '^F' "$OUT/$u.count" 2>/dev/null)))
done
if [ -n "${TEST_TIMINGS:-}" ]; then cat "$OUT"/*.time 2>/dev/null | sort -n > "$TEST_TIMINGS"; fi
echo "$ran suite runs, $failed with failures"
[ "$failed" = 0 ]
