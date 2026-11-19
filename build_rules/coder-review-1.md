# Coder review 1 (Nov 19): six agents, one per slice, triaged (temporary)

Six read-only agents read every row of their slice, followed each pointer, and reported the rows they could not turn into code from the text alone. The repository was unchanged afterwards (git status clean). Each used about 87,000 to 114,000 tokens and 2.3 to 4.6 minutes.

## Baseline (to compare with the next run)

| Slice | Files | Rows read | Could not implement |
|---|---|---|---|
| 1. Account, settings, shell | 3 | 130 | about 62 |
| 2. Calendar, print, search, filter | 4 | 66 | 32 |
| 3. Rules, events, templates | 3 | 117 | 79 |
| 4. Connections | 8 | about 255 | about 62 |
| 5. Sections, plugins, history, diagnostics, documentation, deployment | 9 | 111 | 62 |
| 6. Shared UI, look, rules (common, theme, README) | 3 | about 220 | about 93 |
| **Total** | 30 | about 900 | about 390 (43%) |

Several rows share a cause, so the second number overstates the number of separate defects.

## A. The requirement is wrong: fix the row

**Contradictions between rows (law 2)**
- CAL-02.a (the zone picked in the calendar is temporary) and CAL-06.b (the time zone is a user setting).
- THM-02.b (card is the words on a filled button) and THM-02.g, THM-05.b (onaccent is); THM-03 (icons use the text color) and THM-05.a (muted); THM-04 and THM-04.e (1 px borders and two 2 px lines).
- UIC-27.a and DEF-01 (Saved or Cancelled shown for 3 seconds) and THM-06.c (Cancel takes 1 s); UIC-27.c and DEF-01 (Save pulse "about 5 seconds") against THM-06.c (five pulses).
- RUL-01.e (unbracketed AND and OR "in order" but `A OR B AND C` differs from `(A OR B) AND C`: AND binds tighter, say so); RUL-07.e (a lower rule's emoji can be shadowed) and RUL-03.c (a lower rule still adds its emoji).
- EVT-01.c (start and end times are required) and EVT-02.e (an all-day event has no times); TPL-01.a (keeps its duration exactly) and TPL-01.c (raises a short one).
- SET-01.a (two headings) and SET-01.d (one ordered list, "Theme last"); SET-05.b (the stream comes from the install) and SET-07.c (the stream is chosen in Settings).
- SRH-01.c (no date limit) and DEF-01 (recurrence expansion 1 year back and 2 ahead); CAL-05.d (Print All "sets" a range) and UIC-23 (All is an empty range).
- UIC-12 (multi-select) and the view and language dropdowns (single choice); SET-06.e and SHL-01.d (a custom logo is one PNG, the title bar has a light and a dark mark); DOC-03.a and DOC-03.c (documents removed, the CHANGELOG never rewritten); CAP-03 and CAP-02 against EVT-04.f (imported events are never deleted).
- PGAP-01.a/.d/.m and PGAP-02 describe connections (plugins.d/README rule 3); CGOW-04.k (one-way does not read back) against CGOW-04.b/.c and CGOW-05.c (question already open).

**Wrong or legacy pointers (rule 6)**
- Statements that point at the legacy file `build_rules/theme.md` (UIC-07.a, UIC-14, UIC-15, many THM evidence cells): the badge anchors, offsets and popover values must be ported into THM rows.
- RUL-04.g cites CAP-01 (CAP-02 is meant); EVT-01.d and SET-05.l cite UIC-13 (it does not say that); EVT-05.a and RUL-04.h cite UIC-09 for picking an event; RUL-03.j cites UIC-30 for the Then actions; CCCS-02.j cited SET-01 (fixed).

**Terms to define once (rule 8)**
Event line (a unit in the theme), Activity, write budget, eligible, conflict (events), outside address, regex tester, evaluation run, Then, Change time, Add text, Full mode, Configure heading, event states (Edited, Changed by the source since the edit, Hidden from Google, Deleted), main calendar, health (its look), neutral status, found result, source-qualified identity, original-start identity, combined destination, synchronized marker, bare public host, rule tag and stale, event card, kind text of each connection.

**Rows to complete from what the rows already say**
README: define the Author, the Coder and the Product Owner, add DEF to the Prefixes list, say UIC in the common.md headings; common.md rows in three column layouts (bring them to the line format so the check can read them); TPL-02.b (a template also fills color and notes); CGTW-01.a (all fields, not three); the language list in SHL-02.a to .c.

## B. A rule or a check is too weak: propose

1. `req_check.sh` skips `common.md` (numbers outside DEF-01, exception wording, column layout). Proposed: bring `common.md` to the line format and scan it like every other file.
2. Rule 6 is checked only for IDs. Proposed: the check reports any `build_rules/` path or "section N" in a statement.
3. "Simulate three jobs" (Checking a feature file) has no pass criterion. Proposed: pass means a Coder agent run of that file reports no row it cannot implement.
4. Rule 9 and DEF-02: lists with no stated limit (the remembered Record changes list, suppressed warnings, templates, rules) are not found by any check. Proposed: review question only, listed with the rule.

## C. Answer from the Python app, not by asking (rule 10)

These are behaviors the old app already has; the Author reads the app and writes the rows, then the Product Owner reviews them.
- **Rules:** word characters and wildcards (`*`, `#`, `?`, anchoring, escaping), inclusive bounds of day, time and date conditions, midnight-spanning events, week start; the "no end time" and "near whole-day" tests; the two starter rules; the Change time and Add text actions; the "what it does" wording; the title generator; duplicate and shadow detection.
- **Events and templates:** the typed-time grammar, the end-time suggestions, the offered reminder times, meeting-link patterns, the map link, the template duration forms.
- **Account and security:** the strength estimate and bar levels, the token alphabet (22 characters for 128 bits), the setup code and its retrieval, recovery link and warning, the cookie lifetime, the username rules, the encryption of stored credentials.
- **Updates and deployment:** how releases are looked up, the updater protocol, the backup and restore format, the environment variable names and defaults, STACK_NO and PORT.
- **Time:** the time zone form stored with an event (IANA name), the all-day day-saving rule, the "US zone" test for the 12/24 default.
- **Downloads and Google:** the timeout and redirect limits for non-CCS+ downloads, what "malformed" and "HTML" mean, the callback and notification paths, the retry and pause details, what the synchronized marker is.

## D. The Product Owner decides

- **Missing features:** template management (add, edit, delete, order, the dialog), the link-rule model and its dialog (RUL-04.h, RUL-04.i, EVT-05.d to .h), what each section prints (PRT-01.h, "still to be designed"), the Search interface and its match rules (SRH-01.a), the Report a problem fields and the GitHub address (DIA-02).
- **Web rows in a Flutter port:** which rows drop because they describe a browser (SHL-05 caching, SHL-02.f and .h, ACC-09.c security headers, the cookie, `/api/status` and `/healthz` paths)?
- **Naming:** the section is Calendars or Sources (UIC-05.a, THM-02.l, SRC-01.a).
- **Secrets in logs:** ACC-05.c (never written to a log) against HIS-04.b (a Show secrets switch).
- **The 17 questions already in `open-questions.md`.**
