"""Postgres storage for everything the app keeps: settings/tokens, the saved login session,
events, debug captures, the activity log and sync status.

Tables are created automatically on startup.
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime

from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool

from .parser import Event

log = logging.getLogger("ccs.store")

SCHEMA = """
CREATE TABLE IF NOT EXISTS kv (
    key        text PRIMARY KEY,
    value      jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS events (
    uid         text PRIMARY KEY,
    title       text NOT NULL,
    start       text NOT NULL,
    "end"       text NOT NULL,
    all_day     boolean NOT NULL DEFAULT false,
    location    text NOT NULL DEFAULT '',
    description text NOT NULL DEFAULT '',
    synced_at   timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS debug_files (
    name         text PRIMARY KEY,
    content      bytea NOT NULL,
    content_type text NOT NULL,
    updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS activity_log (
    id    bigserial PRIMARY KEY,
    time  timestamptz NOT NULL DEFAULT now(),
    level text NOT NULL,
    msg   text NOT NULL
);
CREATE INDEX IF NOT EXISTS activity_log_time ON activity_log (time DESC);
"""

LOG_KEEP = 1000  # activity-log rows to keep


class Store:
    def __init__(self, dsn: str):
        self.pool = ConnectionPool(dsn, min_size=1, max_size=4, open=False, kwargs={"autocommit": True})

    def open(self, wait_s: int = 60):
        """Connect (retrying while the database container starts) and create tables."""
        deadline = time.time() + wait_s
        while True:
            try:
                self.pool.open(wait=True, timeout=10)
                with self.pool.connection() as c:
                    c.execute(SCHEMA)
                return
            except Exception as e:
                if time.time() > deadline:
                    raise RuntimeError(f"Can't reach the Postgres database: {e}") from e
                log.warning("Database not ready yet (%s); retrying", e)
                time.sleep(3)

    def close(self):
        self.pool.close()

    # --- key/value ---------------------------------------------------------
    def get(self, key: str, default=None):
        with self.pool.connection() as c:
            row = c.execute("SELECT value FROM kv WHERE key = %s", (key,)).fetchone()
        return row[0] if row else default

    def set(self, key: str, value):
        with self.pool.connection() as c:
            c.execute("""INSERT INTO kv (key, value) VALUES (%s, %s)
                         ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now()""",
                      (key, Jsonb(value)))

    def delete(self, key: str):
        with self.pool.connection() as c:
            c.execute("DELETE FROM kv WHERE key = %s", (key,))

    # --- events ------------------------------------------------------------
    def replace_events(self, events: list[Event]):
        """Swap in a new set of events in one transaction, so the feed never sees a half-written set."""
        with self.pool.connection() as c:
            with c.transaction():
                c.execute("DELETE FROM events")
                with c.cursor() as cur:
                    cur.executemany(
                        'INSERT INTO events (uid, title, start, "end", all_day, location, description) '
                        "VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (uid) DO NOTHING",
                        [(e.uid, e.title, e.start, e.end, e.all_day, e.location, e.description) for e in events])

    def load_events(self) -> list[Event]:
        with self.pool.connection() as c:
            rows = c.execute('SELECT title, start, "end", all_day, location, description '
                             "FROM events ORDER BY start").fetchall()
        return [Event(*r) for r in rows]

    def event_count(self) -> int:
        with self.pool.connection() as c:
            return c.execute("SELECT count(*) FROM events").fetchone()[0]

    # --- debug captures ----------------------------------------------------
    def save_debug(self, name: str, content: bytes, content_type: str):
        with self.pool.connection() as c:
            c.execute("""INSERT INTO debug_files (name, content, content_type) VALUES (%s, %s, %s)
                         ON CONFLICT (name) DO UPDATE SET content = EXCLUDED.content,
                         content_type = EXCLUDED.content_type, updated_at = now()""",
                      (name, content, content_type))

    def get_debug(self, name: str):
        with self.pool.connection() as c:
            row = c.execute("SELECT content, content_type FROM debug_files WHERE name = %s", (name,)).fetchone()
        return (bytes(row[0]), row[1]) if row else None

    def has_debug(self, name: str) -> bool:
        with self.pool.connection() as c:
            return c.execute("SELECT 1 FROM debug_files WHERE name = %s", (name,)).fetchone() is not None

    # --- activity log ------------------------------------------------------
    def add_log(self, level: str, msg: str):
        with self.pool.connection() as c:
            c.execute("INSERT INTO activity_log (level, msg) VALUES (%s, %s)", (level, msg))
            c.execute("DELETE FROM activity_log WHERE id <= (SELECT max(id) FROM activity_log) - %s", (LOG_KEEP,))

    def recent_log(self, limit: int = 100) -> list[dict]:
        with self.pool.connection() as c:
            rows = c.execute("SELECT time, level, msg FROM activity_log ORDER BY id DESC LIMIT %s",
                             (limit,)).fetchall()
        return [{"time": t, "level": lvl, "msg": m} for t, lvl, m in rows]


def iso(d: datetime | None):
    return d.isoformat() if d else None


def from_iso(s: str | None):
    return datetime.fromisoformat(s) if s else None

