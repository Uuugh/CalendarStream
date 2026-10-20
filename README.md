# Calendar Stream

Keeps a Google Calendar in sync with your United CCS+ schedule.

CCS+ has an official **Calendar Sync** download (`Calendar.ics`), protected by your UID and
a Calendar Sync password. Apple Calendar can subscribe to it directly, but Google Calendar
can't send a username and password, so United's guide has you download and re-import the
file by hand every time. Calendar Stream does that for you: it downloads the file on a timer
and republishes it as a feed Google Calendar subscribes to. A status page shows sync results,
a month view of the schedule, and setup help.

## Quick start

1. **Turn on Calendar Sync in CCS+:** Settings → Schedule Settings → Calendar syncing.
   Enable it, create a calendar password (just for Calendar Sync, not your CCS login), and
   press **Copy link**.
2. **Create the secret files** in `$MNT_DOCKER/.secrets` (just the value in each; a trailing
   newline is fine):

   | File | Contents |
   |---|---|
   | `CCS_USER.txt` | Your UID |
   | `CCS_PASSWORD.txt` | The **Calendar Sync** password from step 1 |
   | `USER.txt` / `PASSWORD.txt` | A login you choose for the status page |
   | `DB_PASSWORD.txt` | A password you choose for the database |

   ```bash
   sudo chmod 600 "$MNT_DOCKER/.secrets/"*.txt
   ```
   All five must exist or `docker compose up` stops with an error. The database password is
   set the first time Postgres starts; changing the file later doesn't change it.
3. **Get the stack files.** Only `docker-compose.yml` and `.env` are needed on the server; the
   app comes as a ready-made image. Cloning is the easiest way to keep the compose file current:
   ```bash
   git clone https://github.com/Uuugh/calendar_stream.git ~/stacks/calendar_stream
   cd ~/stacks/calendar_stream
   cp .env.default .env      # then fill in PUBLIC_URL (and check IMAGE_TAG)
   ```
4. **Start it:**
   ```bash
   docker compose pull && docker compose up -d
   ```
5. Open `http://<server>:8080`. If your **Copy link** URL differs from the default, paste it
   in **Setup** and press **Save & sync**. The Setup checklist turns green once CCS+ accepts
   the sign-in and the schedule downloads.

### How the secrets connect

