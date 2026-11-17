# DRAFT requirements: feeds (for the Developer's review)

Not approved. Derived from every inventory row whose candidate feature includes `feeds`, using the
merged inventory at `5dbb9aa2f28529dccf77b801d8fb85b07c33a1cf`. No `requirements/feeds.md` exists at
that revision, so numbering begins FED-01. Evidence keys refer to the pinned source and limitations in
`requirements/inventory/suite_NN.md`. These statements are proposals, not runtime verification.

Shared UI mechanics are not repeated here. References to other drafts identify ownership rather than
approving those drafts; the sources draft was reviewed and merged in PR #53. Its SRC references remain subject to
Claude's cross-feature review.

| ID | status | statement | evidence |
|---|---|---|---|
| FED-01 | proposed | A feed offers a subscription link and ways to add it to Google Calendar, Apple Calendar and Outlook, with instructions for those choices. | S18-11, S18-12, S39-14, S51-19 |
| FED-02 | proposed | A feed reports Not read yet until fetched; afterward it reports its last read, identifying Google when Google is the reader. | S19-28, S19-29, S40-05, S44-11 |
| FED-03 | proposed | Changing the page’s display time zone does not change the feed’s time zone. | S19-32 |
| FED-04 | proposed | A missing feed destination or an invalid feed token does not expose a feed and returns not found. | S23-26, S26-04 |
| FED-05 | proposed | A feed can publish all chosen source calendars under its own name; its calendar data includes those sources’ events and its chosen calendar name. | S26-33, S26-35 |
| FED-06 | proposed | A feed’s included calendars can be changed independently of other destinations. | S26-36 |
| FED-07 | proposed | A feed’s subscription page identifies the feed by its name. | S26-37 |
| FED-08 | proposed (?) | A stream name accepts letters such as OneWay, but refuses spaces and punctuation such as an exclamation mark; malformed input identifies the stream field. What is the complete allowed character set? | S26-38, S26-39, S51-11 |
| FED-09 | proposed | Each feed stream token must be unique; a duplicate is refused without creating another destination and identifies the stream field. | S26-40, S51-10 |
| FED-10 | proposed | Pasting an old full feed URL restores its stream token, both when creating and updating a feed. Once replaced, the new token works and the replaced token no longer does. | S26-41, S26-42, S51-09 |
| FED-11 | proposed | Removing a feed makes its subscription URL stop working. | S26-52 |
| FED-12 | proposed | Legacy migration preserves the feed token and scopes the migrated destination to CCS+. Google migration is owned by the Google feature. | S26-64, S26-65 |
| FED-13 | proposed | A feed can be limited by start and end dates; clearing both limits restores its full event set. A start date may be saved without an end date. | S29-02, S29-04, S39-19 |
| FED-14 | proposed | An end date before the start date is refused and identifies the end-date field. | S29-03, S51-13 |
| FED-15 | proposed | Leaving a new feed’s name and note empty inherits them from its selected source; explicit values are preserved. | S31-01, S58-17, S58-18 |
| FED-16 | proposed (?) | Saving a source does not replace an unrelated unsaved feed-name edit. Is preserving unrelated pending edits a shared saving rule for all features? | S34-15 |
| FED-17 | proposed | Published events include their display reminders, including fifteen-minute and one-hour reminders. Reminder selection belongs to EVT-19. | S36-26 |
| FED-18 | proposed | An unchanged feed supports conditional reads with an ETag and an empty not-modified response; changing its events causes an old ETag to receive updated content. | S39-10, S39-11 |
| FED-19 | proposed | An ordinary feed reports reads rather than a next-push schedule. | S46-02 |
| FED-20 | proposed | Creating a feed saves its chosen name, included calendars, start date and note. | S51-07, S51-52 |
| FED-21 | proposed | The legacy gfeed kind creates an ordinary calendar feed. | S51-08 |
| FED-22 | proposed | A valid replacement stream name is saved and its URL serves the feed. | S51-12, S51-18 |
| FED-23 | proposed | A feed can use a selected configured public base address, and its link combines that address with its stream token. Public-domain configuration belongs to settings. | S26-32, S51-16, S51-17 |
| FED-24 | proposed | A feed can be sent using email or SMS links. | S51-55 |
| FED-25 | proposed (?) | Feed creation supplies a generated stream token and explains how an old feed link can be reused. The checked generated tokens contain at least twenty characters. Is twenty the guaranteed minimum rather than just the tested generator length? | S58-15 |
| FED-26 | proposed | New-feed name and note suggestions follow the selected source; changing which source is selected updates the suggestion. | S58-37, S58-38 |
| FED-27 | proposed (?) | A stream name may contain one through 128 characters; 129 characters and embedded spaces are refused by the checked validator. Does the same limit apply to every save route? | S63-11 |
| FED-28 | proposed | Turning a feed off makes its URL temporarily unavailable; turning it back on clears its off state without changing its included calendars. | S63-22, S63-23, S63-24 |
| FED-29 | proposed | Published calendar data preserves event titles, start times and end times when read back as calendar data. | S77-07 |
| FED-30 | proposed (?) | When creating the required Local calendar, it is included in the destination checked by the oracle. Should this inclusion apply to every existing destination or only the combined/default destination? | S77-16 |

