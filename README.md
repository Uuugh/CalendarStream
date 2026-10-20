# Calendar Stream

Logs in to United's CCS schedule page on a timer, turns your schedule into calendar
events, and serves them as an `.ics` feed that Google Calendar subscribes to. A small
status page shows login results, sync history, upcoming events, and debug captures.

## Quick start

1. Get the code and create your `.env` from the template (it's complete; everything already
   has a working value except `PUBLIC_URL`):
   ```bash
   git clone https://github.com/Uuugh/calendar_stream.git ~/stacks/calendar_stream
   cd ~/stacks/calendar_stream
   cp .env.default .env      # then fill in PUBLIC_URL
   ```
   `.env` is never committed, so your settings stay on the server. To update later, see
   **Versions and releases** below (stable = `latest`, newest = `beta`). `PUID`, `GUID`, `TZ`, `RESTART` and `MNT_DOCKER` feed the compose file.
2. Create five secret files in `$MNT_DOCKER/.secrets` (just the value in each; a trailing
   newline is fine). Two are your CCS login, two are a separate login you choose for the
   status page, and one is a password you choose for the database:
   ```bash
   mkdir -p "$MNT_DOCKER/.secrets"
   printf '%s' 'your-employee-id'     > "$MNT_DOCKER/.secrets/CCS_USER.txt"
   printf '%s' 'your-ccs-password'    > "$MNT_DOCKER/.secrets/CCS_PASSWORD.txt"
   printf '%s' 'status-page-user'     > "$MNT_DOCKER/.secrets/USER.txt"
   printf '%s' 'status-page-password' > "$MNT_DOCKER/.secrets/PASSWORD.txt"
   printf '%s' 'database-password'    > "$MNT_DOCKER/.secrets/DB_PASSWORD.txt"
   chmod 600 "$MNT_DOCKER/.secrets/"*.txt
   ```
   All five must exist or `docker compose up` stops with an error. The database password
   is set the first time Postgres starts; changing the file later doesn't change it.
3. Start it:
   ```bash
   docker compose up -d --build
   ```

How the secrets connect to the app (all in `docker-compose.yml`):

| Host file | Secret | Mounted at | Passed to the app as |
|---|---|---|---|
| `$MNT_DOCKER/.secrets/CCS_USER.txt` | `CCS_USER` | `/run/secrets/CCS_USER` | `CCS_USERNAME_FILE` → `CCS_USERNAME` |
| `$MNT_DOCKER/.secrets/CCS_PASSWORD.txt` | `CCS_PASSWORD` | `/run/secrets/CCS_PASSWORD` | `CCS_PASSWORD_FILE` → `CCS_PASSWORD` |
| `$MNT_DOCKER/.secrets/USER.txt` | `GUI_USER` | `/run/secrets/GUI_USER` | `GUI_USERNAME_FILE` → `GUI_USERNAME` |
| `$MNT_DOCKER/.secrets/PASSWORD.txt` | `GUI_PASSWORD` | `/run/secrets/GUI_PASSWORD` | `GUI_PASSWORD_FILE` → `GUI_PASSWORD` |
| `$MNT_DOCKER/.secrets/DB_PASSWORD.txt` | `DB_PASSWORD` | `/run/secrets/DB_PASSWORD` (both containers) | `DB_PASSWORD_FILE` → `DB_PASSWORD`; `POSTGRES_PASSWORD_FILE` for Postgres |

Leave `CCS_USERNAME`, `CCS_PASSWORD`, `GUI_USERNAME` and `GUI_PASSWORD` blank in `.env`;
the secrets override them. The status page locks out an address for 15 minutes after 5 wrong
logins (the activity log notes it); the calendar feed and subscribe page aren't affected.
Root-only (`600`) files are fine: the container reads them at startup, before it drops to
the `PUID`:`GUID` user. If a secret is missing, the container log shows a warning naming it.

Open http://localhost:8080, wait for the first run (or press **Run now**), and copy the
feed link from the page.

## Adding it to Google Calendar

**Easiest:** on the status page, click **Add to Google Calendar**, then **Add** in Google's prompt.

**Sharing with someone else:** copy the **shareable subscribe page** link from the status page
(`https://<your-address>/subscribe/<token>`) and send it to them. That page needs no
status-page password. It has a one-click **Add to Google Calendar** button, an Apple
Calendar / Outlook link, step-by-step instructions (including phone sync), and a manual
fallback. Each person subscribes with their own Google account.

**Manually:** Google Calendar (on a computer) → **Other calendars** → **+** → **From URL** →
paste the raw feed link.

Either way:

1. Google fetches the feed from *its* servers, so the container must be reachable from
   the internet over HTTPS. Easy options that don't require opening router ports:
   - **Cloudflare Tunnel** (`cloudflared tunnel --url http://localhost:8080`)
   - **Tailscale Funnel** (`tailscale funnel 8080`)
   - A reverse proxy (Caddy/Traefik/nginx) on a server you already run.

   Set `PUBLIC_URL` in `.env` to that public HTTPS address (e.g. `https://ccs.example.com`).
   The feed and subscribe links then use it, and the "not a public address" warning goes away.
2. Google re-polls subscribed calendars on its own schedule (often every 8–24 hours),
   regardless of how often this container scrapes. For near-real-time updates on a phone,
   subscribe directly from iOS/macOS Calendar or another client that honours refresh intervals.

The feed and subscribe-page URLs contain a random secret (`FEED_TOKEN`); anyone with either
link can see your schedule, so treat them like passwords. To revoke access, set a new
`FEED_TOKEN` in `.env` (or delete the `feed_token` row from the `kv` table) and restart — old links stop working and
existing subscribers stop getting updates.

## The status page

| Field | Meaning |
|---|---|
| Status | Healthy · Running · Login failed · MFA needed · Paused · Error |
| Last login | Whether the most recent sign-in succeeded. "none this run" means a saved session was reused. |
| Consecutive login failures | After **2** bad-credential failures auto-login pauses so your account doesn't get locked. Fix `.env`, then `docker compose up -d` or press **Run now**. |
| Debug | Screenshot, HTML, and captured JSON from the last run — the first thing to check when something breaks. |

If a scrape fails, the previous feed is kept, so Google never sees an empty calendar.
Also available: `GET /api/status` (JSON) and `GET /healthz`.

## Items without an end time

Some schedule items (training, reserve, a report time with no release) only have a start.
`DEFAULT_EVENT_HOURS` in `.env` decides how they appear:

| Setting | Result |
|---|---|
| `DEFAULT_EVENT_HOURS=1` (default; decimals OK, e.g. `1.5`) | A timed event starting at the start time, that many hours long. |
| `DEFAULT_EVENT_HOURS=allday` | An all-day event on that date. The start time is kept at the top of the event's notes. |

Items with both a start and end time are always timed events, and items with only a date
are always all-day. After changing the setting, restart (`docker compose up -d`); the
next sync rewrites the feed and Google replaces the old entries when it next refreshes.

## How it works

- **Login**: a headless Chromium (Playwright) opens the schedule URL. If a login form
  appears, it fills username/password, including two-step "username → Next → password"
  pages. Cookies are saved in the database, so most runs skip logging in.
- **Parsing** (`app/parser.py`): first it looks at JSON the page loads from its own API
  (fields like report/release times, pairing/trip numbers, origin/destination). If none
  is found it falls back to reading table rows with dates (`21OCT`, `10/21/2026`,
  `2026-10-21`, `Oct 21`) and times (`0645`, `06:45`). Overnight duties roll into the next day.
- **Feed**: events get stable IDs, so updates change existing calendar entries instead of
  creating duplicates.

## When something needs adjusting

I wrote this without being able to see the logged-in CCS page, so expect to tune it once:

- **Login form not found** → open the debug screenshot/HTML and set `CCS_USER_SELECTOR`,
  `CCS_PASS_SELECTOR`, `CCS_SUBMIT_SELECTOR` (CSS selectors) in `.env`.
- **"MFA needed"** → unattended login can't complete a code or push prompt. Options: ask
  whether your account can use "remember this device", or complete MFA once in the
  container's browser session and rely on the saved cookies (they'll eventually expire).
- **Logged in but 0 events / wrong events** → check *Captured JSON* first. Add the field
  names you see to `FIELD_HINTS` in `app/parser.py`, or adapt `parse_html`. Then
  `docker compose up -d --build`.

## Versions and releases

Versions are numbered `0.0.x`. Every release gets a git tag (`v0.0.1`, `v0.0.2`, …) plus
two moving tags:

| Tag | Points to |
|---|---|
| `beta` | The newest release |
| `latest` | The last release marked stable (set by hand when a version is declared stable) |

`CHANGELOG.md` lists what changed in each version; the status page shows the running version.

To run a particular channel on the server (moving tags need `--force` to update):
```bash
git fetch --tags --force
git checkout latest      # stable;  or: git checkout beta  /  git checkout v0.0.1
docker compose up -d --build
```

## Where data is stored

Everything the app keeps is in the Postgres container `calendar_stream_db`, whose files live in
`$MNT_DOCKER/calendar_stream/postgres`. The app container itself keeps nothing, so it can be
rebuilt or replaced freely.

| Table | Contents |
|---|---|
| `kv` | `feed_token`, `session` (saved CCS login cookies), `status` (last sync/login results) |
| `events` | The current schedule; replaced in one transaction on each successful sync |
| `debug_files` | Screenshot, page HTML and captured JSON from the last run |
| `activity_log` | The status page's log (last 1,000 entries); survives restarts |

The calendar feed is built from `events` on each request. Postgres isn't published on any
host port; to look inside, use `docker exec -it calendar_stream_db psql -U ccs calendar_stream`.

**Backups:** `docker exec calendar_stream_db pg_dump -U ccs calendar_stream > calendar_stream.sql`

**Coming from the file-based version:** the old `config` and `data` folders aren't used any
more. To keep feed links you already shared, run `sudo cat $MNT_DOCKER/ccs_calendar/config/feed_token`
and paste the value after `FEED_TOKEN=` in `.env` before starting. Then the old folders can be deleted.

The app runs as `PUID`:`GUID` (default `1000:100`) after reading the secrets as root.

## Files

```
entrypoint.sh      reads the Docker secrets as root, then drops to PUID:GUID
app/main.py        web app, background loop, status/lockout logic
app/store.py       Postgres storage (tables are created automatically)
app/scraper.py     Playwright login + page capture
app/parser.py      JSON/HTML → events
app/ics.py         events → iCalendar feed
app/templates/     status page
VERSION            current version (0.0.x); see CHANGELOG.md
$MNT_DOCKER/calendar_stream/postgres   (volume) database files
```

## Notes

- The app image is ~600 MB, almost all Chromium (needed to get through United's login).
  The Postgres image (`postgres:18-alpine`) adds roughly 100 MB more.
- `.env` stays on your server (`.gitignore` excludes it); `.env.default` is the committed template.
  Logins and the database password live only in `$MNT_DOCKER/.secrets`.
- Check that automated access to CCS is permitted under United's policies for your account.
