# Suite 63: Meetings, password rules, defaults and source power

Source: [`tests/suite_63.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Pure meeting/password/stream checks followed by Postgres-backed HTTPS TestClient operations; Demo.ics, patched background loops. Meeting Google bodies are built locally, not sent to Google. Later logo/CSS/JS checks inspect source/file existence. No browser.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S63-01 | events | Meeting-link extraction returns the sampled Zoom URL with its query intact. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L24) |
| S63-02 | events | Ordinary non-URL text produces no meeting link. | [L25](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L25) |
| S63-03 | google | The built Google description starts with the fixture Meet URL, blank line and original Agenda notes. | [L29](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L29) |
| S63-04 | google | Reading the built fields back yields Agenda or None, or a description without the Meet host. | [L31](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L31) |
| S63-05 | feeds | Feed source contains URL and notes_with_meeting strings. | [L32](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L32) |
| S63-06 | account | The sampled long mixed-character password has no unmet password rules. | [L36](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L36) |
| S63-07 | account | Each of five sampled deficient passwords has at least one unmet rule. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L38) |
| S63-08 | account | The sampled Bookkeeper password with doubled letters has no unmet rule. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L39) |
| S63-09 | account | Failure sentinel: setting the weak fixture password without LoginError fails. | [L41](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L41) |
| S63-10 | account | The weak-password setter reaches the LoginError handler success marker. | [L43](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L43) |
| S63-11 | feeds | The stream regex matches sampled one/six/128-character names and rejects 129 characters and an embedded space. | [L47](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L47) |
| S63-12 | sources | The initial local source is the default. | [L60](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L60) |
| S63-13 | sources | Page markup has one Default label and a default-source form action. | [L64](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L64) |
| S63-14 | sources | Selecting the second Local as default returns 200 and changes default_sid. | [L65](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L65) |
| S63-15 | sources | Selecting CCS+ as default returns 400. | [L66](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L66) |
| S63-16 | sources | Reordering the new default away from first leaves it the default. | [L68](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L68) |
| S63-17 | rules | Re-adding CCS+ with only the selected starter adds one CCS+-scoped 24-hour rule. | [L74](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L74) |
| S63-18 | rules | The page contains a no-end starter field or CCS+ remains in source IDs. | [L75](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L75) |
| S63-19 | sources | Page markup omits Empty this calendar and has a Remove-calendar control title. | [L78](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L78) |
| S63-20 | sources | The page has a source-power action and a switch role. | [L80](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L80) |
| S63-21 | sources | Turning the second Local off updates its off state and off-class module markup. | [L83](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L83) |
| S63-22 | feeds | If the sampled destination is a feed, turning it off makes its URL return 503. | [L87](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L87) |
| S63-23 | sources / feeds | Turning source/destination back on clears both off states. | [L89](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L89) |
| S63-24 | feeds | The destination's selected-source list remains equal to its earlier list. | [L90](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L90) |
| S63-25 | shell | The title template has light/dark logo mark classes and both corresponding asset files exist. | [L94](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L94) |
| S63-26 | shell | The old top-level app logo PNG path is absent. | [L96](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L96) |
| S63-27 | shell | The two/three-line stylesheet contains its width variable and display:none text. | [L98](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L98) |
| S63-28 | shell | The handle stylesheet includes sampled left-offset and opacity spellings. | [L101](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L101) |
| S63-29 | sources | The saving-script source contains reopenEvents. | [L103](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_63.py#L103) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 04 permits description None and has a hasattr fallback, so it is weaker than a full round-trip meeting/notes assertion. Row 05 scans source rather than serializing a feed.
- Password rows sample inputs with unmet conditions; they do not prove each named reason or all characters. Rows 09/10 are exception sentinel and unconditional success marker.
- Stream regex samples alphabetic names/lengths/space, not every permitted character despite its label. Row 18 can pass merely because CCS+ exists, without proving starter controls render.
- Row 15 targets the sampled CCS+ ID only. Power row 22 is conditional on destination type. Row 23 checks on-state, not all event preservation; row 24 separately compares source selections.
- Logo/CSS/script checks cannot establish actual grip/fold/reopen interactions. Row 13 proves one label and a route action, not a disabled appearance.
- Overlaps: suite 60 source transports; suite 62 rule starters; suites 65/67 hidden/default UI.
