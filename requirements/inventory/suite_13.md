# Suite 13: Google event synchronization

Source: [`tests/suite_13.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; mock Google on 8113; synthetic `tests/data/Demo.ics`. Source and Google background loops are patched. The test explicitly sets the Google destination start date to the sync-window start. Despite the old docstring saying real CCS+ file, the input is Demo.ics.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S13-01 | sources | The count of free United-origin events equals the Demo.ics TRANSP:TRANSPARENT count. | [L63](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L63) |
| S13-02 | google | connecting asks for a full sync | [L68](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L68) |
| S13-03 | google | Initial full sync succeeds and Google contains the expected number of nonhidden events in the window. | [L72](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L72) |
| S13-04 | google | Initial sync writes one POST per expected event and no other write method. | [L73](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L73) |
| S13-05 | google | The latest activity log reports the initial number of Google events added. | [L74](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L74) |
| S13-06 | google | Google summary matches the source title and description ends with Synced by CalendarStream. | [L76](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L76) |
| S13-07 | google | Uploaded Google events disable default reminders and have no reminder overrides. | [L77](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L77) |
| S13-08 | google | An all-day event uses a date-only Google start value matching its source date. | [L79](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L79) |
| S13-09 | google | A timed event has America/New_York as its Google start time zone. | [L80](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L80) |
| S13-10 | google | free/busy carried over | [L81](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L81) |
| S13-11 | google | Without color rules, uploaded events omit colorId. | [L83](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L83) |
| S13-12 | google | second sync: nothing written | [L86](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L86) |
| S13-13 | google | full check with nothing changed: nothing written | [L88](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L88) |
| S13-14 | google | an edit wakes the Google sync | [L96](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L96) |
| S13-15 | google | Editing one event produces one PUT write (exact target OR one PUT of any target). | [L98](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L98) |
| S13-16 | google | edited title in Google | [L100](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L100) |
| S13-17 | google | hidden event removed | [L106](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L106) |
| S13-18 | google | Adding a timed local event makes one Google write and persists its start time and busy transparency. | [L111](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L111) |
| S13-19 | google | A matching color rule produces colored Google events and all colored events have Tomato ID 11. | [L123](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L123) |
| S13-20 | google | calendar renamed in Google | [L124](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L124) |
| S13-21 | google | The latest activity log reports the calendar rename. | [L125](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L125) |
| S13-22 | google | Nearest-color lookup maps the sampled green and blue hex values to Google IDs 2 and 7. | [L126](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L126) |
| S13-23 | google | normal sync doesn't look at Google's copy | [L139](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L139) |
| S13-24 | google | A full check preserves the remote deletion and edited title in Google; see limitation below. | [L141](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L141) |
| S13-25 | google | removes CalendarStream's strays, keeps events made by hand (no CalendarStream calendar to put them in) | [L142](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L142) |
| S13-26 | google | Logs report removal, deletion in Google Calendar and an event changed in Google. | [L143](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L143) |
| S13-27 | google | month rollover: past events left alone in Google | [L151](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L151) |
| S13-28 | google | After moving the start to November, every retained sync row ends on or after November 1. | [L152](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L152) |
| S13-29 | google | Moving the start back accepts the expected write count OR only POST/PUT methods; see limitation below. | [L154](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L154) |
| S13-30 | google | The next unchanged full check produces no writes. | [L157](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L157) |
| S13-31 | google | A deleted Google calendar is recreated under a new ID and filled with the expected eligible CCS+ event count. | [L166](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L166) |
| S13-32 | google | The latest activity log says a new calendar was made. | [L168](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L168) |
| S13-33 | google | menu and status line show the sync | [L172](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L172) |
| S13-34 | google | Sync now asks for a full check | [L174](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L174) |
| S13-35 | google | Two revoked-access sync attempts fail but add only one recent activity log entry. | [L181](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L181) |
| S13-36 | google | revoked: shown in the menu and status line | [L183](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L183) |
| S13-37 | google | disconnect + delete forgets what was synced | [L187](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L187) |

## Direct assertions

- [L50](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_13.py#L50): `r.status_code == 303` — setup/connection redirect guard; a failed prerequisite stops the subsequent checks.

## Coverage limits and reconciliation notes

- Row 24 asserts the remote deletion/title, not local hidden/edit fields. Its label claims local propagation; suite 20 row 12 directly checks a local title update. Keep that distinction when deriving requirements.
- Row 29 uses an OR: a matching write count is sufficient regardless of methods, or all writes may be POST/PUT regardless of count. `all()` also passes on an empty list. This is weaker than exact re-tracking coverage.
- Row 15 allows any single PUT as its fallback; it does not always prove the exact target URL.
- Row 19 only examines colored events; it does not independently prove every matching event received a color.
- Synthetic input is Demo.ics, despite the historical docstring and variable name REAL. No live Google account or CCS+ service is involved.
- Overlaps: suite 12 connection and token lifecycle; suite 19 color precedence; suite 20 two-way notification handling.
