# Suite 19: Clock format, event editor, settings and feeds

Source: [`tests/suite_19.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTP server on 8094; Chromium/Playwright at 800×900; Demo.ics plus synthetic added events. Background loops patched; Google client health records are seeded directly. Browser screenshots are incidental captures, not image assertions.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S19-01 | calendar | F1.5: no Time format in Settings; the icon above the calendar | [L27](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L27) |
| S19-02 | calendar | Automatic in English: 12-hour in the calendar | [L29](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L29) |
| S19-03 | calendar | POST /ui/clock with clock=24 returns HTTP 204. | [L30](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L30) |
| S19-04 | calendar | 24-hour in the calendar | [L32](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L32) |
| S19-05 | events | In 24-hour mode, the editor has start_time=09:00 and no legacy start_hour field. | [L34](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L34) |
| S19-06 | events | In 12-hour mode, the editor renders start_time=9:00am and a 10:00am value. | [L37](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L37) |
| S19-07 | events | time zone menu (the calendar's zone) and the different-end option | [L38](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L38) |
| S19-08 | events | The editor has twelve color inputs including Tomato. | [L39](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L39) |
| S19-09 | calendar | An unknown clock-format value returns HTTP 400. | [L40](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L40) |
| S19-10 | events | Saving the event with the sampled typed times returns HTTP 303. | [L44](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L44) |
| S19-11 | events | Typed 1:30 pm and 1505 persist as 13:30 and 15:05; the selected color is normalized to lowercase. | [L46](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L46) |
| S19-12 | events | The invalid typed time 13pm returns HTTP 400. | [L49](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L49) |
| S19-13 | events | colors outside Google's palette refused | [L52](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L52) |
| S19-14 | events | An event using plain HH:MM time values still saves with HTTP 303. | [L55](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L55) |
| S19-15 | events | event color shows in the calendar | [L57](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L57) |
| S19-16 | events | event color beats the tag (Google color Grape) | [L62](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L62) |
| S19-17 | events | edit page shows the chosen color | [L65](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L65) |
| S19-18 | events | Changing a United-origin event color retains the color and marks the event edited but not stale. | [L72](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L72) |
| S19-19 | sources | Exactly one rendered CCS+ Validated marker is present. | [L76](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L76) |
| S19-20 | google | Seeded accepted Google client renders Not checked or Healthy, a status box and the saved client ID. | [L81](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L81) |
| S19-21 | google | A gconnectbtn class occurs in the rendered page. | [L82](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L82) |
| S19-22 | google | Rejected client markup includes Client rejected, a warn status box and its rejection message. | [L85](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L85) |
| S19-23 | rules | 0.2: Rules (were Tag Colors) inside the source box | [L91](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L91) |
| S19-24 | sources | 0.2.6: no (edit); the title is a field while Configure is open | [L92](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L92) |
| S19-25 | rules | The newly saved calendar-specific rule is first in that source’s rule list. | [L94](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L94) |
| S19-26 | rules | Renaming the source keeps its calendar-specific rule. | [L96](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L96) |
| S19-27 | rules | Deleting the rule removes it from all_rules. | [L98](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L98) |
| S19-28 | feeds | Before any feed request, the page shows Not read yet. | [L102](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L102) |
| S19-29 | feeds | after Google's reader fetched it: last read shown | [L105](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L105) |
| S19-30 | calendar | The unknown display time zone Mars/Base returns HTTP 400. | [L107](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L107) |
| S19-31 | calendar | Selecting Los Angeles displays the sample event as 06:45–13:15 and selects that zone. | [L111](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L111) |
| S19-32 | feeds | Changing the display zone leaves the feed X-WR-TIMEZONE at America/New_York. | [L113](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L113) |
| S19-33 | events | new events start in the calendar's time zone | [L115](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L115) |
| S19-34 | events | Changing start to 11am normalizes it to 11:00am and moves the one-hour end to 12:00pm. | [L126](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L126) |
| S19-35 | events | The end-time menu shows 12:30pm with a 1h30 duration annotation. | [L128](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L128) |
| S19-36 | events | Selecting the 12:30pm suggestion updates the field and hides the menu. | [L130](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L130) |
| S19-37 | events | Changing start to 2300 preserves 90 minutes and advances the end to 12:30am on the next day. | [L132](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L132) |
| S19-38 | events | Moving the overnight event start date from October 8 to 12 moves its end date to October 13. | [L134](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L134) |
| S19-39 | events | 25:00 is marked and blocks saving | [L136](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L136) |
| S19-40 | events | color under Location (F11); Cancel &#124; Save at bottom right | [L143](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L143) |
| S19-41 | events | picking a color shows it and closes the palette | [L146](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L146) |
| S19-42 | events | The different-end-zone field is hidden by default. | [L149](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L149) |
| S19-43 | events | After choosing a Los Angeles end zone, changing start to 10am leaves end at 11am Los Angeles. | [L152](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L152) |
| S19-44 | events | picking a color shows it and closes the palette | [L154](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L154) |
| S19-45 | events | Saving the browser event persists 10am New York start, 11am Los Angeles end and Tomato color. | [L157](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L157) |
| S19-46 | events | reopens with both time zones | [L159](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L159) |
| S19-47 | sources | dashboard: ✓ Validated, no button | [L162](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L162) |
| S19-48 | sources | Editing the source username hides the Validated marker and shows its save control. | [L164](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L164) |
| S19-49 | settings | Settings contains neither the old ccsmenu node nor a node with ID google; see scope note below. | [L166](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L166) |
| S19-50 | account | The page-login status chip is visible, its text contains Signed in, and current password is hidden. | [L167](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L167) |
| S19-51 | account | typing a new password asks for the current one and shows Save | [L169](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L169) |
| S19-52 | settings | Settings groups are exactly pagelogin, domains, updates, look, googlesync in that order. | [L172](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L172) |
| S19-53 | settings | The This page button lies horizontally inside the public-address input bounds. | [L174](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_19.py#L174) |

## Coverage limits and reconciliation notes

- Rows 41 and 44 intentionally repeat the same palette selection check in two contexts; retained as separate evidence.
- Row 20’s legacy label says Ready to connect but its actual predicate allows Not checked or Healthy. Row 21 checks a connect-button class exists, not its physical position outside a fold.
- Row 43 checks the displayed end after a zone change. Row 45 separately asserts persisted offset-bearing timestamps; together they give stronger cross-zone evidence.
- Row 49 checks old node IDs only; it does not prohibit the `googlesync` group, which row 52 explicitly requires.
- Row 53 checks horizontal geometry only; the label’s independent-form/Cancel/Save claim is not asserted there.
- Row 15 accepts either a swatch style or any occurrence of the color string; it is weaker than a pixel/color check.
- Screenshots are written to temporary paths without visual comparisons.
- Overlaps: suite 13 colors and rules; suite 18 source state; suite 21 clock and Settings groups.
