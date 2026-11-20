#!/bin/bash
# (Re)start the demo server (demo.py) in the background. Restart it after changing the page: it caches the
# script and stylesheet. Its log: $DEMO_LOG (/tmp/cs-demo.log).
LOG="${DEMO_LOG:-/tmp/cs-demo.log}"
pkill -f '[t]ests/tools/demo.py' 2>/dev/null; sleep 1
cd "$(dirname "$0")/../.." && (python3 tests/tools/demo.py > "$LOG" 2>&1 &)
for _ in $(seq 1 30); do grep -q READY "$LOG" 2>/dev/null && break; sleep 1; done
grep -v "INFO\|NOTICE" "$LOG" | tail -5