| Host file | Secret | Passed to the app as |
|---|---|---|
| `$MNT_DOCKER/.secrets/CCS_USER.txt` | `CCS_USER` | `CCS_USERNAME_FILE` → `CCS_USERNAME` |
| `$MNT_DOCKER/.secrets/CCS_PASSWORD.txt` | `CCS_PASSWORD` | `CCS_PASSWORD_FILE` → `CCS_PASSWORD` |
| `$MNT_DOCKER/.secrets/USER.txt` | `GUI_USER` | `GUI_USERNAME_FILE` → `GUI_USERNAME` |
| `$MNT_DOCKER/.secrets/PASSWORD.txt` | `GUI_PASSWORD` | `GUI_PASSWORD_FILE` → `GUI_PASSWORD` |
| `$MNT_DOCKER/.secrets/DB_PASSWORD.txt` | `DB_PASSWORD` | `DB_PASSWORD_FILE` → `DB_PASSWORD` (and Postgres' `POSTGRES_PASSWORD_FILE`) |

Leave `CCS_USERNAME`, `CCS_PASSWORD`, `GUI_USERNAME` and `GUI_PASSWORD` blank in `.env`; the
secrets override them. Root-only (`600`) files are fine: the container reads them at startup,
before it drops to the `PUID`:`GUID` user (default `1000:100`). If a secret is missing, the
container log names it. The status page locks out an address for 15 minutes after 5 wrong
logins; the calendar feed and subscribe page aren't affected.

## How syncing works

- Every `SYNC_INTERVAL_MINUTES` (default 60, minimum 15) the app requests the Calendar Sync
  link with your UID and Calendar Sync password, the same way an Apple Calendar subscription
  does. It identifies itself honestly as `calendar_stream/<version>` and sends `If-None-Match`
  so unchanged schedules cost almost nothing.
- The calendar file is kept as United sends it: same event IDs, times, time zones and
  details. Calendar Stream only changes:
  - the calendar's name (`CALENDAR_NAME`) and refresh hints for subscribers;
  - **events with no end time** → `DEFAULT_EVENT_HOURS` long, or all-day with `allday`;
  - **events lasting exactly 24 hours** (or 48 h, 72 h…) → all-day events on the day(s) they
    start, with the original times kept in the notes. Turn off with `ALLDAY_24H=false`.
- Event IDs come from CCS+, so a changed trip updates the existing Google event rather than
  adding a duplicate.
- If a download fails, or CCS+ suddenly returns an empty calendar, the previous feed is kept,
  so Google never sees your schedule disappear.

| Status | Meaning |
|---|---|
| Healthy | Last check succeeded (the message says whether anything changed) |
| Sign-in rejected | HTTP 401: check `CCS_USER.txt` (UID) and `CCS_PASSWORD.txt` (Calendar Sync password) |
| Paused | After 2 rejected sign-ins in a row, automatic checks stop so your account isn't locked. Fix the files, restart or press **Sync now** |
| Blocked | HTTP 403, e.g. from Akamai. The message includes the reference number |
| Error | Network trouble, or CCS+ answered with something that isn't a calendar |

After changing `CALENDAR_NAME`, `DEFAULT_EVENT_HOURS` or `ALLDAY_24H`, restart the container;
the feed is rebuilt from the last download straight away.

## The status page

- **Month view**: the schedule exactly as it's sent to Google, with ‹ › to change months and
  **Today** to come back. Multi-day trips appear on every day they cover; click an event for
  its times, location and details. Green items are all-day events.
- **Setup**: checklist for Calendar Sync (UID, password, link, sign-in accepted, schedule
  downloaded), a box for the **Copy link** URL, and the CCS+ steps. A link saved here wins over
  `CCS_CALENDAR_URL` in `.env`; **Reset** goes back to `.env`. The password is never shown.
- **Activity log**: each check and what changed (e.g. "3 new, 1 removed"). Kept in the database.
- **Debug**: the last response's details and the calendar file exactly as downloaded.
- `GET /api/status` (JSON) and `GET /healthz` for monitoring.

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

   Set `PUBLIC_URL` in `.env` to that public HTTPS address (e.g. `https://cal.example.com`).
   The feed and subscribe links then use it, and the "not a public address" warning goes away.
2. Google re-polls subscribed calendars on its own schedule (often every 8–24 hours),
   regardless of how often this container checks CCS+.

The feed and subscribe-page URLs contain a random secret (`FEED_TOKEN`); anyone with either
link can see your schedule, so treat them like passwords. To revoke access, set a new
`FEED_TOKEN` in `.env` (or delete the `feed_token` row from the `kv` table) and restart. Old
links stop working and existing subscribers stop getting updates.

## Versions and releases

Versions are numbered `0.0.x`. Every release gets a git tag (`v0.0.1`, `v0.0.2`, …), an image
`ghcr.io/uuugh/calendar_stream:0.0.x`, and two moving tags on both:

| Tag | Points to |
|---|---|
| `beta` | The newest release |
| `latest` | The last release marked stable |

Choose which one the server runs with `IMAGE_TAG` in `.env` (`beta`, `latest`, or a version).
`latest` exists only once a version has been marked stable. To update:
```bash
cd ~/stacks/calendar_stream
git pull                                   # newest docker-compose.yml / .env.default
docker compose pull && docker compose up -d
```

Releases are made by the **Release** GitHub Action: pushing a new `VERSION` to `main` tags it,
moves `beta`, and builds and pushes the image (amd64 and arm64). To mark a version stable,
open the repository's **Actions** tab → **Release** → **Run workflow** and enter the version
(e.g. `0.0.3`); that moves `latest` for both git and the image.

If `docker compose pull` asks you to log in, the image package is private: on GitHub open
your profile → **Packages** → `calendar_stream` → **Package settings** → change visibility to
**Public** (or run `docker login ghcr.io` with a token that has `read:packages`).

`CHANGELOG.md` lists what changed in each version; the status page shows the running version.

## Where data is stored

Everything the app keeps is in the Postgres container `calendar_stream_db`, whose files live in
`$MNT_DOCKER/calendar_stream/postgres`. The app container itself keeps nothing.

| Table | Contents |
|---|---|
| `calendar_files` | `source` (the calendar as downloaded) and `feed` (as served to Google) |
| `events` | The current schedule, for the status page; replaced in one transaction per change |
| `kv` | `feed_token`, `status`, `calendar_url` (if set on the status page), `http_cache` (ETag) |
| `debug_files` | The last response's details and download |
| `activity_log` | The status page's log (last 1,000 entries) |

Postgres isn't published on any host port; to look inside, use
`docker exec -it calendar_stream_db psql -U ccs calendar_stream`.

**Backups:** `docker exec calendar_stream_db pg_dump -U ccs calendar_stream > calendar_stream.sql`

## Files

```
docker-compose.yml   the stack: app image + Postgres (no build needed)
.env.default         settings template (copy to .env, which stays on the server)
Dockerfile           how GitHub Actions builds the image
entrypoint.sh        reads the Docker secrets as root, then drops to PUID:GUID
app/main.py          web app, sync loop, month view, status/lockout logic
app/calsync.py       Calendar Sync download + feed processing
app/store.py         Postgres storage (tables are created automatically)
app/templates/       status page and subscribe page
VERSION              current version (0.0.x); see CHANGELOG.md
```

## Notes

- The image is Python only (no browser), a small fraction of the old ~600 MB build; Postgres
  (`postgres:18-alpine`) adds roughly 100 MB.
- `.env` stays on your server (`.gitignore` excludes it). Logins and the database password live
  only in `$MNT_DOCKER/.secrets`.
- Calendar Sync is United's own export feature, used here the way a calendar subscription uses it.
