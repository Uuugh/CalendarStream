#!/bin/bash
# Gets a machine ready to run the tests (a new cloud session, or any Debian/Ubuntu box): a Postgres just for the
# suites, the app's packages, and Playwright's Chromium. Safe to run again: it starts what's stopped and skips
# what's done. Run it as root (it installs Postgres with apt when it's missing).
#
#   tests/tools/setup.sh          then: export TEST_DB_PORT=55432 (it prints this)
#
# The test Postgres: data in $TEST_PG_DIR (/srv/pg1), port $TEST_DB_PORT (55432), user ccs / testpw with
# CREATEDB. Only made-up data ever goes in it (tests/data).
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PORT="${TEST_DB_PORT:-55432}" DIR="${TEST_PG_DIR:-/srv/pg1}"
pgbin() { ls -d /usr/lib/postgresql/*/bin 2>/dev/null | sort -V | tail -1; }
if [ -z "$(pgbin)" ]; then
  echo "Installing Postgres…"
  apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq postgresql >/dev/null
fi
BIN="$(pgbin)"
if [ ! -d "$DIR/data" ]; then
  mkdir -p "$DIR" && chown postgres "$DIR"
  su postgres -c "$BIN/initdb -D '$DIR/data' -U postgres --auth-local=trust --auth-host=scram-sha-256" >/dev/null
fi
if ! su postgres -c "$BIN/pg_ctl -D '$DIR/data' status" >/dev/null 2>&1; then
  su postgres -c "$BIN/pg_ctl -D '$DIR/data' -l '$DIR/log' -o '-p $PORT' -w start" >/dev/null
fi
mkdir -p /var/run/postgresql && chown postgres /var/run/postgresql
if ! PGPASSWORD=testpw psql -qw -h 127.0.0.1 -p "$PORT" -U ccs -d postgres -c "SELECT 1" >/dev/null 2>&1; then
  su postgres -c "psql -qw -p $PORT -d postgres -c \"CREATE ROLE ccs LOGIN CREATEDB PASSWORD 'testpw'\""
fi
python3 -c "import fastapi, psycopg, icalendar, recurring_ical_events" 2>/dev/null ||
  pip install -q -r "$ROOT/requirements.txt" --break-system-packages
# Playwright: cloud sessions come with it (never install a second copy there); elsewhere, install it.
python3 -c "import playwright" 2>/dev/null || { pip install -q playwright --break-system-packages && python3 -m playwright install chromium; }
echo "Ready. Postgres on 127.0.0.1:$PORT (ccs / testpw). Now: export TEST_DB_PORT=$PORT"
