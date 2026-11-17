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
  The current two batches cover 12–31; no claim is made about suites outside that range.
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
