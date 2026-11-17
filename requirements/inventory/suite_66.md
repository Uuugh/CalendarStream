# Suite 66: Settings/calendar markup and installer defaults

Source: [`tests/suite_66.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8166; seed.demo; patched background loops. Checks inspect HTTP markup, stored default theme, generated rule label and many source/file strings; bash -n validates installer syntax. No browser interaction despite several interaction-oriented labels.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S66-01 | shell | With no saved override, effective theme is system. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L39) |
| S66-02 | sources | Source-section title markup contains Sources. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L44) |
| S66-03 | sources | The source-title pattern no longer matches Calendars. | [L45](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L45) |
| S66-04 | sources | A read-only calendar's Default control is disabled with a read-only tooltip. | [L48](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L48) |
| S66-05 | sources | Page source contains the combined note/power row marker. | [L51](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L51) |
| S66-06 | settings | Settings markup contains the public-address row-list ID. | [L55](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L55) |
| S66-07 | settings | The sampled domain-row source orders its delete control before add control. | [L56](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L56) |
| S66-08 | settings | Settings source omits the old separate More addresses heading. | [L57](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L57) |
| S66-09 | settings | Settings page includes Theme text. | [L60](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L60) |
| S66-10 | history | The sampled page contains accepted-check markup or a check_circle occurrence anywhere. | [L65](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L65) |
| S66-11 | history | When History markup exists, the sampled Time header has the expected data-col marker. | [L68](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L68) |
| S66-12 | history | Coverage marker: if History table markup is absent, ok(True) reports the skipped-table branch. | [L69](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L69) |
| S66-13 | history | When the table node exists, its column IDs are time,type,event,undo in order. | [L73](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L73) |
| S66-14 | history | That table-header substring contains draggable=true. | [L74](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L74) |
| S66-15 | calendar | Page markup has a zone icon wrapper and picker ID. | [L78](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L78) |
| S66-16 | calendar | Page markup has clock ID, switch role and clock-icon class. | [L79](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L79) |
| S66-17 | rules | The long rule name is rendered as the sampled truncated text or appears in a full-name title attribute. | [L84](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L84) |
| S66-18 | events | The event page has the End Time zone tooltip. | [L88](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L88) |
| S66-19 | events | The event-template source contains display:revert. | [L89](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L89) |
| S66-20 | events | Event script includes eventSuspend and the guarded blank-frame assignment. | [L93](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L93) |
| S66-21 | rules / events | Rule/saving scripts include ruleFromEvent and the event-dialog reopen call. | [L94](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L94) |
| S66-22 | shell | Status-fold source includes the animation-duration variable and hold-base symbol. | [L98](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L98) |
| S66-23 | shell | Status-fold source comments contain the sampled keep-icon-and-words wording. | [L99](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L99) |
| S66-24 | calendar | Calendar script contains touchstart, touchend and dx strings. | [L103](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L103) |
| S66-25 | shell | Base CSS has a card rule with padding:12px. | [L107](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L107) |
| S66-26 | shell | Two/three-line CSS contains border:0 and background:none. | [L111](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L111) |
| S66-27 | shell | That CSS contains the auto-left-margin expression. | [L112](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L112) |
| S66-28 | shell | That CSS omits the sampled old min-width:900px media expression. | [L113](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L113) |
| S66-29 | process | Installer source contains calendarstream and Subdomain strings. | [L117](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L117) |
| S66-30 | process | Installer and compose both contain STACK_PREFIX. | [L118](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L118) |
| S66-31 | process | Installer source includes current path plus subdomain. | [L119](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L119) |
| S66-32 | process | Installer source includes the conflict-awareness question phrase. | [L120](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L120) |
| S66-33 | process | bash -n returns zero for install.sh. | [L121](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_66.py#L121) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Most rows are markup/source-string checks; swipe, nested-dialog restoration and status-fold timing are not executed here. Row 23 checks comments only, not behavior.
- Row 10 permits any check_circle occurrence instead of a specific Accepted row. Row 12 is an unconditional skip marker and cannot independently verify History. Rows 13/14 only run when the table exists.
- Row 17 permits a full-name tooltip instead of requiring truncation and thus does not establish an exact 25-character cut. Icon shape/badge rendering is not measured by IDs/classes alone.
- Installer default assertions only check strings. bash -n is syntax validation. Several CSS checks assert literal spellings rather than computed geometry.
- Overlaps: suite 67 actual nested-dialog/menu paths; suite 62 installer strings; suite 65 editor geometry.
