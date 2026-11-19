# Oracle coverage notes (temporary)

Moved out of the feature files on Nov 19 so those files speak for themselves. Each section lists the Python-suite evidence rows that were excluded from a feature (not requirements, or owned by another feature) and what was still open. The IDs inside are the old IDs (see `requirements/oldkey.md`). Delete this file with the evidence column when the conversion ends.

## account.md


### Not requirements

The following observations are excluded or mapped to another owner rather than duplicated.

- S16-02: Legacy CCS+ credential import and its activity record are owned by sources (SRC-03), not a second account requirement.
- S16-03: Legacy CCS+ credential import and its activity record are owned by sources (SRC-03), not a second account requirement.
- S16-19: Environment-specific performance sample for five authenticated requests; does not establish a portable latency requirement.
- S21-11: Field alignment is a theme measurement; User name wording is a shared field-label observation, not a separate login capability.
- S35-09: Static parent-path request rejection belongs to shared asset-serving security; one sampled path does not establish the complete traversal policy.
- S39-09: Authenticated-page compression header policy belongs to shared HTTP security, not credential behavior; retained for shared review.
- S55-39: No window.opener in a new tab is shared external-navigation security, not an account-specific rule.
- S63-09: Failure sentinel and unconditional exception-handler success marker; not independent password validation evidence.
- S63-10: Failure sentinel and unconditional exception-handler success marker; not independent password validation evidence.
- S64-11: Settings form structure and signed-in/out wording are mapped to existing SET-01 and account signed-in state above, not duplicated UI mechanics.
- S65-24: Icon variables and CSS-selector source checks are Python presentation implementation details.
- S65-25: Icon variables and CSS-selector source checks are Python presentation implementation details.
- S81-07: Settings dialog navigation and field visibility are shared mechanics (SET-01, UI-01/UI-02), not new account behavior.
- S81-08: Settings dialog navigation and field visibility are shared mechanics (SET-01, UI-01/UI-02), not new account behavior.

### Coverage and open questions

All 81 account-candidate rows are accounted for in 27 proposed requirements and
14 excluded/shared-owner mappings. The exact block budget, reset interval, trusted-address
policy and expiry boundary remain questions; finite security samples are not comprehensive audits.
No real credentials or schedules are included. No application suites were run locally.

## calendar.md


### Shared UI and owning-feature references

These are evidence mappings, not duplicate CAL requirements. Shared behavior is defined once in
[common.md](common.md); event behavior is owned by [events.md](events.md) and the existing
[events requirements](../events.md). Removed draft IDs remain reserved for review continuity.

- Former CAL-16: S18-19, S18-20, S18-21 → UI-01 and UI-02 (event details/dialog lifetime). The click-outside persistence observation is retained as an open shared-dialog question, rather than restated here.
- Former CAL-17: S18-22 → EVT-01 (new event for a selected day).
- Former CAL-18: S18-18 → UI-02 (Close), EVT-03 (reminders) and EVT-01 (Add event). Old pin replacement is presentation history.
- Former CAL-28: S21-04 → UI-09 (date selection). Outside-click dismissal is an open shared-picker question; it is not a second calendar rule.
- Former CAL-29: S21-06, S21-22, S64-02 → UI-07 (explanatory help). Calendar/Key grouping is presentation; no new help mechanic is defined here.
- Former CAL-31: S26-57, S39-20 → Events owns event tools; see EVT-04 and UI-02. Editor/Delete availability evidence is retained for its review.
- Former CAL-32: S39-21 → Events owns generated-event tools; see EVT-01. Copy-only availability is retained as an events coverage question, not duplicated here.
- Former CAL-44: S37-16 → EVT-05 (saved event link).
- Former CAL-46: S44-42, S45-21, S50-02, S65-07 → EVT-01 and EVT-01 (deletion/restoration). The imported-event tombstone/deletion-note observations remain evidence for events reconciliation; these references do not claim those drafts already specify every detail.
- Former CAL-52: S57-32, S57-39 → Existing planned EVT-06 (event printing); UI-01 and UI-02 govern dialog layers. No implementation or approval status is inferred.
- Former CAL-64: S67-36, S67-37, S67-39 → Shared menu mechanics. Open/choose/dismiss evidence is retained for shared UI review; UI-02 covers layer dismissal, but a general menu rule is still an open shared-UI question.

