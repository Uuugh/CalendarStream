# Old keys: the history of rekeying

When requirements are reorganized or renumbered, the old ID and its new ID are recorded here, so any old reference (in CHANGELOG.md, an issue, a note or a test name) can be found with one search. Rows are only added, never edited or removed. To trace an old ID, search it in the `old ID` column; if its new ID was later rekeyed, search that in turn.

An ID can mean something different before and after a batch (the old ACC-01 was a legacy login import; since R1 it is the Initial setup requirement). A reference older than a batch's date means the old meaning.

Columns: `batch` (R1, R2, ... in order), `date`, `old ID`, `new ID(s)` (several for a split, "retired" for a drop), `note`.

| batch | date | old ID | new ID(s) | note |
|---|---|---|---|---|
| R1 | 2026-11-18 | ACC-01 | ACC-01.f | legacy page login import (now a question) |
| R1 | 2026-11-18 | ACC-02 | ACC-01.a | |
| R1 | 2026-11-18 | ACC-03 | ACC-01.b | |
| R1 | 2026-11-18 | ACC-04 | ACC-01.d | |
| R1 | 2026-11-18 | ACC-05 | ACC-01.e | |
| R1 | 2026-11-18 | ACC-06 | ACC-02.a | |
| R1 | 2026-11-18 | ACC-07 | ACC-02.e | |
| R1 | 2026-11-18 | ACC-08 | ACC-03.a | |
| R1 | 2026-11-18 | ACC-09 | ACC-03.b | |
| R1 | 2026-11-18 | ACC-10 | ACC-03.c | |
| R1 | 2026-11-18 | ACC-11 | ACC-05 | secret protection |
| R1 | 2026-11-18 | ACC-12 | ACC-02.a | merged earlier on Nov 18 |
| R1 | 2026-11-18 | ACC-13 | ACC-09.a | |
| R1 | 2026-11-18 | ACC-14 | ACC-09.b | |
| R1 | 2026-11-18 | ACC-15 | ACC-09.c | |
| R1 | 2026-11-18 | ACC-16 | ACC-06.a, ACC-07.a | split: failure limit and global block |
| R1 | 2026-11-18 | ACC-17 | ACC-07.b | |
| R1 | 2026-11-18 | ACC-18 | ACC-02.b | |
| R1 | 2026-11-18 | ACC-19 | ACC-02.b | merged earlier on Nov 18 |
| R1 | 2026-11-18 | ACC-20 | ACC-02.c | |
| R1 | 2026-11-18 | ACC-21 | ACC-08.a | |
| R1 | 2026-11-18 | ACC-22 | ACC-07.c | |
| R1 | 2026-11-18 | ACC-23 | ACC-07.d | |
| R1 | 2026-11-18 | ACC-24 | ACC-08.b | |
| R1 | 2026-11-18 | ACC-25 | ACC-08.c | |
| R1 | 2026-11-18 | ACC-26 | ACC-04.a | |
| R1 | 2026-11-18 | ACC-27 | retired | Google traffic is visible only to the signed-in user (GGL-02); dropped earlier on Nov 18 |
| R1 | 2026-11-18 | ACC-28 | ACC-06.b | |
| R1 | 2026-11-18 | ACC-29 | ACC-02.d | |
| R1 | 2026-11-18 | ACC-30 | ACC-03.d | |
| R1 | 2026-11-18 | ACC-31 | ACC-06.e | |
| R1 | 2026-11-18 | ACC-32 | ACC-06.c | |
| R1 | 2026-11-18 | ACC-33 | ACC-06.d | |
| R1 | 2026-11-18 | ACC-34 | ACC-01.c | |
| R1 | 2026-11-18 | ACC-35 | ACC-04.b | |
| R2 | 2026-11-18 | ACC-01.b | ACC-01.b, ACC-01.g, ACC-01.h | split: the setup code (requirement, case and dash, incorrect code) |
| R2 | 2026-11-18 | ACC-01.d | ACC-01.d | the weak-password sentence dropped (it is ACC-04.a) |
| R2 | 2026-11-18 | ACC-02.b | ACC-02.b, ACC-02.f | split: sign-in result and where the user goes next |
| R2 | 2026-11-18 | ACC-05 | ACC-05, ACC-05.a, ACC-05.b, ACC-05.c, ACC-05.d | split: hashed passwords, encrypted credentials, logs, pages |
| R2 | 2026-11-18 | ACC-07.a | ACC-07.a, ACC-07.e, ACC-07.f, ACC-07.h | split: start of the block, refusal, 7-day address, end of the block |
| R2 | 2026-11-18 | ACC-08.a | ACC-08.a, ACC-08.d | split: the warning and its unlock link |
| R3 | 2026-11-18 | ACC-04.c | ACC-04.d | the empty-password question is answered by ACC-04.a (Developer, Nov 18: passwords are enforced after all) |
| R3 | 2026-11-18 | ACC-05.d | ACC-05.d | the question is answered: the Show secrets switch in History (HIS-34) |
| R4 | 2026-11-18 | GGL-01, GGL-02, GGL-03, GGL-04 | retired | the Beta feature is deleted (Developer, Nov 18): it duplicated Sync Now and the health chip, and History covers the rest |
| R4 | 2026-11-18 | GGL-88 | retired | the Google traffic log went with the Beta feature |
| R0 | 2026-11-18 | CAL-78, CAL-71, CAL-68 | merged | into CAL-33, CAL-60, CAL-39 as they were before R5 |
| R5 | 2026-11-18 | CAL-04 | CAL-04.a | and its footer part is CAL-04.e (was CAL-73) |
| R5 | 2026-11-18 | CAL-15 | CAL-03.a, CAL-03.b, CAL-03.c, CAL-03.d | split; the press time is also SET-62 |
| R5 | 2026-11-18 | CAL-19 | retired | duplicated TIM-03 |
| R5 | 2026-11-18 | CAL-25 | CAL-02.a | |
| R5 | 2026-11-18 | CAL-27 | CAL-01.d | |
| R5 | 2026-11-18 | CAL-30 | CAL-01.a | |
| R5 | 2026-11-18 | CAL-33 | CAL-01.b | |
| R5 | 2026-11-18 | CAL-34 | CAL-01.c | |
| R5 | 2026-11-18 | CAL-39 | CAL-05.b | |
| R5 | 2026-11-18 | CAL-41 | CAL-05.d | |
| R5 | 2026-11-18 | CAL-42 | CAL-05.e | |
| R5 | 2026-11-18 | CAL-57 | CAL-04.b, CAL-04.c | split: resize bar and Collapse/Expand |
| R5 | 2026-11-18 | CAL-59 | CAL-04.d | |
| R5 | 2026-11-18 | CAL-60 | CAL-05.c | |
| R5 | 2026-11-18 | CAL-65 | retired | duplicated TIM-04 |
| R5 | 2026-11-18 | CAL-66 | CAL-05.a | |
| R5 | 2026-11-18 | CAL-67 | CAL-05.f | |
| R5 | 2026-11-18 | CAL-69 | CAL-05.g | |
| R5 | 2026-11-18 | CAL-70 | CAL-05.j | |
| R5 | 2026-11-18 | CAL-72 | CAL-05.h | |
| R5 | 2026-11-18 | CAL-73 | CAL-04.e | |
| R5 | 2026-11-18 | CAL-74 | CAL-01.f | |
| R5 | 2026-11-18 | CAL-75 | CAL-01.e | |
| R5 | 2026-11-18 | CAL-76 | CAL-01.g | |
| R5 | 2026-11-18 | CAL-77 | CAL-05.i | |
| R6 | 2026-11-18 | CAL-02.b | CAL-06.b | the question is answered: right-zone choices stay on the device until changed (Developer, Nov 18) |
| R7 | 2026-11-18 | CAL-05.a | UI-22.a | print follows what the user sees; Print Preview became shared UI (UI-22) |
| R7 | 2026-11-18 | CAL-05.b | UI-22.b | the print choices are kept on the device |
| R7 | 2026-11-18 | CAL-05.c | CAL-05.a | automatic orientation; the generic part is UI-22.c |
| R7 | 2026-11-18 | CAL-05.d | CAL-05.c, UI-22.f | two months, and honoring the theme |
| R7 | 2026-11-18 | CAL-05.e | CAL-05.b | Itinerary |
| R7 | 2026-11-18 | CAL-05.f | CAL-05.d | Print All; the date range is UI-23 |
| R7 | 2026-11-18 | CAL-05.g | UI-22.d | page fit |
| R7 | 2026-11-18 | CAL-05.h | UI-22.e | titles wrap |
| R7 | 2026-11-18 | CAL-05.i | CAL-05.e | |
| R7 | 2026-11-18 | CAL-05.j | CAL-05.b | the printable views |
| R7 | 2026-11-18 | FED-14 | UI-23 | an end before the start is not valid |
| R8 | 2026-11-18 | UI-22, UI-22.a, UI-22.b, UI-22.c, UI-22.d, UI-22.e, UI-22.f | PRT-01, PRT-01.a, PRT-01.b, PRT-01.c, PRT-01.d, PRT-01.e, PRT-01.f | Print is its own feature (print.md), used by the Calendar and Events; PRT-01.g is new |
| R9 | 2026-11-18 | SHL-12 | SET-05 | the page's sections are the modules SET-05 lists (and the Beta section is gone) |
| R9 | 2026-11-18 | SRC-91 | SRC-42 | retained deletions are kept until they leave History (HIS-09) |
