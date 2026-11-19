# Requirements: history

Statuses: verified, built, open, planned (approved, not built yet) and proposed (drafted, not yet reviewed by the Developer).

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| HIS-01 | proposed | History records what changes in the app and what happens with Google, so the user can see what happened and why. | — | — |
| HIS-01.a | proposed | Activity records calendar changes, identifying the changed calendar. | — | S33-13 |
| HIS-01.b | proposed | A synchronization that changes events records in its activity summary how many events it added and how many it updated. | — | changelog_gaps_2101-2336:19, changelog_gaps_2101-2336:19 |
| HIS-01.c | proposed | When a Google change is saved locally, History records that outcome; when a newer local change wins, it records that the local change was kept. | — | S45-08, S45-17 |
| HIS-01.d | proposed | A deletion received from Google is recorded with its Google origin. | — | S45-20 |
| HIS-01.e | proposed | If a former Google client’s calendar cannot be reached for cleanup, History warns that manual deletion is needed. | — | S48-22 |
| HIS-01.f | proposed | A Google color-update failure records the failed operation, the upstream status and its reasons so the refusal can be diagnosed (CON-04). | — | S55-12, S56-20 |
| HIS-01.g | proposed | An unsigned Google module produces one not-signed-in or unsynced warning (HIS-01); resetting the remembered warning permits a new one. | — | S68-03, S68-04, S68-05 |
| HIS-01.h | proposed | A failure or warning that repeats unchanged is recorded in History once, until it changes or clears. | — | CON-07, CON-06, CON-07, HIS-21 |
| HIS-01.i | proposed | An external removal or Google notification without an undoable local change does not become the current Undo entry. | — | S49-18, S49-41 |
| HIS-01.j | proposed (?) | Activity reports Healthy when its source is healthy and Unhealthy when its source is in error. How should mixed source states determine the overall Activity status? | — | S36-43, S36-44 |
| HIS-02 | proposed | History lists its entries with their type, in a table the user can filter and rearrange. | — | — |
| HIS-02.a | proposed | History names the type of each change: Calendar, Rule, Event, Sync, Feed, Google, Settings or Update. | — | S49-13, changelog_gaps_601-900:31 |
| HIS-02.b | proposed | History has a filter that follows the common filter rules (UI-21), with three parts: the change type (the types in HIS-02), words in its entries, and the time of its entries. | — | readme_gaps:71, changelog_gaps_601-900:31 |
| HIS-02.c | proposed | The user can choose the order of History's columns by sliding a header, or with the left and right arrows when a header is focused; Undo starts at the end. | — | readme_gaps:71, changelog_gaps_1-300:27 |
| HIS-02.d |  | History is a table: Time \| Type \| Event \| Undo; folded it shows the latest lines with Undo and Redo where they apply, newest first (a stack). | — | theme.md section 15; picture 2·15 |
| HIS-02.e |  | Something done outside CalendarStream (deleted in Google, removed by United) has no Undo icon; Restore is on the event. | — | theme.md section 15 |
| HIS-02.f |  | An accepted sign-in is shown as a ✓ with no words; the word stays as its tooltip and accessible name. | — | theme.md Clarifications |
| HIS-02.g |  | History's three latest lines sit left-aligned in its section header, before its Healthy box. | — | theme.md Clarifications |
| HIS-03 | proposed | The user can undo and redo what History records. | — | — |
| HIS-03.a | proposed | Only the newest completed undoable change can be undone. | — | S49-10 |
| HIS-03.b | proposed | Undo restores the state before any undoable change and Redo reapplies it (HIS-03), in the order HIS-03 sets. This covers rule deletions; feed and event-template changes; an import (the event set before it); a calendar merge (the original calendar and its rule scope, with the merged events removed from the target); CCS+ removal (the source and its saved credentials); and Hide (the event's visible state, EVT-04). | — | S49-11, S49-12, S49-25, S49-30, S49-34, S57-15, changelog_gaps_601-900:32, changelog_gaps_601-900:32 |
| HIS-03.c | proposed | An undoable change records what is needed to restore it, before and after. | — | S77-32, S77-33 |
| HIS-03.d | proposed | A deleted event kept for Undo is permanently removed when its deletion leaves the retained history. | — | S49-16 |
| HIS-03.e | proposed | When removal of a CCS+ calendar leaves retained Undo history, its retained sign-in credentials are forgotten; protection while retained follows ACC-05. | — | changelog_gaps_601-900:33 |
| HIS-04 | proposed | History keeps a limited number of changes and does not show secrets unless the user may see them. | — | — |
| HIS-04.a | proposed | History keeps the number of changes set in Settings (DEF-01 has the default and the limits); saving a different number updates the effective retention and the displayed value, and a number outside the limits is not valid (UI-19). | — | S58-19, S58-20 |
| HIS-04.b | proposed | History has a Show secrets switch for every log view on the page. By default secrets are masked: authorization headers, client secrets, tokens, authorization codes, and any secret value the app stores, wherever it appears in the text. Turning the switch on shows them, only to a user authorized to see secrets, and it turns off again whenever the page is opened (ACC-05.d). | — | Developer, Nov 18 |