Other shared-UI observations retained in the table evidence (not separate calendar rules): CAL-22’s
switch/tooltip mechanics, CAL-27’s selection mechanics, CAL-49’s keyboard focus, and CAL-53/CAL-56’s
pressed-state mechanics belong to shared UI. CAL-58 retains only height adjustment, not the widget type.
Shared UI does not yet explicitly state every one of these mechanics; Claude can reconcile them in its
shared-UI ownership review. This PR changes only calendar.md, as scoped by the Developer.

### Not requirements

These rows are accounted for but do not independently establish a user-facing requirement.
Pure geometry and appearance decisions belong to `build_rules/theme.md`.

- S34-05: Print-button/CSS media-block presence only; does not execute printing.
- S34-06: Computed color equality is a theme assertion.
- S39-12: Python event-tool template/placeholder structure, not an exercised user action.
- S44-25: Pixel alignment belongs to theme rules; presence of a Link tool is also observed, but this compound geometry row does not exercise linking.
- S44-44: Today-cell shadow thickness is a theme measurement.
- S45-24: Class/color-variable implementation check; it does not compare rendered user behavior.
- S46-11: Control offsets and alignment are theme measurements.
- S46-27: Event-control rectangle alignment is a theme measurement.
- S58-26: Padding and icon inset are theme measurements.
- S62-14: Source-string checks for hide/deletion labels do not execute behavior.
- S65-11: Absence of an ID in a page substring is an implementation-placement check.
- S65-17: CSS source declarations, not runtime behavior.
- S65-30: Viewport scroll dimensions are layout measurements.
- S65-31: Calendar width threshold is a layout measurement.
- S65-38: Rounded icon top-coordinate spread is a layout measurement.
- S66-24: Touch handler strings in source do not prove swipe behavior.
- S67-34: Control IDs and absence of an obsolete native picker are implementation structure.
- S67-38: Icon x-coordinate equality is a layout measurement.
- S67-51: Legend separator gap is a pixel measurement.
- S79-03: Grip-dot class and circle count specify visual implementation.
- S79-04: Element type and obsolete spelling are implementation structure.
- S79-05: Absent CSS selector spelling does not prove grip independence.
- S79-09: Absent obsolete control ID is implementation structure.

### Coverage and remaining questions

All 131 calendar-candidate inventory rows are accounted for in 38 proposed requirements,
11 owning-feature/shared-UI reference groups, or the 23 exclusions above. This is static evidence reconciliation; no suites were run locally.
Related event editing, source configuration and publishing behaviors remain with their owning feature drafts.
The questions in proposed rows require review; existing CAL-07/CAL-08 disagree about leaving Full page,
and the draft preserves the later asserted persistence rather than silently approving either statement.

## events.md


Not requirements: source-text checks (S62-12, S62-16, S62-17, S65-01..03 partly, S66-19, S66-20, S77-22 failure
callback), `ok(True)`-style markers, and the layout rows listed in the header.

## feeds.md


### Not requirements

Each remaining row is mapped to shared ownership or excluded with its reason. These are not
additional feed requirements. Unspecified shared mechanics remain questions for shared-UI review.

