# CalendarStream

Maintains a Google Calendar in sync with your United Airlines CCS+ schedule.

United Airlines' CCS+ does not provide a method to keep your Google Calendar up to date
automatically. United instead offers an official **Calendar Sync** download (`Calendar.ics`),
protected by your UID and a Calendar Sync password, which must be downloaded and re-imported into
Google Calendar by hand.

CalendarStream automates this process by downloading the official `.ics` file on a timer and
either:

1. writes it into a Google calendar of its own (updated within minutes, with tag colors), or
2. republishes it as a feed that Google, Apple Calendar and others can subscribe to.

A status page shows the schedule, lets you edit events, and walks you through setup.

## Quick start

On a Linux server with Docker, run:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)
```

[`install.sh`](install.sh) asks three questions (press Enter for the default):

1. the folder for `docker-compose.yml` and `.env` (`~/stacks/calendarstream`);
2. the folder for CalendarStream's config and data, the database and `.secrets/` (the same folder);
3. which release to install, `latest` (stable) or `beta` (`stable`).

It then downloads `docker-compose.yml` and `.env`, creates a random database password, starts
CalendarStream and prints its address and a **setup code**. Running it again updates
CalendarStream; your `.env` (apart from those answers) and the database password are kept.

Then open the address it printed:

1. **Create your login** with the setup code.
2. **Status & setup → Setup:** enter your CCS+ UID and Calendar Sync password.
3. **☰ → Public address:** your public `https://` address (needed for Google and for sharing).
4. **☰ → Google Calendar:** connect it (recommended), or use **Add to Google Calendar** to
   subscribe to the feed instead.

## Settings

Everything is optional. Most settings are made on the status page; `.env` holds the rest, each
explained in [`.env.default`](.env.default):

| Setting | Default | Notes |
|---|---|---|
| `MNT_DOCKER` | the stack folder | Where the database (`calendar_stream/postgres`) and `.secrets/` live; the installer asks |
| `TZ` | `America/Chicago` | Time zone the schedule is shown in |
| `IMAGE_TAG` | `latest` | `latest` (stable), `beta` (newest) or a version, e.g. `0.1.6`; the installer asks |
| `PUID` / `GUID`, `RESTART` | `1000` / `100`, `unless-stopped` | |
| `PUBLIC_URL` | — | Overridden by ☰ → Public address |
| `SYNC_INTERVAL_MINUTES` | `60` | 15–1,440; overridden by the box under the health bar |
| `CCS_CALENDAR_URL`, `CALENDAR_NAME` | United's link, "United CCS Schedule" | Overridden in Setup and (edit) |
| `DEFAULT_EVENT_HOURS` | `1` | Hours for items with no end time, or `allday` |
| `ALLDAY_24H` | `true` | Show 24-hour (48 h…) events as all-day |
| `FEED_TOKEN` | made once | Secret part of the feed links; change it to cut off old links |

**Secrets.** The only file is `.secrets/DB_PASSWORD.txt`, made by the installer. The status-page
login (hashed), the CCS+ password, and the Google client secret and sign-in (encrypted) are kept in
the database. The encryption key comes from `DB_PASSWORD`, so a copy of the database alone reveals
nothing; keep that file and don't change it (if you do, re-enter those passwords). Five wrong
logins or setup codes lock an address out for 15 minutes.

## How syncing works

- CalendarStream downloads the Calendar Sync link with `curl` (it identifies itself honestly;
  United's bot protection holds Python's HTTP clients) and only fetches it again when it changed.
- Events keep United's IDs, times and details, except: day codes (RDO, HDO…) and other items with no
  end become all-day or `DEFAULT_EVENT_HOURS` long, and 24-hour events (CCS+ writes full days as
  00:01–23:59:59) become all-day with the original times in the notes.
- A failed download or a suddenly empty calendar keeps the previous schedule.
- If the download is blocked, open the Calendar Sync link in a browser and use **Upload & publish**
  under the health bar.
- **Sign-in rejected** means CCS+ refused the UID or password; after two rejections, automatic
  checks pause so your account isn't locked (press **Sync now** after fixing them).

## The status page

- **Month view:** the schedule as it's sent to Google. Click an event to see or **Edit** it (title,
  times, notes, or hide it from Google), or **+** to add your own. Edits survive new downloads; ✎ marks
  an edited event, ⚠ one United changed since. Nothing is ever changed in CCS+.
- **Status & setup:** the calendar's name and colour, and **tags** (e.g. RDO in red) matched by whole
  word, contains, starts with or exact title. Below: the health bar, **Sync now**, the check
  interval, the upload, the feed links, and Setup.
- **Activity log:** each check and what changed, plus the last download for debugging.
- **☰ Settings:** status-page login, public address, Google Calendar.
- **Language** (🌐, left of the Light / Dark / System theme switch): English, Español, Français,
  Deutsch, Português and Vlaams, or Automatic (the browser's language). Everything on the page is
  translated, including status messages and the activity log; event titles stay as United sends
  them. The shareable subscribe page uses each visitor's browser language.
- `GET /api/status` and `GET /healthz` for monitoring.

## Syncing straight to Google Calendar

CalendarStream writes the schedule into a calendar it creates in your Google account. It only asks
for access to **calendars it created** and your e-mail address, so it can't see your other calendars.

- Events from the first of the current month onward, with your edits, without reminders; CCS+'s
  "free" items stay free. Older events are left alone.
- Tags become the nearest Google event colour (Tomato, Basil, Peacock…); the calendar's name follows
  the status page.
- Changes reach Google within seconds. A daily check (or **Sync now**) puts back events changed or
  deleted in Google and makes a new calendar if it was deleted.

**Setup:** ☰ → Google Calendar has a step-by-step guide to creating a free OAuth client in Google
Cloud. Paste its client ID and secret (checked with Google straight away), then **Connect**. Google
warns the app "hasn't verified" it because it's your own: choose **Advanced → Go to CalendarStream**.
One client serves the whole install, for up to 100 people while unverified. If you also subscribed
to the feed in Google, remove that calendar, or you'll see everything twice.

## Versions and releases

Versions are `0.y.z`. Each release has a git tag, a GitHub Release with its
[`CHANGELOG.md`](CHANGELOG.md) notes, and an image `ghcr.io/uuugh/calendarstream:<version>`
(`calendar_stream` up to 0.1.0). `beta` is the newest release; `latest` is the last one marked
stable (the `STABLE` file). The **Release** GitHub Action builds a release when `VERSION` changes
and moves `latest` when `STABLE` changes (or from **Actions → Release → Run workflow**).

## Data and backups

Everything is in the Postgres container `calendar_stream_db` (files in
`$MNT_DOCKER/calendar_stream/postgres`); the app container keeps nothing. Tables are created
automatically.

```bash
docker exec calendar_stream_db pg_dump -U ccs calendar_stream > calendar_stream.sql   # backup
docker exec -it calendar_stream_db psql -U ccs calendar_stream                         # look inside
```

**Starting over:** `docker compose down`, then delete `calendar_stream/postgres`. This erases
everything: edits, tags, settings, logins, the Google connection and the feed links.
