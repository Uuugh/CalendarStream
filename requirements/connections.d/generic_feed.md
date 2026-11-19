# Requirements: Generic Feed

The Generic Feed connection: the user's events published as a calendar feed that other calendar apps subscribe to. Common connection rules and the content every published event carries are in `connections.md` (CON-09). Issues and history of this feature are in git.
Terms: the **stream token** is the part of a feed's address that identifies it (called the stream name in the old app); a **destination** is a feed or a Google calendar that the app publishes to.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CFED-01 | proposed | A feed publishes the calendars the user chooses, under its own name, for other apps to read. | — | — |
| CFED-01.i | proposed | A Generic Feed is a feed. | — | — |
| CFED-01.a | proposed | A feed can publish all chosen source calendars under its own name; its calendar data includes those sources’ events and its chosen calendar name. | — | S26-33, S26-35 |
| CFED-01.b | proposed | A feed’s included calendars can be changed independently of other destinations. | — | S26-36 |
| CFED-01.c | proposed | Each feed decides which calendars it carries; the required Local calendar is in a feed only as that feed's own settings say, never because of a rule special to Local. | — | S77-16 |
| CFED-01.d | proposed | A feed can be limited by a date range (UIC-23); with no range it publishes its full event set. | — | S29-02, S29-04, S39-19, S29-03, S51-13 |
| CFED-01.e | proposed | A new feed's name and note default to the selected source's and follow it when the selected source changes; values the user typed are kept. | — | S31-01, S58-17, S58-18, S58-37, S58-38 |
| CFED-01.f | proposed | A feed’s subscription page identifies the feed by its name. | — | S26-37 |
| CFED-01.g | proposed | Turning a feed off makes its URL temporarily unavailable; turning it back on clears its off state without changing its included calendars. | — | S63-22, S63-23, S63-24 |
| CFED-01.h | proposed | Removing a feed makes its subscription URL stop working. | — | S26-52 |
| CFED-02 | proposed | A feed has an address that contains its stream token, which is generated or chosen by the user. | — | — |
| CFED-02.a | proposed | A token is generated automatically when a feed is created, with the length and strength in DEF-01, from a cryptographically secure generator (OWASP's recommendation for unguessable identifiers). The user may enter a different token instead; its strength is shown as UIC-18, with the hint recommending the strength in DEF-01. Reusing an old feed link is CFED-02.b. | — | S58-15 |
| CFED-02.b | proposed | Pasting an old full feed URL restores its stream token, both when creating and updating a feed. Once replaced, the new token works and the replaced token no longer does. | — | S26-41, S26-42, S51-09 |
| CFED-02.c | proposed | A stream token may contain any character. Characters outside the RFC 3986 unreserved set (letters, digits, hyphen, period, underscore, tilde) are percent-encoded in the feed's address, so a space becomes %20. A character is as DEF-03 says. | — | S26-38, S26-39, S51-11 |
| CFED-02.d | proposed | A stream token has a length within the limits in DEF-01, wherever it is saved; the characters it may contain are CFED-02.c. | — | S63-11 |
| CFED-02.e | proposed | Each feed stream token is unique; a duplicate is not valid (UIC-19) and no second destination is created. | — | S26-40, S51-10 |
| CFED-02.f | proposed | A feed can use a selected configured public base address, and its link combines that address with its stream token. Public-domain configuration belongs to settings. | — | S26-32, S51-16, S51-17 |
| CFED-02.g | proposed | A missing feed destination or an invalid feed token does not expose a feed and returns not found. | — | S23-26, S26-04 |
| CFED-03 | proposed | The user can subscribe to a feed from other calendar apps. | — | — |
| CFED-03.a | proposed | A feed offers a subscription link and ways to add it to Google Calendar, Apple Calendar and Outlook, with instructions for those choices. | — | S18-11, S18-12, S39-14, S51-19 |
| CFED-03.b | proposed | The user can share a feed subscription address by copying it, through the device's own sharing facility, or in an email or SMS link. | — | S51-55, readme_gaps:64, changelog_gaps_601-900:27, readme_gaps:64, changelog_gaps_601-900:27 |
| CFED-03.c | proposed | Subscription guidance (shown with the feed's instructions, CFED-03.a) tells the user: to enable calendar synchronization on Android and iPhone and to use Google's desktop site to add a subscription; that using a feed and direct synchronization for the same calendar can duplicate events; that Google may take up to twelve hours to read a feed; that Google may keep the name from its first read, so the user may need to rename the subscribed calendar (direct naming is CGOW-02); that Google subscriptions do not use the feed's color; and how the destination types compare, naming the current one (UIC-07). This is provider guidance, not a CalendarStream delivery guarantee. | — | readme_gaps:87, changelog_gaps_1501-1800:19, readme_gaps:87, changelog_gaps_1501-1800:19, changelog_gaps_1801-2100:21, changelog_gaps_1801-2100:21, changelog_gaps_2101-2336:22, changelog_gaps_2101-2336:23, changelog_gaps_601-900:29 |
| CFED-04 | proposed | A feed's content reads correctly in calendar apps. | — | — |
| CFED-04.a | proposed | Published ICS carries the feed’s color in X-APPLE-CALENDAR-COLOR for consumers that support that calendar property. | — | changelog_gaps_2101-2336:23, changelog_gaps_601-900:40 |
| CFED-04.b | proposed | An unchanged feed supports conditional reads with an ETag and an empty not-modified response; changing its events causes an old ETag to receive updated content. | — | S39-10, S39-11 |
| CFED-05 | proposed | A feed shows when it was last read. | — | — |
| CFED-05.a | proposed | A feed reports Not read yet until fetched; afterward it reports its last read, identifying Google when Google is the reader. | — | S19-28, S19-29, S40-05, S44-11 |
| CFED-05.b | proposed | An ordinary feed reports reads rather than a next-push schedule. | — | S46-02 |
