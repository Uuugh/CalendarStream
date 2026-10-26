# Changelog

Versions follow [semver](https://semver.org): `x.y.z-beta.N` for betas (from 0.2.7-beta.1) and
`x.y.z` for stable releases; versions before 0.2.7 are `0.y.z`. Planned: 0.2 more calendar sources
and destinations, 0.3 backups, 0.4 more users, 0.5 notifications, 0.6 theming. Every version is
tagged `v<version>`; the newest is also tagged `beta`. The last stable one (in the `STABLE` file) is
the `latest` image and the GitHub Release marked **Latest**; when a version is released, its betas'
entries are gathered under its heading. Each version lists what was **added**, **changed**,
**fixed** and **removed**. Labels refer to that beta's request list: F = feature request,
I = issue, # = review item, R = README; numbers start again with each beta.

**Stable (`latest`): 0.0.6 · Newest (`beta`): 0.2.8-beta.14**

## 0.2.8-beta.14 — 2026-10-26

### Added
- **F1** ☰ Settings → Google Calendar API Sync: **Connect** in one straight line instead of Save,
  Validate and Connect in turn. One button in the status box goes **Saving… → Checking… → Checking
  address… → Opening Google…** and on to Google's sign-in. The first step that fails stops it
  (**Stopped**), and the line under it says what to fix as a click path, with **Copy** and **Open**
  buttons (e.g. Google Cloud › Clients › CalendarStream › Authorized redirect URIs › + Add URI › the
  address › Save › wait 5 min › Connect).
- **F2** The redirect address is checked with Google for real (Google's sign-in page is asked, without
  signing in): a missing address shows **Address missing** before you're sent to Google's error page.
  The guided setup's step 6 ticks itself only once Google confirms the address, and the "Set it up with
  Claude" request asks for it to be added while the client is created. (CalendarStream can't add the
  address to your client itself: Google offers no way to do that from an app.)
- **F3** Disconnecting, reconnecting and starting over, tested end to end: reconnect with the same client
  → the same Google calendar, no duplicate events; delete the client and set up a new one → a new
  calendar (Google only lets an app see the calendars it made), with the old one named in the log so
  you can delete it by hand; the Google feed says **Not connected** while disconnected, without errors.

### Changed
- **F4** One look per meaning, everywhere: **green** = done or OK; the **pressed** look (blue words on
  the box) = in action or waiting on you (Syncing…, Checking…, Downloading…, Restarting…, Update found,
  Update available, Ready to connect, Not checked, Not set up, Not connected, Not read yet, Setup
  needed, Paused, rule conflicts); **amber** = a problem outside CalendarStream (United, Google, GitHub,
  the internet); **red** = CalendarStream itself failed (Update failed, **Internal error**, a new status
  for an unexpected error while syncing a calendar); **blue** fills = buttons only.