- S18-23: Shared copy-control feedback and icon reset; owned by shared UI, not a separate feed rule. UI-01/UI-02 do not yet specify copy feedback; retained for shared-UI review.
- S18-24: Shared copy-control feedback and icon reset; owned by shared UI, not a separate feed rule. UI-01/UI-02 do not yet specify copy feedback; retained for shared-UI review.
- S21-21: Google sign-in placement belongs to settings/google; historical two-destination arrangement is not a separate feed behavior rule.
- S29-05: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S31-02: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S31-08: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S31-09: Field/control markup and section configuration mechanics; shared UI ownership (UI-05), with date input details retained for shared-control reconciliation.
- S35-13: Font and SVG-symbol markup are presentation/implementation, not subscription behavior.
- S38-16: Source-color change is owned by sources (SRC-01 in its pending draft); calendar-key effects are CAL-45. Source-picker color markup is not restated here.
- S39-15: Markup order is presentation, not a separate feed rule.
- S41-01: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S41-02: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-08: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-23: Single-destination handle visibility is shared reorder-control UI, not feed publishing behavior; retained as an open shared-UI mapping.
- S44-31: Shared modal/backdrop behavior: UI-01; visual filter belongs to theme.
- S44-37: Shared date-range input grouping rather than a separate feed rule; actual date filtering is specified above.
- S44-49: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-54: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-55: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-56: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S44-57: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S51-05: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-06: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-20: Markup order is presentation, not a separate feed rule.
- S51-21: Markup order is presentation, not a separate feed rule.
- S51-48: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-49: Shared multi-step add-dialog mechanics and choice-panel markup; UI-01/UI-02 cover dialog layers, while module-choice enabling belongs to google/settings.
- S51-50: Shared field-error styling/reset mechanics, not feed behavior. Invalid stream rejection is specified above; styling belongs to theme.
- S51-51: Shared field-error styling/reset mechanics, not feed behavior. Invalid stream rejection is specified above; styling belongs to theme.
- S51-53: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S51-54: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S55-10: Absence of a palette note is presentation, not a publishing guarantee.
- S58-16: Source metadata/label implementation; source naming and notes belong to sources (SRC-01).
- S58-39: Pixel geometry, alignment, dimensions and responsive columns belong to build_rules/theme.md.
- S59-07: Shared removal confirmation (UI-06); newline formatting belongs to presentation. The stopped-link consequence is specified above.
- S63-05: Source-string presence for URL/meeting notes does not establish executed publishing behavior.

### Coverage and open questions

All 93 feed-candidate evidence rows are accounted for in 30 proposed requirements and
36 excluded/shared-owner mappings. Questions in the table preserve uncertainty rather than
generalizing beyond the oracle. The complete stream character set, generated-token guarantee and
default-destination inclusion policy need review. No application suites were run locally.

## google.md


### Not requirements

Implementation-only observations, sentinels and shared-owner evidence are accounted for individually.
A reference identifies ownership; it does not assert that every shared mechanic is already approved.

- S12-05: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-11: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S12-12: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-13: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-14: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S12-16: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S12-23: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S12-32: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S12-38: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S12-40: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S13-04: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S13-05: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-21: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-26: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-32: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S13-33: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S14-14: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S18-10: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S19-21: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S20-06: History message observations; History owns recording outcomes (HIS-01..05 and its activity rules), while sync outcomes are specified above.
- S23-09: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S24-04: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S24-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S25-01: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S25-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S26-49: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S35-12: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S35-16: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S39-13: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S39-17: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S39-22: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S40-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S46-01: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S46-03: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S46-05: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S47-07: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S47-08: Pixel offsets belong to build_rules/theme.md.
- S48-06: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S50-01: Shared deletion-confirmation wording (UI-06), not another calendar-deletion rule.
- S51-02: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S51-04: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S51-23: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S51-30: Shared page-authentication/security-token checks; owned by shared/account security rather than duplicated per feature.
- S51-32: Internal sign-in/invite map bookkeeping; single-use consent/invite outcomes are specified above.
- S51-33: Internal sign-in/invite map bookkeeping; single-use consent/invite outcomes are specified above.
- S51-48: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-02: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-03: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-10: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-11: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S54-12: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S55-14: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S55-16: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S55-17: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S55-19: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S55-22: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S56-01: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S56-04: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S56-16: Exact HTTP-method counts, internal status-key shapes, color lookup-table size and saved method spellings are implementation contracts. User-visible publication/color fallback outcomes are specified above.
- S56-25: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S67-24: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S67-27: Setup/navigation/control markup and shared mechanics; UI-01/UI-02 govern shared dialog layers. Underlying connection/address outcomes are retained above; presentation is not a separate Google rule.
- S68-06: Setup endpoint result encoding; client configuration behavior is specified above.
- S69-01: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-02: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-03: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-04: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-05: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-06: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S69-07: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S69-08: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S69-09: Python exception/enum/dataclass/facade contracts, not user-facing requirements.
- S70-01: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S70-05: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S70-06: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S70-12: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S70-17: Failure sentinels or unconditional exception-handler success markers; not independent behavior verification.
- S70-20: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S70-21: Dictionary initialization, verifier representation and Python facade configuration contracts; not user-facing promises. The verifier predicate does not prove complete secrecy.
- S72-01: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-02: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-03: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-04: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-05: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-06: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S72-07: Classifier input-to-enum contracts; resulting recovery behavior is specified above, without exposing Python error taxonomy as user requirements.
- S73-12: Always-true or True predicate; cannot independently verify secret/token storage.
- S74-01: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-02: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-03: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-04: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-06: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-07: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-08: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S74-09: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S77-28: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S77-29: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.
- S77-30: Python facades/helpers/job defaults and override contracts; no independent user behavior. Stable ID samples do not establish a general collision guarantee.

