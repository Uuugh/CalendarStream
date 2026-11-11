# Build rules, theme rules and Dashboard review

## Scope and status

Report only, prepared at the owner's request. No recommendations in this document change active policy. The owner has final authority; Claude should independently accept, qualify or reject each finding before proposing implementation.

Reviewed main commit: `25e854f4b227caf03bd44cd6c4668dc7c4480139`, including merged PRs #13 and #14. Observed `review-rules` marker: `50f3556e19b9c1b0d7477832ed0b1d8b8596220c`; its `4-review.md` is identical to the reviewed main copy. Neither review marker was moved. This explicit request for a report PR supplies the scope instead of the normal issue-based review exchange.

Scope includes all Markdown under `build_rules/`: overview, PLAN, BUILD, TEST, REVIEW, DEPLOY, Dashboard, theme, UI/UX, cost ledger/prediction method, roadmap, Low findings and generated dependency map; the historical Light/Dark theme-picture references; `AGENTS.md`, `CLAUDE.md`, and the implementation evidence cited below. This is a governance and documentation review, not a fresh application accessibility certification or visual regression assessment. Historical pictures are deliberately frozen and are not current appearance requirements.

The live CalendarStream Dashboard artifact, its URL, implementation and ArtifactData collection were not available for inspection. Dashboard findings concern the tracked specification and its consistency, not observed data loss or verified live defects. The application's planned admin dashboard in the roadmap is a different product feature.

Evidence links below are pinned to the reviewed commit. Severity follows `4-review.md`: documentation/clarity problems are Low. Two Medium findings identify concrete validation/release contract gaps in executable workflows; neither establishes that a bad release has actually occurred. No High findings.

## Findings

### BR01 — Medium: the release commit can differ from the commit whose Tests passed

