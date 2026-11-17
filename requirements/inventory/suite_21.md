# Suite 21: Month picker, clock, settings and rule dialog

Source: [`tests/suite_21.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTP server on 8090; Chromium/Playwright; Demo.ics and a synthetic event. Main asserted browser viewport is 1100×900. The final 390×900 dark context only captures a screenshot; it has no `ok()` assertion.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S21-01 | calendar | Opening the month picker shows it and marks October as the active month. | [L31](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L31) |
| S21-02 | calendar | Advancing the picker year twice shows 2028 and no active month in that year. | [L34](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L34) |
| S21-03 | calendar | picking Mar jumps to March 2028 | [L36](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L36) |
| S21-04 | calendar | clicking elsewhere closes the picker | [L38](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L38) |
| S21-05 | calendar | Clock control has switch role, a Time format tooltip and badge 12; hollow shape is not asserted. | [L42](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L42) |
| S21-06 | calendar | legend help dot: one 15 px help icon (F1.2, 0.2.8) | [L45](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L45) |
| S21-07 | calendar | Clock defaults to aria-checked false with 9:45am shown and is within 330px of the calendar right edge. | [L46](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L46) |
| S21-08 | calendar | icon → 24-hour, saved, calendar redrawn, badge now reads 24 | [L48](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L48) |
| S21-09 | calendar | Clicking the clock again persists 12-hour mode. | [L51](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L51) |
| S21-10 | settings | There are five Settings groups and every group has a solid left border. | [L54](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L54) |
| S21-11 | account | Login username/password fields align vertically within 3px and the username label says User name. | [L56](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L56) |
| S21-12 | sources | 0.2.2: the source's header shows its status and Sync Now | [L59](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L59) |
| S21-13 | rules | The source starts with two predefined rules and the first names Items without an end time. | [L63](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L63) |
| S21-14 | rules | + Add a rule has no menu while nothing can be reused | [L65](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L65) |
| S21-15 | rules | New rule… in a calendar opens the rule dialog, applying to that calendar (0.2.8-beta.3) | [L67](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L67) |
| S21-16 | rules | The source rule saves RDO OR LSR conditions and applies to CCS+. | [L73](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L73) |
| S21-17 | rules | After adding the rule, the source and All Rules each contain three rules. | [L75](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L75) |
| S21-18 | rules | Unapplying a source rule removes it from that source but retains it in All Rules. | [L78](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L78) |
| S21-19 | events | I2: clicking empty space to the right of All-day doesn't tick it | [L83](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L83) |
| S21-20 | events | clicking the words ticks it | [L85](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L85) |
| S21-21 | feeds | 0.2.8-beta.4: two destinations; the Google sign-in is in Settings | [L87](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L87) |
| S21-22 | calendar | #10: the Calendars and Key parts each with a help dot (beta.29, F15.5) | [L88](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L88) |
| S21-23 | rules | beta.3 (F5.1): How rules work is in the rule dialog, not under All Rules | [L89](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L89) |
| S21-24 | sources | #9: the file field shows the chosen file | [L91](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L91) |
| S21-25 | shell | The filtered set of visible source/destination controls has no measured height other than 34px. | [L93](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_21.py#L93) |

## Coverage limits and reconciliation notes

- Rows 05–09 assert role, tooltip, badge, state, persistence and sampled calendar text; the hollow-clock drawing is only described in comments/labels.
- Row 25 measures a filtered control set; `set(heights) <= {34}` also passes if that set is empty. It does not cover all buttons or accessibility target sizes.
- The final dark/phone month-picker screenshot is not an automated assertion of phone/dark behavior.
- Row 11 compares field positions and label text; it does not independently assert labels are above fields.
- Overlaps: suite 19 clock format, Settings groups and login UI; suite 18 calendar/dialog interactions; rule rows extend source-scoped add/unapply behavior.
