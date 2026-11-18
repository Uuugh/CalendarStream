# DRAFT CHANGELOG behavior gaps: lines 1201–1500

Candidate gaps only. CHANGELOG and comparison requirements are pinned to
`4fe4ae19e9dea9415ef22f36e912bdaef1bb675e`. Compared user-visible release claims against all `requirements/*.md` and
`requirements/drafts/*.md` statements, including deployment/documentation. Existing proposed/planned
statements count as coverage. Gap reports and excluded evidence notes are not requirements.
Closest IDs indicate partial coverage; Claude decides whether to confirm each candidate.

The range starts with the blank after beta.3's previous chunk, then beta.2, and ends after beta.2 of
0.2.7. Older names/defaults/layouts are not automatically current behavior. Pure theme measurements,
license prose, screenshot process and internal implementation are not promoted to requirements.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L1205](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1205) | 0.2.8-beta.2 | Calendar and feed order can be changed by drag or up/down controls and is saved immediately. Whole-rule reordering is covered, but source/feed order editing is not fully specified. | RUL-26, SRC-34 | sources / feeds / shared UI |
| [L1210](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1210) | 0.2.8-beta.2 | The first Print Preview uses the calendar view before any remembered print preference; preview supports a Monday–Friday five-day mode. CAL-43 covers remembered choice, not initial choice or the complete five-day interpretation. | CAL-39, CAL-40, CAL-43 | calendar |
| [L1213](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1213) | 0.2.8-beta.2 | At most five reminders can be chosen, ranging from at-start to one-week-before. Existing reminder selection/publication rules provide examples without the complete count/range. | EVT-19, FED-17, GGL-25 | events |
| [L1217](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1217) | 0.2.8-beta.2 | Upgrade creates its initial Local once and includes it in every feed. Fresh-install/default rules and FED-30’s question do not establish upgrade-time universal inclusion. The historical always-top default is later replaced. | SRC-16, FED-30 (?) | sources / feeds |
| [L1231](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1231) | 0.2.8-beta.2 | Rule priority wins even over a calendar-specific rule, and editing a rule preserves its calendar applicability. RUL-12/24 describe precedence/scope without expressly promising edit-time scope preservation. | RUL-12, RUL-24 | rules |
| [L1235](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1235) | 0.2.8-beta.2 | Each source lists its own rules before applicable shared rules, and each source’s list can be reordered. RUL-25/26 cover insertion/global reordering without defining the complete per-source precedence/list contract. | RUL-25, RUL-26 | rules / sources |
| [L1237](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1237) | 0.2.8-beta.2 | Every earlier-format rule converts preserving order and calendar scope. Existing RUL-35 covers particular legacy tag/default cases, not this general migration promise. | RUL-35 | rules |
| [L1240](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1240) | 0.2.8-beta.2 | Module Cancel also closes the configuration. Generic UI-05/SET-07 do not specify this cancellation consequence. | UI-05, SET-07 | shared UI |
| [L1243](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1243) | 0.2.8-beta.2 | An inline calendar event stays expanded on redraw and no longer closes on outside click. The former calendar evidence mapping leaves this shared interaction open rather than defining a requirement. | UI-02 | calendar / shared UI |
| [L1252](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1252) | 0.2.8-beta.2 | CCS+ setup guidance explains enabling trips as a single event and all options, changing a dedicated Calendar Sync password and completing an Accomplished checklist. SRC-13 offers setup guidance without this detailed configuration contract. | SRC-13 | sources / documentation |
| [L1286](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1286) | 0.2.8-beta.1 | The page footer links to README License & Attribution. Existing documentation requirements cover README explanations, not the in-app link. | DOC-05 | shell / documentation |
| [L1291](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1291) | 0.2.8-beta.1 | All Sync Now controls, including Google, immediately acknowledge work and return from terminal feedback to an idle action. Source sync outcomes are specified without a general shared acknowledgement/reset rule. | SRC-31, GGL-35 | shared UI |
| [L1320](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1320) | 0.2.8-beta.1 | Pages never fetch any external resource; locally served fonts/icons are narrower than this blanket network claim. The status API also includes Google synchronization data without a requirement defining that response. | SHL-13, SHL-14 | shell / diagnostics |
| [L1326](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1326) | 0.2.7-beta.6 | Help opens on pointer hover, can be pinned by click/tap and closes on outside click or Escape. UI-07 specifies click and placement without the full hover/pinning contract. | UI-07, UI-02 | shared UI |
| [L1342](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1342) | 0.2.7-beta.6 | Save feedback includes Saving during transfer and persists Saved/Cancelled for three seconds before reset. SET-07 states control appearance, not this shared feedback timeline. | SET-07 | shared UI |
| [L1344](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1344) | 0.2.7-beta.6 | Saving, cancelling and removing replace only affected page regions and preserve text being entered elsewhere. FED-16 questions a source-save example, not the complete generic guarantee. | FED-16 (?), SRC-33 | shared UI |
| [L1381](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1381) | 0.2.7-beta.5 | Record changes tracks source title, time and location changes, moved recurrences and dropped events; it annotates the event and records activity. RUL-18 gives later-edit annotations without all these change categories/removal guarantees. | RUL-18 | rules / history |
| [L1385](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1385) | 0.2.7-beta.5 | Report/Suggest forms select evidence/contact/reply details, redact private identifiers, preview output, open a prefilled GitHub issue or copy/download without an account. No diagnostics requirement specifies this workflow. | DIA-01 (log copy only) | diagnostics |
| [L1422](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1422) | 0.2.7-beta.5 | Month and time-zone changes swap the calendar immediately without reloading; a prior phone view query cannot leave the chosen view stale. CAL-33 covers view selection without the full navigation/state guarantee. | CAL-25, CAL-27, CAL-33 | calendar / shared UI |
| [L1430](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1430) | 0.2.7-beta.4 | Source status/interval wording shortens based on measured available space, including translated text. This is adaptive content behavior beyond fixed pixel layout, without a shared requirement defining it. | SHL-05, SRC-24 | shared UI |
| [L1451](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1451) | 0.2.7-beta.3 | An unreachable updater reports Update failed with its reason. SET-29 covers token rejection and SET-26 readiness, but not failure after an accepted action loses updater connectivity. | SET-26, SET-29 | settings / deployment |
| [L1481](https://github.com/Uuugh/CalendarStream/blob/4fe4ae19e9dea9415ef22f36e912bdaef1bb675e/CHANGELOG.md#L1481) | 0.2.7-beta.2 | An unconnected Google account’s configuration opens automatically, while other module open states are retained. Existing UI-05/SHL-18 do not define needs-attention auto-expansion. The historical account-in-Settings structure is superseded. | UI-05, SHL-18 (?) | shared UI / google |

## Coverage and exclusions

- 0.2.8-beta.2: UI-01/02/05, CAL-33/39..43, EVT-04/19, SRC-16/35/57/59, RUL-03..17/24..29/35,
  SRC-13/39 and HIS-02 cover dialog modes, views, prints, Local/default creation, rule basics, source
  guidance/color and healthy status. Table rows isolate reminders, upgrade inclusion, priority/migration,
  cancellation and redraw qualifiers. Old top-calendar default/removal fallback are superseded by explicit
  Local default; old status labels, icons, color box placement and layout are not additional gaps.
  New-feed naming is FED-15/26; tooltip placement and field sizes remain shared/theme.
- 0.2.8-beta.1: SHL-13/16, UI-05, SRC-31/32 and GGL-35 cover fonts, title/footer, sections and sync outcomes.
  Local font/asset delivery is not a guarantee of zero external requests, and no status API schema is
  specified. Rounded rectangles, icon family, color/font placement and fixed header heights are theme.
  Cancel spelling/icons are shared presentation; their general behavior is not restated as feature rules.
- 0.2.7-beta.6: CAL-39..43/60..63 cover Print and its remembered options; later Preview supersedes printing
  the current grid only. UI-07/02 cover part of help, and EVT-16..18/CAL-37 cover event colors/key.
  Generic partial-refresh/pending-edit and feedback timing qualifiers remain above. Dimensions, wording
  history and old Added-here color are theme or later superseded behavior.
- 0.2.7-beta.5: SRC-28/30, RUL-27/28/36/39/41, TPL-04, UI-05, SRC-31 and CAL-33 cover provider presets,
  source notes, rule edit/copy/delete and sections/navigation. Record-changes scope, diagnostic reporting
  and all navigation variants remain candidates. Old inline per-source editing/shared-template save modes
  are replaced by All Rules; no obsolete UI is silently promoted. Source next-check schedule is SRC-03.
- 0.2.7-beta.4: status shortening is a candidate shared behavior; left-edge alignment itself is theme.
  Light/dark README screenshots are documentation/process, not app behavior.
- 0.2.7-beta.3: DEP-02/03/10/11 and SET-26..32/37 cover optional updater, network/token protection,
  deployment hosts, progress and automation. Historical no-by-default updater is superseded by later
  yes-by-default; updater fork/version facts are external implementation context. Connectivity failure
  beyond readiness/token refusal remains above.
- 0.2.7-beta.2: SRC-29, FED-15, UI-05, TPL-04, SHL-12 and SET-06 cover username wording, inherited feed
  name and sections. Automatically opening unconnected Google configuration remains an uncovered qualifier.
  Renamings, narrow-screen geometry, spacing and screenshots are theme/documentation history.

No existing file, README, CHANGELOG or source code was edited. No application suites were run locally.
