#!/bin/bash
# tests/tools/harness_selftest.sh: tests tests/run.sh itself (review #8, the Developer's "add self test").
# Copies run.sh next to made-up suites and a fake `psql`, then injects each failure it must catch:
#   database not made · database not seeded · suite exits nonzero without printing FAIL · suite times out ·
#   a passing suite still passes · a suite's leftover child process is killed.
# Needs no Postgres. Prints PASS/FAIL per case; exits 1 if any case is wrong.
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cp "$HERE/run.sh" "$T/run.sh"; mkdir "$T/bin" "$T/tools"; cp "$HERE/tools/shard.py" "$T/tools/shard.py"
cat > "$T/bin/psql" <<'P'
#!/bin/bash
# fake psql: fails when FAKE_PSQL_FAIL (a word) appears in its arguments
[ -n "${FAKE_PSQL_FAIL:-}" ] && [[ "$*" == *"$FAKE_PSQL_FAIL"* ]] && { echo "psql: injected failure" >&2; exit 2; }
exit 0
P
chmod +x "$T/bin/psql"
echo 'import sys; sys.exit(3)' > "$T/suite_901.py"
echo 'import time; time.sleep(60)' > "$T/suite_902.py"
echo 'print("PASS made-up suite")' > "$T/suite_903.py"
cat > "$T/suite_904.py" <<'P'
import os, subprocess, sys, time
if os.environ.get("LEFTOVER"): time.sleep(300)   # the leftover: the same suite, still running after its parent finished
subprocess.Popen([sys.executable, "suite_904.py", "cs904"], env={**os.environ, "LEFTOVER": "1"}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("PASS")
P
bad=0
# check <name> <expected: pass|fail> <extra env...> -- <suite numbers>
check() {
  local name=$1 want=$2; shift 2; local envs=(); while [ "$1" != -- ]; do envs+=("$1"); shift; done; shift
  out=$(env PATH="$T/bin:$PATH" TEST_CLOCK=real "${envs[@]}" bash "$T/run.sh" "$@" 2>&1); rc=$?
  got=pass; [ $rc != 0 ] && got=fail
  if [ "$got" = "$want" ]; then echo "PASS $name"; else echo "FAIL $name: wanted $want, run.sh exited $rc: $out" | head -3; bad=1; fi
}
check "passing suite passes"                         pass A=1 -- 903
check "database not made fails"                      fail FAKE_PSQL_FAIL="CREATE DATABASE" -- 903
check "database not seeded fails"                    fail FAKE_PSQL_FAIL="CREATE TABLE" -- 903
check "nonzero exit without FAIL text fails"         fail A=1 -- 901
check "time-out fails"                               fail TEST_SUITE_TIMEOUT=2 -- 902
check "leftover process is killed"                   pass A=1 -- 904
# (0.2.8-beta.47) the parallel run: the same results as one-by-one, in less time; shards; chains
for n in 905 906 907; do echo 'import time; time.sleep(3); print("PASS slept")' > "$T/suite_$n.py"; done
echo 'print("PASS made-up twice-run suite")' > "$T/suite_12.py"
echo 'import sys; print("FAIL made-up failure"); sys.exit(1)' > "$T/suite_908.py"
checkout() {   # checkout <name> <want: text in the output> <extra env...> -- <suite numbers>
  local name=$1 want=$2; shift 2; local envs=(); while [ "$1" != -- ]; do envs+=("$1"); shift; done; shift
  out=$(env PATH="$T/bin:$PATH" TEST_CLOCK=real "${envs[@]}" bash "$T/run.sh" "$@" 2>&1)
  if echo "$out" | grep -qF -- "$want"; then echo "PASS $name"; else echo "FAIL $name: wanted '$want' in: $out" | head -3; bad=1; fi
}
checkout "two passing suites together count two"     "2 suite runs, 0 with failures" TEST_JOBS=2 -- 903 905
checkout "a failing suite among passing ones counts" "3 suite runs, 1 with failures" TEST_JOBS=3 -- 903 908 905
checkout "a suite that runs twice counts twice"      "2 suite runs, 0 with failures" TEST_JOBS=2 -- 12
checkout "a failure prints under its own suite"      "suite 908 (cs908): FAIL" TEST_JOBS=2 -- 903 908
checkout "a shard runs only its share"               "1 suite runs, 0 with failures" TEST_SHARD=1/2 -- 905 906
checkout "the other shard runs the rest"             "1 suite runs, 0 with failures" TEST_SHARD=2/2 -- 905 906
check    "a bad shard is refused"                    fail TEST_SHARD=3/2 -- 903
t0=$SECONDS; env PATH="$T/bin:$PATH" TEST_CLOCK=real TEST_JOBS=3 bash "$T/run.sh" 905 906 907 >/dev/null 2>&1; dt=$((SECONDS - t0))
if [ $dt -le 6 ]; then echo "PASS three 3-second suites with 3 jobs took ${dt}s, not 9"; else echo "FAIL three 3-second suites with 3 jobs took ${dt}s (not parallel)"; bad=1; fi
t0=$SECONDS; env PATH="$T/bin:$PATH" TEST_CLOCK=real TEST_JOBS=1 bash "$T/run.sh" 905 906 >/dev/null 2>&1; dt=$((SECONDS - t0))
if [ $dt -ge 6 ]; then echo "PASS TEST_JOBS=1 runs one by one (${dt}s)"; else echo "FAIL TEST_JOBS=1 took ${dt}s (ran in parallel)"; bad=1; fi
sleep 1
if pgrep -f "suite_904.py cs904" >/dev/null; then echo "FAIL leftover process still running"; pkill -f "suite_904.py cs904"; bad=1; else echo "PASS leftover process gone"; fi
[ $bad = 0 ] && echo "ALL PASSED" || { echo "SELFTEST FAILED"; exit 1; }
