# Open questions for the Developer

Only unanswered questions are listed. Answer on the `Answer:` line under a question (or tell the orchestrator); the orchestrator applies the answer to the requirement rows and removes the question. Before asking, the orchestrator looks in the other requirements, the Python app (`build_rules/reverse-engineering/`) and https://docs.flutter.dev/ and https://dart.dev/.

## Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **CGOW-04.d** Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? 
  Answer:
- **CGOW-04.e** If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? 
  Answer:
  Code check: the old app makes a new calendar when a sync finds it missing (deleted in Google), drops the stored per-event state, writes everything again and notes it (reverse-engineering R5-20.f). Our CGOW-06.h and PGAP-02.c say a missing calendar pauses recovery: which wins?
- **CGOW-04.j** Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? 
  Answer:

- **CCCS-02.l** Existing CCS+ credentials can be imported from the old configuration, stored encrypted, and recorded as imported activity. Is this still needed after the port, given that the migration tool (DEP-05) copies the saved credentials? 
  Answer:
- **CON-06.l** Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Code check (Nov 19): only CCS+ retries (CCCS-03.b and CCCS-03.c give its plans); every other download makes one attempt per check. Suggestion: reword CON-06.l to say a failed download is tried again at the next check, and leave retry plans to CCCS-03.
  Answer:

## Open, from the connections work (Nov 19)


## Found by a cold read of the requirements (test of the process)

- **Kind text per connection:** CON-02.d used to list five kind texts (CalendarStream, United Airlines CCS+, Google Calendar, Apple Calendar, Calendar Feed) in the common file, which every new connection would have to edit. Each connection now states its own kind text, but none does yet. Recommended: Local calendar = CalendarStream; CCS+ = United Airlines CCS+; calendar link = Google Calendar, Apple Calendar or Calendar Feed by its preset (CLNK-01.c); Google one-way and two-way = Google Calendar. Is that right?
  Answer: CON-02.d is invalid
- **Removing the Google API client:** CGOW-01.r keeps the Google connections in their sections needing their account restored. Does publishing stop, which status do they show, and is the user asked to confirm before removing the client?
  Answer:

- **One-way and two-way Google rows:** CGOW-04.k says one-way sync publishes and does not read back, yet CGOW-04.b, CGOW-04.c, CGOW-04.g and the instant updates (CGOW-05) describe reading Google's changes, which are two-way behaviors. Code check: the old app agrees (one-way only writes and puts back what changed in Google; two-way reads Google first during a full check: reverse-engineering R5-28). Recommended: move those rows to `google_two_way.md`. Is that right?
  Answer:


## From the Coder's second run (Nov 19)


## Differences from the old app (ours wins unless you say otherwise)

Each line says what our requirement says and what the running Python app does. Leave Answer empty to keep ours; write the old behavior to switch. Left out: differences already answered or obsolete, and about 30 trivial or repeated ones (the six comparison files list about 100). The first eleven lines are the big ones.

- **ACC-07.a** ours: global block at 25 failures in 15 minutes; old app: 50. Keep ours?
  Answer:
- **ACC-08.d** ours: unlock link valid 24 hours, single use; old app: 1 hour, and the link goes to the container log. Keep ours?
  Answer:
- **ACC-04.a** ours: password rules configurable, minimum 11 characters; old app: fixed: 12 or more, a capital, a digit, a symbol, no character 3 times in a row. Keep ours?
  Answer:
- **CFED-02.a** ours: stream token 22 characters, any character allowed; old app: 32 characters, only letters, digits, hyphen and underscore. Keep ours?
  Answer:
- **CON-01.d** ours: 50 connections in total; old app: 10 calendars and 20 destinations separately. Keep ours?
  Answer:
- **CON-09.a** ours: each event keeps its own time zone in feeds and Google (also TIM-01, TIM-06, TIM-07); old app: one server zone for everything; timed events go out in UTC. Keep ours?
  Answer:
