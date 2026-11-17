# Requirements: settings

☰ Settings, preferences, updates, public address. Issues against this feature (kept in the issues database): I2
(auto-update toggle, built beta.46), I25, I22.

| ID | status | statement | test | was |
|---|---|---|---|---|
| SET-01 | planned | Settings lets the Developer select another release (a build), including one typed by hand, for a temporary release made to solve one user's problem. Deferred: needs a change to the updater container's protocol. | — | F24.1 |
| SET-02 | planned | Settings can show an alternate port, and write it to `.env`; a change takes effect when the container is recreated. Deferred with SET-01. | — | F24.3 |
| SET-03 | planned | The update channel is selectable: Stable, Beta or Other. Deferred with SET-01. | — | F24.4, F54 |
| SET-04 | open | Changing or adding a domain, with Google Calendar API Sync already configured, pops up a notice pointing at that module's assist box, since the API always becomes unhealthy. | — | F56 |
| SET-05 | built | In Full mode, the page's modules (Calendar, Sources, Feeds, All Rules, Event Templates, History) are hidden elsewhere and listed above Settings under a Configure heading. | — | F65 |
| SET-06 | built | Settings has two headings, User (Login, Updates, Theme, each its own item) and Site Admin (Domains, Google API, more as added); every item opens as a pop-up. | — | F65 |
| SET-07 | built | The Settings pop-up stays centered with a dimmed background and a 130×34 px joined Cancel \| Save pair, as theme.md §6 says. | — | F65 |
