# Requirements: shell and shared UI

The frame (top bar, modules, navigation), theme and branding, shared widgets.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| SHL-01 | proposed | The page identifies CalendarStream in its title bar, footer and favicon. | — | — |
| SHL-01.a | proposed | The footer shows the running version, linked to its release (including the full beta identifier), the copyright, and a link to README License & Attribution (DOC-01). | — | S61-07, S29-01, S30-05, S61-08, changelog_gaps_1201-1500:25 |
| SHL-01.b | proposed | The favicon is the light CalendarStream icon with its white background cropped to a circle and the rest transparent. | — | F63 |
| SHL-01.c | proposed | The CalendarStream logo files have no compression or visual artifacts. | — | F1 |
| SHL-01.d | backlog | The title bar shows the logo's mark (no words; the Light mark on light pages, the Dark mark on dark ones) left of the title, and the title in the logo colors (THM-02.m). One transparent favicon serves light and dark. | — | theme.md Clarifications |
| SHL-01.e | proposed | A browser tab is titled CalendarStream on the main page and "<page name> · CalendarStream" on the sign-in page (msg:signInAction) and the initial-setup page (msg:welcome). | — | R1 gap |
| SHL-01.f | proposed | The sign-in and initial-setup pages show the running version as vX.Y.Z beside the name CalendarStream; the main page shows it in the footer only (SHL-01.a). | — | R1 gap |
| SHL-01.g | proposed | The default icons are a favicon, an app icon and an Apple touch icon at the sizes in DEF-01, each with the version in its address; a custom favicon (SET-06.f) replaces all three. | — | R1 gap |
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
| SHL-03.b | proposed | The Light / Dark / Match system choice is one icon when closed, a button plus menu like the view picker, replacing a three-way cycling button. | — | F57 |
| SHL-03.c | proposed | The sign-in and initial-setup pages follow the saved theme. | — | R1 gap |
| SHL-05 | proposed | The page loads everything from the installation and keeps its errors machine-readable for programs. | — | — |
| SHL-05.a | proposed | Rendering a CalendarStream page loads its resources, including its fonts (the Mono font with its license), from the CalendarStream installation, without contacting external resource providers such as Google Fonts. | — | readme_gaps:55, changelog_gaps_1201-1500:27, S35-07, S35-08, S35-10, S35-18 |
| SHL-05.b | proposed | Versioned stylesheet, language-script and font assets can be cached as immutable, fonts for one year; an obsolete script version or an unsupported script language is not served, and the unversioned font is not advertised as immutable. | — | S39-03, S39-04, S39-05, S39-06, S39-07, S39-08, changelog_gaps_901-1200:28 |
| SHL-05.d | proposed | API-style requests retain structured JSON errors rather than receiving translated HTML pages. | — | S17-13 |

