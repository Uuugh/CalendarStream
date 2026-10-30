#!/bin/bash
# tests/tools/one.sh NN: run one suite the way run.sh does, but print everything except the PASS lines and
# log lines (run.sh prints only failures). Uses the same TEST_DB_* settings, defaulting to setup.sh's Postgres.
cd "$(dirname "$0")/.." || exit 1
export TEST_DB_HOST="${TEST_DB_HOST:-127.0.0.1}" TEST_DB_PORT="${TEST_DB_PORT:-55432}"
export TEST_DB_USER="${TEST_DB_USER:-ccs}" TEST_DB_PASSWORD="${TEST_DB_PASSWORD:-testpw}" PGPASSWORD="${TEST_DB_PASSWORD:-testpw}"
P=(psql -q -h "$TEST_DB_HOST" -p "$TEST_DB_PORT" -U "$TEST_DB_USER")
"${P[@]}" -d postgres -c "DROP DATABASE IF EXISTS cs$1" -c "CREATE DATABASE cs$1" 2>&1 | grep -v NOTICE
[ "$1" != 26 ] && "${P[@]}" -d "cs$1" -c "CREATE TABLE kv (key text PRIMARY KEY, value jsonb NOT NULL, updated_at timestamptz NOT NULL DEFAULT now()); INSERT INTO kv (key, value) VALUES ('sources', '[{\"id\": \"ccs\", \"type\": \"ccs\"}]'), ('destinations', '[\"feed\", \"google\"]')"
timeout 600 python3 "suite_$1.py" "cs$1" "${@:2}" 2>&1 | grep -vE "^PASS|^20[0-9]{2}-[0-9]{2}-[0-9]{2} "