- **F5** Words on the page are click paths and short lines (e.g. "calendar.google.com › Settings › the
  calendar › Integrate calendar › Secret address in iCal format"), not paragraphs: about 90 texts were
  trimmed, the guides, the guided Google setup and its troubleshooting, the add menus, feeds, rules,
  the report and the event pop-up included. The explanations stay in the (?).
- **R1** The theme rules (build_rules/theme.md and the Theme Rules pictures) are spelled out for anyone
  reviewing a change: the tokens; the one-look-per-meaning table with every status word; every
  transition with its trigger, style, duration, easing, hold and reduced-motion behaviour; the flows of
  Sync Now, Check now, Update now and Connect, frame by frame; and the click-path rule. Every written
  rule names its picture card. New Clarifications: one look per meaning; in-page instructions are click
  paths. The theme suite (suite 44) fails a status word in the wrong look, or a sentence on the page
  longer than 20 words.
- With reduced motion (the device's setting), status boxes, Expand / Close and Save no longer grow,
  slide or fade: each state simply replaces the last.

### Fixed
- **I1** Update now (top bar and ☰ Settings): the two copies now use the same words, colors and ending;
  the top bar's pill no longer blinks blank when pressed (only its words change); and on the way back
  the button shrinks first and then the status word fades in, instead of the box fading through itself.
- **I2** Connecting again after a disconnect (with the client's redirect address missing at Google) ended
  on Google's "Error 400: redirect_uri_mismatch" page with no hint here: Connect now stops before Google
  with the address to add and buttons to copy it and open the client (F1, F2).

## 0.2.8-beta.13 — 2026-10-26

### Fixed
- **I1** The two Update now buttons (the top bar's and ☰ Settings → Updates') weren't in step: the top
  bar said Downloading… then Restarting… while Settings said Updating…, and they ended at different
  times. Now whichever is pressed, both show the same words at the same moment (**Downloading…**,
  **Restarting…**, then **Updated** or **Update failed**) and go back together.
- **R1** Theme rules: **one action, one state**: the same action in more than one place (Update now;
  Sync Now for Google in Feeds and in Settings) shows the same progress, in the same words, in every
  copy at once. Checked by the tests (suite 47).

## 0.2.8-beta.12 — 2026-10-26

### Fixed
- **I1** ☰ Settings → Google Calendar API Sync, while it works: the credentials and Disconnect were
  under an Expand line that didn't show (it was drawn outside the menu), so the trash couldn't be
  reached. Now nothing is hidden: the header (account; Last synced and instant updates; Connected
  over Sync Now), then the credentials row (Client ID with Copy, Client secret, ✓ Connected, the
  trash), then a red **Remove** in the lower left (it disconnects, after asking) with **Also delete
  these calendars in Google** beside it. The explanations moved into the (?), the calendars and the
  last notice from Google into the header's tooltips.
- **I2** The theme rules gained: the status box is a multi-button (an overall status over the action
  that updates it, CCS+'s Healthy over Sync Now the model); a Settings group that works shows
  everything, nothing under Expand.

## 0.2.8-beta.11 — 2026-10-26

### Added
- **F4.1** The calendar has a **+** in its top right corner, like the other sections (adds an event).
- **F4.2** **Search**: the search icon (left of Time Zone) opens a search line: words found in titles,
  places and notes, one calendar or all, From and To (a year back to a year ahead when empty). Matches
  are listed by day as you type; ✕ closes it and brings the calendar back.
- **F3.4** The event pop-up's Location has a **map** button: it opens the place in Google Maps, to
  check it or find it.
- **F2.3** ☰ Settings → Google Calendar API Sync: the credentials row (Client ID, Client secret)
  ends with a **trash**, which asks first ("Delete the Google client ID and secret?"); while
  connected, it disconnects first (CalendarStream's calendars stay in Google).

### Changed
- **F1** A Google calendar's header says **Next push instantaneous** (each change goes at once).
- **F2.1** ☰ Settings → Updates: **Check for updates [Hourly ▾] ☐ Auto-update** on one line.
- **F2.2** ☰ Settings → **Update now** works like Sync Now: **Updating…** over the status box,
  then **Updated** (the page then reloads) or **Failed**. "Upgrade" has been gone since beta.9; a page
  still showing it is an older page: reload it.
- **F3** The event pop-up, laid out to the theme: **Calendar | Title** (the calendar as plain text
  when it can't be changed); the color, link, duplicate and delete beside **Location**, under the
  calendar; **All-day** and **The end is in a different time zone** on one line, above the times;
  **Starts | Ends**, each with its **Time** under it; the end is always **Ends** (no "Last day");
  "times in …" is gone; every field 34 px with a 12 px label, 2 px apart; Cancel | Save the theme's
  pair.
- **F5** **All Rules** and **Event Templates**: + moved out of the header, to the bottom right
  corner of the open section; Event Templates' Save is now the theme's Cancel | Save.
- **R1** New Clarifications in `build_rules/theme.md` (fields; + in a corner; the credentials trash;
  one line of settings; Next push instantaneous; an opened event's Close in the bottom left corner),
  each checked by the tests.

### Fixed
- **I2** An opened event in a narrow day: Close stays in the bottom left corner, and the icons go
  right-aligned on a line above it (they used to wrap under Close).
- The opened event's icons are 1 px smaller (25 px), with 1 px less space around them.

## 0.2.8-beta.10 — 2026-10-26

### Added
- **F5** **Two-way sync** with the Google calendars CalendarStream makes (only those): a change made
  there comes here as if made on the status page, so CCS+ is never touched. An edit of a CCS+ (or
  other source's) event becomes an edit; an edit of an event added here changes it; an event added in
  Google goes into a CalendarStream (local) calendar the Google calendar gets; a deletion hides the
  event (an added one is deleted). A rule's events stay read-only (put back). When both sides
  changed, the **newest change wins** (logged). **More than 3 deletions at once** wait at the top of
  Activities and Logs: **Hide them here too** or **Put them back in Google**. Repeating events made
  in Google aren't copied yet.
- **F1.2** ☰ Settings → Google Calendar API Sync, when the client is missing or failing, offers two
  ways to set it up: **Set it up with Claude** (a request to copy into a chat with Claude, who does
  the Google Cloud steps in your own signed-in browser; with how to link one) and the **Guided
  setup** (each Google page opens in a window beside CalendarStream; Copy buttons; the client and
  Connect steps tick themselves, the others are ticked by hand; the current step is marked).
- **F2.1** An opened event has a **link** icon, which opens it at "Linked to" (Move with it / Delete
  with it).

### Fixed
- **I1** An event added here showed the fixed purple "Added here" color instead of its calendar's
  color, which Google shows. Events now show the color Google shows: their own, their rule's, else
  their calendar's; "Added here" is gone from the key.
- Opening or closing a CalendarStream (local) calendar's module wasn't remembered.

### Changed
- **F1.1** "Google Calendar sync" is now **Google Calendar API Sync**. While it works, Settings shows
  only a module header (the account; Last synced and instant updates; Connected over Sync Now), with
  the details under Expand.
- **F2.2** An opened event: Close on the left, its icons on the right (on a line of their own in a
  narrow day). The edit pop-up's Notes take the room that's left, and its Cancel | Save is the
  theme's 130 × 34 pair (Save also when adding).
- **F3.1** Close's triangles point up.
- **F3.2** Pop-ups: a darker backdrop (55%) that keeps the page in view, and a 200 ms fade and
  scale-up (none with reduced motion).
- **F4** Rule lines with a title also say what the rule does ("Items without an end time → Change
  length to 1:00").
- **R1** New Clarifications in `build_rules/theme.md` (Close points up; pop-ups; an opened event's
  tools; event colors; rule lines), each checked by the theme suite.

## 0.2.8-beta.9 — 2026-10-26

### Fixed
- **I1.1** The top bar and ☰ Settings → Updates both say **Update now**.
- **I1.2** After an update, the page kept running the previous version's script and stylesheet:
  Settings → Check now then gave no sign it was pressed and sat over the status. The page now
  reloads once the new version is in (Settings stays open). Updating *to* this version still runs the
  old page: reload it once after that update.

### Changed
- **F1.1** Calendar and feed module headers: line 1 is the module's kind, fixed text in a larger font
  (17 px): **CalendarStream** (was Local), **United Airlines CCS+**, **Google Calendar**, **Apple
  Calendar**, **Calendar Feed**, **Google Calendar Feed**; line 2 its name (a field while expanded).
  On a phone the kind may take two lines rather than be cut off.
- **F1.2** A note shows as a raised **(i)** after the name, only when there is one; it's changed in a
  **Note** field under Close. The old default notes ("CCS+ Calendar Sync", "Events added here"…),
  which said what the kind now says, count as no note.
- **F1.3** No handle (▲ ☰ ▼) where there's nothing to reorder: a list of one module or one rule.
- **F2** **+ Add a calendar** ends with the standard **Cancel | Save** (was Add); Cancel closes it. The
  "Local" choice is now **CalendarStream**.
- **F3** **All Rules**: the rule lines' handles sit in the section's right margin, like the modules', so
  the lines are as wide as the header. (Read from "Event Templates", whose lines have no handles; the
  All Rules heading above it was empty.)
- **F4** ☰ Settings → Google Calendar sync, once connected, is laid out like a login, as before
  connecting: **Client ID** (with Copy) and **Client secret** (Saved), then **✓ Connected**; under
  them the account, the last sync and instant updates; **Also delete these calendars in Google** beside
  **Disconnect**. The small "OAuth client" box is gone.
- **F5** Settings → Updates says **Last checked 10:45** (was "Checked"), like Last synced.
- **R1** The theme is enforced by tests: `tests/suite_44.py` (the theme suite) checks the whole page,
  light and dark, computer and phone, against `build_rules/theme.md`, with a check for each
  Clarification; theme.md ("Enforced by tests"), basics.md (EOF checklist) and review.md (Reviewers)
  say so. New Clarifications: the module header (kind over name, (i) note), no handle for a list of
  one, Cancel | Save when adding, Client ID / secret laid out like a login, a reload after an update.

## 0.2.8-beta.8 — 2026-10-26

### Fixed
- **I1** ☰ Settings → **Check now** gave no sign it had been pressed: when the answer was the same as
  before, nothing on the page changed. It now works like Sync Now: **Checking…** at once, growing
  over the status box, then **Up to date** (a green pulse), **Update found** or **Couldn't check**
  (a yellow pulse), then back to Check now with Updates redrawn, every time it's pressed.

### Changed
- **R1** `build_rules/theme.md` → Clarifications: every button in a status box works like Sync Now
  (also in the Theme Rules pictures).

## 0.2.8-beta.7 — 2026-10-26

### Fixed
- **I1.1** ☰ Settings → Updates: the button for a newer version says **Update** (was "Upgrade").
- **I1.2** Once an update had installed, Settings → Updates still showed "Update available" with a
  button that did nothing, instead of going back to **Up to date** and **Check now**. After a Check
  now (Settings is redrawn in place), Update and the top bar's Update now could stop responding.
  Both buttons now keep working after any redraw, and Updates is redrawn when the new version is in.

## 0.2.8-beta.6 — 2026-10-26

### Changed
- **I1** A module's handle (▲ ☰ ▼) sits in its section's right margin instead of taking room beside
  the module: calendars and feeds are now as wide as their section header (their right edge lines
  up with the +).
- **R1** `build_rules/theme.md` has a **Clarifications** list: the Developer's decisions about how the
  page looks (the handles, the module header layout, the status words, + in the corner, a box only
  for what can be changed, Copy inside its field, rule colors, Light = Soft). The Theme Rules
  pictures show it as part 2's last card, read from theme.md each time they're drawn; part 2's
  module and handle rules were updated to match.

## 0.2.8-beta.5 — 2026-10-26

### Added
- **F1.1** ☰ Settings → Google Calendar sync: a **Copy** button inside the Client ID box, laid out like
  the Status-page login's Password box (the button sits in the field). The client secret has no Copy:
  once saved it's sealed and never sent back to the page.
- **F7** Light mode now uses the softer palette (warm off-white background, quieter lines, muted
  blue accent and gentler event colors). It keeps the name **Light** and its icon; Dark is unchanged.

### Changed
- **I1** A rule's **Color** picks from Google Calendar's 11 event colors (Tomato, Flamingo, … Graphite)
  instead of a free color picker, so a rule's color is always one Google can show. A rule saved
  earlier with another color shows the nearest of the 11 when it's opened.
- **F1.2** ☰ Settings → **Updates** is laid out like a module header, always open: Updates and the
  channel (Stable or Beta versions) on the left, "Checked …" / "Next check @ …" on the right, then
  the status box (Up to date, Update available or Not checked) with **Check now** or **Upgrade**.
  Under it, **Check for updates** and **Auto-update** are changed in place.
- **F2** Rule lines everywhere read **Color ■ (Name)**: the color block right after "Color", the
  color's name in parentheses (e.g. "RDO" → Color ■ (Tomato)).
- **F3** **All Rules**: the + is in the top right corner, after the count box.
- **F4** **Event Templates**: the + is in the top right corner, after the count box.
- **F5** A calendar's header says **Last synced 00:31** (or **Sync failed 00:31**) instead of "Last
  check was successful @ 00:31"; feeds use the same words.
- **F6** Calendar and feed module headers share one layout: line 1, the color (calendars only), the
  name, then on the right the last sync and the status box (Healthy…); line 2, the note, then on the
  right "Next check @ …" and Sync Now. A line with nothing to say is left blank (Local has no sync,
  a feed has no next check). A feed shows **Last read by Google …** or **Last read …** (when an app
  last fetched it); a Google calendar **Last synced …**. A feed's calendars and dates moved into
  the header's tooltip.
- **R1** The CalendarStream Theme Rules pictures (`build_rules/`, Light and Dark) show the whole
  page with each part named where it is, a module open in every section, and the Close bar.

### Removed
- **F1.3** "Updater: running, so updates can be installed from this page." It said nothing the
  Upgrade and Auto-update controls don't; a note remains only when the updater isn't set up.

## 0.2.8-beta.4 — 2026-10-26

### Added
- **F1** **Google Calendar sync** moved from Feeds into **☰ Settings**: the step-by-step guide, Client ID
  and secret, Connect / Disconnect, the account and its last sync. **Feeds → + → Google Calendar** is
  then a calendar kept in sync through the Google API when Google Calendar sync is set up, and
  otherwise a feed for your Google account to subscribe to (with a pointer to Settings for colors,
  reminders and updates within seconds). **Sync Now** for Google is on each Google calendar's module.
- **F2** A feed's module leads with its buttons, **Add to Google Calendar** (first for a Google feed),
  **Add to Apple / Outlook** and **Open subscribe page**, then the **Feed link** with Copy, for any
  other calendar app or if a button doesn't work. "+ → Calendar feed" is now **Apple, Outlook or
  another app**.
- **F3** The test suites are in the repository (`tests/`, with `tests/run.sh` and a README), using the
  made-up demo schedule only.
- **F4** How work is done here moved into `AGENTS.md` (for any agent) and `build_rules/` (basics,
  deploy, review, theme, roadmap); `CLAUDE.md` now loads the basics and points to the rest. Every
  EOF runs the tests and pip-audit before a beta is published; Deploy step a runs the tests, step b
  all three scans.

### Changed
- **F5** Caching: the page's stylesheet and script are now files the browser keeps for the version
  (sent compressed), instead of being inside every page (and every in-place save); the fonts are
  kept a year; an unchanged feed answers "304 Not Modified"; an event's tools (Close, reminders,
  edit, duplicate, delete) are made when it's opened, from one copy in the page. The page is about
  a third smaller, the calendar much more.
- **#1** (security) FastAPI 0.162 and Starlette 1.10 (from 0.115 and 0.46.2): fixes Starlette's
  known problems (pip-audit: 7 advisories, among them one that let anyone tie up the server with a
  crafted Range header on `/static`).

### Fixed
- If the database wasn't ready within 10 seconds at start-up, CalendarStream kept retrying a
  connection that could never open, and stopped after a minute.
- After the FastAPI upgrade, a field sent empty (a calendar's note cleared, a feed's End date, an
  empty Site Address) was read as "not sent"; those are read as sent again.

## 0.2.8-beta.3 — 2026-10-25

Three request lists, merged into one beta (the third continues the numbering: F5–F10, I3–I7).

### Added
- **F1.1** The **theme rules** picture ([light](docs/theme-rules-light.png) ·
  [dark](docs/theme-rules-dark.png)) is kept in the repository and redrawn whenever the theme
  changes; it now also shows the handles, pop-ups and drop-downs.
- **F3.1** **Removing a calendar** asks what becomes of its events: **keep them in a Local
  calendar** (same name and color, in its place, in its feeds, with its own rules; the default),
  **add them to another calendar**, or **delete them**.
- **F3.2** **Linked events:** the link icon on the event page links an event to another one (events
  within three weeks, in any calendar), with **Delete with it** and **Move with it** (e.g. a drive
  to the airport that follows its trip). The event's details on the calendar say what it's linked to.
- **F5** Settings → Updates: an **Auto-update** tick box, left of Check now: with the updater, a newer
  version of your release (stable or beta) is installed by itself (once per version; greyed out
  without the updater).
- **F1.4** The theme rules picture is now **docs/CalendarStream_Theme_Rules.png** (and
  **…_Dark.png**), titled "CalendarStream Theme Rules", and starts with the page itself, its parts
  numbered and named (section, section header, module, module header, color box, status lines,
  status box, Sync Now, handle, Expand / Close line, rule line, count box…).
- **F4.2** **Conflicting rules:** when a lower rule can never set a color, an emoji or a time change
  because a higher one matches the same events (for some of the same calendars), or two rules are
  the same, All Rules says so (and "n to check" beside its title), with what can be done: **Put it
  first**, **Take the color (emoji, time) out of it**, **Merge them**, or **Keep as is** (not shown
  again).

### Changed
- **F1.2** While **Sync Now** syncs (and says Synced / Failed), Healthy goes away and the button
  fills the status box, its state in the middle. The rest works as before.
- **F1.3** Every **(?)** sits right after the word it explains; the calendar key's and a feed's
  Start / End (?) were at the right of their row.
- **F2** Settings:
  - **F2.1** The theme's spacing (5 px between groups and titles) and its saving rules: Public
    address and Admin e-mail show **✓ Saved** until you type, then **✕ | ✓**, like the login.
  - **F2.2** When a newer version is out, **Upgrade** replaces **Check now** (it runs Update now, or
    without the updater links to how to update).
- **F3.3** A calendar's status lines ("Last check was successful @ 20:10", "0 events added here")
  are on the right, beside its status.
- **F3.4** A calendar's color box changes its color only while the module is expanded, like its title
  and note.
- **F4.1** **Apply to** is a drop-down of the calendars, each with its color. A rule made in a
  calendar starts with that calendar; one made in All Rules with All calendars.
- **F4.3** Choosing a **)** with no **(** before it adds the **(** on the first line of its group (the
  rule's first line at the top), which flashes.
- **F4.4** A line's brackets end with the chosen **)** first, then the grey one.
- **F6** A rule's calendars badge (in a calendar's rules and in All Rules) is in the color of the
  calendar it applies to, in stripes of each calendar's color when it applies to several, and white
  for All calendars.
- **F7** **All Rules** looks like a module: its (?) right after the title, then **+** and a box with
  the number of rules on the right (green, or yellow with "n to check" while a rule conflicts), and
  an **Expand for Details** / **Close** line instead of the ▸. **How rules work** moved from under
  the rules to the bottom of the rule dialog.
- **F8** Theme: a section title's (?) is raised right after the title; **Sync Now**'s words are
  centered in it, and it grows over the status box and shrinks back smoothly (it no longer jumps
  when the module's header is refreshed).
- **F9** **Event Templates** looks the same way: Expand / Close line, and "**2 Templates**" in a box
  on the right.
- **F10** **Activities and Logs** opens only from its Expand line (a click on its header no longer
  opens it); the latest line sits on the right of its header, by Healthy.

### Fixed
- **I1** Rule dialog: **Change → to a length of** didn't show its length field (and **Create event →
  New event…** didn't show its fields).
- **I2** A calendar module's rules didn't list the shared rules that apply to it: rules converted
  from earlier versions that every calendar used were kept for those calendars only, so the Local
  calendar (and calendars added later) didn't get them. They're now for All calendars.
- A new feed with no name and the Google calendar name suggested are no longer "Local".
- **I3** The calendar key, the feeds' calendar colors and the rule badges follow a calendar's new
  color straight away.
- **I4** A second (and later) color change on a calendar module wasn't saved.
- **I5** Settings are saved in place: only Settings (and what depends on them, such as the feed
  links) are redrawn, without reloading the page. (A new status-page password still reloads it,
  as the browser must sign in again.)
- **I6** Settings follow the theme's layout: Check for updates is a label over its menu, with
  Auto-update and Check now (or Upgrade) beside it, all 34 px.
- Saving Public address or Check for updates in place went to the wrong address (a button named
  "action" hid the form's address).

## 0.2.8-beta.2 — 2026-10-25

### Added
- **F1.2** **Handles:** every module (calendars, feeds) and every rule line has a handle on its
  right, outside the box: **▲** above, **☰** to drag, **▼** below. The order is saved at once (the
  calendars' order, the feeds' order, the rules' priority).
- **F1.3** On a computer, adding or editing an event and the rule dialog open in a **pop-up**; on a
  phone they're a full page with a **←** back button.
- **F2.1** **Print Preview** with a **Print** button: **Itinerary**, **Day**, **5-day** (Monday to
  Friday), **Week** or **Month**; **include weekends**; **light** or **dark**; a date range (From /
  To). It opens with the last print's choices (the first time, the calendar's view).
- **F2.2.5** An event's **reminders** (the bell): up to five, from "at the start" to "1 week
  before", sent to Google Calendar and written into the feeds.
- **F3.1** A **(?)** next to **Calendars**.
- **F3.2** The **Local** calendar: a kind of calendar for events added here.
  - **F3.2.1** Every install gets one, at the top, so it's the default calendar for new events
    (upgrades too, once; it's in every feed).
  - **F3.2.2** Its (?) says so.
  - **F3.2.3** Removed, the calendar below it becomes the default.
  - **F3.2.4** **+ → Local calendar** adds another.
- **F3.3** The top calendar is the **Default**: its expanded module says so in the upper right,
  under the Close line.
- **F4** **All Rules** (was Rule Templates): every rule is **If … Then …**.
  - **If:** conditions joined by **and** / **or**, with grey **(** **)** brackets that turn white
    when chosen (the outer brackets in a different color). **Date** and **Time**: is / after /
    between / before. **Day(s)**: the same, choosing several days with ctrl / shift. **Length**:
    weeks : days : hours : minutes. **Text**: is / contains / begins with / ends with / regex.
  - **Then** (+ after the last adds more): **Color**, **Add emoji to title**, **Create event** (a
    new one, or from an event template) and **Change** (to all-day, or to a length).
  - An instruction tile at the bottom. A higher rule wins over a lower one, even a calendar's own.
    A new rule applies to All calendars; changing one keeps its choice.
  - The footer: **Remove** … **Cancel | Apply**, with **Apply to** (ctrl / shift: **All
    calendars** and each calendar).
  - Each calendar module lists its own rules above the shared rules it uses; every list of rules
    can be reordered with its handles.
  - Rules from earlier versions are converted, in the same order and for the same calendars.

### Changed
- **F1.1** The expand line becomes a **Close** line while a module is open; **Cancel** also closes
  it.
- **F2.2** Events:
  - **F2.2.1** An expanded event stays expanded (also when the calendar is redrawn).
  - **F2.2.2** No pin.
  - **F2.2.3** **Close** where **Edit** was.
  - **F2.2.4** The event's icons are on the right: reminders, edit, copy, bin.
- **F3.4** The module header's color box always shows the calendar's color (the color of its
  events).
- **F3.5** **Next check @ 14:49** is on the right, beside Sync Now.
- **F3.6** "98 events @ 14:34 (0 new, 0 removed)" is now **Last check was successful @ 14:34** (or
  **failed**); what changed is in Activities and Logs.
- **F3.7** **How to enable CCS+**, step by step:
  1. Open CCS+ Schedule (<https://ccsplus.ual.com/schedule/>) → Settings → Calendar syncing.
  2. Enable calendar export / syncing.
  3. Site Address: if the CCS+ link differs, press **Copy link** and replace the Site Address.
  4. Edit calendar sync settings → Include Trips Enabled → As a single event → enable all available
     options → Save → Back to Calendar syncing.
  5. Change Password → use a password just for Calendar Sync, not your CCS login.
  6. Enter the Username (Uxxxxxx) and the Calendar Sync password\*, then Save.
  7. The list on the right turns green.

  \* The password is stored encrypted.
- **F5** **Activities and Logs** follows the module rules (it folds the same way). Folded, its
  right side says **Healthy**, or **Unhealthy** while a problem is still there.
- **F6** The feeds follow the theme rules.
- Google's note: events are copied with only the reminders set here.

### Fixed
- **I1** An **Accomplished** line wraps under its first word, not under the check mark.
- **I2** Pop-ups and pages use the same padding and margins as the rest.
- **I3** The color box in a calendar module's header changes the calendar's color, like the other
  fields.
- The (?) next to **Apply to** in the rule dialog showed its explanation all the time.
- ▲ / ▼ were hidden on every rule line of the bottom calendar module.
- A new feed with no name is named after the first calendar that isn't a Local one.

### Removed
- The pin on an event, and closing an event by clicking elsewhere.

## 0.2.8-beta.1 — 2026-10-25

The first beta of 0.2.8 (EOF b); it includes everything in 0.2.7-beta.1 to beta.6, which weren't
released as a stable 0.2.7.

### Added
- **F1.5** A **License & Attribution** section in the README (CalendarStream's license, and the
  fonts' and icons' licenses), linked from the page's footer.

### Changed
- **F1** General:
  - **F1.1** **Sync Now** is the same rounded rectangle in every module, and answers at once: it
    says **Syncing…**, then pulses green (**Synced**) or yellow (**Failed**), then says Sync Now
    again. The Google account's Sync Now moved into its module header and works the same way.
  - **F1.2** The **(?)** is a small help icon, raised like a superscript right after the word it
    explains.
  - **F1.3** "Canceled" is spelled **Cancelled**.
  - **F1.4** Fields changed in place (a login, a link, a rule line) get **✕ | ✓** icons (Cancel and
    Save) instead of words. Cancel | Save at the bottom of a module and in the rule dialog keep
    their words.
  - **F1.6** Theming:
    - **F1.6.1** No pills: everything is a rounded rectangle (8 px corners on controls, 12 px on
      sections and modules), including status chips, the ✓ Validated slot, rule lines, the 12h /
      24h switch and today's date.
    - **F1.6.2** Every icon is a [Material Symbol](https://fonts.google.com/icons) (Rounded): the
      section icons, the language, theme, Settings and Print buttons, the arrows, +, ✎, the bin,
      copy, pin, the password eye, the status chips (each with its own icon) and the setup
      checklists.
    - **F1.6.3** An image of the theme rules (sent with this beta).
    - **F1.6.4** The standard font is **IBM Plex Sans**.
    - **F1.6.5** The typed font, **IBM Plex Mono**, is used in fields that hold code: links, IDs,
      the Username, the client ID and the stream name.
    - **F1.6.6** Each calendar and feed is a **module**:
      - **F1.6.6.1** Its header, which is also all a folded module shows (from the Developer's
        mockup): the color; the title over the note, each in a box (fields of the same size while
        expanded); the last download over the next check; the status over Sync Now.
      - **F1.6.6.2** Every module header is **50 px** tall (on a narrow screen the two status lines
        go under it).
      - **F1.6.6.3** Folded, there's no line under the header: **▸ Expand for Details or to Edit
        Configuration ◂** sits in the module's bottom border.
- The fonts and icons come with CalendarStream (served from `/static`), so the pages never load
  anything from elsewhere. `/api/status` also reports Google's sync (`google`).

## 0.2.7-beta.6 — 2026-10-24

### Added
- **F1.1** A **(?)** next to a title or button explains it: point at it, or click (tap) it to keep it
  open (Escape or a click elsewhere closes it). The longer explanations moved behind one: the rules
  in a calendar, Rule Templates, Event Templates, Feeds, a feed's dates and calendars, Add to Google
  Calendar, Share it, and Settings' public address and admin e-mail.
- **F1.3** A small icon left of each section title (F4.2: a streaming icon for Feeds).
- **F2.1** **Print** in the calendar's upper right corner: prints the calendar as it's shown (that
  view and month), without the rest of the page.

### Changed
- **F1** General:
  - **F1.2** Every "Configure" reads **"Expand for Details or to Edit Configuration"** ("Expand" on a
    phone).
    - **F1.2.1** 5 px above it.
  - **F1.4** Every Cancel and Save form one **130 × 34 px** rounded rectangle, 65 px each, in the
    same colors and text size (the calendars' and feeds' bottom lines, and the rule dialog; on a
    rule line, 130 × 26 px to fit inside its 34 px line). The pressed side fills the rectangle and
    says **Canceled** or **Saved** (or **Saving…** while it's sent) for 3 seconds, then it's back.
    The ✓ Validated box keeps its own half width.
  - **F1.5** Saving, cancelling and removing refresh only the parts of the page they change, without
    reloading it (anything being typed elsewhere stays).
  - **F1.6** Section title row: gap 5 px.
  - **F1.7** Subsection titles (Automatic Upload, Manual Upload, Rules): 5 px above and below.
  - **F1.8** Everything else in a section: 2 px apart vertically.
  - **F1.9** Rule lines and text boxes: 34 px rounded rectangles.
  - **F1.10** Instruction tiles ("How to get a Calendar Sync link, ID and secret (step by step)") keep
    their size (38 px) and spacing (12 px above).
- **F3** Calendar Sources:
  - **F3.1** Renamed **Calendars** (and "All sources" on a rule line reads "All calendars").
  - **F3.2** A line above Remove / Cancel | Save.
  - **F3.3** "How to enable CCS+" and "Accomplished" are underlined.
- **F4** Calendar Destinations:
  - **F4.1** Renamed **Feeds**, with a (?): what other apps can subscribe to; CalendarStream delivers
    your calendars to them. A feed's box now ends like a calendar's: Remove on the left (it asks
    first), Cancel | Save on the right.

### Fixed
- **I1** Calendar:
  - **I1.1** Timed and all-day events had colors of their own (and all-day events turned green) that
    were never set. Now all of a calendar's events share its color; only a rule, an event's own
    color or "Added here" change it.
  - **I1.2** Timed and All-day are gone from the key; it lists each calendar, "Added here" and the
    rules' colors.

## 0.2.7-beta.5 — 2026-10-23

### Added
- **F2.3** Calendar Sources → +:
  - **F2.3.1** Presets: **United CCS+**, **Google**, **Apple** and **Other**. Google and Apple
    calendars connect by their private iCal link, in the same box as United CCS+, with step-by-step
    help for finding the link.
  - **F2.3.2** Everything built for CCS+ (Automatic Upload, setup help, Manual Upload) is the United
    CCS+ preset of one source box shared by all of them.
  - **F2.3.3** "CCS+ Calendar Sync" is now the CCS+ source's note, like any other source's note
    (it can be changed or emptied).
- **F3.2** Rule Templates: each rule can be changed (✎), copied or deleted.
- **F3.3** A new kind of rule, **Record changes**: when the source changes a matching event (its
  time, title or location; every event when nothing is entered to match), a note is added to the
  event ("Changed Oct 22: time … → …") and a line goes in Activities and Logs. A moved occurrence of
  a repeating event counts as a change, and a dropped event is logged.
- **F5** Report a problem / Suggest a feature open a form instead of a bare GitHub page: what
  happened (or the idea), with each thing to include ticked separately: the Activities and Logs
  lines, each source's last download details, device and setup, contact details, and whether you'd
  like replies. Private details (Username, links, stream names, e-mail addresses, the public
  address) are taken out, and a preview shows exactly what's sent. **Open on GitHub** fills in a new
  issue (its page is the link to follow it; GitHub notifies the author of replies). Without a GitHub
  account, the report can be copied or downloaded; it can't be sent from the page without one.

### Changed
- **F2** Calendar Sources:
  - **F2.1** The source box follows the mockup:
    - **F2.1.1** **Automatic Upload** first, then **Manual Upload** (CCS+), then **Rules**.
    - **F2.1.2** "Check every … min" sits beside the Site Address.
    - **F2.1.3** The header shows the next scheduled check ("Next scheduled check @ 10:20pm").
    - **F2.1.4** The setup help has two sides with a line between them:
      - **F2.1.4.1** **How to enable CCS+** (the steps) on the left, **Accomplished** (the checklist)
        on the right.
    - **F2.1.5** Rules:
      - **F2.1.5.1** Thinner lines.
      - **F2.1.5.2** Rules can be changed right in the source:
        - **F2.1.5.2.1** ✎ next to the bin.
        - **F2.1.5.2.2** While changing one, ✎ and the bin become **Cancel** and **Save**, like the
          other responsive buttons. **Save** then splits into **This calendar** and **All sources**.
        - **F2.1.5.2.3** Each line says **Shared** (a Rule Template; click it to change it for every
          source) or **This calendar** (a rule for this source only, made by saving for This
          calendar; it isn't listed in Rule Templates).
        - **F2.1.5.2.4** A menu only on a new line (+ Add a rule); existing lines are changed
          directly.
  - **F2.2** At the bottom: **Cancel** and **Save** on the right; **Remove** on the lower left,
    asking "Are you sure?" first.
- **F3.1** Rule Templates folds to just its title (open or folded is remembered); + stays in the
  corner.
- **F4.1** Event Templates folds the same way.
- **F6.1** Activities and Logs: the debug links are at the bottom.

### Fixed
- **F2.1.5.3** The rule menus were light in dark mode.
- **I1.1** Sync Now reloaded the whole page; now only the source's status, the calendar and the log
  update. Switching the calendar's view (or month, or time zone) now swaps the calendar in at once;
  before, the view sometimes didn't change until the page was refreshed (a phone's `?view=list`
  stuck in the address).

## 0.2.7-beta.4 — 2026-10-22

### Fixed
- **I1** A source's header didn't fit on its two lines and overflowed. The last-download and
  check-interval lines now start at the same left edge, and switch to the short wording ("98 events
  @ 14:53", "Check every 15 min") whenever the long one wouldn't fit beside the title; this is
  measured on the page, so it also works in other languages.

### Changed
- **R1** README: every screenshot is shown in the light and the dark theme, side by side (and the
  add-event screenshot is new).

## 0.2.7-beta.3 — 2026-10-22

### Added
- **F1** Updates from the status page:
  - **F1.1** An optional updater container next to CalendarStream: Watchtower, with an HTTP "update
    now" endpoint protected by a secret token (`.secrets/UPDATER_TOKEN.txt`). It's reachable only
    inside the Docker network, never checks on its own, and only updates the CalendarStream
    container (not the database).
  - **F1.2** "(v… is available)" gets an **Update now** button that asks the updater to download
    the new image and restart. The button shows the progress like the ✓ Validated box does:
    **Update now** → **Downloading…** (with a moving bar; the updater doesn't report how far the
    download is) → **Restarting…** → gone once CalendarStream is running again, with the version at
    the top (and in the footer) showing the new one. If the updater refuses or isn't reachable, it
    says **✗ Update failed**, with the reason. Settings → Updates says whether the updater is
    running.
  - **F1.3** The installer asks whether to set it up (no by default; yes adds
    `COMPOSE_PROFILES=updater` to `.env`), and it works the same on Linux, macOS (Docker Desktop)
    and Windows (WSL).
  - **F1.4** The updater is [nicholas-fedor/watchtower](https://github.com/nicholas-fedor/watchtower),
    the maintained fork: the original containrrr/watchtower was archived in December 2025, and the
    fork releases every week or two (v1.23.2 on 2026-10-22).
- **R1** README: light and dark screenshots side by side (the calendar and a phone).

## 0.2.7-beta.2 — 2026-10-22

### Changed
- **F1** Settings:
  - **F1.1** Hard to see when opened: the Settings panel is now light blue (the blue of the Sync
    Now box), with each part on white.
- **F2** Calendar:
  - **F2.1** "Time Zone" before the time-zone menu; "TZ" when space is limited.
- **F3** Calendar Sources:
  - **F3.1** The last-download line no longer fit: when the box is narrow it shortens to
    "40 events @ 1:10pm (…)".
  - **F3.2** Likewise "Check for changes every 60 minutes" shortens to "Check every 60 min"; on a
    phone the status box sits beside the title.
  - **F3.3** "UID" is now "Username".
  - **F3.4** Every "✓ Validated" box is half as wide, in the same place; Save and Cancel share that
    width, and a failed check says "✗ Failed" (the reason shows under the boxes).
- **F4** Calendar Destinations:
  - **F4.1** Each destination's box, and the Google account's, has the same header as a source's
    (name, kind, its sources and dates, status) and folds the rest under **▸ Configure ◂**. The
    Google account opens by itself until it's connected; the others stay as you left them.
  - **F4.2** Add a destination: the Name's hint reads "How your calendar will be titled via stream"
    (left empty, it takes the first source's name).
- **F5** Rules:
  - **F5.1** The same section heading as Calendar Sources.
  - **F5.2** Renamed **Rule Templates**.
- **F6** Event Templates:
  - **F6.1** Its own section (it was a box inside Rules), with **+** in its heading.
  - **F6.2** Where Activity was: beside Rule Templates on a wide screen.
- **F7** Activity:
  - **F7.1** Renamed **Activities and Logs**.
  - **F7.2** Spans the full width.
- **F8** Layout:
  - **F8.1** Checked on a wide screen, a narrow one and a phone, with shorter words where needed
    (no sideways scrolling at any width).
  - **F8.2** Spacing: 10 px between sections, 5 px between the boxes in a section, 2 px between rows
    of fields.
- **R1** Fuller README screenshots: the calendar (light and dark), each section in use, the rule
  dialog, Settings and a phone (made-up demo schedule).

## 0.2.7-beta.1 — 2026-10-22

### Changed
- **F1** Version numbers follow [semver](https://semver.org): betas are `x.y.z-beta.N` (this is
  0.2.7-beta.1), and stable releases are `x.y.z` (every beta of 0.2.7 comes before 0.2.7 itself).
  - **F1.1** The full version shows at the top of the page (on its own line on phones) and in the
    footer, still linked to its release notes.
  - **F1.2** Check for updates: a beta install is offered newer betas and stable releases; a
    stable install only stable releases. An exact beta version in `IMAGE_TAG` (e.g.
    `0.2.7-beta.1`) follows beta.
  - **F1.3** The release build accepts `x.y.z-beta.N`. Only an `x.y.z` can become `latest`; a
    release changes `VERSION` and `STABLE` together, and is built before it's marked latest.
  - **F1.4** The installer and `.env` accept an exact beta version.

## 0.2.6 — 2026-10-22

### Added
- **F1.2** The version number at the top links to its release notes on GitHub.
- **F3.1** Adding a calendar source: "Calendar feed (.ics link) — add any calendar with a link
  starting with `webcal://` or ending in `.ics`", with a **Title**, the **Link** and a **Note** (a
  short message shown next to the source's title).
- **F4** Each destination has a **Start** and **End** date (empty = no limit); it only gets the
  events between them.
- **F5.1** Predefined rules in the Rules section: **Items without an end time** and **24-hour
  events**. New sources start with both.

### Changed
- **F1.1** "(v0.2.0)" next to the version reads "(v0.2.0 is available)".
- **F2** The page's layout:
  - **F2.1** **▸ Configure ◂** uses the same rotating arrows as the other collapsible parts.
    - **F2.1.1** Equal, smaller spacing above and below it.
  - **F2.2** No more **(edit)** links: opening Configure turns a source's color, title and note
    into fields.
  - **F2.3** **✓ Validated** is a rounded box like **Healthy**.
    - **F2.3.1** **Save** and **Cancel** together are the same size as that box.
  - **F2.4** Every section except the Calendar has the same kind of heading as Calendar Sources.
    - **F2.4.1** The sections are Calendar, Calendar Sources, Calendar Destinations (the Google
      calendar boxes moved in here), Rules and Activity.
  - **F2.5** Wide screens: Calendar (opens on the calendar view unless another is chosen), then
    Calendar Sources | Calendar Destinations and Rules | Activity side by side, then the footer.
    Narrow screens and phones: one column, the Calendar opens on the List (itinerary) view unless
    another is chosen, and the view and theme switches become one button each that steps through
    the choices.
- **F3.2** A source's Rules:
  - **F3.2.1** Each rule is a rounded box spanning the line.
  - **F3.2.2** Each line starts with a menu of the rules defined in the Rules section, ending with
    **Create a New Rule…**, which opens the same dialog as creating a rule in the Rules section.
- Rule templates are now simply **Rules**: every rule lives in the Rules section and sources pick
  from it. A source's own rules and the ticked rule templates of 0.2.5 are moved there, in the same
  order, with their settings. **Event templates** are a box inside Rules.

### Fixed
- **I1** "Add to Google Calendar" on Android: the calendar was added but never appeared. Google's
  Android app can't subscribe by link, and a linked calendar stays hidden on the phone until its
  **Sync** is turned on. The subscribe page (on Android and iPhone) and each feed's box now explain
  how: add it on calendar.google.com (desktop site), then in the app **Settings →** the calendar
  **→ Sync**; Google can take a few hours to load it.

## 0.2.5 — 2026-10-22

### Changed
- **F1** The page's sections, in order: **Calendar, Sources, Destinations, Rule templates, Event
  templates, Activity**.
  - **F1.1** **Rule templates** (new section): rules kept once, for any source. Each source's Rules
    (under Configure) has a subsection where it ticks the rule templates it uses, alongside its own
    rules; changing a template changes every source that ticks it. A source's own rules come first.
  - **F1.2** **Event templates** is its own section (it was a box at the end of Sources).

## 0.2.4 — 2026-10-22

### Changed
- **F1** The "✓ Validated" slot next to each login (CCS+, the Google client, a feed's Site Address, the
  status-page login):
  - **F1.1** When text is entered, ✓ Validated is replaced by **Save** and **Cancel**, side by side in
    the same space.
  - **F1.2** **Cancel** grows to fill the space, undoes the typing and fades back to ✓ Validated.
  - **F1.3** **Save** grows to fill the space and says **Saved**, then **Verifying…** (yellow) while
    CalendarStream checks the login, then **✓ Validated** (green) or **✗ Verification failed** (red,
    with the reason under the boxes). The page login is simply saved (your browser then asks for it).

## 0.2.3 — 2026-10-22

### Fixed
- The debug links (Response details, Last calendar file received) are back, in the Activity log
  for each source (0.2.2 had dropped them with the old source footer).

## 0.2.2 — 2026-10-22

### Changed
- **F1** Calendar Sources look like the mockups:
  - **F1.1** Each source's header: name (**(edit)**) and kind on the left; on the right, the last
    download ("Downloaded 98 events from feed @ 23:13. (0 new, 0 removed)") above the check
    interval (saved as soon as it's changed), then the status with **Sync Now** under it.
  - **F1.2** **> Configure <** under the header opens the rest; it's folded until opened (and
    remembered), unless something needs doing.
  - **F1.3** **Site Address** (the Calendar Sync link) sits with the UID and password and is saved
    with them; the hand upload is to its right. A feed source's Site Address is its link.
  - **F1.4** Two built-in rules end each source's Rules: **Items without an end time** (last a set
    time, or all day) and **24-hour events** (shown as all-day, or keep their times). They replace
    the ".env" note and override `DEFAULT_EVENT_HOURS` / `ALLDAY_24H` for that source.
  - **F1.5** One line at the bottom: How rules work, **Save** and **Remove**.

## 0.2.1 — 2026-10-21

### Changed
- **F1** Destinations are independent of sources (0.2.0 made a Google calendar and a feed for each
  source). There can be several Google calendars and several feeds; each has its own name and
  ticks the sources it gets, and every event keeps its source's colors and rules. One **Google
  account** box signs in for all the Google calendars. Removing a source takes it off every list;
  removing a Google destination keeps its calendar in Google unless "Also delete it in Google" is
  ticked. Installs from 0.2.0 and before keep their feed links and Google calendar.
- **F3.2** No more "33 events · times in" above the calendar.
- **F3.3** The calendar's time zone moved to the right: time zone, view, 12h / 24h.

### Added
- **F2.1** **Duplicate** and **Delete** icons at the bottom of an event's details and on the event
  page. Delete removes an event added here; a source's own event is hidden instead (its source
  would send it again).
- **F3.1** **Month / Week / Day / List** views, left of the 12h / 24h switch.
- **F4** The **PolyForm Noncommercial License 1.0.0** (`LICENSE.md`): free for non-commercial use, with
  credit to the author; see the README.

## 0.2.0 — 2026-10-21

Calendar sources and destinations: CalendarStream is no longer only for CCS+. An install from
before keeps what it had (CCS+ as its source; the feed, and Google Autosync if it was set up).

### Added
- **F1** The status page has two sections, **Calendar Sources** and **Calendar Destinations**, each
  with **+** in its corner. A new install starts with neither.
  - **F1.1** Sources: **United CCS+ Calendar Sync** (once) and **calendar feeds** (any `.ics` or
    `webcal://` link: another airline, work, school, sports). Each source has its own box: name and
    color (**(edit)**), status chip, check interval, **Sync now**, its login or link, its rules and
    a **Remove** button. Repeating events in feeds are shown from a year back to two years ahead.
  - **F1.2** Destinations: **Google Calendar Autosync**, with a Google calendar of its own for each
    source (removing a source deletes its calendar there), and **Calendar feed**, with a feed link
    and subscribe page for each source.
  - **F1.3** The CCS+ step-by-step help ("How to get a Calendar Sync link, ID and secret") is in the
    same box as the UID and Calendar Sync password.
  - **F1.4** Adding an event asks which calendar it goes in (with more than one source).
- **F2** The first destination asks for the public address (filled in with this page's address
  when it's https://), noting that it can be changed later in ☰ Settings.
- **F3** **Rules** replace Tag Colors (existing tags carry over as color rules). A rule matches a
  title as before; coloring is now one of its actions, so more can follow.
  - **F3.1** Each rule (and each template) has a bin icon to delete it.
  - **F3.2** **Add event**: a rule can add an event from a template some time before the start,
    after the start or after the end of each matching event, e.g. "Drive to the airport", 1:30
    long, 2:00 before each trip. These events follow their event; edit the rule or the template to
    change them.
  - **F3.3** **Event templates**: title, length (or all day), location and color, used by those
    rules and by **Start from a template** when adding an event by hand.
- **F4** **Stream names**: each feed's secret link part can be entered by hand (or taken from a
  pasted old link), so links from before a reinstall, or from a source removed by mistake, work
  again.

### Changed
- `/api/status` also lists each source and the destinations (its top-level fields stay CCS+'s).
- Google sign-in finds or makes a calendar for each source.

## 0.1.24 — 2026-10-21

### Added
- **F1** ☰ Settings → **Admin e-mail**: the administrator's address. The Google Calendar Autosync
  guide fills it in as the support and contact e-mail and as the test user.
- **F2.1** Every password box has an eye button to show what's being typed.
- **F2.2** Password boxes where you choose a password (status-page login, first visit, CCS+
  Calendar Sync password) show a strength bar along their bottom edge as you type (estimated in
  the browser; nothing is sent).

### Changed
- **F3.1** The public address is set only in ☰ Settings. `PUBLIC_URL` is gone from `.env` and the
  installer (which now asks three questions); an existing `PUBLIC_URL` is moved into Settings once,
  after which it can be deleted from `.env`.
- **F3.2** ☰ Settings → Updates reads, e.g., "Subscribed to beta versions (Up to date). Next check at
  10:19.", above **Check for updates** · Weekly · **Check now** on one line.

## 0.1.23 — 2026-10-21

The Autosync setup, reviewed for first-time users (after a real first setup ran into each of these).

### Changed
- The Google Calendar Autosync guide follows the order Google needs: "Before you start" (the public
  address must match the browser's address bar), then create the project, turn on the Calendar API,
  set up the sign-in screen, allow calendar access, **publish the app or add yourself as a test user
  (before creating the client)**, create the client with its Authorized redirect URI, copy both keys
  (Google shows the secret only once) and Connect. Each step ends with a ✓ checkpoint showing what
  you should see.
- Beside **Connect Google Calendar**: the exact address Google sends you back to, which Gmail account
  to use, and what to press on "Google hasn't verified this app" (**Continue**).
- The installer's public-address question and the README Quick start say the address needs
  `https://` and must be typed exactly as in the browser; the first-visit page says where to find the
  setup code.

### Added
- **If Google shows an error:** what to do about redirect_uri_mismatch, access_denied, "hasn't
  verified this app", invalid_client, deleted_client and being asked to connect again each week.
- A warning when the public address and the address the page is open at differ (e.g. a ccs/css
  typo), since Google always sends you back to the public address.

### Fixed
- A refused Google sign-in (403 access_denied) now explains the test-users fix instead of only
  "cancelled".

## 0.1.22 — 2026-10-21

Deploy review, rounds 3–4 (release candidate).

### Fixed
- The login limit across all addresses no longer locks out the owner: addresses that logged in
  successfully in the last 7 days are exempt (strangers' failures can't keep you out).
- Login-failure bookkeeping is thread-safe (two logins at once could cause an error).
- A Google client check saved by 0.1.20 shows correctly after upgrading (✓ Validated plus the
  missing redirect URI, instead of "Google rejected the client").
- The installer can't stop silently on macOS when looking up this computer's address.
- The 12h / 24h switch and the event pin keep their size again (0.1.18 had squashed the switch), and
  the calendar legend's "?" sits in its circle.

### Added
- README screenshots (from a made-up demo schedule).
- Translations for everything added since 0.1.18.

## 0.1.21 — 2026-10-21

Deploy review, second round.

### Security
- Forwarded headers (the visitor's address and https) are only believed from this computer unless
  `FORWARDED_ALLOW_IPS` names your reverse proxy (see `.env.default`); behind a proxy, set it and the
  Public address. A limit across all addresses (50 failed logins in 15 minutes) stops guessing from
  many made-up addresses, and addresses that are locked out are never forgotten early.

### Fixed
- When Google doesn't list the redirect URI, the Google box keeps **✓ Validated** (the ID and secret
  are right) and shows a separate red line with the exact address to add, a **Check again** button,
  and Connect waits; the result only counts for the address that was checked.
- The old installer default `http://localhost:8080` (macOS) also counts as not set; the installer
  finds this computer's address on macOS.
- **Check now** no longer makes the log announce the same update again.
- An https link that redirects to http gets an accurate message.
- The public address refuses typos such as `http:/example.com` and `…;params`; `.local` addresses
  aren't offered to Google.

## 0.1.20 — 2026-10-21

Deploy review fixes (programming, commenting, security).

### Fixed
- **Google sign-in (`redirect_uri_mismatch`):** the installer's default public address was
  `http://<this computer's IP>:8080`, which then replaced the address the page is opened at, so the
  redirect URI didn't match what's registered in Google Cloud. The installer now leaves it empty
  (Enter skips it, "-" clears it), and that old default in `.env` counts as not set.
- The client check now says when Google doesn't list the redirect URI (with the exact address to
  add) instead of showing ✓, and Connect stays off until it's fixed. The guide only shows a redirect
  URI Google can accept (https with a domain name).
- The public address is tidied the same way everywhere: lower-case scheme and host, default ports
  and a trailing slash dropped.
- The background loops (CCS+, Google) survive a database restart; finishing a Google sign-in can no
  longer race a sync (no duplicate calendars); "Update available" is logged once, not at every check.
- The Public address text no longer runs under the "This page" button in Settings.

### Security
- The login lockout can't be dodged with a made-up `X-Forwarded-For` as easily: forwarded headers
  were limited to proxies on private networks (0.1.21 tightens this further), and the failure list
  is bounded.
- The first-visit page has its own form token, the status page's token is renewed whenever the
  login is created or changed, and form posts from other websites are refused.
- Pages can't be framed, and send `nosniff` and `no-referrer`; `/healthz` no longer shows database
  details; non-ASCII tokens no longer cause errors.
- Downloads from CCS+ are https only (also after redirects), at most 5 redirects and 5 MB.
- The installer makes `.env` readable by you only and stores answers with `|` or `&` safely; the
  release workflow gives each job only the permissions it needs.

### Changed
- Comments, docstrings, README and `.env.default` brought up to date; unused CSS, scripts and code
  removed.

## 0.1.19 — 2026-10-21

### Added
- **F1** ☰ Settings → **Check for updates**: Hourly, Weekly (the default), Monthly or Never, plus
  **Check now**. It follows this install's release (`IMAGE_TAG`): a stable install is only told
  about stable versions, a beta install about the newest beta. A newer version shows in brackets
  next to the version at the top, linked to its release notes, and once in the activity log.

### Changed
- **F1 (tags)** Tag Colors shows only saved tags. With none, the box is just its header with **+**
  in the corner; **+** at the end of the last tag adds another. The Save line appears once there's
  something to save.
- **F2** The Google client guide is seven short steps, with its own "Create the OAuth client ID"
  step, and what to do when Google won't publish the app (stay in Testing and add yourself as a
  test user).
- **F3** **Sync now** is in the CCS+ Calendar Sync box (the schedule header keeps the status chip).
- `docker-compose.yml` passes `IMAGE_TAG` to the app.

### Fixed
- **I2** On the event page, only the All-day box and its words tick it (clicking elsewhere on the
  line did too); the same for the other check boxes there.

## 0.1.18 — 2026-10-20

The presentation review (#1–#11), except #4: logins stay on the dashboard.

### Changed
- **#1** One pattern for every section: the schedule card's header shows its status chip and
  **Sync now** on the right (folded or not), and each part of Status & setup is a box with a title,
  a one-line subtitle and a status chip. Activity log uses the same title style.
- **Logins:** the CCS+ login and the Google Autosync client (with Connect, Disconnect and the
  instant-updates line) live only on the dashboard, in their boxes. **☰ Settings** now holds only
  site settings: the status-page login and the public address.
- **#2** Tag Colors' explanation is folded behind "How tags match".
- **#3** "Check for changes every [60] minutes" is a labelled field; the `.env` facts are one line under it.
- **#5** Box titles have short subtitles instead of long bracketed descriptions.
- **#6** Autosync is the main path; **Subscribe to the feed** and **Share it** are folded under
  "Other ways to get the schedule".
- **#7** The feed's "read by Google" status is a chip, with "What to check" folded.
- **#8** One status chip (✓ good, ! warning, ✗ problem, ↻ working) everywhere.
- **#9** Two button styles (primary, secondary), all the same height; "Choose Calendar.ics…"
  replaces the browser's file box and shows the chosen file.
- **#10** The calendar's legend is one row, with its hint behind a "?".
- **#11** All step-by-step and help folds look the same.

## 0.1.17 — 2026-10-20

### Changed
- **F1** CCS+ Calendar Sync is laid out like Google Calendar Autosync: the step-by-step help is at
  the bottom of the box, now called "How to get a Calendar Sync link, ID and secret (step by step)".
- **F3.1** "Colour" is spelled "color" everywhere in English.
- **F4** The folded schedule header shows **Sync now** on the right.
- The release workflow no longer copies images from the old `calendar_stream` package (every
  version is under `calendarstream`; the old package is being removed).

## 0.1.16 — 2026-10-20

### Added
- **F2.2** A time-zone menu above the calendar ("times in …"): shows the calendar in any time zone.
  It only changes this page; the feed, Google and the server keep `TZ` from `.env`.
- **F2.3** Event times are one box each: type them ("9:30", "9:30pm", "21:30", "930") or pick from
  a list every 15 minutes (the end list shows the length). A **Time zone** menu, and **The end is
  in a different time zone** for events such as flights; lengths are kept in real hours across
  zones, and the event page remembers the zones used.
- The Subscribe box says when Google Calendar last read the feed, or that it hasn't yet, with
  what to check.

### Changed
- **F1.1, F1.2** In Settings and Status & setup, the CCS+ and Google client logins show
  **✓ Validated** to the right of the boxes; it turns into **Save & sync** / **Save** when a box is
  empty, being edited, or the check failed.
- **F1.3** The status-page login looks like the other logins: user name and password with
  **✓ Signed in**; typing a new password asks for the current one and shows **Save**.
- **F1.4** **Public address** is right under the status-page login, with **This page** inside the
  box, **Save** on the same line and the explanation underneath. Buttons are now always on the
  same line as their boxes.
- **F1.5** Time format is no longer in Settings; use the 12h / 24h switch above the calendar.

### Removed
- The hour / minute / am-pm menus on the event page (replaced by the time boxes).

## 0.1.15 — 2026-10-20

### Added
- **F3** Instant updates from Google (webhooks). With Autosync and a public `https://` address,
  CalendarStream asks Google to notify `/google/notify` whenever its calendar changes there; a
  change or deletion made by hand in Google is put back within seconds instead of at the daily
  check. Notifications are checked against a secret token, renewed every week, moved when the
  public address changes, and stopped on disconnect. If Google refuses them, Autosync carries on
  with the daily check and asks again 6 hours later. Settings and the Google section show whether
  they're on.
- **F1.1** Click the month and year above the calendar to jump to any month (‹ › change the year).
- **I1** A **12h / 24h** switch at the top right of the calendar (the same setting as ☰ → Time format).

### Changed
- **F2.1** Settings forms match the status page: labels above the boxes, boxes side by side
  (user name and current password; new password twice), buttons beside their notes.
- **F2.2** Each Settings section is in its own outlined block.

## 0.1.14 — 2026-10-20

### Changed
- **I1 (labels)** The CCS+ Calendar Sync login and the Google Autosync client have their labels
  outside the boxes, and the two boxes of each sit side by side on one line (UID and password;
  Client ID and Client secret), with the button at the end of the line.
- **F2** CCS+ Calendar Sync's contents are in a box, like the Google Calendar ones.
- **F1** In the Google Calendar boxes, the buttons (Connect, Add to Google Calendar, Open subscribe
  page) sit to the right of their explanation, so the section is shorter.
- **I1 (tags)** **Tag Colors** is now its own block, always visible right under the health bar,
  instead of inside (edit). (edit) keeps the calendar's name and default colour.

## 0.1.13 — 2026-10-20

### Changed
- **F1** The Google Calendar Autosync client form looks like the CCS+ Calendar Sync login: the
  Client ID and Client secret boxes are stacked full width and named by their placeholders, with
  the description and **Save** below them.

## 0.1.12 — 2026-10-20

### Changed
- **F1** Settings → Google Calendar Autosync is shorter: **Client ID** and **Client secret** each sit
  on one line with their box, and the description shares the last line with **Save**. The Google
  section of Status & setup uses the same layout.
- **I1, I2** The "Subscribe to the feed" note now says what Google does with a subscribed feed: it
  re-reads it on its own schedule, which can take up to 12 hours, and keeps the name it saw first.
  New events and a new name reach Google within minutes only with Autosync.

## 0.1.11 — 2026-10-20

### Added
- **F1.2** **Time format** in Settings: 12-hour (1:30pm), 24-hour (13:30, "military") or Automatic
  (12-hour in English, 24-hour in the other languages). It applies to the calendar, event details,
  the activity log and the event page.
- **F1.3** An event colour, bottom left on the event page: one of Google Calendar's 11 event colours,
  or the default (from a tag or the calendar). It wins over tags, on this page and in Autosync.

### Changed
- **F1.1** On the event page, changing the start (date or time) moves the end by the same amount,
  so the event keeps its length. Changing the end sets a new length.
- **F1.2** Times are picked from hour and minute menus (01–12 with am/pm, or 00–23) instead of the
  browser's time box, whose values ran on endlessly when scrolled.
- **F1.4** **Cancel** and **Save** are at the bottom right of the event page.
- **F2.1** Once Google accepts the client, the Client ID and Client secret fold away behind
  "✓ Validated: Client ID & Client secret" (click it to change them).
- **I2** "✓ Validated: CCS+ accepted the sign-in" now reads "✓ Validated: CCS+ sign-in".

## 0.1.10 — 2026-10-20

### Changed
- **F1.1** The setup checklist (UID, Calendar Sync password, link, CCS+ accepted the sign-in,
  schedule received) now sits just under the CCS+ login, above "CCS+ Calendar Sync · checks every".
- **F1.1.1** "How to turn on Calendar Sync in CCS+" sits to the right of the checklist (below it on
  phones), in a sub-block of their own with the Calendar Sync link box.
- **F1.1.2** That sub-block is only open while the UID or Calendar Sync password is missing, or the
  last update failed (sign-in rejected, blocked, error or paused); otherwise it's closed.
- The month view's hint mentions clicking an empty spot on a day to add an event.

### Fixed
- The calendar-name hint for Autosync (0.1.9) never showed; it now does when Google is connected.

## 0.1.9 — 2026-10-20

### Added
- **F1.3** The installer asks for the **public address** (default `http://<this computer's IP>:8080`);
  it may also be entered later in ☰ Settings.
- **I1.2** The CCS+ UID and Calendar Sync password are in the **Settings** menu (☰), with whether
  CCS+ accepted them.
- **F4** A footer with the version and links to **Report a problem** and **Suggest a feature**
  (GitHub issue forms; the bug form is filled in with the version).
- **F6.2** A pin (bottom right of an open event) keeps it open.
- **F6.3** Clicking an empty spot on a day opens **Add event** for that day.
- **F6.4** A line under **Add to Google Calendar** and **Open subscribe page** explaining each.
- The installer works on macOS (Docker Desktop) and on Windows inside WSL.

### Changed
- **F1.1** Running the installer again offers your current settings as the defaults.
- **F1.2** The installer's questions are now: release (stable or beta), the folder for
  `docker-compose.yml` and `.env`, then the config and data folder, which is always asked so you can
  confirm it.
- **I1.1** With no CCS+ login yet, the health bar shows **Setup needed** (not an error) and asks for
  it; nothing is downloaded until it's entered. The **CCS+ Calendar Sync** login now sits just under
  the health bar, always visible, with "✓ Validated: CCS+ accepted the sign-in" when it works, and
  the note "Your CCS+ UID and Calendar Sync password may be updated in Status & setup, or in
  Settings (☰)." Status & setup opens by itself until it's set up.
- **F2.1** The Settings Google section is now **Google Calendar Autosync**: Client ID, Client secret
  and a closed "How to get a client ID and secret (step by step)".
- **F3** Status & setup's Google section has three parts: **Autosync** (connected, or the client
  ID and secret with the same guide), **Subscribe to the feed** (the raw feed URL and **Add to Google
  Calendar**) and **Share it** (the shareable subscribe page and **Open subscribe page**).
- **F4** Copy buttons use the Bootstrap "copy" icon.
- **F5** The upload line is shorter: "Or upload **Calendar.ics** by hand."
- **F6.1** Clicking anywhere else closes an open event (unless it's pinned).
- **I2** The calendar-name hint says Autosync renames the Google calendar by itself; without
  Autosync, Google keeps the name it saw when you subscribed, so rename it in Google too.
- README: works on Linux, macOS or Windows (WSL); the installer's four questions in order.

## 0.1.8 — 2026-10-20

### Added
- **F1** A copy button next to the setup-code command on the first-visit page.

### Fixed
- **I1** The setup-code command named the service (`calendar_stream`), which is easy to mistype as
  `calendarstream` ("no such service"). It's now `docker compose logs | grep "setup code"`, run in
  the folder with `docker-compose.yml`, which needs no service name. The "wrong setup code" message
  says the same.

## 0.1.7 — 2026-10-20

### Changed
- **R1** The installer's release question now reads "Which release would you like to install,
  latest (stable) or beta [stable]:". Both `latest` and `stable` choose the stable release.

## 0.1.6 — 2026-10-20

### Added
- **F1** The installer asks which release to run: **stable** (the default) or **beta**. Pressing
  Enter on a later run keeps the current choice; it's saved in `.env` as `IMAGE_TAG`.

### Changed
- **R1.1** New README introduction, explaining why CalendarStream exists and its two ways of
  getting the schedule into Google.
- The README's Quick start lists the installer's three questions and defaults exactly, and stays short.

## 0.1.5 — 2026-10-20

### Added
- **F1** **Languages:** English, Español, Français, Deutsch, Português (Brasil) and Vlaams. Choose
  one with the new **globe** button, left of the theme switch, or **Automatic** to follow the
  browser; the choice is saved in the database. Everything on screen is translated: every page,
  menu, button, help text and guide, status messages, the activity log, error pages, and the
  month and day names. Event titles stay as United sends them. The shareable subscribe page uses
  each visitor's browser language.
- Errors from forms (e.g. a check interval below 15 minutes) are shown as a small page in your
  language with a **Go back** link, instead of raw JSON.

### Changed
- **F2.1** The installer's first question names what goes there: "Folder for docker-compose.yml
  and .env".
- **F2.2** The installer then asks for **CalendarStream's config and data folder** (the database
  and `.secrets/`, saved in `.env` as `MNT_DOCKER`). It defaults to the first folder and is only
  asked once.
- README: running the installer again is safe: it never overwrites an existing `.env` or the
  database password. The note about upgrading from 0.1.2 is gone.
- Two messages that still pointed at the old secret files and the old upload location now point
  at Setup and **Upload & publish**.

### Fixed
- On narrow screens the title could be squeezed under the header buttons; it now shortens neatly.

## 0.1.4 — 2026-10-20

### Added
- **`install.sh`**: installs or updates CalendarStream with one command
  (`bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)`). It
  downloads `docker-compose.yml` and `.env` (keeping an existing `.env`), creates a random database
  password once, starts the stack and shows the setup code.

### Changed
- **F1** `MNT_DOCKER` is optional. Without it, the installer asks for an installation folder, and the
  database and `.secrets/` live next to `docker-compose.yml`. Set it in `.env` (or before running the
  installer) to keep them elsewhere, e.g. `/mnt/SSD/docker`.
- The README is about a third as long, with a one-command quick start and a table of settings.

## 0.1.3 — 2026-10-20

The logins move into the app. Only `DB_PASSWORD.txt` stays on the server.

### Added
- **First visit:** CalendarStream asks you to create the status-page login. It first asks for a
  **setup code** printed in the container log (`docker compose logs calendar_stream | grep "setup code"`),
  so only someone with access to the server can claim a new install. The password is stored hashed.
- **Settings (☰) → Status-page login:** change the user name and password (needs the current one).
- **Setup:** boxes for your CCS+ **UID** and **Calendar Sync password**, with **Save & sync**. The
  password is stored encrypted and never shown again. Setup opens by itself until they're entered.
- Logins from the old secret files are imported once, if the old compose file still mounts them.

### Changed
- `docker-compose.yml` mounts only `DB_PASSWORD.txt`. `CCS_USER.txt`, `CCS_PASSWORD.txt`, `USER.txt`
  and `PASSWORD.txt` are no longer used and can be deleted (after the import, if you want it).
- `DB_PASSWORD` is also the key that encrypts the stored passwords (CCS+, Google), as it already was
  for Google.
- Messages about a rejected or missing CCS+ login point to Setup instead of the secret files.

## 0.1.2 — 2026-10-20

### Added
- **Settings (☰) → Public address**: the https:// address people use to reach the status page,
  used for the feed and subscribe links and Google's sign-in redirect. It overrides `PUBLIC_URL`
  in `.env`, which is now optional; **Reset** goes back to `.env`, and **This page** fills in the
  address the page is open at. "cal.example.com" is completed to "https://cal.example.com".

### Changed
- `.env.default` is shorter and clearer: only `MNT_DOCKER` is required, and every other setting is
  marked `# optional` with its default and what overrides it. The unused shared-host folders and the
  `CCS_*`/`GUI_*` login lines (the secret files replace them) are gone.
- Warnings about a missing public address point to Settings instead of `.env`.

## 0.1.1 — 2026-10-20

### Changed
- The image is now **`ghcr.io/uuugh/calendarstream`** (was `ghcr.io/uuugh/calendar_stream`), to match
  the repository's new name, `Uuugh/CalendarStream`. Every earlier version, `beta` and `latest` were
  copied to the new name, so any tag can be pulled from it. Update `docker-compose.yml` (`git pull`);
  the old name gets no new releases.

## 0.1.0 — 2026-10-20

First minor version: **Google Calendar sync** (0.0.12 and 0.0.13), plus the items below. A beta
until it passes the stable reviews and your approval.

### Added
- **F2.1.1** The check interval can be changed on the status page: type the minutes (15–1,440) and
  press **Save**. It's saved in the database (overriding `SYNC_INTERVAL_MINUTES`), and the next
  check moves to match.
- **F3.2** CalendarStream checks the Google client ID and secret with Google when they're saved,
  and shows ✓ accepted, ✗ rejected (unknown client ID or wrong secret) or ? (Google couldn't be
  reached). **Check again** repeats it. **Connect** is disabled while Google rejects them.

### Changed
- **F1** The theme switch is in the order Light, Dark, System.
- **F2.1** The line "CCS+ Calendar Sync · checks every … · items without an end time …" moved from
  under the title to just below the health bar.
- **F2.2** **Upload Calendar.ics** moved out of Setup to just below that line, in a smaller, more
  compact row (the full explanation is in its tooltip).
- **F3.1** In Settings → Google Calendar, the Client ID and Client secret boxes come first; the
  step-by-step guide is below them and starts closed.
- The release workflow keeps the image name `ghcr.io/uuugh/calendar_stream` even if the GitHub
  repository is renamed, so `docker-compose.yml` and the `latest`/`beta` tags keep working.

## 0.0.13 — 2026-10-20

Second beta of **Google Calendar sync** (planned for 0.1.0): the events are copied.

### Added
- **Event sync to Google.** Once connected, CalendarStream writes the schedule into its Google
  calendar and keeps it in step: within seconds of a download, upload or edit, sending only what
  changed. Covered: events from the first day of the current month onward (older ones are left
  alone in Google), edits, hidden events (removed from Google) and added events. No reminders.
  CCS+'s "free" items stay *free* in Google, the rest *busy*.
- **Tag colours in Google:** each tag uses the nearest Google event colour (Tomato, Basil, Peacock
  and so on). Events with no tag take the calendar's colour.
- **F2 (from 0.0.10):** renaming the calendar on the status page renames it in Google too.
- A daily check, and **Sync now** in the menu, compare Google's copy with the schedule and put back
  events changed or deleted there (events you added to that calendar yourself are kept). A calendar
  deleted in Google is made again.
- The menu shows the last sync and its result; the Activity log's status line shows Google's state,
  and the log records each sync that changed something (e.g. "Google: 3 added, 1 updated").
- **The Google OAuth client is entered in Settings (☰) → Google Calendar** (Client ID and Client
  secret), with a step-by-step guide for getting them in Google Cloud. The secret is stored
  encrypted with a key derived from `DB_PASSWORD` and never shown again. One client serves the
  whole app.

### Removed
- The `GOOGLE_CLIENT_ID.txt` and `GOOGLE_CLIENT_SECRET.txt` secrets from 0.0.12, and their lines in
  `docker-compose.yml` (now the same as in 0.0.11). Those files can be deleted.

## 0.0.12 — 2026-10-20

First beta of **Google Calendar sync** (planned for 0.1.0): connecting a Google account. Events
are copied in the next beta.

### Added
- **Settings (☰) → Google Calendar**: **Connect** signs in to Google and creates a calendar of
  CalendarStream's own, named like the feed; the menu then shows the connected account and
  calendar. **Disconnect** removes CalendarStream's access in Google, and can also delete the
  calendar. Connecting the same account again reuses the calendar.
- CalendarStream asks Google only for calendars it creates (`calendar.app.created`) and your
  e-mail address. The sign-in is stored encrypted with a key derived from `DB_PASSWORD`.
- Secrets `GOOGLE_CLIENT_ID.txt` and `GOOGLE_CLIENT_SECRET.txt` for the Google OAuth client, with
  set-up steps in the README. The menu shows the redirect URI to give Google.

### Changed
- `docker-compose.yml` mounts the two new secrets. **Create both files before recreating the
  stack**, even empty: Docker won't start a stack with a missing secret file.

## 0.0.11 — 2026-10-20

### Added
- **F1** Each tag row has a **match** setting: *Whole word* (default; "RDO" matches "RDO." but not
  "VRDO"), *Contains* (anywhere, even inside a word), *Starts with*, or *Exact title*; and an **Aa**
  button to match capitals exactly.

### Changed
- **F2.1** In **Setup: CCS+ Calendar Sync**, the box for the CCS+ **Copy link** URL comes first,
  directly under the title.
- **F2.2** Setup can be collapsed and starts closed, showing a one-line summary (e.g. "Schedule
  received · 97 events"). Whether it's open is saved in the database like the other sections.

## 0.0.10 — 2026-10-20

### Added
- A reminder under the calendar name in the editor: Google only reads the name when the calendar is
  first added, so a calendar already in Google Calendar has to be renamed there too (with the steps).

### Not done
- **F2** (rename the calendar in Google automatically) is skipped for now. It would need CalendarStream
  to connect to a Google account through the Google Calendar API.

## 0.0.9 — 2026-10-20

### Added
- **F1** Tag colours. In the Status & setup editor, each row has a tag, a colour, **×** to remove it
  and **+** (on the last row) to add another. An event whose title contains a tag as a whole word
  (ignoring capitals) uses that tag's colour in the month view, and the first matching tag wins.
  Other events use the default colour. Tags also appear in the colour key.
- **F1.3** A **Default** button next to the colour picker returns to the standard colours.

### Changed
- **F1.4** The Status & setup title now shows the calendar's name as text in the chosen colour,
  outlined when that colour would be hard to read on the background. A small **(edit)** next to
  it opens the editor (name, default colour, tag colours, **Save**).
- **F1.1** **Save** is right-aligned in the editor, next to **Cancel**.
- **F1.2** The name field stretches to fill the editor's width.

## 0.0.8 — 2026-10-20

### Added
- **F1** A colour picker next to **Save**. The colour tints United's events in the month view
  (timed lighter, all-day stronger) and is added to the feed as `X-APPLE-CALENDAR-COLOR`, which
  Apple Calendar uses. Google Calendar ignores feed colours, so Google subscribers choose their own.

### Changed
- **F2** The Activity log starts closed. Which sections are open is now saved in the database, so
  it's the same in every browser and after signing in again.
- The light / dark / system theme is also saved in the database, so every browser uses the same
  theme. Pages are drawn in the chosen theme from the start (no flash of the other theme).
- **F3** The calendar is now at the top of the page.
- **F4** The calendar's name, colour and **Save** are now the title of the Status & setup section.
  Clicking elsewhere in that title, or its arrow, opens or closes the section.

## 0.0.7 — 2026-10-20

### Added
- **F3** A **Settings** menu (☰) at the right of the title bar. It's empty for now.
- **F4** A **Light / System / Dark** theme switch just left of the Settings menu. The choice is
  remembered in this browser; **System** follows the device's setting. The event editor uses it too.
- **F5** Every section except the calendar can be collapsed by clicking its title. Each browser
  remembers which sections are open. A collapsed section still shows a summary: the status and
  latest message, or the latest activity-log entry.

### Changed
- **F1** The dashboard is reorganised:
  - **F1.1** The health bar, the Google Calendar feed and **Setup: CCS+ Calendar Sync** are now
    one section, **Status & setup**, in that order.
  - **F1.2** The activity log scrolls inside a window five rows tall.
  - **F1.3** The debug links (last download) are inside the Activity log section, below the log.
  - **F1.4** The Activity log title is at the top of its section, above the status line.
- **F2** The app is now called **CalendarStream** (one word).

## 0.0.6 — 2026-10-20

### Added
- **F1** A **Calendar Name** box next to the Google Calendar feed buttons. It sets the name Google
  shows for the calendar and is used by the feed and the subscribe page. It's saved in the
  database and overrides `CALENDAR_NAME`.
- **F3** Editing in the month view:
  - Click an event, then **Edit**, to change its title, all-day setting, start and end, location
    or notes, or to **hide it from Google Calendar**.
  - Edits to United's events are stored separately and re-applied after every download, so they
    survive syncs. ✎ marks an edited event; ⚠ marks one that United changed after your edit.
    **Revert to United's version** undoes an edit.
  - **+** on a day adds your own event (shown in purple), which can be edited or deleted later.
  - Nothing is ever changed in CCS+.
- A colour key under the month view.

### Changed
- **F2** "(Recommended)" now appears before the shareable subscribe page link.
- **F4** The sign-in, last check, schedule changed, next check and event count are condensed into
  one line at the top of the Activity log card. Today's times are shown without the date.
- **Add to Google Calendar** passes the feed as `webcal://`, the format Google's "Add calendar?"
  prompt expects.
- Status messages count the events in the feed (hidden events are excluded).

### Fixed
- **Add to Google Calendar** opened Google Calendar without offering to add the calendar.
- Two elements on the status page shared an `id`, which could break the **Copy** buttons.

## 0.0.5 — 2026-10-20

### Changed
- Downloads from CCS+ now use **curl**. curl identifies itself as curl; the UID and Calendar Sync
  password are passed to it privately, never on a command line.

### Fixed
- Automatic downloads never completed: United's Akamai protection held requests from Python's
  HTTP library (no reply for 60 s, or an immediate 403) but answers curl normally.
- Status messages said "ccs+" instead of "CCS+".

### Removed
- The `httpx` library (replaced by curl).

## 0.0.4 — 2026-10-20

### Changed
- `docker-compose.yml` sets `pull_policy: always` for the app, so `docker compose up -d` (including
  a recreate) checks for a newer image first.

### Fixed
- Recreating the stack didn't pick up a moved `beta` tag without a separate `docker compose pull`.

## 0.0.3 — 2026-10-20

### Added
- **Upload Calendar.ics** in Setup: publish a file downloaded by hand from the Calendar Sync link
  (United's own procedure for Google Calendar) when the automatic download can't get through.

### Changed
- Timeout errors say whether the connection failed or the server never replied.

### Fixed
- Day codes (RDO, HDO, VRDO, VHDO…), which CCS+ sends as a midnight start with no end, appeared as
  00:00–01:00 events. They're now all-day events.
- Full reserve and sick days, sent as 00:01–23:59:59, weren't treated as 24-hour events. The
  24-hour rule now allows up to 5 minutes either way (previously 1).
- Event details on the status page started with a blank line.

## 0.0.2 — 2026-10-20

### Added
- Downloads from United's official **CCS+ Calendar Sync** (`Calendar.ics`) with your UID and
  Calendar Sync password, on a timer (`SYNC_INTERVAL_MINUTES`, default 60, minimum 15). Unchanged
  schedules aren't downloaded again (ETag).
- Events lasting exactly 24 hours (or 48, 72…) become all-day events (`ALLDAY_24H`).
- A month view on the status page, with ‹ › navigation, **Today** and event details.
- **Setup**: a checklist, a box for the CCS+ **Copy link** URL, and the CCS+ steps.
- A prebuilt image `ghcr.io/uuugh/calendar_stream`, tagged `0.0.x`, `beta` and `latest`, for amd64
  and arm64; `docker-compose.yml` uses `image:` and needs no build.
- Settings `CCS_CALENDAR_URL`, `SYNC_INTERVAL_MINUTES`, `ALLDAY_24H` and `IMAGE_TAG`.
- Protection against cross-site form submissions on the status page.

### Changed
- United's events are republished as sent (same IDs, times and details) under `CALENDAR_NAME`.
- Clear statuses for a rejected sign-in (automatic checks pause after 2), an Akamai block, and an
  answer that isn't a calendar. The previous feed is kept after any failure or a sudden empty
  calendar.

### Fixed
- The schedule couldn't be read: the CCS website blocks automated browsers (Akamai "Access Denied").

### Removed
- The headless browser (Playwright/Chromium), CCS website login and HTML parsing.
- Settings `CCS_URL` and `CCS_*_SELECTOR` (`SCRAPE_INTERVAL_MINUTES` is still read as a fallback).

## 0.0.1 — 2026-10-19

First release as **Calendar Stream** (previously `ccs_calendar`).

### Added
- iCalendar feed for Google Calendar, plus a shareable subscribe page.
- Status page with login results, sync history, upcoming events, debug captures and the version.
- `DEFAULT_EVENT_HOURS`: a number of hours, or `allday`, for items without an end time.
- Status-page lockout after 5 failed logins.
- All data stored in Postgres (`calendar_stream_db`).
- Docker secrets for the CCS login, the status-page login and the database password.

### Fixed
- Pages that never go quiet timed out while loading ("networkidle").
- Copy buttons didn't work when the status page was opened over plain HTTP.