## Not requirements

Each remaining row is mapped to shared ownership or excluded with its reason. These are not
additional feed requirements. Unspecified shared mechanics remain questions for shared-UI review.

- S18-23: Shared copy-control feedback and icon reset; owned by shared UI, not a separate feed rule. UI-01/UI-02 do not yet specify copy feedback; retained for shared-UI review.
- S18-24: Shared copy-control feedback and icon reset; owned by shared UI, not a separate feed rule. UI-01/UI-02 do not yet specify copy feedback; retained for shared-UI review.
- S21-21: Google sign-in placement belongs to settings/google; historical two-destination arrangement is not a separate feed behavior rule.
- S29-05: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S31-02: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S31-08: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S31-09: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S35-13: Font and SVG-symbol markup are presentation/implementation, not subscription behavior.
- S38-16: Source-color change is owned by sources (SRC-39 in its pending draft); calendar-key effects are CAL-45. Source-picker color markup is not restated here.
- S39-15: Markup order is presentation, not a separate feed rule.
- S41-01: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S41-02: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-08: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-23: Single-destination handle visibility is shared reorder-control UI, not feed publishing behavior; retained as an open shared-UI mapping.
- S44-31: Shared modal/backdrop behavior: UI-01; visual filter belongs to theme.
- S44-37: Shared date-range input grouping rather than a separate feed rule; actual date filtering is specified above.
- S44-49: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-54: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-55: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-56: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-57: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S51-05: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-06: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-20: Markup order is presentation, not a separate feed rule.
- S51-21: Markup order is presentation, not a separate feed rule.
- S51-48: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-49: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-50: Shared field-error styling/reset mechanics, not feed behavior. Invalid stream rejection is specified above; styling belongs to theme.
- S51-51: Shared field-error styling/reset mechanics, not feed behavior. Invalid stream rejection is specified above; styling belongs to theme.
- S51-53: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S51-54: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S55-10: Absence of a palette note is presentation, not a publishing guarantee.
- S58-16: Source metadata/label implementation; source naming and notes belong to sources (SRC-28).
- S58-39: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S59-07: Shared removal confirmation (UI-06); newline formatting belongs to presentation. The stopped-link consequence is specified above.
- S63-05: Source-string presence for URL/meeting notes does not establish executed publishing behavior.

## Coverage and open questions

All 93 feed-candidate evidence rows are accounted for in 30 proposed requirements and
36 excluded/shared-owner mappings. Questions in the table preserve uncertainty rather than
generalizing beyond the oracle. The complete stream character set, generated-token guarantee and
default-destination inclusion policy need review. No application suites were run locally.