Evidence: [BUILD checkpoints, lines 74–81](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L74) waits for green Tests, then adds CHANGELOG and bumps VERSION. [Release beta job](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/.github/workflows/release.yml#L87) needs only its own `detect` job, not Tests.

Concrete sequence: checkpoint C passes; VERSION is committed as R; pushing R triggers Release and Tests independently. Release may publish before Tests for R completes, including when that run later fails. The existing Trivy gate does not establish application test success.

Proposed wording: “Publication requires a successful Tests run for the exact release source SHA. Record that SHA and run URL before publication; a successful predecessor run is insufficient.” An owner-approved follow-up must enforce that ordering in workflows, rather than merely asking the author to wait. Acceptance: deliberately failing Tests on a candidate SHA prevents its publication; a passing predecessor cannot satisfy the gate.

### BR02 — Medium: “exactly the beta tested” does not establish image identity

Evidence: [DEPLOY, lines 37–39](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/5-deploy.md#L37) promises exactly the tested beta, then changes VERSION. [Release detection](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/.github/workflows/release.yml#L73) builds a changed VERSION. The [scan build](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/.github/workflows/release.yml#L105) and [published multi-platform build](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/.github/workflows/release.yml#L168) are separate builds.

Concrete sequence: the human tests beta image B; dropping the suffix produces another build S. The policy supplies no digest comparison proving B = S. Similarly, scanning the first local image does not prove that every platform of the second build was scanned. This identifies missing provenance guarantees, not an observed vulnerable image.

Owner decision: does “exactly” mean source behavior or immutable artifact identity? If identity is intended, promote the tested digest and define version metadata separately; otherwise explicitly require testing/scanning the final rebuilt artifact. Acceptance: release evidence links source SHA, tested digest, published digest and scan/platform coverage, with any permitted differences explained.

### BR03 — Low: validation and publication rules need explicit change lanes

Evidence: [BUILD, lines 31–43](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L31) exempts rules/docs from versioning; [After](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L93) unconditionally describes publishing a beta. [Checkpoint instructions](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L74) say CI runs for each push; [Tests triggers](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/.github/workflows/tests.yml#L7) cover main pushes, pull requests and manual dispatch, not every arbitrary branch push. AGENTS also describes full pre-push testing, whereas R20 uses relevant local suites plus CI.

Proposed wording: “Use the validation matrix below; checkpoint instructions qualify the general pre-push checklist. A branch push without an open PR requires dispatch or another documented trigger.” Define docs/rules, application, UI and release lanes. Docs-only work checks references and scope and uses the existing CI policy without VERSION/CHANGELOG edits. Application work runs relevant local suites plus required CI; UI adds visual/accessibility evidence; release adds same-SHA and artifact gates. Preserve suite 17's deliberate DEPLOY-only policy explicitly rather than calling every invocation ‘all tests’. Acceptance: a rules-only PR and an unpublished checkpoint each have one unambiguous checklist.

### BR04 — Low: the review area map still describes the pre-PR13 architecture

Evidence: [review coverage table](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/4-review.md#L17) places rule logic in `app/rules.py`, calendar logic in `app/calsync.py` and auth/Undo/Google responsibilities in `app/main.py`. The current AGENTS code map instead includes extracted `app/rule_engine/`, `app/calendars/`, `app/services/` and runtime modules.

A whole-app review following only those concrete paths can inspect facades while missing their implementations. Update the map against AGENTS and the generated dependency graph; make module families and security boundaries authoritative, with example paths secondary. Acceptance: every extracted implementation belongs to an area, and cross-cutting auth/data-flow review follows calls across areas. Do not hand-edit generated `dependencies.md`.

### BR05 — Low: review evidence and late-finding rules are too absolute

Evidence: [review response, lines 60–61](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/4-review.md#L60) rejects unreproduced High/Medium findings; [line 73](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/4-review.md#L73) prohibits new findings after round one except on fix lines.

A static proof of a missing guard can be material even when an exploit cannot safely be executed. A newly discovered serious defect on unchanged lines should not disappear because round two has started. Proposed wording: “Use a failing test, safe reproduction, or explicit static data/control-flow evidence. Mark unresolved evidence as unverified, explain attempts, and let the owner decide. Escalate newly discovered serious findings in a linked issue or an explicitly extended scope.” Preserve bounded rounds and independent review. Acceptance: static evidence and late security findings have a documented disposition without silently expanding every review.

### BR06 — Low: Dashboard display numbers conflict with persistent verdict identity

Evidence: [overview inputs, line 80](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/0-overview.md#L77) restarts numbers after each BUILD. [Dashboard IDs, lines 15–16](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/dashboard.md#L15) forbids reusing verdict-bearing IDs but permits deleting stale verdicts to reuse them.

Scenario: build A's F1 has Good; build B also has F1. Unless identity includes build scope, a verdict can be attached to the wrong input or history must be deleted. The specification does not define that scope; live implementation may already supply it.

Proposed wording: “Each input has an immutable internal ID; F1 is a display label scoped to a build. Verdicts reference the immutable ID and retain history. Merge records identify absorbed IDs.” Acceptance: two builds with F1 cannot share verdicts; reopening/merging preserves original words and audit history. Verify the actual ArtifactData schema before any migration.

### BR07 — Low: Dashboard read-before-edit lacks a concurrency and recovery contract

Evidence: [Dashboard, lines 8–9](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/dashboard.md#L8) correctly acknowledges that verdicts change while Claude works. [Editing, lines 34–35](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/dashboard.md#L34) validates script replacements and list counts, then republishes the same URL.

A read at t1 followed by a new Bad verdict at t2 and publication at t3 is not protected merely by reading first. The tracked specification does not state whether artifact publication touches verdict storage or how revisions are reconciled. Require a fresh reconciliation immediately before publication and conditional revision updates where supported; on conflict, re-read and merge rather than overwrite. Keep source inputs/verdicts authoritative and rendered lists derived.

Also record a non-secret artifact identifier/provider, collection schema, supported operations and owner-approved recovery procedure. If access is unavailable, report that blocker and retain pending changes; do not invent verdicts or create a replacement Dashboard. Acceptance: simulate a verdict arriving mid-edit and recover the same URL after an interrupted update. No live loss is alleged here.

### BR08 — Low: actual usage, extrapolation and PLAN forecasts need distinct provenance

Evidence: [Dashboard cost graph](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/dashboard.md#L26) permits only real readings and forbids extrapolated dots; [BUILD cost projection](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L24) requires planned projections. [Prediction method](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/build-costs.md#L27) uses low-confidence fallback ratios and ±20% ranges.

These can coexist, but the display contract does not specify forecast marks, confidence or reset epochs. Proposed wording: “Measured readings, derived consumption and forecasts are separate series with explicit labels and provenance. Forecasts use ranges and never appear as measured dots; unknown readings stay unknown.” Retain the existing low-confidence warning, record model/plan/reset context, and avoid making the historical fallback ratio a universal efficiency assumption. Acceptance: an unknown after-reading and a cross-reset estimate cannot look like observed meter values.

### BR09 — Low: handoff and usage instructions assume capabilities or contradict waiting behavior

Evidence: [BUILD usage, line 19](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L19) both “waits” for readings and proceeds with none given, without defining an explicit skip. [Handoff, lines 103–106](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/2-build.md#L103) must say the repo is not on disk and must be cloned with `add_repo`, regardless of the receiving environment.

Proposed wording: “Ask for unavailable meter readings; proceed with unknown only on an explicit skip or the documented non-blocking policy. A handoff reports observed checkout/branch/SHA and in-flight work; the receiver checks for an existing checkout before cloning and uses its available tools.” Preserve human control of model/effort and the explicit second-DEPLOY approval; routine environment discovery does not need another approval. Acceptance: a handoff is truthful both in a fresh chat and an existing worktree, and lack of a provider-specific tool does not falsely block read-only work.

### BR10 — Low: theme history still contains conflicting current-looking requirements

Evidence: [theme sources, line 7](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/theme.md#L7) mentions PDF counterparts that are not tracked. [Clarification, line 400](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/theme.md#L400) lists a five-day calendar dropdown option; [the actual view set](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/app/routes/page.py#L174) is month/week/day/list. Five-day printing exists separately, so its context matters.

PR14 already corrected numerous spacing, handle, palette and popup rules. Do not reintroduce the older values or treat the frozen pictures as live requirements. Give current requirements stable rule IDs; turn chronological clarifications into dated rationale with explicit superseded/current links. Mark PDFs as unavailable or remove the obsolete source claim. Owner decision: reconcile the five-day dropdown wording with intended current behavior; this report does not add a view. Acceptance: each active component value has one normative definition and history cannot accidentally override it.

### BR11 — Low: accessibility precedence differs between overview and UI/UX guidance

Evidence: [overview, line 98](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/0-overview.md#L98) says theme wins where requirements differ; [UI/UX authority](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/ui_ux.md#L3) says flag conflicts to the owner, and its baseline requires applicable WCAG 2.2 AA criteria.

Proposed wording: “Theme governs approved visual values; UI/UX defines accessibility acceptance criteria. An apparent conflict is unresolved until presented to the owner with evidence and an accessible proposal; neither document silently waives the other.” This is a policy inconsistency, not a claim of current WCAG nonconformance. Acceptance: a hypothetical token/contrast conflict has the same escalation path from either document. Preserve PR14's corrected light muted palette and both-theme/phone/keyboard checks.

### BR12 — Low: enforcement claims overstate what automation establishes

Evidence: [review style checklist](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/4-review.md#L133) says Ruff runs automatically; [Tests scan steps](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/.github/workflows/tests.yml#L36) run pip-audit and informational Bandit, without Ruff. No tracked Ruff configuration/workflow was found. Theme/BUILD/REVIEW also promise each Clarification is tested by suite 44; that suite combines actual browser assertions with text/keyword bookkeeping, and additional theme coverage lives in other suites. Text membership alone cannot prove every requirement's semantics.

Proposed wording: name actual commands, distinguish blocking gates from advisory findings, and map stable theme rule IDs to assertions/manual evidence across suites. Do not add a dependency or quietly weaken tests just to align the claim. Acceptance: every claimed automatic gate has a workflow/configuration reference; passing CI is not presented as proof that Bandit has zero findings or every theme statement is exhaustively verified.

### BR13 — Low: duplicated process text and fixed review thresholds increase maintenance cost

Evidence: [overview Dashboard summary](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/0-overview.md#L22) repeats ordering, lifecycle, publication and verdict rules owned by `dashboard.md`; PLAN repeats verdict handling and BUILD repeats handoff/setup requirements. [Review scope](https://github.com/Uuugh/CalendarStream/blob/25e854f4b227caf03bd44cd6c4668dc7c4480139/build_rules/4-review.md#L8) applies two issues/whole-app thresholds and cites unspecified studies for line/time cutoffs.

Keep one normative owner for each operation, with short summaries linking to it. Separate historical cost rows and theme rationale from instructions loaded every time, without discarding audit history. Treat line counts as planning heuristics, not evidence of risk or review completeness; cite the research or remove the unsupported attribution. Let docs-only/generated-heavy changes use a justified scope while retaining independent review of actual risks. Acceptance: changing verdict handling requires one normative edit, and a large generated diff does not automatically force an unjustified whole-app review.

The roadmap and Low-findings list are useful deferred-work stores, but should reference durable input/finding IDs and source issues, with a clear owner/state. Avoid repeatedly copying backlog prose into PLAN/Dashboard/history. Preserve original user wording and the rule that recording an input does not authorize implementation.

## Recommended follow-up structure

| Canonical owner | Responsibility | Other files should contain |
| --- | --- | --- |
| `0-overview.md` | Commands, roles, owner authority, privacy, navigation | Short links to operative procedures |
| `1-plan.md` | Scope agreement, exact proposed rule wording, estimates | References to input identity and cost schema |
| `2-build.md` | Change lanes, checkpoints, validation evidence | Links to release and UI gates |
| `3-test.md` | Human testing, browser consent, safe evidence | No duplicate release authority |
| `4-review.md` | Review scope, evidence, dispositions and final covered SHA | Current architecture families and gate references |
| `5-deploy.md` | Explicit stable approval, source/artifact promotion | Same-SHA/digest acceptance contract |
| `dashboard.md` | Durable identities, verdict lifecycle, concurrency, recovery | One provider/schema reference; actual/forecast display contract |
| `theme.md` | Current numbered design requirements | Separate linked historical rationale/pictures |
| `ui_ux.md` | Applicable accessibility and usability acceptance | Conflict escalation and evidence requirements |
| `build-costs.md` | Recorded measurements and calibrated prediction method | Explicit unknowns, confidence and reset context |
| `roadmap.md`, `low-findings.md` | Deferred work and review debt | Durable references, state and owner |
| `dependencies.md` | Generated import evidence | Generator invocation, not manually maintained policy |

Suggested sequence: first decide BR01/BR02 release guarantees; then reconcile validation and review coverage; then verify live Dashboard schema and identity/concurrency requirements; finally consolidate wording/history and evidence mappings. Implement approved changes in small, separately reviewable commits. Do not move `reviewed`/`review-rules`, publish a release, alter theme values, migrate verdicts or delete history as part of accepting this report.

## Strengths to retain

The existing rules protect owner authority, explicit stable-release consent, read-only real calendar sources, synthetic test data, secret-free evidence, reversible checkpoints, independent review and generated dependency documentation. The tests workflow uses pipe failure propagation, pip-audit is blocking, and the release workflow explicitly gates fixable High/Critical Trivy findings. PR14's component ownership map and distinction between historical pictures and current written rules materially improve theme maintenance. Consolidation should preserve these controls rather than shortening them away.

## Validation and limits

This PR adds only this report: no active rules, application code, CSS, dependencies, workflow, VERSION or CHANGELOG changes. Checks performed for the report are recorded in its PR description, alongside any completed GitHub Tests run. Existing application CI checks regressions but does not validate these proposed governance changes or the inaccessible live Dashboard. The dependency graph remains generated and unchanged.

## Claude review handoff

1. Check out this PR and independently verify all pinned evidence against the stated base, then check whether main has changed since it.
2. Reply Accepted / Partly / Rejected for BR01–BR13 with evidence; distinguish policy ambiguities from verified implementation gaps. Do not mark a finding fixed merely because proposed wording appears here.
3. Resolve the owner's release-identity and publication-gate decisions before drafting workflow changes. Identify actual final covered/tested SHAs and image digests.
4. For Dashboard findings, inspect the real artifact/provider and ArtifactData schema before proposing migration or asserting a live defect. Preserve verdict history and the same artifact URL.
5. Reconcile theme and UI/UX authority without reverting PR14 or changing appearance. Treat picture references as historical; verify current rule-to-test mappings.
6. Present approved changes as a separate PLAN with exact wording and proportionate checks. Keep this report PR in Draft until the owner/Claude review is complete; do not merge automatically.
