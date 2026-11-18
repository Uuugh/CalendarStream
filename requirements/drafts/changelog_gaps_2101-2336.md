# DRAFT CHANGELOG behavior gaps: lines 2101–2336 (final chunk)

Candidate gaps only. Source and requirement comparison revision:
`ec7310f32d362d57f41548939c7e959be99e9f88`. Scanned this full final range through the last CHANGELOG line against statements
in `requirements/*.md` and `requirements/drafts/*.md`, including common TIM/UI/CAP and deployment.
Existing proposed/planned statements count as coverage. Gap reports and excluded inventory notes do not.
Closest IDs give partial context, not approval of new behavior. No requirements are written or extended.

Range begins with 0.1.0's Changed continuation and ends at 0.0.1's last Fixed item. Earlier one-way
semantics, fixed colors, pin interactions, secret-file setup and default thresholds may be superseded
by later releases or Developer decisions. No exception to a common rule is proposed here; contradictory
historical claims are for reconciliation, not adoption.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L2114](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2114) | 0.0.13 | Downloads, uploads and edits reach Google within seconds. Scheduling and updating changed events are covered without an explicit latency guarantee. | GGL-28 | google |
| [L2115](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2115) | 0.0.13 | The default publication window begins on the first day of the current month while leaving older remote events alone. GGL-33 describes window movement without its initial anchor. | GGL-23, GGL-33 (?) | google |
| [L2121](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2121) | 0.0.13 | A daily full check reconciles the remote calendar. Normal/full check semantics and Sync Now are covered without the daily cadence. Later two-way policies supersede unconditional remote-edit overwrite. | GGL-31, GGL-35, GGL-59 | google |
| [L2125](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2125) | 0.0.13 | Each sync that changes events records added/updated counts in activity. History describes change outcomes without a complete sync-summary count contract. | HIS-01, HIS-03 | history / google |
| [L2128](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2128) | 0.0.13 | One OAuth client serves the installation, with secrets encrypted using a key derived from DB_PASSWORD. Client sharing and plaintext protection do not fully define this derivation contract. | GGL-07, GGL-61, DEP-12 (?) | shared security / deployment |
| [L2145](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2145) | 0.0.12 | OAuth requests calendar.app.created plus email, limiting access to calendars the app created. Existing creation/identity requirements do not specify this scope/privacy boundary. | GGL-11, GGL-77 (?) | google / security |
| [L2170](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2170) | 0.0.10 | Feed-name guidance explains that a subscribed Google calendar may need manual renaming because Google reads the initial name. FED-01 offers generic instructions without this caveat; direct API renaming is a different behavior. | FED-01, GGL-30 | feeds / documentation |
| [L2197](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2197) | 0.0.8 | Published ICS carries X-APPLE-CALENDAR-COLOR for consumers that support it and explains Google feed-color limitations. Module/Google colors are covered, not that specific ICS metadata/guidance. | FED-05, GGL-60 | feeds |
| [L2201](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2201) | 0.0.8 | Open section state is shared across browsers and after signing in again, rather than merely remembered in one page. SHL-18 covers fresh/expired state without cross-browser persistence. | SHL-18 (?) | shell / shared UI |
| [L2203](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2203) | 0.0.8 | Saved theme is shared across browsers and applied on initial render without flashing another theme. SHL-19 specifies default/selection, not cross-browser storage or flash-free initial rendering. | SHL-19 | shell |
| [L2224](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2224) | 0.0.7 | Activity exposes links to the last download’s debug captures. No diagnostics requirement defines these source-debug endpoints/content. | DIA-01 | diagnostics |
| [L2237](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2237) | 0.0.6 | Edits to imported events survive every download, show edited/source-changed indicators, and can be reverted to the original source version. CAP-01 permits editing and EVT-17 covers colors, not the complete persistence/revert/staleness contract. | CAP-01, EVT-17, RUL-18 | events / sources |
| [L2247](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2247) | 0.0.6 | Activity timestamps occurring today omit the date. No common time rule or History display requirement specifies this formatting. | HIS-01, TIM-03 | history / shared UI |
| [L2248](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2248) | 0.0.6 | Add to Google Calendar uses a webcal subscription handoff that actually offers to add the feed. FED-01 names the action without its URL-format/handoff contract. | FED-01 | feeds |
| [L2250](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2250) | 0.0.6 | Status event counts reflect the published feed and exclude hidden events. Generic status/history/type requirements do not define this counting basis. | FED-05, CAP-02 | sources / diagnostics |
| [L2259](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2259) | 0.0.5 | Download credentials are passed privately and never exposed on process command lines. Current secret storage/log protection does not explicitly cover process arguments. Curl-only selection is later superseded. | SRC-07 | sources / security |
| [L2273](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2273) | 0.0.4 | Starting or recreating the deployment checks for a newer image automatically, including a moved beta tag, without a separate image-pull command. DEP-09 covers installer reruns, not direct compose startup. | DEP-09 | deployment |
| [L2286](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2286) | 0.0.3 | Timeout feedback distinguishes connection failure from a server accepting a connection but never replying. SRC-55 names nonreply/manual upload without the full diagnostic distinction. | SRC-55 | sources / diagnostics |
| [L2291](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2291) | 0.0.3 | Near whole-day conversion tolerates five minutes on either side of the full-day span. RUL-16 covers near whole-day examples but does not state the exact tolerance; new TIM-04 defines exported all-day semantics, not source-recognition tolerance. | RUL-16, TIM-04 | rules / sources |
| [L2302](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2302) | 0.0.2 | Calendar navigation includes a Today action returning to the current month, beyond month/year picking and week arrows. UI-09 describes the small event picker, not the main calendar’s navigation. | CAL-27, CAL-34 | calendar |
| [L2304](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2304) | 0.0.2 | A prebuilt deployment image supports amd64 and arm64 without local building. DEP-01/02 describe Docker/host support without CPU architecture coverage. | DEP-01, DEP-02 | deployment |
| [L2311](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2311) | 0.0.2 | Automatic CCS+ checks pause after two rejected sign-ins; failed or suddenly empty downloads retain the previous schedule. Source verification/error reporting does not specify these anti-lockout/data-retention consequences. | SRC-14, SRC-32 | sources |
| [L2320](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2320) | 0.0.2 | SCRAPE_INTERVAL_MINUTES remains a legacy fallback for scheduling configuration. Source interval/environment precedence does not define that compatibility alias. | SRC-02 | sources / deployment |
| [L2331](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2331) | 0.0.1 | All durable app data is stored in Postgres. Deployment-controlled storage and a backup command do not explicitly guarantee no durable state in the app container. | DEP-01, DEP-12 (?) | shared data / deployment |
| [L2336](https://github.com/Uuugh/CalendarStream/blob/ec7310f32d362d57f41548939c7e959be99e9f88/CHANGELOG.md#L2336) | 0.0.1 | Copy actions work when the page is opened through plain HTTP, not just a secure context. Shared copy behavior is not specified by the current feature requirements. | DIA-01, GGL-04 | shared UI |

## Coverage and exclusions

- 0.1.0 continuation: SRC-41/GGL-47 cover upload/setup guidance; the row placement and old image-name
  freeze are theme/release history, later superseded by the namespace change.
- 0.0.13: GGL-23..35, TIM-06/07, CAP-02, HIS-03 and GGL-07 cover event publishing, identity/free-busy,
  colors, hiding, renaming, remote reconciliation and secret protection. No-reminders is superseded by
  EVT-19/GGL-25; monthly-window default, latency, daily cadence and activity counts remain qualifiers.
  Secret-file removal and old Settings sync layout are implementation/history.
- 0.0.12: GGL-10/11/17..19 and GGL-45..47 cover connection/calendar creation, reuse, disconnection
  and callback guidance. OAuth scope remains a gap; old required client secret files/mount steps are
  superseded by database storage. TIM-06 supplies recorded time-zone semantics.
- 0.0.11: RUL-03/04/44 cover matching/case behavior and evolving regex policy; old Tag Colors UI is
  superseded by Rules. Setup open-state is broadly SHL-18/UI-05; layout/summary position is theme.
- 0.0.10: manual rename guidance is isolated above. The Not done API rename request is delivered later
  under GGL-30, not a second uncovered behavior.
- 0.0.9: RUL-03/12/24/35/40, UI-10 and SRC-39 cover tag migration, color precedence/names and palette;
  historical tag-row controls/default color buttons are superseded, while geometry/outlines are theme.
- 0.0.8: feed color metadata, cross-browser state and flash-free theme are isolated above. Old
  timed-versus-all-day color strength and header-toggle behavior are later changed, not current rules.
- 0.0.7: SHL-12/16/19, UI-05 and SET-06 cover naming, sections, theme and settings. Later section title
  click rules supersede click-anywhere folding; browser-only state was replaced by persisted state.
  Log window size/header arrangement is visual; last-download debug links remain a diagnostics gap.
- 0.0.6: SRC-28, FED-05/15, EVT-04..06/16/17/20/21, CAP-01/02, CAL-37 and GGL-30 cover naming,
  event editing/creation/hiding and source immutability. Generic retained edits, revert and source-change
  indicators remain above. Old purple custom-event color/pin behavior and link recommendation order
  are superseded or visual. Unique DOM IDs are an implementation correctness condition, not a new rule.
- 0.0.5: later browser-like CCS+ clients supersede curl-only selection. Credential process-argument
  privacy and timeout diagnostics remain candidates. Dependency removal and capitalization are implementation/
  wording, not separate feature requirements.
- 0.0.4: direct compose pull/update behavior remains a deployment qualifier beyond installer reruns.
- 0.0.3: SRC-41/55 and RUL-16/29 cover file upload and broad no-end/whole-day conversion. TIM-04 states
  current all-day semantics; precise import tolerance remains open. Removed leading blank lines are presentation.
- 0.0.2: SRC-02/04/49, TIM-02/04/06/07, ACC-14, DEP-01/05 and RUL-16/29 cover schedule defaults,
  caching, event-time preservation, cross-site security and conversion. Anti-lockout/retained data, architectures
  and legacy interval fallback remain gaps. Browser-scraping removal/library choices are implementation history.
- 0.0.1: FED-01/05/07, ACC-02/03/06, RUL-29 and DEP-01/05 cover basic feed, subscribe, login and defaults.
  Old five-failure limit is superseded by current Developer account decisions, so it is not proposed anew.
  Secret-file installation is replaced by database credentials. Network-idle waiting is browser-test/loading
  implementation rather than a portable user rule; plain-HTTP copy support remains above.

## Full-file scan boundary

CHANGELOG.md has 2,336 lines at this revision. The eight report ranges are contiguous:
1–300, 301–600, 601–900, 901–1200, 1201–1500, 1501–1800, 1801–2100 and 2101–2336.
Previous report files/PRs are tracked separately; this file adds only the final range. Claude reviews the
candidate gaps and converts confirmed ones. No existing file, README, CHANGELOG or code was changed.
No application suites were run locally for this documentation comparison.
