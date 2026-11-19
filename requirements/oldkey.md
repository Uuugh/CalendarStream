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
| R10 | 2026-11-19 | SRC-16 | SRC-01.a |  |
| R10 | 2026-11-19 | SRC-17 | SRC-01.b |  |
| R10 | 2026-11-19 | SRC-60 | SRC-01.c |  |
| R10 | 2026-11-19 | SRC-18 | SRC-01.d |  |
| R10 | 2026-11-19 | SRC-61 | SRC-01.e |  |
| R10 | 2026-11-19 | SRC-30 | SRC-01.f |  |
| R10 | 2026-11-19 | SRC-28 | SRC-01.g |  |
| R10 | 2026-11-19 | SRC-39 | SRC-01.h |  |
| R10 | 2026-11-19 | SRC-92 | SRC-01.i |  |
| R10 | 2026-11-19 | SRC-73 | SRC-01.j |  |
| R10 | 2026-11-19 | SRC-57 | SRC-02.a |  |
| R10 | 2026-11-19 | SRC-59 | SRC-02.b |  |
| R10 | 2026-11-19 | SRC-34 | SRC-02.c |  |
| R10 | 2026-11-19 | SRC-35 | SRC-02.d |  |
| R10 | 2026-11-19 | SRC-80 | SRC-02.e |  |
| R10 | 2026-11-19 | SRC-13 | SRC-03.a |  |
| R10 | 2026-11-19 | SRC-12 | SRC-03.b |  |
| R10 | 2026-11-19 | SRC-11 | SRC-03.c |  |
| R10 | 2026-11-19 | SRC-29 | SRC-03.d |  |
| R10 | 2026-11-19 | SRC-09 | SRC-03.e |  |
| R10 | 2026-11-19 | SRC-10 | SRC-03.f |  |
| R10 | 2026-11-19 | SRC-08 | SRC-03.g |  |
| R10 | 2026-11-19 | SRC-07 | SRC-03.h |  |
| R10 | 2026-11-19 | SRC-14 | SRC-03.i |  |
| R10 | 2026-11-19 | SRC-26 | SRC-03.j |  |
| R10 | 2026-11-19 | SRC-81 | SRC-03.k |  |
| R10 | 2026-11-19 | SRC-06 | SRC-03.l |  |
| R10 | 2026-11-19 | SRC-02 | SRC-04.a |  |
| R10 | 2026-11-19 | SRC-04 | SRC-04.b |  |
| R10 | 2026-11-19 | SRC-03 | SRC-04.c |  |
| R10 | 2026-11-19 | SRC-05 | SRC-04.d |  |
| R10 | 2026-11-19 | SRC-72 | SRC-04.e |  |
| R10 | 2026-11-19 | SRC-15 | SRC-05.a |  |
| R10 | 2026-11-19 | SRC-52 | SRC-05.b |  |
| R10 | 2026-11-19 | SRC-54 | SRC-05.c |  |
| R10 | 2026-11-19 | SRC-84 | SRC-05.d |  |
| R10 | 2026-11-19 | SRC-53 | SRC-05.e |  |
| R10 | 2026-11-19 | SRC-48 | SRC-05.f |  |
| R10 | 2026-11-19 | SRC-49 | SRC-05.g |  |
| R10 | 2026-11-19 | SRC-50 | SRC-05.h |  |
| R10 | 2026-11-19 | SRC-51 | SRC-05.i |  |
| R10 | 2026-11-19 | SRC-55 | SRC-05.j |  |
| R10 | 2026-11-19 | SRC-85 | SRC-05.k |  |
| R10 | 2026-11-19 | SRC-56 | SRC-05.l |  |
| R10 | 2026-11-19 | SRC-62 | SRC-05.m |  |
| R10 | 2026-11-19 | SRC-63 | SRC-05.n |  |
| R10 | 2026-11-19 | SRC-65 | SRC-06.a |  |
| R10 | 2026-11-19 | SRC-66 | SRC-06.b |  |
| R10 | 2026-11-19 | SRC-67 | SRC-06.c |  |
| R10 | 2026-11-19 | SRC-82 | SRC-06.d |  |
| R10 | 2026-11-19 | SRC-68 | SRC-06.e |  |
| R10 | 2026-11-19 | SRC-69 | SRC-07.a |  |
| R10 | 2026-11-19 | SRC-70 | SRC-07.b |  |
| R10 | 2026-11-19 | SRC-19 | SRC-07.c |  |
| R10 | 2026-11-19 | SRC-75 | SRC-07.d |  |
| R10 | 2026-11-19 | SRC-89 | SRC-07.e |  |
| R10 | 2026-11-19 | SRC-01 | SRC-07.f |  |
| R10 | 2026-11-19 | SRC-74 | SRC-07.g |  |
| R10 | 2026-11-19 | SRC-42 | SRC-07.h |  |
| R10 | 2026-11-19 | SRC-41 | SRC-08.a |  |
| R10 | 2026-11-19 | SRC-43 | SRC-08.b |  |
| R10 | 2026-11-19 | SRC-44 | SRC-08.c |  |
| R10 | 2026-11-19 | SRC-76 | SRC-08.d |  |
| R10 | 2026-11-19 | SRC-77 | SRC-08.e |  |
| R10 | 2026-11-19 | SRC-71 | SRC-08.f |  |
| R10 | 2026-11-19 | SRC-25 | SRC-08.g |  |
| R10 | 2026-11-19 | SRC-45 | SRC-08.h |  |
| R10 | 2026-11-19 | SRC-31 | SRC-09.a |  |
| R10 | 2026-11-19 | SRC-40 | SRC-09.b |  |
| R10 | 2026-11-19 | SRC-20 | SRC-09.c |  |
| R10 | 2026-11-19 | SRC-83 | SRC-09.d |  |
| R10 | 2026-11-19 | SRC-58 | SRC-09.e |  |
| R10 | 2026-11-19 | SRC-87 | SRC-09.f |  |
| R10 | 2026-11-19 | SRC-21 | SRC-10.a |  |
| R10 | 2026-11-19 | SRC-36 | SRC-10.b |  |
| R10 | 2026-11-19 | SRC-37 | SRC-10.c |  |
| R10 | 2026-11-19 | SRC-46 | SRC-10.d |  |
| R10 | 2026-11-19 | SRC-78 | SRC-10.e |  |
| R10 | 2026-11-19 | SRC-47 | SRC-10.f |  |
| R10 | 2026-11-19 | SRC-22 | DEP-14 | merged or dropped |
| R11 | 2026-11-19 | FED-05 | FED-01.a |  |
| R11 | 2026-11-19 | FED-06 | FED-01.b |  |
| R11 | 2026-11-19 | FED-30 | FED-01.c |  |
| R11 | 2026-11-19 | FED-13 | FED-01.d |  |
| R11 | 2026-11-19 | FED-31 | FED-01.e |  |
| R11 | 2026-11-19 | FED-15 | FED-01.f |  |
| R11 | 2026-11-19 | FED-07 | FED-01.g |  |
| R11 | 2026-11-19 | FED-28 | FED-01.h |  |
| R11 | 2026-11-19 | FED-11 | FED-01.i |  |
| R11 | 2026-11-19 | FED-25 | FED-02.a |  |
| R11 | 2026-11-19 | FED-10 | FED-02.b |  |
| R11 | 2026-11-19 | FED-08 | FED-02.c |  |
| R11 | 2026-11-19 | FED-27 | FED-02.d |  |
| R11 | 2026-11-19 | FED-09 | FED-02.e |  |
| R11 | 2026-11-19 | FED-23 | FED-02.f |  |
| R11 | 2026-11-19 | FED-04 | FED-02.g |  |
| R11 | 2026-11-19 | FED-01 | FED-03.a |  |
| R11 | 2026-11-19 | FED-24 | FED-03.b |  |
| R11 | 2026-11-19 | FED-34 | FED-03.c |  |
| R11 | 2026-11-19 | FED-03 | FED-04.a |  |
| R11 | 2026-11-19 | FED-29 | FED-04.b |  |
| R11 | 2026-11-19 | FED-17 | FED-04.c |  |
| R11 | 2026-11-19 | FED-38 | FED-04.d |  |
| R11 | 2026-11-19 | FED-40 | FED-04.e |  |
| R11 | 2026-11-19 | FED-18 | FED-04.f |  |
| R11 | 2026-11-19 | FED-02 | FED-05.a |  |
| R11 | 2026-11-19 | FED-19 | FED-05.b |  |
| R11 | 2026-11-19 | FED-12 | DEP-14 | merged or dropped |
| R11 | 2026-11-19 | FED-21 | DEP-14 | merged or dropped |
| R12 | 2026-11-19 | RUL-03 | RUL-01.a |  |
| R12 | 2026-11-19 | RUL-04 | RUL-01.b |  |
| R12 | 2026-11-19 | RUL-45 | RUL-01.c |  |
| R12 | 2026-11-19 | RUL-05 | RUL-01.d |  |
| R12 | 2026-11-19 | RUL-06 | RUL-01.e |  |
| R12 | 2026-11-19 | RUL-07 | RUL-01.f |  |
| R12 | 2026-11-19 | RUL-08 | RUL-01.g |  |
| R12 | 2026-11-19 | RUL-09 | RUL-01.h |  |
| R12 | 2026-11-19 | RUL-10 | RUL-01.i |  |
| R12 | 2026-11-19 | RUL-44 | RUL-02.a |  |
| R12 | 2026-11-19 | RUL-22 | RUL-02.b |  |
| R12 | 2026-11-19 | RUL-56 | RUL-02.c |  |
| R12 | 2026-11-19 | RUL-11 | RUL-03.a |  |
| R12 | 2026-11-19 | RUL-37 | RUL-03.b |  |
| R12 | 2026-11-19 | RUL-12 | RUL-03.c |  |
| R12 | 2026-11-19 | RUL-13 | RUL-03.d |  |
| R12 | 2026-11-19 | RUL-14 | RUL-03.e |  |
| R12 | 2026-11-19 | RUL-15 | RUL-03.f |  |
| R12 | 2026-11-19 | RUL-16 | RUL-03.g |  |
| R12 | 2026-11-19 | RUL-43 | RUL-03.h |  |
| R12 | 2026-11-19 | RUL-55 | RUL-03.i |  |
| R12 | 2026-11-19 | RUL-53 | RUL-03.j |  |
| R12 | 2026-11-19 | RUL-17 | RUL-04.a |  |
| R12 | 2026-11-19 | RUL-63 | RUL-04.b |  |
| R12 | 2026-11-19 | RUL-64 | RUL-04.c |  |
| R12 | 2026-11-19 | RUL-23 | RUL-04.d |  |
| R12 | 2026-11-19 | RUL-18 | RUL-04.e |  |
| R12 | 2026-11-19 | RUL-65 | RUL-04.f |  |
| R12 | 2026-11-19 | RUL-51 | RUL-04.g |  |
| R12 | 2026-11-19 | RUL-02 | RUL-04.h |  |
| R12 | 2026-11-19 | RUL-01 | RUL-04.i |  |
| R12 | 2026-11-19 | RUL-24 | RUL-05.a |  |
| R12 | 2026-11-19 | RUL-46 | RUL-05.b |  |
| R12 | 2026-11-19 | RUL-48 | RUL-05.c |  |
| R12 | 2026-11-19 | RUL-25 | RUL-05.d |  |
| R12 | 2026-11-19 | RUL-26 | RUL-05.e |  |
| R12 | 2026-11-19 | RUL-30 | RUL-05.f |  |
| R12 | 2026-11-19 | RUL-57 | RUL-05.g |  |
| R12 | 2026-11-19 | RUL-61 | RUL-05.h |  |
| R12 | 2026-11-19 | RUL-39 | RUL-05.i |  |
| R12 | 2026-11-19 | RUL-27 | RUL-06.a |  |
| R12 | 2026-11-19 | RUL-28 | RUL-06.b |  |
| R12 | 2026-11-19 | RUL-29 | RUL-06.c |  |
| R12 | 2026-11-19 | RUL-36 | RUL-06.d |  |
| R12 | 2026-11-19 | RUL-40 | RUL-06.e |  |
| R12 | 2026-11-19 | RUL-62 | RUL-06.f |  |
| R12 | 2026-11-19 | RUL-41 | RUL-06.g |  |
| R12 | 2026-11-19 | RUL-19 | RUL-06.h |  |
| R12 | 2026-11-19 | RUL-20 | RUL-06.i |  |
| R12 | 2026-11-19 | RUL-21 | RUL-06.j |  |
| R12 | 2026-11-19 | RUL-31 | RUL-07.a |  |
| R12 | 2026-11-19 | RUL-32 | RUL-07.b |  |
| R12 | 2026-11-19 | RUL-33 | RUL-07.c |  |
| R12 | 2026-11-19 | RUL-54 | RUL-07.d |  |
| R12 | 2026-11-19 | RUL-59 | RUL-07.e |  |
| R12 | 2026-11-19 | RUL-60 | RUL-07.f |  |
| R12 | 2026-11-19 | RUL-34 | retired | merged or dropped |
| R12 | 2026-11-19 | RUL-35 | DEP-14 | merged or dropped |
| R13 | 2026-11-19 | HIS-01 | HIS-01.a |  |
| R13 | 2026-11-19 | HIS-27 | HIS-01.b |  |
| R13 | 2026-11-19 | HIS-03 | HIS-01.c |  |
| R13 | 2026-11-19 | HIS-04 | HIS-01.d |  |
| R13 | 2026-11-19 | HIS-05 | HIS-01.e |  |
| R13 | 2026-11-19 | HIS-15 | HIS-01.f |  |
| R13 | 2026-11-19 | HIS-21 | HIS-01.g |  |
| R13 | 2026-11-19 | HIS-33 | HIS-01.h |  |
| R13 | 2026-11-19 | HIS-10 | HIS-01.i |  |
| R13 | 2026-11-19 | HIS-02 | HIS-01.j |  |
| R13 | 2026-11-19 | HIS-08 | HIS-02.a |  |
| R13 | 2026-11-19 | HIS-24 | HIS-02.b |  |
| R13 | 2026-11-19 | HIS-23 | HIS-02.c |  |
| R13 | 2026-11-19 | HIS-06 | HIS-03.a |  |
| R13 | 2026-11-19 | HIS-07 | HIS-03.b |  |
| R13 | 2026-11-19 | HIS-20 | HIS-03.c |  |
| R13 | 2026-11-19 | HIS-09 | HIS-03.d |  |
| R13 | 2026-11-19 | HIS-32 | HIS-03.e |  |
| R13 | 2026-11-19 | HIS-19 | HIS-04.a |  |
| R13 | 2026-11-19 | HIS-34 | HIS-04.b |  |
| R14 | 2026-11-19 | GGL-05 | GGL-01.a |  |
| R14 | 2026-11-19 | GGL-06 | GGL-01.b |  |
| R14 | 2026-11-19 | GGL-07 | GGL-01.c |  |
| R14 | 2026-11-19 | GGL-08 | GGL-01.d |  |
| R14 | 2026-11-19 | GGL-13 | GGL-01.e |  |
| R14 | 2026-11-19 | GGL-12 | GGL-01.f |  |
| R14 | 2026-11-19 | GGL-37 | GGL-01.g |  |
| R14 | 2026-11-19 | GGL-45 | GGL-01.h |  |
| R14 | 2026-11-19 | GGL-46 | GGL-01.i |  |
| R14 | 2026-11-19 | GGL-47 | GGL-01.j |  |
| R14 | 2026-11-19 | GGL-110 | GGL-01.k |  |
| R14 | 2026-11-19 | GGL-113 | GGL-01.l |  |
| R14 | 2026-11-19 | GGL-91 | GGL-01.m |  |
| R14 | 2026-11-19 | GGL-95 | GGL-01.n |  |
| R14 | 2026-11-19 | GGL-09 | GGL-02.a |  |
| R14 | 2026-11-19 | GGL-10 | GGL-02.b |  |
| R14 | 2026-11-19 | GGL-14 | GGL-02.c |  |
| R14 | 2026-11-19 | GGL-20 | GGL-02.d |  |
| R14 | 2026-11-19 | GGL-21 | GGL-02.e |  |
| R14 | 2026-11-19 | GGL-22 | GGL-02.f |  |
| R14 | 2026-11-19 | GGL-61 | GGL-02.g |  |
| R14 | 2026-11-19 | GGL-62 | GGL-02.h |  |
| R14 | 2026-11-19 | GGL-63 | GGL-02.i |  |
| R14 | 2026-11-19 | GGL-64 | GGL-02.j |  |
| R14 | 2026-11-19 | GGL-65 | GGL-02.k |  |
| R14 | 2026-11-19 | GGL-67 | GGL-02.l |  |
| R14 | 2026-11-19 | GGL-76 | GGL-02.m |  |
| R14 | 2026-11-19 | GGL-77 | GGL-02.n |  |
| R14 | 2026-11-19 | GGL-93 | GGL-02.o |  |
| R14 | 2026-11-19 | GGL-104 | GGL-02.p |  |
| R14 | 2026-11-19 | GGL-107 | GGL-02.q |  |
| R14 | 2026-11-19 | GGL-11 | GGL-03.a |  |
| R14 | 2026-11-19 | GGL-17 | GGL-03.b |  |
| R14 | 2026-11-19 | GGL-18 | GGL-03.c |  |
| R14 | 2026-11-19 | GGL-19 | GGL-03.d |  |
| R14 | 2026-11-19 | GGL-50 | GGL-03.e |  |
| R14 | 2026-11-19 | GGL-58 | GGL-03.f |  |
| R14 | 2026-11-19 | GGL-69 | GGL-03.g |  |
| R14 | 2026-11-19 | GGL-100 | GGL-03.h |  |
| R14 | 2026-11-19 | GGL-30 | GGL-03.i |  |
| R14 | 2026-11-19 | GGL-103 | GGL-03.j |  |
| R14 | 2026-11-19 | GGL-96 | GGL-03.k |  |
| R14 | 2026-11-19 | GGL-49 | GGL-03.l |  |
| R14 | 2026-11-19 | GGL-23 | GGL-03.m |  |
| R14 | 2026-11-19 | GGL-85 | GGL-04.a |  |
| R14 | 2026-11-19 | GGL-26 | GGL-04.b |  |
| R14 | 2026-11-19 | GGL-24 | GGL-04.c |  |
| R14 | 2026-11-19 | GGL-25 | GGL-04.d |  |
| R14 | 2026-11-19 | GGL-27 | GGL-04.e |  |
| R14 | 2026-11-19 | GGL-60 | GGL-04.f |  |
| R14 | 2026-11-19 | GGL-70 | GGL-04.g |  |
| R14 | 2026-11-19 | GGL-73 | GGL-04.h |  |
| R14 | 2026-11-19 | GGL-29 | GGL-04.i |  |
| R14 | 2026-11-19 | GGL-28 | GGL-05.a |  |
| R14 | 2026-11-19 | GGL-31 | GGL-05.b |  |
| R14 | 2026-11-19 | GGL-32 | GGL-05.c |  |
| R14 | 2026-11-19 | GGL-33 | GGL-05.d |  |
| R14 | 2026-11-19 | GGL-34 | GGL-05.e |  |
| R14 | 2026-11-19 | GGL-35 | GGL-05.f |  |
| R14 | 2026-11-19 | GGL-52 | GGL-05.g |  |
| R14 | 2026-11-19 | GGL-53 | GGL-05.h |  |
| R14 | 2026-11-19 | GGL-54 | GGL-05.i |  |
| R14 | 2026-11-19 | GGL-55 | GGL-05.j |  |
| R14 | 2026-11-19 | GGL-56 | GGL-05.k |  |
| R14 | 2026-11-19 | GGL-59 | GGL-05.l |  |
| R14 | 2026-11-19 | GGL-66 | GGL-05.m |  |
| R14 | 2026-11-19 | GGL-99 | GGL-05.n |  |
| R14 | 2026-11-19 | GGL-101 | GGL-05.o |  |
| R14 | 2026-11-19 | GGL-38 | GGL-06.a |  |
| R14 | 2026-11-19 | GGL-40 | GGL-06.b |  |
| R14 | 2026-11-19 | GGL-41 | GGL-06.c |  |
| R14 | 2026-11-19 | GGL-42 | GGL-06.d |  |
| R14 | 2026-11-19 | GGL-43 | GGL-06.e |  |
| R14 | 2026-11-19 | GGL-44 | GGL-06.f |  |
| R14 | 2026-11-19 | GGL-36 | GGL-07.a |  |
| R14 | 2026-11-19 | GGL-57 | GGL-07.b |  |
| R14 | 2026-11-19 | GGL-68 | GGL-07.c |  |
| R14 | 2026-11-19 | GGL-74 | GGL-07.d |  |
| R14 | 2026-11-19 | GGL-78 | GGL-07.e |  |
| R14 | 2026-11-19 | GGL-79 | GGL-07.f |  |
| R14 | 2026-11-19 | GGL-80 | GGL-07.g |  |
| R14 | 2026-11-19 | GGL-81 | GGL-07.h |  |
| R14 | 2026-11-19 | GGL-82 | GGL-07.i |  |
| R14 | 2026-11-19 | GGL-83 | GGL-07.j |  |
| R14 | 2026-11-19 | GGL-89 | GGL-07.k |  |
| R14 | 2026-11-19 | GGL-106 | GGL-07.l |  |
| R14 | 2026-11-19 | GGL-51 | DEP-14 | merged or dropped |
| R15 | 2026-11-19 | SET-06 | SET-01.a |  |
| R15 | 2026-11-19 | SET-05 | SET-01.b |  |
| R15 | 2026-11-19 | SET-07 | SET-01.c |  |
| R15 | 2026-11-19 | SET-04 | SET-01.e |  |
| R15 | 2026-11-19 | SET-47 | SET-02.a |  |
| R15 | 2026-11-19 | SET-48 | SET-02.b |  |
| R15 | 2026-11-19 | SET-58 | SET-03.a |  |
| R15 | 2026-11-19 | SET-62 | SET-03.b |  |
| R15 | 2026-11-19 | SET-40 | SET-03.c |  |
| R15 | 2026-11-19 | SET-42 | SET-03.d |  |
| R15 | 2026-11-19 | SET-39 | SET-03.e |  |
| R15 | 2026-11-19 | SET-41 | SET-03.f |  |
| R15 | 2026-11-19 | SET-08 | SET-04.a |  |
| R15 | 2026-11-19 | SET-09 | SET-04.b |  |
| R15 | 2026-11-19 | SET-10 | SET-04.c |  |
| R15 | 2026-11-19 | SET-11 | SET-04.d |  |
| R15 | 2026-11-19 | SET-12 | SET-04.e |  |
| R15 | 2026-11-19 | SET-13 | SET-04.f |  |
| R15 | 2026-11-19 | SET-14 | SET-04.g |  |
| R15 | 2026-11-19 | SET-35 | SET-04.h |  |
| R15 | 2026-11-19 | SET-38 | SET-04.i |  |
| R15 | 2026-11-19 | SET-43 | SET-04.j |  |
| R15 | 2026-11-19 | SET-45 | SET-04.k |  |
| R15 | 2026-11-19 | SET-17 | SET-05.a |  |
| R15 | 2026-11-19 | SET-18 | SET-05.b |  |
| R15 | 2026-11-19 | SET-19 | SET-05.c |  |
| R15 | 2026-11-19 | SET-20 | SET-05.d |  |
| R15 | 2026-11-19 | SET-21 | SET-05.e |  |
| R15 | 2026-11-19 | SET-23 | SET-05.f |  |
| R15 | 2026-11-19 | SET-25 | SET-05.g |  |
| R15 | 2026-11-19 | SET-26 | SET-05.h |  |
| R15 | 2026-11-19 | SET-27 | SET-05.i |  |
| R15 | 2026-11-19 | SET-28 | SET-05.j |  |
| R15 | 2026-11-19 | SET-29 | SET-05.k |  |
| R15 | 2026-11-19 | SET-31 | SET-05.l |  |
| R15 | 2026-11-19 | SET-36 | SET-05.m |  |
| R15 | 2026-11-19 | SET-37 | SET-05.n |  |
| R15 | 2026-11-19 | SET-46 | SET-05.o |  |
| R15 | 2026-11-19 | SET-59 | SET-06.a |  |
| R15 | 2026-11-19 | SET-60 | SET-06.b |  |
| R15 | 2026-11-19 | SET-61 | SET-06.c |  |
| R15 | 2026-11-19 | SET-15 | SET-06.d |  |
| R15 | 2026-11-19 | SET-01 | SET-07.a |  |
| R15 | 2026-11-19 | SET-02 | SET-07.b |  |
| R15 | 2026-11-19 | SET-03 | SET-07.c |  |
| R16 | 2026-11-19 | SHL-16 | SHL-01.a |  |
| R16 | 2026-11-19 | SHL-02 | SHL-01.b |  |
| R16 | 2026-11-19 | SHL-03 | SHL-01.c |  |
| R16 | 2026-11-19 | SHL-04 | SHL-02.a |  |
| R16 | 2026-11-19 | SHL-24 | SHL-02.b |  |
| R16 | 2026-11-19 | SHL-25 | SHL-02.c |  |
| R16 | 2026-11-19 | SHL-23 | SHL-02.d |  |
| R16 | 2026-11-19 | SHL-08 | SHL-02.e |  |
| R16 | 2026-11-19 | SHL-09 | SHL-02.f |  |
| R16 | 2026-11-19 | SHL-07 | SHL-02.g |  |
| R16 | 2026-11-19 | SHL-26 | SHL-02.h |  |
| R16 | 2026-11-19 | SHL-19 | SHL-03.a |  |
| R16 | 2026-11-19 | SHL-01 | SHL-03.b |  |
| R16 | 2026-11-19 | SHL-18 | SHL-04.a |  |
| R16 | 2026-11-19 | SHL-27 | SHL-04.b |  |
| R16 | 2026-11-19 | SHL-20 | SHL-05.a |  |
| R16 | 2026-11-19 | SHL-14 | SHL-05.b |  |
| R16 | 2026-11-19 | SHL-15 | SHL-05.c |  |
| R16 | 2026-11-19 | SHL-10 | SHL-05.d |  |
| R17 | 2026-11-19 | EVT-04 | EVT-01.a |  |
| R17 | 2026-11-19 | EVT-05 | EVT-01.b |  |
| R17 | 2026-11-19 | EVT-06 | EVT-01.c |  |
| R17 | 2026-11-19 | EVT-08 | EVT-01.d |  |
| R17 | 2026-11-19 | EVT-21 | EVT-01.e |  |
| R17 | 2026-11-19 | EVT-22 | EVT-01.f |  |
| R17 | 2026-11-19 | EVT-24 | EVT-01.g |  |
| R17 | 2026-11-19 | EVT-07 | EVT-01.h |  |
| R17 | 2026-11-19 | EVT-10 | EVT-02.a |  |
| R17 | 2026-11-19 | EVT-11 | EVT-02.b |  |
| R17 | 2026-11-19 | EVT-12 | EVT-02.c |  |
| R17 | 2026-11-19 | EVT-13 | EVT-02.d |  |
| R17 | 2026-11-19 | EVT-14 | EVT-02.e |  |
| R17 | 2026-11-19 | EVT-15 | EVT-03.a |  |
| R17 | 2026-11-19 | EVT-16 | EVT-03.b |  |
| R17 | 2026-11-19 | EVT-17 | EVT-03.c |  |
| R17 | 2026-11-19 | EVT-18 | EVT-03.d |  |
| R17 | 2026-11-19 | EVT-19 | EVT-03.e |  |
| R17 | 2026-11-19 | EVT-33 | EVT-03.f |  |
| R17 | 2026-11-19 | EVT-48 | EVT-03.g |  |
| R17 | 2026-11-19 | EVT-41 | EVT-03.h |  |
| R17 | 2026-11-19 | EVT-20 | EVT-04.a |  |
| R17 | 2026-11-19 | EVT-23 | EVT-04.b |  |
| R17 | 2026-11-19 | EVT-42 | EVT-04.c |  |
| R17 | 2026-11-19 | EVT-43 | EVT-04.d |  |
| R17 | 2026-11-19 | EVT-44 | EVT-04.e |  |
| R17 | 2026-11-19 | EVT-27 | EVT-05.a |  |
| R17 | 2026-11-19 | EVT-29 | EVT-05.b |  |
| R17 | 2026-11-19 | EVT-30 | EVT-05.c |  |
| R17 | 2026-11-19 | EVT-31 | EVT-05.d |  |
| R17 | 2026-11-19 | EVT-38 | EVT-05.e |  |
| R17 | 2026-11-19 | EVT-39 | EVT-05.f |  |
| R17 | 2026-11-19 | EVT-32 | EVT-05.g |  |
| R17 | 2026-11-19 | EVT-47 | EVT-05.h |  |
| R17 | 2026-11-19 | EVT-01 | EVT-06.a |  |
| R17 | 2026-11-19 | EVT-02 | EVT-06.b |  |
| R17 | 2026-11-19 | EVT-03 | EVT-06.c |  |
| R18 | 2026-11-19 | SRH-01 | SRH-01.a |  |
| R18 | 2026-11-19 | SRH-07 | SRH-01.b |  |
| R18 | 2026-11-19 | SRH-06 | SRH-01.c |  |
| R18 | 2026-11-19 | SRH-02 | SRH-01.d |  |
| R18 | 2026-11-19 | SRH-03 | SRH-01.e |  |
| R18 | 2026-11-19 | SRH-04 | SRH-01.f |  |
| R18 | 2026-11-19 | SRH-05 | SRH-01.g |  |
| R18 | 2026-11-19 | SRH-08 | SRH-02.a |  |
| R18 | 2026-11-19 | SRH-09 | SRH-02.b |  |
| R19 | 2026-11-19 | TPL-01 | TPL-01.a |  |
| R19 | 2026-11-19 | TPL-02 | TPL-01.b |  |
| R19 | 2026-11-19 | TPL-03 | TPL-01.c |  |
| R19 | 2026-11-19 | TPL-04 | TPL-02.a |  |
| R19 | 2026-11-19 | TPL-05 | TPL-02.b |  |
| R19 | 2026-11-19 | TPL-07 | TPL-02.c |  |
| R20 | 2026-11-19 | FLT-01 | FLT-01.a |  |
| R20 | 2026-11-19 | FLT-02 | FLT-01.b |  |
| R20 | 2026-11-19 | FLT-03 | FLT-01.c |  |
| R20 | 2026-11-19 | FLT-04 | FLT-01.d |  |
| R20 | 2026-11-19 | FLT-05 | FLT-01.e |  |
| R21 | 2026-11-19 | DOC-01 | DOC-01.a |  |
| R21 | 2026-11-19 | DOC-02 | DOC-01.b |  |
| R21 | 2026-11-19 | DOC-06 | DOC-01.c |  |
| R21 | 2026-11-19 | DOC-05 | DOC-01.d |  |
| R21 | 2026-11-19 | DOC-03 | DOC-02.a |  |
| R21 | 2026-11-19 | DOC-04 | DOC-02.b |  |
| R21 | 2026-11-19 | DOC-07 | DOC-03.a |  |
| R21 | 2026-11-19 | DOC-08 | DOC-03.b |  |
| R21 | 2026-11-19 | DOC-10 | DOC-03.c |  |
