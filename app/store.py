"""Postgres storage for everything the app keeps: settings/tokens, the downloaded calendar and
the feed built from it, events, debug captures, the activity log and sync status.

Tables are created automatically on startup.
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime

from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool

from .calsync import Event

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
CREATE TABLE IF NOT EXISTS calendar_files (
    name         text PRIMARY KEY,          -- 'source' (as downloaded) / 'feed' (served to Google)
    content      bytea NOT NULL,
    content_type text NOT NULL,
    sha256       text NOT NULL DEFAULT '',
    updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS debug_files (
    name         text PRIMARY KEY,
    content      bytea NOT NULL,
    content_type text NOT NULL,
    updated_at   timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE events ADD COLUMN IF NOT EXISTS origin text NOT NULL DEFAULT 'united';
ALTER TABLE events ADD COLUMN IF NOT EXISTS edited boolean NOT NULL DEFAULT false;
ALTER TABLE events ADD COLUMN IF NOT EXISTS stale  boolean NOT NULL DEFAULT false;
ALTER TABLE events ADD COLUMN IF NOT EXISTS hidden boolean NOT NULL DEFAULT false;
ALTER TABLE events ADD COLUMN IF NOT EXISTS free   boolean NOT NULL DEFAULT false;
ALTER TABLE events ADD COLUMN IF NOT EXISTS color  text NOT NULL DEFAULT '';   -- a color chosen for this event (#rrggbb)
-- What was last written to Google Calendar for each event (see gsync.py)
CREATE TABLE IF NOT EXISTS google_events (
    uid        text PRIMARY KEY,            -- CalendarStream / CCS+ event UID
    google_id  text NOT NULL,               -- the Google event ID (derived from the UID)
    hash       text NOT NULL,               -- hash of what was sent, to notice changes
    ends       text NOT NULL,               -- the event's end, so past events are left alone
    synced_at  timestamptz NOT NULL DEFAULT now()
);
-- Changes made on the status page; re-applied on top of every download from CCS+
CREATE TABLE IF NOT EXISTS event_edits (
    uid        text PRIMARY KEY,            -- United's event UID
    data       jsonb NOT NULL,              -- title, start, end, all_day, location, description, color, hidden, base
    updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS custom_events (
    uid        text PRIMARY KEY,
    data       jsonb NOT NULL,              -- title, start, end, all_day, location, description, color
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
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
                        'INSERT INTO events (uid, title, start, "end", all_day, location, description, '
                        "origin, edited, stale, hidden, free, color) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                        "ON CONFLICT (uid) DO NOTHING",
                        [(e.uid, e.title, e.start, e.end, e.all_day, e.location, e.description,
                          e.origin, e.edited, e.stale, e.hidden, e.free, e.color) for e in events])

    def load_events(self) -> list[Event]:
        with self.pool.connection() as c:
            rows = c.execute('SELECT title, start, "end", all_day, location, description, uid, '
                             "origin, edited, stale, hidden, free, color FROM events ORDER BY start").fetchall()
        return [Event(*r) for r in rows]

    def get_event(self, uid: str) -> Event | None:
        with self.pool.connection() as c:
            r = c.execute('SELECT title, start, "end", all_day, location, description, uid, '
                          "origin, edited, stale, hidden, free, color FROM events WHERE uid = %s", (uid,)).fetchone()
        return Event(*r) if r else None

    # --- edits and added events ---------------------------------------------
    def get_edits(self) -> dict:
        with self.pool.connection() as c:
            return {uid: data for uid, data in c.execute("SELECT uid, data FROM event_edits").fetchall()}

    def set_edit(self, uid: str, data: dict):
        with self.pool.connection() as c:
            c.execute("""INSERT INTO event_edits (uid, data) VALUES (%s, %s)
                         ON CONFLICT (uid) DO UPDATE SET data = EXCLUDED.data, updated_at = now()""",
                      (uid, Jsonb(data)))

    def delete_edit(self, uid: str):
        with self.pool.connection() as c:
            c.execute("DELETE FROM event_edits WHERE uid = %s", (uid,))

    def get_customs(self) -> list[dict]:
        with self.pool.connection() as c:
            rows = c.execute("SELECT uid, data FROM custom_events ORDER BY created_at").fetchall()
        return [{**data, "uid": uid} for uid, data in rows]

    def set_custom(self, uid: str, data: dict):
        with self.pool.connection() as c:
            c.execute("""INSERT INTO custom_events (uid, data) VALUES (%s, %s)
                         ON CONFLICT (uid) DO UPDATE SET data = EXCLUDED.data, updated_at = now()""",
                      (uid, Jsonb(data)))

    def delete_custom(self, uid: str):
        with self.pool.connection() as c:
            c.execute("DELETE FROM custom_events WHERE uid = %s", (uid,))

    def event_count(self) -> int:
        with self.pool.connection() as c:
            return c.execute("SELECT count(*) FROM events").fetchone()[0]

    # --- calendar files (source download + feed) ---------------------------
    def save_calendar(self, name: str, content: bytes, sha256: str = "", content_type: str = "text/calendar"):
        with self.pool.connection() as c:
            c.execute("""INSERT INTO calendar_files (name, content, content_type, sha256) VALUES (%s, %s, %s, %s)
                         ON CONFLICT (name) DO UPDATE SET content = EXCLUDED.content, sha256 = EXCLUDED.sha256,
                         content_type = EXCLUDED.content_type, updated_at = now()""",
                      (name, content, content_type, sha256))

    def get_calendar(self, name: str):
        with self.pool.connection() as c:
            row = c.execute("SELECT content, sha256, updated_at FROM calendar_files WHERE name = %s",
                            (name,)).fetchone()
        return (bytes(row[0]), row[1], row[2]) if row else None

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
    # --- Google Calendar sync state ---

    def google_rows(self) -> dict[str, dict]:
        """uid -> {google_id, hash, ends, synced_at} for events last written to Google."""
        with self.pool.connection() as c:
            rows = c.execute("SELECT uid, google_id, hash, ends, synced_at FROM google_events").fetchall()
        return {r[0]: {"google_id": r[1], "hash": r[2], "ends": r[3], "synced_at": r[4]} for r in rows}

    def google_saved(self, uid: str, google_id: str, hash_: str, ends: str):
        with self.pool.connection() as c:
            c.execute("INSERT INTO google_events (uid, google_id, hash, ends) VALUES (%s, %s, %s, %s) "
                      "ON CONFLICT (uid) DO UPDATE SET google_id = EXCLUDED.google_id, hash = EXCLUDED.hash, "
                      "ends = EXCLUDED.ends, synced_at = now()", (uid, google_id, hash_, ends))

    def google_forget(self, uid: str | None = None):
        """Forget one event's Google state, or all of it (uid=None)."""
        with self.pool.connection() as c:
            if uid is None:
                c.execute("DELETE FROM google_events")
            else:
                c.execute("DELETE FROM google_events WHERE uid = %s", (uid,))

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

