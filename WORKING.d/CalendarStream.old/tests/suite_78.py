"""CSS ownership and duplicate-declaration guard for consolidated components; no app or database."""
import importlib.util
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('csscheck', HERE / 'tools/csscheck.py')
csscheck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csscheck)
findings = csscheck.check()
if findings:
    print('FAIL ' + '\nFAIL '.join(findings)); sys.exit(1)
# Prove the lint guard detects regressions, including duplicates spread across rules and source files.
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory); styles = root / 'app/styles'; styles.mkdir(parents=True)
    (styles / '19-calendar-header.css').write_text('.calhead{gap:8px;gap:9px}.calhead{gap:10px}')
    (styles / '99-late.css').write_text('.calhead{margin:1px}')
    found = csscheck.check(root)
    if len(found) != 3:
        print('FAIL duplicate/ownership fixtures not detected:', found); sys.exit(1)
    (styles / '99-late.css').unlink()
    (styles / '19-calendar-header.css').write_text('.calhead{gap:8px}@media print{.calhead{gap:0}}')
    if csscheck.check(root):
        print('FAIL intentional media states rejected'); sys.exit(1)
print('ALL PASSED: component ownership, duplicate declarations and media-state lint contracts')
