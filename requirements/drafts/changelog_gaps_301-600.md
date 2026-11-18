# DRAFT CHANGELOG behavior gaps: lines 301–600

Candidate gaps only; no new requirements. Source revision: `7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a`. Compared claims in this
exact line range against `requirements/*.md` and `requirements/drafts/*.md` at that revision.
Prior gap reports and excluded evidence notes are not requirement statements. Proposed/planned rows
count as statement coverage; nearby IDs below identify partial coverage, not a confirmed new requirement.

This chunk begins inside beta.31 and ends at beta.19’s heading. Beta.19 body begins in the next chunk.
Reversions, replaced alternatives, process notes, internal refactors and pure theme measurements are
not promoted to current feature behavior. Repeated gaps from README/earlier chunks remain candidates
here when the release makes its own claim; Claude can reconcile them without changing source history.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L306](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L306) | 0.2.8-beta.31 | Deleted and hidden events do not count toward a day cell’s overflow. Event hiding/deletion is covered without the overflow-count consequence. | EVT-20, EVT-21 | calendar |
| [L307](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L307) | 0.2.8-beta.31 | Rule creation from an unsaved Add-event reads the live title and date. Existing rule/event navigation does not promise using pending unsaved values. | EVT-32, RUL-36 | events / rules |
| [L315](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L315) | 0.2.8-beta.30 | Rule text actions can render through translation without crashing page loads. This is narrow robustness evidence beyond generic translation; confirm whether a user requirement or regression-only note is appropriate. | RUL-11, SHL-08 | rules / shell |
| [L320](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L320) | 0.2.8-beta.30 | Saving a rule without a title generates one from its conditions/actions. RUL-40 describes displaying a title if present, not automatic title generation. | RUL-40 | rules |
| [L338](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L338) | 0.2.8-beta.29 | Dimmed calendar/key choices also affect Print, not just the displayed calendar. The later persistent visibility rules omit print filtering. | CAL-54 (?), CAL-56 | calendar |
| [L345](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L345) | 0.2.8-beta.29 | Printed titles wrap without clipping, and each sheet fits one physical page across itinerary/five-day/week/month choices. Existing print pagination is fixture-qualified and does not provide the complete overflow guarantee. | CAL-62 (?), CAL-63 (?) | calendar |
| [L356](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L356) | 0.2.8-beta.28 | An explicit Online Meeting field can be opened; dedicated conference data and supported service links prefill it only when it is not already filled. Extraction rules do not cover field preservation/opening. | EVT-33 | events |
| [L358](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L358) | 0.2.8-beta.28 | A meeting link is published as ICS URL and the first notes line, without being mistaken for a remote edit on readback. Google description handling covers part, not the ICS field guarantee. | GGL-73 (?), FED-29 | feeds / events / google |
| [L359](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L359) | 0.2.8-beta.28 | A disabled source is omitted from every feed while its selected membership is retained. Sources/feed off-state requirements do not explicitly specify source exclusion from published content. | SRC-58, FED-28 | sources / feeds |
| [L361](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L361) | 0.2.8-beta.28 | CCS+ starter rules can each be removed during source creation, before adding the calendar. Existing starter-rule requirements do not specify creation-time removal. | RUL-29 | rules / sources |
| [L362](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L362) | 0.2.8-beta.28 | Password and stream-name validation guidance updates while typing, including individual strength-rule feedback. Strength validity exists without this shared-field feedback contract. | ACC-26, FED-08 (?) | shared UI |
| [L364](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L364) | 0.2.8-beta.28 | Existing passwords continue working after stronger creation rules are introduced. Existing login/password strength requirements do not explicitly guarantee grandfathering. | ACC-26 | account |
| [L368](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L368) | 0.2.8-beta.28 | Source ordering determines priority when events conflict. The default calendar’s independence from order does not define conflict priority. | SRC-34, SRC-59 | sources |
| [L369](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L369) | 0.2.8-beta.28 | Stream names accept precisely 1–128 letters, digits, hyphen or underscore. FED-08/27 explicitly leave the full character set/save-route bound open. | FED-08 (?), FED-27 (?) | feeds |
| [L374](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L374) | 0.2.8-beta.28 | An opened calendar event remains expanded across module saves and Sync Now redraws. Dialog-return rules do not specify inline event persistence during redraw. | UI-02 | calendar / shared UI |
| [L381](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L381) | 0.2.8-beta.27 | Rule-deleted events cannot be individually restored; changing/removing the rule brings them back, and they are excluded from feeds. RUL-14 covers hiding and labeling but not these recovery/publishing consequences. | RUL-14 | rules / feeds |
| [L384](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L384) | 0.2.8-beta.27 | Event links migrate at startup into editable link rules; delete-with and move-with actions can each be removed. Existing linked-event behavior does not specify migration or independent action removal. | EVT-27, EVT-31, RUL-11 | events / rules |
| [L388](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L388) | 0.2.8-beta.27 | Then actions can be reordered and their order defines action priority and emoji sequence. Whole-rule reordering/ordered emoji effects do not specify changing action order. | RUL-12, RUL-26 | rules / shared UI |
| [L389](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L389) | 0.2.8-beta.27 | Installer enables the updater by default and detects a second installation, allocating distinct numbered containers and port persisted in environment settings. The historical stack-folder default was later superseded; no deployment requirement covers the allocation/default-updater behavior. | none | deployment |
| [L403](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L403) | 0.2.8-beta.27 | Emoji selection counts immediately as a pending change; Enter in emoji search selects its first result rather than submitting the form. Generic searchable emoji picking does not specify keyboard submission behavior. | UI-11, RUL-43 | shared UI |
| [L405](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L405) | 0.2.8-beta.27 | Resolving a rule conflict by dropping an action removes the correct field-specific action kind (such as title versus notes). Existing conflict resolution wording does not explicitly cover action subtype identity. | RUL-31 | rules |
| [L412](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L412) | 0.2.8-beta.26 | Module/editor save controls remain disabled until dirty; a popup Cancel remains usable and a new-item popup can save defaults. Shared SET-07 specifies appearance, not this complete enabled-state contract. | SET-07 | shared UI |
| [L424](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L424) | 0.2.8-beta.26 | Sections/modules automatically fold after exactly 24 hours. SHL-18’s tested twenty-five-hour point leaves the exact expiry rule open. | SHL-18 (?) | shell / shared UI |
| [L430](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L430) | 0.2.8-beta.26 | A new rule’s Add emoji action begins empty rather than with a default airplane. Searchable picker behavior does not specify that default. | RUL-37, UI-11 | rules |
| [L451](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L451) | 0.2.8-beta.25 | CCS_CLIENT selects auto/browser/browser-patient/curl; auto retries with longer browser wait then curl, browser-patient allows three 90-second attempts, and each attempted client is diagnosed. Sources leaves precise retry/transport policy open. | SRC-56 (?) | sources |
| [L453](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L453) | 0.2.8-beta.25 | A rejected CCS+ password stops transport fallback immediately, and redirects have a maximum of five. Existing source error/redirect rules do not specify this stop condition and numeric redirect budget. | SRC-50, SRC-52 | sources |
| [L467](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L467) | 0.2.8-beta.24 | Updates initiated elsewhere appear on every open page and trigger reload fifteen seconds after Restarting; checks wake when due rather than on hourly polling. Current settings rules leave exact reload timing and scheduler granularity open. | SET-37 (?), SET-22 (?) | settings |
| [L498](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L498) | 0.2.8-beta.23 | The calendar’s link icon opens the linked target directly. EVT-30 specifies displaying a saved link but not this action. | EVT-30 | events |
| [L532](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L532) | 0.2.8-beta.22 | Printing an event temporarily uses Day view without changing the otherwise remembered print view. Existing CAL-43 remembers preferences and the event-print mapping does not specify preservation during this override. | CAL-43, EVT-03 | calendar / events |
| [L559](https://github.com/Uuugh/CalendarStream/blob/7033ae1b0ae5e6f5e9b30ddb029e76adbc74c60a/CHANGELOG.md#L559) | 0.2.8-beta.21 | A color request rejected with an access token issued within the last minute is not retried with another fresh token. General color fallback/recovery rules omit that precise anti-refresh condition. | GGL-68, GGL-79 | google |

## Coverage and excluded history

- beta.31 continuation: CAL-55 covers restoring the final dimmed item; EVT-21 covers custom deletion.
  Administrator placement is shared/theme history. Overflow and unsaved-rule inputs are isolated above.
- beta.30: RUL-11/13 and SHL-08 cover text actions/translation generally. Title generation is not specified.
  Narrow-screen Default placement and handle margins are theme-only; waiting items are not delivered changes.
- beta.29: CAL-02/06/07/33/53/58, SET-39..41 and UI-10 cover clock, legend, Full page and preference basics.
  Combined Administrator and segmented switch are later superseded. Print filtering/wrapping remain qualifiers.
- beta.28: SRC-57/58, FED-28, RUL-29, ACC-26, EVT-33 and GGL-73 cover defaults, power, starter rules,
  password validity and meeting extraction. Gaps above isolate missing content/creation/compatibility policy.
  Last-Local removal is SRC-36; visual positions, boxes and naming changes do not add data behavior.
- beta.27: RUL-11/13/14/15, EVT-20/21/31, UI-02/11 and SET-07 cover actions, event distinction and generic
  dialogs. UI placement/label/tint changes are excluded. Earlier default stack path is historical after beta.32;
  second-install allocation and updater-default behavior are not covered by any deployment requirement.
- beta.26: SHL-16/17 and UI-05 cover branding/sections. Layout, pulse/radius/tint/spacing/timing aesthetics,
  static-picture and build-process changes are excluded. The dirty-state exceptions and exact fold lifetime
  are behavioral qualifiers rather than color/dimension rules; status folding is also flagged in chunk 1–300.
- beta.25: SRC-49..56 cover validation, caching, size, redirects and retry outcomes. Five-MB/HTTPS and
  cross-host credential protection are covered; client fallback, rejection stop and redirect count remain gaps.
  Library/image choices and build-policy prose are not additional user requirements.
- beta.24: SET-31/32/37 cover update progress and automation; the exact timing/granularity remains open.
  Removal confirmation is UI-06/FED-11; event color defaults are EVT-18; field placement and palette styling
  are theme/shared UI, not missing feature rules.
- beta.23: UI-09/06, EVT-27..29, FED-10/15/25/26 and HIS-19 cover picking, links, feed defaults and retention.
  Superseded undo-column placement/preview presentation and icon alignment are excluded. Event source effects
  are EVT-23/24; direct target navigation is isolated above.
- beta.22: UI-01..03, EVT-25..29/20/23 and TPL-05/07 cover dialogs, template choice, duplicate, link removal
  and Hide/Show. Layout, scratch-work folders and roadmap entries are excluded; temporary print preference
  preservation remains a candidate gap.
- beta.21: GGL-68..72 and HIS-15/17 cover color fallback, retained method, refusal/unreachable distinctions
  and diagnostic history; only the fresh-token time condition remains above. Tooltip edge behavior is UI-07;
  measured spacing/columns/Today border and process instructions are theme/process, not feature gaps.
- beta.20: explicitly behavior-preserving refactor, source paths and build rules; no new app-user behavior gap.
- beta.19: only the heading is in this range; body is deferred to lines 601–900.

Claude confirms and assigns gaps; this file does not alter README, CHANGELOG, existing requirements or code.
No application suites were run locally for this documentation comparison.
