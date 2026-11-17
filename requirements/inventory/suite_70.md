# Suite 70: GoogleApi dictionary-backed state and PKCE

Source: [`tests/suite_70.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

GoogleApi uses a simple dictionary store, fixture SecretBox password and synthetic account/client/URLs; no database, app server or network. Sign-in URLs/stored state are inspected, fresh objects simulate restart, and fake token requests provide synthetic JWT claims for audience checks.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S70-01 | google | A new API object with empty dictionary storage is unconfigured with an empty client tuple. | [L21](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L21) |
| S70-02 | google | Saving fixture client credentials makes it configured and retrieves the expected ID prefix/secret. | [L23](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L23) |
| S70-03 | google | Stored dictionary repr does not contain the fixture secret plaintext. | [L24](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L24) |
| S70-04 | google | Saving a blank secret retains the existing fixture secret. | [L26](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L26) |
| S70-05 | google | Failure sentinel: saving a malformed client ID without an exception fails. | [L28](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L28) |
| S70-06 | google | The malformed-ID attempt reaches a broad exception-handler success marker. | [L30](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L30) |
| S70-07 | google | A fresh account is unconnected with empty info. | [L31](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L31) |
| S70-08 | google | A second account shares configured client state but has distinct info/token storage keys. | [L33](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L33) |
| S70-09 | google | The sign-in URL uses S256/offline/expected client ID and stores one pending state. | [L35](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L35) |
| S70-10 | google | After creating more states than allowed, the stored pending map size is at most MAX_PENDING. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L38) |
| S70-11 | google | The new state belongs only to its account and its stored record has a verifier representation. | [L42](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L42) |
| S70-12 | google | The sign-in-map repr omits the sampled calendarstream string and the URL challenge is absent from stored verifier repr. | [L43](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L43) |
| S70-13 | google | A newly constructed API object using the same store recognizes the pending state. | [L46](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L46) |
| S70-14 | google | Taking that state once succeeds; taking it again returns None and ownership becomes false. | [L47](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L47) |
| S70-15 | google | Setting expiry into the past prevents ownership and taking the state. | [L50](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L50) |
| S70-16 | google | The first account cannot take a state belonging to the second account. | [L52](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L52) |
| S70-17 | google | Failure sentinel: finishing an unknown state without an exception fails. | [L54](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L54) |
| S70-18 | google | The unknown-state exception contains expired-or-already-used guidance. | [L56](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L56) |
| S70-19 | google | Across three fake ID-token audiences, email is accepted only for the matching client audience. | [L68](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L68) |
| S70-20 | google | The facade Google class directly inherits GoogleApi. | [L69](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L69) |
| S70-21 | google | An AUTH_URL assigned on gsync is used by a new facade object. | [L71](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_70.py#L71) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Secret-storage row 03 checks absence of fixture plaintext in repr, not cryptographic algorithm/security. Row 12 excludes a string and the public challenge from verifier repr; that is weaker than independently proving decrypted verifier equality/encryption strength.
- Rows 05/06 use broad exception sentinel/handler; row 06 alone cannot verify a requirement. Rows 17/18 pair unknown-state failure sentinel with an error-message check.
- Restart simulation constructs a new object sharing an in-memory dictionary, not a real process/database restart. Expiry is set into the past rather than testing a precise lifetime.
- Audience row 19 repeats missing/other/matching aud cases with fake token requests and synthetically encoded claims. It does not verify JWT signatures or all OIDC claims.
- Overlaps: suite 51 invite-state storage; suite 48 real mock consent; suite 69 shared error identity.
