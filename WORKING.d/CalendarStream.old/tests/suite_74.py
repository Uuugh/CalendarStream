"""0.2.8-beta.35 (F58 checkpoint 8): app/google/sync.py's pure helpers and the gsync facade, tested without the app,
a database or a network (R18). The database name argument is accepted and unused."""
import os, sys
from datetime import date
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google import sync, api
from app import gsync
ok(gsync.event_id is sync.event_id and gsync.event_body is sync.event_body and gsync.in_window is sync.in_window
   and gsync.SyncResult is sync.SyncResult and gsync.nearest_color_id is sync.nearest_color_id, "gsync re-exports the helpers (the same objects)")
g0 = gsync.Google(None, None, "UTC")
# (0.2.8-beta.40, F58 checkpoint 10: GoogleSync is handed the connection instead of being mixed into it)
ok(gsync.Google.__mro__[1] == api.GoogleApi and not issubclass(gsync.Google, sync.GoogleSync),
   "Google is the API connection, not also a GoogleSync by inheritance")
ok(isinstance(g0._sync_engine, sync.GoogleSync) and g0._sync_engine.api_client is g0,
   "Google holds a GoogleSync handed itself as the connection")
ok(sync.event_id("abc") == sync.event_id("abc") and sync.event_id("abc") != sync.event_id("abd") and sync.event_id("abc").isalnum(), "an event's Google ID is stable, distinct and plain letters and digits")
ok(sync.nearest_color_id("#d50000") == "11" and sync.nearest_calendar_color("#ac725e") == "1", "colors map to Google's nearest")
ok(sync.in_window is not None and callable(sync.google_fields), "the window and field helpers are there")
r = sync.SyncResult()
ok(not r.changed and isinstance(r.summary(), str), "an empty sync result changed nothing")
gsync.MAX_WRITES, old = 7, gsync.MAX_WRITES
try:
    ok(gsync.Google(None, None, "UTC").MAX_WRITES == 7, "a suite can lower the write limit on gsync (read each time)")
finally:
    gsync.MAX_WRITES = old
ok(sync.GoogleSync.MAX_WRITES == 1500, "the default limit is 1500 writes a sync")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
