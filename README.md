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
school, sports) becomes a source. Destinations (Google calendars and feed links, as many as you
like) each pick which sources they get. A status page shows them all, lets you edit events, color
or add events with rules, and walks you through setup.

<p align="center">
  <img src="docs/screenshots/calendar-light.png" alt="The status page's month view in the light theme: the schedule and a work calendar, with RDO, VAC and SIM rule colors, the time zone, the views and the 12h/24h switch" width="49%">
  <img src="docs/screenshots/calendar-dark.png" alt="The same month view in the dark theme" width="49%">
</p>

<details>
<summary>More screenshots, light and dark: calendars, feeds, rules, event templates, adding an event, Settings, phone, activity</summary>
<p align="center">
  <img src="docs/screenshots/sources-light.png" alt="Calendars: United CCS+ Calendar Sync expanded (Site Address, Username, password, upload, its rules) and a work calendar feed (light theme)" width="49%">
  <img src="docs/screenshots/sources-dark.png" alt="The same in the dark theme" width="49%"><br><br>
  <img src="docs/screenshots/destinations-light.png" alt="Feeds: the Google account, a Google calendar and a calendar feed with its dates, sources, feed link and subscribe page (light theme)" width="49%">
  <img src="docs/screenshots/destinations-dark.png" alt="The same in the dark theme" width="49%"><br><br>
  <img src="docs/screenshots/rules-light.png" alt="All Rules: color and emoji rules, a Create event rule and the two predefined rules, highest priority first, with the calendars each applies to and its handle (light theme)" width="49%">
  <img src="docs/screenshots/rules-dark.png" alt="The same in the dark theme" width="49%"><br><br>
  <img src="docs/screenshots/templates-light.png" alt="Event Templates: a drive to the airport and a day off (light theme)" width="49%">
  <img src="docs/screenshots/templates-dark.png" alt="The same in the dark theme" width="49%"><br><br>
  <img src="docs/screenshots/rule-dialog-light.png" alt="The rule dialog: If Text whole word VAC, Then Color Basil and an emoji in front of the title (light theme)" width="45%">
  <img src="docs/screenshots/rule-dialog-dark.png" alt="The same in the dark theme" width="45%"><br><br>
  <img src="docs/screenshots/event-light.png" alt="Adding an event: calendar, template, title, times, time zone, location, notes and color (light theme)" width="49%">
  <img src="docs/screenshots/event-dark.png" alt="The same in the dark theme" width="49%"><br><br>
  <img src="docs/screenshots/settings-light.png" alt="Settings: status-page login, public address, admin e-mail and updates (light theme)" width="40%">
  <img src="docs/screenshots/settings-dark.png" alt="The same in the dark theme" width="40%"><br><br>
  <img src="docs/screenshots/phone-light.png" alt="On a phone: the list view, with TZ and the view button (light theme)" width="30%">
  <img src="docs/screenshots/phone-dark.png" alt="The same in the dark theme" width="30%"><br><br>
  <img src="docs/screenshots/activity-light.png" alt="Activities and Logs: each source's last check and the log (light theme)" width="49%">
  <img src="docs/screenshots/activity-dark.png" alt="The same in the dark theme" width="49%">
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

[`install.sh`](install.sh) asks four questions (press Enter for the default):

