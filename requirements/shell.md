# Requirements: shell and shared UI

The frame (top bar, modules, navigation), theme and branding, shared widgets. Issues against this area (kept in the
issues database): I4, I27, I33 (2/3-line status box), I39 (animation), I46 and I35 (icon alignment), I48.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| SHL-01 | proposed | The page identifies CalendarStream in its title bar, footer and favicon. | — | — |
| SHL-01.a | proposed | The page identifies CalendarStream in its title. Its footer shows the running version, linked to its release (including the full beta identifier), the copyright, and a link to README License & Attribution (DOC-01). | — | S61-07, S29-01, S30-05, S61-08, changelog_gaps_1201-1500:25 |
| SHL-01.b | built | The favicon is the light CalendarStream icon with its white background cropped to a circle and the rest transparent. | — | F63 |
| SHL-01.c | planned | The CalendarStream logo files have no compression or visual artifacts. | — | F1 |
| SHL-01.d |  | The title bar shows the logo's mark (no words; the Light mark on light pages, the Dark mark on dark ones) left of the title, and the title in the logo colors (THM-02.m). One transparent favicon serves light and dark. | — | theme.md Clarifications |
| SHL-02 | proposed | The page is available in several languages, chosen automatically or by the user. | — | — |
| SHL-02.a | proposed | The initial page language is English; Automatic follows supported browser language preferences, including French, German and Belgian Dutch, while an unknown browser language falls back to English. Choosing Automatic clears the explicit language override. | — | S17-01, S17-02, S17-03, S17-04, S17-10 |
| SHL-02.b | proposed | The selected language applies to every screen, setup guide, error message (including validation guidance), month name and day name; user-supplied text follows SHL-02. Languages offered include Spanish, French, German, Portuguese and Dutch (SHL-02 adds Brazilian Portuguese). | — | changelog_gaps_1801-2100:29, S17-05, S17-06, S17-07, S17-08, S17-09, S17-11 |
| SHL-02.c | proposed | Brazilian Portuguese is offered as a page language. | — | changelog_gaps_1801-2100:29 |
| SHL-02.d | proposed | The selected page language is a view setting kept on the device for later visits (SET-01). | — | changelog_gaps_1801-2100:29 |
| SHL-02.e | proposed | Translation supports composed and nested messages, including sync-change summaries and download-failure explanations, without translating user event titles. Unknown messages retain their original English wording. | — | S17-14, S17-15, S17-16, S17-17 |
| SHL-02.f | proposed | Values inserted into translated messages are escaped rather than interpreted as markup. | — | S17-18 |
| SHL-02.g | proposed | The subscription page and Google setup-error guide follow the visitor’s supported browser language. | — | S17-12, S24-10 |
| SHL-02.h | proposed | A browser form error presents a localized error page with a way to return to the preceding page; API error responses follow SHL-05. | — | changelog_gaps_1801-2100:30 |
| SHL-03 | proposed | The page uses a light, dark or system theme, and starts in the saved one. | — | — |
| SHL-03.a | proposed | With no saved theme override, the page uses Match system; choosing Dark applies it and indicates it as the selected choice. The page starts in the saved theme without first showing another (SHL-03 owns the choice control). | — | S66-01, S67-47, S67-49, changelog_gaps_2101-2336:25 |
| SHL-03.b | built | The Light / Dark / Match system choice is one icon when closed, a button plus menu like the view picker, replacing a three-way cycling button. | — | F57 |
| SHL-04 | proposed | The page's sections open and fold, and say how. | — | — |
| SHL-04.a | proposed | A section the user left open folds by itself after the time in DEF-01; each section is judged on its own, and its closed state is kept (SET-01). | — | S61-13, S61-14 |
| SHL-04.b | proposed | The open or closed state of the page's sections is a view setting kept on the device, like the other view settings (SET-01); expiry follows SHL-04. | — | changelog_gaps_2101-2336:24 |
| SHL-04.c |  | A folded section says "Expand to Configure" (Calendars, Feeds, All Rules, Event Templates) or "Expand for Details" (History). | — | theme.md Clarifications |
| SHL-04.d |  | Every section's header reads: icon, title, space, status lines, health, + (UI-24). Calendars and Feeds have no status lines; All Rules and Event Templates have up to three (the conflicts or errors, otherwise how many); + is in the top right corner. | — | theme.md Clarifications |
| SHL-05 | proposed | The page loads everything from the installation and keeps its errors machine-readable for programs. | — | — |
| SHL-05.a | proposed | Rendering a CalendarStream page loads its resources, including its fonts (the Mono font with its license), from the CalendarStream installation, without contacting external resource providers such as Google Fonts. | — | readme_gaps:55, changelog_gaps_1201-1500:27, S35-07, S35-08, S35-10, S35-18 |
| SHL-05.b | proposed | Versioned stylesheet, language-script and font assets can be cached as immutable, fonts for one year; an obsolete script version or an unsupported script language is not served, and the unversioned font is not advertised as immutable. | — | S39-03, S39-04, S39-05, S39-06, S39-07, S39-08, changelog_gaps_901-1200:28 |
| SHL-05.c | proposed | Newer emoji display older-Windows compatibility guidance, while older compatible choices do not. Editing or choosing an older emoji clears the compatibility warning; choosing a newer one displays it. Shared explanatory help follows UI-07. | — | S55-37, S55-41, S55-43, S55-44, S55-45, S55-46, S55-47 |
| SHL-05.d | proposed | API-style requests retain structured JSON errors rather than receiving translated HTML pages. | — | S17-13 |

## Notes from the draft

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
