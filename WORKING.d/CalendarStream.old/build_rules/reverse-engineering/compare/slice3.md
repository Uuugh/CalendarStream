# Slice 3 comparison (A = rules.md, events.md, event_templates.md + common.md; B = reverse/slice3.md)
Note: A rows are high level; most exact values (limits, messages, formats) are absent from A. Where A refers to DEF-01 the value is checked there.

## GAP (B ID | behavior and values | A file)
R3-01 | a rule with no condition matches every event (label "Every event") | rules.md
R3-01.e | unknown condition type dropped on read-back; operator not allowed for the kind replaced by the kind's first operator | rules.md
R3-01.f | incomplete condition dropped on read-back; refused on save with "Fill in every condition (or take the empty ones out)." | rules.md
R3-02 | text operator order: is, contains, whole word, begins with, ends with, matches pattern, contains regex | rules.md
R3-02.a | default operator of a new text condition is "contains" | rules.md
R3-02.f/.g | begins/ends tolerate leading/trailing white space; is, contains, whole word, begins, ends treat value literally | rules.md
R3-02.h | text value trimmed, not empty, cut to 200 chars (100 for pattern and regex) | rules.md
R3-03.b | in a pattern * and ? also match line breaks (Any text pattern spans title/location/notes) | rules.md
R3-03.c, R3-04.d, R3-04.e | placeholders "*E####" / "E\d{4}"; insert buttons (* # ? ; ^ $ \b(A|B) .* \d+ \s ? a\.b) and their cursor/wrapping/escape behaviour | rules.md (dialog UI)
R3-05.a | test-box sample titles: next 10 different event titles from today (then past, newest first), excluding hidden and rule-made; editable | rules.md
R3-05.b | tester limits: 30 samples, sample cut to 300 chars, value cut to 100; empty value/invalid pattern gives no results | rules.md / common.md DEF-01
R3-05.c | per sample check or cross, summary "{n} of {total} match" | rules.md
R3-05.e | Apply disabled while a regex/pattern condition shows an error | rules.md
R3-05.f | tester refuses non-text operator "Unknown way to match." | rules.md (low value)
R3-06, R3-06.a | Date operators is, after, before, between (YYYY-MM-DD); after/before exclusive, between inclusive | rules.md
R3-07, R3-07.a | Time operators is/after/before/between, HH:MM (9:05 stored 09:05); after/before exclusive, between inclusive | rules.md
R3-07.c | an all-day event never matches a Time condition (check against A TIM-04: all-day = 24 h midnight-to-midnight) | rules.md
R3-08.b | Day after/before take exactly one day, strict within Monday-Sunday week, no wrap; between takes exactly two days; is stores sorted unique days | rules.md
R3-08.d/.e | day-picker clicks (click, Ctrl/Cmd-click, Shift-click); operator change keeps first day / first two days | rules.md (dialog UI)
R3-09 | Length operators "is" and "is whole days"; range 0 to 52 weeks (524160 min); whole days stored as 1440 | rules.md
R3-09.a | length entered as weeks, days, hours, minutes boxes, summed | rules.md
R3-09.c | "is" with >= 1 hour matches within 5 minutes inclusive; shorter must match exactly; "is" 0 matches only timed events with end = start | rules.md
R3-09.e | length text forms "Length is 1 w 2 d 3:30", "No end time", "Length is whole days" | rules.md
R3-10.b | up to 3 opening and 3 closing brackets per condition; groups nest | rules.md / common.md DEF-01
R3-10.d | stored rule with unbalanced brackets read back with all brackets zeroed, not dropped | rules.md
R3-10.e | dialog buttons: "&"/"|" adds or changes join, x removes (hidden at one; removing first resets next join to and); first condition's join ignored | rules.md
R3-10.f | typing a closing bracket without opener adds opener on first line of group (flash 1.5 s) | rules.md
R3-10.g | a single blank text condition is ignored (matches every event); with several, a blank one is refused | rules.md
R3-10.h | condition word forms: Title contains "RDO" (+" Aa"), Date between a – b, Day(s) is Sat, Sun, Day(s) between Fri – Mon; rule "(A or B) and … → actions" | rules.md
R3-11.b | new Then defaults to Color Tomato #d50000; "+" after last Then adds an Emoji line; x hidden when one remains | rules.md
R3-11.c | invalid action dropped on read-back; rule survives if one action remains | rules.md
R3-12 / .a | color stored #rrggbb lower-case; stored color not in the 11 shown as nearest palette color (squared RGB distance); 11 names+hex list | rules.md / theme.md THM-09
R3-13 | Emoji text up to 16 chars, white space collapsed, no < > & or "; empty drops action | rules.md
R3-13.a | only the highest-priority matching rule with emoji actions supplies emoji, joined by spaces, prefixed with one space; skipped if title already starts with it | rules.md
R3-13.b | ten quick emoji (✈️ 🏝️ 📚 🏠 🚗 ⭐ ❗ 🛌 🎓 🎉), Enter picks first match | common.md UIC-11
R3-14.a | Change length 5 to 10080 min, default 60, timed events only; no-end event stops being "no end"; all-day unchanged | rules.md
R3-14.c | all-day conversion prepends note "Start: HH:MM" (no end time) or "Original time: Mon Oct 23 07:15 – Mon Oct 23 09:30"; notes cut to 2000 | rules.md
R3-14.d | time changes: first matching rule with one wins, only its first time action counts | rules.md
R3-14.f | Title/Notes/Location change: new Title non-empty; limits 200/1000/200; Title/Location collapse white space; Notes keep line breaks, trimmed | rules.md
R3-14.g | text Change not applied to an event the user edited (Add still is) | rules.md
R3-14.h | final limits after rules: notes 4000, location 200 | rules.md
R3-15 | Add action targets Title, Notes or Location (default Title); empty text drops action; limits as R3-14.f | rules.md
R3-15.b/.c | every Add of the highest matching rule that has one for that field applies in order; applied even to edited events; order: time changes, Add/Change text, emoji last | rules.md
R3-16 | Move range -10080..+10080 min, nonzero, entered +h:mm / -h:mm; placeholder "+1:00" tooltip "Move by hours:minutes (− for earlier)" | rules.md
R3-16.a | Move applies after time changes, first matching rule's Move only | rules.md
R3-17.a/.b | Delete not applied to hidden/deleted event; creates no companions; Restore refused "A rule deletes this event; change or remove the rule to bring it back." | rules.md / events.md
R3-18.a | Create event placement before the start / after the start / after the end, offset 0 to 10080 min (h:mm) | rules.md
R3-18.b/.c | created event times: all-day source = midnight of first day to midnight after last day; timed lasts its length; all-day created covers the day containing the start | rules.md
R3-18.f | created event ID = source ID + "#rule-" + rule ID (+ "-" + action position for 2nd+ Create of one rule); duplicates produce one event | rules.md
R3-18.g | hidden source events, or events made by a rule, produce no companions | rules.md
R3-18.h | text `Create “Title”, 0:30 before the start` | rules.md
R3-18.i | created events cannot be edited, deleted or chosen as link target | events.md
R3-19.a | note format "Changed Oct 22: time Oct 23 7:15am–9:30am → …"; parts joined "; " (title "old" → "new", location old → new, "—" empty); last 20 changes per event; blank-line separated | rules.md
R3-19.b | History line "<calendar> changed <title>: <parts>"; vanished event "<calendar> removed <title> (<day and time>)" and its notes discarded | rules.md
R3-19.c | nothing recorded on the first download | rules.md
R3-20.a | link data: event, calendar, linked event, its calendar, its start when last seen, title (200); same events or missing ID invalid | rules.md / events.md
R3-20.b | link rule applies only while its calendar is ticked in Apply to | rules.md
R3-20.c | linked event missing: Delete present deletes this event, otherwise the link is removed | events.md (EVT-05.d covers only delete)
R3-20.e | linked event's title refreshed in the rule | events.md
R3-20.f | wording `Linked to “name” → Delete this event; Move this event with the linked event`; info line "Follows “{name}”: when it is deleted or moves, this event does the same." | rules.md
R3-20.g | link rule never conflicts and is never duplicate-checked | rules.md
R3-21, R3-21.a | per-effect priority (color, emoji, time change, move, delete, each text Change) = highest matching rule with that effect; Create from every matching rule; apply order: time changes/Move, user edits and hand-added events, Create, text, emoji, color, delete | rules.md
R3-22 | action word forms: `Change to all-day`, `Change length to 1:30`, `Change Title to “x”`, `Add “x” to Notes` (breaks " ⏎ "), `🙂 in front of the title` | rules.md
R3-23 | rule dialog title "New rule"/"Change rule", Title optional up to 80 chars placeholder "Optional, e.g. Days off in red", Remove only when editing | rules.md
R3-23.a | generated name `Title contains “RDO” → Color (Tomato)` / "Every event → …" when saved without title; collapse white space | rules.md
R3-23.d | Apply enabled only when dialog differs from opening; Escape closes Apply-to menu first; from event pop-up Cancel returns there | rules.md / UIC-02
R3-24 | Apply to: tick box per calendar with its color, "All calendars" and individual calendars mutually exclusive, none shows "No calendar yet" | rules.md
R3-24.b/.c | save keeps only existing calendar IDs, no duplicates, may be none (inert); "local" = lists exactly that one calendar | rules.md
R3-25.b | at most 60 rules; "Up to 60 rules can be kept." (also on copy) — not in DEF-01 | common.md DEF-01
R3-25.d | rule ID 1-16 lower-case letters/digits; invalid/duplicate gets "t"+6 hex; duplicates in stored list dropped keeping first | rules.md
R3-25.e | History lines "Rule added/changed/merged into/deleted/copied: <label>", "Rule conflict settled (<how>): <label>", "Rule added to / taken off <calendar>: <label>"; every change rebuilds feeds | rules.md
R3-26 / .a | All Rules header: "+" button, count box "1 Rule"/"{n} Rules" (green, amber "{n} to check"), status lines "{n} for all calendars / for chosen calendars / without a calendar yet", up to three conflict lines, empty "No rules yet. Press + to add one." | rules.md
R3-26.b | rule line: words, calendar badge, edit/copy/delete buttons, drag handle, conflict mark | rules.md
R3-26.d | adding a calendar to an "all" rule keeps all; taking one off an "all" rule makes it list every other calendar | rules.md
R3-27 | clone opens in rule dialog to be changed (same title, new ID) | rules.md
R3-28 | delete asks "Delete this rule? It’s removed from every calendar that uses it."; missing rule "That rule doesn't exist (any more)." | rules.md
R3-29 | ALLDAY_24H server setting (default on) decides whether "24-hour events" starter exists; no-end default is all-day or N hours (default 1) | rules.md / common.md
R3-29.b | conversion of 0.2.6-0.2.8-beta.1 rules to current form (B unsure the port needs it) | rules.md (probably not needed)
R3-30 | duplicate check on new rule with >=1 condition: identical conditions, identical action set (order ignored), shares a calendar; link rules ignored | rules.md
R3-30.a/.b | text `This looks the same as “<label>” for the same calendars.`; Merge into vanished rule refused "That rule isn't there any more." | rules.md
R3-31 | conflict test: rules share a calendar and higher rule has no conditions or identical conditions (text case-insensitive unless Aa/regex); link rules excluded | rules.md
R3-31.a | Duplicate = has conditions and same action set; Shadowed kinds: color, emoji, Change time/Title/Notes/Location, Add Title/Notes/Location, Move | rules.md
R3-31.b | overlap calendars shown "(in A, B)" only when not all calendars | rules.md
R3-31.d | Keep remembers conflict key (last 200); Merge them: a takes both calendars, b removed; Take out: remove kind's actions, b removed if none left | rules.md
R3-31.e | "Unknown choice." / "That conflict isn't there any more." | rules.md (low value)
R3-32 / .a | server re-validates colors, calendar IDs, emoji on the way out; invalid JSON "That rule couldn't be read." | rules.md (low value)
R3-33 | headings "Add event", "Duplicate event", "Edit event", "Edit United event" (CCS+); phone = own page | events.md
R3-33.a | field limits: Title 200, Location 200, Online Meeting 500, Notes 4000 (10 lines tall); asterisks on required fields | events.md
R3-34 | new event defaults to 9:00-10:00 on the clicked day (today if missing); | events.md
R3-34.b/.c | missing event "That event isn't in the current schedule any more."; rule-made event cannot be opened/saved/deleted "This event is made by a rule; change the rule or its event template instead." | events.md
R3-36 | Title required "The event needs a title."; cut to 200; location 200; notes 4000; invalid color "Choose one of the colors offered." | events.md
R3-37 | Online Meeting must be empty or http(s):// with no spaces "Online Meeting is a link starting with https://"; open button only when valid | events.md
R3-37.a | extraction order CONFERENCE, X-GOOGLE-CONFERENCE, X-MICROSOFT-SKYPETEAMSMEETINGURL, X-MICROSOFT-ONLINEMEETINGEXTERNALLINK, then notes, location, URL; cut to 500 | events.md
R3-39 | all-day: end date inclusive last day; ending before start "The last day is before the first day."; empty end = start; time fields hidden but place kept | events.md
R3-39.a | changing start date of all-day event keeps its number of days | events.md
R3-40 | end must be after start "The end has to be after the start."; "Check the dates and times."; empty time = 0:00 | events.md
R3-40.c | invalid time entry outlined with "Type a time like 9:30, 9:30pm or 21:30." | events.md
R3-40.d | time list: 96 entries in 15-minute steps, nearest within 8 min highlighted (9:00 when empty), end list shows length "(1 h 30 min)"; Escape/Tab close, Enter accepts | events.md
R3-41 | "Time zone" label becomes "Start time zone" when different end zone shown; unticking resets end zone to start zone | events.md
R3-41.a | zone list: 14 common zones first (America/New_York, Chicago, Denver, Phoenix, Los_Angeles, Anchorage; Pacific/Honolulu, Guam; UTC; Europe/London, Frankfurt; Asia/Tokyo, Hong_Kong; Australia/Sydney), then others containing "/" except Etc/, SystemV/, posix/, right/ | events.md / common.md TIM-09
R3-42 | save with no change and no prior edit records no edit; History `Edited "<original title>" (<start date>)` | events.md
R3-42.a | stale warning texts ("United changed this event since your edit…" / feed variant); stale = fingerprint of title, start, end, all-day, location, notes differs | events.md
R3-42.b/.c | editor shows source's version above form ("United’s version (from CCS+)" / "The feed’s version (from <name>)", "— not edited yet"); Revert shown only when edited, labels "Revert to United’s version"/"…the feed’s version"; History `Reverted "<title>" to its calendar’s version` | events.md
R3-43 | Delete confirm "Delete this event?" "(It may be restored here or in History, Undo & Logs)"; "That event is already deleted; History › Undo brings it back." | events.md
R3-43.a/.b | Hide confirm "Hide this event from the feeds?"; refusal "Only an event from a calendar source can be hidden or shown."; Show removes the edit if hiding was its only change; History `Hid "<title>" (<date>) from the feeds` / `Showed … in the feeds again` | events.md
R3-43.c | source event that vanishes is kept struck through only if it has not ended before today | events.md
R3-43.d | Restore refused "That event can't be restored any more." when not deleted or already "gone"; History `Restored "<title>" (<date>)` | events.md
R3-44 | reminder choices exactly: at the start, 5, 10, 15, 30 min, 1 h, 2 h, 1 d, 2 d, 1 week; at five ticked the others disabled | events.md
R3-44.a/.b | labels "at the start", "{n} min before", "1 hour before", "{n} days before", "1 week before"; kept by event ID across downloads/edits; sent to Google (<=5) and written to feeds; History `Reminders for "<title>" (<date>): …` or "none" | events.md
R3-45 | Link to: "Event" opens small month calendar (prev/next/Today); "Rule" lists rules touching the event and "Create new: its title and date" (If Title is <title> and Date is <date>, event's calendar); x removes link at Save | events.md
R3-45.a/.b | picked event shows "Title · date" + note "Saving makes a rule: if it is deleted → Delete this event; if it moves → Move this event. Change it under Rule."; picker blocks itself and rule-made events ("This event"/"Made by a rule: it can’t be linked to"), hides deleted | events.md
R3-45.c | saving with link makes one link rule on own calendar with Delete + Move; same target leaves rule as is; other target updates; clearing or hidden/deleted/missing target removes it | events.md
R3-45.d | "Rule" list highest first, link rule then matching rules; empty "No rule touches it yet." | events.md
R3-46 | event Print opens Print Preview in Day view (Itinerary, Day, 5-day, Week, Month; weekends; range; orientation; light/dark; remembers prefs except one-day print) | events.md (or printing file)
R3-47.a | History `Updated "<title>" (<date>)` / `Added "<title>" (<date>)`; new event ID "cs-"+16 hex+"@calendar_stream" | events.md
R3-49.a | Event Templates section: "+", counts "{n} all-day"/"{n} timed", "1 Template"/"{n} Templates", empty "No event templates yet. Press + to add one." | event_templates.md
R3-49.b/.c | template row fields (Title placeholder "Title, e.g. Drive to the airport", Timed/All day, Length, Location 200, color or "Its calendar’s color", delete, +); "+" pop-up "Add an event template" defaults Timed 1:00 no color; "Give it a title." | event_templates.md
R3-50 | at most 30 templates "Up to 30 templates can be kept."; empty-title rows dropped on save | event_templates.md / DEF-01
R3-50.a | extra length forms: h:m, 1h, "1,5", "90min", up to 3 hour digits, empty = 1:00 (A lists 1:30, 2, 1.5, 90m, 1h15) | event_templates.md
R3-50.b | error texts `Check the length of "<title>" (e.g. 1:30).`; timed outside 0:05-24:00 refused; all-day stores 60 min | event_templates.md
R3-50.e | read-back: title cut 200, length 5-1440 (default 60), location 200, notes 2000, color kept only if one of the 11 | event_templates.md
R3-51 | removing a template makes using rules stop adding events (rule stays); History "Event templates saved: <n>" | event_templates.md
R3-49 (notes) | notes exist on a template but are not editable on the page | event_templates.md

## DIFFERENT (B ID | A ID | A says | B says)
R3-01.c | RUL-01.f, TIM-05 | conditions judged in the event's own recorded time zone | judged in the server's configured time zone
R3-01.d | TIM-04 | all-day event = 24-hour event local midnight to midnight in its own zone | all-day: date of start, length = whole days, no time of day
R3-02.b | RUL-01.a | case is always ignored | ignored unless the condition's "Aa" toggle is on
R3-04.b | RUL-02.a | regexes use Dart (ECMAScript) syntax; Python-only syntax unsupported | Python `regex` package dialect
R3-13.b | UIC-11.a, UIC-11.b | emoji up to Emoji 13.0, no flags; newer ones show compatibility note | note shown for flags or newer than Emoji 12.0
R3-14 | RUL-03.a | actions Change title, Change notes, Add text, Change length, Change time (no Change location) | Change has five targets: all-day, length, Title, Notes, Location
R3-14.b | RUL-03.g | Change length turns a near whole-day event into all-day | separate "to all-day" action converts any timed event (rounded days)
R3-18.e | RUL-04.a | Add event is made from an existing event template | Create event from a template OR typed "New event…" fields (title 200, all-day, length 5 min-24 h, location)
R3-52 | RUL-04.a | template only | choice list adds "New event…" as last choice
R3-20 | RUL-04.h, RUL-04.i | "Link to Event" is a new Then in the rule dialog; link UI simplified to "Link to a Rule" | link rule has no conditions and only Thens Delete / Move with linked event, made from the event editor
R3-25.a | RUL-05.d | new calendar-specific rule first in that calendar's list; all-calendar rule last | one-calendar rule inserted above first shared/multi-calendar rule the calendar uses; any other new rule at end
R3-28 | RUL-06.b | default rules cannot be deleted | any rule can be deleted
R3-29 | RUL-06.c | each calendar starts with two predefined rules, permanent (unassign/assign, never delete); 24-hour rule uses local midnight | starter rules created once on a new install, for all calendars (24-hour rule optional by setting), deletable
R3-31.c | RUL-07.a | choices Put first, Keep as is, Drop and Merge | Duplicate: Merge them / Keep both; Shadowed: Put first / Take the {what} out / Keep as is
R3-31.a | RUL-07.a, RUL-07.e | shadowing of color, emoji, time named | ten shadow kinds (color, emoji, time, 3 Change text, 3 Add text, Move)
R3-34 | EVT-01.b | new event zone = system zone or calendar's zone; no calendar chosen goes to initial Local calendar | display time zone, default calendar; no calendar = refused "Add a calendar source first (Calendar Sources → +)."
R3-41.c | TIM-01 | start/end stored in UTC with the zone recorded | stored as ISO date-times with offset
R3-48 | TPL-02.b | picking a template fills title, location and end time | fills Title, Location, All-day, length and color (not Notes)
R3-49 | TPL-01.a | template stores title, duration, color, location, notes | adds a Timed/All-day flag
R3-50.b | TPL-01.c | duration under 5 min raised to 5 | timed length outside 5 min-24 h refused with an error
R3-07.c | TIM-04, RUL-01 | all-day is a 24 h event with times (no special case) | all-day never matches a Time condition

## A-ONLY (A ID | one phrase)
RUL-03.h/.i | emoji search; new Emoji action starts empty
RUL-04.c | template change updates generated events
RUL-04.g | deleted-by-rule event returns when rule changes
RUL-05.c/.g/.h | keep applicability on edit; reuse rule from another calendar; badge color follows source color
RUL-06.k | backlog: rule line wording with Color ■ (Name)
RUL-07.f | Keep as is suppresses repeat warning (partly in B R3-31.d)
EVT-01.d | save confirmation names the event
EVT-01.e/.f | custom-event delete leaves deletion marker; restore gives custom origin
EVT-01.i/.j | backlog: dialog layout, all-day/zone placement, icons on one line
EVT-03.c | imported event color edit marks edited, not stale
EVT-03.d | default color follows calendar until picked
EVT-03.g/.h | open meeting address; exported in ICS URL
EVT-04.f | backlog: deleted event wording of where deleted, Restore, not drawn when added+deleted here
EVT-05.b | removing a link then Cancel keeps stored link
EVT-05.g | starting a rule closes event dialog, Cancel reopens it exactly
EVT-06.b | event dialog offers Move (CAP-03)
EVT-06.a | Duplicate icon placement; different calendar choice (B has Duplicate only)
TPL-02.c | saved events offer no template picker (B: new events only, same)

## Counts
B rows: covered ~58, different 19, gap ~140 (of 217; approximate: grouped lines and partial coverage counted as gap). A rows only-in-A: 21 lines above (about 27 rows).
