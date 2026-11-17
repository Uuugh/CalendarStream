#!/bin/bash
# Gets a machine ready to run the tests (a new cloud session, or any Debian/Ubuntu box): a Postgres just for the
# suites, the app's packages, and Playwright's Chromium (version-pinned, I40). Safe to run again: it starts
# what's stopped and skips what's done. Run it as root (it installs Postgres with apt when it's missing).
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
# libfaketime: tests/run.sh fixes the clock at 2026-10-30 12:00 so the demo schedule's dates never lapse (R12)
command -v faketime >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq faketime >/dev/null; }
python3 -c "import fastapi, psycopg, icalendar, recurring_ical_events" 2>/dev/null ||
  pip install -q -r "$ROOT/requirements.txt" --break-system-packages
# Playwright: pinned (I40, PR #15 BR03/CI) — an unpinned `pip install playwright` let GitHub's runner silently
# pick up whatever Chromium build was newest at install time, which is how a plain `main` push started failing
# suite 67 (Escape in the rule dialog) with no app or test code changing: pip just resolved a newer Playwright,
# carrying a newer bundled Chromium, between one run and the next. Pinned here to the version suite 67 last
# passed clean against, matching what this repo's own cloud sessions already carry. Bump it only deliberately,
# with a suite 67 recheck — never by letting pip resolve "latest" again.
PLAYWRIGHT_PIN="1.63.0"
python3 -c "import PIL" 2>/dev/null || pip install -q pillow --break-system-packages    # pixdiff.py (R15)
# curl (suite 60 runs the real download path) and pypdf (suites 64 and 65 read the Print Preview PDF): a fresh Debian box
# has neither (0.2.8-beta.47). The workflow installs pypdf in its own step; this makes setup.sh complete by itself.
command -v curl >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq curl >/dev/null; }
python3 -c "import pypdf" 2>/dev/null || pip install -q pypdf --break-system-packages
installed_pw="$(python3 -m playwright --version 2>/dev/null | awk '{print $2}')"
if [ "$installed_pw" != "$PLAYWRIGHT_PIN" ]; then
  pip install -q "playwright==$PLAYWRIGHT_PIN" --break-system-packages
  python3 -m playwright install chromium
fi
# Chromium's own system libraries (libnss3, libgbm, libasound…): GitHub's runner carries them already, a fresh Debian
# or WSL box does not and the browser then dies at launch (0.2.8-beta.47). Skipped when they are all there.
if [ -z "${CI:-}" ] && [ "$(id -u)" = 0 ]; then
  python3 -m playwright install-deps chromium >/dev/null
fi
# Run as `sudo setup.sh`, Chromium lands in root's cache, but the suites run as whoever typed sudo: install it for
# that user too (0.2.8-beta.47: a WSL Debian run of the suites found no browser). Not on CI, where run.sh is root's too.
if [ -n "${SUDO_USER:-}" ] && [ "$SUDO_USER" != root ] && [ -z "${CI:-}" ]; then
  home="$(getent passwd "$SUDO_USER" | cut -d: -f6)"
  ls -d "$home"/.cache/ms-playwright/chromium_headless_shell-* >/dev/null 2>&1 ||
    su "$SUDO_USER" -c "python3 -m playwright install chromium"
fi
echo "Ready. Postgres on 127.0.0.1:$PORT (ccs / testpw). Now: export TEST_DB_PORT=$PORT"
