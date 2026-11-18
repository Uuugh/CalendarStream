# DRAFT CHANGELOG behavior gaps: lines 1–300

Candidate gaps only; no new requirements. Source: `CHANGELOG.md` at `51d9fe43c2cb13f8ef530832e61af0e302451887`.
Compared each behavior claim in lines 1–300 against requirement statements in `requirements/*.md`
and `requirements/drafts/*.md` at the same revision. A closest ID is partial coverage, not an assertion
that the whole claim is already specified. Proposed/planned rows count as statement coverage; this scan
does not change approval or implementation status. Prior gap reports are not requirement statements.

Boundary: beta.46 through the first three Changed bullets of beta.31. Beta.31 continues in lines 301–600;
that continuation belongs to the next report. Files, refactors, workflows and visual-only details are not
user behavior requirements. Reverted beta.43/beta.44 history is not promoted to current behavior.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L21](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L21) | 0.2.8-beta.46 | Reopening Settings refreshes Check for updates frequency as well as Auto-update from the server. SET-46 names only auto-update, leaving the frequency half uncovered. | SET-46 | settings |
| [L27](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L27) | 0.2.8-beta.46 | The Settings drawer does not cover its own toggle; a second click can close it. Existing drawer/dialog descriptions do not specify toggle reachability or repeat-click dismissal. | SET-06, UI-02 | shared UI |
| [L39](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L39) | 0.2.8-beta.45 | Full-page Configure temporarily shows the real section, preserving forms/listeners/state and restoring its original location on closing, without duplicated controls. Existing SET-05 names the listing but not this state-preservation contract. | SET-05, UI-02 | shared UI / shell |
| [L51](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L51) | 0.2.8-beta.45 | A refused update-frequency save redraws the control from current server state, matching the explicit auto-update guarantee. | SET-46 | settings |
| [L77](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L77) | 0.2.8-beta.44 | Expired-token recovery explains that retry occurs at the next scheduled sync, rather than implying an immediate retry. Recovery specifies one retry without that scheduling/feedback distinction. | GGL-79 | google |
| [L147](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L147) | 0.2.8-beta.38 | Google Traffic can be cleared and is memory-only, never persisted and cleared on restart. Existing traffic requirements cover content/access/copy but not clearing or lifetime. | GGL-01, GGL-02, GGL-04 | google / diagnostics |
| [L166](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L166) | 0.2.8-beta.36 | Per-account health and backoff survive restart; success or a new sign-in clears health without changing mappings, settings or tokens. Current recovery rules omit new-sign-in reset and the preservation/persistence contract. | GGL-74, GGL-82 | google |
| [L168](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L168) | 0.2.8-beta.36 | The final API setup step reports setup separately and identifies each unsigned, failed or never-synced module. Readiness classification exists, but this per-module diagnostic output is not fully specified. | GGL-78, HIS-22 | google |
| [L169](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L169) | 0.2.8-beta.36 | Consent PKCE verifiers are encrypted; pending sign-ins and invite states survive restart and expire after fifteen minutes. GGL-14/76 omit the exact lifetime and explicit invite-state restart guarantee. | GGL-14, GGL-76 | google / security |
| [L205](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L205) | 0.2.8-beta.33 | After a public-address change, the callback assist box redraws immediately without a reload. SET-04 covers the warning and GGL-46 stale feedback, not immediate refreshed remediation content. | SET-04, GGL-46 | settings / google |
| [L210](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L210) | 0.2.8-beta.33 | One-off status confirmation disappears entirely and frees its space; ongoing health indicators stay visible. Shared status mechanics were excluded from feature drafts and no shared requirement defines this distinction. | UI-05, SET-07 | shared UI |
| [L214](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L214) | 0.2.8-beta.33 | Google sign-in setup resists duplicate submission without leaving an orphan destination. Single-use OAuth state does not specify idempotent module creation/step submission. | GGL-14, GGL-61 | google |
| [L255](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L255) | 0.2.8-beta.32 | History columns can be reordered by dragging or keyboard left/right while focused. Table order/drag attributes were excluded, leaving actual reordering uncovered. | HIS-08 | history / shared UI |
| [L257](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L257) | 0.2.8-beta.32 | Horizontal touch swipes navigate next/previous calendar pages without altering vertical scrolling. Calendar source-string observations were excluded. | CAL-27 (month navigation only) | calendar / shared UI |
| [L259](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L259) | 0.2.8-beta.32 | Installer chooses a subdomain/stack/container prefix and default app/etc/data folders, handling a taken path with use/numbered/alternate/cancel choices. No deployment requirement states this behavior. | none | deployment |
| [L266](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L266) | 0.2.8-beta.32 | Cancel from a rule opened by an event restores the prior event dialog with unsaved edits intact. UI-02 specifies returning to its parent but not preservation of pending field values. | UI-02, EVT-32 | shared UI / events |
| [L267](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L267) | 0.2.8-beta.32 | Status/Action controls retain icon and words together; elsewhere folding occurs after a hold scaled by Animation duration. No shared status requirement defines that policy/timing. | SET-40 (animation settings only) | shared UI |
| [L275](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L275) | 0.2.8-beta.32 | Accepted sign-in is an icon with its words retained as tooltip and accessible name. Existing login-state requirements do not define accessible confirmation content. | ACC-07 | account / shared UI |
| [L276](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L276) | 0.2.8-beta.32 | Toggling All-day or Different end time zone does not resize the event dialog. UI-03 allows growing for content but does not promise this stability for field toggles. | UI-03, EVT-14 | shared UI / events |
| [L282](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L282) | 0.2.8-beta.32 | A rule name in the calendar key is truncated after 25 characters with its full name available as a tooltip. Generic rule naming has no key-specific truncation/disclosure contract. | RUL-40 | calendar / shared UI |
| [L294](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L294) | 0.2.8-beta.31 | Week and Day hour height can be adjusted by keyboard and is remembered. CAL-58 covers Week adjustment without keyboard operation or explicit Day availability. | CAL-58, CAL-59 (?) | calendar / shared UI |
| [L298](https://github.com/Uuugh/CalendarStream/blob/51d9fe43c2cb13f8ef530832e61af0e302451887/CHANGELOG.md#L298) | 0.2.8-beta.31 | Full page hides the footer. CAL-04/53 cover Full page and other sections, without explicitly specifying footer suppression. | CAL-04, CAL-53 | calendar / shell |

## Coverage and excluded history

- beta.46/beta.45: existing SET-05/06, ACC-07, and SET-46 cover Settings grouping/login and auto-update state;
  table rows isolate the missing frequency and shared drawer/section-preservation qualifiers.
- beta.44: reversion narration, code-header/doc fixes, low-finding records and test-clock correction add no
  current user rule. The expired-token scheduling explanation is retained as a candidate gap.
- beta.42: DIA-01 and GGL-04 cover container/traffic bulk copying.
- beta.41: CAL-02 and CAL-11..13 cover clock badge, grip independence and collapse/expand; CAL-57 retains
  the negative-height samples. Visual dot counts are theme details, not additional feature gaps.
- beta.40/beta.39: SHL-02, SET-06, CAL-09, SET-43, RUL-33 and CAL-02 cover the user behavior;
  alignment/refactor/release/header/test-maintenance changes are excluded. Superseded segmented-clock and
  Settings-order descriptions are historical alternatives, not missing current requirements. “Not reproducible”
  and “Still open” items are not delivered changes; existing planned CAL rows already record those requests.
- beta.38/beta.37/beta.36: GGL-01..04 cover traffic content/access/duplicated sync controls; GGL-75/77,
  GGL-74/78/80, HIS-21/22 and GGL-14/76 cover classification, audience, readiness and broad recovery/consent
  behavior. Gaps above isolate lifetime/reset details. Module splits, dependency maps, checkpoints and test
  harness/workflow changes are implementation/process changes, not new user behavior rules.
- beta.35: GGL-64 and HIS-21/22 cover pending-invite ownership and unsigned-module warnings; test-runner
  changes are excluded. beta.34 republishes beta.33, so it is not counted twice.
- beta.33: CAL-55, CAL-54 (?), SET-04, RUL-30 and UI-02/EVT-32 cover dim/restore, callback warning,
  removed-calendar naming and nested-dialog return. CAL-14 already states the icon-per-view behavior
  (planned versus release history is a status question, not an uncovered statement). SHL-01 and SET-34
  cover theme choice and running-version feedback. Reverted ordering, grip-side history and logo-path tidying
  are not additional current gaps. Status lifetime/double-submit qualifiers remain in the table.
- beta.32: SRC-57, SET-43/45, SRC-58, SHL-19 and CAL-26 cover read-only default, address data, power,
  system theme and zone identity. Theme measurements/label history are excluded; status/accessibility,
  touch/keyboard and unsaved-dialog qualifiers remain gaps.
- beta.31 (only lines through 300): SET-42, CAL-60/61 and CAL-11..13 cover grip-side/orientation/stretch
  choices. Picture composition, margins and icon/row alignment are theme-only observations. The keyboard
  hour-height and Full-page footer qualifiers remain in the table.

Claude decides which candidate gaps are valid and whether existing shared requirements should absorb them.
No README, CHANGELOG, existing requirements or source code was edited. No application suites were run.
