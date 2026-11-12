# Low findings

Read when planning a version (1-plan.md), to see which waiting cleanups touch the code that version changes.

Low findings from whole-app reviews (4-review.md), done when that code is next changed. Each: the audit issue, #N,
file:line, what to do. Taken off when done.

PR #15 (build-rules/theme/Dashboard governance review, Accepted by independent review Nov 11; BR01, BR02, BR11
and I40 already built as BUILD R — not listed here):

- **BR03** `2-build.md:31-43,74,93`, `.github/workflows/tests.yml:7` — define explicit validation/publication
  lanes (docs-only, application, UI, release); state plainly that Tests only runs on pushes to main, pull
  requests and manual dispatch, not every arbitrary branch push.
- **BR04** `4-review.md:17-22` — the review-area table still names `app/rules.py`, `app/calsync.py`, `app/main.py`
  for logic AGENTS.md shows now extracted to `app/rule_engine/`, `app/calendars/`, `app/services/`, `app/runtime/`.
  Point areas at the module families instead of stale example paths.
- **BR05** `4-review.md:60-61,73` — allow static control/data-flow evidence (not only a reproduced failing test)
  for a High/Medium finding, and let a newly discovered serious finding be escalated after round one instead of
  being unable to surface at all.
- **BR06** `dashboard.md:15-16` — Inputs Status items (F1, I21, R18…) are literally the `tests` collection's
  document IDs with no build-scoping; confirmed live, not just in the spec (`ArtifactData`'s `col.doc(id)`, the
  Dashboard's own script). Needs an immutable ID separate from the display label before two builds can safely
  reuse F1.
- **BR07** `dashboard.md:8-9,34-35` — define a conflict/recovery contract for a verdict arriving mid-edit (read →
  edit → publish race); record the artifact/provider and collection schema (confirmed live: `ArtifactData`,
  collection `tests`, doc shape `{verdict, comment, at}`).
- **BR08** `dashboard.md:26`, `2-build.md:24`, `build-costs.md:27` — give measured/derived/forecast cost-graph
  series distinct labels and provenance; forecasts never render as measured dots.
- **BR09** `2-build.md:19,103-106` — an explicit skip for "no usage reading given" instead of "waits, then
  proceeds anyway" with no stated trigger; a handoff should report the receiver's actual checkout state rather
  than assuming "not on disk" unconditionally.
- **BR10** `theme.md:7,400` — drop the untracked `.pdf` claim (only the two `.png` Theme Rules pictures are in
  the repo); reconcile the "5 days" dropdown option in Clarifications with the actual `VIEWS` in
  `app/routes/page.py:174` (month/week/day/list — no 5-day option exists).
- **BR12** `4-review.md:~137`, `.github/workflows/tests.yml` — the style checklist says "ruff runs automatically"
  but no ruff config or workflow step exists anywhere in the tree (Tests runs pip-audit and informational bandit
  only); either add the ruff gate or stop claiming it.
- **BR13** `0-overview.md` (Dashboard summary), `1-plan.md`, `2-build.md` — duplicated process text that
  `dashboard.md`/`4-review.md` already own; reduce to short links so one edit updates one place. Line-count
  review thresholds (4-review.md) are a planning heuristic, not a cited-research cutoff — word them that way or
  find the citation.
