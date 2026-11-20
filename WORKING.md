# WORKING.md

Everything here and in `WORKING.d/` is temporary; delete an item when its work is done.

- [ ] The Product Owner answers `requirements/open-questions.md` and agrees to rows (`proposed` to `backlog`); decides the three proposed rule changes (bucket B in `build_rules/coder-review-1.md`)
- [ ] Re-run the six Coder slices and compare with the baseline (about 390 of 900 rows could not be implemented); repeat the fix, check and review cycle until the count is acceptable
- [ ] Move the live files and fix every reference to them: follow `WORKING.d/move-plan.md`
- [ ] Add the status-regression check to `req_check.sh` (see `WORKING.d/move-plan.md`)
- [ ] Retire the legacy files listed in `build_rules/README.md` (the Product Owner decides)
- [ ] Cold-agent acceptance test of the new `AGENTS.md`: where are the rules, tests and open questions?
- [ ] Story: define how Dart tests run in parallel and what a run reports (see `packages/README.md`)
- [ ] Port, story by story, with the `dart-flutter` skill
- [ ] Open: still to fix from the first Coder review: about 30 undefined terms, statements pointing at the legacy theme file, README roles and the DEF prefix, `common.md` to the line format

See `WORKING.d/` for longer temporary material (`WORKING.d/move-plan.md` is the plan for the move).
