# Suite 18: Source setup, feeds, rules and month interactions

Source: [`tests/suite_18.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTP server on 8097; Chromium/Playwright; Demo.ics. Download patched to AuthError; background loops patched. Browser uses 1100×900; clipboard permissions enabled for copy feedback.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S18-01 | sources | no CCS+ login: 'Setup needed', not an error | [L30](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L30) |
| S18-02 | sources | no error logged for a missing login | [L31](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L31) |
| S18-03 | sources | 0.2: the CCS+ source box is open, with its login | [L33](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L33) |
| S18-04 | sources | CCS+ login only on the dashboard (not in Settings) | [L34](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L34) |
| S18-05 | sources | The CCS+ setup page contains the note distinguishing Calendar Sync credentials from the CCS login. | [L35](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L35) |
| S18-06 | sources | Sync now disabled until the login is entered | [L36](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L36) |
| S18-07 | sources | saving returns to the CCS+ box | [L38](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L38) |
| S18-08 | sources | rejection shown next to the boxes | [L40](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L40) |
| S18-09 | sources | Setting last_auth_ok displays the Validated marker; typing behavior is checked in suite 19. | [L42](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L42) |
| S18-10 | google | Autosync client form on the dashboard only, with its guide | [L43](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L43) |
| S18-11 | feeds | Feeds (beta.17): the feed link, then Add to Google / Apple / Outlook beside it; Google Calendar sync is in Settings | [L46](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L46) |
| S18-12 | feeds | the buttons are explained (Information & Instructions) | [L48](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L48) |
| S18-13 | shell | At least three copy-icon buttons are present and no literal Copy text button is rendered. | [L49](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L49) |
| S18-14 | diagnostics | footer: report a problem / suggest a feature | [L50](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L50) |
| S18-15 | sources | 0.2.8-beta.15: CCS+'s Manual Upload row, laid out like Import (the file field fills the line) | [L51](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L51) |
| S18-16 | rules | Saved RDO and LSR color rules render their labels/swatches and a calendar swatch style. | [L59](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L59) |
| S18-17 | sources | Renaming the calendar renders the submitted calendar name. | [L60](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L60) |
| S18-18 | calendar | 0.2.8: Close and the bell instead of the pin; add-on-click days | [L61](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L61) |
| S18-19 | calendar | click an event: it opens | [L70](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L70) |
| S18-20 | calendar | F2.2.1 (0.2.8): click elsewhere: it stays open | [L72](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L72) |
| S18-21 | calendar | …until its Close | [L74](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L74) |
| S18-22 | calendar | 6.3 / F1.3: click an empty day: Add event in a pop-up | [L76](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L76) |
| S18-23 | feeds | Clicking a copy button shows Copied feedback. | [L85](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L85) |
| S18-24 | feeds | After the delay, the copy button again contains one SVG icon. | [L87](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_18.py#L87) |

## Coverage limits and reconciliation notes

- Row 09 seeds successful authentication state; it does not perform a successful real CCS+ sign-in.
- Row 16 checks a rendered page containing rule labels/swatches; its historical label mentions multiple sections more broadly than the predicate proves.
- Row 22 dispatches a synthetic click on a day node; it verifies the opened dialog/iframe, not physical hit-testing on all empty-day areas.
- Clipboard rows 23–24 assert Copied feedback then icon restoration, not the clipboard’s actual text.
- Overlaps: suite 19 Validated/edit controls and rule ownership; suite 21 adding/unapplying rules and help placement.
