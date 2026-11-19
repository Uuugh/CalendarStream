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
| RUL-04.g | proposed | An event deleted by a rule follows that rule’s current outcome: changing or removing the deleting action brings the event back (RUL-03, CAP-02). | — | changelog_gaps_301-600:30 |
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
| RUL-07.f | proposed | Choosing Keep as is suppresses that same conflict warning on subsequent observations (RUL-07). The conflicts remembered are limited as DEF-01 says, the oldest forgotten first. | — | changelog_gaps_901-1200:30 |
| RUL-01.j | proposed | A rule with no condition matches every event; its label is msg:everyEvent. | — | R3 gap |
| RUL-01.k | proposed | A condition that is incomplete (a date or time range with an end missing, a day condition with no day, a text condition with no value in a rule that has other conditions) is not valid (UIC-19): saving shows msg:fillInEveryConditionOr and stores nothing. | — | R3 gap |
| RUL-01.l | proposed | A rule whose only condition is a text condition with no value drops it when saved, so the rule matches every event (RUL-01.j). | — | R3 gap |
| RUL-01.m | proposed | A stored condition of a kind the app does not know is dropped when rules are read back. | — | R3 gap |
| RUL-01.n | proposed | A stored condition whose operator is not allowed for its kind gets the first operator of that kind when rules are read back. | — | R3 gap |
| RUL-01.o | proposed | A stored condition that is incomplete (RUL-01.k) is dropped when rules are read back. | — | R3 gap |
| RUL-01.p | proposed | The text operators are, in this order: msg:opIs, msg:opContains, msg:opWholeWord, msg:opBeginsWith, msg:opEndsWith, msg:opMatchesPattern, msg:opContainsRegex. | — | R3 gap |
| RUL-01.q | proposed | A new text condition starts with the operator msg:opContains. | — | R3 gap |
| RUL-01.r | proposed | msg:opBeginsWith and msg:opEndsWith ignore white space at the start or end of the text they are compared with. | — | R3 gap |
| RUL-01.s | proposed | msg:opIs, msg:opContains, msg:opWholeWord, msg:opBeginsWith and msg:opEndsWith take the typed value literally, so wildcard and regex characters in it are ordinary characters; wildcards belong to msg:opMatchesPattern (RUL-01.b, RUL-01.c) and regular expressions to msg:opContainsRegex (RUL-02). | — | R3 gap |
| RUL-01.t | proposed | A text value is trimmed, must not be empty, and is cut to the text value length in DEF-01 (the shorter pattern and regex length for msg:opMatchesPattern and msg:opContainsRegex). | — | R3 gap |
| RUL-01.u | proposed | In a pattern, `*` and `?` also match line breaks, so a pattern on msg:fieldAnyText can match across the title, the location and the notes. | — | R3 gap |
| RUL-01.v | proposed | A Date condition offers msg:opIs, msg:opAfter, msg:opBefore and msg:opBetween on a calendar date; after and before leave out the date typed, between includes both its dates. | — | R3 gap |
| RUL-01.w | proposed | A Time condition offers msg:opIs, msg:opAfter, msg:opBefore and msg:opBetween on a time of day; after and before leave out the time typed, between includes both its times. | — | R3 gap |
| RUL-01.x | proposed | A time of day in a condition is kept with two digits for the hour (9:05 is kept as 09:05). | — | R3 gap |
| RUL-01.y | proposed | A Day condition with msg:opIs holds any number of days, kept once each in week order from Monday to Sunday. | — | R3 gap |
| RUL-01.z | proposed | A Day condition with msg:opAfter or msg:opBefore holds exactly one day and compares inside the Monday-to-Sunday week without wrapping; with msg:opBetween it holds exactly two days. | — | R3 gap |
| RUL-08 | proposed | A Length condition matches events by how long they last. | — | — |
| RUL-08.a | proposed | The Length operators are msg:opIs and msg:opIsWholeDays; whole days needs no length typed. | — | R3 gap |
| RUL-08.b | proposed | A length is typed in four boxes, weeks, days, hours and minutes, and is their sum; it is none or more, up to the longest length in DEF-01. | — | R3 gap |
| RUL-08.c | proposed | msg:opIs with a length at or above the threshold in DEF-01 matches events whose length is within the tolerance in DEF-01 of it, both ends included. | — | R3 gap |
| RUL-08.d | proposed | msg:opIs with a shorter length matches only events of exactly that length. | — | R3 gap |
| RUL-08.e | proposed | msg:opIs with length none matches only timed events whose end is their start. | — | R3 gap |
| RUL-08.f | proposed | A length condition reads msg:lengthIsValue, where {value} is the weeks and days (with msg:unitWeekShort and msg:unitDayShort) followed by hours:minutes, such as 1 w 2 d 3:30; length none reads msg:noEndTime and whole days reads msg:lengthIsWholeDays. | — | R3 gap |
| RUL-09 | proposed | A Day condition is entered by clicking days in a row of the seven weekdays. | — | — |
| RUL-09.a | proposed | With msg:opIs a click selects one day, Ctrl or Cmd with a click adds or removes a day, and Shift with a click selects the run of days between the last click and this one. | — | R3 gap |
| RUL-09.b | proposed | With msg:opAfter, msg:opBefore and msg:opBetween a click selects one day; with msg:opBetween a Shift click selects the second end. | — | R3 gap |
| RUL-09.c | proposed | Changing a Day condition's operator keeps the first chosen day for after and before and the first two chosen days for between. | — | R3 gap |
| RUL-10 | proposed | The dialog joins conditions with and or or and groups them with brackets (RUL-01.e). | — | — |
| RUL-10.a | proposed | A condition has at most the number of opening and of closing brackets in DEF-01, and groups nest. | — | R3 gap |
| RUL-10.b | proposed | A stored rule whose brackets do not balance is read back with every bracket of its conditions removed; its conditions stay. | — | R3 gap |
| RUL-10.c | proposed | Every condition after the first shows a join button that switches between msg:joinAnd and msg:joinOr, drawn as & and \|. | — | R3 gap |
| RUL-10.d | proposed | Every condition has an x that removes it; the x is hidden while only one condition is left. | — | R3 gap |
| RUL-10.e | proposed | Removing the first condition sets the next condition's join to msg:joinAnd; the join of the first condition is not used. | — | R3 gap |
| RUL-10.f | proposed | Typing a closing bracket that has no opening bracket before it adds an opening bracket on the first line of its group, which flashes for the time in DEF-01. | — | R3 gap |
| RUL-11 | proposed | A text condition has a test box that shows which sample titles it matches (RUL-02.b). | — | — |
| RUL-11.a | proposed | The samples start as the next different event titles from today on across all calendars, then earlier ones newest first (the count in DEF-01); hidden events and events made by a rule are left out; the user can edit the samples. | — | R3 gap |
| RUL-11.b | proposed | The test box holds at most the number of samples in DEF-01, cuts a sample and the typed value to their lengths in DEF-01, and shows no results while the value is empty or the pattern is not valid. | — | R3 gap |
| RUL-11.c | proposed | Each sample shows a check when it matches and a cross when it does not, with the summary msg:matchCount ({n} matching samples, {total} samples). | — | R3 gap |
| RUL-11.d | proposed | Apply is disabled while a pattern or regex condition shows an error (UIC-19). | — | R3 gap |
| RUL-11.e | proposed | An empty pattern value shows the placeholder msg:patternPlaceholder and offers insert buttons msg:insAnyText for `*`, msg:insDigit for `#` and msg:insOneChar for `?`. | — | R3 gap |
| RUL-11.f | proposed | An empty regex value offers insert buttons msg:insStarts (`^`), msg:insEnds (`$`), msg:insWord (`\b…\b`), msg:insEither (`(A\|B)`), msg:insAny (`.*`), msg:insDigits (`\d+`), msg:insSpace (`\s`), msg:insOptional (`?`) and msg:insLiteral (`a\.b`). | — | R3 gap |
| RUL-11.g | proposed | The start and end insert buttons put their character at the start or at the end of the value, once; the other insert buttons put theirs at the cursor and wrap the selected text for word, either and literal; literal escapes the characters that have a meaning in a regex. | — | R3 gap |
| RUL-12 | proposed | A rule is shown in words: its conditions, then what it does. | — | — |
| RUL-12.a | proposed | A condition reads field, operator and value, such as msg:title msg:opContains “RDO” with the mark Aa added when case matters; a range reads a – b; msg:fieldDays lists days separated by commas, and a day range reads first day – last day. | — | R3 gap |
| RUL-12.b | proposed | A rule reads its conditions joined by msg:joinAnd or msg:joinOr, with its brackets, then → and its actions; with no condition it starts with msg:everyEvent. | — | R3 gap |
| RUL-12.c | proposed | An action reads msg:actChangeToAllDay, msg:actChangeLength ({value} as h:mm), msg:actChangeField ({field} is the field's name, {value} the new text), msg:actAddToField ({text} with line breaks shown as ⏎, {field}), msg:actEmojiInFront ({emoji}), msg:actColorNamed ({name} the palette name), msg:actDeleteEvent or msg:actCreateEvent ({title}, {offset} as h:mm, {placement} one of msg:placeBeforeStart, msg:placeAfterStart, msg:placeAfterEnd). | — | R3 gap |
| RUL-12.d | proposed | A link rule reads msg:linkedTo, →, then msg:actDeleteEvent and msg:actMoveWithLinked separated by semicolons. | — | R3 gap |
| RUL-13 | proposed | Each kind of action has its own entry rules and effect. | — | — |
| RUL-13.a | proposed | A color is kept as lower-case #rrggbb; a stored color that is not one of the palette colors (THM-09) is shown as the palette color with the smallest squared difference in red, green and blue (UIC-20). | — | R3 gap |
| RUL-13.b | proposed | A new Color action starts as Tomato (THM-09.a). | — | R3 gap |
| RUL-13.c | proposed | A + after the last action adds an Emoji action; every action has an x that removes it, hidden while only one action is left. | — | R3 gap |
| RUL-13.d | proposed | An action that is not valid when rules are read back is dropped; the rule stays while one action remains. | — | R3 gap |
| RUL-13.e | proposed | An Emoji action's text is at most the emoji length in DEF-01, with white space collapsed and without the characters < > & and double quotes; empty text drops the action. | — | R3 gap |
| RUL-13.f | proposed | Only the highest rule that matches and has Emoji actions supplies the emoji: they are joined by spaces and put before the title followed by one space, and nothing is added when the title already starts with that text. | — | R3 gap |
| RUL-13.g | proposed | A Change length action sets the length to the number of minutes entered, between the least and the most in DEF-01 (default in DEF-01); it applies to timed events, an event with no end time stops having none, and an all-day event is left as it is. | — | R3 gap |
| RUL-13.h | proposed | An event that becomes all-day gets a first line in its notes, msg:allDayNoteStart ({time}) when it had no end time and otherwise msg:allDayNoteOriginal ({range} is its start and end with weekday, month, day and 24-hour time); the notes are cut to the length in DEF-01. | — | R3 gap |
| RUL-13.i | proposed | Of the rules that match, the first one with a time change supplies it, and only that rule's first time action counts. | — | R3 gap |
| RUL-13.j | proposed | A Change Title or Change Notes action needs a new text that is not empty and is cut to its length in DEF-01; a title collapses white space, notes keep their line breaks and are trimmed. | — | R3 gap |
| RUL-13.k | proposed | A Change of text is not applied to an event the user edited; an Add still is. | — | R3 gap |
| RUL-13.l | proposed | After all rules, notes and location are cut to their lengths in DEF-01. | — | R3 gap |
| RUL-13.m | proposed | An Add action targets Title, Notes or Location (Title is the default); empty text drops the action; its text is cut to the length in DEF-01 for that field. | — | R3 gap |
| RUL-13.n | proposed | Every Add for a field of the highest matching rule that has one applies, in order, also to an event the user edited. | — | R3 gap |
| RUL-13.o | proposed | A Move action is a number of minutes within the range in DEF-01, not zero, typed as +h:mm or -h:mm with the placeholder msg:movePlaceholder and the tooltip msg:moveByTooltip. | — | R3 gap |
| RUL-13.p | proposed | Move is applied after the time changes, from the first matching rule that has one. | — | R3 gap |
| RUL-13.q | proposed | A Delete action is not applied to an event that is already hidden or deleted. | — | R3 gap |
| RUL-14 | proposed | When several rules match an event, each effect has one winner and the effects are applied in a fixed order. | — | — |
| RUL-14.a | proposed | For each kind of effect (color, emoji, time change, move, delete, each text Change) the highest rule in the list that matches and has that effect supplies it; Create event actions come from every matching rule. | — | R3 gap |
| RUL-14.b | proposed | Rules apply to a calendar's events in this order: time changes and Move, then the user's edits and events added by hand, then Create event, then text Change and Add, then emoji, then color, then delete. | — | R3 gap |
| RUL-15 | proposed | A Create event action makes an event beside each event the rule matches (RUL-04.a). | — | — |
| RUL-15.a | proposed | A Create event action places its event before the start, after the start or after the end of the matching event (msg:placeBeforeStart, msg:placeAfterStart, msg:placeAfterEnd), plus an offset entered as h:mm within the range in DEF-01. | — | R3 gap |
| RUL-15.b | proposed | When the matching event is all-day, the created event runs from midnight of its first day to midnight after its last day. | — | R3 gap |
| RUL-15.c | proposed | A created timed event lasts the length of its template from the placed moment; a created all-day event covers the day that contains that moment. | — | R3 gap |
| RUL-15.d | proposed | A created event has a stable identity made from the matching event, the rule and the action's position, so a repeat run updates the same event and two actions that make the same identity produce one event. | — | R3 gap |
| RUL-15.e | proposed | An event that is hidden, or was made by a rule, or is deleted by a rule, produces no created events. | — | R3 gap |
| RUL-15.f | proposed | A Create event action whose event template no longer exists creates nothing. | — | R3 gap |
| RUL-16 | proposed | The rule dialog adds a rule or changes one (RUL-06.d). | — | — |
| RUL-16.a | proposed | The dialog's heading is msg:newRule when adding and msg:changeRule when changing. | — | R3 gap |
| RUL-16.b | proposed | The rule's Title is optional, at most the title length in DEF-01, with white space collapsed and the placeholder msg:ruleTitlePlaceholder. | — | R3 gap |
| RUL-16.c | proposed | Remove is offered while a rule is being changed. | — | R3 gap |
| RUL-16.d | proposed | Apply is enabled while the dialog differs from how it opened and disabled while it matches it. | — | R3 gap |
| RUL-16.e | proposed | Apply to shows one tick box for each calendar with its color; msg:allCalendars and the single calendars exclude each other, and with no calendar yet it shows msg:noCalendarYet. | — | R3 gap |
| RUL-16.f | proposed | Saving keeps only calendars that exist, each once; a rule may apply to no calendar and then does nothing. | — | R3 gap |
| RUL-17 | proposed | All Rules shows what the rules are and which need attention (RUL-07). | — | — |
| RUL-17.a | proposed | The header has the + of UIC-24 and a count box, msg:ruleCountOne or msg:ruleCount ({n}), green while no conflict is open and amber with msg:rulesToCheck ({n} conflicts) otherwise. | — | R3 gap |
| RUL-17.b | proposed | With no conflict open, the status lines are msg:rulesForAll, msg:rulesForChosen and msg:rulesWithoutCalendar ({n} rules each); otherwise up to the number of lines in DEF-01 show the conflicts. | — | R3 gap |
| RUL-17.c | proposed | An empty list shows msg:noRulesYet. | — | R3 gap |
| RUL-17.d | proposed | A rule line shows the rule in words (RUL-12), a badge naming its calendars (RUL-05.i), edit, copy and delete buttons, the handle of UIC-30 and a mark while a conflict of it is open. | — | R3 gap |
| RUL-17.e | proposed | Adding a calendar to a rule that applies to all calendars leaves it applying to all; taking a calendar off such a rule makes it list every other calendar. | — | R3 gap |
| RUL-17.f | proposed | Copying a rule opens a copy in the rule dialog with the same title; it is stored when it is saved. | — | R3 gap |
| RUL-17.g | proposed | Delete asks msg:deleteRuleAsk (UIC-06); a rule that no longer exists shows msg:ruleMissing. | — | R3 gap |
| RUL-18 | proposed | Stored rules have a limit, identities and History entries. | — | — |
| RUL-18.a | proposed | At most the number of rules in DEF-01 are kept; one more, added or copied, is not valid (UIC-19) and shows msg:rulesLimit ({n} the limit). | — | R3 gap |
| RUL-18.b | proposed | A rule's ID is 1 to the length in DEF-01 of lower-case letters and digits; an ID that is invalid or already used is replaced by a new one, and a stored list with the same ID twice keeps the first. | — | R3 gap |
| RUL-18.c | proposed | History (HIS-01) records msg:ruleAdded, msg:ruleChanged, msg:ruleMergedInto, msg:ruleDeleted and msg:ruleCopied ({label} the rule's label); a conflict settled records msg:ruleConflictSettled ({how} the choice, {label}); adding or taking off a calendar records msg:ruleAddedToCalendar or msg:ruleTakenOffCalendar ({calendar}, {label}). | — | R3 gap |
| RUL-18.d | proposed | Every change to the rules rebuilds the calendars and feeds that use them. | — | R3 gap |
| RUL-19 | proposed | A link rule makes one event follow another (EVT-05). | — | — |
| RUL-19.a | proposed | A link records its event and calendar, the linked event and its calendar, the linked event's start when it was last seen and its title (length in DEF-01); a link whose two events are the same, or that lacks one, is not valid (UIC-19). | — | R3 gap |
| RUL-19.b | proposed | A link rule applies only while its calendar is ticked in Apply to. | — | R3 gap |
| RUL-19.c | proposed | When the linked event is missing, an event whose link rule has a Delete action is deleted; otherwise the link is removed. | — | R3 gap |
| RUL-19.d | proposed | The linked event's title in the rule is refreshed when it changes. | — | R3 gap |
| RUL-19.e | proposed | The dialog's info line for a link rule is msg:followsInfo ({name} the linked event's title). | — | R3 gap |
| RUL-04.j | proposed | The note that Record changes adds to an event's notes reads msg:changedNote ({date}, {parts} the changed parts separated by semicolons: msg:changePartTime, msg:changePartTitle, msg:changePartLocation, an empty value shown as —); only the last changes in DEF-01 are kept per event, each separated from other notes by a blank line. | — | R3 gap |
| RUL-04.k | proposed | A noted change is also recorded in History as msg:historyChanged ({calendar}, {title}, {parts}); an event that vanished from its source is recorded as msg:historyRemoved ({calendar}, {title}, {when} its day and time) and its notes are discarded. | — | R3 gap |
| RUL-04.l | proposed | Nothing is recorded for a calendar's first download. | — | R3 gap |
| RUL-06.l | proposed | The title made for an untitled rule is the rule in words (RUL-12), for example Title contains “RDO” → Color (Tomato), with white space collapsed. | — | R3 gap |
| RUL-07.g | proposed | A new rule that has at least one condition is a duplicate of a stored rule when their conditions are identical, their sets of actions are identical (order ignored) and they share a calendar; link rules are not compared. The user sees msg:thisLooksTheSameAs ({label}) and chooses as RUL-07.c says. | — | R3 gap |
| RUL-07.h | proposed | Merging into a rule that no longer exists shows msg:ruleIsntThereAnyMore and changes nothing. | — | R3 gap |
| RUL-07.i | proposed | Two rules conflict when they share a calendar and the higher one matches at least everything the lower one matches: it has no conditions, or the same conditions (text is compared ignoring case; a case-sensitive condition or a regex is compared exactly); a link rule is never part of a conflict. | — | R3 gap |
| RUL-07.j | proposed | A conflict is a duplicate when the higher rule has conditions and both rules have the same set of actions. | — | R3 gap |
| RUL-07.k | proposed | A conflict names the calendars where the rules overlap as msg:conflictIn ({calendars}) when they do not apply to all calendars. | — | R3 gap |
