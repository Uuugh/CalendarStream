# Suite 44: Theme measurements and clarification mapping

Source: [`tests/suite_44.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8106; seed.demo; fake work.ics download and update checker; patched loops. The first browser matrix is light/dark × 1230/390px, opening Rules/Templates. Additional interaction/geometry checks are mostly desktop, some light-only. A later page uses the current New York month and disables animation for positioning. The final scan reads the pinned theme.md Clarifications text.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S44-01 | shell | In each palette/width combination, document scroll width does not exceed the viewport. | [L93](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L93) |
| S44-02 | shell | Computed body and note font sizes are 14px and 13px. | [L101](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L101) |
| S44-03 | shell | The sampled top icon measures 34×34px and legend margin-top is 5px. | [L103](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L103) |
| S44-04 | shell | The three sampled anchored menus each have 12px padding and top-left radius. | [L105](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L105) |
| S44-05 | shell | Contrast computed from muted/card/background/soft hex tokens is at least 4.5:1 on all three sampled surfaces. | [L119](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L119) |
| S44-06 | shell | Module header measurements are nonempty and are 50px at desktop or at least 50px on phone. | [L122](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L122) |
| S44-07 | shell | Measured module kind text is above its name, has minimum 17px desktop/15px phone font, no top border and no nested input. | [L124](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L124) |
| S44-08 | sources / feeds / rules | At desktop width, measured rows are nonempty, module right edges align with header plus and handles lie between section left and module left. | [L128](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L128) |
| S44-09 | shell | Each measured singleton list handle has visibility hidden. | [L130](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L130) |
| S44-10 | shell | The nonempty sampled status-button set has the expected syncnow/state-span pattern or an upgradebtn class. | [L132](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L132) |
| S44-11 | sources / feeds | Sampled status lines match the allowed last-sync/failure/read/check spellings and page source omits Last check was. | [L135](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L135) |
| S44-12 | shell | Each measured copy button is nested within an inbox or feed container. | [L138](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L138) |
| S44-13 | shell | In light contexts, the background token is #f7f6f3. | [L141](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L141) |
| S44-14 | shell | No pageerror events are collected during each sampled palette/width load. | [L142](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L142) |
| S44-15 | rules / event_templates | In light desktop, count/plus controls satisfy the sampled top/right offsets and each section has no sfoot. | [L148](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L148) |
| S44-16 | sources | The Work name line has one note dot with its fixture note, and CCS+ tooltip text has no Note label. | [L151](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L151) |
| S44-17 | rules | The page contains the checked Color swatch and Tomato-name markup. | [L155](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L155) |
| S44-18 | sources | Each of two Sync Now presses reaches syncing or done at the sampled 150ms observation. | [L160](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L160) |
| S44-19 | settings | Each of two Check now presses reaches syncing while the status-chip opacity is below 0.1 at the sampled observation. | [L166](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L166) |
| S44-20 | settings | Every sampled Updates fixed-text element has transparent computed background. | [L171](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L171) |
| S44-21 | shell | The status-chip set is nonempty and every chip's text matches the regex for its good/run/warn/bad meaning class. | [L175](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L175) |
| S44-22 | shell | The filtered page-text scan reports no sampled sentence segment over twenty space-separated words. | [L176](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L176) |
| S44-23 | feeds | After removing other destinations, exactly one destination remains and its handle is hidden. | [L183](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L183) |
| S44-24 | shell | The expanded Rules arrow has a transform matrix whose second component starts with -1. | [L188](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L188) |
| S44-25 | calendar | The opened event's Close/icon insets are at most 9px, differ by at most 2px, include one Link tool and satisfy sampled row alignment. | [L199](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L199) |
| S44-26 | events | Delete confirmation opens with a block note and a 130×34px No/Yes button pair. | [L209](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L209) |
| S44-27 | events | The edit-dialog backdrop is rgba(0,0,0,0.55) with popin animation and duration 0.2s. | [L213](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L213) |
| S44-28 | events | The embedded editor's button pair rounds to 130×34px. | [L216](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L216) |
| S44-29 | sources | Adding Local shows Cancel and Save controls and no button with Add text in the sampled source dialog. | [L220](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L220) |
| S44-30 | sources | Cancelling that add flow hides the source dialog. | [L223](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L223) |
| S44-31 | sources / feeds | Each sampled source/feed plus opens a horizontally centered modal whose backdrop filter contains blur. | [L230](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L230) |
| S44-32 | event_templates | Event Templates plus opens a modal dialog. | [L234](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L234) |
| S44-33 | shell | The first module has 1px top border, 5px top padding and 9px left padding. | [L243](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L243) |
| S44-34 | sources | The sampled folded source label has transparent top-border color and background. | [L244](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L244) |
| S44-35 | shell | The nonzero module count equals the number of note dots in module name lines. | [L245](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L245) |
| S44-36 | shell | No free color input exists and every palette popup has eleven non-nocolor buttons. | [L246](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L246) |
| S44-37 | feeds | Every sampled main date input is inside a date range with All, or inside destination dates. | [L247](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L247) |
| S44-38 | sources | Every sampled source body has an import form containing a file field and a final button. | [L248](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L248) |
| S44-39 | shell | The scanned page-script modules and event template contain no calls matching the alert/confirm/prompt regex. | [L250](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L250) |
| S44-40 | shell | Those scanned sources omit the two disallowed danger-class string spellings. | [L251](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L251) |
| S44-41 | rules | The emoji picker has ten columns, auto vertical overflow, its search placeholder, over 1000 items and a numeric radius below the pill threshold. | [L261](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L261) |
| S44-42 | calendar | After deletion, the sampled imported event has deleted class, struck-through summary, grayscale filter, Restore tool and deletion-origin note. | [L271](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L271) |
| S44-43 | sources | The sampled folded note dot starts 0–4px after the label and above its top. | [L285](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L285) |
| S44-44 | calendar | Today's sampled cell box-shadow contains inset and a 2px spelling. | [L286](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L286) |
| S44-45 | events | The embedded editor places Notes right of Title, corner tools at header right, link section below Notes, button pair right-aligned, link panels hidden and iframe height within 1px of main. | [L294](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L294) |
| S44-46 | shell | A synthetic tooltip opens aligned to its icon's left edge and below the icon. | [L308](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L308) |
| S44-47 | shell | A synthetic right-edge tooltip ends at viewport right while keeping the sampled top position. | [L309](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L309) |
| S44-48 | shell | A synthetic bottom-edge tooltip ends at viewport bottom and aligns to its icon's left edge. | [L310](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L310) |
| S44-49 | feeds | The nonempty sampled tooltip set inside Add feed stays within its right/bottom dialog bounds. | [L315](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L315) |
| S44-50 | shell | The filtered flow-spacing scan of open module bodies finds no gap differing from 5px or 1px after a label. | [L339](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L339) |
| S44-51 | shell | The sampled sibling sections satisfy 5px/14px gap logic and all modules have 9px side/5px top padding. | [L345](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L345) |
| S44-52 | shell | At least ten popup dialogs are found and all four computed padding values are 12px for each. | [L353](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L353) |
| S44-53 | shell | The filtered flow-spacing scan over those dialogs finds no gap violations. | [L354](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L354) |
| S44-54 | feeds | The sampled destination date fields have 1px heading gap, 5px vertical/label gaps and aligned input left edges. | [L365](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L365) |
| S44-55 | feeds | The sampled app-link buttons all match their container width, which equals intrinsic Google-button width. | [L366](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L366) |
| S44-56 | feeds | The Include source-pick lists are nonempty and all sampled items stack with the same x position and 5px gaps. | [L367](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L367) |
| S44-57 | feeds | After cloning two choices, the wide source picker has columns of three and two items; constraining width yields one column of five. | [L379](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L379) |
| S44-58 | process | Every scanned Clarifications bullet matches some configured keyword string in the suite's coverage-name map. | [L444](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_44.py#L444) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 01–14 are within the four-context matrix, with desktop/light-only exceptions noted in the rows. Rows 15–22 are light desktop only, with some repeated presses/sections. Most later checks run outside that matrix; do not claim every interaction is tested in every palette/width.
- Several all() or JavaScript every() predicates permit empty measured sets (singleton handles, copy buttons, palette/date/import/spacing subsets). Contrast uses token hex values, not composited pixels for every real text element.
- Row 10's OR permits upgradebtn regardless of the syncnow/state-span test. Row 12 establishes DOM ancestry, not exact field geometry. Row 20 checks transparent backgrounds rather than border absence.
- The filtered text/spacing scanners skip many DOM categories and cannot establish blanket prose/spacing compliance. Row 27 checks CSS animation names/duration rather than actual scale/fade frames; later positioning disables animation.
- Row 33 measures the first module only, notwithstanding the legacy label. Row 37 permits destdates inputs without explicitly asserting an All control there. Row 38 checks import file-field/final-button structure, not every heading.
- Row 39 is a source regex scan, not proof that no browser dialog can ever be triggered. Row 40 bans two class spellings, not all incorrect danger styling.
- Row 44 checks a shadow's inset/2px text but not the accent color. Row 49 checks sampled right/bottom tooltip bounds only. Row 56 explicitly requires boolean true, so its diagnostic-string fallback does not pass.
- Row 58 only checks keyword coverage of clarification bullet text; it does not prove an assertion executes for every clarification, and the map explicitly delegates many entries to later suites. Treat it as a mapping check, not behavioral verification of all theme rules.
- Overlaps: suites 35/41 layout; suites 46/47 controls; suite 45 colors; later suites referenced by the clarification map.