- **CLCL-01.d** ours: a new Local calendar joins feeds only when none existed; old app: every new Local calendar joins every feed. Keep ours?
  Answer:
- **CON-05.a** ours: one download interval for all sources; old app: an interval per source. Keep ours?
  Answer:
- **CCCS-03.f** ours: CCS+ pause ends on Sync Now after the credentials are fixed; old app: any successful sign-in or new credentials ends it. Keep ours?
  Answer:
- **SET-06.b** ours: Backup and Restore exists (backlog); old app: none; backup is a database dump. Keep ours?
  Answer:
- **CAL-01.b** ours: Month, Week, 5-day, Day, List views; old app: no 5-day view except in Print Preview. Keep ours?
  Answer:
- **CAL-03** ours: drag an event to move it; old app: no dragging; edit in the form. Keep ours?
  Answer:
- **CAL-01.g** ours: a count of events that do not fit a day cell; old app: cells grow; no overflow count. Keep ours?
  Answer:
- **CAL-04.b** ours: stretch and hour height in whole event lines (1-6); old app: pixels (stretch -300 to 1200, hour height 20-120). Keep ours?
  Answer:
- **ACC-07.b** ours: trusted networks for the global block: 192.168/16, 10.10/16, loopback; old app: all local ranges; proxy headers ignored; own public domain judged by what it resolves to. Keep ours?
  Answer:
