# Suite 55: Google refusals, unlock cookies, opening tabs and emoji

Source: [`tests/suite_55.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8125; Demo.ics; patched loops/API readiness. Mock color refusals, revoked refresh tokens and forced global/per-address lockout states drive HTTP checks. Browser at 1230×900 routes cs.test through the authenticated client and stubs Google Calendar navigation. Temporary test cookies/unlock links and fixture credentials only.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S55-01 | google | A newly created remote calendar has shown=false and the module includes its Google-open action URL. | [L56](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L56) |
| S55-02 | google | The Google-open page returns 200 and includes Making the calendar plus its module name. | [L60](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L60) |
| S55-03 | google | While sync is pending, its check endpoint returns an empty JSON object. | [L61](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L61) |
| S55-04 | google | After sync, the check endpoint returns the exact Google Calendar URL selecting the fixture account. | [L65](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L65) |
| S55-05 | google | That URL omits cid and the waiting page omits Add calendar text. | [L67](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L67) |
| S55-06 | google | After marking shown, the module omits the Google-open action attribute. | [L68](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L68) |
| S55-07 | google | Opening the Google-page route for a plain feed returns 404. | [L70](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L70) |
| S55-08 | google | An old calendar record with shown=None does not render the open action. | [L72](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L72) |
| S55-09 | google | Before a refused color, the Google module has no palette note. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L76) |
| S55-10 | feeds | The plain feed module has no palette note. | [L77](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L77) |
| S55-11 | google | The sync succeeds when the mock refuses a color change. | [L83](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L83) |
| S55-12 | history | Recent color-failure text includes the sampled PATCH endpoint, HTTP 401/authError and both upstream reason strings. | [L86](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L86) |
| S55-13 | google | Recent logs omit the generic lost-sign-in message and the module has no last_error. | [L89](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L89) |
| S55-14 | google | Mock color request counts stay within four PATCH and two PUT calls. | [L91](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L91) |
| S55-15 | google | The refused-color module renders the Color change does not carry to Google palette note. | [L94](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L94) |
| S55-16 | google | Failure sentinel: a fresh-token color setter unexpectedly succeeding fails. | [L98](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L98) |
| S55-17 | google | Failure sentinel: treating that color refusal as AccessRevoked fails. | [L100](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L100) |
| S55-18 | google | The expected GoogleError contains refused wording. | [L102](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L102) |
| S55-19 | google | With a fresh token, the recorded color attempts are exactly two PATCH and one PUT. | [L103](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L103) |
| S55-20 | google | Syncing again after the same refused color sends no calendar-list PATCH. | [L108](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L108) |
| S55-21 | google | Clearing the older color-try marker causes a further PATCH attempt. | [L112](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L112) |
| S55-22 | google | Failure sentinel: API access with all refresh tokens revoked unexpectedly succeeding fails. | [L117](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L117) |
| S55-23 | google | Actual revoked sign-in raises AccessRevoked with Connect again guidance. | [L119](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L119) |
| S55-24 | account | A successful login returns 303 and sets the known-browser cookie. | [L126](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L126) |
| S55-25 | account | The issued known-browser cookie is accepted by the known_browser verifier. | [L128](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L128) |
| S55-26 | account | Replacing its signature with the sampled forged value is rejected. | [L129](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L129) |
| S55-27 | account | Triggering the global limit writes a warning containing an unlock path and within-an-hour guidance. | [L135](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L135) |
| S55-28 | history | Recent History tells the user to find the recovery link in the container log within an hour. | [L136](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L136) |
| S55-29 | account | A new browser's login returns 429 under that block. | [L138](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L138) |
| S55-30 | account | A browser carrying the known cookie can log in with 303 under the global block. | [L140](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L140) |
| S55-31 | account | Adding a per-address block makes that known browser's login return 429. | [L142](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L142) |
| S55-32 | account | The generated unlock link starts with the configured public address and unlock route. | [L145](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L145) |
| S55-33 | account | Visiting the fresh unlock link redirects 303 to login and gives that browser a known cookie. | [L149](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L149) |
| S55-34 | account | That newly known browser can then log in with 303. | [L151](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L151) |
| S55-35 | account | A second visit to the consumed unlock link returns 404. | [L152](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L152) |
| S55-36 | account | Setting the unlock expiration one second into the past makes it return 404. | [L154](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L154) |
| S55-37 | shell | The sampled newer emoji has a compatibility marker while the two sampled older emoji do not. | [L161](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L161) |
| S55-38 | google | Clicking the module Sync Now opens a new tab at the waiting Google-open page. | [L183](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L183) |
| S55-39 | account | That new tab has no window.opener reference. | [L184](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L184) |
| S55-40 | google | After mock sync, the tab navigates to the Google Calendar path. | [L188](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L188) |
| S55-41 | shell | In the searched emoji grid, both newer/older groups exist and only the newer group carries the older-Windows tooltip. | [L195](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L195) |
| S55-42 | shell | The newer emoji's after pseudo-element has literal i content. | [L197](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L197) |
| S55-43 | shell | Typing the fixture flag shows the emoji compatibility warning. | [L202](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L202) |
| S55-44 | shell | Clicking that warning opens its tooltip with older-Windows guidance. | [L204](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L204) |
| S55-45 | shell | Typing the older airplane emoji hides the warning. | [L206](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L206) |
| S55-46 | shell | Typing the newer face emoji shows the warning. | [L207](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L207) |
| S55-47 | shell | Picking an older emoji clears the warning and leaves a nonempty emoji field. | [L209](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L209) |
| S55-48 | shell | No pageerror events are collected in the sampled browser interactions. | [L210](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_55.py#L210) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 16/17 are deliberately failing success/wrong-exception branches; row 18 checks the expected GoogleError. Rows 22/23 pair revoked-call failure sentinel with AccessRevoked guidance.
- Counts in row 14 bound requests, not direct token-refresh count. Row 20 only excludes PATCH, whereas row 19 explicitly counts PATCH/PUT. Row 36 expires an unlock in the past; it does not prove the exact one-hour default duration.
- Known-browser behavior is tested under patched own-network handling and specific TestClient cookies/IP state, not every external network or browser.
- Browser navigation to Google Calendar is stubbed. No actual Google UI or real upstream credentials are used. Compatibility emoji checks sample selected code points and tooltip markers, not actual older-Windows rendering.
- The browser pageerror listener is on the main page, not independently on every new tab.
- Overlaps: suite 53 lockout; suite 56 color fallback; suite 47 update tabs/security; suite 44 emoji picker.
