# Suite 25: Admin email, password markup and update status

Source: [`tests/suite_25.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; empty environment public address. Background loops patched; a fixture Google client is saved directly. Admin-email requests and a direct frequency change exercise the rendered guide/settings page.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S25-01 | google | The page contains neither the adminemail field ID nor the Admin e-mail label. | [L19](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L19) |
| S25-02 | google | With no saved admin email, the guide includes support e-mail: your Gmail. | [L20](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L20) |
| S25-03 | settings | The admin-email route returns HTTP 400 for four sampled malformed addresses. | [L23](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L23) |
| S25-04 | settings | Saving a space-padded fixture email returns HTTP 303 and retrieves the trimmed address. | [L24](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L24) |
| S25-05 | google | The guide contains the saved fixture email inside code tags at least three times. | [L27](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L27) |
| S25-06 | google | The guide substring contains no escaped opening code tag (&lt;code&gt;). | [L28](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L28) |
| S25-07 | settings | Submitting an empty admin email clears the effective address. | [L30](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L30) |
| S25-08 | shell | The page has two inputs marked data-strength, omits _pwfield and includes the level(pw, min) script definition. | [L31](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L31) |
| S25-09 | shell | The rendered page contains Show password text. | [L32](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L32) |
| S25-10 | settings | The page shows Stable versions, Not checked and Next check @ update text. | [L33](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L33) |
| S25-11 | settings | After setting update frequency to never, the page says Automatic checks are off. | [L36](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L36) |
| S25-12 | settings | With an empty environment public URL, the import marker is true and the effective address is empty. | [L37](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_25.py#L37) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Row 03 is one call site looping over four invalid email samples; it is not exhaustive email validation.
- Row 05 counts at least three occurrences of the saved email rather than proving which individual guide roles each occurrence serves.
- Rows 08 and 09 inspect HTML/script strings, not actual strength-bar calculations or eye-toggle behavior. Row 06 checks one escaped-tag spelling rather than general escaping safety.
- The admin-email field is absent from UI while its route is exercised; inventory keeps these separate observations rather than declaring the setting removed.
- Overlaps: suite 22 update state/frequency; suite 15 public-address import; suite 24 guide markup; suite 19 password UI.
