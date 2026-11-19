# Requirements: deployment

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| DEP-01 | proposed | The app runs in the user's own Docker stack and keeps all of its data there. | — | — |
| DEP-01.a | proposed | The app runs as a Docker stack and keeps its calendars, credentials and history in the user's own deployment, not with any outside service. | — | L5 |
| DEP-01.b | proposed | The installer supports Linux, macOS (Docker Desktop) and Windows (WSL). | — | L94 |
| DEP-01.c | proposed | Prebuilt app images run on amd64 and arm64 hosts without building the app locally. | — | changelog_gaps_2101-2336:L36 |
| DEP-01.d | proposed | The configured user and group identity and the restart policy are applied to the stack. | — | L153 |
| DEP-01.e | proposed | When the database is not ready at startup, the app retries the connection at the interval in DEF-01 for up to the wait in DEF-01; if it still cannot connect, startup fails with a message that the database cannot be reached. | — | changelog_gaps_901-1200:L29 |
| DEP-01.f | proposed | Deleting the Postgres directory resets the app to a fresh install: sources, destinations, edits, rules, templates, settings, logins, the Google connection and feed links. | — | L530 |
| DEP-01.g | proposed | The database and the calendar data are backed up and restored from Settings > Site Admin (SET-06). A restored database needs the deployment secrets (the database password) to read its encrypted credentials. | — | L525 |
| DEP-02 | proposed | An installer sets up the stack and can be run again to keep it current. | — | — |
| DEP-02.a | proposed | The installer asks for a subdomain or stack prefix, stable or beta, the app, config and data paths and whether to install the updater (enabled by default), and offers working defaults; an existing folder is detected and reused. | — | L103, changelog_gaps_301-600:L33 |
| DEP-02.b | proposed | When the chosen app folder already exists, the installer offers using it, choosing a numbered folder, choosing another path or cancelling. | — | changelog_gaps_1-300:L29, readme_gaps:L24 |
| DEP-02.c | proposed | A second install on the same host detects the existing containers and picks distinct container names and ports, and remembers them (STACK_NO and PORT). | — | L114 |
| DEP-02.d | proposed | The installer generates the database credentials, downloads the deployment files, starts the app and prints the address and the setup code (see ACC-01). Running it again keeps the saved settings, the database password and the data folder, offers the saved settings as its defaults, and installs the newest image of the selected release (see SET-05). | — | L119, L490, changelog_gaps_1801-2100:L26 |
| DEP-02.e | proposed | Host-address lookup failures are reported to the user rather than silently terminating installation. | — | changelog_gaps_1501-1800:L32 |
| DEP-02.f | proposed | The installer writes the environment configuration with read access restricted to its owner. | — | changelog_gaps_1501-1800:L38 |
| DEP-02.g | proposed | Installer answers containing pipe or ampersand characters are preserved literally in the saved configuration. | — | changelog_gaps_1501-1800:L38 |
| DEP-02.h | proposed | The installer accepts stable and latest as names for the stable release channel. | — | changelog_gaps_1801-2100:L28 |
| DEP-02.i | proposed | The installer accepts an exact release identifier, including a beta, and installs that release with its own matching deployment definition. | — | changelog_gaps_601-900:L24, changelog_gaps_1501-1800:L16 |
| DEP-02.j | proposed | Starting or recreating the app deployment checks the selected image tag for an updated image before starting the app. | — | changelog_gaps_2101-2336:L32 |
| DEP-03 | proposed | The stack works behind a proxy and with Google's notifications. | — | — |
| DEP-03.a | proposed | FORWARDED_ALLOW_IPS lists the proxies trusted to report the visitor's address and HTTPS use (see ACC-07). | — | L154 |
| DEP-03.b | proposed | Google notifications need valid TLS and proxy access to the unauthenticated notification endpoint; without it the daily check still runs (see GGL-06, GGL-06). | — | L455 |
| DEP-04 | proposed | An updater, when installed, acts only when the app asks it and is not reachable from outside. | — | — |
| DEP-04.a | proposed | The updater acts only when the app asks it: when the user presses Update now, or when automatic updating is on and a check finds a newer version (SET-05). It never updates the database, and it removes old images after an update. | — | L500 |
| DEP-04.b | proposed | The updater is not reachable from outside the Docker network, needs a generated secret token and uses the Docker socket; the installer can remove it without losing other data (see SET-05). | — | L502 |
| DEP-05 | proposed | Settings can start in the environment and move to the database, and a Python installation can be migrated. | — | — |
| DEP-05.a |  | Environment (.env) values are only starting values: a value saved in the database always overrides the matching environment setting (time zone, sync interval, CCS+ client and link, calendar name, default event hours, 24-hour rule). The only settings that stay environment-only are the ones the app needs before it can read the database: the stack name and folders, the image tag, the updater profile, the user, group and restart policy, the trusted proxy addresses and the database password. (Developer, Nov 17: the database overrides all env settings) | — | Developer, Nov 17; README Settings |
| DEP-05.b |  | The installer sets the installation's time zone (the server's TZ setting). It is the default zone for an imported event that carries no zone and for server work without a device (scheduled downloads), until the user defines otherwise: a default zone saved in Settings > Site Admin (SET-06) overrides the installer's. (Developer, Nov 17) | — | Developer, Nov 17 |
| DEP-05.c |  | A one-time migration tool copies all data from a Python-app database into the new Dart database (events, edits, custom events, History, rules, sources, destinations, settings, Google connection and feeds), never changes the old database, and prints a report of what it copied for the Developer to check. The page password is not carried over: after migration the user requests a new login password (Developer, Nov 17). The tool is tested in three steps: first on a made-up demo database, then on a copy of the real database, and only then on the real database (Developer, Nov 17). | — | Developer, Nov 17 |

