# Python suite inventory — Task A

This is evidence for reconciling the frozen Python oracle into feature requirements during the Dart/Flutter
transition (`build_rules/layer-map.md`, step 2). It records what existing checks assert. It does not add behavior,
assign permanent requirement IDs, mark anything Developer-verified, or replace the feature requirement files.
Claude reviews each batch PR; the Developer decides disputed interpretations and approves the eventual spec.

## First batch: suites 12–21

Source revision: `87eadf4fa0f586889473a2598031d9e4bbe71a10`. All source links are pinned to that revision.
The ten suites contain 283 `ok()` call sites and four direct `assert` statements. Branches, loops and
exception sentinels mean call-site counts are not execution counts or counts of distinct requirements.

| Suite | Inventory | Main areas | ok call sites | Direct asserts |
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

## Second batch: suites 22–31

Source revision: `d70343f7476177a25f32827262d991cdc95c045f`. The ten suites contain 197 `ok()` call sites
and no direct `assert` statements. These are additional static observations, not runtime success claims.
The first batch remains pinned to its original revision; neither batch assigns permanent requirement IDs.

| Suite | Inventory | Main areas | ok call sites | Direct asserts |
|---|---|---|---:|---:|
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

Batch-specific setup: suite 26 requires the fresh-install database path (the harness deliberately omits legacy
source/destination seeding for it). Suite 28 uses a delayed fake credential verifier. Suite 31 checks three widths,
with some checks conditional on width or node presence, and does not explicitly test both palettes. Suite 23's
header check samples one page, while its URL/download rejection checks include paired exception sentinels.
Suite 26's final header observation uses a previously fetched week page. See the per-suite notes before deriving
requirements from these checks. All 197 source references, row keys and table structures were checked statically;
the application suites were not run locally for this inventory-only change.

## Reading and extending the inventory

- One file per suite, named `suite_NN.md`. Evidence keys `SNN-NN` are local to this inventory; do not reuse them
  as approved feature requirement IDs. Preserve keys when correcting descriptions; append new evidence keys
  if a source revision adds checks.
- Each row names a candidate owning feature, the observed behavior, and the original assertion's line. The setup
  and nearby source establish the input/state. Interpret the predicate rather than trusting historical labels.
  Several call sites combine behaviors; feature-spec reconciliation may split them without losing the evidence.
- Include every `ok()` call site and direct `assert`, including conditional paths, looped checks and deliberate
  failure sentinels. Do not count screenshots, comments, fixture construction or unasserted requests as coverage.
- Record limitations, weak predicates, skipped variants and overlaps. Keep duplicate evidence until reconciliation;
  these files do not decide which historical behavior should prevail or promise whole-feature completeness.
- A later suite batch should use the same structure and its own pinned source revision. Check main, open PRs and
  inventory branches before selecting uncovered suites, including unmerged work, to avoid duplicate batches.
  The first two batches cover 12–31; no claim is made about suites outside that range.
- Use only synthetic fixtures. Historical variable names or docstrings saying REAL do not authorize real data.

## Execution coverage and validation

This batch is a static, assertion-by-assertion inventory. The application and test code are unchanged; the suites
were not run for this documentation change. No test-success or Developer Good verdict is inferred from an
assertion's existence. Source-reference, assertion-count, Markdown-table and whitespace checks validate the
inventory itself.

At the pinned revision, [`tests/run.sh`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/run.sh)
creates isolated seeded databases, uses a fixed late-October 2026 clock when faketime is installed, and checks
FAIL output as well as exit status. All of these suites need Postgres. Browser suites also need Chromium and
Playwright. Do not run concurrent local suites against the same harness databases.

The default complete run exercises suite 12 configured and unconfigured, and suite 15 with/without PUBLIC_URL;
it omits suite 17 unless `all` is supplied. Selecting individual suite numbers does **not** add those extra
variants: suite 15 still needs its URL argument. Suite 16's import branch needs a separate isolated invocation;
the default run only exercises fresh mode. See each suite's setup section before claiming runtime coverage.

Notable evidence gaps for reconciliation: suite 16's status-message predicate is always true; suite 13's re-tracking
check uses a permissive OR; suite 20 samples renewal/retry times without proving precise boundaries; suite 21's
control-height assertion can pass for an empty selection. These are inventory notes for review, not code changes.

## Third batch: suites 32–41

Source revision: `d70343f7476177a25f32827262d991cdc95c045f`. These ten suites contain 271 `ok()` call sites
and no direct `assert` statements. These are static observations; the application suites were not run locally for
this documentation change. First-batch evidence remains pinned to its original revision.

Suites 22–31 are covered independently by [PR #44](https://github.com/Uuugh/CalendarStream/pull/44). That PR was
open and unreviewed when this batch was prepared; its files are not duplicated here. This batch can be reviewed
independently and does not assume that PR's acceptance or merge.

| Suite | Inventory | Main areas | ok call sites | Direct asserts |
|---|---|---|---:|---:|
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

Batch-specific limits: updater tests use a local stand-in or fake invocation rather than installing an image;
phone and light/dark assertions cover different subsets of scenarios; some geometry predicates can pass on an
empty selection. Static template string checks do not establish a blanket icon/shape policy. Suite 39's later
Google client-check request is not mocked by that suite and may need external connectivity. Cache assertions
check `immutable`, not exact year/day retention. See the individual notes for the exact predicates and overlaps.

All 271 new evidence keys, source anchors and table structures were checked against the pinned suite ASTs;
the README links were checked against files present in this branch. When selecting the next batch, account for
both this batch and the separate 22–31 PR, including unmerged work, to avoid duplicate inventory.

## Fourth batch: suites 42–51

Source revision: `8e0e71757323d773cd7f2ec3b9e0671381302973`. These ten suites contain 285 `ok()` call sites
and no direct `assert` statements. These are static observations; no application suites were run locally for this
inventory-only change. First/second-batch evidence keeps its original source revisions.

Suites 32–41 were reviewed in [PR #45](https://github.com/Uuugh/CalendarStream/pull/45) and merged during this run.
The exception-marker clarification was pushed to that same branch after its merge completed; this batch also
carries that single coverage-note amendment into the current tree. It explicitly treats `ok(True, ...)`
exception-handler markers as non-independent evidence, not verified requirements.
This batch continues to separate assertion existence from behavior verification and Developer approval.

| Suite | Inventory | Main areas | ok call sites | Direct asserts |
|---|---|---|---:|---:|
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

Batch-specific limits: suite 44's light/dark/phone matrix covers only part of its interaction set, and its final
Clarifications keyword map does not prove all delegated behaviors. Suite 49 needs the fixed-clock Demo.ics scenario
for external-removal checks. Suite 50 inspects workflow text rather than executing release scans. Suite 51 tests
stored invitation state and a past expiry, not a real restart or the precise seven-day lifetime. Updater services
are stand-ins and version changes are simulated. See the per-suite notes for exact limits and overlapping evidence.

All 285 new row keys, pinned line anchors and table cells were validated against source ASTs, along with local index
links. Include unmerged PRs when selecting the next batch so that covered suite numbers are not duplicated.
