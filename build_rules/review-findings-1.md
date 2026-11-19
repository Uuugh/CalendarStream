# Process test 1 (Nov 19): cold read by two read-only agents (temporary)

Two agents were given only the repository and "read AGENTS.md and follow it". Nothing was changed by either (checked with git status).

## Scorecard

- **Reviewer** on a scratch copy with 13 planted faults: found 12. Missed: a connection file with no role statement (the check now catches it). Both scripted and judgment faults were found; it also reported that the script misses links to UI-nn IDs, "milliseconds" and a status such as `built` (all now checked).
- **Coder** answered five questions by following pointers; all five answers were correct. It followed the process (read the README, ran the check script). It wrote its progress file only at the end (an instruction slip, not a requirements issue).
- **Process gaps found and fixed:** `req_check.sh` now checks links to two-letter prefixes, more units, history wording ("Developer, Nov", "old app", "legacy"), statuses other than `proposed` and `backlog`, and a role statement in every connection file. The README index no longer holds derived counts (they went stale). Pure "(Developer, Nov N)" attributions were removed from statements.

## Real findings fixed

CON-01.a connection list, CON-02.d kind text (each connection states its own), UI-29 term, UI-05.f add dialog, GAP-01.e and GAP-01.h pointers, README index counts.

## Findings left to triage (row IDs, by kind)

Triage each against the README rules; fix in the one owning row, record ID changes in `oldkey.md`.

- **Repeated rules (rule 1):** THM-02.g and THM-05.b; THM-02/THM-08 border colors; THM-08.a/.b/.c; CAL-01.b and CAL-01.h; CAL-03.a/.d; CAL-04.c; FLT-01.b/.c/.d/.f; PRT-01.a/.e; SRH-02.b; EVT-01.b/.h; EVT-06.c and CAL-05.e; RUL-01.f and TIM-05; RUL-02.c; RUL-04.e/.f; RUL-04.h and RUL-03.a; RUL-06.b/.c; HIS-02.f and UI-28; HIS-04.b and ACC-05.d (Show secrets); FED-01.h and FED-02.g; CON-09.a, CON-09.d; CON-09.c and EVT-03.h (each says the other owns the ICS URL); LCL-03.a and CAP-05; LCL-01.b and CAP-06; GTW-01.d and CAP-01; GOW-03.a; DEP-05.b with TIM-08 and SET-06.a; DEP-01.g and SET-06.b; SET-01.d and SET-04.i; SET-02.a and CAL-02.a; ACC-04 with SET-06.c and UI-18; DIA-01.b and UI-25; UI-10 and THM-09.
- **Contradictions (rule 2):** one-way Google sync is said not to read back (GOW-04.k) yet GOW-04.b, .c, .g and GOW-05 describe reading Google edits (see the open question); TIM-10 and CAL-06 are fixed; EVT-06.b and CAP-03; LCL-01.d and FED-01.c; LCL-02.a and its parent; THM-04 and THM-04.e (1 px borders); ACC-05.c (never logged) and ACC-05.d (shown when switched on); DEP-05.a (database overrides, with exceptions).
- **Exception wording to review:** UI-32, UI-27.b, UI-33, EVT-04.b, EVT-04.f, TPL-02.c, FED-01.c, GOW-02.g, CCS-01.a, RUL-06.c.
- **Numbers outside DEF-01 (rule 3):** UI-14, UI-07, UI-16, UI-10, UI-32 (counts), CAL-04.f (2:3), PRT-01.i (5 mm), FLT-01.f (three rows), SRH-01.h, RUL-01.i/RUL-03.g/RUL-06.c ("near whole-day"), CCS-03.b, GAP-02.a/.c, SHL-05.b, FED-03.c (twelve hours), DEP-03.b.
- **Limits not stated for lists that grow (rule 9):** connections (CON-01.d), Local calendars, feeds, rules, event templates, custom events and deletion markers, extra public addresses, imports, debug captures, the last received file (DIA-01.c).
- **Undefined terms (rule 8):** write budget, Activity, former Google client, Then actions, Put first/Keep as is/Drop/Merge, wildcard meanings (RUL-01.a/.b/.c), source-qualified and original-start identity, handmade remote event, full check, Connect me, explicit health reset, form security token, Soft palette, module kind, Full mode, bare public host.
- **Rows with several rules (rule 7):** HIS-03.b, GAP-01.j, FED-03.c, SET-05.d, DEP-02.a, DEP-02.d, DEP-05.a, DEP-05.c, RUL-06.c, EVT-01.i, EVT-03.f, EVT-04.a, EVT-04.b, GOW-03.g, CON-06.h, ACC-02.f, SET-06.b, SET-04.b, THM-02.e, THM-02.l, THM-07.c.
- **Wire and web mechanics (rule 7):** ACC-02.a/.f, ACC-09.c, FED-02.c, FED-04.a/.b, GOW-01.m/.n, SHL-02.f, SHL-05.b, DIA-03.a/.b, DEP-03.a, DEP-02.c, SET-07.b, CON-06.g/.i, EVT-03.a.
- **Naming:** stream token or stream name or feed token; the section called Calendars (UI-05.b, FLT-01.f, THM-02.l) or Sources; "source", "imported", "downloaded" and "connection".
- **Malformed or out of order:** EVT-01.e (cut off); common.md has three table layouts; IDs out of order in several files; UI-27 parent `proposed` with `backlog` children (and SRC-01).
- **Not requirements of the app:** DIA-04 and DOC-03 (documents and the Dashboard are process); the "Dart note" and "Conversion progress" paragraphs at the end of theme.md.
