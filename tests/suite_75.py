"""0.2.8-beta.35 (F58 checkpoint 9): build_rules/dependencies.md is current (R19), and every app/google file has the
header R19 asks for (Holds / Depends on / Used by / Reads/writes / Dart note). No app, database or network. The
database name argument is accepted and unused."""
import glob, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
r = subprocess.run([sys.executable, os.path.join(HERE, "tools", "deps.py"), "--check"], capture_output=True, text=True)
ok(r.returncode == 0, "build_rules/dependencies.md is current (" + (r.stdout or r.stderr).strip() + ")")
for path in sorted(glob.glob(os.path.join(ROOT, "app", "google", "*.py"))):
    name = os.path.basename(path)
    if name == "__init__.py":
        continue
    head = open(path).read().split('"""')[1]
    missing = [k for k in ("Holds:", "Depends on:", "Used by:", "Reads/writes:", "Dart note:") if k not in head]
    ok(not missing, f"app/google/{name} has its R19 header" + (f" (missing {missing})" if missing else ""))
print(f"{fails} failed" if fails else "ALL PASSED"); sys.exit(1 if fails else 0)
