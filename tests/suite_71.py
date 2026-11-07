"""0.2.8-beta.35 (F58 checkpoint 5): app/google/readiness.py alone (R18), no app, database or network. The database
name argument is accepted and unused."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google.readiness import Readiness, ReadinessStage as S
of = lambda **k: Readiness.of(**{"configured": True, "authorized": True, "last_error": None, "last_sync": "2026-10-30T12:00:00", **k})
ok(of(configured=False, authorized=False).stage is S.NO_CLIENT, "no OAuth client: its own stage, whatever else is true")
ok(of(authorized=False).stage is S.NOT_SIGNED_IN and "Connect me" in of(authorized=False).text, "client set up but not signed in")
ok(of(last_error="HTTP 403").stage is S.API_ERROR and "HTTP 403" in of(last_error="HTTP 403").text, "signed in, Google refused: an API error, said with its reason")
ok(of(last_sync=None).stage is S.NOT_SYNCED and not of(last_sync=None).working, "signed in, no error, never synced")
ok(of().stage is S.SYNCED and of().working, "signed in and synced is the only working stage")
ok(of(last_error="x", last_sync="2026-10-30T12:00:00").stage is S.API_ERROR, "an error after a good sync still shows the error (a signed-in module whose sync fails is not 'ready')")
ok(of(last_error="").stage is S.SYNCED, "an empty error is no error")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
