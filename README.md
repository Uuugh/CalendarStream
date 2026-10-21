# CalendarStream

Maintains a Google Calendar in sync with your United Airlines CCS+ schedule.

United Airlines' CCS+ does not provide a method to keep your Google Calendar up to date
automatically. United instead offers an official **Calendar Sync** download (`Calendar.ics`),
protected by your UID and a Calendar Sync password, which must be downloaded and re-imported into
Google Calendar by hand.

CalendarStream automates this process by downloading the official `.ics` file on a timer and
either:

1. writes it into a Google calendar of its own (updated within minutes, with rule colors), or
2. republishes it as a feed that Google, Apple Calendar and others can subscribe to.

Other calendars can be added the same way: any `.ics` / `webcal://` feed (another airline, work,
school, sports) becomes a source of its own, each with its own Google calendar and feed link. A
status page shows them all, lets you edit events, color or add events with rules, and walks you
through setup.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/calendar-dark.png">
    <img src="docs/screenshots/calendar-light.png" alt="The status page's month view: the schedule with RDO, VAC and SIM tag colors, a 12h/24h switch and a time-zone menu" width="760">
  </picture>
</p>

<details>
<summary>More screenshots: setup, adding an event, Settings</summary>
<p align="center">
  <img src="docs/screenshots/status.png" alt="Status &amp; setup: Tag Colors, CCS+ Calendar Sync and Google Calendar Autosync boxes" width="620"><br><br>
  <img src="docs/screenshots/event.png" alt="Adding an event: typed times with a time list, time zones and an event color" width="420">
  <img src="docs/screenshots/settings.png" alt="Settings: status-page login, public address and update checks" width="300">
</p>
<sub>Made-up demo schedule.</sub>
</details>

## Quick start

On any computer with Docker (Linux, macOS with Docker Desktop, or Windows in a WSL terminal), run the
installer below. For Google Calendar **Autosync** you also need a web address with your own domain
name, reached over `https://` (through a reverse proxy or a tunnel to this computer); without one,
use the feed instead.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)
```

[`install.sh`](install.sh) asks three questions (press Enter for the default):

1. which release to install, `latest` (stable) or `beta` (`stable`);
2. the folder for `docker-compose.yml` and `.env` (`~/stacks/calendarstream`);
3. the folder for CalendarStream's config and data, the database and `.secrets/` (the same folder).

It then downloads `docker-compose.yml` and `.env`, creates a random database password, starts
CalendarStream and prints its address and a **setup code**. Running it again updates
CalendarStream: the defaults are then your current settings, and your `.env` (apart from those
answers) and the database password are kept.

Then open the address it printed:

1. **Create your login** with the setup code.
2. **Calendar Sources → +** → **United CCS+ Calendar Sync**, then enter your CCS+ UID and Calendar
   Sync password. (Or add any calendar feed.)
3. **Calendar Destinations → +**: it first asks for the public `https://` address; check the
   spelling, because Google sends you back to exactly this address. Then add:
   - **Google Calendar Autosync** (recommended): follow its step-by-step guide in order. Publish the
     app, or add yourself as a test user, **before** pressing Connect; or
   - **Calendar feed**, and press **Add to Google Calendar** to subscribe to it instead.

## Settings

Everything is optional. Most settings are made on the status page; `.env` holds the rest, each
explained in [`.env.default`](.env.default):

| Setting | Default | Notes |
|---|---|---|
| `MNT_DOCKER` | the stack folder | Where the database (`calendar_stream/postgres`) and `.secrets/` live; the installer asks |
| `TZ` | `America/Chicago` | Time zone the schedule is shown in |
| `IMAGE_TAG` | `latest` | `latest` (stable), `beta` (newest) or a version, e.g. `0.1.6`; the installer asks |
| `PUID` / `GUID`, `RESTART` | `1000` / `100`, `unless-stopped` | |
| `FORWARDED_ALLOW_IPS` | `127.0.0.1` | Behind a reverse proxy: its address or network (e.g. `172.18.0.0/16`), so visitors' addresses and https are seen |
| `SYNC_INTERVAL_MINUTES` | `60` | 15–1,440, for CCS+; overridden by “Check for changes every” in its box |
| `CCS_CALENDAR_URL`, `CALENDAR_NAME` | United's link, "United CCS Schedule" | Overridden in the CCS+ Calendar Sync help and (edit) |
| `DEFAULT_EVENT_HOURS` | `1` | Hours for items with no end time, or `allday` |
| `ALLDAY_24H` | `true` | Show 24-hour (48 h…) events as all-day |
| `FEED_TOKEN` | made once | CCS+'s stream name (the secret part of its feed links); a stream name entered on the status page wins |

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
  in the CCS+ Calendar Sync box.
