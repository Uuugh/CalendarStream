# Suite 67: Status vanish, nested dialogs, Domains and icon menus

Source: [`tests/suite_67.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8167; seed.demo; all background loops patched. Several 1230×900 Chromium pages exercise retention feedback, nested dialogs, public-address rows, view/theme menus and legend controls. Client check and public address are seeded for redirect guidance. Master logo/file/docs checks follow browser interactions.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S67-01 | shell | Status-fold source contains vanish and data-fold-vanish markers. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L39) |
| S67-02 | shell | Status-fold source contains the gone-class addition. | [L40](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L40) |
| S67-03 | shell | Macro source includes keep=True and the data-fold-vanish attribute. | [L42](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L42) |
| S67-04 | history | History template source includes keep=False. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L44) |
| S67-05 | shell | The gone-selector CSS suffix includes reduced-motion handling text. | [L46](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L46) |
| S67-06 | rules | Page-route source uses rule_used for non-all rule scopes in the sampled expression. | [L52](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L52) |
| S67-07 | rules | A rule with a stale source ID does not show No calendar yet in its badge substring. | [L61](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L61) |
| S67-08 | rules | That badge still displays the saved removed-calendar name. | [L62](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L62) |
| S67-09 | rules | A rule whose scope was genuinely empty displays No calendar yet. | [L66](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L66) |
| S67-10 | history | Immediately after saving retention, its confirmation mark exists and is not hidden. | [L81](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L81) |
| S67-11 | history | After the sampled hold, its class includes shrunk. | [L84](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L84) |
| S67-12 | history | After another hold, the mark is removed or hidden with gone class. | [L87](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L87) |
| S67-13 | events | Clicking the sampled day opens a new-event dialog. | [L95](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L95) |
| S67-14 | events | Starting a new event-derived rule closes the event dialog. | [L101](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L101) |
| S67-15 | rules | The corresponding rule dialog opens. | [L102](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L102) |
| S67-16 | rules | Escape closes that rule dialog. | [L105](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L105) |
| S67-17 | events | Escape restores the event dialog. | [L106](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L106) |
| S67-18 | settings | Deleting the main domain row while an extra exists leaves one main input. | [L117](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L117) |
| S67-19 | settings | Exactly one visible add-address control remains. | [L119](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L119) |
| S67-20 | settings | The cleared main public-address input value is empty. | [L121](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L121) |
| S67-21 | settings | With an extra row present, the visible add control's parent is not the main domain row. | [L128](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L128) |
| S67-22 | settings | Removing that extra row leaves one address row. | [L132](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L132) |
| S67-23 | settings | The main row's add control is visible again. | [L134](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L134) |
| S67-24 | google | Before the public-address edit, seeded healthy Google settings has no assist box. | [L145](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L145) |
| S67-25 | settings | Saving a changed public address opens the notice dialog. | [L150](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L150) |
| S67-26 | google | Its notice text mentions redirect URI and Google Calendar API Sync. | [L152](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L152) |
| S67-27 | google | The same page has one Google assist box after saving. | [L153](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L153) |
| S67-28 | settings | Clicking the notice button closes it. | [L157](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L157) |
| S67-29 | settings | The first Settings group is pagelogin. | [L168](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L168) |
| S67-30 | settings | Settings group order is Login, Domains, Updates, Theme, Google. | [L169](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L169) |
| S67-31 | settings | The Theme group's sampled heading contains Theme. | [L172](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L172) |
| S67-32 | settings | The page omits the former Appearance heading text. | [L173](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L173) |
| S67-33 | settings | Up-to-date Updates chip markup has a title naming the running version. | [L174](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L174) |
| S67-34 | calendar | The page has view button/menu IDs and no old native viewpick ID. | [L179](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L179) |
| S67-35 | calendar | All four view choices have menuitemradio markup. | [L181](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L181) |
| S67-36 | calendar | The view menu starts hidden. | [L189](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L189) |
| S67-37 | calendar | Clicking the view button unhides its menu. | [L191](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L191) |
| S67-38 | calendar | The sampled view-menu icon x positions form one unique value. | [L195](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L195) |
| S67-39 | calendar | Choosing Week hides the view menu again. | [L198](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L198) |
| S67-40 | calendar | Choosing Week renders one hourview. | [L199](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L199) |
| S67-41 | calendar | The full-page button is not pressed before the normal-view legend check. | [L204](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L204) |
| S67-42 | calendar | Clicking the CCS+ legend item in normal mode changes pressed to false. | [L207](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L207) |
| S67-43 | shell | The theme menu starts hidden. | [L211](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L211) |
| S67-44 | shell | Clicking the theme control unhides its menu. | [L214](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L214) |
| S67-45 | shell | The sampled theme-menu icon x positions form one unique value. | [L216](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L216) |
| S67-46 | shell | Choosing Dark hides the menu. | [L219](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L219) |
| S67-47 | shell | Choosing Dark sets the root data-theme to dark. | [L220](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L220) |
| S67-48 | shell | The closed theme button's HTML changes after choosing Dark. | [L222](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L222) |
| S67-49 | shell | The Dark menu choice has aria-checked=true. | [L223](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L223) |
| S67-50 | calendar | The calendar body contains the stretch control. | [L228](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L228) |
| S67-51 | calendar | The sampled legend separator gap is below twenty pixels. | [L234](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L234) |
| S67-52 | calendar | View All is absent before dimming an item. | [L235](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L235) |
| S67-53 | calendar | View All appears after dimming CCS+. | [L237](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L237) |
| S67-54 | calendar | Clicking View All restores the CCS+ pressed attribute true. | [L240](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L240) |
| S67-55 | calendar | View All disappears again after restoration. | [L241](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L241) |
| S67-56 | shell | Each of eight named master logo assets exists under the source-logo folder. | [L250](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L250) |
| S67-57 | shell | Each corresponding old build_rules logo path is absent. | [L251](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L251) |
| S67-58 | documentation | README source uses the moved mark path and omits its old build_rules prefix. | [L253](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L253) |
| S67-59 | documentation | README2 source uses the moved logo path and omits its old build_rules prefix. | [L255](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L255) |
| S67-60 | process | Both Theme Rules picture files still exist under build_rules. | [L258](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_67.py#L258) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Source markers/macros/comments do not independently prove conditional behavior; rows 10–12 separately observe one History confirmation at finite waits. Reduced motion is a source check, not an emulated browser setting.
- The stale-calendar fixture is directly seeded; it does not exercise every actual removal path. The nested-dialog test checks open flags, not typed unsaved-field preservation despite the label.
- Address-assist checks seed healthy client state and inspect a notice/assist node, not a live Google client update. No reload events are directly recorded for the no-reload claim.
- Menu icon alignment has a nonempty unique-value requirement but only one desktop width. Separator-gap test has no lower bound. Legend off/restore assertions inspect pressed attributes rather than all displayed event contents.
- Logo rows 56/57 each repeat across eight files. Picture existence does not make those diagrams authoritative/current visual specifications.
- Overlaps: suite 61 folding/feedback; suites 64/65 calendar views; suite 58 History/defaults; suite 66 Settings source checks.
