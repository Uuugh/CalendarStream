# CalendarStream

Keeps a Google Calendar in sync with your United CCS+ schedule.

CCS+ has an official **Calendar Sync** download (`Calendar.ics`), protected by your UID and
a Calendar Sync password. Apple Calendar can subscribe to it directly, but Google Calendar
can't send a username and password, so United's guide has you download and re-import the
file by hand every time. CalendarStream does that for you: it downloads the file on a timer
and either writes it straight into a Google calendar of its own (Google Calendar sync, with tag
colours, updated within minutes) or republishes it as a feed that Google Calendar, Apple Calendar
and others subscribe to. A status page shows sync results, a month view where you can edit
events, and setup help.

## Quick start

What you need: a Linux server with Docker and Docker Compose, and (for Google) a public `https://`
address that reaches the server's port 8080, for example through a reverse proxy, Cloudflare
Tunnel or Tailscale Funnel.

1. **Get the stack files and make your `.env`.** Only `docker-compose.yml` and `.env` are needed
   on the server; the app comes as a ready-made image. Cloning keeps the compose file easy to update
   (`git pull`):
   ```bash
   git clone https://github.com/Uuugh/CalendarStream.git ~/stacks/calendarstream
   cd ~/stacks/calendarstream
   cp .env.default .env
   ```
   Open `.env` and check `MNT_DOCKER` (the only required setting: where the secrets and the
   database live) and `TZ`. Set `IMAGE_TAG=beta` to run the newest release instead of the stable
   one. Everything else is optional and explained in the file.

2. **Create the database password file**, the only secret kept on the server. Choose any
   password; `printf` writes it without a trailing newline (one is fine too):
   ```bash
   mkdir -p /mnt/SSD/docker/.secrets        # your MNT_DOCKER + /.secrets
   printf '%s' 'a-db-password' > /mnt/SSD/docker/.secrets/DB_PASSWORD.txt
   chmod 600 /mnt/SSD/docker/.secrets/DB_PASSWORD.txt
   ```
   It's set when the database is first created (changing the file later doesn't change it), and
   it's also the key that encrypts the passwords CalendarStream stores, so keep it safe.

3. **Start it** (from `~/stacks/calendarstream`):
   ```bash
   docker compose up -d
   ```
   The images are downloaded on the first start.

4. **Create your login.** Open `http://<server>:8080`. The first visit asks for a **setup code**
   and the user name and password you want for the status page. The code is in the container log:
   ```bash
   docker compose logs calendar_stream | grep "setup code"
   ```
   Only someone who can read the server's log can create the login. From then on the browser asks
   for it; change it in **Settings (☰) → Status-page login**.

