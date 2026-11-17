# Suite 39: Asset caching, feed validators, event tools and Google setup

Source: [`tests/suite_39.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8095; seed.demo and fake work.ics downloader; background loops patched. CSS/script/font HTTP responses, feed validators and seeded accepted Google-client records drive checks. Chromium uses 1400×1000. The later client-check request is not given a fake Google HTTP client in this suite and may depend on external connectivity.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S39-01 | google | Adding a Google destination before client setup returns 400 and creates no destination with the requested name. | [L32](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L32) |
| S39-02 | google | The page explains that an admin must enable Google Calendar API Sync in Settings. | [L34](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L34) |
| S39-03 | shell | The page links versioned CSS and English script URLs and omits the sampled old inline-style opening. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L38) |
| S39-04 | shell | The versioned CSS response is 200/gzip, has immutable cache-control and contains the sampled checks-list selector. | [L41](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L41) |
| S39-05 | shell | The versioned French script returns 200 with rendered PAGE JSON code, no template brace pair and immutable cache-control. | [L44](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L44) |
| S39-06 | shell | An old script version and an unknown language code each return 404. | [L46](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L46) |
| S39-07 | shell | The versioned font response returns 200 with immutable cache-control and its versioned URL appears in the page. | [L48](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L48) |
| S39-08 | shell | The unversioned font response's cache-control omits immutable. | [L49](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L49) |
| S39-09 | account | The sampled gzip-accepting page request receives no content-encoding header. | [L50](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L50) |
| S39-10 | feeds | An unchanged feed has an ETag and an If-None-Match request returns 304 with an empty body. | [L55](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L55) |
| S39-11 | feeds | After adding a fixture event to that feed's source, the old ETag request returns 200. | [L57](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L57) |
| S39-12 | calendar | The page has one event-tools template, one close-control occurrence and an empty tool placeholder for a United-origin event. | [L59](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L59) |
| S39-13 | google | The page omits the legacy dest-google ID and contains a googlesync section before header end with its client form. | [L62](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L62) |
| S39-14 | feeds | The page includes Add to Google Calendar, Apple Calendar and Outlook text. | [L64](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L64) |
| S39-15 | feeds | The sampled feed module's markup orders Feed link, Google, Apple and Outlook. | [L67](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L67) |
| S39-16 | google | After seeding an accepted client, adding a Google destination makes the final destination type google. | [L73](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L73) |
| S39-17 | google | The client-check form response has Location pointing to Settings googlesync. | [L75](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L75) |
| S39-18 | sources | Clearing a source note leaves calendar_note empty, or under the legacy fallback omits Office from the sampled source markup. | [L79](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L79) |
| S39-19 | feeds | Saving a start date and empty end stores that start date and an empty end string. | [L81](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L81) |
| S39-20 | calendar | Opening the added event creates one Close control, a UID editor link and a delete-form UID matching the event node. | [L92](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L92) |
| S39-21 | calendar | Opening a rule-generated event exposes one Copy control and no Edit or Delete controls. | [L96](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L96) |
| S39-22 | google | Opening Settings shows googlesync and at least one visible state chip. | [L99](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L99) |
| S39-23 | shell | No browser pageerror events are collected during the sampled interactions. | [L100](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_39.py#L100) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Historical docstring says unconfigured Google creates a feed; the actual row 01 expects rejection. The observed predicate governs this inventory.
- Cache rows check immutable presence/absence, not exact max-age of a year/day as labels claim. Row 09 samples one page's content-encoding absence, not all routes or transport compression side channels.
- Row 15 checks DOM/source ordering, not that the buttons lie beside the feed field. Row 17 checks Location but not an explicit response status; its preceding client-check call may attempt external Google traffic.
- Row 18 has a conditional legacy markup fallback. Row 19 checks empty end storage, not runtime inclusion of an event beyond an end boundary.
- Row 20 checks the edit URL has a UID prefix; only the delete UID is compared to the exact event node. Row 21 checks UI tool absence, not server-side authorization of rule-event writes.
- Browser pageerror checks sample this path. Fonts/gzip/assets are inspected through HTTP client responses rather than a performance benchmark.
- Overlaps: suite 35 fonts/icons; suite 26 Google setup gating; suite 29 date bounds; suite 36 embedded event UI.
