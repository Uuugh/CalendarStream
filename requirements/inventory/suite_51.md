# Suite 51: Feed add flow and Google invitations

Source: [`tests/suite_51.py`](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py) at `8e0e71757323d773cd7f2ec3b9e0671381302973`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; HTTPS TestClient; mock Google 8122; Demo.ics; loops patched. API readiness is patched true for later Google scenarios. Separate anonymous TestClient handles invitation forms/callbacks. Chromium 1230×900 routes cs.test requests through the authenticated TestClient for add-flow/field/rule layout checks. Only fixture accounts/tokens are used.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S51-01 | google | With API off, both Google picker choices are disabled and the page explains the admin setup requirement. | [L49](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L49) |
| S51-02 | google | The information table has off-class Google 2-way Sync markup. | [L51](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L51) |
| S51-03 | google | Adding a Google module while API is off returns 400 and creates no named destination. | [L53](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L53) |
| S51-04 | google | The page omits adminmail, Admin e-mail and the administrator-email route text. | [L54](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L54) |
| S51-05 | feeds | The first add step has three module choices and no Label or old every-source note. | [L59](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L59) |
| S51-06 | feeds | The second step has label/note/stream/source/start fields and no status box, Configure line or Remove text. | [L62](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L62) |
| S51-07 | feeds | Adding the Crew feed returns 303 and retains its source list, start date and note. | [L66](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L66) |
| S51-08 | feeds | Adding legacy gfeed type yields an ordinary feed destination. | [L69](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L69) |
| S51-09 | feeds | Pasting an old full feed URL on creation extracts its original stream token. | [L71](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L71) |
| S51-10 | feeds | Reusing that token returns 400 with X-CS-Fields=stream and creates no duplicate named destination. | [L73](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L73) |
| S51-11 | feeds | Updating with a malformed stream returns 400 naming stream as the field. | [L76](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L76) |
| S51-12 | feeds | Updating with the valid stream returns 303 and persists the token. | [L78](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L78) |
| S51-13 | feeds | An end before the start returns 400 naming end as the field. | [L80](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L80) |
| S51-14 | settings | An invalid second extra address returns 400 naming url1 as the field. | [L84](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L84) |
| S51-15 | settings | Saving one valid extra address plus an empty one stores only the valid address. | [L86](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L86) |
| S51-16 | feeds | The selected extra base address appears in its dropdown with an Add a domain option. | [L91](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L91) |
| S51-17 | feeds | The sampled feed link markup includes the chosen base and stream in plain or encoded form. | [L93](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L93) |
| S51-18 | feeds | Requesting the new stream URL returns 200. | [L95](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L95) |
| S51-19 | feeds | The module has Outlook add-from-web, Google/Apple/Send controls and no Open subscribe page text. | [L96](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L96) |
| S51-20 | feeds | Module markup orders Feed link, Account, Include, Cancel and Information. | [L98](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L98) |
| S51-21 | feeds | The editable optional-note field is in markup before the right-header section. | [L100](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L100) |
| S51-22 | google | The initial mock account is connected. | [L109](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L109) |
| S51-23 | google | When api_on is patched true, Google module options are no longer disabled. | [L112](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L112) |
| S51-24 | google | A new one-way Google module returns 303, has its own account ID and is not connected. | [L116](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L116) |
| S51-25 | google | A sync creates no additional mock calendars or first-account mapping for that unconnected module. | [L119](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L119) |
| S51-26 | google | Its page offers connect/invite choices with no account specified and no first email in the sampled substring. | [L123](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L123) |
| S51-27 | google | Creating an invite produces a token link and page text for single-use expiry and Invited status. | [L130](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L130) |
| S51-28 | google | Anonymous invite GET returns 200 with module name, Continue with Google and a hex form token. | [L135](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L135) |
| S51-29 | account | The anonymous root-page response does not expose the destinations section. | [L136](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L136) |
| S51-30 | google | Invite POST with the sampled wrong form token returns 400. | [L138](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L138) |
| S51-31 | google | Invite POST with its form token redirects 303 to the mock authorization URL. | [L140](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L140) |
| S51-32 | google | The resulting OAuth state exists in both stored invite-state and sign-in maps. | [L143](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L143) |
| S51-33 | google | After callback, that state is absent from both maps. | [L149](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L149) |
| S51-34 | google | The callback response is 200/Done and the module is connected as the invited fixture account. | [L151](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L151) |
| S51-35 | google | The module's remote calendar exists and belongs to the invitee fixture account. | [L153](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L153) |
| S51-36 | google | The initial account's email and connected state remain unchanged. | [L154](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L154) |
| S51-37 | google | Reusing the consumed invite link returns 404. | [L155](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L155) |
| S51-38 | google | A second module's fresh invite link returns 200. | [L161](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L161) |
| S51-39 | google | Withdrawing that invite makes the link return 404. | [L163](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L163) |
| S51-40 | google | Setting the invite expiry to one second before now makes it return 404. | [L167](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L167) |
| S51-41 | google | The sampled invented token returns 404. | [L168](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L168) |
| S51-42 | google | Inviting a module on the first account preserves its current assignment and stores old/new account identities in the pending invite. | [L175](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L175) |
| S51-43 | google | Withdrawing that pending invite leaves the module on the first account. | [L178](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L178) |
| S51-44 | google | Adding a module with Connect me redirects 303 directly to mock authorization. | [L183](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L183) |
| S51-45 | google | After consent the new module is connected with the first fixture email. | [L186](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L186) |
| S51-46 | google | Removing that same-email module removes it without revoking its token and leaves the first account connected. | [L189](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L189) |
| S51-47 | google | After removing the separate invitee module, the mock revoked-token set is nonempty. | [L192](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L192) |
| S51-48 | google / feeds | Browser add step shows the feed option and enables Google module selection while API setup is on. | [L207](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L207) |
| S51-49 | feeds | Choosing Feed closes step one and opens step two with Calendar Feed kind, hidden Google account panel and feed type. | [L213](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L213) |
| S51-50 | feeds | A rejected stream field gets needsfix class and 2px outline width. | [L219](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L219) |
| S51-51 | feeds | Editing that stream field clears needsfix class. | [L221](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L221) |
| S51-52 | feeds | Saving a valid browser feed persists its name/token and closes the second-step dialog. | [L223](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L223) |
| S51-53 | feeds | The feed copy control lies horizontally after .ics and within the feed field's right boundary. | [L233](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L233) |
| S51-54 | feeds | All four app-link buttons have equal measured dimensions. | [L234](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L234) |
| S51-55 | feeds | Send to opens visible mailto and sms links. | [L236](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L236) |
| S51-56 | rules | The action-add control starts at or outside the sampled action-box right padding boundary. | [L252](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L252) |
| S51-57 | rules | All measured action-delete controls share one rounded right-edge coordinate. | [L253](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L253) |
| S51-58 | rules | The create-event action has four groups and no measured group is taller than 40px. | [L254](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L254) |
| S51-59 | shell | No browser pageerror events are collected during the sampled interactions. | [L255](https://github.com/Uuugh/CalendarStream/blob/8e0e71757323d773cd7f2ec3b9e0671381302973/tests/suite_51.py#L255) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Invite state persistence is checked by reading stored maps, not restarting the app. Row 40 sets expiry to the past; it does not prove the exact seven-day lifetime claimed in its old label.
- Row 47 checks a nonempty revoked set without tying the exact newly revoked token to that module. Row 46 is stronger for the shared-account case, checking the saved token is not revoked.
- Row 29 only checks destinations markup is absent on an anonymous response, not its exact redirect/auth status. Expired/used/withdrawn/invented links each sample one token.
- Row 16 checks selected and Add-domain options, not every configured address. Row 20 is source ordering rather than physical layout; row 21's edit class/placeholder is not a direct rendered header measurement.
- Row 50 asserts 2px outline width but not the amber color. Row 53 checks horizontal bounds only. Row 55 exposes mailto/sms choices; it does not send messages.
- Row 58 uses group count/heights, not exact line-wrap detection. Browser requests are fulfilled via an authenticated TestClient, so browser interactions do not independently verify authentication.
- Overlaps: suites 26/39 feed add/API gating; suite 48 client/account lifecycle; suite 49 multi-account removal; suite 44 rule-dialog layout.
