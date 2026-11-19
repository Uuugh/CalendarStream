# Requirements: rules

The app's Rules: the rule model and engine, the rule dialog, All Rules, link rules.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| RUL-01 | proposed | A rule has conditions that decide which events it matches. | — | — |
| RUL-01.a | proposed | A text condition matches by equality (trimmed), contains, whole word, prefix, suffix or regex; whole word `RDO` does not match `RDOS`. Case is ignored. | — | S36-01, S52-04 |
| RUL-01.b | proposed | `*` and `#` wildcards are supported: `*E####` matches `Trip E1234` and `e9999` but not `E12345`. | — | S49-04, S52-03 |
| RUL-01.c | proposed | The wildcard ? matches exactly one character in a text pattern (RUL-01). | — | readme_gaps:67, changelog_gaps_601-900:37 |
| RUL-01.d | proposed | A condition on "Any text" matches title, location or notes. | — | S49-09 |
| RUL-01.e | proposed | Conditions combine with AND/OR in order with optional brackets: `A OR B AND C` differs from `(A OR B) AND C`. | — | S36-02 |
| RUL-01.f | proposed | Day conditions cover selected days, a Fri-Mon range, after and before a day. Conditions on days and times are judged in the event's own time zone: a rule has no time zone of its own. | — | S36-08, S36-09 |
| RUL-01.g | proposed | A time range may be overnight (22:00-06:00 matches 23:00, not daytime). | — | S36-10 |
| RUL-01.h | proposed | Date conditions: a range (reversed order is accepted) and "after date". | — | S36-11 |
| RUL-01.i | proposed | Length conditions distinguish no end time, a normal event, a near whole-day event and an exact duration. | — | S36-12 |
| RUL-02 | proposed | A regular expression in a condition is checked as the user types and cannot slow the app down. | — | — |
| RUL-02.a | proposed | A typed regex is checked for legality as it is typed or saved; when it is not legal, the site says why and highlights the broken part of the pattern. Regexes use Dart (ECMAScript) syntax; Python-only syntax is not supported. | — | Developer, Nov 17 |
| RUL-02.b | proposed | A regex that takes too long is stopped within the pattern budget in DEF-01 and reported as Too slow; the regex tester reports an invalid pattern, shows the match spans and highlights the match. | — | S52-01, S52-05, S52-06, S49-05, S49-06, S49-56 |
| RUL-02.c | proposed | A pattern that exceeds its evaluation budget (DEF-01) matches no further events during that evaluation run (RUL-02). | — | changelog_gaps_601-900:19 |
| RUL-03 | proposed | A rule has actions that change the events it matches. | — | — |
| RUL-03.a | proposed | Actions: Color, Emoji, Change title, Change notes, Add text, Change length, Change time, Delete, Move, Add event, Record changes, link rules (delete/move). | — | S62-01, S62-09 |
| RUL-03.b | proposed | Each action asks for what it needs: minutes for Change length, a title or an event template for Add event, a color for Color (UIC-10). | — | S37-37, S37-38, S40-09..11 |
| RUL-03.c | proposed | Color: the higher rule wins; a lower rule still adds its emoji; a second pass does not duplicate it; several emoji actions prefix the title in order. | — | S36-14, S49-08 |
| RUL-03.d | proposed | Change title replaces the title; Add appends (a new line for notes, a space for location). | — | S62-05 |
| RUL-03.e | proposed | Delete hides the event with a rule-labelled marker; non-matching events stay. | — | S62-02 |
| RUL-03.f | proposed | Move shifts start and end together, forward or back by a number of minutes. | — | S62-03, S62-04 |
| RUL-03.g | proposed | Change length makes a near whole-day event all-day (keeping an original-time note) or shortens a normal one. | — | S36-13, S27-09, S27-13 |
| RUL-03.h | proposed | An Emoji action lets the user find and choose any emoji by searching (UIC-11). | — | S44-41 |
| RUL-03.i | proposed | A newly added Emoji action starts without a chosen emoji; selection follows UIC-11. | — | changelog_gaps_301-600:38 |
| RUL-03.j | proposed | Then actions are reordered as UIC-30 says; the saved action order determines their priority and emoji sequence (RUL-03). | — | changelog_gaps_301-600:32 |
| RUL-04 | proposed | A rule can create events, follow events and record changes. | — | — |
| RUL-04.a | proposed | Add event creates a rule-origin event relative to the matching event (e.g. a Prep event 08:00-08:45, an hour before), from an existing event template. | — | S36-15, S26-19 |
| RUL-04.b | proposed | An Add-event action can place a template-derived event before or after the matching event’s start or after its end (RUL-04). | — | changelog_gaps_1501-1800:25 |
| RUL-04.c | proposed | Changing an event template updates the events generated from it by rules (RUL-04). | — | changelog_gaps_1501-1800:25 |
| RUL-04.d | proposed | An Add-event rule that names an event template that does not exist, and has no title, is not valid (UIC-19). | — | S26-26 |
| RUL-04.e | proposed | Record changes remembers later edits to a matching event and annotates it ("Changed ... time"). | — | S33-11, S33-12 |
| RUL-04.f | proposed | Record changes tracks source title, time and location changes, moved recurring occurrences and dropped events, annotates the affected event and records the observed changes in activity (RUL-04, HIS-01). | — | changelog_gaps_1201-1500:31, changelog_gaps_1201-1500:31 |
| RUL-04.g | proposed | An event deleted by a rule follows that rule’s current outcome: changing or removing the deleting action brings the event back (RUL-03, CAP-01). | — | changelog_gaps_301-600:30 |
| RUL-04.h | proposed | A new Then action, "Link to Event", links the rule to a specific event chosen with the existing date picker, alongside "Delete this event" and "Move this event". | — | F60.2 |
| RUL-04.i | proposed | "Link to" in the rule dialog is simplified to "Link to a Rule": it keeps its place in the dialog but uses the layout of the Sources > Rules subsection. | — | F60.1 |
| RUL-05 | proposed | A rule applies to all calendars or to chosen ones, and rules have an order. | — | — |
| RUL-05.a | proposed | A rule applies to all calendars or to chosen ones; unapplying removes it from that calendar and keeps it in All Rules. | — | S21-17, S21-18, S26-22..24, S33-06, S33-08 |
| RUL-05.b | proposed | A rule scoped to All calendars applies to calendars added later as well as current calendars (RUL-05). | — | readme_gaps:69, changelog_gaps_901-1200:34 |
| RUL-05.c | proposed | Editing a rule preserves its calendar applicability until the user changes that applicability (RUL-05). | — | changelog_gaps_1201-1500:19 |
| RUL-05.d | proposed | A new calendar-specific rule is first in that calendar's list; an all-calendar rule goes last; renaming a calendar keeps its rules. | — | S19-25, S19-26, S36-16, S36-38 |
| RUL-05.e | proposed | Rules are reordered as UIC-30 says, and the order is stored and shown. | — | S34-17, S34-18, S36-17, S36-39 |
| RUL-05.f | proposed | A rule whose calendar was removed still shows the saved name; a rule with no calendar says so. | — | S67-07..09 |
| RUL-05.g | proposed | When adding a rule, the user can reuse an existing rule from another calendar when such a rule is available (RUL-05, RUL-06). | — | changelog_gaps_601-900:43 |
| RUL-05.h | proposed | A source color change updates the source’s color in rule applicability badges (RUL-05, UIC-13, UIC-15). | — | changelog_gaps_901-1200:35 |
| RUL-05.i | proposed | A rule shows which calendars it applies to: All, one calendar, or several (with the count). | — | S38-05, S38-06, S33-07, S33-09 |
| RUL-06 | proposed | The user creates, shows, clones and deletes rules. | — | — |
| RUL-06.a | proposed | A rule can be cloned; the clone is unapplied and placed right after the original. | — | S33-10, S36-41 |
| RUL-06.b | proposed | Deleting a rule removes it from every list; default rules (RUL-06) cannot be deleted. | — | S19-27, S27-10 |
| RUL-06.c | proposed | A calendar starts with two predefined rules (items without an end time, 24-hour events), kept in All Rules like any rule. Default rules are permanent: they can be unassigned from a calendar and assigned again, but never deleted. Adding CCS+ again re-assigns its starters. The 24-hour rule aligns a whole-day event to the local day: an event spanning about 24 hours becomes all-day, local midnight to the next local midnight in the event's time zone, so daylight-saving days stay correct. | — | S21-13, S27-08, S63-17 |
| RUL-06.d | proposed | The rule dialog opens from "New rule…" in a calendar (that calendar preselected) or from All Rules (All preselected); dialog behavior follows UIC-02. | — | S21-15, S37-33..36, S37-41, S67-15, S67-16 |
| RUL-06.e | proposed | A rule shows its title (if any), what it does, and its color by name. | — | S40-01, S40-02, S66-17, S45-26 |
| RUL-06.f | proposed | Saving a rule without a title generates a title from its conditions and actions (RUL-06). | — | changelog_gaps_301-600:18 |
| RUL-06.g | proposed | How rules work is explained from the rule dialog. | — | S33-24, S38-01, S38-03, S38-04, S38-13, S21-23 |
| RUL-06.h | proposed | A rule with no actions is not valid (UIC-19). | — | S27-12 |
| RUL-06.i | proposed | A malformed regex, an unmatched bracket, an incomplete date range or an empty Add is not valid (UIC-19). | — | S36-03..07, S40, S49-07, S62-06, S62-07 |
| RUL-06.j | proposed | A rule has at most the number of conditions and of actions in DEF-01; one more is not valid (UIC-19) and the message names the limit; a rule at the limit saves. | — | S52-07..11 |
| RUL-06.k | backlog | A rule line says what the rule does, titled or not (for example "Items without an end time → Change length to 1:00"); its color reads "Color ■ (Name)". | — | theme.md Clarifications |
| RUL-07 | proposed | Rules that conflict or repeat each other are reported, and the user chooses what to do. | — | — |
| RUL-07.a | proposed | All Rules reports a higher rule that shadows a lower one's color, and duplicate rules, with the choices Put first, Keep as is, Drop and Merge. | — | S37-01..03, S37-08..12 |
| RUL-07.b | proposed | Merging rules unions their calendars (All if any is All). | — | S37-04, S49-29 |
| RUL-07.c | proposed | Saving a condition identical to an existing rule offers Save as new or Merge; the stored count does not change until chosen. | — | S37-42..47 |
| RUL-07.d | proposed | Dropping a conflicting action removes the selected field-specific action, preserving actions for other fields (RUL-07). | — | changelog_gaps_301-600:35 |
| RUL-07.e | proposed | Conflict reporting identifies a higher rule that shadows a lower rule’s Emoji or Time action (RUL-07). | — | changelog_gaps_901-1200:30 |
| RUL-07.f | proposed | Choosing Keep as is suppresses that same conflict warning on subsequent observations (RUL-07). | — | changelog_gaps_901-1200:30 |

