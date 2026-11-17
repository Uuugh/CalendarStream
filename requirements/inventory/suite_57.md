# Suite 57: Event editor layout, hide/show and nested dialogs

Source: [`tests/suite_57.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8157; seed.demo; fake work.ics download; patched loops. A synthetic fixed UID identifies the imported event. Chromium 1400×900 later changes to 390×844; both pageerror and console-error events are collected. Notes growth is simulated via style assignment.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S57-01 | events | New-event header has Back, Add event and template picker/fixture title, without print or copy controls. | [L39](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L39) |
| S57-02 | events | The page omits the old template-field ID and Start from a template wording. | [L42](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L42) |
| S57-03 | events | Required-label markup names exactly title, start/end dates and start/end times. | [L44](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L44) |
| S57-04 | events | The sampled field IDs appear in the asserted order from Title/Location/source/color through dates/times/zones/Notes/link box. | [L45](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L45) |
| S57-05 | events | New-event link markup includes active Event/Rule choices, Remove, hidden link panel and no old link button. | [L50](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L50) |
| S57-06 | events | The new editor omits Delete/Hide controls and hidden-field markup. | [L53](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L53) |
| S57-07 | events | Saved imported-event header includes its day-specific print link/date and duplicate UID, without a template picker. | [L57](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L57) |
| S57-08 | events | The imported-event footer has Hide confirmation and info text before its button pair, without Delete. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L61) |
| S57-09 | events | The editor omits the old hidden field and Hide from Google Calendar wording. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L65) |
| S57-10 | events | Posting Hide returns 200 or 303, sets hidden and records the exact sampled History line. | [L69](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L69) |
| S57-11 | events | Hidden-event markup shows Show with show=1 and no adjacent ask attribute. | [L72](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L72) |
| S57-12 | events | Saving a renamed hidden event preserves its hidden state. | [L77](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L77) |
| S57-13 | events | Show clears hidden while preserving the edited title and recording Showed text. | [L80](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L80) |
| S57-14 | events | Hide then Show on an unedited event leaves no edit record. | [L83](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L83) |
| S57-15 | history | Undoing the latest Hide unhides the stored event. | [L87](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L87) |
| S57-16 | events | Hiding an unknown UID returns 404. | [L88](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L88) |
| S57-17 | events | A custom-event footer has Delete with confirmation and no Hide. | [L96](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L96) |
| S57-18 | events | A saved linked event renders its active Event segment, visible link panel and target UID. | [L99](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L99) |
| S57-19 | events | The link-mode add editor has the pick-now attribute. | [L102](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L102) |
| S57-20 | events | The outer dialog header is hidden while the embedded Add event title and Back are visible. | [L114](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L114) |
| S57-21 | events | Notes lies beside/aligned with Title, extends to the zone row, has at least ten sampled lines of height and sits above the link box. | [L121](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L121) |
| S57-22 | events | The template picker right edge aligns with the embedded header right edge. | [L122](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L122) |
| S57-23 | events | The dialog fits under viewport height minus 48px and iframe height matches embedded main within 1px. | [L123](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L123) |
| S57-24 | events | Setting Notes height to 520px increases the iframe height by over 100px. | [L126](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L126) |
| S57-25 | event_templates | Choosing the airport template fills the sampled title/location/end time and hides the template menu. | [L129](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L129) |
| S57-26 | events | Choosing Event linking opens the picker with over five event buttons. | [L133](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L133) |
| S57-27 | events | Removing the picked link hides its panel, clears target UID and leaves no active link-kind segment. | [L136](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L136) |
| S57-28 | events | Back closes the event dialog. | [L139](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L139) |
| S57-29 | events | Escape from the time list hides only the list and leaves the event dialog open. | [L142](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L142) |
| S57-30 | events | A second Escape closes the event dialog. | [L144](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L144) |
| S57-31 | events | Removing a link then cancelling the editor preserves its stored original target. | [L148](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L148) |
| S57-32 | calendar | Print from the imported event opens day preview for its date while the event dialog remains open behind. | [L154](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L154) |
| S57-33 | events | Clicking Hide opens a confirmation with the expected question prefix. | [L158](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L158) |
| S57-34 | events | Confirming Hide sets the stored event hidden and closes the event dialog. | [L160](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L160) |
| S57-35 | events | The sampled Hide-info tooltip opens above its icon with aligned left edge. | [L164](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L164) |
| S57-36 | events | Clicking Show on the hidden event clears hidden. | [L166](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L166) |
| S57-37 | events | At phone width, Notes is below the date row, aligned with Title and Back is visible. | [L171](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L171) |
| S57-38 | shell | At phone width, document scroll width does not exceed innerWidth. | [L173](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L173) |
| S57-39 | calendar | Phone Print navigates to the event-date print query and opens Print Preview. | [L175](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L175) |
| S57-40 | shell | No pageerror or collected console-error events occur in the sampled browser paths. | [L176](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_57.py#L176) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Several early assertions inspect source ordering/classes/wording rather than browser positions or focus. Hide/show route checks inspect stored hidden state and logs, not all downstream feed bodies.
- Row 24 sets textarea height in JavaScript instead of physically dragging a resize handle. Row 27 clears unsaved link UI; row 31 separately proves Cancel retains the saved link. No positive persisted unlink save is asserted in that branch.
- Row 35 checks tooltip above/left alignment, not all popup bounds. Row 37 compares Notes to the start-date row only, not every field.
- Template fill samples title/location/end time. Browser waits are finite observations, not exact transition-time requirements.
- Overlaps: suites 36/46 editor; suite 58 link selection/info/Delete; suite 59 All-day layout.
