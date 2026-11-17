"""tests/tools/shard.py: which suites one shard of the run takes, balanced by their recorded time.

Usage: shard.py I/N TIMINGS UNIT...   (I of N, 1-based; TIMINGS is tests/timings.txt: "<unit> <seconds>" lines)
Prints the units of shard I, longest first (the order to start them in), separated by spaces.
With 1/1 it just orders every unit longest first.

Depends on: tests/timings.txt (optional: a unit with no recorded time counts as the median).
Used by: tests/run.sh (TEST_SHARD, and the longest-first start order), .github/workflows/tests.yml (through run.sh).
Reads: the timings file. Writes: nothing. No network, database or clock.
Dart note: a pure function (list of weighted units, shard index) -> list; no state. A test-tooling script, not
part of the app, so it has no Dart counterpart.
"""
import statistics
import sys


def read_timings(path):
    times = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) == 2:
                    try:
                        times[parts[0]] = float(parts[1])
                    except ValueError:
                        pass
    except OSError:
        pass
    return times


def split(units, times, count):
    """Greedy longest-first: each unit goes to the lightest shard so far. Same answer on every machine."""
    known = [times[u] for u in units if u in times]
    default = statistics.median(known) if known else 1.0
    weight = {u: times.get(u, default) for u in units}
    order = sorted(units, key=lambda u: (-weight[u], u))
    bins = [[] for _ in range(count)]
    load = [0.0] * count
    for u in order:
        i = min(range(count), key=lambda k: (load[k], k))
        bins[i].append(u)
        load[i] += weight[u]
    return bins


def main(argv):
    spec, path, units = argv[1], argv[2], argv[3:]
    try:
        index, count = (int(x) for x in spec.split("/"))
        if not 1 <= index <= count:
            raise ValueError
    except ValueError:
        print(f"bad shard {spec!r}: wanted I/N with 1 <= I <= N", file=sys.stderr)
        return 2
    print(" ".join(split(units, read_timings(path), count)[index - 1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
