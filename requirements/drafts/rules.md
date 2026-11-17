# DRAFT requirements: rules (for the Developer's approval)

Not approved. Written by Claude from the 169 `rules` rows of `requirements/inventory/` (suites 12-71, pinned to
d70343f). Each row says what the Python app's own tests already check; on approval a row moves to
`requirements/rules.md` as `verified`, with its test column pointing at the Dart test that replaces the Python check.
`Evidence` = inventory keys. Rows marked **(?)** need a decision (see `build_rules/open-questions.md`). Pure layout
measurements (pixels, offsets, opacity) are left to the theme and not turned into requirements: **(Q-R1)**.

Existing in `requirements/rules.md`: RUL-01, RUL-02 (from the Developer's F60). Numbering continues from RUL-03.

## Matching (domain)

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-03 | proposed | A text condition matches by equality (trimmed), contains, whole word, prefix, suffix or regex; whole word `RDO` does not match `RDOS`. Case is ignored. | S36-01, S52-04 |
| RUL-04 | proposed | `*` and `#` wildcards are supported: `*E####` matches `Trip E1234` and `e9999` but not `E12345`. | S49-04, S52-03 |
| RUL-05 | proposed | A condition on "Any text" matches title, location or notes. | S49-09 |
| RUL-06 | proposed | Conditions combine with AND/OR in order with optional brackets: `A OR B AND C` differs from `(A OR B) AND C`. | S36-02 |
| RUL-07 | proposed | Day conditions cover selected days, a Fri-Mon range, after and before a day. | S36-08, S36-09 |
| RUL-08 | proposed | A time range may be overnight (22:00-06:00 matches 23:00, not daytime). | S36-10 |
| RUL-09 | proposed | Date conditions: a range (reversed order is accepted) and "after date". | S36-11 |
| RUL-10 | proposed | Length conditions distinguish no end time, a normal event, a near whole-day event and an exact duration. | S36-12 |

## Actions (domain)

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-11 | proposed | Actions: Color, Emoji, Change title, Change notes, Add text, Change length, Change time, Delete, Move, Add event, Record changes, link rules (delete/move). | S62-01, S62-09 |
| RUL-12 | proposed | Color: the higher rule wins; a lower rule still adds its emoji; a second pass does not duplicate it; several emoji actions prefix the title in order. | S36-14, S49-08 |
| RUL-13 | proposed | Change title replaces the title; Add appends (a new line for notes, a space for location). | S62-05 |
| RUL-14 | proposed | Delete hides the event with a rule-labelled marker; non-matching events stay. | S62-02 |
| RUL-15 | proposed | Move shifts start and end together, forward or back (+90, -30 minutes). | S62-03, S62-04 |
| RUL-16 | proposed | Change length makes a near whole-day event all-day (keeping an original-time note) or shortens a normal one. | S36-13, S27-09, S27-13 |
| RUL-17 | proposed | Add event creates a rule-origin event relative to the matching event (e.g. a Prep event 08:00-08:45, an hour before), from an existing event template. | S36-15, S26-19 |
| RUL-18 | proposed | Record changes remembers later edits to a matching event and annotates it ("Changed ... time"). | S33-11, S33-12 |

## Saving and limits

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-19 | proposed | A rule with no actions is refused (400). | S27-12 |
| RUL-20 | proposed | A malformed regex, unmatched bracket, incomplete date range or empty Add is refused with a clear message; unmatched brackets are cleared when not strict. | S36-03..07, S40, S49-07, S62-06, S62-07 |
| RUL-21 | proposed | Maximum conditions and actions per rule are enforced with a message naming the limit; a rule at the limit saves. | S52-07..11 |
| RUL-22 | proposed | A regex that could take too long is stopped within a second with "Too slow"; the regex tester reports an invalid pattern, match spans and highlights the match. | S52-01, S52-05, S52-06, S49-05, S49-06, S49-56 |
| RUL-23 | proposed | An Add-event rule naming a template that does not exist, with no title, is refused. | S26-26 |

## Scope, order and sharing

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-24 | proposed | A rule applies to all calendars or to chosen ones; unapplying removes it from that calendar and keeps it in All Rules. | S21-17, S21-18, S26-22..24, S33-06, S33-08 |
| RUL-25 | proposed | A new calendar-specific rule is first in that calendar's list; an all-calendar rule goes last; renaming a calendar keeps its rules. | S19-25, S19-26, S36-16, S36-38 |
| RUL-26 | proposed | Rules can be reordered (up/down, before/after a neighbour) and the order is stored and shown. | S34-17, S34-18, S36-17, S36-39 |
| RUL-27 | proposed | A rule can be cloned; the clone is unapplied and placed right after the original. | S33-10, S36-41 |
| RUL-28 | proposed | Deleting a rule removes it from every list. | S19-27, S27-10 |
| RUL-29 | proposed | A calendar starts with two predefined rules (items without an end time, 24-hour events); adding CCS+ again re-adds its starters. | S21-13, S27-08, S63-17 |
| RUL-30 | proposed | A rule whose calendar was removed still shows the saved name; a rule with no calendar says so. | S67-07..09 |

## Conflicts and duplicates

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-31 | proposed | All Rules reports a higher rule that shadows a lower one's color, and duplicate rules, with the choices Put first, Keep as is, Drop and Merge. | S37-01..03, S37-08..12 |
| RUL-32 | proposed | Merging rules unions their calendars (All if any is All). | S37-04, S49-29 |
| RUL-33 | proposed | Saving a condition identical to an existing rule offers Save as new or Merge; the stored count does not change until chosen. | S37-42..47 |
| RUL-34 | proposed | An unknown conflict key is refused (400). | S37-13 |

## Older data

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-35 | proposed (?) | Legacy tag-colors and defaults migrate to rules (RDO, VAC color and a 120-minute no-end action), keeping IDs and order, then the legacy records are removed. | S29-06, S29-07, S36-18, S37-06, S37-07 |

## Dialog and page (UI)

| ID | status | statement | evidence |
|---|---|---|---|
| RUL-36 | proposed | The rule dialog opens from "New rule…" in a calendar (that calendar preselected) or from All Rules (All preselected); Escape closes the Apply to menu first, then the dialog. | S21-15, S37-33..36, S37-41, S67-15, S67-16 |
| RUL-37 | proposed | Choosing an action reveals its inputs (minutes, new-event title); the colour action is a palette of eleven named colours. | S37-37, S37-38, S40-09..11 |
| RUL-38 | proposed | Bracket controls keep the condition form balanced. | S37-39, S37-40 |
| RUL-39 | proposed | Badges show All or the calendar colour; a shared rule shows a striped two-colour badge and "N calendars". | S38-05, S38-06, S33-07, S33-09 |
| RUL-40 | proposed | A rule's label shows its title and what it does; the colour with name; long names truncate with the full name in a tooltip. | S40-01, S40-02, S66-17, S45-26 |
| RUL-41 | proposed | Rules and templates sections show a count box and one plus control; bodies stay hidden until expanded. "How rules work" lives in the dialog. | S33-24, S38-01, S38-03, S38-04, S38-13, S21-23 |
| RUL-42 | proposed (?) | The rule dialog fits a 390 px phone screen. | S36-56 |
| RUL-43 | proposed | The emoji picker has search and more than 1000 emoji. | S44-41 |

Not requirements: Failure-sentinel rows (S36-04, S36-06, S52-07, S52-09, S62-06) are test mechanics; source-text checks
(S62-13, S62-15, S66-21, S67-06) test the Python implementation and have no Dart counterpart.
