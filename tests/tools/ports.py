"""tests/tools/ports.py: checks that no two suites use the same port (they run in parallel, tests/run.sh).

Usage: python3 tests/tools/ports.py        (exit 0: every port belongs to one suite; exit 1: lists the clashes)

A port here is a literal 8000-8999 number that a suite binds (uvicorn port=, PORT =, a made-up updater's
address) or connects to on 127.0.0.1. 8080 is skipped: it is the app's own default in made-up addresses, never bound.

Depends on: tests/suite_*.py, tests/mockgoogle.py. Used by: tests/suite_82.py. Reads files only.
Dart note: a lint over source files; no counterpart.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUITES = os.path.join(HERE, "..")
PORT = re.compile(r"(?:port\s*=\s*|PORT\s*=\s*|127\.0\.0\.1[:\"', ]+\s*|127\.0\.0\.1:)(8[0-9]{3})\b")
SKIP = {"8080"}


def ports_by_suite():
    found = {}
    for path in sorted(glob.glob(os.path.join(SUITES, "suite_*.py"))):
        name = os.path.basename(path)[6:-3]
        with open(path, encoding="utf-8") as f:
            text = f.read()
        found[name] = {p for p in PORT.findall(text) if p not in SKIP}
    return found


def clashes():
    owner = {}
    for suite, ports in ports_by_suite().items():
        for p in ports:
            owner.setdefault(p, []).append(suite)
    return {p: s for p, s in owner.items() if len(s) > 1}


if __name__ == "__main__":
    bad = clashes()
    for p, s in sorted(bad.items()):
        print(f"port {p} used by suites {', '.join(s)}")
    sys.exit(1 if bad else 0)
