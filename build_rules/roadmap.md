# Roadmap (subject to change)

Read when planning a version.

0.2 = more sources and destinations (0.2.8-beta.10: two-way sync with the Google calendars CalendarStream makes)

0.3 Backups, and more two-way calendars
- Backups.
- Outlook 1-way Sync and Outlook 2-way Sync (Microsoft Graph): a "Microsoft API" module in ☰ Settings (an app
  registered once in Microsoft's Azure portal), then Connect me / Invite someone in each module, like Google.
- Apple iCloud 2-way Sync (CalDAV): each person makes an app-specific password at account.apple.com and enters it
  on an invite page (kept encrypted); iCloud is checked every few minutes, since it sends no change notices.
- Claude reminds the Developer of these at the first PLAN of 0.3.

0.4 Additional Users
- Login via authentik.
- Each new login is a new user. The new user will need to add their own calendars unless a calendar has been shared with them
- Add share calendar with other users toggle to the top right of status and setup
- build the login on OpenID Connect in general, with authentik as the tested provider, so Authelia, Keycloak or Google logins also work.
- keep the built-in login as a fallback admin, so a broken authentik doesn't lock you out. And today's data should belong to whoever logs in first.
- put the share switch on each source and destination rather than one page-wide toggle. Sharing is per calendar, and you may want to share your schedule but not a personal feed.

0.5 Notifications
- triggers  are defined in rules say the may be resued
  - trip added, changed or dropped
  - failed sync, a sign-in rejected
  - settings allows options for (Apprise library): email, ntfy, Pushover, Telegram and others

0.6 Theming

## Low findings

Low findings from whole-app reviews (build_rules/4-review.md), done when that code is next changed. Each: the audit
issue, #N, file:line, what to do. Taken off when done.
