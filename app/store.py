"""Postgres storage for everything the app keeps: settings/tokens, the downloaded calendar and
the feed built from it, events, debug captures, the activity log and sync status.

Tables are created automatically on startup.
"""
from __future__ import annotations

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
ALTER TABLE events ADD COLUMN IF NOT EXISTS source text NOT NULL DEFAULT 'ccs'; -- which calendar source it's from
ALTER TABLE events ADD COLUMN IF NOT EXISTS alarms text NOT NULL DEFAULT '';      -- 0.2.8: reminders, minutes before ("15,60")
ALTER TABLE events ADD COLUMN IF NOT EXISTS rule_color text NOT NULL DEFAULT '';  -- 0.2.8: the color its rules give it
-- What was last written to Google Calendar for each event (see gsync.py)
CREATE TABLE IF NOT EXISTS google_events (
    uid        text PRIMARY KEY,            -- CalendarStream / CCS+ event UID
    google_id  text NOT NULL,               -- the Google event ID (derived from the UID)
    hash       text NOT NULL,               -- hash of what was sent, to notice changes
    ends       text NOT NULL,               -- the event's end, so past events are left alone
    synced_at  timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE google_events ADD COLUMN IF NOT EXISTS source text NOT NULL DEFAULT 'ccs';  -- which Google calendar (destination ID)
-- 0.2.1: an event can be in several Google calendars, so the key is the event and the calendar
DO $$ BEGIN
  IF (SELECT count(*) FROM information_schema.key_column_usage
      WHERE table_name = 'google_events' AND constraint_name = 'google_events_pkey') = 1 THEN
    ALTER TABLE google_events DROP CONSTRAINT google_events_pkey;
    ALTER TABLE google_events ADD PRIMARY KEY (uid, source);
  END IF;
END $$;
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
        self.dsn = dsn
        self.pool = self._new_pool()

    def _new_pool(self) -> ConnectionPool:
        return ConnectionPool(self.dsn, min_size=1, max_size=4, open=False, kwargs={"autocommit": True})

    def open(self, wait_s: int = 60):
        """Connect (retrying while the database container starts) and create tables."""
        deadline = time.time() + wait_s
        while True:
            try:
                # A pool that didn't get a connection in time is closed and can't be opened again,
                # so each try gets a new one (0.2.8-beta.4: before, every retry failed at once).
                if self.pool.closed:
                    self.pool = self._new_pool()
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
    _COLS = ('title, start, "end", all_day, location, description, uid, origin, edited, stale, hidden, free, color, source, '
             'alarms, rule_color')

    def replace_events(self, events: list[Event], source: str = "ccs"):
        """Swap in a source's new set of events in one transaction, so the feed never sees a half-written set."""
        with self.pool.connection() as c:
            with c.transaction():
                c.execute("DELETE FROM events WHERE source = %s", (source,))
                with c.cursor() as cur:
                    cur.executemany(
                        f"INSERT INTO events ({self._COLS}) VALUES ({', '.join(['%s'] * 16)}) "
                        "ON CONFLICT (uid) DO NOTHING",
                        [(e.title, e.start, e.end, e.all_day, e.location, e.description, e.uid,
                          e.origin, e.edited, e.stale, e.hidden, e.free, e.color, source, e.alarms, e.rule_color) for e in events])

    def load_events(self, source: str | None = None) -> list[Event]:
        """All events, or one source's."""
        with self.pool.connection() as c:
            if source is None:
                rows = c.execute(f"SELECT {self._COLS} FROM events ORDER BY start").fetchall()
            else:
                rows = c.execute(f"SELECT {self._COLS} FROM events WHERE source = %s ORDER BY start", (source,)).fetchall()
        return [Event(*r) for r in rows]

    def get_event(self, uid: str) -> Event | None:
        with self.pool.connection() as c:
            r = c.execute(f"SELECT {self._COLS} FROM events WHERE uid = %s", (uid,)).fetchone()
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

    def changed_at(self, uid: str):
        """When an event was last changed on the status page (its edit, or the added event), or None."""
        with self.pool.connection() as c:
            r = c.execute("SELECT max(t) FROM (SELECT updated_at AS t FROM event_edits WHERE uid = %s "
                          "UNION ALL SELECT updated_at FROM custom_events WHERE uid = %s) x", (uid, uid)).fetchone()
        return r[0] if r else None

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

    def event_count(self, source: str | None = None) -> int:
        with self.pool.connection() as c:
            if source is None:
                return c.execute("SELECT count(*) FROM events").fetchone()[0]
            return c.execute("SELECT count(*) FROM events WHERE source = %s", (source,)).fetchone()[0]

    def forget_source(self, source: str):
        """Remove everything kept for a removed source: its events, edits, added events and files."""
        with self.pool.connection() as c:
            with c.transaction():
                uids = [r[0] for r in c.execute("SELECT uid FROM events WHERE source = %s", (source,)).fetchall()]
                c.execute("DELETE FROM events WHERE source = %s", (source,))
                if uids:
                    c.execute("DELETE FROM event_edits WHERE uid = ANY(%s)", (uids,))
                c.execute("DELETE FROM custom_events WHERE coalesce(data->>'source', 'ccs') = %s", (source,))
                names = ["source", "feed"] if source == "ccs" else [f"source:{source}", f"feed:{source}"]
                c.execute("DELETE FROM calendar_files WHERE name = ANY(%s)", (names,))

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

    # --- Google Calendar sync state ---

    def google_rows(self, source: str = "ccs") -> dict[str, dict]:
        """uid -> {google_id, hash, ends, synced_at} for the events last written to one Google calendar."""
        with self.pool.connection() as c:
            rows = c.execute("SELECT uid, google_id, hash, ends, synced_at FROM google_events WHERE source = %s",
                             (source,)).fetchall()
        return {r[0]: {"google_id": r[1], "hash": r[2], "ends": r[3], "synced_at": r[4]} for r in rows}

    def google_saved(self, uid: str, google_id: str, hash_: str, ends: str, source: str = "ccs"):
        with self.pool.connection() as c:
            c.execute("INSERT INTO google_events (uid, google_id, hash, ends, source) VALUES (%s, %s, %s, %s, %s) "
                      "ON CONFLICT (uid, source) DO UPDATE SET google_id = EXCLUDED.google_id, hash = EXCLUDED.hash, "
                      "ends = EXCLUDED.ends, synced_at = now()", (uid, google_id, hash_, ends, source))

    def google_rekey(self, old: str, new: str):
        with self.pool.connection() as c:
            c.execute("UPDATE google_events SET source = %s WHERE source = %s", (new, old))

    def google_forget(self, uid: str | None = None, source: str | None = None):
        """Forget one event's Google state (in one calendar, when `source` is given), a calendar's, or
        all of it (no arguments). `source` is the Google calendar's key (its destination's ID)."""
        with self.pool.connection() as c:
            if uid is not None and source is not None:
                c.execute("DELETE FROM google_events WHERE uid = %s AND source = %s", (uid, source))
            elif uid is not None:
                c.execute("DELETE FROM google_events WHERE uid = %s", (uid,))
            elif source is not None:
                c.execute("DELETE FROM google_events WHERE source = %s", (source,))
            else:
                c.execute("DELETE FROM google_events")

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