### Coverage and open questions

All 400 Google-candidate rows are accounted for in 80 proposed requirements and
98 excluded/shared-owner mappings. Questions above preserve gaps in token protection, retry/renewal
thresholds, color/description handling and conflicting historical client/calendar recovery behavior.
Historical tests use finite samples and permissive predicates; they do not establish full OAuth validation,
exact production timing, or live-service availability. No application suites were run locally.

## history.md


### Not requirements

These rows remain accounted for without creating duplicate shared-UI or Python implementation requirements.

- S31-13: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S38-13: Shared section expansion behavior is owned by UI-05 in common.md.
- S38-14: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S49-55: Copy-control ID presence is implementation markup; the container-log retrieval outcome is specified above.
- S58-21: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S58-23: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S61-18: Activity widths, preview positioning/alignment and collapsed preview presentation belong to theme/shared section UI (UI-05), not a separate history rule.
- S65-06: Deleted-event storage marker belongs to events (EVT-01); its retention consequence for Undo is specified above.
- S66-10: Permissive accepted-check/icon markup predicate does not independently establish a history behavior.
- S66-11: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S66-12: ok(True) skip marker when the History table is absent; not independent verification.
- S66-13: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S66-14: Table column markup/order and draggable attributes are shared table presentation/implementation. These checks do not exercise sorting, dragging or a history state change.
- S67-04: Template source-string check (keep=False), not an executed user behavior.
- S67-10: Shared save acknowledgement/shrink/dismiss mechanics; shared UI owns feedback timing, not a separate history rule. See the common.md pending save/cancel ownership note and SET-01; these references do not claim the exact timings are already specified.
- S67-11: Shared save acknowledgement/shrink/dismiss mechanics; shared UI owns feedback timing, not a separate history rule. See the common.md pending save/cancel ownership note and SET-01; these references do not claim the exact timings are already specified.
- S67-12: Shared save acknowledgement/shrink/dismiss mechanics; shared UI owns feedback timing, not a separate history rule. See the common.md pending save/cancel ownership note and SET-01; these references do not claim the exact timings are already specified.
- S77-31: Injected record return value is a Python collaborator contract, not a user requirement.
- S77-34: Injected trimming callback count is an implementation contract; it does not independently prove a user-visible retention limit.

### Coverage and open questions

All 55 history-candidate rows are accounted for in 22 proposed requirements and
19 excluded/shared-owner mappings. Open questions above cover aggregate health, type vocabulary,
retention validation and snapshot scope; no broader guarantees are inferred from finite examples.
No application suites were run locally for this documentation-only draft.

## settings.md


### Not requirements

Evidence rows that belong elsewhere, by reason:

