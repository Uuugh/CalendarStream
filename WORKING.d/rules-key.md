# Key: requirements rules, old to new numbers (delete when every link is fixed)

Rules 1 and 2 were removed at the Product Owner's decision (they restated the laws of `AGENTS.md`). The rest moved up by two.

| Old | New |
|---|---|
| 1, 2 | removed (the laws, `AGENTS.md`) |
| 3 | 1 |
| 4 | 2 |
| 5 | 3 |
| 6 | 4 |
| 7 | 5 |
| 8 | 6 |
| 9 | 7 |
| 10 | 8 |
| 11 | 9 |
| 12 | 10 |
| 13 | 11 |
| 14 | 12 |
| 15 | 13 |

The removed words, kept here:

1. **Law: no duplication. Say it once.** A rule is written in one place and referenced everywhere else. Before adding a row, search the folder for the same rule in other words. **Test:** `req_check.sh` lists identical statements; review: name the one row that owns the rule, and every other row only links to it.
2. **Law: no exceptions.** If a rule has an exception, the requirement is wrong: change it so it holds for every case, or give the different case its own requirement. A row never says "except", "never for" or "only when X is not". A new kind of thing (a connection, a component) follows the existing rules and does not get a special case. **Test:** `req_check.sh` lists exception wording (a condition that says when something happens is fine; an exception to another rule is not); review: would the rule hold unchanged for the next new connection or component?

`tests/tools/req_check.sh` printed these numbers in its messages; they are updated with the move.

## Key: Orchestrator rules, old to new (fix links, then delete)

| Old | New |
|---|---|
| Or-01 | Or-01, Or-01.a, Or-01.b, Or-01.c |
| Or-02 | Or-03 |
| Or-17 | Or-02.e.b |
| Or-18 | Or-02.f |
| Or-19 | Or-02.e.c |
| Or-21 | Or-02.c |
| Or-27 (marks, breaking requests) | Or-02.d, Or-02.e, Or-02.e.a, Or-02.e.b, Or-02.e.c; Or-27 keeps only the question rule |
