# Process test 1 (Nov 19): cold read by two read-only agents (temporary)

Two agents were given only the repository and "read AGENTS.md and follow it". Nothing was changed by either (checked with git status).

## Scorecard

- **Reviewer** on a scratch copy with 13 planted faults: found 12. Missed: a connection file with no role statement (the check now catches it). Both scripted and judgment faults were found; it also reported that the script misses links to UI-nn IDs, "milliseconds" and a status such as `built` (all now checked).
- **Coder** answered five questions by following pointers; all five answers were correct. It followed the process (read the README, ran the check script). It wrote its progress file only at the end (an instruction slip, not a requirements issue).
- **Process gaps found and fixed:** `req_check.sh` now checks links to two-letter prefixes, more units, history wording ("Developer, Nov", "old app", "legacy"), statuses other than `proposed` and `backlog`, and a role statement in every connection file. The README index no longer holds derived counts (they went stale). Pure "(Developer, Nov N)" attributions were removed from statements.

## Real findings fixed

CON-01.a connection list, CON-02.d kind text (each connection states its own), UIC-29 term, UIC-05.f add dialog, PGAP-01.e and PGAP-01.h pointers, README index counts.

## Triage (Nov 19): each finding sorted by what it needs

Fixing follows: A is fixed in the one owning row (and `oldkey.md` for any ID change); B is proposed to the Product Owner because it changes how every agent works; C is dropped with the reason given; D goes to the Product Owner as a question.

### A. The requirement is wrong: fix the row (about 55 rows)

