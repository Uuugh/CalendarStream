# Suite 17: Languages and translated messages

Source: [`tests/suite_17.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; Demo.ics; background loops patched. Page/log/status/editor/error checks iterate es, fr, de, pt and nl. The default harness skips this suite; `tests/run.sh all` includes it.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S17-01 | shell | globe left of the theme switch; English by default | [L21](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L21) |
| S17-02 | shell | Automatic follows the browser (French) | [L22](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L22) |
| S17-03 | shell | Flemish from nl-BE | [L23](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L23) |
| S17-04 | shell | unknown browser language → English | [L24](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L24) |
| S17-05 | shell | For es/fr/de/pt/nl, HTML language and translated October title are present and sampled English phrases absent. | [L34](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L34) |
| S17-06 | shell | For each tested language, every sampled recent activity-log message changes under translation. | [L38](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L38) |
| S17-07 | shell | For each tested language, the current status message changes under translation. | [L40](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L40) |
| S17-08 | shell | For each tested language, the event editor contains its translated edit-event title. | [L42](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L42) |
| S17-09 | shell | For each tested language, an invalid interval returns 400 and translated 15–1440 minute guidance. | [L44](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L44) |
| S17-10 | shell | Choosing auto clears the stored language override and follows a German browser preference. | [L46](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L46) |
| S17-11 | shell | unknown language refused | [L47](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L47) |
| S17-12 | shell | subscribe page in the visitor's language | [L49](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L49) |
| S17-13 | shell | API-style requests still get JSON errors | [L50](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L50) |
| S17-14 | shell | Spanish translation composes Google added/updated/renamed text with a nested next-sync suffix. | [L53](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L53) |
| S17-15 | shell | German translation recognizes the nested download connection-failure message prefix. | [L55](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L55) |
| S17-16 | shell | titles kept as they are | [L56](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L56) |
| S17-17 | shell | unknown message stays English | [L57](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L57) |
| S17-18 | shell | values are escaped | [L59](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L59) |

## Direct assertions

- [L28](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_17.py#L28): `r.status_code == 204` — language-setting request succeeds before the translated page checks.

## Coverage limits and reconciliation notes

- Five assertions inside the language loop produce repeated checks for es/fr/de/pt/nl; the table records call sites rather than expanding runtime repetitions.
- The page translation check samples fixed English phrases and a month title; it does not prove every visible string is translated. Activity checks sample recent logs.
- Row 18 only checks that the literal `<script>` is absent from one interpolated translation; it is not exhaustive HTML/JS injection coverage.
- Row 12 covers pt-BR on the public subscription page separately from the main-page loop.
- Default CI/harness runs must not be reported as executing this suite unless the invocation includes it explicitly (normally Deploy/all).
