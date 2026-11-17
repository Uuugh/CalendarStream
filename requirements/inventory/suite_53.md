# Suite 53: Google traffic, sync limits, recurrence and lockout

Source: [`tests/suite_53.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8123; Demo.ics; patched loops/API readiness. Fixture token/API traffic is inspected without redaction. Later pure feed parsing uses generated ICS, patched event caps and date bounds. Installer/CSS/JS are source-scanned, and bash -n is executed on install.sh. No browser.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S53-01 | diagnostics | The stored mock token-exchange request body includes the fixture client secret unredacted. | [L50](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L50) |
| S53-02 | diagnostics | Calendar API traffic records are nonempty and all sampled requests retain a Bearer Authorization header. | [L54](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L54) |
| S53-03 | diagnostics | Each sampled Calendar API traffic record has an integer response status. | [L56](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L56) |
| S53-04 | diagnostics | Clearing traffic makes the recent-record list empty. | [L58](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L58) |
| S53-05 | google | The sampled sync row records the same nonempty remote_updated timestamp as its mock Google event. | [L63](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L63) |
| S53-06 | google | A remote edit immediately after sync updates the local title and yields the sampled changed-in-Google log message. | [L68](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L68) |
| S53-07 | google | With five remote orphans and MAX_WRITES=2, three remain and recent logs say more at the next sync. | [L80](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L80) |
| S53-08 | google | The next full sync leaves no active orphan records. | [L82](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L82) |
| S53-09 | account | Reaching the global failure limit produces exactly one recent History message naming the container log and restart recovery. | [L91](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L91) |
| S53-10 | account | During the global block, the sampled new external IP is blocked. | [L101](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L101) |
| S53-11 | account | During that block, four sampled private/loopback/IPv6-local addresses are not blocked. | [L102](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L102) |
| S53-12 | account | The IP supplied by patched public-domain DNS resolution is not blocked. | [L104](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L104) |
| S53-13 | sources | Moving one recurrence through RECURRENCE-ID preserves the complete sampled UID list and includes its changed title. | [L129](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L129) |
| S53-14 | sources | With a cap of ten, the reverse-ordered sixty-event fixture retains exactly the ten earliest IDs in the uncapped sort order. | [L141](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L141) |
| S53-15 | process | Installer text selects the pinned version-tag URL for compose download and omits the checked default-branch compose expression. | [L146](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L146) |
| S53-16 | process | Running bash -n on install.sh returns zero. | [L149](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L149) |
| S53-17 | sources | Combined CSS omits the sampled hidden date-label rule and contains the checked flex rule. | [L153](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L153) |
| S53-18 | shell | The savePref source slice includes response-error throwing and failure feedback and omits the sampled older continuation expression. | [L156](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_53.py#L156) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Traffic rows intentionally observe raw fixture secret/header data in diagnostics. No live credential values are copied into this inventory; they are observations of tests, not a change to data-handling policy.
- Row 03's all() is vacuous by itself; row 02 supplies nonempty API records. Row 05 checks one selected sync row, not every write.
- Lockout helper treats exceptions other than status 429 as unblocked; DNS is patched, not resolved externally. Network classifications use four finite samples.
- Recurrence row 13 checks stable UIDs and changed title, not retained user-edit values independently. Installer/CSS/JS string checks do not execute install/view/error behavior; bash -n checks shell syntax only.
- Overlaps: suites 45/48 Google sync; suites 55/60 lockout/downloads; suite 49 recurrence/import context.
