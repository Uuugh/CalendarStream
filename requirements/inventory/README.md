# Python suite inventory — Task A

This static inventory records the Python oracle for feature-requirement reconciliation during the
Dart/Flutter transition (`build_rules/layer-map.md`, step 2). Suites 12–81 are inventoried in 70 files.
The batch PRs were reviewed by Claude and merged; this final index is submitted separately for review.
Evidence is not an approved requirement, a Developer Good verdict, or proof of whole-feature coverage.
No application or test behavior is changed.

## Totals and evidence units

| Evidence unit | Count |
|---|---:|
| Inventoried suite files | 70 |
| `ok()` call sites | 1,663 |
| unittest assertion calls (suite 77, including exception contexts) | 33 |
| Conditional unittest failure callback (suite 77) | 1 |
| Explicit CSS failure guards (suite 78) | 3 |
| Evidence rows for the preceding four check types | 1,700 |
| Direct Python `assert` statements, recorded separately | 4 |

Counts are static source sites, not executions, distinct requirements or independently verified behaviors.
Loops, conditional paths, deliberate failure sentinels, `ok(True)` handler/skip markers and weak predicates
must be interpreted with their per-suite limitations. Suite 77 has no `ok()` calls; its 34 rows include
33 unittest assertion calls and one conditional `self.fail` callback. Suite 78 has no `ok()` calls or
Python assertions; its three rows document explicit failure guards.

## Full suite index

Each inventory retains its own pinned source revision and setup, candidate owning features, predicates,
line anchors, direct assertions, gaps and overlaps. Evidence-row counts exclude the separate direct assertions.

