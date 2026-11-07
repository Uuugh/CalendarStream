"""F59: TrafficLog and TrafficEntry alone (R18): no app, no database, no network."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
from app.google.traffic_entry import TrafficEntry
from app.google.traffic_log import TrafficLog

log = TrafficLog(maxlen=3)
ok(log.recent() == [], "a new log is empty")
for i in range(5):
    log.record(TrafficEntry(at=float(i), account="", method="GET", url=f"/x{i}", status=200))
got = log.recent()
ok(len(got) == 3, "only the last `maxlen` entries are kept")
ok([e.url for e in got] == ["/x4", "/x3", "/x2"], "newest first")
log.clear()
ok(log.recent() == [], "Clear empties it")

e = TrafficEntry(at=1.0, account="a1b2c3", method="POST", url="https://x/token", request_headers={"a": "b"},
                 request_body="secret=s3cret", status=200, response_headers={"c": "d"}, response_body="{}", ms=12.3)
d = e.to_dict()
ok(d["account"] == "a1b2c3" and d["request_body"] == "secret=s3cret" and d["ms"] == 12.3,
   "to_dict keeps everything, unredacted, for the Beta traffic view")

print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