- **Belongs to theme.md (pixels, colors, dimensions):** S19-53, S21-10, S31-17, S38-19, S43-02, S44-20.
- **Settings grouping, headings and form markup (SET-06 owns organization):** S19-49, S19-52, S22-02, S37-24, S64-11, S66-06, S66-07, S66-08, S66-09, S67-29, S67-30, S67-31, S67-32.
- **Control state, callbacks and feedback reset (UI mechanics; the check and update outcomes are above):** S38-09, S40-07, S43-01, S43-03, S44-19, S46-04, S46-28, S47-06, S59-23.
- **Add/remove-row controls and notice dismissal (shared UI; UI-02 governs layers):** S67-19, S67-21, S67-23, S67-28.
- **Settings/Configure navigation and dialogs (SET-05, SET-06, UI-01, UI-02):** S80-01 to S80-11, S81-01, S81-02, S81-04, S81-06.
- **Shared security or validation:** S15-07 (change-security token, account security), S31-10 (section-key validation, shared UI).
- **Failure markers, not coverage:** S23-14, S23-15.
- **Saving persists the choice (SET-06, UI-13):** S38-17, S38-18.

### Coverage

All 165 settings-candidate evidence rows are in a requirement above or in the list above.

## shell.md


### Not requirements

The remaining evidence is retained individually for shared ownership, theme or implementation reconciliation.

- S14-01: Theme-choice order and menu open/close/icon mechanics belong to existing SHL-01 and shared menu UI; no second menu rule is created here.
- S18-13: Shared copy-button icon/count presentation, not a distinct shell capability.
- S21-25: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S25-08: Password-strength markup and Show password control belong to account/shared password-field UI; no behavior is inferred from script/marker presence.
- S25-09: Password-strength markup and Show password control belong to account/shared password-field UI; no behavior is inferred from script/marker presence.
- S28-15: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S31-11: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S31-14: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S31-15: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S32-12: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S33-26: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S34-02: Shared section affordance/label mechanics; see UI-05 and the existing Settings section rules.
- S34-03: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S34-07: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S34-08: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S34-24: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S35-01: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-02: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-03: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-04: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-05: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-06: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-11: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S35-15: Shared Cancel completion spelling/feedback, not a feature-specific outcome; shared save/cancel ownership remains with SET-01/shared UI.
- S35-20: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S35-21: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S35-24: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S35-25: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S35-26: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S35-27: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S35-37: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S35-38: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S36-45: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S36-54: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S36-58: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S37-27: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S37-53: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S38-02: Shared section affordance/label mechanics; see UI-05 and the existing Settings section rules.
- S38-20: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S39-23: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S40-08: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S40-12: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S41-03: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S41-04: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S42-08: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S43-10: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S44-01: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-02: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-03: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-04: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-05: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-06: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-07: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-09: Singleton drag-handle visibility is shared reorder-control presentation; does not establish reordering behavior.
- S44-10: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-12: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-13: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-14: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S44-21: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-22: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-24: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-33: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-35: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-36: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S44-39: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S44-40: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S44-46: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S44-47: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S44-48: Shared explanatory tooltip behavior belongs to UI-07 and layer dismissal UI-02; precise positioning remains theme evidence.
- S44-50: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-51: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-52: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S44-53: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S46-29: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S47-09: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S49-57: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S51-59: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S53-18: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S55-42: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S55-48: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S57-38: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S57-40: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S58-40: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S59-19: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S59-20: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S59-21: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S59-28: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S61-10: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S61-11: Shared section affordance/label mechanics; see UI-05 and the existing Settings section rules.
- S61-15: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S61-16: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S61-23: Shared status/section/palette/control presentation or wording checks; UI-05/UI-10 and shared status components own these, with timing/accessibility details retained for their review.
- S61-27: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S62-18: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S63-25: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S63-26: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S63-27: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S63-28: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S65-28: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S65-39: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.
- S66-22: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S66-23: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S66-25: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S66-26: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S66-27: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S66-28: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S67-01: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S67-02: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S67-03: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S67-05: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S67-43: Theme-choice order and menu open/close/icon mechanics belong to existing SHL-01 and shared menu UI; no second menu rule is created here.
- S67-44: Theme-choice order and menu open/close/icon mechanics belong to existing SHL-01 and shared menu UI; no second menu rule is created here.
- S67-45: Appearance, geometry, contrast or visual-token measurement belongs to build_rules/theme.md; do not promote its pixel/style predicate into another feature requirement.
- S67-46: Theme-choice order and menu open/close/icon mechanics belong to existing SHL-01 and shared menu UI; no second menu rule is created here.
- S67-48: Theme-choice order and menu open/close/icon mechanics belong to existing SHL-01 and shared menu UI; no second menu rule is created here.
- S67-56: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S67-57: Python template/CSS/script/icon/asset-path implementation check or sentinel; not independent executed user behavior. Asset-file organization does not specify the port’s layout.
- S81-11: Shared navigation element semantics and reduced-motion behavior, not separate shell feature mechanics. UI-01/UI-02 own navigation layers; reduced-motion detail remains for shared UI review.
- S81-12: Shared navigation element semantics and reduced-motion behavior, not separate shell feature mechanics. UI-01/UI-02 own navigation layers; reduced-motion detail remains for shared UI review.
- S81-13: No-error observation over finite browser interactions; quality evidence, not an independent user requirement or guarantee of every path.

