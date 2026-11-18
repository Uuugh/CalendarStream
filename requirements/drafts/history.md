# DRAFT requirements: history (for the Developer's review)

Not approved. Derived from every inventory row whose candidate feature includes `history`, at
`3ddb4b76f8b23735af1bdfbf7a2687899e0c7578`. No `requirements/history.md` exists there, so IDs start
HIS-01. Evidence keys refer to `requirements/inventory/suite_NN.md`, including its pinned source,
setup and limitations. These are proposals for reconciliation, not runtime verification.

Undo effects are stated here; the underlying event, source and Google operations remain owned by
those features. Shared dialogs, section mechanics, confirmations and save feedback are referenced
rather than duplicated. No permanent approval or Developer Good status is assigned.

| ID | status | statement | evidence |
|---|---|---|---|
| HIS-01 | proposed | Activity records calendar changes, identifying the changed calendar. | S33-13 |
| HIS-02 | proposed (?) | Activity reports Healthy when the checked source state is healthy and Unhealthy when that source is in error. How should mixed source states determine the overall Activity status? | S36-43, S36-44 |
| HIS-03 | proposed | When a Google change is saved locally, History records that outcome; when a newer local change wins, it records that the local change was kept. | S45-08, S45-17 |
| HIS-04 | proposed | A deletion received from Google is recorded with its Google origin. | S45-20 |
| HIS-05 | proposed | If a former Google client’s calendar cannot be reached for cleanup, History warns that manual deletion is needed. | S48-22 |
| HIS-06 | proposed | Only the newest completed undoable change can be undone; trying to undo an older completed entry is refused. | S49-10 |
| HIS-07 | proposed | Undo restores the state before a rule deletion, and Redo reapplies that same deletion. | S49-11, S49-12 |
| HIS-08 | proposed (?) | History identifies the change type, including Rule, Event, Calendar or Sync in the checked cases. Is this a closed list or may other types be displayed? | S49-13 |
| HIS-09 | proposed | A deleted event kept for Undo is permanently removed when its deletion leaves the retained history. | S49-16 |
| HIS-10 | proposed | An external removal or Google notification without an undoable local change does not become the current Undo entry. | S49-18, S49-41 |
| HIS-11 | proposed | Undoing an import restores the event set that existed before the import. | S49-25 |
| HIS-12 | proposed | Undoing a calendar merge restores its original calendar and rule scope and removes the merged events from the target. | S49-30 |
| HIS-13 | proposed | Undoing CCS+ removal restores the source and its saved credentials. | S49-34 |
| HIS-14 | proposed | The container log can be retrieved as plain text. | S49-54 |
| HIS-15 | proposed | A Google color-update failure records the failed operation, upstream status and reasons so the refusal can be diagnosed. | S55-12, S56-20 |
| HIS-16 | proposed | Account recovery guidance in History tells the user to obtain the recovery link from the container log within 24 hours (ACC-21). Recovery-link validity belongs to account requirements. | S55-28 |
| HIS-17 | proposed | When a working Google color-update fallback is selected, History identifies the retained method; later successful updates use shorter color wording without repeating the method-selection notice. | S56-03, S56-05, S56-08, S56-11, S56-15 |
| HIS-18 | proposed | Undoing Hide restores the event’s visible state. Event Hide/Show behavior itself belongs to EVT-20. | S57-15 |
| HIS-19 | proposed (?) | History retains 100 changes by default, and saving a retention choice of 37 updates the effective retention and displayed value. The input offers bounds of 1 through 200; are these bounds enforced on every save path? | S58-19, S58-20 |
| HIS-20 | proposed (?) | Completing an undoable change records the before and after states for restoration. The oracle directly captures a change from one to two; what state categories must be included in every snapshot? | S77-32, S77-33 |
| HIS-21 | proposed | An unsigned Google module produces one not-signed-in/unsynced warning rather than repeating it on subsequent sync attempts. Resetting the remembered warning permits a new warning. | S68-03, S68-04, S68-05 |
| HIS-22 | proposed | Google setup messages distinguish API Sync being configured from modules being signed in, and identify the signed-out module. | S68-07, S68-08 |

## Not requirements

These rows remain accounted for without creating duplicate shared-UI or Python implementation requirements.

- S31-13: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S38-13: Shared section expansion behavior is owned by UI-05 in common.md.
- S38-14: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S49-55: Copy-control ID presence is implementation markup; the container-log retrieval outcome is specified above.
- S58-21: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S58-23: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S61-18: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S65-06: Deleted-event storage marker belongs to events (EVT-21); its retention consequence for Undo is specified above.
- S66-10: Permissive accepted-check/icon markup predicate does not independently establish a history behavior.
- S66-11: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S66-12: ok(True) skip marker when the History table is absent; not independent verification.
- S66-13: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S66-14: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S67-04: Template source-string check (keep=False), not an executed user behavior.
- S67-10: Shared save acknowledgement/shrink/dismiss mechanics; shared UI owns feedback timing, not a separate history rule. See the common.md pending save/cancel ownership note and SET-07; these references do not claim the exact timings are already specified.
- S67-11: Shared save acknowledgement/shrink/dismiss mechanics; shared UI owns feedback timing, not a separate history rule. See the common.md pending save/cancel ownership note and SET-07; these references do not claim the exact timings are already specified.
- S67-12: Shared save acknowledgement/shrink/dismiss mechanics; shared UI owns feedback timing, not a separate history rule. See the common.md pending save/cancel ownership note and SET-07; these references do not claim the exact timings are already specified.
- S77-31: Injected record return value is a Python collaborator contract, not a user requirement.
- S77-34: Injected trimming callback count is an implementation contract; it does not independently prove a user-visible retention limit.

## Coverage and open questions

All 55 history-candidate rows are accounted for in 22 proposed requirements and
19 excluded/shared-owner mappings. Open questions above cover aggregate health, type vocabulary,
retention validation and snapshot scope; no broader guarantees are inferred from finite examples.
No application suites were run locally for this documentation-only draft.
