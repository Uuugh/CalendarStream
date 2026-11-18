# Requirements: deployment

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | was |
|---|---|---|---|---|
| DEP-14 |  | A one-time migration tool copies all data from a Python-app database into the new Dart database (events, edits, custom events, History, rules, sources, destinations, settings, Google connection and feeds), never changes the old database, and prints a report of what it copied for the Developer to check. | — | Developer, Nov 17 |
| DEP-27 |  | The installer sets the installation's time zone (the server's TZ setting). It is the default zone for an imported event that carries no zone and for server work without a device (scheduled downloads), until the user defines otherwise: a default zone saved in Settings > Site Admin (SET-59) overrides the installer's. (Developer, Nov 17) | — | Developer, Nov 17 |
| DEP-01 | proposed | The app runs as a Docker stack and keeps its calendars, credentials and history in the user's own deployment, not with any outside service. | — | L5 |
| DEP-02 | proposed | The installer supports Linux, macOS (Docker Desktop) and Windows (WSL). | — | L94 |
| DEP-03 | proposed | The installer asks for a subdomain or stack prefix, stable or beta, the app, config and data paths and whether to install the updater, and offers working defaults; an existing folder is detected and reused. | — | L103 |
| DEP-04 | proposed | A second install on the same host detects the existing containers and picks distinct container names and ports, and remembers them (STACK_NO and PORT). | — | L114 |
| DEP-05 | proposed | The installer generates the database credentials, downloads the deployment files, starts the app and prints the address and the setup code (see ACC-03). Running it again keeps the settings and the database password. | — | L119 |
| DEP-06 | proposed | The configured user and group identity and the restart policy are applied to the stack. | — | L153 |
| DEP-07 | proposed | FORWARDED_ALLOW_IPS lists the proxies trusted to report the visitor's address and HTTPS use (see ACC-17). | — | L154 |
| DEP-08 | proposed | Google notifications need valid TLS and proxy access to the unauthenticated notification endpoint; without it the daily check still runs (see GGL-41, GGL-44). | — | L455 |
| DEP-09 | proposed | Running the installer again keeps the settings and installs the newest image of the selected release (see SET-26). | — | L490 |
| DEP-10 | proposed (?) | The updater never updates the database, never checks for updates on its own, and removes old images. Conflicts with auto-update (SET-32): which wins? | — | L500 |
| DEP-11 | proposed | The updater is not reachable from outside the Docker network, needs a generated secret token and uses the Docker socket; the installer can remove it without losing other data (see SET-29). | — | L502 |
| DEP-12 | proposed (?) | The database is backed up with pg_dump; keeping the deployment secrets is required to read the encrypted credentials after a restore. Is a restore procedure part of the product? | — | L525 |
| DEP-13 | proposed | Deleting the Postgres directory resets the app to a fresh install: sources, destinations, edits, rules, templates, settings, logins, the Google connection and feed links. | — | L530 |
