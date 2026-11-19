# Requirements: feeds

Statuses: verified, built, open, planned (approved, not built yet) and proposed (drafted, not yet reviewed by the Developer).
Terms: the **stream token** is the part of a feed's address that identifies it (called the stream name in the old app); a **destination** is a feed or a Google calendar that the app publishes to.


| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| FED-01 | proposed | A feed publishes the calendars the user chooses, under its own name, for other apps to read. | — | — |
| FED-01.a | proposed | A feed can publish all chosen source calendars under its own name; its calendar data includes those sources’ events and its chosen calendar name. | — | S26-33, S26-35 |
| FED-01.b | proposed | A feed’s included calendars can be changed independently of other destinations. | — | S26-36 |
| FED-01.c | proposed | Each feed decides which calendars it carries; the required Local calendar is in a feed only as that feed's own settings say, never because of a rule special to Local. | — | S77-16 |
| FED-01.d | proposed | A feed can be limited by a date range (UI-23); with no range it publishes its full event set. | — | S29-02, S29-04, S39-19, S29-03, S51-13 |
| FED-01.e | proposed | A published feed includes events according to their visibility under CAP-02 and EVT-20; hiding an imported event removes it from feed publication. | — | readme_gaps:47 |
| FED-01.f | proposed | A new feed's name and note default to the selected source's and follow it when the selected source changes; values the user typed are kept. | — | S31-01, S58-17, S58-18, S58-37, S58-38 |
| FED-01.g | proposed | A feed’s subscription page identifies the feed by its name. | — | S26-37 |
| FED-01.h | proposed | Turning a feed off makes its URL temporarily unavailable; turning it back on clears its off state without changing its included calendars. | — | S63-22, S63-23, S63-24 |
| FED-01.i | proposed | Removing a feed makes its subscription URL stop working. | — | S26-52 |
| FED-02 | proposed | A feed has an address that contains its stream token, which is generated or chosen by the user. | — | — |
| FED-02.a | proposed | A token is generated automatically when a feed is created, with the length and strength in DEF-01, from a cryptographically secure generator (OWASP's recommendation for unguessable identifiers). The user may enter a different token instead; its strength is shown as UI-18, with the hint recommending the strength in DEF-01. Reusing an old feed link is FED-02.b. | — | S58-15 |
| FED-02.b | proposed | Pasting an old full feed URL restores its stream token, both when creating and updating a feed. Once replaced, the new token works and the replaced token no longer does. | — | S26-41, S26-42, S51-09 |
| FED-02.c | proposed | A stream token may contain any character. Characters outside the RFC 3986 unreserved set (letters, digits, hyphen, period, underscore, tilde) are percent-encoded in the feed's address, so a space becomes %20. A character is as DEF-03 says. | — | S26-38, S26-39, S51-11 |
| FED-02.d | proposed | A stream token has a length within the limits in DEF-01, wherever it is saved; the characters it may contain are FED-02.c. | — | S63-11 |
| FED-02.e | proposed | Each feed stream token is unique; a duplicate is not valid (UI-19) and no second destination is created. | — | S26-40, S51-10 |
| FED-02.f | proposed | A feed can use a selected configured public base address, and its link combines that address with its stream token. Public-domain configuration belongs to settings. | — | S26-32, S51-16, S51-17 |
| FED-02.g | proposed | A missing feed destination or an invalid feed token does not expose a feed and returns not found. | — | S23-26, S26-04 |
| FED-03 | proposed | The user can subscribe to a feed from other calendar apps. | — | — |
| FED-03.a | proposed | A feed offers a subscription link and ways to add it to Google Calendar, Apple Calendar and Outlook, with instructions for those choices. | — | S18-11, S18-12, S39-14, S51-19 |
| FED-03.b | proposed | The user can share a feed subscription address by copying it, through the device's own sharing facility, or in an email or SMS link. | — | S51-55, readme_gaps:64, changelog_gaps_601-900:27, readme_gaps:64, changelog_gaps_601-900:27 |
| FED-03.c | proposed | Subscription guidance (shown with the feed's instructions, FED-03.a) tells the user: to enable calendar synchronization on Android and iPhone and to use Google's desktop site to add a subscription; that using a feed and direct synchronization for the same calendar can duplicate events; that Google may take up to twelve hours to read a feed; that Google may keep the name from its first read, so the user may need to rename the subscribed calendar (direct naming is GGL-30); that Google subscriptions do not use the feed's color; and how the destination types compare, naming the current one (UI-07). This is provider guidance, not a CalendarStream delivery guarantee. | — | readme_gaps:87, changelog_gaps_1501-1800:19, readme_gaps:87, changelog_gaps_1501-1800:19, changelog_gaps_1801-2100:21, changelog_gaps_1801-2100:21, changelog_gaps_2101-2336:22, changelog_gaps_2101-2336:23, changelog_gaps_601-900:29 |
| FED-04 | proposed | A feed's content reads correctly in calendar apps. | — | — |
| FED-04.a | proposed | Feeds carry each event's own time zone (TIM-07); the page's display time zone does not change them. | — | S19-32 |
| FED-04.b | proposed | Published calendar data preserves event titles, start times and end times when read back as calendar data. | — | S77-07 |
| FED-04.c | proposed | Published events include their display reminders, including fifteen-minute and one-hour reminders. Reminder selection belongs to EVT-19. | — | S36-26 |
| FED-04.d | proposed | Published ICS carries the feed’s color in X-APPLE-CALENDAR-COLOR for consumers that support that calendar property. | — | changelog_gaps_2101-2336:23, changelog_gaps_601-900:40 |
| FED-04.e | proposed | A published event's online meeting address is also the first line of its notes (EVT-41 owns the ICS URL). | — | changelog_gaps_301-600:22 |
| FED-04.f | proposed | An unchanged feed supports conditional reads with an ETag and an empty not-modified response; changing its events causes an old ETag to receive updated content. | — | S39-10, S39-11 |
| FED-05 | proposed | A feed shows when it was last read. | — | — |
| FED-05.a | proposed | A feed reports Not read yet until fetched; afterward it reports its last read, identifying Google when Google is the reader. | — | S19-28, S19-29, S40-05, S44-11 |
| FED-05.b | proposed | An ordinary feed reports reads rather than a next-push schedule. | — | S46-02 |

## Notes from the draft

### Not requirements

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
- S38-16: Source-color change is owned by sources (SRC-01 in its pending draft); calendar-key effects are CAL-45. Source-picker color markup is not restated here.
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
- S58-16: Source metadata/label implementation; source naming and notes belong to sources (SRC-01).
- S58-39: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S59-07: Shared removal confirmation (UI-06); newline formatting belongs to presentation. The stopped-link consequence is specified above.
- S63-05: Source-string presence for URL/meeting notes does not establish executed publishing behavior.

### Coverage and open questions

All 93 feed-candidate evidence rows are accounted for in 30 proposed requirements and
36 excluded/shared-owner mappings. Questions in the table preserve uncertainty rather than
generalizing beyond the oracle. The complete stream character set, generated-token guarantee and
default-destination inclusion policy need review. No application suites were run locally.
