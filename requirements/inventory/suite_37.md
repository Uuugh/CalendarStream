# Suite 37: Rule conflicts, linked events, removal and rule-dialog choices

Source: [`tests/suite_37.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure helper checks use normalized synthetic rules and link date/time values. Integration uses Postgres, app server 8093, seed.demo and fake work.ics download with a controllable delay; background loops patched. Chromium runs at 1400×900. A newer update offer is patched for a markup check.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S37-01 | rules | The fixture conflicts are exactly one color-shadow pair and two duplicate pairs, with the shadow limited to CCS+. | [L34](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L34) |
| S37-02 | rules | With the first conflict key ignored, the first remaining conflict is a duplicate. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L36) |
| S37-03 | rules | A conditionless higher rule is reported as shadowing the sampled lower rule. | [L37](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L37) |
| S37-04 | rules | Merging sampled rules unions explicit calendars, or yields all if one scope is all. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L38) |
| S37-05 | events | The helper computes a 90-minute timed move, returns None for mixed date/timed types and shifts both all-day endpoints by two days. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L39) |
| S37-06 | rules | The converted no-end rule becomes apply=all and appears in Local's effective list. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L53) |
| S37-07 | rules | Migrating a rule subscribed by the sole source yields apply=all. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L55) |
| S37-08 | rules | All Rules renders the color-shadow warning, put-first instruction, Keep as is and to-check text. | [L60](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L60) |
| S37-09 | rules | Resolving up returns 303 and puts the sampled duplicate rule first in CCS+'s list. | [L63](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L63) |
| S37-10 | rules | Resolving drop removes the other RDO condition rule that had only the conflicting action. | [L67](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L67) |
| S37-11 | rules | The duplicate fixture renders is the same as and Merge them text. | [L70](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L70) |
| S37-12 | rules | Resolving merge leaves one lowercase-rdo rule applied to both fixture sources. | [L74](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L74) |
| S37-13 | rules | Resolving the unknown key nope returns HTTP 400. | [L75](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L75) |
| S37-14 | events | Saving the linked Pack event records its target trip UID and CCS+ target-source key. | [L81](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L81) |
| S37-15 | events | Its editor contains the link box, target UID field and active event-link segment. | [L83](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L83) |
| S37-16 | calendar | The calendar page includes Linked to plus the sampled target title. | [L84](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L84) |
| S37-17 | events | After moving the target two hours, the linked event start also moves two hours. | [L90](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L90) |
| S37-18 | events | Deleting the target removes Pack and its link record. | [L92](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L92) |
| S37-19 | events | Linking the sampled imported event alone does not add its UID to stored edits. | [L97](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L97) |
| S37-20 | sources | Removing Work with merge-into-new returns 303 and removes its original source ID. | [L102](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L102) |
| S37-21 | sources | The new Work local source has the prior event count/color and belongs to every prior destination that used Work. | [L104](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L104) |
| S37-22 | sources | Merging that local source into Local returns 303 and leaves at least the prior event count there. | [L106](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L106) |
| S37-23 | sources | The sampled removal with keep=nope returns HTTP 400. | [L107](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L107) |
| S37-24 | settings | The Settings substring contains loginform and domainsform, no okslot-class occurrences and no adminmail text. | [L111](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L111) |
| S37-25 | settings | With no offered version, Settings contains Check now and no upgradebtn. | [L112](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L112) |
| S37-26 | settings | With available patched to a newer version, Settings has upgradebtn and omits Check now. | [L116](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L116) |
| S37-27 | shell | No measured visible help-dot gap exceeds 12px in the sampled opened sections. | [L130](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L130) |
| S37-28 | sources | With source Configure folded, the CCS+ color picker has pointer-events none. | [L133](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L133) |
| S37-29 | sources | Expanding Configure changes its pointer-events away from none. | [L135](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L135) |
| S37-30 | sources | When collapsed, the source status rectangle lies horizontally within the right header rectangle (one-pixel tolerance). | [L140](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L140) |
| S37-31 | sources | During delayed sync, the chip opacity is zero and the sync button is taller than status-box height minus 12px. | [L146](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L146) |
| S37-32 | sources | After the sync delay, the status chip is visible again. | [L148](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L148) |
| S37-33 | rules | A rule created from CCS+ starts with only CCS+ selected and the source name on its dropdown button. | [L151](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L151) |
| S37-34 | rules | Opening Apply to shows the dropdown and one swatch entry per source plus one. | [L154](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L154) |
| S37-35 | rules | Selecting All after another source leaves only all checked. | [L156](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L156) |
| S37-36 | rules | Escape closes the Apply to menu while leaving the rule dialog open. | [L158](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L158) |
| S37-37 | rules | Choosing Change to length shows its minute input with 1:00. | [L162](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L162) |
| S37-38 | rules | Choosing Create event and a blank template shows the new-event title field. | [L165](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L165) |
| S37-39 | rules | Adding a lone closing bracket sets the first condition opening count, adds a flashing opening bracket and leaves the form balanced. | [L170](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L170) |
| S37-40 | rules | The second condition's closing-bracket controls are active then spare in that order. | [L173](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L173) |
| S37-41 | rules | A rule opened from All Rules starts with only all checked. | [L176](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L176) |
| S37-42 | rules | Saving the first synthetic duplicate-test condition increases the rule count by one. | [L183](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L183) |
| S37-43 | rules | Saving the same condition again displays one duplicate-offer message and leaves the dialog open. | [L187](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L187) |
| S37-44 | rules | While that duplicate offer is shown, the stored rule count has not increased. | [L189](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L189) |
| S37-45 | rules | Choosing Save as new increases the count to two above baseline. | [L191](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L191) |
| S37-46 | rules | A third identical submission again displays one duplicate-offer message. | [L195](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L195) |
| S37-47 | rules | Choosing Merge on that submission leaves the count at two above baseline. | [L197](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L197) |
| S37-48 | sources | The Remove dialog opens with merge selected and the source itself disabled as a merge target. | [L200](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L200) |
| S37-49 | sources | Closing the Remove dialog hides it and leaves CCS+ in source IDs. | [L203](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L203) |
| S37-50 | events | The linkevent control is hidden for the new event page. | [L206](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L206) |
| S37-51 | events | Choosing Event linking opens the picker and exposes more than five event buttons. | [L208](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L208) |
| S37-52 | events | Picking an event makes the linkevent control and link note visible. | [L210](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L210) |
| S37-53 | shell | No browser pageerror events are collected during the sampled interactions. | [L212](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_37.py#L212) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 02 checks the first remaining conflict is duplicate, not a full list excluding every ignored key. Row 13 posts an arbitrary unknown key, rather than replaying an actual previously resolved key.
- Row 17 checks linked start-time movement only; no direct linked-end assertion. Row 21 checks event count/color/destination membership, not each merged event field. Row 22 permits at least the old count and does not independently prove source removal.
- Row 23 targets a source already removed earlier, so the 400 does not isolate invalid keep-choice validation.
- Settings row 24 checks form IDs and absent text, not every pair's controls. Color-picker rows 28/29 inspect pointer-events, not persistence after choosing a color.
- Row 27 treats missing previous siblings as gap zero and an empty measured set can pass. Row 31 checks button height only, not full width. Row 32 asserts chip visibility rather than exact Healthy text.
- Row 34 checks swatch entry count, not each calendar's displayed color. Duplicate Merge row 47 checks count only, not the final rule scope/actions.
- Row 48 checks merge default and a disabled self-target; it does not assert every removal option. Row 52 checks link UI visibility only; no save of a generated link rule is asserted in that browser path.
- Overlaps: suite 36 rule engine/Local; suite 33 shared scopes; suite 38 conflict badges; suite 28 verification UI.