- **Repeated rules, keep one owner and link:** THM-02.g (keep the token values; THM-05.b owns the use); THM-08 (drop the sentence repeating THM-02.l); CAL-01.b (drop the hourly sentence; CAL-01.h owns it); CAL-03.a (repeats the parent); FLT-01.f (drop the last sentence, FLT-01.d owns it); PRT-01.e (repeats PRT-01.d); SRH-02.b (repeats SRH-01); EVT-01.b (TIM-02 owns the new-event time zone); EVT-01.h (CAP-01 and CAP-04 own it, delete); RUL-01.f (TIM-05 owns the time zone sentence); RUL-02.c (repeats RUL-02.b); RUL-04.e and RUL-04.f (merge); RUL-03.a and RUL-04.h (one list of actions); RUL-06.b (RUL-06.c owns default rules); CON-09.c and EVT-03.h (circular: EVT-03.h owns the ICS URL, CON-09.c links to it); CLCL-03.a (CAP-05 owns it, and it names CCS+); DEP-05.b (TIM-08 owns the default zone for an event with none); DEP-01.g (SET-06.b owns backup and restore); SET-04.i and SET-01.d (one statement that each part saves on its own); UIC-10 (THM-09 owns the palette); HIS-02.f (UIC-28.c owns status words); CAL-04.c (UIC-16 owns collapse and expand); CON-03.a and CON-03.g with UIC-28 and UIC-29.a (status words).
- **Rule is placed in the wrong feature:** CLCL-02 (UIC-33 says every calendar has the Import row, so file import belongs in `connections.md`, not only Local); HIS-01.c to .g and HIS-01.k, .l (Google rows in the generic History file; keep one pointer each or move to the Google connection files).
- **Exception wording to rewrite so the rule holds in every case:** UIC-32, UIC-27.b, UIC-33 (also repeats CCCS-05.a), EVT-04.b (names CCS+), EVT-04.f, TPL-02.c, CFED-01.c, CGOW-02.g, CCCS-01.a (an add control that "is refused"), RUL-06.c (a CCS+ special case), DEP-05.a (a rule with its own exceptions), THM-04 and THM-04.e (a border is 1 px; the focus outline and today's day are lines, not borders).
- **Undefined terms, define once (rule 8):** write budget, Activity, former Google client, Then actions, Put first, Keep as is, Drop, Merge, the wildcard characters (RUL-01.a to .c), source-qualified identity, original-start identity, handmade remote event, full check, normal synchronization, Connect me, explicit health reset, form security token, Soft palette, module kind, Full mode, bare public host, Calendar Sync credentials, Accomplished checklist. Also one name for the feed token (stream token, stream name, feed token).
- **Contradictions and wrong pointers:** PGAP-01.d and PGAP-01.e (removing the client versus changing it); EVT-01.e (malformed row); THM-06.c against DEF-01 was checked and is not a conflict (Cancel versus Saved are different things).
- **Role names:** "the Developer" in statements (SET-07, DIA-04, DEP-05.c and others) becomes the Product Owner or the user.
- **common.md** has three table layouts; bring it to the line format.

### B. A rule or a check is too weak: propose to the Product Owner

1. **Rule 7 is not testable.** About 20 rows carry several rules (HIS-03.b, PGAP-01.j, CFED-03.c, SET-05.d, DEP-02.a, DEP-02.d, DEP-05.a, DEP-05.c, RUL-06.c, EVT-01.i, EVT-03.f, EVT-04.a, EVT-04.b, CGOW-03.g, CON-06.h, ACC-02.f, SET-06.b, SET-04.b, THM-02.e, THM-02.l, THM-07.c). Proposed test: the check script warns for a statement longer than a set number of sentences or characters (a lint setting of the script, not a requirement number).
2. **Rule 7 and interfaces.** Web mechanics are banned for the page, but a program-facing interface (DIA-03 monitoring paths, the feed's ETag, the security headers in ACC-09.c, S256 in CGOW-01.m) must state its exact form. Proposed: say so in rule 7, so those rows stop being flagged.
3. **Rule 3 test misses spelled numbers** ("twelve hours", "once"). Proposed: add number words to the check.
4. **Parent and child status.** UIC-27 and SRC-01 are `proposed` with `backlog` children. Proposed rule: a parent is `backlog` only when all its sub-requirements are; the check enforces it.
5. **Row order and letters.** Rows are out of order in several files. Proposed rule: rows appear in ID order and sub-letters are contiguous; the check enforces it.
6. **Rule 8 has no home for terms.** Proposed: one terms block per feature file for its own terms, and the shared ones in `common.md`.

### C. Not a defect: dropped (with the reason)

FLT-01.b and FLT-01.c (a link and one added fact); PRT-01.a (detail of the parent); CFED-01.h and CFED-02.g (different cases); CGTW-01.d and CAP-01 (CAP-01 only points); SET-02.a and CAL-02.a (a setting versus a temporary view); DIA-01.b and UIC-25 (what is copied); the same evidence cells in several account rows (temporary column); the exception-wording warnings that are conditions (ACC-02.f, ACC-05.d, FLT-01.g, DEP-04, DEP-04.a, HIS-04, SET-05.h); CON-06.a naming curl, DIA-02.e naming GitHub and CFED-03.a naming Google and Apple (these are the requirement itself); SRH-01.f and EVT-01.d citing UIC-13; HIS-01.h evidence citing HIS-21 (temporary evidence); the README counts (removed from the index).

### D. The Product Owner decides (questions)

Already in `open-questions.md`: kind text per connection; removing the Google API client; a feed's status line; one-way and two-way Google rows; the update stream; limit on connections.
New: (1) limits for lists the user grows (connections, Local calendars, feeds, rules, templates, custom events, deletion markers, extra public addresses, imports, debug captures, the last received file): one policy or one limit each; (2) the section name: Calendars (UIC-05.b, FLT-01.f, THM-02.l) or Sources (SRC-01.a); (3) ACC-05.c (a secret is never written to a log) against HIS-04.b (secrets are masked, with a Show secrets switch); (4) CLCL-01.d (a new Local calendar is added to every feed) against CFED-01.c (a feed decides what it carries); (5) DIA-04 and DOC-03 (the Dashboard, the CHANGELOG and the README are process, not app behavior): move to the Scrum rewrite? (6) UIC-12 says the language dropdown is multi-select, but a language is one choice.

## Round 2 (Nov 19): Reviewer on the real repository, Coder on five new questions

Both read-only (git status clean before and after). The Reviewer read all 30 files and reported only new findings; the Coder answered all five questions correctly by following pointers, and listed what it could not decide.

### Fixed (A)

- The requirement rows UIC-11, UIC-11.a and UIC-11.b sat outside their table after a loose "Pending:" line; an empty heading removed; "(Developer ...)" attributions removed from common.md.
- README index links pointed at `requirements/requirements/x.md`; fixed.
- File headers listed issue numbers (Issues live in GitHub); removed from calendar, diagnostics, events, rules, settings, shell, CGOW and CFED.
- Repeated rules removed: DEP-01.a, CGTW-01.e, EVT-01.h, SRC-01.b, FDS-01.b; date-range limit for published calendars said once (CON-09.e); DEP-04.a, SHL-01.a, EVT-05.a, SRH-01.c trimmed.
- THM-05.b (no exception: a button that shows no status), THM-02 (palette is in THM-09), EVT-01.i (Move added), two wrong pointers in CCCS, and the connections terms (one-way and two-way describe both inbound and outbound connections).
- `req_check.sh` no longer writes any file (the Coder skipped it for that reason), and it now reports a row outside its table and a README link to a missing file.

### Still to triage (new, from round 2)

- **Placement:** PGAP-01.a/.d/.e/.m and PGAP-02 still describe connections (plugins.d/README rule 3); THM-08.a/.b/.c are filed under the module border; FLT-01.i belongs with the calendar header (CAL-06); CLNK-01.c holds a CCS+ preset; SET-01.a and SET-01.d lists are incomplete (Password requirements, Administrator email, Language, Time Zones, Search, Backup); EVT-04.a repeats CAP-02, EVT-04.b repeats EVT-01.i.
- **Numbers (rule 3):** UIC-07 and UIC-14 (24 by 24 px), UIC-32 (20 words), CAL-04.f (2:3), SHL-05.b (one year), SET-05.a (lists the values it says are in DEF-01), RUL-01.i, RUL-03.g and RUL-06.c (point at the whole-day tolerance in DEF-01), THM-06.c (repeats the Save pulse in DEF-01).
- **Self-links:** a sub-requirement citing its own parent (RUL-04.b/.c, RUL-05.b/.c, RUL-07.d to .f, HIS-03.b, EVT-04.c, DIA-01.a, SHL-02.b, SHL-03.a).
- **Terms (rule 8):** Activity, outside address (circular), the browser, browser-patient and curl modes, invalid CCS+ username, ordinary feed and next-push, the regex tester, initial secret, assisted-setup request, source presets, combined destination, Upload & publish against Manual Upload, "source" in CON-02 to CON-08 against feed-only connections.
- **Rows with several rules (rule 7):** RUL-03.c, RUL-05.d, EVT-05.d, CLNK-01.c; history wording in RUL-04.h/.i, EVT-06.a, SHL-03.b, SHL-01.c, PRT-01.h, DOC-01.a; page mechanics in EVT-03.a, SHL-02.f/.h.
- **Content gaps:** TPL-02.b fills only title, location and end time though a template stores color and notes; CGTW-01.a lists only title, location and start time; the language list in SHL-02.a to .c differs (Belgian Dutch or Dutch); the favicon is described twice (SHL-01.b and SHL-01.d); common.md mixes 4-column and 5-column rows (UIC-37 has 4).
