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