| Suite | Inventory | Main areas | Evidence rows | Direct asserts |
|---|---|---|---:|---:|
| 12 | [Google connection](suite_12.md) | Google client, OAuth, connection lifecycle | 41 | 2 |
| 13 | [Google sync](suite_13.md) | event mapping, deltas, full checks, recovery | 37 | 1 |
| 14 | [Interval and client checks](suite_14.md) | sources, shell, Google | 18 | 0 |
| 15 | [Public address](suite_15.md) | settings, URL validation and migration | 10 | 0 |
| 16 | [Logins](suite_16.md) | account, source credentials and migration | 34 | 0 |
| 17 | [Languages](suite_17.md) | shell/shared UI and translated messages | 18 | 1 |
| 18 | [Source and calendar UI](suite_18.md) | sources, feeds, rules, diagnostics, calendar | 24 | 0 |
| 19 | [Event editor and preferences](suite_19.md) | events, calendar, sources, Google, settings, account, feeds, rules | 53 | 0 |
| 20 | [Google notifications](suite_20.md) | watch lifecycle, notifications, two-way sync | 23 | 0 |
| 21 | [Browser controls and rules](suite_21.md) | calendar, settings, account, rules, feeds, events, sources, shell | 25 | 0 |
| 22 | [Update channels](suite_22.md) | settings, account | 15 | 0 |
| 23 | [Deploy guard regressions](suite_23.md) | settings, account, Google, feeds, sources | 28 | 0 |
| 24 | [Google guide](suite_24.md) | Google, public address, shell | 10 | 0 |
| 25 | [Email and password markup](suite_25.md) | settings, Google, shell | 12 | 0 |
| 26 | [Sources and destinations](suite_26.md) | sources, feeds, Google, rules, templates, events, calendar, shell, diagnostics | 65 | 0 |
| 27 | [Source configuration](suite_27.md) | sources, built-in rules | 13 | 0 |
| 28 | [Verification UI](suite_28.md) | sources, account, shell | 15 | 0 |
| 29 | [Dates and legacy rules](suite_29.md) | feeds, rules, sources, shell | 11 | 0 |
| 30 | [Beta versions](suite_30.md) | settings, shell | 9 | 0 |
| 31 | [Responsive layout](suite_31.md) | feeds, calendar, sources, shell, settings, history | 19 | 0 |
| 32 | [Updater requests](suite_32.md) | settings, account, shell | 13 | 0 |
| 33 | [Presets and in-place changes](suite_33.md) | sources, rules, history, diagnostics, calendar, templates, shell | 26 | 0 |
| 34 | [Help, saves and handles](suite_34.md) | shell, calendar, sources, feeds, rules | 24 | 0 |
| 35 | [Fonts, icons and feedback](suite_35.md) | shell, sources, Google, feeds, account, documentation | 38 | 0 |
| 36 | [Rules, Local and event tools](suite_36.md) | rules, sources, events, feeds, Google, calendar, account, history, shell | 58 | 0 |
| 37 | [Conflicts, links and removal](suite_37.md) | rules, events, calendar, sources, settings, shell | 53 | 0 |
| 38 | [Counts, colors and auto-update](suite_38.md) | rules, templates, history, sources, settings, calendar, feeds, shell | 20 | 0 |
| 39 | [Assets and feed validators](suite_39.md) | shell, account, sources, feeds, calendar, Google | 23 | 0 |
| 40 | [Rule palette and headers](suite_40.md) | rules, templates, sources, feeds, Google, settings, shell | 12 | 0 |
| 41 | [Module and handle edges](suite_41.md) | sources, feeds, shell | 4 | 0 |
| 42 | [Updates after redraw](suite_42.md) | settings, shell | 8 | 0 |
| 43 | [Repeated check feedback](suite_43.md) | settings, shell | 10 | 0 |
| 44 | [Theme and clarifications](suite_44.md) | shell, sources, feeds, rules, templates, events, calendar, settings, process | 58 | 0 |
| 45 | [Two-way Google changes](suite_45.md) | Google, history, calendar, rules, events | 27 | 0 |
| 46 | [Search and event layout](suite_46.md) | calendar, events, Google, feeds, settings, rules, templates, shell | 29 | 0 |
| 47 | [Shared update state](suite_47.md) | settings, Google, shell | 9 | 0 |
| 48 | [Google setup lifecycle](suite_48.md) | Google, history | 24 | 0 |
| 49 | [History and calendar lifecycle](suite_49.md) | sources, rules, history, events, calendar, Google, account, shell | 57 | 0 |
| 50 | [Deletion and release source](suite_50.md) | Google, calendar, process | 4 | 0 |
| 51 | [Feeds and invitations](suite_51.md) | feeds, Google, settings, account, rules, shell | 59 | 0 |
| 52 | [Regex limits](suite_52.md) | rules | 11 | 0 |
| 53 | [Sync, traffic and recurrence](suite_53.md) | diagnostics, Google, account, sources, process, shell | 18 | 0 |
| 54 | [Google reconnect and health](suite_54.md) | Google | 14 | 0 |
| 55 | [Google refusals and unlock](suite_55.md) | Google, feeds, history, account, shell | 48 | 0 |
| 56 | [Calendar color fallbacks](suite_56.md) | Google, history | 29 | 0 |
| 57 | [Editor and hide/show](suite_57.md) | events, history, templates, calendar, shell | 40 | 0 |
| 58 | [Links and feed defaults](suite_58.md) | events, feeds, history, rules, calendar, shell | 40 | 0 |
| 59 | [Update observers and colors](suite_59.md) | settings, process, feeds, events, shell, sources | 28 | 0 |
| 60 | [Download transports](suite_60.md) | sources | 27 | 0 |
| 61 | [Theme controls and folding](suite_61.md) | process, rules, templates, sources, shell, history | 28 | 0 |
| 62 | [Rule actions and installer source](suite_62.md) | rules, events, calendar, shell, process | 23 | 0 |
| 63 | [Meetings, defaults and power](suite_63.md) | events, Google, feeds, account, sources, rules, shell | 29 | 0 |
| 64 | [Views, PDFs and Settings](suite_64.md) | calendar, account, settings | 21 | 0 |
| 65 | [Calendar carryover](suite_65.md) | events, history, calendar, account, settings, shell | 39 | 0 |
| 66 | [Markup and installer defaults](suite_66.md) | shell, sources, settings, history, calendar, rules, events, process | 33 | 0 |
| 67 | [Status, dialogs and icon menus](suite_67.md) | shell, history, rules, events, settings, Google, calendar, documentation, process | 60 | 0 |
| 68 | [Unsigned accounts and health](suite_68.md) | Google, history, diagnostics, account | 17 | 0 |
| 69 | [Shared Google types](suite_69.md) | Google | 9 | 0 |
| 70 | [Dictionary-backed Google API](suite_70.md) | Google | 21 | 0 |
| 71 | [Readiness stages](suite_71.md) | Google | 7 | 0 |
| 72 | [Google failure classification and recovery decisions](suite_72.md) | google | 19 | 0 |
| 73 | [Google account health with a fake clock](suite_73.md) | google | 13 | 0 |
| 74 | [Sync helpers and facade composition](suite_74.md) | google | 9 | 0 |
| 75 | [Dependency-map freshness and Google module headers](suite_75.md) | process | 2 | 0 |
| 76 | [Traffic retention and serialization](suite_76.md) | diagnostics | 5 | 0 |
| 77 | [Refactor contracts using unittest](suite_77.md) | process, sources, feeds, events, rules, event_templates, settings, account, google, history | 34 | 0 |
| 78 | [CSS guard failure branches](suite_78.md) | process | 3 | 0 |
| 79 | [Calendar stretch controls and clock badge](suite_79.md) | calendar | 13 | 0 |
| 80 | [Full-page Settings markup](suite_80.md) | settings | 11 | 0 |
| 81 | [Full-page Settings and live auto-update state](suite_81.md) | settings, sources, account, shell | 13 | 0 |