### Coverage and open questions

All 170 shell-candidate rows are accounted for in 16 proposed requirements and
120 excluded/shared-owner mappings. Section vocabulary and exact remembered-open expiry remain
questions. Localization evidence samples messages and languages; it is not a claim that every string
is translated. No-error browser observations cover only their exercised paths. No application suites
were run locally for this draft.

## sources.md


### Not requirements

These mappings account for evidence without defining duplicate UI or implementation requirements.

- S14-02: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S14-03: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S16-21: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S19-24: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S21-12: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S21-24: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S23-27: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S26-13: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S27-07: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S28-02: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S28-03: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S28-04: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S31-12: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S31-16: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S33-04: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S33-20: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-09: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S34-10: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-11: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-12: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-14: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S34-19: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S34-20: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S34-21: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S34-22: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-19: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-22: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-23: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-30: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-33: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S35-34: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S35-35: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S35-36: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S37-28: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S37-29: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S37-30: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S37-31: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S37-32: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S37-48: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S37-49: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S41-01: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S41-02: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S44-08: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S44-29: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S44-30: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S44-31: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S44-34: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S44-43: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S49-03: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S49-20: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S53-17: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S60-01: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-02: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-03: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-04: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-06: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-07: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-08: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-09: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S60-20: Always-true predicate or deliberate failure sentinel, not independent behavior verification.
- S60-27: Transport selection, user-agent/debug or authorization implementation contract. No additional user-facing source rule inferred; transport/security outcomes are stated separately.
- S61-06: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S61-19: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-20: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-21: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-22: Shared save/cancel mechanics; see SET-01 in requirements/settings.md. Source outcome requirements above retain only persisted data and verification results.
- S61-28: Theme/layout/font/CSS measurement or implementation styling; belongs to build_rules/theme.md, not a source requirement.
- S63-19: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S63-29: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S66-02: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S66-03: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S66-05: Rendered control structure, wording history or shared control mechanics; no separate source-data rule. Generic sections/help belong to shared UI (UI-05/UI-07). These observations do not independently prove the labeled behavior.
- S77-19: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-20: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-21: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-26: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S77-27: Python source-string, injected-provider/logging or cached-version compatibility contract; not a user-facing source requirement.
- S81-03: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.
- S81-05: Shared dialog/navigation mechanics: see UI-01, UI-02 and UI-06 in common.md. Default merge selection/self-target disabling in S37-48 remains an open removal-flow detail for owner review.

### Coverage and open questions

All 227 source-candidate rows are accounted for: 60 proposed requirements and
79 excluded/shared-owner evidence mappings. No application suites were run locally.
Questions above preserve uncertainty about retention and automatic retries. The import conflict policy,
complete validation ranges and source-removal dialog defaults require Developer review beyond the finite
examples in the oracle; these drafts do not silently add broader guarantees.
