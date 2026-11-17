# Suite 26: Fresh sources, destinations, rules, templates and migration

Source: [`tests/suite_26.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient at a synthetic HTTPS host; mock Google server on 8126. Fresh database with no legacy source/destination seed. Source downloads are replaced with synthetic work.ics; later duplicate/delete checks upload Demo.ics. Main source/Google/update loops patched. Mock OAuth is used for Google destinations.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S26-01 | sources | A fresh install has exactly one local source named Local and no destinations. | [L34](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L34) |
| S26-02 | sources | The initial page shows Local and No feeds yet, without a CCS+ source node. | [L35](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L35) |
| S26-03 | events | The add-event editor for the sampled date returns HTTP 200. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L36) |
| S26-04 | feeds | Before adding a feed destination, requesting the default feed-token URL returns HTTP 404. | [L37](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L37) |
| S26-05 | sources | Adding CCS+ returns HTTP 303 and appends ccs after the initial Local source. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L39) |
| S26-06 | sources | Adding a second CCS+ source returns HTTP 400. | [L40](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L40) |
| S26-07 | sources | Adding an ICS source with the sampled plain-HTTP URL returns HTTP 400. | [L41](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L41) |
| S26-08 | sources | Adding the named webcal source returns HTTP 303, stores the equivalent HTTPS URL and keeps its name. | [L44](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L44) |
| S26-09 | sources | Adding the same feed URL again returns HTTP 400. | [L45](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L45) |
| S26-10 | sources | Expanding the fixture yields eight Union meetings with distinct UIDs; every source event UID has its source-ID prefix. | [L49](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L49) |
| S26-11 | sources | The downloaded source status is ok and the CCS+ source still has no events. | [L50](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L50) |
| S26-12 | calendar | The page contains both source nodes and the fixture Union meeting text. | [L52](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L52) |
| S26-13 | sources | In page markup, the CCS+ node, login form, URL input, help heading and upload form occur in that order. | [L53](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L53) |
| S26-14 | event_templates | Saving the sampled timed template returns HTTP 303. | [L56](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L56) |
| S26-15 | event_templates | The saved template retains duration 45 minutes, its gray color and Desk location. | [L58](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L58) |
| S26-16 | event_templates | Saving a template with duration x returns HTTP 400. | [L59](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L59) |
| S26-17 | event_templates | The duration samples 1:30, 2, 1.5, 90m and 1h15 parse to 90, 120, 90, 90 and 75 minutes. | [L60](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L60) |
| S26-18 | rules | The first two source rules have event and color actions, with event offset 60. | [L65](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L65) |
| S26-19 | rules | The source has eight rule-origin events; the earliest spans 09:00–09:45 on the sampled date and has Desk location. | [L68](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L68) |
| S26-20 | rules | After applying those rules, the CCS+ source remains empty. | [L70](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L70) |
| S26-21 | events | Opening the editor for the generated rule event returns HTTP 400. | [L72](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L72) |
| S26-22 | rules | A rule scoped to CCS+ appears in CCS+'s effective rules but not Work's. | [L76](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L76) |
| S26-23 | rules | Applying the existing rule to Work returns HTTP 303 and adds it to Work's effective rules. | [L77](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L77) |
| S26-24 | rules | Unapplying it from Work returns HTTP 303, removes it there and retains it on CCS+. | [L78](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L78) |
| S26-25 | rules | The sampled Work Columbus events are nonempty and all resolve to Tomato color. | [L80](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L80) |
| S26-26 | rules | Saving an Add event rule naming a nonexistent template and no event title returns HTTP 400. | [L82](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L82) |
| S26-27 | rules | The page contains All Rules and its dialog, omits Tag Colors, and has the sampled minimum counts of unapply/add-rule controls. | [L84](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L84) |
| S26-28 | rules | The page has at least three delete-icon use elements. | [L86](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L86) |
| S26-29 | events | The event editor renders a source selector, template picker and Prep template data. | [L88](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L88) |
| S26-30 | events | Saving Lunch into Work returns HTTP 303 and creates a custom-origin Lunch event in that source. | [L90](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L90) |
| S26-31 | settings | Before the first destination, the page includes a public-address field prefilled from the request and Settings guidance. | [L93](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L93) |
| S26-32 | feeds | Adding a named feed with a bare public host returns HTTP 303 and saves the normalized HTTPS public address. | [L94](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L94) |
| S26-33 | feeds | The new Everything feed has its requested name, all three source IDs and a token at least 16 characters long. | [L97](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L97) |
| S26-34 | settings | After the address is set, the page no longer contains a public-address input named public. | [L99](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L99) |
| S26-35 | feeds | The Everything feed returns HTTP 200 with 18 VEVENTs and its requested X-WR-CALNAME. | [L101](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L101) |
| S26-36 | feeds | Updating the second feed to Work alone returns HTTP 303 and stores only that source ID. | [L104](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L104) |
| S26-37 | feeds | The second feed's subscription page returns HTTP 200 and contains its Work only name. | [L106](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L106) |
| S26-38 | feeds | The sampled stream name containing a space and exclamation mark returns HTTP 400. | [L108](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L108) |
| S26-39 | feeds | The short stream name OneWay receives a response other than HTTP 400. | [L109](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L109) |
| S26-40 | feeds | A stream name equal to another feed's token returns HTTP 400. | [L110](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L110) |
| S26-41 | feeds | Pasting an old full feed URL returns HTTP 303 and extracts its stream token. | [L111](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L111) |
| S26-42 | feeds | The restored old-token feed URL returns HTTP 200 and the replaced token URL returns HTTP 404. | [L113](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L113) |
| S26-43 | google | Connecting the mock account sets connected state and creates exactly two Google calendars. | [L128](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L128) |
| S26-44 | google | The initial full sync returns success. | [L129](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L129) |
| S26-45 | google | The two mock Google calendars use their respective destination names. | [L131](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L131) |
| S26-46 | google | The CCS+-only destination's tracking rows contain no Work UID; the combined destination's rows contain a Work UID. | [L133](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L133) |
| S26-47 | google | The combined destination has a Columbus Day event whose first matching mock record has Tomato ID 11. | [L135](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L135) |
| S26-48 | google | Renaming the combined destination updates its existing mock Google calendar summary. | [L138](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L138) |
| S26-49 | google | The page has a googlesync node and four destination-box markup occurrences. | [L140](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L140) |
| S26-50 | sources | Removing Work returns HTTP 303, leaves only Local and CCS+ source IDs and removes Work's stored events. | [L143](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L143) |
| S26-51 | sources | After Work removal, the combined Google calendar remains and no destination source list contains Work. | [L144](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L144) |
| S26-52 | feeds | Removing the Work feed returns HTTP 303 and makes its restored old-token URL return HTTP 404. | [L146](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L146) |
| S26-53 | google | Removing one Google destination without delete retains its remote calendar and clears its local calendar info. | [L148](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L148) |
| S26-54 | google | Removing the other Google destination with delete removes its remote calendar. | [L150](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L150) |
| S26-55 | diagnostics | The status API lists Local and CCS+ source IDs and the sole remaining Everything destination name. | [L152](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L152) |
| S26-56 | events | Duplicating the sampled event opens an editor containing Duplicate event, its existing title and an empty UID field. | [L159](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L159) |
| S26-57 | calendar | The rendered event details contain evicon markup and an event-delete form action. | [L161](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L161) |
| S26-58 | events | Deleting the imported source event returns HTTP 303 and marks the stored event hidden. | [L162](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L162) |
| S26-59 | events | Deleting an added event returns HTTP 303 and either removes it or records a calendarstream-prefixed deletion marker. | [L167](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L167) |
| S26-60 | calendar | For week, day, list and month, choosing the view persists its value, renders its expected layout class and checks its view control. | [L173](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L173) |
| S26-61 | calendar | The sampled week page shows the October 11–17 title and links one week backward and forward. | [L176](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L176) |
| S26-62 | calendar | The sampled week header omits times in and event-count text and orders time-zone, view and clock controls. | [L179](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L179) |
| S26-63 | shell | The page orders Calendar, Sources, Destinations, Rules, Templates and Activity section nodes. | [L181](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L181) |
| S26-64 | sources / feeds / google | Legacy migration creates one CCS+ source and feed/Google destinations, both scoped to CCS+. | [L190](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L190) |
| S26-65 | feeds / google | Migration preserves the legacy feed token, Google calendar ID and sync row under the destination and clears the old global calendar ID. | [L191](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_26.py#L191) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- This suite uniquely starts without the old-install source/destination seed: the pinned harness explicitly excludes suite 26 from that seed. Reusing a seeded database changes its scenario.
- Row 03 only checks HTTP 200 on the editor. It does not assert that an event is actually saved into Local.
- Row 10 proves distinct IDs for eight Union events and a prefix for all source events; it does not assert global UID uniqueness for every event type.
- Row 13's observed markup order differs from the broad historical layout label. It does not measure positions or prove upload is beside login.
- Row 19 checks count and the earliest generated event's exact times/location; it does not verify all eight offsets/durations independently. Row 20 only asserts CCS+ remains empty.
- Row 26 covers an absent template and absent title; it does not alone prove the positive inline-new-event-title path.
- Row 35 checks count/name, not every feed event's identity. Row 39 only asserts status is not 400; a redirect or persistence assertion would be stronger.
- Row 47 checks the first matching Columbus event in the combined Google destination, not color behavior in every destination as its label suggests.
- Row 57 checks icon-class presence and delete-action markup; row 59 allows either physical absence or a deletion marker and does not inspect strike-through/Restore/Undo UI.
- Row 60 is one call site iterated for four views. Row 62 reuses the previously fetched week page even though the code has since posted month; it establishes week-header markup only.
- Row 65 checks migration of the feed token, remote calendar mapping and a tracking-row key; it does not assert every field of the migrated row.
- Overlaps: suites 13/20 Google sync; suite 21 source rule applicability; suite 27 built-ins; suite 29 migrations/date ranges; suite 31 destination Configure.