## Source revisions and reviewed batches

| Suites | Pinned source revision | Batch PR |
|---|---|---|
| 12–21 | `87eadf4fa0f586889473a2598031d9e4bbe71a10` | [#42](https://github.com/Uuugh/CalendarStream/pull/42) |
| 22–31 | `d70343f7476177a25f32827262d991cdc95c045f` | [#44](https://github.com/Uuugh/CalendarStream/pull/44) |
| 32–41 | `d70343f7476177a25f32827262d991cdc95c045f` | [#45](https://github.com/Uuugh/CalendarStream/pull/45) |
| 42–51 | `8e0e71757323d773cd7f2ec3b9e0671381302973` | [#46](https://github.com/Uuugh/CalendarStream/pull/46) |
| 52–61 | `8e0e71757323d773cd7f2ec3b9e0671381302973` | [#47](https://github.com/Uuugh/CalendarStream/pull/47) |
| 62–71 | `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8` | [#48](https://github.com/Uuugh/CalendarStream/pull/48) |
| 72–81 | `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8` | [#49](https://github.com/Uuugh/CalendarStream/pull/49) |

The suite 36 exception-handler-marker clarification requested on #45 reached main through #46.
Pinned evidence is historical: it should not silently be interpreted as a check of later source changes.

## Reading and extending the inventory

- Evidence keys `SNN-NN` are local references, not permanent feature requirement IDs. Preserve keys when
  correcting descriptions. Full predicates and setup govern the interpretation, rather than historical labels.
- Keep compound predicates together unless they clearly represent separate requirements. Keep overlapping
  evidence until feature reconciliation decides ownership and disputed behavior.
- Include every check site and direct assertion, including conditional paths and deliberate failure markers.
  Screenshots, fixture construction and unasserted requests are not assertion coverage.
- Future batch PRs add only new `requirements/inventory/suite_NN.md` files. They do not edit README or any
  existing file. Put counts, suites without `ok()` calls and unusual evidence in the PR description.
- Fetch and branch from latest `origin/main`, verify the starting revision, and check merged/open PRs before
  selecting uncovered suites. Keep at most two inventory PRs open. Only synthetic/demo data is permitted.

## Validation and execution limits

Static validation checked all 1,700 row keys and pinned source anchors against the appropriate AST check
sites, all four direct assertions, Markdown table cells, and all 70 index links in suite order. This final PR
changes only this README. Application suites were not run locally for the documentation-only inventory;
GitHub runtime CI is separate evidence. In particular, the post-merge-update `suites` check for #49 passed
in [run 44164646492](https://github.com/Uuugh/CalendarStream/actions/runs/44164646492).

Setup varies: many suites need isolated Postgres databases; browser scenarios need Chromium/Playwright;
others use pure objects, fake clocks, in-memory collaborators or local servers. Fixed-clock Demo.ics scenarios,
configured/unconfigured modes, URL variants and import/fresh modes must be considered before claiming execution
coverage. Selecting an individual suite does not necessarily exercise all harness variants. See each suite's
setup section and the harness at its pinned revision. Do not run concurrent suites against shared databases.

## Open questions for feature reconciliation

- suite_82.py not inventoried: uncommitted at inventory time.
- Which candidate observations become approved feature requirements, and which feature owns overlapping
  evidence? These decisions remain with the Developer; this inventory assigns no permanent requirement IDs.
- How should weak or vacuous predicates be strengthened? Examples include suite 16's status-message check,
  suite 73's `or True`, permissive OR checks, empty-selection geometry and optional-node fallbacks.
- Which untested modes and boundaries need direct evidence? Examples include fresh/import and configured modes,
  exact retry/expiry boundaries, real restart persistence, and complete light/dark/phone interaction matrices.
- Which source-string/keyword checks and handler/skip success markers need runtime verification? These checks
  cannot independently establish the behaviors suggested by their labels. Suite 36's S36-05 marker is one example.

Per-suite coverage notes retain the specific predicates and overlaps needed to resolve these questions.
Inventory completion is reported only after this final README-only PR is merged by the Developer.