- **ACC-02.f** ours: stricter check of the page to return to after login (no //, backslash or control character); old app: also refuses any character code 32 or lower. Keep ours?
  Answer:
- **ACC-01.d** ours: username refusal rule as written there; old app: 1-64 characters, no whitespace, no colon. Keep ours?
  Answer:
- **SET-04.e** ours: public address invalid for FTP, query, credentials, non-URL; old app: also invalid: no host, fragment, whitespace, over 300 characters, bad port. Keep ours?
  Answer:
- **CAL-02.a** ours: time zone, view, language, theme and clock kept on the device (SET-01.a, SHL-02.d, CAL-06.b); old app: all stored on the server and shared by every browser. Keep ours?
  Answer:
- **TIM-10** ours: default clock 12-hour in a US zone, else 24-hour; old app: 12-hour for English, 24-hour for the other five languages. Keep ours?
  Answer:
- **CAL-01.e** ours: Today returns to the current month; old app: goes to today in the current view. Keep ours?
  Answer:
- **CAL-06.a** ours: Full page button in the calendar's right zone; old app: in the page header. Keep ours?
  Answer:
- **PRT-01.d** ours: each print sheet fits one page; old app: the Itinerary flows over several pages. Keep ours?
  Answer:
- **SRH-01.a** ours: search in the top bar across events, rules, calendars, feeds, templates and History (SRH-02 groups results); old app: calendar-only search line under the calendar title. Keep ours?
  Answer:
- **FLT-01.f** ours: the Key's rule colors can be clicked to dim or hide; old app: rule color entries are not clickable; key names cut at 25 characters. Keep ours?
  Answer:
- **RUL-01.f** ours: rule conditions judged in the event's own time zone (TIM-05); old app: the server's zone. Keep ours?
  Answer:
- **TIM-04** ours: all-day event is a 24-hour event, midnight to midnight; old app: a date only, no time; an all-day event never matches a Time condition. Keep ours?
  Answer:
- **RUL-01.a** ours: text matching always ignores case; old app: ignored unless the condition's Aa toggle is on. Keep ours?
  Answer:
- **RUL-02.a** ours: regular expressions use Dart syntax; old app: the Python dialect. Keep ours?
  Answer:
- **RUL-03.a** ours: actions Change title, notes, Add text, Change length, Change time (no location); old app: Change has five targets including Location; a separate to-all-day action (RUL-03.g). Keep ours?
  Answer:
- **RUL-04.a** ours: Add event is made from an event template only; old app: a template or typed New event fields. Keep ours?
  Answer:
- **RUL-04.h** ours: Link to Event is a Then in the rule dialog; old app: a link rule has no conditions and is made from the event editor. Keep ours?
  Answer:
- **RUL-05.d** ours: new calendar-specific rule goes first, all-calendar rule last; old app: above the first shared rule that calendar uses; others at the end. Keep ours?
  Answer:
- **RUL-06.b** ours: default rules cannot be deleted; each calendar starts with two (RUL-06.c); old app: any rule can be deleted; starter rules are made once, for all calendars. Keep ours?
  Answer:
- **RUL-07.a** ours: conflict choices Put first, Keep as is, Drop and Merge; old app: Duplicate: Merge or Keep both; Shadowed: Put first, Take out, Keep as is; ten shadow kinds. Keep ours?
  Answer:
- **EVT-01.b** ours: new event with no calendar goes to the initial Local calendar; old app: refused: Add a calendar source first. Keep ours?
  Answer:
- **TPL-02.b** ours: a template fills title, location and end time (TPL-01.c: duration under 5 minutes raised to 5); old app: also fills all-day and color; a length outside 5 minutes to 24 hours is refused. Keep ours?
  Answer:
- **CFED-01.e** ours: a new feed's name and note follow the selected source until typed over; old app: computed once when added; does not follow. Keep ours?
  Answer:
- **CCCS-04.a** ours: full-day normalization by rules, originals kept in notes; old app: the parser makes a no-end midnight event all-day; rules set other lengths. Keep ours?
  Answer:
- **CON-02.c** ours: a note that only repeats the kind counts as no note; old app: an empty note stays empty; the kind is shown when never set. Keep ours?
  Answer:
- **CGOW-02.a** ours: Google calendar uses the calendar's own time zone; window starts the first day of the month (CGOW-02.j); old app: the install's zone; window starts at the destination's Start date. Keep ours?
  Answer:
- **CGOW-03.a** ours: send each event's recorded time zone to Google; old app: always the install's zone. Keep ours?
  Answer:
- **PGAP-01.a** ours: Google connecting unavailable until the client is set up and accepted; old app: on when configured, unless the last check said not ok. Keep ours?
  Answer:
- **PGAP-02.b** ours: one retry schedule: 5 seconds doubling to 15 minutes, 5 attempts; old app: calls wait 1, 2, 4, 8 seconds; recovery uses the longer schedule. Keep ours?
  Answer:
- **PGAP-02.a** ours: after exhausted failure or reauthorization, next try at the next scheduled sync; old app: next attempt within 15 minutes; paused states set no retry. Keep ours?
  Answer:
- **HIS-02.a** ours: History Types order Calendar, Rule, Event, Sync, Feed, Google, Settings, Update (HIS-01.b: sync says added and updated); old app: different order; sync says new and removed. Keep ours?
  Answer:
- **HIS-03.b** ours: undo covers rules, feeds, templates, import, merge, CCS+ removal, Hide; old app: every snapshot always holds all settings. Keep ours?
  Answer:
- **HIS-04.a** ours: a number outside 1-200 shows a field note; old app: a saved bad value falls back to 100; refused save says Between 1 and 200 changes. Keep ours?
  Answer:
- **DIA-03.a** ours: every connection shows its own sync status; old app: top-level legacy status comes from CCS+. Keep ours?
  Answer:
- **TIM-09** ours: only real time zones offered; old app: UTC or any name with a slash, excluding some prefixes. Keep ours?
  Answer:
- **CLCL-02.b** ours: import range excludes events outside it; old app: default 3,650 days each side, From and To swapped if reversed. Keep ours?
  Answer:
- **UIC-11.a** ours: emoji up to Emoji 13.0, newer ones show a note; old app: note for flags or newer than Emoji 12.0. Keep ours?
  Answer:
