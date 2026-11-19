# Requirements: deployment

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| DEP-01 | proposed | The app runs in the user's own Docker stack and keeps all of its data there. | — | — |
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
| DEP-02.k | proposed | The installer lower-cases the subdomain and the names it is given and keeps only letters, digits, dot, underscore and hyphen. | — | R1 gap |
| DEP-02.l | proposed | Without an answer the installer uses port 8080, the time zone America/Chicago, the image tag latest and the restart policy unless-stopped. | — | R1 gap |
| DEP-03 | proposed | The stack works behind a proxy and with Google's notifications. | — | — |
| DEP-03.a | proposed | FORWARDED_ALLOW_IPS lists the proxies trusted to report the visitor's address and HTTPS use (see ACC-07). | — | L154 |
| DEP-03.b | proposed | Google notifications need valid TLS and proxy access to the unauthenticated notification endpoint; without it the daily check still runs (see CGOW-05). | — | L455 |
| DEP-04 | proposed | An updater, when installed, acts only when the app asks it and is not reachable from outside. | — | — |
| DEP-04.a | proposed | The app asks the updater to update when the user presses Update now, or when automatic updating is on and a check finds a newer version (SET-05). The updater never updates the database and removes old images after an update. | — | L500 |
| DEP-04.b | proposed | The updater is not reachable from outside the Docker network, needs a generated secret token and uses the Docker socket; the installer can remove it without losing other data (see SET-05). | — | L502 |
| DEP-05 | proposed | Settings can start in the environment and move to the database, and a Python installation can be migrated. | — | — |
| DEP-05.a | backlog | Environment (.env) values are only starting values: a value saved in the database always overrides the matching environment setting (time zone, sync interval, CCS+ client, calendar name, default event hours, 24-hour rule). The only settings that stay environment-only are the ones the app needs before it can read the database: the stack name and folders, the image tag, the updater profile, the user, group and restart policy, the trusted proxy addresses and the database password. | — | Developer, Nov 17; README Settings |
| DEP-05.b | backlog | The installer sets the installation's time zone (the server's TZ setting). It is the default zone for an imported event that carries no zone and for server work without a device (scheduled downloads), until the user defines otherwise: a default zone saved in Settings > Site Admin (SET-06) overrides the installer's. | — | Developer, Nov 17 |
| DEP-05.c | backlog | A one-time migration tool copies all data from a Python-app database into the new Dart database (events, edits, custom events, History, rules, sources, destinations, settings, Google connection and feeds), never changes the old database, and prints a report of what it copied for the Developer to check. The page password is not carried over: after migration the user requests a new login password. The tool is tested in three steps: first on a made-up demo database, then on a copy of the real database, and only then on the real database. | — | Developer, Nov 17 |
| DEP-02.m | proposed | Every installer question shows its default in square brackets and Enter accepts it; later runs default to the current settings, and answers are read from the terminal even when the installer's input is piped. | — | R6 gap |
| DEP-02.n | proposed | The installer stops at the first failure. | — | R6 gap |
| DEP-02.o | proposed | The installer finds a previous installation in the current folder (a compose file naming calendar_stream) or else in the default stack folder, and takes its defaults from that folder's .env. | — | R6 gap |
| DEP-02.p | proposed | The subdomain slug is lower case with every run of other characters replaced by one hyphen and leading and trailing hyphens and dots removed; an empty slug becomes calendarstream. | — | R6 gap |
| DEP-02.q | proposed | A folder path accepts ~ and relative paths, is made absolute, loses a trailing slash and is created when missing. | — | R6 gap |
| DEP-02.r | proposed | The default port and stack number follow DEF-01 (Installer stack defaults); containers are named prefix and number, prefix_db and number, and prefix_updater and number, the prefix defaulting to calendar_stream. | — | R6 gap |
| DEP-02.s | proposed | The installer writes its answers to .env (the image tag, stack prefix, data folder, stack number, port and profiles), replacing an existing or commented line and keeping the others. | — | R6 gap |
| DEP-02.t | proposed | The installer creates the updater token file, owner-readable, even when the updater is declined, with the length in DEF-01. | — | R6 gap |
| DEP-06 | proposed | The stack's parts are fixed. | — | — |
| DEP-06.a | proposed | The stack is the app, a Postgres database and an optional updater started by a profile. | — | R6 gap |
| DEP-06.b | proposed | The database reports ready by the check in DEF-01 (Database health check). | — | R6 gap |
| DEP-06.c | proposed | The container reports health by calling the health interface (DIA-03) at the interval in DEF-01 (Container health check). | — | R6 gap |
| DEP-06.d | proposed | The database name and user take effect when the database is first created. | — | R6 gap |
| DEP-06.e | proposed | The entrypoint starts as root, reads the secret files with line breaks removed, then runs the app as the configured user and group, without extra groups; a missing secret file is warned about. | — | R6 gap |
| DEP-06.f | proposed | The app listens on all addresses on the port in DEF-01 (Installer stack defaults) inside the container. | — | R6 gap |
| DEP-06.g | proposed | The public address is set on the page, not in .env; an older environment value is read once and moved to the page setting, and a value naming only a host address and the app port counts as not set. | — | R6 gap |
| DEP-06.h | proposed | The defaults of .env are in DEF-01 (Environment defaults). | — | R6 gap |
| DEP-06.i | proposed | The CCS+ calendar address defaults to the one in DEF-01; a saved link replaces it. | — | R6 gap |
| DEP-06.j | proposed | A feed token from an older version is made once as a random URL-safe value, and a typed stream name wins over it. | — | R6 gap |
| DEP-06.k | proposed | Old login files and their secret variants are imported once; the user name is trimmed and the page user name defaults to admin. | — | R6 gap |
| DEP-06.l | proposed | The database host, port and password (from its secret file) come from the environment; a missing password is warned about, and the user and password are percent-encoded. | — | R6 gap |
| DEP-06.m | proposed | The database uses the connection pool in DEF-01, and shutdown cancels the background loops and closes the database. | — | R6 gap |
| DEP-06.n | proposed | A beta image is built when the version changes and the suites pass and the image scan has no fixable high or critical finding; it is tagged with the version, the version with its v prefix, and beta; the latest tag moves when the stable version changes. | — | R6 gap |
| DEP-06.o | proposed | An event length setting accepts decimals, an h suffix and the all-day words; an invalid one is warned about and the default length in DEF-01 is used. | — | R6 gap |
| DEP-06.p | proposed | The 24-hour rule setting is off for 0, false, no and off. | — | R6 gap |
