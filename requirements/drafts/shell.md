# DRAFT requirements: shell (for the Developer's review)

Not approved. Derived from all inventory rows whose candidate feature includes `shell`, at
`26453f66c45ae5b0a1ec2efe51b5125dbf4fdef1`. IDs continue after SHL-03 in `requirements/shell.md`.
Evidence keys refer to the pinned predicates, setup and limits in `requirements/inventory/suite_NN.md`.
No Developer approval or new runtime verification is inferred.

Shared widget mechanics remain in shared_ui.md or their existing owner, rather than being duplicated
here. Visual measurements belong to build_rules/theme.md. A shared-owner mapping is not a claim that
every detailed observation has already become an approved shared requirement. Claude owns the final
cross-feature duplication review; this file does not change the other drafts.

| ID | status | statement | evidence |
|---|---|---|---|
| SHL-04 | proposed | The initial page language is English; Automatic follows supported browser language preferences, including French, German and Belgian Dutch, while an unknown browser language falls back to English. Choosing Automatic clears the explicit language override. | S17-01, S17-02, S17-03, S17-04, S17-10 |
| SHL-05 | proposed | Choosing Spanish, French, German, Portuguese or Dutch translates the calendar month title, activity/status messages and event-editor heading, and identifies the page language. | S17-05, S17-06, S17-07, S17-08 |
| SHL-06 | proposed | Validation guidance follows the selected language, including the fifteen-to-1440-minute interval guidance; unknown language choices are refused. | S17-09, S17-11 |
| SHL-07 | proposed | The subscription page and Google setup-error guide follow the visitor’s supported browser language. | S17-12, S24-10 |
| SHL-08 | proposed | Translation supports composed and nested messages, including sync-change summaries and download-failure explanations, without translating user event titles. Unknown messages retain their original English wording. | S17-14, S17-15, S17-16, S17-17 |
| SHL-09 | proposed | Values inserted into translated messages are escaped rather than interpreted as markup. | S17-18 |
| SHL-10 | proposed | API-style requests retain structured JSON errors rather than receiving translated HTML pages. | S17-13 |
| SHL-11 | proposed | The displayed running version links to its corresponding release, including the full beta version identifier. | S29-01, S30-05, S61-08 |
| SHL-12 | proposed (?) | The page provides Calendar, Sources, Feeds/Destinations, Rules, Event Templates and Activity/History sections, with the Beta section after Activity. Historical source labels differ; which final section vocabulary should be canonical? | S26-63, S31-06, S31-07, S34-01 |
| SHL-13 | proposed | Page fonts are served locally, including the Mono font and its license, without depending on Google Fonts. Font appearance belongs to the theme. | S35-07, S35-08, S35-10, S35-18 |
| SHL-14 | proposed | Versioned stylesheet, language-script and font assets can be cached as immutable; an obsolete script version or unsupported script language is refused, while the unversioned font is not advertised as immutable. | S39-03, S39-04, S39-05, S39-06, S39-07, S39-08 |
| SHL-15 | proposed | Newer emoji display older-Windows compatibility guidance, while older compatible choices do not. Editing or choosing an older emoji clears the compatibility warning; choosing a newer one displays it. Shared explanatory help follows UI-07. | S55-37, S55-41, S55-43, S55-44, S55-45, S55-46, S55-47 |
| SHL-16 | proposed | The page identifies CalendarStream in its title and identifies the running release and copyright in the footer; the title does not embed a version link. | S61-07 |
| SHL-17 | proposed | The page provides a favicon and the checked light/dark logo assets. Existing SHL-02 owns the favicon’s appearance; asset existence does not establish artifact-free rendering under planned SHL-03. | S61-09 |
| SHL-18 | proposed (?) | An opened section remains open when freshly observed; an open section older than twenty-five hours is closed and its closed state saved independently of another recently opened section. What is the exact expiry rule rather than this tested point? | S61-13, S61-14 |
| SHL-19 | proposed | With no saved theme override, the page uses Match system; choosing Dark applies it and indicates it as the selected choice. Existing SHL-01 owns the theme-choice affordance. | S66-01, S67-47, S67-49 |

## Not requirements

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
- S35-15: Shared Cancel completion spelling/feedback, not a feature-specific outcome; shared save/cancel ownership remains with SET-07/shared UI.
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

## Coverage and open questions

All 170 shell-candidate rows are accounted for in 16 proposed requirements and
120 excluded/shared-owner mappings. Section vocabulary and exact remembered-open expiry remain
questions. Localization evidence samples messages and languages; it is not a claim that every string
is translated. No-error browser observations cover only their exercised paths. No application suites
were run locally for this draft.
