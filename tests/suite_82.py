"""0.2.8-beta.47 (parallel test run): no two suites share a port, tools/shard.py splits the suites fairly and
the same way every time, and the shell scripts keep LF line endings (a CRLF one fails under bash). No app,
database or network. The database name argument is accepted and unused."""
import glob, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tools"))
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
import ports, shard
bad = ports.clashes()
ok(not bad, "no two suites share a port" + ("" if not bad else f" (clashes: {bad})"))
ok(len(ports.ports_by_suite()) >= 60, "the port check reads every suite")

units = [str(n) for n in range(1, 41)]
times = {str(n): float(1 + (n * 7) % 23) for n in range(1, 41)}
bins = shard.split(units, times, 4)
ok(sorted(u for b in bins for u in b) == sorted(units), "every suite is in exactly one shard")
loads = [sum(times[u] for u in b) for b in bins]
ok(max(loads) - min(loads) <= max(times.values()), f"shards take about as long as each other ({[round(x) for x in loads]})")
ok(shard.split(units, times, 4) == bins, "the same input gives the same shards on every machine")
ok(shard.split(units, {}, 3) == shard.split(units, {}, 3) and sum(len(b) for b in shard.split(units, {}, 3)) == 40,
   "with no recorded times every suite still lands in a shard")
b1 = shard.split(["a", "b", "c"], {"a": 10.0, "b": 1.0, "c": 1.0}, 1)
ok(b1 == [["a", "b", "c"]], "one shard keeps every suite, longest first")
ok(subprocess.run([sys.executable, os.path.join(HERE, "tools", "shard.py"), "5/4", "none", "1"], capture_output=True).returncode == 2,
   "a shard past the last is refused")
for path in sorted(glob.glob(os.path.join(HERE, "*.sh")) + glob.glob(os.path.join(HERE, "tools", "*.sh"))):
    ok(b"\r" not in open(path, "rb").read(), f"tests/{os.path.relpath(path, HERE).replace(os.sep, '/')} has LF line endings")
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
