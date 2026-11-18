# DRAFT CHANGELOG behavior gaps: lines 1501–1800

Candidate gaps only. CHANGELOG and comparison requirements are pinned at
`63efddb7a8d36c09376e16e4dc783b0f22046b2e`. Compared all user-visible claims in this range against statement rows in
`requirements/*.md` and `requirements/drafts/*.md`, including deployment/documentation. Proposed
or planned statements count as coverage; prior gap reports and excluded evidence are not requirements.
Closest IDs supply context/partial coverage; no new requirements or approval is created.

Range covers 0.2.7-beta.1 through the heading of 0.1.18. The 0.1.18 body belongs to the next chunk.
Historical top-default, one-account-for-all-Google, source-per-destination and Tag Colors arrangements
are superseded, not silently adopted as current rules. Pure theme/layout and release-process changes
are excluded from app-user behavior.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L1513](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1513) | 0.2.7-beta.1 | Installer accepts an exact beta version rather than only stable/beta channels. DEP-03 specifies channel selection but not arbitrary exact-beta installation. | DEP-03, SET-18 | deployment |
| [L1522](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1522) | 0.2.6 | Every Google destination honors its own Start/End date range with empty bounds unrestricted. Feed filtering is specified, but the Google draft only refers generally to the configured synchronization window. | FED-13, GGL-23, GGL-33 (?) | google |
| [L1541](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1541) | 0.2.6 | A phone initially uses List unless a view was chosen. Existing view selection rules do not specify device-dependent initial view. The historical cycling switches are later replaced by menus. | CAL-33 | calendar |
| [L1553](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1553) | 0.2.6 | Subscribe/feed guidance explains using Google’s desktop site and enabling calendar Sync on Android/iPhone, including possible delayed availability. FED-01 names instructions without this provider-specific guidance contract. | FED-01 | feeds / documentation |
| [L1574](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1574) | 0.2.4 | Shared editable-login fields support cancelling pending typing and a Saved/Verifying/Validated-or-Failed sequence. Source verification is specified, not a shared field feedback contract. | SRC-14, SRC-26, SET-07 | shared UI |
| [L1584](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1584) | 0.2.3 | Per-source Activity exposes Response details and the last calendar file received. No diagnostics requirement defines these download-debug interfaces. | DIA-01 | diagnostics |
| [L1594](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1594) | 0.2.2 | Source configuration automatically expands when action is needed, otherwise preserves its folded/open state. UI-05 and SHL-18 do not specify needs-attention expansion. | UI-05, SHL-18 (?) | sources / shared UI |
| [L1598](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1598) | 0.2.2 | Starter-rule values override DEFAULT_EVENT_HOURS/ALLDAY_24H for the source. RUL-29 specifies starter existence/permanence but not the precedence of environment defaults versus source rule choices. | RUL-29 | rules / settings |
| [L1634](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1634) | 0.2.0 | Repeating feed events are expanded from one year back through two years ahead. SRC-19 specifies recurrence identity without the complete expansion window. | SRC-19 | sources |
| [L1646](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1646) | 0.2.0 | Template-derived events can be placed before/after the start or after the end, and changing the template updates generated events. RUL-17/ TPL-06 cover relative creation with examples but not explicit after-end anchors and update propagation. | RUL-17, TPL-06 | rules / event_templates |
| [L1657](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1657) | 0.2.0 | The status API lists every source and destination while retaining legacy top-level CCS+ fields. No monitoring response/schema requirement specifies this compatibility. | ACC-20 | diagnostics |
| [L1665](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1665) | 0.1.24 | Every password box can show typed text and new-password strength is estimated locally without sending it. Password validity is covered, but the shared field interaction and privacy contract are not. | ACC-26 | shared UI / account |
| [L1682](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1682) | 0.1.23 | Google setup guidance specifically requires publishing or adding a test user before client creation/connection and explains unverified-app consent; every step includes an expected-result checkpoint. Generic ordered setup guidance is narrower. | GGL-47 | google / documentation |
| [L1695](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1695) | 0.1.23 | Google troubleshooting includes deleted_client and repeated weekly reconnection, beyond the named errors in GGL-47. | GGL-47 | google / documentation |
| [L1710](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1710) | 0.1.22 | A successful-address exemption from global lockout lasts seven days. ACC-16/17 leave trust-policy timing unspecified. | ACC-16 (?), ACC-17 (?) | account |
| [L1711](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1711) | 0.1.22 | Concurrent failed logins do not race failure bookkeeping and produce internal errors. This is a narrow concurrency robustness promise absent from generic login behavior. | ACC-16 (?) | account |
| [L1714](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1714) | 0.1.22 | Installer address detection on macOS does not stop the installation silently. DEP-02 lists host support without this failure handling. | DEP-02, DEP-05 | deployment |
| [L1729](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1729) | 0.1.21 | Global login blocking triggers after fifty failures within fifteen minutes and blocked addresses are never evicted before their lockout expires. Account drafts leave thresholds/retention policy open. | ACC-16 (?) | account |
| [L1738](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1738) | 0.1.21 | Checking again does not announce the same available version again in History. SET-25 retains a logged marker but explicitly leaves notification suppression open. | SET-25 (?) | settings / history |
| [L1757](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1757) | 0.1.20 | CCS+ and Google background loops recover after a database restart; concurrent consent completion/synchronization cannot create duplicate calendars. Reconnect reuse and deployment start do not specify these races/recovery. | GGL-17, DEP-05 | google / sources / shared data |
| [L1767](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1767) | 0.1.20 | Health responses do not expose database details, and non-ASCII authentication/token inputs do not crash request handling. Specific feed invalid-token rejection is narrower than the generic safety promise. | ACC-02, FED-04 | diagnostics / account |
| [L1769](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1769) | 0.1.20 | CCS+ downloads allow at most five redirects. HTTPS/cross-host credential/size requirements cover other restrictions, not this numeric redirect limit. | SRC-52, SRC-53, SRC-54 | sources |
| [L1770](https://github.com/Uuugh/CalendarStream/blob/63efddb7a8d36c09376e16e4dc783b0f22046b2e/CHANGELOG.md#L1770) | 0.1.20 | Installer environment output is readable only by its owner and safely preserves answers containing pipe or ampersand. No deployment requirement specifies permissions or input escaping. | DEP-03, DEP-05 | deployment / security |

## Coverage and exclusions

- 0.2.7-beta.1: SET-18/19, SHL-11 and DOC-07 cover channel/version ordering and release links;
  publishing workflow/tag promotion is process, not additional app behavior. Exact-beta installer selection
  remains above. Phone version-line placement is visual.
- 0.2.6: SRC-18/28, RUL-29/35, CAL-33, UI-05, FED-13 and SET-06 cover feed-source creation, starters,
  migration, views, sections and feed range filtering. Table rows isolate Google range, initial phone view
  and provider guidance. Old theme/view cycling and source-section arrangement are historical.
- 0.2.5: RUL-24/25/35 and TPL-04 cover shared rule scope/order and template sections; checkbox-template
  selection and section names are later replaced. No separate current gap is inferred.
- 0.2.4: SRC-14/26 and ACC-07/08 cover actual verification/credential changes. The shared field-feedback
  contract remains above; grow/fade/colors are theme only. Browser Basic-login prompting is later replaced.
- 0.2.3: per-source debug interfaces are a candidate diagnostics gap.
- 0.2.2: SRC-03/23/24, RUL-29, UI-05 and SHL-18 cover scheduling/address/status/starters/open memory.
  Needs-attention expansion and environment-versus-rule precedence remain above; field order/status labels
  and old edit links are visual or superseded.
- 0.2.1: FED-05/06/10, SRC-21/22, GGL-49/50/51, CAL-33, EVT-20/21/25 and DOC-05 cover independent
  destinations, migration, event actions, views and license documentation. One account for all destinations
  is historical; the later module-per-account requirements apply.
- 0.2.0: SRC-17/18/19/22, SET-16, RUL-11/17/29/35, TPL-01/05/06, EVT-05 and FED-10 cover broad
  multi-source/destination/rule/template behavior. Fresh install with no sources and remote deletion on
  source removal were later changed; no obsolete guarantees are proposed. Recurrence bounds, template
  propagation/anchors and status compatibility remain qualifiers above.
- 0.1.24: SET-08/15, GGL-48 and ACC-26 cover imported address/admin email and password validity;
  shared strength privacy/visibility is not yet specified.
- 0.1.23: GGL-20/45..48 and SET-14 cover callback/permission/client guidance and public-host mismatch.
  Expected-result checkpoints, specific setup order and additional troubleshooting topics remain above.
  Old installer public-address prompting is superseded by Settings ownership.
- 0.1.22: GGL-46 covers legacy missing-redirect interpretation; SHL-05 covers translation. Screenshot,
  switch size and icon geometry are documentation/theme; login concurrency/exemption lifetime and silent
  installer failure remain behavior qualifiers.
- 0.1.21: DEP-07, GGL-46, SET-10/12/13, SRC-52 and SET-25 cover trusted proxies, callback validity,
  normalization, redirects and marker preservation. Exact lockout bookkeeping and duplicate announcements
  remain gaps, not new broader security guarantees.
- 0.1.20: SET-10/13, GGL-45/46, ACC-13..15 and SRC-52..54 cover address cleanup, tokens, origin checks,
  page headers, redirects and size. Old private-network proxy trust is later tightened by DEP-07.
  Database restart/consent concurrency, health detail omission and installer permissions remain candidates.
  Source cleanup/doc updates and release-job permission policy are implementation/process, excluded.
- 0.1.19: SET-17/18/20/22/23/25, GGL-47, SRC-31 and UI-08 cover checking, guidance and checkbox labels.
  Tag Colors is superseded by Rules; container IMAGE_TAG wiring is implementation supporting existing channel
  behavior. 0.1.18 has only its heading in this chunk.

Claude confirms gap validity/ownership. No existing requirement, README, CHANGELOG or source file was changed.
No application suites were run locally for this documentation comparison.