1. which release to install, `latest` (stable) or `beta` (`stable`);
2. the folder for `docker-compose.yml` and `.env` (`~/stacks/calendarstream`);
3. the folder for CalendarStream's config and data, the database and `.secrets/` (the same folder);
4. whether to allow updating from the status page (`no`): yes adds a small updater container (see
   [Updating](#updating)).

It then downloads `docker-compose.yml` and `.env`, creates a random database password, starts
CalendarStream and prints its address and a **setup code**. Running it again updates
CalendarStream: the defaults are then your current settings, and your `.env` (apart from those
answers) and the database password are kept.

Then open the address it printed:

1. **Create your login** with the setup code.
2. **Calendars → +** → **United CCS+**, then enter your CCS+ Username (UID)
   and Calendar Sync password. (Or add any calendar feed.)
3. **Feeds → +**: it first asks for the public `https://` address; check the
   spelling, because Google sends you back to exactly this address. Name the destination, then add:
   - a **Google calendar** (recommended): in the **Google account** box, follow the step-by-step
     guide in order. Publish the app, or add yourself as a test user, **before** pressing Connect; or
   - a **Calendar feed**, and press **Add to Google Calendar** to subscribe to it instead.

## Settings

Everything is optional. Most settings are made on the status page; `.env` holds the rest, each
explained in [`.env.default`](.env.default):

| Setting | Default | Notes |
|---|---|---|
| `MNT_DOCKER` | the stack folder | Where the database (`calendar_stream/postgres`) and `.secrets/` live; the installer asks |
| `TZ` | `America/Chicago` | Time zone the schedule is shown in |
| `IMAGE_TAG` | `latest` | `latest` (stable), `beta` (newest) or a version, e.g. `0.2.7` or `0.2.7-beta.1`; the installer asks |
| `COMPOSE_PROFILES` | empty | `updater` adds the updater behind **Update now** ([Updating](#updating)); the installer asks |
| `PUID` / `GUID`, `RESTART` | `1000` / `100`, `unless-stopped` | |
| `FORWARDED_ALLOW_IPS` | `127.0.0.1` | Behind a reverse proxy: its address or network (e.g. `172.18.0.0/16`), so visitors' addresses and https are seen |
| `SYNC_INTERVAL_MINUTES` | `60` | 15–1,440, for CCS+; overridden by “Check for changes every” in its box |
| `CCS_CALENDAR_URL`, `CALENDAR_NAME` | United's link, "United CCS Schedule" | Overridden in the CCS+ box (Expand) |
| `DEFAULT_EVENT_HOURS` | `1` | Hours for items with no end time, or `allday`; the Items-without-an-end-time rule overrides it, and a new install's rule starts from it |
| `ALLDAY_24H` | `true` | Whether a new install starts with the 24-hour-events rule (24 h, 48 h… events shown as all-day) |
| `FEED_TOKEN` | made once | The stream name of the feed made when upgrading from before 0.2.1; feeds' stream names are set on the status page |

**Secrets.** The files are `.secrets/DB_PASSWORD.txt` and `.secrets/UPDATER_TOKEN.txt`, made by the installer. The status-page
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
- **Sign-in rejected** means CCS+ refused the Username or password; after two rejections, automatic
  checks pause so your account isn't locked (press **Sync Now** after fixing them).

## The status page

- **Calendar:** every source's events (views, months and the time zone change in place, without
  reloading the page). On the right: the **Time Zone** it's shown in (**TZ** when
  space is tight; on this page only, the feeds and Google keep `TZ`), **Month / Week / Day / List**, the **12h / 24h** switch,
  and **Print** (Print Preview, below). Click the title to jump to any month. Click an event to
  open it; it stays open (also while the calendar is redrawn) until its **Close**. On the right of
  its details: the bell (**reminders**: up to five, from "at the start" to "1 week before", sent to
  Google and written into the feeds), **✎ Edit** (title, times, notes, or hide it), **duplicate**
  and **delete** (a source's own event is hidden instead, since the source would send it again).
  Click an empty spot on a day (or **+**) to add your own. On a computer, adding and editing an
  event (and the rule dialog) open in a pop-up; on a phone they're a full page with a **←** back
  button. New events go into the top calendar (the **Default**). Events can have their own color (one of
  Google's 11), which wins over rules; otherwise all of a calendar's events (timed or all-day) share
  its color. The key under the calendar lists each calendar, "Added here" and the rules' colors.
  Edits survive new downloads; ✎ marks an edited event, ⚠ one its source changed since. Nothing is
  ever changed in CCS+.
- **Print Preview:** the pages as they'll print, with **Print**. Choose **Itinerary**, **Day**,
  **5-day** (Monday to Friday), **Week** or **Month**, with or without weekends, light or dark, and
  the dates (From / To); it opens with your last print's choices (or the calendar's view the first
  time). One page per month, week or day.
- The page's sections: **Calendar** at the top, then **Calendars**, **Feeds**, **All Rules**,
  **Event Templates** and **Activities and Logs**, each with a small icon and the same kind of
  section title row. On a wide screen they sit in two columns (Calendars | Feeds, All Rules |
  Event Templates), with Activities and Logs across the full width; on a narrow screen or a phone
  they're one column, the calendar opens on the List view, the view and theme switches become one
  button each that steps through the choices, and long labels get shorter ("Expand", "Check every
  60 min").
- **Look:** text in [IBM Plex Sans](https://github.com/IBM/plex), and anything you'd copy or type
  exactly (links, IDs, the Username, the client ID) in IBM Plex Mono; every icon is a
  [Material Symbol](https://fonts.google.com/icons). Everything is a rounded rectangle (8 px corners
  on controls, 12 px on sections and modules); nothing is pill-shaped. The fonts and icons come with
  CalendarStream, so the page never loads anything from elsewhere.
- A small **(?)**, raised after a word like a superscript, explains it: point at it, or click (tap)
  it to keep it open.
- Saving, cancelling and removing happen in place: only the parts of the page they change are
  updated, without reloading it. **Cancel | Save** is one 130 px pair at the bottom of a module and
  (**Cancel | Apply** in the rule dialog); the pressed side fills it and says **Cancelled** or
  **Saved** for 3 seconds, and a module's Cancel also closes it. A field changed in place (a login,
  a link) gets **✕ | ✓** icons instead.
- **Handles:** to the right of every module and rule line, **▲ ☰ ▼**: drag it by **☰**, or press ▲ ▼,
  to change the order (of the calendars, the feeds, or the rules' priority). It's saved at once.
- Spacing: 10 px between sections, 5 px between the modules in a section (14 px under a folded one,
  for its Expand line) and around subsection titles (Automatic Upload, Manual Upload, Rules), 2 px
  between everything else; text boxes and rule lines are 34 px rounded rectangles; instruction tiles
  ("How to …") keep their own size.
- **Calendars** (**+** adds one). A new install has one **Local** calendar: it holds the events you
  add here, and you can add more (**+ → Local calendar**). The top calendar is the **Default** (the
  one new events go into; its expanded module says so); remove it or move another above it, and the
  next becomes the Default. Other presets: **United CCS+** (once),
  **Google** and **Apple** calendars (by their private iCal link, with step-by-step help for finding
  it) and **Other** (any link starting with `webcal://` or ending in `.ics`; repeating events are
  shown from a year back to two years ahead). Each calendar is a **module**. Its header is 50 px
  tall and is all a folded module shows: its color (the color of its events; click it to change it),
  its title over its note (e.g. "CCS+ Calendar Sync"), "Last check was successful @ 07:59" (or
  failed; what changed is in Activities and Logs), and on the right "Next check @ 08:59" beside its
  status over **Sync Now**, in a box of the same size in every module. **Sync Now** says
  **Syncing…** at once, then pulses green (**Synced**) or yellow (**Failed**) and goes back to Sync
  Now; the status, the calendar and the log update in place, without reloading the page.
  **▸ Expand for Details or to Edit Configuration ◂** sits in a folded module's bottom border; it
  opens the rest (it opens by itself when something needs doing) and becomes a **Close** line under
  the header, and turns the title and note into fields of the same size:
  - **Automatic Upload:** the **Site Address** with **Check every … min** beside it, CCS+'s
    **Username** (your UID) and password (**✓ Validated** until you type; then **✕ | ✓** (Cancel and
    Save), and ✓ shows Saved → Verifying… → ✓ Validated or ✗ Failed, with the reason under the boxes),
    and step-by-step help: how to enable it on the left, what's **Accomplished** on the right.
  - **Manual Upload** (CCS+): upload Calendar.ics by hand.
  - **Rules:** the rules this calendar uses, highest priority first (its own first, then the shared
    ones), each marked **This calendar**, **All calendars** or **n calendars**. ✎ opens the rule
    dialog; the bin takes the rule off this calendar; the handle changes its priority. **+ Add a
    rule** offers **New rule…** or a rule another calendar uses.
  - At the bottom, under a line: **Remove** on the left (it asks first), **Cancel | Save** on the
    right.
- **Feeds** (**+** adds one; the first asks for the public address): what other apps subscribe to,
  independent of the calendars: **Google calendars** (Autosync; one **Google account** box signs in for all of them)
  and **Calendar feeds** (a feed link and a shareable subscribe page each), as many as you like.
  Each is a module with the same 50 px header as a calendar's (name over kind, its calendars and
  dates, status; the Google account's has **Sync Now**), and
  **▸ Expand for Details or to Edit Configuration ◂** opens the rest: the name, a **Start** and
  **End** date (empty = no limit), the calendars it gets, a feed's links, and Remove / Cancel | Save. Every event keeps its source's colors and rules. Each feed has a **stream name**, the secret
  part of its links: after a reinstall, or removing a feed by mistake, enter the old one (or paste
  an old link) and existing subscriptions work again.
- **All Rules** (folds to its title; **+** stays in the corner): every rule, highest priority first,
  with the calendars it applies to (**+** or ✎ opens the rule dialog, the copy button makes a copy
  for no calendar yet, the bin deletes it, the handle changes its priority). A higher rule wins over
  a lower one (for a color, an emoji or a time change), even a calendar's own. A rule is
  **If … Then …**:
  - **If** (no lines: every event): **Text** is / contains / whole word / begins with / ends with /
    regex (**Aa** for matching case); **Date** and **Time** is / after / before / between (a time
    range can go past midnight); **Day(s)** is / after / before / between (ctrl- or shift-click for
    several; Fri – Mon goes round the weekend); **Length** is (weeks : days : hours : minutes; 0 =
    no end time) or is whole days. Join lines with **and** / **or** (and goes first); click the grey
    **(** and **)** to group lines, the outer brackets in a different color.
  - **Then** (+ adds more): **Color**, **Add emoji to title**, **Create event** (a new one, or from
    an event template, some time before the start, after the start or after the end), **Change**
    (to all-day, with the original time in the notes, or to a length) and **Record changes** (when
    the source changes a matching event, a note on it and a line in Activities and Logs).
  - **Apply to** (ctrl or shift for several): **All calendars** (also ones you add later) or the
    ones chosen. A new rule applies to All; changing one keeps its choice. **Remove** deletes it.

  A new install starts with two rules for every calendar: **Items without an end time** (from
  `DEFAULT_EVENT_HOURS`) and **24-hour events** (shown as all-day; CCS+ writes full days as
  00:01–23:59:59). Rules from earlier versions are converted, in the same order.
- **Event Templates** (folds to its title; **+** stays in the corner): ready-made events (title, length or all day, location, color) for Add-event
  rules and for **Start from a template** when adding an event by hand.
- **Activities and Logs** (a module like the others): each check and what changed, for each source;
  each source's last download details (for debugging) at the bottom. Folded, it shows **Healthy**,
  or **Unhealthy** while a problem is still there (a calendar failing, a sign-in rejected, Google
  sync failing).
- **☰ Settings** (a light blue panel): site settings only: the status-page login (with a show-password eye and a
  strength bar, like every password box), the public address, the **admin e-mail** (filled into the
  Google setup guide) and **Check for updates** (hourly, weekly, monthly or never; only versions of
  your release, stable or beta, are offered, and a newer one shows next to the version at the top).
- **Report a problem / Suggest a feature** at the bottom of the page open a form: what happened (or
  your idea), and tick what to include: the Activities and Logs lines, each source's last download
  details, your device and setup, your contact details, and whether you'd like replies. Private
  details (your Username, links, stream names, e-mail addresses, the public address) are taken out;
  a preview shows exactly what's sent. **Open on GitHub** fills in a new issue there (its page is
  the link to follow it, and GitHub notifies you of replies); without a GitHub account, **Copy** or
  **Download** the report instead.
- **Language** (the globe, left of the Light / Dark / System theme switch): English, Español, Français,
  Deutsch, Português and Vlaams, or Automatic (the browser's language). Everything on the page is
  translated, including status messages and the activity log; event titles stay as United sends
  them. The shareable subscribe page uses each visitor's browser language.
- `GET /api/status` and `GET /healthz` for monitoring.

## Syncing straight to Google Calendar

CalendarStream writes each Google destination into a calendar it creates in your Google account,
with the events of the sources it ticks. It only asks
for access to **calendars it created** and your e-mail address, so it can't see your other calendars.

- Events within the destination's Start and End dates (all of them when empty), with your edits
  and only the reminders you set here (the bell on an event); CCS+'s "free" items stay free. Events before the Start are left alone.
- Each event gets the nearest Google event color (Tomato, Basil, Peacock…) to its own color, its
  rules' color or its calendar's color; each calendar's name follows its destination's.
  Removing a destination leaves its calendar in Google unless you tick "Also delete it in Google".
- Changes reach Google within seconds. A daily check (or the Google account's **Sync Now**) puts back events changed or
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

**Feeds on Android:** Google's Android app can't add a calendar by link, and a calendar added by
link on calendar.google.com stays hidden on the phone until it's turned on there: in the app,
**Settings →** the calendar **→ Sync**. The subscribe page explains this on Android and iPhone.

## Updating

Run the installer again: it keeps your settings and starts the newest image of your release.

Or, if you answered yes to updating from the status page, press **Update now** next to
"(v0.2.8 is available)" at the top of the page. The button shows **Downloading…** (with a moving
bar) while the new image is fetched, then **Restarting…** while CalendarStream starts again (the
page is unreachable for a few seconds), then disappears, and the version at the top shows the new
one. Behind it is the updater container, `calendar_stream_updater`:
[Watchtower](https://github.com/nicholas-fedor/watchtower), the maintained fork (the original,
containrrr/watchtower, was archived in December 2025).

- It only updates when you press the button (it never checks on its own), and only the
  CalendarStream container (it's labelled for it), never the database. Old images are removed.
- It needs Docker's socket (`/var/run/docker.sock`) to pull the image and restart the container,
  which is why it's optional. Its API isn't published on any port: only CalendarStream reaches it,
  inside the Docker network, with a random token in `.secrets/UPDATER_TOKEN.txt`.
- It works the same on Linux, macOS (Docker Desktop) and Windows (WSL). It's turned on by
  `COMPOSE_PROFILES=updater` in `.env`; run the installer again and answer no to remove it.
- An install pinned to an exact version (`IMAGE_TAG=0.2.7`) is updated with the installer.

## Versions and releases

Versions follow [semver](https://semver.org): `x.y.z` for a stable release, and `x.y.z-beta.N` for
the betas leading up to it (0.2.7-beta.1, 0.2.7-beta.2, … then 0.2.7). Each version has a git tag,
a GitHub Release with its [`CHANGELOG.md`](CHANGELOG.md) notes, and an image
`ghcr.io/uuugh/calendarstream:<version>`. `beta` is the newest version; `latest` is the last stable
one (the `STABLE` file). The **Release** GitHub Action builds a version when `VERSION` changes and
moves `latest` when `STABLE` changes (or from **Actions → Release → Run workflow**). A stable
install is only told about stable releases; a beta install about every newer version.

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

## License & Attribution

CalendarStream is free for **non-commercial use** under the
[PolyForm Noncommercial License 1.0.0](LICENSE.md): you may use, change and share it for any
non-commercial purpose, but not sell it or use it in a commercial product or service. Anyone who
passes it on must include the license and its required notice, which credits the author:

> Required Notice: Copyright 2026 Richard Friendlich (https://github.com/Uuugh/CalendarStream)

Because commercial use isn't allowed, this is "source-available" rather than open source in the
OSI sense. For commercial use, ask the author via a GitHub issue.

### Third-party fonts and icons

CalendarStream includes these, under their own licenses (a copy of each comes with it):

| What | By | License | Copy in this repository |
| --- | --- | --- | --- |
| [Material Symbols](https://github.com/google/material-design-icons) (Rounded, weight 400): every icon on the pages | Google | [Apache License 2.0](app/material_symbols/LICENSE) | `app/material_symbols/` |
| [IBM Plex Sans and IBM Plex Mono](https://github.com/IBM/plex): the pages' fonts | IBM Corp. | [SIL Open Font License 1.1](app/static/fonts/OFL.txt) | `app/static/fonts/` |

The icons are copied from the [`@material-symbols/svg-400`](https://www.npmjs.com/package/@material-symbols/svg-400)
package by `tools/vendor_icons.py`; the fonts are the `latin` and `latin-ext` files of
[`@fontsource/ibm-plex-sans`](https://www.npmjs.com/package/@fontsource/ibm-plex-sans) and
[`@fontsource/ibm-plex-mono`](https://www.npmjs.com/package/@fontsource/ibm-plex-mono) 5.3.0.
