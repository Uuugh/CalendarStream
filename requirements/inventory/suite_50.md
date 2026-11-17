# Suite 50: Deletion wording and release scan source

Source: [`tests/suite_50.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_50.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; seed.demo; loops patched. After two page assertions, the test reads release.yml as text to inspect gate ordering and selected configuration strings. It does not execute a scan or release.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S50-01 | google | The nonempty module-removal question set omits the Flying phrase with an extra article and includes the delete-Flying wording. | [L33](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_50.py#L33) |
| S50-02 | calendar | The sampled deleted event's rendered block has a deletion note and no Edited here text. | [L41](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_50.py#L41) |
| S50-03 | process | Release workflow source places trivy gate before beta tag movement and before the Build and push image step text. | [L46](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_50.py#L46) |
| S50-04 | process | Workflow source has a commit-pinned trivy-action and the sampled High/Critical, ignore-unfixed and error/exit strings in the gate suffix. | [L48](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_50.py#L48) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Workflow checks inspect string positions and suffix text, not parsed YAML execution/control flow. They do not prove the actual scan ran on the published artifact, handled both architectures or blocked a release. Row 04 does not establish that only the named severities can stop every workflow path.
- Row 02 checks the existence of a deletion note and absence of Edited here, not its exact origin text. Row 01 checks the sampled module question set, not every calendar name.
- Overlaps: suite 44 deleted styling; suite 49 source/remote deletions. Process ownership for workflow assertions is provisional and not an application requirement ID.
