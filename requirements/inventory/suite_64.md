# Suite 64: Calendar modes, generated PDFs and Settings

Source: [`tests/suite_64.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; seed.demo; patched source/Google/update loops. Chromium renders print HTML to actual in-memory PDF bytes, read with pypdf for page counts/orientation. Letter/A4 are requested. Upload tests use synthetic PNG-shaped bytes, malformed favicon bytes and a scripted SVG, not user images.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S64-01 | calendar | Page markup includes view and clock controls and omits the old viewseg marker. | [L35](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L35) |
| S64-02 | calendar | The legend contains separate calendar and key part classes. | [L36](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L36) |
| S64-03 | calendar | After selecting week/day, the sampled page contains hourview markup. | [L39](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L39) |
| S64-04 | calendar | Saving full mode returns an allowed success status and the page has calfull class. | [L42](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L42) |
| S64-05 | calendar | Setting hidden edited while full mode is on stores the edited hidden set. | [L43](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L43) |
| S64-06 | calendar | Requesting stretch 1500 leaves stored stretch at most 1200. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L44) |
| S64-07 | calendar | Leaving full mode preserves the hidden set and removes calfull markup. | [L45](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L45) |
| S64-08 | calendar | For Letter/A4 month PDFs, one landscape page is produced and no sampled day cell overflows vertically. | [L60](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L60) |
| S64-09 | calendar | For Letter/A4 day PDFs, the first page is portrait and no sampled cell overflows vertically. | [L62](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L62) |
| S64-10 | calendar | The Letter week PDF has at least two pages and no sampled cell vertical overflow. | [L63](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L63) |
| S64-11 | account / settings | Settings has separate login/domain forms, no old public-url action and Signed in/Sign out text. | [L66](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L66) |
| S64-12 | settings | Saving Domains alone returns 303 and stores the sampled extra address. | [L68](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L68) |
| S64-13 | settings | Invalid main address returns 400 naming main as a field. | [L71](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L71) |
| S64-14 | account | Changing username with a wrong current password returns 400 naming current and leaves the saved username unchanged. | [L73](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L73) |
| S64-15 | settings | Before upload, the custom logo endpoint returns 404. | [L76](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L76) |
| S64-16 | settings | Uploading the PNG-shaped fixture returns 303, serves image/png and includes the brand URL in page markup. | [L78](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L78) |
| S64-17 | settings | Uploading nonpicture favicon bytes returns 400 naming favicon. | [L80](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L80) |
| S64-18 | settings | Uploading the sampled script-bearing SVG returns 400. | [L82](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L82) |
| S64-19 | settings | Saving animation 150/50 makes page markup include intensity 1.5 and duration 0.5 variables. | [L83](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L83) |
| S64-20 | settings | Reset/removing logo clears animation overrides and makes the brand endpoint return 404. | [L85](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L85) |
| S64-21 | settings | Saving intensity 500 returns 400. | [L86](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_64.py#L86) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Full-page HTTP checks assert a class, not absence/visibility of each other section. The hidden-set check uses one fixture entry; stretch checks only an upper bound, not exact capped value or negative inputs.
- Month/day PDF rows repeat for requested Letter/A4. They check page orientation/count and DOM vertical overflow; actual paper dimensions and complete visual fidelity are not independently asserted. Week only requires at least two pages, not one page per week exactly.
- The PNG-shaped fixture is not a realistic decoded image. SVG rejection tests one script case, not exhaustive upload safety. Row 11 checks separate forms/text, not physical Signed in/Sign out layout.
- Overlaps: suite 65 portrait printing/full-page browser; suite 67 Settings order; suite 59 color/header UI.
