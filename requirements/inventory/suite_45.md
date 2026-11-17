# Suite 45: Two-way Google sync and remote deletions

Source: [`tests/suite_45.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient at a synthetic HTTPS host; mock Google on 8114; Demo.ics and local fixture events. Loops and sync-window start patched. Full syncs follow direct mock event/timestamp mutations; a changed_at override forces the newer-local branch. No real Google or CCS+ write.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S45-01 | google | Mock consent leaves the Google account connected. | [L47](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L47) |
| S45-02 | google | The initial full sync returns success. | [L53](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L53) |
| S45-03 | google | At least ten eligible timed CCS+ fixture events have corresponding Google records. | [L66](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L66) |
| S45-04 | google | The full sync after a remote edit returns success. | [L72](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L72) |
| S45-05 | google | The remote title change appears in local stored edits and its remote location appears in the local event. | [L73](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L73) |
| S45-06 | google | The sampled United-original event title remains equal to its prior original title. | [L75](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L75) |
| S45-07 | google | The edited remote record keeps the changed title and confirmed status. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L76) |
| S45-08 | history | A sampled recent log reports that the Google change was saved locally. | [L77](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L77) |
| S45-09 | google | Editing the custom Dentist remotely changes its local title and start instant. | [L85](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L85) |
| S45-10 | google | A remote handmade event becomes exactly one custom local event with its fixture location. | [L92](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L92) |
| S45-11 | google | The handmade remote ID is cancelled and CalendarStream's mapped replacement is confirmed. | [L93](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L93) |
| S45-12 | google | A remote deletion marks the imported local event hidden and leaves the remote record cancelled. | [L100](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L100) |
| S45-13 | google | The generated rule event has a corresponding remote record. | [L104](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L104) |
| S45-14 | google | A remote edit of the rule event is replaced by the rule title both locally and remotely. | [L107](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L107) |
| S45-15 | google | A remote deletion of the rule event is restored to confirmed. | [L110](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L110) |
| S45-16 | google | With local change time patched newer, local and remote titles both keep the local title. | [L120](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L120) |
| S45-17 | history | Recent logs report that the newer local change was kept. | [L121](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L121) |
| S45-18 | google | With a remote timestamp in 2099, the local event title becomes the remote title. | [L127](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L127) |
| S45-19 | google | Four remote deletions each hide the corresponding local event with a google-prefixed deletion marker. | [L135](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L135) |
| S45-20 | history | A recent log has a Deleted in Google Calendar message and Google kind. | [L137](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L137) |
| S45-21 | calendar | The page includes Deleted in Google Calendar text and an event-restore form action. | [L139](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L139) |
| S45-22 | google | Restoring one deleted event clears its local hidden/deleted flags and confirms its remote record. | [L141](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L141) |
| S45-23 | google | The other three remote records remain cancelled. | [L143](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L143) |
| S45-24 | calendar | The sampled custom event markup has tint class and its calendar's expected color variable. | [L149](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L149) |
| S45-25 | calendar | The sampled legend substring omits Added here color wording. | [L150](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L150) |
| S45-26 | rules | The page renders the titled rule's Change to all-day summary. | [L154](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L154) |
| S45-27 | events | The link-mode embedded editor contains its link box and Cancel pair markup. | [L157](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_45.py#L157) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Remote title/location/start, originals and timestamps are sampled fixture values. Row 06 proves the original title unchanged, not every original field or a live upstream system write prohibition.
- Row 20 asserts at least one matching History line, not exactly one. Row 21 checks origin text/Restore markup, not strike-through styling (suite 44 checks that separately).
- Row 27 checks link-box/pair markup, not focus/scroll positioning or a newly saved link. The old docstring's held-deletion behavior is obsolete; rows 19–23 expect immediate markers/restoration.
- Overlaps: suites 13/20 sync; suite 49 one-way/multi-account deletions; suite 36 reminders/rule-event behavior.