- **Sign-in rejected** means CCS+ refused the UID or password; after two rejections, automatic
  checks pause so your account isn't locked (press **Sync now** after fixing them).

## The status page

- **Month view:** every source's events, as they're sent to Google. Click the month and year to jump to any
  month; the **12h / 24h** switch (top right) picks the time format, and the time-zone menu next to
  the event count shows the calendar in another zone (on this page only; the feed and Google keep
  `TZ`). Click an event to see or **Edit** it (title,
  times, notes, or hide it from Google); clicking elsewhere closes it, and its 📌 pin keeps it open.
  Click an empty spot on a day (or **+**) to add your own. Events can have their own color (one of
  Google's 11), which wins over rules. Edits survive new downloads; ✎ marks
  an edited event, ⚠ one its source changed since. Nothing is ever changed in CCS+.
- **Calendar Sources** (**+** adds one; a new install has none): **United CCS+ Calendar Sync**
  (once) and **calendar feeds** (any `.ics` or `webcal://` link; repeating events are shown from a
  year back to two years ahead). Each source's box has its name and color (**(edit)**), status
  chip, check interval, **Sync now**, its login or link (CCS+'s with its step-by-step help; the
  login shows **✓ Validated** until you change it), CCS+'s hand upload, and its **Rules**:
  match a title (whole word, contains, starts with or exact title) and either **color** the event
  (e.g. RDO in red) or **add an event** from a template some time before the start, after the
  start or after the end (e.g. a 1:30 drive to the airport 2:00 before each trip). The bin removes
  a rule or the source.
- **Event templates:** ready-made events (title, length or all day, location, color) for those
  rules and for **Start from a template** when adding an event by hand.
- **Calendar Destinations** (**+** adds one; the first asks for the public address):
  **Google Calendar Autosync** (one Google calendar per source) and **Calendar feed** (a feed link
  and a shareable subscribe page per source). Each feed has a **stream name**, the secret part of
  its links: after a reinstall, or removing a source by mistake, enter the old one (or paste an
  old link) and existing subscriptions work again.
- **Activity log:** each check and what changed, for each source.
- **☰ Settings:** site settings only: the status-page login (with a show-password eye and a
  strength bar, like every password box), the public address, the **admin e-mail** (filled into the
  Google setup guide) and **Check for updates** (hourly, weekly, monthly or never; only versions of
  your release, stable or beta, are offered, and a newer one shows next to the version at the top).
- **Report a problem / Suggest a feature** at the bottom of the page open a GitHub issue form.
- **Language** (🌐, left of the Light / Dark / System theme switch): English, Español, Français,
  Deutsch, Português and Vlaams, or Automatic (the browser's language). Everything on the page is
  translated, including status messages and the activity log; event titles stay as United sends
  them. The shareable subscribe page uses each visitor's browser language.
- `GET /api/status` and `GET /healthz` for monitoring.

## Syncing straight to Google Calendar

CalendarStream writes each source into a calendar it creates in your Google account. It only asks
for access to **calendars it created** and your e-mail address, so it can't see your other calendars.

- Events from the first of the current month onward, with your edits, without reminders; CCS+'s
  "free" items stay free. Older events are left alone.
- Color rules become the nearest Google event color (Tomato, Basil, Peacock…); each calendar's name
  follows its source's. Removing a source deletes its calendar in Google.
- Changes reach Google within seconds. A daily check (or **Sync now**) puts back events changed or
  deleted in Google and makes a new calendar if it was deleted.
- **Instant updates from Google:** with a public `https://` address, CalendarStream asks Google to
  notify it (a webhook to `/google/notify`) whenever one of its calendars changes there, and puts back
  hand edits within seconds instead of at the daily check. Nothing to set up; it needs a valid
  certificate, and your proxy must let Google's POSTs to `/google/notify` through without a login.
  Without it, the daily check carries on as before.

**Setup:** the Google Calendar Autosync box has a step-by-step guide to creating a free OAuth client in Google
Cloud. Paste its client ID and secret (checked with Google straight away), then **Connect**. Google
warns it "hasn't verified this app" because it's your own: press **Continue** (or **Advanced → Go to
CalendarStream**), tick the calendar box and press **Continue**. The guide ends with a list of
Google's error messages and what to do about each.
One client serves the whole install, for up to 100 people while unverified. If you also subscribed
to a feed in Google, remove that calendar, or you'll see everything twice.

## Versions and releases

Versions are `0.y.z`. Each release has a git tag, a GitHub Release with its
[`CHANGELOG.md`](CHANGELOG.md) notes, and an image `ghcr.io/uuugh/calendarstream:<version>`.
`beta` is the newest release; `latest` is the last one marked
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
everything: sources, destinations, edits, rules, templates, settings, logins, the Google connection and the feed links.