5. **Finish on the status page:**
   - **Status & setup → Setup:** enter your CCS+ **UID** and **Calendar Sync password** and press
     **Save & sync**. Setup explains how to turn on Calendar Sync in CCS+ and create that password;
     if your **Copy link** URL differs from the default, paste it too. The checklist turns green once
     CCS+ accepts the sign-in and the schedule downloads.
   - **☰ → Public address:** enter your public `https://` address (or press **This page** if you
     opened it through that address) and **Save**. It's used for the feed and subscribe links and
     for Google sign-in.
   - **Google Calendar** (choose one):
     - *Sync (recommended):* **☰ → Google Calendar**. Enter an OAuth client ID and secret (the menu
       has a step-by-step guide for getting them in Google Cloud), wait for the ✓, and press
       **Connect Google Calendar**. See [Syncing straight to Google Calendar](#syncing-straight-to-google-calendar-beta).
     - *Subscribe to the feed:* **Add to Google Calendar** in Status & setup. Google refreshes it
       only every 8–24 hours and shows no tag colours.

**Updating:** `cd ~/stacks/calendarstream && git pull && docker compose up -d`. The compose file
pulls a newer image for the tag in `IMAGE_TAG` on every `up`.

**Starting over:** stop the stack (`docker compose down`) and delete
`$MNT_DOCKER/calendar_stream/postgres`. This erases everything saved: event edits, tags, settings,
the Google connection and the feed link you may have shared.

### Where the logins and secrets are kept

| What | Where | Stored as |
|---|---|---|
| Database password | `$MNT_DOCKER/.secrets/DB_PASSWORD.txt` (Docker secret `DB_PASSWORD`) | The only file; read at startup |
| Status-page login | Created on the first visit; **Settings → Status-page login** | Password hashed (scrypt) |
| CCS+ UID and Calendar Sync password | **Setup** | Password encrypted |
| Google OAuth client | **Settings → Google Calendar** | Secret encrypted |
| Google sign-in | **Settings → Google Calendar → Connect** | Encrypted |

Encrypted values use a key derived from `DB_PASSWORD`, which isn't stored in the database, so a
copy of the database alone can't reveal them. If `DB_PASSWORD` changes, enter the CCS+ password
and the Google client secret again and reconnect Google. A root-only (`600`) `DB_PASSWORD.txt` is
fine: the container reads it at startup, before it drops to the `PUID`:`GUID` user (default
`1000:100`). The status page locks out an address for 15 minutes after 5 wrong logins (or setup
codes); the calendar feed and subscribe page aren't affected.

**Upgrading from 0.1.2 or earlier:** start 0.1.3 once with your old `docker-compose.yml` (which
still mounts `CCS_USER.txt`, `CCS_PASSWORD.txt`, `USER.txt` and `PASSWORD.txt`): it imports those
logins into the database. Then `git pull` the new compose file, `docker compose up -d`, and delete
the four old files. (Or skip that and enter the logins on the page.)

## How syncing works

- Every few minutes (60 by default; change it under the health bar on the status page, between 15
  and 1,440, or with `SYNC_INTERVAL_MINUTES`) the app requests the Calendar Sync
  link with your UID and Calendar Sync password, the same way an Apple Calendar subscription
  does. The download is done with `curl` (United's Akamai protection answers curl but holds
  requests from Python's HTTP libraries), which identifies itself as curl. It sends
  `If-None-Match`, so unchanged schedules cost almost nothing.
- The calendar file is kept as United sends it: same event IDs, times, time zones and
  details. CalendarStream only changes:
  - the calendar's name (`CALENDAR_NAME`) and refresh hints for subscribers;
  - **events with no end time that start at midnight** → all-day. CCS+ sends day codes
    (RDO, HDO, VRDO, VHDO…) this way;
  - **other events with no end time** → `DEFAULT_EVENT_HOURS` long, or all-day with `allday`;
  - **events lasting 24 hours** (or 48 h, 72 h…, within 5 minutes, so CCS+'s full days written
    as 00:01–23:59:59 count) → all-day events on the day(s) they start, with the original times
    kept in the notes. Turn off with `ALLDAY_24H=false`.
- Event IDs come from CCS+, so a changed trip updates the existing Google event rather than
  adding a duplicate.
- If a download fails, or CCS+ suddenly returns an empty calendar, the previous feed is kept,
  so Google never sees your schedule disappear.

| Status | Meaning |
|---|---|
| Healthy | Last check succeeded (the message says whether anything changed) |
| Sign-in rejected | HTTP 401: check the UID and Calendar Sync password in **Setup** |
| Paused | After 2 rejected sign-ins in a row, automatic checks stop so your account isn't locked. Fix the files, restart or press **Sync now** |
| Blocked | HTTP 403, e.g. from Akamai. The message includes the reference number |
| Error | Network trouble, a timeout, or CCS+ answered with something that isn't a calendar |

**If the automatic download doesn't get through** (for example, United's bot protection holds
the request), open the Calendar Sync link in your browser, sign in with your UID and Calendar
Sync password, and upload the `Calendar.ics` it downloads with **Upload & publish** (under the
health bar).
The feed updates immediately. This is United's own procedure for Google Calendar; Calendar
Stream just saves you the re-import.

After changing `CALENDAR_NAME`, `DEFAULT_EVENT_HOURS` or `ALLDAY_24H`, restart the container;
the feed is rebuilt from the last download straight away.

## The status page

The title bar shows **CalendarStream** and its version, a **Light / Dark / System** theme switch,
and a **Settings** menu (☰) with the Google Calendar connection. Below it, top to bottom: the month view, **Status &
setup** (its title is the calendar's name, colour and **Save**), and the **Activity log** (closed at
first). Click a section's title or arrow to open or close it. The theme and which sections are open
are saved in the database, so they're the same in every browser.

- **Month view**: the schedule exactly as it's sent to Google, with ‹ › to change months and
  **Today** to come back. Multi-day trips appear on every day they cover; click an event for
  its times, location and details. Green items are all-day events.
- **Editing**: click an event → **Edit** to change its title, times, location or notes, or to
  hide it from Google. Edits to United's events are stored separately and re-applied after every
  download, so they survive syncs; ✎ marks an edited event and ⚠ one that United changed after
  your edit (open it to compare, then keep yours or **Revert to United's version**). Use **+** on
  a day to add your own event (purple). Edits never change anything in CCS+.
- **Calendar name, colour and tags**: the title of Status & setup shows the name in the calendar's
  colour; **(edit)** opens the editor. The name is what Google shows (overrides `CALENDAR_NAME`);
  calendars already subscribed keep their name, so rename those in Google. The default colour
  tints the month view and is offered to subscribers as `X-APPLE-CALENDAR-COLOR` (Apple Calendar
  uses it; Google subscribers pick their own); **Default** goes back to the standard colours.
  **Tag colours**: an event whose title matches a tag uses that tag's colour on this page; the
  first matching tag wins. Each tag matches by *Whole word* (default: `RDO` matches "RDO." but not
  "VRDO"), *Contains*, *Starts with* or *Exact title*, and **Aa** makes it match capitals exactly.
- **Health bar** (top of Status & setup): the status, **Sync now**, then a small line with how
  often CCS+ is checked (type a number of minutes and press **Save**; the next check moves to match)
  and how items without an end time are treated, and a compact **Upload Calendar.ics** row.
- **Setup** (inside Status & setup, closed at first): a box for the **Copy link** URL, a checklist
  for Calendar Sync (UID, password, link, sign-in accepted, schedule received), and the CCS+ steps. A link saved here wins over
  `CCS_CALENDAR_URL` in `.env`; **Reset** goes back to `.env`. The password is never shown.
- **Activity log**: a one-line status (sign-in, last check, schedule changed, next check, events in
  the feed), then each check and what changed (e.g. "3 new, 1 removed") in a window five rows
  tall that scrolls. Kept in the database. Below it, **Debug** links show the last response's
  details and the calendar file exactly as received.
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

   Enter that public HTTPS address (e.g. `https://cal.example.com`) in **Settings (☰) → Public
   address** (or set `PUBLIC_URL` in `.env`; the Settings value wins, and **Reset** goes back to `.env`).
   The feed and subscribe links then use it, and the "not a public address" warning goes away.
2. Google re-polls subscribed calendars on its own schedule (often every 8–24 hours),
   regardless of how often this container checks CCS+.

The feed and subscribe-page URLs contain a random secret (`FEED_TOKEN`); anyone with either
link can see your schedule, so treat them like passwords. To revoke access, set a new
`FEED_TOKEN` in `.env` (or delete the `feed_token` row from the `kv` table) and restart. Old
links stop working and existing subscribers stop getting updates.

## Syncing straight to Google Calendar (beta)

Being built for 0.1.0 (plan: `docs/plans/0.1.0-google-calendar-sync.md`). Instead of Google
subscribing to the feed, CalendarStream writes the schedule into a calendar of its own in your
Google account, through Google's Calendar API: updates within minutes and tag colours in Google.
It asks only for permission to manage **calendars it created** (`calendar.app.created`) and to see
your e-mail address; it can't see or change your other calendars.

**What it does:**
- Copies every event from the first day of the current month onward (older ones are left alone),
  with the edits, hides and added events made on the status page, and without reminders.
  CCS+'s "free" items (days off, reserve…) are shown as *free*, the rest as *busy*.
- **Tag colours** become Google event colours: each tag uses the nearest of Google's 11 colours
  (Tomato, Flamingo, Tangerine, Banana, Sage, Basil, Peacock, Blueberry, Lavender, Grape, Graphite).
  Events with no tag take the calendar's colour, which you choose in Google.
- The calendar's **name** follows the name set on the status page.
- Changes go to Google within seconds of a download, upload or edit. Once a day (and with **Sync
  now**) it also checks Google's copy and puts back anything changed or deleted there; events you
  add to that calendar yourself are left alone. If the calendar is deleted in Google, a new one is
  made.

**Setting it up.** Everything happens in **Settings (☰) → Google Calendar**, which has a
step-by-step guide with links:

1. In Google Cloud (free), create an **OAuth client** for CalendarStream: a project, the Google
   Calendar API turned on, the consent screen (scopes `openid`, `userinfo.email` and
   `calendar.app.created`) **published**, and a *Web application* client whose authorised
   redirect URI is the one the menu shows (`https://<your public address>/google/callback`).
2. Paste its **Client ID** and **Client secret** into the menu and press **Save**. The secret is
   stored encrypted and never shown again. CalendarStream asks Google straight away whether it
   accepts them and shows ✓ (accepted), ✗ (wrong ID or secret) or ? (couldn't check);
   **Check again** repeats it. The redirect URI and consent screen are checked when you connect.
3. Press **Connect Google Calendar** and allow access. Google warns that it "hasn't verified this
   app" because it's your own: choose **Advanced → Go to CalendarStream**.

One OAuth client serves the whole install: everyone who connects uses it with their own Google
account (up to 100 people while the app is unverified). To change the client, disconnect first.
**Disconnect** removes CalendarStream's access in Google; tick *Also delete this calendar in
Google* to remove the calendar too (otherwise connecting the same account again reuses it). If you
also subscribed to the `.ics` feed in Google, remove that calendar there, or you'll see everything
twice.

The public address (Settings → Public address, or `PUBLIC_URL`) must be the page's `https://` address, because Google only sends the sign-in
back to https addresses (or `localhost`). The client secret and the sign-in (a refresh token) are
stored in the database encrypted with a key derived from `DB_PASSWORD`, so a copy of the database
alone can't reach your Google account. If `DB_PASSWORD` changes, enter the secret and connect
again.

## Versions and releases

Versions are numbered `0.y.z` (0.1.0 is the first minor version; fixes and features go into
`0.1.x` until the next minor version is decided). Every release gets a git tag (`v0.1.0`, …), an
image `ghcr.io/uuugh/calendarstream:<version>` (called `calendar_stream` up to 0.1.0), and a GitHub Release with its notes. Two moving image tags:

| Image tag | Points to |
|---|---|
| `beta` | The newest release (also a git tag) |
| `latest` | The last release marked stable (in `STABLE`; its GitHub Release is marked **Latest**) |

Choose which one the server runs with `IMAGE_TAG` in `.env` (`beta`, `latest`, or a version).
`latest` exists only once a version has been marked stable. To update:
```bash
cd ~/stacks/calendarstream
git pull                                   # newest docker-compose.yml / .env.default
docker compose up -d                       # pulls the newest image for IMAGE_TAG, then recreates if it changed
```

Releases are made by the **Release** GitHub Action:

- A new `VERSION` on `main` tags it, moves `beta`, builds and pushes the image (amd64 and arm64),
  and publishes a GitHub Release (pre-release) with that version's `CHANGELOG.md` notes.
- A new `STABLE` on `main` marks that version stable: the `latest` image points at it, and its
  GitHub Release becomes the latest one. (There's no `latest` git tag; `STABLE` records it.) You can also do this from the repository's
  **Actions** tab → **Release** → **Run workflow** with the version (e.g. `0.0.6`).

`CHANGELOG.md` lists what was added, changed, fixed and removed in each version.

If `docker compose pull` asks you to log in, the image package is private: on GitHub open
your profile → **Packages** → `calendar_stream` → **Package settings** → change visibility to
**Public** (or run `docker login ghcr.io` with a token that has `read:packages`).

The status page shows the running version.

## Where data is stored

Everything the app keeps is in the Postgres container `calendar_stream_db`, whose files live in
`$MNT_DOCKER/calendar_stream/postgres`. The app container itself keeps nothing.

| Table | Contents |
|---|---|
| `calendar_files` | `source` (the calendar as downloaded) and `feed` (as served to Google) |
| `events` | The current schedule, for the status page; replaced in one transaction per change |
| `kv` | `feed_token`, `status`, `http_cache` (ETag), and what's set on the status page: `page_login` (hashed), `ccs_login` (encrypted), `public_url`, `sync_interval`, `calendar_url`, `calendar_name`, `calendar_color`, `calendar_tags`, `ui_theme`, `ui_sections`; `google` (connected account, calendar and last sync), `google_client` (OAuth client; secret encrypted) and `google_token` (the encrypted Google sign-in) |
| `google_events` | What was last written to Google for each event (to send only changes) |
| `event_edits` | Your changes to United's events (re-applied after each download) |
| `custom_events` | Events you added on the status page |
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
app/logins.py        the CCS+ and status-page logins (kept in the database)
app/secretbox.py     encryption and password hashing
app/calsync.py       Calendar Sync download + feed processing
app/gsync.py         Google Calendar sync (OAuth sign-in, encrypted secrets, writing the events)
app/store.py         Postgres storage (tables are created automatically)
app/templates/       status page, event editor and subscribe page
VERSION              current version (e.g. 0.1.0); see CHANGELOG.md
STABLE               the version marked stable (tagged latest)
```

## Notes

- The image is Python only (no browser), a small fraction of the old ~600 MB build; Postgres
  (`postgres:18-alpine`) adds roughly 100 MB.
- `.env` stays on your server (`.gitignore` excludes it). Logins and the database password live
  only in `$MNT_DOCKER/.secrets`.
- Calendar Sync is United's own export feature, used here the way a calendar subscription uses it.
