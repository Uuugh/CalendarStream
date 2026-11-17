# Suite 62: Rule delete/move/link actions and installer source

Source: [`tests/suite_62.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Direct rules/link helper tests construct fixture Event/Ruleset values in New York time. Most later checks scan templates/scripts/styles/installer/compose as text, with bash -n syntax validation. Environment credentials are fixture values; the file accepts a database argument but creates no app server/TestClient/browser.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S62-01 | rules | The action-type map has the sampled Delete, Move and expanded Record changes labels. | [L25](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L25) |
| S62-02 | rules | A matching Delete action hides its event with a rule-prefixed deletion marker while the nonmatching event stays visible. | [L29](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L29) |
| S62-03 | rules | Moving by 90 minutes advances both sampled start and end by 90 minutes. | [L32](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L32) |
| S62-04 | rules | Moving by negative 30 minutes advances the sampled start to the earlier expected time. | [L34](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L34) |
| S62-05 | rules | Change replaces the title, Add appends a newline note while preserving the old prefix, and appends location text with a space. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L39) |
| S62-06 | rules | Failure sentinel: strict normalization accepting Add with empty text without RuleError fails. | [L42](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L42) |
| S62-07 | rules | The empty-Add case reaches a RuleError handler success marker. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L44) |
| S62-08 | rules | Change-title and change-notes actions have different shadow-kind identifiers. | [L45](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L45) |
| S62-09 | rules | A normalized link rule keeps its target UID, empty conditions and delete/move action types. | [L50](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L50) |
| S62-10 | events | Extracting link rules yields delete/move flags and the target UID for the owner event. | [L52](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L52) |
| S62-11 | rules | The sample link ruleset is empty or finishing the sampled event does not hide it. | [L53](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L53) |
| S62-12 | events | Event-template source omits Delete with it wording and contains linknote markup. | [L54](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L54) |
| S62-13 | rules | Combined page-script source contains THEN_HANDLE, thenDrag and hgrip strings. | [L58](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L58) |
| S62-14 | calendar | Calendar template source contains hide action/evhide strings and main source names Deleted by a rule. | [L62](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L62) |
| S62-15 | rules | Source-template text contains the new-rule button classes and reuse marker, without New rule menu wording. | [L66](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L66) |
| S62-16 | events | The sampled end-time template region contains label-line/checkbox/zone markup ordered checkbox before zone picker. | [L72](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L72) |
| S62-17 | events | Event-template source contains no label for end_tz. | [L74](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L74) |
| S62-18 | shell | The status-fold source includes the statusbox/countbox exclusion lookup. | [L78](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L78) |
| S62-19 | process | Installer source includes the current-path/subdomain default and a conflict-awareness phrase. | [L85](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L85) |
| S62-20 | process | Installer source includes the sampled existing-data-or-app-data folder expression. | [L86](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L86) |
| S62-21 | process | Installer source defaults updating to yes and has exactly two no-default assignment spellings. | [L87](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L87) |
| S62-22 | process | Installer/compose source includes the sampled stack numbering, prefixes, container names and port expression. | [L88](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L88) |
| S62-23 | process | bash -n returns zero for install.sh. | [L93](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_62.py#L93) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 06/07 pair a failure sentinel with an unconditional exception-handler marker; the marker alone cannot verify a requirement. Row 11 permits either an empty ruleset or one nonhidden sampled event, not proof over all events.
- Rows 12–22 mostly assert strings/file content rather than rendered interaction, installer prompts or actual multi-stack behavior. Row 12 excludes one old phrase, not both named phrases independently. Row 13 does not count/reorder actual Then handles.
- Delete/move checks inspect direct engine outputs, not serialized feed bodies. Negative movement checks start only. bash -n is syntax validation, not an installation.
- Overlaps: suites 36/37 rule/link logic; suite 63 source defaults; suite 66 installer strings.
