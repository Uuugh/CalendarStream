# DRAFT CHANGELOG behavior gaps: lines 901–1200

Candidate gaps only; no new requirements. CHANGELOG and comparison requirements are pinned at
`1e6d782b5a1d849a606a18b6b2219e9be6ce2e23`. Compared against all `requirements/*.md` and `requirements/drafts/*.md` statements,
including the newly added deployment draft. Existing proposed/planned statements count as coverage;
prior gap reports and excluded evidence mappings do not. Closest IDs indicate partial coverage.

This chunk starts mid-item in beta.12 and ends in beta.3's final Fixed item, whose continuation belongs
to the next chunk. Superseded interaction arrangements are historical, not automatically current rules.
Pure theme measurements, packaging/security dependency upgrades and process notes are excluded.

| CHANGELOG line | release | claim | closest requirement ID or none | proposed owning feature |
|---|---|---|---|---|
| [L913](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L913) | 0.2.8-beta.11 | Search matches title, location and notes and groups matches by day as the user types. CAL-47 specifies query matches without naming all fields or grouping. | CAL-47, CAL-48 | calendar |
| [L914](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L914) | 0.2.8-beta.11 | Empty search bounds mean one year back/ahead. This conflicts with CAL-51 finding an event 700 days forward; reconcile rather than treating the historical statement as an unquestioned new rule. | CAL-51 | calendar |
| [L916](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L916) | 0.2.8-beta.11 | The location map action opens Google Maps for the place, rather than only maintaining a URL-encoded map link. | EVT-15 | events |
| [L918](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L918) | 0.2.8-beta.11 | Deleting connected API client credentials disconnects first while retaining the remote calendars. GGL-08 clears state but does not specify this client-removal retention guarantee across all destinations. Later single-Remove UI supersedes the old trash affordance. | GGL-08, GGL-18 | google |
| [L923](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L923) | 0.2.8-beta.11 | Each source change is pushed to Google immediately/within seconds. Scheduling a sync is specified without a latency commitment. | GGL-28 | google |
| [L950](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L950) | 0.2.8-beta.10 | A remote-created event is placed in a Local calendar included by that Google destination. GGL-53 specifies local import without the destination-membership guarantee. | GGL-53, FED-30 (?) | google / sources |
| [L955](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L955) | 0.2.8-beta.10 | Repeating events created in Google are not copied back. Current import requirements do not state the recurring-event exclusion. | GGL-53 | google |
| [L956](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L956) | 0.2.8-beta.10 | Google setup offers a copyable Claude-assisted browser request and a guide opening adjacent Google windows, with manual/automatic step checks and current-step indication. GGL-47 covers guide contents, not the two complete assisted workflows. | GGL-47 | google / shared UI |
| [L961](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L961) | 0.2.8-beta.10 | The inline event link icon opens the linked event context directly. Showing a saved link is covered without the action. | EVT-30 | events |
| [L989](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L989) | 0.2.8-beta.9 | After updating, the page reloads the new script/style assets while keeping Settings open. SET-31/37 specify version/progress/reload but not preservation of the open Settings context. | SET-31, SET-37 (?) | settings / shell |
| [L999](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L999) | 0.2.8-beta.9 | Legacy default source notes that merely repeat the kind are treated as absent notes. Current editable-note requirements do not specify this migration/normalization. | SRC-28 | sources |
| [L1002](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1002) | 0.2.8-beta.9 | Singleton module and rule lists show no reorder control. The feature drafts exclude this shared-control observation and no shared reorder requirement states it. | UI-05, RUL-26 | shared UI |
| [L1055](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1055) | 0.2.8-beta.5 | Client ID is copyable, but a saved client secret is never returned to the page or offered for copy. GGL-07 covers plaintext omission, not the copy-policy distinction. | GGL-07 | google / shared UI |
| [L1062](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1062) | 0.2.8-beta.5 | Opening an older rule with a nonpalette color presents the nearest supported palette color. Existing UI-10/RUL-37 cover choosing supported colors, not migration/display of previously saved arbitrary colors. | UI-10, RUL-37 | rules |
| [L1108](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1108) | 0.2.8-beta.4 | The versioned script is compressed and fonts are cached for a year. SHL-14 states immutable caching but not these particular encoding/lifetime promises. | SHL-14 | shell |
| [L1118](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1118) | 0.2.8-beta.4 | Startup tolerates a database becoming available later than ten seconds, rather than repeatedly retrying a permanently failed connection then stopping. DEP-01/05 do not define startup connection retry/recovery behavior or its limit. | DEP-01, DEP-05 | deployment / shared data |
| [L1144](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1144) | 0.2.8-beta.3 | Conflict detection identifies a higher rule shadowing a lower emoji or time action, and Keep as is suppresses that warning thereafter. RUL-31 covers color/duplicate conflicts and choices without these broader action/persistence qualifiers. | RUL-31 | rules |
| [L1158](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1158) | 0.2.8-beta.3 | When a newer release is offered without an updater, the update action links to manual update guidance. SET-26 offers installer guidance, but does not explicitly require a version-specific update action to remain useful without the updater. | SET-26 | settings / deployment |
| [L1162](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1162) | 0.2.8-beta.3 | Calendar color is editable only while its configuration is expanded. SRC-39 specifies saving a color without restricting when it may be edited. | SRC-39 | sources / shared UI |
| [L1166](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1166) | 0.2.8-beta.3 | Choosing a closing bracket without an opening bracket inserts the opening bracket at the group start. RUL-06/20 cover grouped condition semantics/validation, not this editor repair behavior. | RUL-06, RUL-20 | rules / shared UI |
| [L1187](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1187) | 0.2.8-beta.3 | Migrated globally shared rules apply to Local and calendars added later rather than retaining only the previously existing source selection. Existing migration examples do not explicitly guarantee this future-calendar scope. | RUL-24, RUL-35 | rules |
| [L1191](https://github.com/Uuugh/CalendarStream/blob/1e6d782b5a1d849a606a18b6b2219e9be6ce2e23/CHANGELOG.md#L1191) | 0.2.8-beta.3 | Changing a source color updates rule badges as well as the calendar key and feed source choices. CAL-45 covers the latter displays; RUL-39 only says scope is shown. | CAL-45, RUL-39 | rules / sources |

## Coverage and exclusions

- beta.12 continuation: GGL-18/19/50 cover disconnect/remote deletion and SET-06 supplies settings access.
  The obsolete sync-in-Settings header/trash layout and status-button geometry are not new current gaps.
- beta.11: EVT-04/15, CAL-47..50, SET-31/32 and GGL-08 cover adding, map links, search, update and
  client removal basics. The table isolates content/latency/retention qualifiers. Field placement, icon
  sizes, plus placement and early Update wording are visual or superseded.
- beta.10: GGL-52..59, HIS-03 and EVT-17 cover two-way changes, source immutability, newer-wins and
  colors. The old more-than-three deletion approval step is explicitly superseded by beta.15, so no new
  requirement is inferred. Rule-generated read-only behavior is GGL-55; unsynced recurring-event exclusion
  remains above. Local open-state memory is SHL-18; rule descriptions are RUL-40. Obsolete Settings
  auto-sync structure, triangles, fades, layout and color appearance are excluded.
- beta.9: SET-31/34 cover update offer cleanup and repeated checks; the open Settings/reload context is
  isolated above. Source name/note behavior is SRC-28; kind layout/fonts and margin placement are theme.
  Singleton handles and redundant-note normalization remain uncovered shared/source qualifiers.
- beta.8 and beta.7: SET-31/34 cover repeated checking and useful controls after update/redraw. Specific
  grow/pulse/fade styling and label history are not new feature behavior requirements.
- beta.6: handle geometry and theme enforcement picture instructions are theme/process only.
- beta.5: GGL-07, SET-26/32/34, RUL-40, UI-05/10, SRC-24/40 and FED-02 cover secret omission, updates,
  rule color names, section structure and last-sync/read wording. The copy distinction and legacy color
  presentation remain above. Historical button names/field locations/palette appearance are excluded.
- beta.4: FED-01, GGL-35/61/84, SHL-14 and FED-18 cover subscription choices, module sync, asset caching
  and conditional feeds. Google Calendar feed fallback is superseded by the separate kinds later.
  Single-copy event-tool construction, file/module paths, dependency upgrades and test/audit process are
  implementation/process; startup database recovery and cache encoding/lifetime qualifiers remain gaps.
  Clearing source note, feed End and Site Address is SRC-28, FED-13 and SRC-23.
- beta.3: SRC-37, EVT-27..31, SET-32, RUL-24/31/32/36/37/41, UI-05/07, TPL-04 and CAL-45 cover the
  broad remove/link/auto-update/rule/section behavior. DEP-03/05 now cover installer defaults and preservation;
  no deployment gap is repeated merely because earlier reports predated that draft. Historical three-week
  link picking is replaced by the small calendar in beta.23; picture redraw duties are later removed.
  Table rows isolate conflict semantics, editor repair, migration scope and rule-badge refresh. Colors,
  bracket flashing and layout details are visual, not new rules.
- The line-1199/1200 saving-route fix supports SET-33's persisted public address/frequency; the following
  continuation is deferred to lines 1201–1500.

Claude validates and assigns confirmed gaps. README, CHANGELOG, existing requirements and code are unchanged.
No application suites were run locally for this documentation comparison.
