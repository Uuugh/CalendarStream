# Suite 15: Public address settings

Source: [`tests/suite_15.py`](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py) at `87eadf4fa0f586889473a2598031d9e4bbe71a10`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; TestClient; background loops patched. Requires a second argument: an initial PUBLIC_URL or an empty string. The default harness runs both variants.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S15-01 | settings | On initial import, a nonempty environment public address is stored and displayed without PUBLIC_URL in Settings. | [L16](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L16) |
| S15-02 | settings | Without a public address, the page says Not set yet and points to Settings Public address. | [L18](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L18) |
| S15-03 | settings | bare host → https://, slash dropped | [L21](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L21) |
| S15-04 | settings | links and redirect URI use it | [L23](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L23) |
| S15-05 | settings | After saving an address, Settings omits PUBLIC_URL and the Public address section has no unset warning. | [L24](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L24) |
| S15-06 | settings | Reject FTP, a query-bearing URL, embedded credentials and a non-URL with HTTP 400. | [L26](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L26) |
| S15-07 | settings | needs CSRF | [L27](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L27) |
| S15-08 | settings | Saving an empty public address removes the stored value and makes public_url empty. | [L29](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L29) |
| S15-09 | settings | F6.1: .env isn't imported again after it was removed | [L31](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L31) |
| S15-10 | settings | subscribe page warning | [L33](https://github.com/Uuugh/CalendarStream/blob/87eadf4fa0f586889473a2598031d9e4bbe71a10/tests/suite_15.py#L33) |

## Coverage limits and reconciliation notes

- Row 01 runs with a nonempty environment address; row 02 with an empty one. A complete inventory includes both branches.
- Row 06 is one call site iterating four invalid inputs. It is not a claim of exhaustive URL validation.
- Row 09 explicitly calls import again after removal and checks the stored setting remains empty; it does not restart the process.
- Overlaps: suite 20 channel address changes; suite 19 Domains control placement.
