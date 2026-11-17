# Suite 49: Rules, History, source import/removal and accounts

Source: [`tests/suite_49.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8121; Demo.ics and date-relative synthetic events/ICS. Loops patched. The externally removed event scenario requires a future Demo.ics event; the harness fixed clock matters. Chromium requests to cs.test are fulfilled through the authenticated TestClient for regex highlighting, without a second app server.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S49-01 | sources | Initial sources start with a local source and there is exactly one local source. | [L47](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L47) |
| S49-02 | sources | Moving CCS+ before Local returns 200 while default_sid remains Local. | [L50](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L50) |
| S49-03 | sources | The page has the last-local data-empty marker and omits Empty this calendar wording. | [L53](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L53) |
| S49-04 | rules | The pattern *E#### matches Trip E1234 and lowercase e9999 but not E12345. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L61) |
| S49-05 | rules | Testing that pattern as regex reports the sampled nothing-to-repeat error. | [L63](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L63) |
| S49-06 | rules | Testing the valid regex matches Trip E1234 but not RDO and reports span 5–10. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L65) |
| S49-07 | rules | Saving the malformed regex returns 400 with a Not a valid regex detail. | [L68](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L68) |
| S49-08 | rules | Two emoji actions both prefix the sampled event title in order. | [L72](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L72) |
| S49-09 | rules | An Any text condition matching the fixture location applies the sampled gold color. | [L75](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L75) |
| S49-10 | history | Trying to undo an older completed entry returns 400. | [L82](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L82) |
| S49-11 | history | Undoing the newest rule deletion returns 200 and restores the prior rule count. | [L83](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L83) |
| S49-12 | history | Redo points at that same entry, returns 200 and removes the rule again. | [L85](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L85) |
| S49-13 | history | The latest log entry kind belongs to the sampled allowed type set. | [L86](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L86) |
| S49-14 | events | A deleted custom event UID is absent from its calendar page while the stored event retains its deletion marker. | [L92](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L92) |
| S49-15 | events | Restoring it clears the deletion marker. | [L95](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L95) |
| S49-16 | history | With retention set to one and two newer changes, the deleted event is removed from storage and page. | [L100](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L100) |
| S49-17 | sources | If a future fixture event is removed from the uploaded feed, a retained United-deletion event exists with its title. | [L111](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L111) |
| S49-18 | history | The sampled external-removal history line has blank state and is not the current undo-stack entry. | [L114](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L114) |
| S49-19 | events | Restoring that externally removed event clears its deletion marker and gives it custom origin. | [L116](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L116) |
| S49-20 | sources | Failure sentinel: if the demo contains no future removable event, the suite prints a failing check. | [L119](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L119) |
| S49-21 | sources | Importing the two-event fixture with a 30-day end bound returns 200 with total one and no conflicts. | [L128](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L128) |
| S49-22 | sources | Finishing that import creates one custom Dentist event. | [L131](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L131) |
| S49-23 | sources | Reimporting with no date limits reports total two and one conflict for Dentist moved. | [L134](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L134) |
| S49-24 | sources | Choosing merge yields exactly the sampled moved-Dentist and Far-away titles. | [L137](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L137) |
| S49-25 | history | Undoing the import restores the filtered title set to Dentist only. | [L140](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L140) |
| S49-26 | sources | Export returns 200, includes Lunch in ICS and sets attachment disposition. | [L149](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L149) |
| S49-27 | sources | The second calendar's remove markup records one owned rule. | [L151](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L151) |
| S49-28 | sources | Merging the second local calendar removes its ID and places Lunch in the target. | [L153](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L153) |
| S49-29 | rules | Its owned rule scope changes to the merge target. | [L154](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L154) |
| S49-30 | history | Undo restores the source ID/rule scope and removes merged Lunch from the target. | [L157](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L157) |
| S49-31 | sources | Deleting the second calendar removes its source ID and owned rule ID. | [L160](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L160) |
| S49-32 | sources | Deleting the last Local keeps its ID first and leaves no customs in it. | [L163](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L163) |
| S49-33 | sources | Removing CCS+ removes its source ID and active stored login. | [L167](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L167) |
| S49-34 | history | Undo restores CCS+ and retrieves the fixture username. | [L170](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L170) |
| S49-35 | calendar | Searching without date bounds finds the fixture event 700 days ahead. | [L176](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L176) |
| S49-36 | google | The first mock Google account connects. | [L185](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L185) |
| S49-37 | google | New one-way and two-way destinations have the respective oneway flags. | [L189](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L189) |
| S49-38 | google | The full sync returns success after assigning the two destinations to the first account. | [L194](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L194) |
| S49-39 | google | The two-way remote calendar background color equals the chosen module color. | [L196](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L196) |
| S49-40 | google | A two-way remote deletion gives the local event a google marker and the page origin text. | [L205](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L205) |
| S49-41 | history | Its Google history line has blank state and is not the current undo entry. | [L207](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L207) |
| S49-42 | google | A different one-way remote-deleted event is restored to confirmed. | [L208](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L208) |
| S49-43 | google | Connecting a second fixture account to one module sets that account/email while retaining the first account's email. | [L215](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L215) |
| S49-44 | google | That module's new remote calendar is owned by the second fixture account. | [L218](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L218) |
| S49-45 | google | The page includes the second email and one-way/two-way module labels. | [L220](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L220) |
| S49-46 | google | Removing the two-way module with delete removes its remote calendar. | [L224](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L224) |
| S49-47 | account | An unauthenticated HTML page request redirects 303 to a login URL. | [L230](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L230) |
| S49-48 | account | Submitting a wrong fixture password to login returns 400. | [L232](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L232) |
| S49-49 | account | Successful login with a protocol-relative external next returns 303 to root and sets a session cookie. | [L234](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L234) |
| S49-50 | account | The hidden-tab redirect sample is reduced to root while the sampled local query/fragment is preserved. | [L235](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L235) |
| S49-51 | account | The new session can load the page with HTTP 200. | [L236](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L236) |
| S49-52 | account | After logout, an HTML root request again redirects 303. | [L238](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L238) |
| S49-53 | account | Authenticated HTTP Basic still permits the status API with 200. | [L239](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L239) |
| S49-54 | history | The container-log endpoint returns 200 with text/plain content type. | [L241](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L241) |
| S49-55 | history | The page contains the copycontainerlog control ID. | [L242](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L242) |
| S49-56 | rules | The regex test UI highlights exactly RDO in a sample prefixed by an airplane emoji. | [L262](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L262) |
| S49-57 | shell | No browser pageerror events are collected during that regex interaction. | [L263](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_49.py#L263) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Uses date.today() for fixtures but Demo.ics has fixed dates; rows 17–19 depend on a future event branch and row 20 is a failure sentinel if none exists. Use the harness fixed clock before claiming execution coverage.
- Row 09 tests location matching, not notes independently. Row 13 samples the latest log Type only, not every line. Rows 17/40 inspect stored markers/text rather than strike-through styles.
- Row 30 asserts restored source/rule and absence of merged Lunch at target but not every event field. Row 31 checks source/rule absence, not a direct event-row count. Row 34 retrieves the restored login but does not inspect encryption of the intermediate Undo snapshot.
- Row 35 proves a sampled 700-day future search, not literally every date. Row 41 checks blank history state/current stack inequality, not icon DOM.
- Login redirect tests cover specific protocol-relative/hidden-tab examples, not exhaustive URL schemes. Row 55 checks a control ID, not adjacency or clipboard operation.
- Browser routing uses an already authenticated client; that browser portion is not an anonymous-access test. No explicit viewport/palette matrix is configured there.
- Overlaps: suite 36 Local/reminders; suite 45 remote edits/deletions; suite 51 account isolation/invites; suite 16 login.
