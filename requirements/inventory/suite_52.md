# Suite 52: Regex time limits and rule-size caps

Source: [`tests/suite_52.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure rules-module checks; no database/server/browser setup in this file. A pathological regex runs against 500 near matches; strict normalization samples one-over and exact configured limits. Timing depends on the execution environment.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S52-01 | rules | Five hundred evaluations of the pathological near-match regex complete in under one second and none match. | [L19](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L19) |
| S52-02 | rules | The ordinary fixture regex matches a title containing E1234 and not a title without it. | [L21](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L21) |
| S52-03 | rules | The wildcard pattern matches the sampled pairing title. | [L23](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L23) |
| S52-04 | rules | The default regex condition matches uppercase RDO when the pattern is lowercase. | [L25](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L25) |
| S52-05 | rules | The pathological regex test box returns a Too slow error and no results. | [L27](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L27) |
| S52-06 | rules | The malformed opening-parenthesis regex reports a missing-closing-parenthesis error. | [L28](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L28) |
| S52-07 | rules | Failure sentinel: accepting more than MAX_CONDS in strict normalization without RuleError fails. | [L35](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L35) |
| S52-08 | rules | The condition-limit RuleError has the exact configured-limit message. | [L37](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L37) |
| S52-09 | rules | Failure sentinel: accepting more than MAX_ACTIONS in strict normalization without RuleError fails. | [L39](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L39) |
| S52-10 | rules | The action-limit RuleError has the exact configured-limit message. | [L41](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L41) |
| S52-11 | rules | Strict normalization at both limits retains exactly the maximum condition/action counts. | [L43](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_52.py#L43) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 07/08 and 09/10 pair failure sentinels with exception-message checks. Exact-limit normalization does not call a save route or database despite the old label saying saved.
- Row 01 samples one pathological expression and a one-second runtime bound, not a complete ReDoS audit or a direct assertion of the internal timeout/cache mechanism. Row 04 checks default case-insensitivity, not the Aa-enabled case.
- Overlaps: suite 36 rule normalization/operators; suite 49 regex test UI.
