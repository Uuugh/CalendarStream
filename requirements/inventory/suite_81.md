# Suite 81: Full-page Settings and live auto-update state

Source: [`tests/suite_81.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8097; seed.demo; loops patched; updater readiness forced true. Chromium at 1400×900 exercises navigation and real DOM relocation. A separate HTTP client simulates another browser changing auto-update; a route interception rejects a save. A second browser page emulates reduced motion.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S81-01 | settings | Full-page Settings navigation is visible while the login setting popup is not visible. | [L38](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L38) |
| S81-02 | settings | Choosing Sources Configure opens the shared popup. | [L43](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L43) |
| S81-03 | sources | The shared Configure body contains the actual Sources section node. | [L44](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L44) |
| S81-04 | settings | Opening Configure hides Settings navigation. | [L45](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L45) |
| S81-05 | sources | Back restores Sources to a parent with the previously recorded class name. | [L47](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L47) |
| S81-06 | settings | Back from Configure makes navigation visible again. | [L48](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L48) |
| S81-07 | account | Choosing Login opens its own setting dialog. | [L52](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L52) |
| S81-08 | account | That dialog contains a visible username field. | [L53](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L53) |
| S81-09 | settings | After an HTTP client changes auto-update, reopening Settings/Updates changes the browser checkbox from its earlier value. | [L66](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L66) |
| S81-10 | settings | Intercepting an auto-update save with 400 makes the checkbox revert to its prior value. | [L75](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L75) |
| S81-11 | shell | All sampled navigation-item and settings Back nodes are BUTTON elements. | [L80](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L80) |
| S81-12 | shell | Under emulated reduced motion, the slide-out computed animationName is none. | [L85](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L85) |
| S81-13 | shell | No main-page pageerror events are collected during the sampled interactions. | [L89](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_81.py#L89) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Restoring Sources is checked via parent class name rather than original DOM node/parent identity. No drag/reorder functionality is tested.
- Auto-update cross-browser state is simulated with a separate HTTP client. Changed boolean is asserted rather than exact server value, while rejection explicitly checks reversion. Rejection is intercepted rather than caused by a server validation case.
- BUTTON-tag checks can pass on an empty set and do not directly exercise Enter/Space, focus visibility or tab order. Reduced-motion animation is measured on a second page; its errors are not added to the first page's error collection.
- The final error row watches pageerror, not console errors despite its label. Only desktop/default-palette Settings paths are covered.
- Overlaps: suite 80 markup; suite 67 actual nested-dialog/Settings state.
