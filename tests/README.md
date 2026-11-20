# tests: how requirements are tested

A test verifies one or more requirements. Its test cell in the requirement row names it (what a test cell means is
defined in `requirements/README.md`). Who writes and who runs tests is defined in `SCRUM.d/README.md`.

## The rule

**A requirement is tested by the cheapest method, in agent usage and in time, that still verifies it.** No method is
required and none is banned. Pick the cheapest one that can fail when the requirement is not met. **Test:** review:
for each test, name a cheaper method and show it would not verify the row.

## Methods, cheapest first (a guide, not a limit)

1. A static check or script on files (`tests/tools/req_check.sh` is one).
2. A unit test of pure logic, with a clock the test controls and made-up data.
3. An API test against a running server and a throwaway database.
4. A comparison with stored expected output (made-up fixtures, or screenshots).
5. A browser run by an agent, for layout and behavior nothing cheaper can check.
6. A written procedure an agent follows, for a row no script can decide.

Expected outputs of the old app are captured once as made-up fixtures and compared by script (method 4), not by
running the old app each time.

## Results

Each run reports one result per requirement ID: `pass`, `fail` (with the ID, what was expected and what was found) or
`not run` (the test could not start or crashed before its checks). A row passes when every test it lists passes.

## Layout

Tests sit in `tests/<feature>/`, mirroring `requirements/<feature>.md`. Fakes and made-up data are never real data
(`AGENTS.md`). How runs are split and what a run reports to the dashboard is the first open story in `WORKING.d/README.md`.
