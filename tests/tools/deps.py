#!/usr/bin/env python3
"""tests/tools/deps.py: writes build_rules/dependencies.md, the map of which app file imports which (R19), so the next file
to port to Dart is one whose prerequisites are already done. `--check` only says whether the file is current
(suite 75 runs it). Imports made inside functions are counted too; they are also the ones R19 asks to avoid.

Depends on: nothing outside the standard library. Reads: app/**/*.py. Writes: build_rules/dependencies.md.
"""
import ast, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "build_rules", "dependencies.md")


def modules():
    found = {}
    for base, dirs, files in os.walk(os.path.join(ROOT, "app")):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "templates", "styles", "static")]
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(base, f)
                rel = os.path.relpath(path, ROOT)
                name = rel[:-3].replace(os.sep, ".")
                if name.endswith(".__init__"):
                    name = name[: -len(".__init__")]
                found[name] = rel
    return found


def imports_of(name, rel, known):
    tree = ast.parse(open(os.path.join(ROOT, rel)).read())
    pkg = name if rel.endswith("__init__.py") else name.rpartition(".")[0]
    deps = set()
    for n in ast.walk(tree):
        targets = []
        if isinstance(n, ast.Import):
            targets = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            base = n.module or ""
            if n.level:
                parts = pkg.split(".")
                parts = parts[: len(parts) - (n.level - 1)]
                base = ".".join(parts + ([base] if base else []))
            subs = [f"{base}.{a.name}" for a in n.names]
            targets = subs if any(x in known for x in subs) else [base] + subs   # `from . import x` is x, not the package
        for t in targets:
            if t in known and t != name:
                deps.add(t)
    return deps


def build():
    known = modules()
    deps = {m: imports_of(m, rel, known) for m, rel in known.items()}
    users = {m: sorted(u for u, d in deps.items() if m in d) for m in known}
    # leaves first: a file after everything it depends on (cycles are listed last, marked)
    order, done, left = [], set(), set(known)
    while left:
        ready = sorted(m for m in left if deps[m] <= done)
        if not ready:
            ready = sorted(left); cyc = True
        else:
            cyc = False
        for m in ready:
            order.append((m, cyc)); done.add(m); left.discard(m)
    lines = ["# Dependencies (made by `tests/tools/deps.py`; do not edit)", "",
             "Which `app/` file imports which, leaves first: port a file when everything under **Depends on** is ported.",
             "A file marked ⟲ is in an import cycle (it can't be ported before the files it cycles with are split). Suite 75",
             "checks this file is current; rebuild it with `python3 tests/tools/deps.py`.", "",
             "| Order | File | Depends on | Used by |", "|---|---|---|---|"]
    for i, (m, cyc) in enumerate(order, 1):
        d = ", ".join(f"`{x}`" for x in sorted(deps[m])) or "nothing"
        u = ", ".join(f"`{x}`" for x in users[m]) or "nothing"
        lines.append(f"| {i} | `{known[m]}`{' ⟲' if cyc else ''} | {d} | {u} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        cur = open(OUT).read() if os.path.exists(OUT) else ""
        print("current" if cur == text else "STALE: run python3 tests/tools/deps.py")
        sys.exit(0 if cur == text else 1)
    open(OUT, "w").write(text)
    print("wrote", os.path.relpath(OUT, ROOT))
