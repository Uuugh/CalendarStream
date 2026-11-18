# Requirements: rules

The app's Rules: the rule model and engine, the rule dialog, All Rules, link rules. Issues against this feature
(GitHub, label `feature:rules`): I3, I35, I38, I40.

| ID | status | statement | test | was |
|---|---|---|---|---|
| RUL-01 | planned | "Link to" in the rule dialog is simplified to "Link to a Rule": it keeps its place in the dialog but uses the layout of the Sources > Rules subsection. | — | F60.1 |
| RUL-02 | planned | A new Then action, "Link to Event", links the rule to a specific event chosen with the existing date picker, alongside "Delete this event" and "Move this event". | — | F60.2 |
| RUL-03 | verified | A text condition matches by equality (trimmed), contains, whole word, prefix, suffix or regex; whole word `RDO` does not match `RDOS`. Case is ignored. | — | S36-01, S52-04 |
| RUL-04 | verified | `*` and `#` wildcards are supported: `*E####` matches `Trip E1234` and `e9999` but not `E12345`. | — | S49-04, S52-03 |
| RUL-05 | verified | A condition on "Any text" matches title, location or notes. | — | S49-09 |
| RUL-06 | verified | Conditions combine with AND/OR in order with optional brackets: `A OR B AND C` differs from `(A OR B) AND C`. | — | S36-02 |
| RUL-07 | verified | Day conditions cover selected days, a Fri-Mon range, after and before a day. | — | S36-08, S36-09 |
| RUL-08 | verified | A time range may be overnight (22:00-06:00 matches 23:00, not daytime). | — | S36-10 |
| RUL-09 | verified | Date conditions: a range (reversed order is accepted) and "after date". | — | S36-11 |
| RUL-10 | verified | Length conditions distinguish no end time, a normal event, a near whole-day event and an exact duration. | — | S36-12 |
| RUL-11 | verified | Actions: Color, Emoji, Change title, Change notes, Add text, Change length, Change time, Delete, Move, Add event, Record changes, link rules (delete/move). | — | S62-01, S62-09 |
| RUL-12 | verified | Color: the higher rule wins; a lower rule still adds its emoji; a second pass does not duplicate it; several emoji actions prefix the title in order. | — | S36-14, S49-08 |
| RUL-13 | verified | Change title replaces the title; Add appends (a new line for notes, a space for location). | — | S62-05 |
| RUL-14 | verified | Delete hides the event with a rule-labelled marker; non-matching events stay. | — | S62-02 |
| RUL-15 | verified | Move shifts start and end together, forward or back (+90, -30 minutes). | — | S62-03, S62-04 |
| RUL-16 | verified | Change length makes a near whole-day event all-day (keeping an original-time note) or shortens a normal one. | — | S36-13, S27-09, S27-13 |
| RUL-17 | verified | Add event creates a rule-origin event relative to the matching event (e.g. a Prep event 08:00-08:45, an hour before), from an existing event template. | — | S36-15, S26-19 |
| RUL-18 | verified | Record changes remembers later edits to a matching event and annotates it ("Changed ... time"). | — | S33-11, S33-12 |
| RUL-19 | verified | A rule with no actions is refused (400). | — | S27-12 |
| RUL-20 | verified | A malformed regex, unmatched bracket, incomplete date range or empty Add is refused with a clear message; unmatched brackets are cleared when not strict. | — | S36-03..07, S40, S49-07, S62-06, S62-07 |
| RUL-21 | verified | Maximum conditions and actions per rule are enforced with a message naming the limit; a rule at the limit saves. | — | S52-07..11 |
| RUL-22 | verified | A regex that could take too long is stopped within a second with "Too slow"; the regex tester reports an invalid pattern, match spans and highlights the match. | — | S52-01, S52-05, S52-06, S49-05, S49-06, S49-56 |
| RUL-23 | verified | An Add-event rule naming a template that does not exist, with no title, is refused. | — | S26-26 |
| RUL-24 | verified | A rule applies to all calendars or to chosen ones; unapplying removes it from that calendar and keeps it in All Rules. | — | S21-17, S21-18, S26-22..24, S33-06, S33-08 |
| RUL-25 | verified | A new calendar-specific rule is first in that calendar's list; an all-calendar rule goes last; renaming a calendar keeps its rules. | — | S19-25, S19-26, S36-16, S36-38 |
| RUL-26 | verified | Rules can be reordered (up/down, before/after a neighbour) and the order is stored and shown. | — | S34-17, S34-18, S36-17, S36-39 |
| RUL-27 | verified | A rule can be cloned; the clone is unapplied and placed right after the original. | — | S33-10, S36-41 |
| RUL-28 | verified | Deleting a rule removes it from every list. | — | S19-27, S27-10 |
| RUL-29 | verified | A calendar starts with two predefined rules (items without an end time, 24-hour events), kept in All Rules like any rule. Removing one from a calendar only unassigns it: it stays in All Rules and can be assigned again (Developer, Nov 17). Adding CCS+ again re-assigns its starters. The 24-hour rule aligns a whole-day event to the local day: an event spanning about 24 hours becomes all-day, local midnight to the next local midnight in the event's time zone, so daylight-saving days stay correct. | — | S21-13, S27-08, S63-17 |
| RUL-30 | verified | A rule whose calendar was removed still shows the saved name; a rule with no calendar says so. | — | S67-07..09 |
| RUL-31 | verified | All Rules reports a higher rule that shadows a lower one's color, and duplicate rules, with the choices Put first, Keep as is, Drop and Merge. | — | S37-01..03, S37-08..12 |
| RUL-32 | verified | Merging rules unions their calendars (All if any is All). | — | S37-04, S49-29 |
| RUL-33 | verified | Saving a condition identical to an existing rule offers Save as new or Merge; the stored count does not change until chosen. | — | S37-42..47 |
| RUL-34 | verified | An unknown conflict key is refused (400). | — | S37-13 |
| RUL-35 | verified | Legacy tag-colors and defaults migrate to rules (RDO, VAC color and a 120-minute no-end action), keeping IDs and order, then the legacy records are removed. | — | S29-06, S29-07, S36-18, S37-06, S37-07 |
| RUL-36 | verified | The rule dialog opens from "New rule…" in a calendar (that calendar preselected) or from All Rules (All preselected); dialog behavior follows UI-02. | — | S21-15, S37-33..36, S37-41, S67-15, S67-16 |
| RUL-37 | verified | Each action asks for what it needs: minutes for Change length, a title or an event template for Add event, a color for Color (UI-10). | — | S37-37, S37-38, S40-09..11 |
| RUL-39 | verified | A rule shows which calendars it applies to: All, one calendar, or several (with the count). | — | S38-05, S38-06, S33-07, S33-09 |
| RUL-40 | verified | A rule shows its title (if any), what it does, and its color by name. | — | S40-01, S40-02, S66-17, S45-26 |
| RUL-41 | verified | How rules work is explained from the rule dialog. | — | S33-24, S38-01, S38-03, S38-04, S38-13, S21-23 |
| RUL-43 | verified | An Emoji action lets the user find and choose any emoji by searching (UI-11). | — | S44-41 |
| RUL-44 | verified | A typed regex is checked for legality as it is typed or saved; when it is not legal, the site says why and highlights the broken part of the pattern. Regexes use Dart (ECMAScript) syntax; Python-only syntax is not supported. | packages/domain/test/rules/text_matching_test.dart | Developer, Nov 17 |
