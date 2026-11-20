"""0.2.8-beta.18 tests (review #2, Rules): a typed regex or wildcard pattern can't stall the sync (it gets a time limit
per event; once over it, it matches nothing for the rest of that run), and the regex test box says it's too slow
(#2.1); a rule with more conditions or actions than allowed is refused when saved, saying why, never cut off (#2.2)."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from app import rules as R
fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)

# #2.1: a pathological regex, against many long near-matches
cond = R._cond({"type": "text", "op": "regex", "value": "(a|aa)+$"})
test = R._compile([cond])
info = {"title": "a" * 60 + "!", "text": "a" * 60 + "!"}
t = time.time()
hits = [test(None, info) for _ in range(500)]
took = time.time() - t
ok(took < 1.0 and not any(hits), f"#2.1: (a|aa)+$ on 500 long near-matches: no match, {took:.2f} s (not a stall)")
good = R._compile([R._cond({"type": "text", "op": "regex", "value": r"E\d{4}"})])
ok(good(None, {"title": "Trip E1234", "text": ""}) and not good(None, {"title": "Trip", "text": ""}), "#2.1: an ordinary regex still matches")
pat = R._compile([R._cond({"type": "text", "op": "pattern", "value": "*E####"})])
ok(pat(None, {"title": "Pairing E1234", "text": ""}), "#2.1: a wildcard pattern still matches")
ci = R._compile([R._cond({"type": "text", "op": "regex", "value": "rdo"})])
ok(ci(None, {"title": "RDO", "text": ""}), "#2.1: a regex ignores capitals unless Aa is on")
box = R.test_text("(a|aa)+$", "regex", False, ["a" * 60 + "!"])
ok(box["error"].startswith("Too slow") and not box["results"], f"#2.1: the test box says it's too slow ({box['error'][:40]})")
ok(R.pattern_error("(", "regex").startswith("Not a valid regex: missing )"), "#2.1: a broken regex still says what's wrong")

# #2.2: over the limits
rule = lambda n_conds, n_acts: {"title": "x", "apply": "all",
                                "conds": [{"type": "text", "op": "contains", "value": f"v{i}"} for i in range(n_conds)],
                                "actions": [{"type": "emoji", "emoji": "✈️"} for _ in range(n_acts)]}
try:
    R.normalize(rule(R.MAX_CONDS + 1, 1), strict=True); ok(False, "#2.2: 13 conditions refused")
except R.RuleError as e:
    ok(str(e) == f"Up to {R.MAX_CONDS} conditions in a rule.", f"#2.2: 13 conditions refused, saying why ({e})")
try:
    R.normalize(rule(1, R.MAX_ACTIONS + 1), strict=True); ok(False, "#2.2: 7 actions refused")
except R.RuleError as e:
    ok(str(e) == f"Up to {R.MAX_ACTIONS} actions in a rule.", f"#2.2: 7 actions refused, saying why ({e})")
r = R.normalize(rule(R.MAX_CONDS, R.MAX_ACTIONS), strict=True)
ok(r and len(r["conds"]) == R.MAX_CONDS and len(r["actions"]) == R.MAX_ACTIONS, "#2.2: exactly at the limits is saved")
print("FAILED:", fails) if fails else print("ALL PASSED")
