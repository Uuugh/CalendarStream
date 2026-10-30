# Roadmap (subject to change)

Read when planning a version.

0.2 = more sources and destinations (0.2.8-beta.10: two-way sync with the Google calendars CalendarStream makes)

0.2.9 Outlook
- Outlook 1-way and 2-way Sync (Microsoft Graph): a Microsoft API module in ☰ Settings (an app registered once
  in Microsoft's Azure portal), then Connect me / Invite someone in each module, like Google.

0.2.10 Apple
- Apple iCloud 2-way Sync (CalDAV): an app-specific password per person (made at account.apple.com), entered on
  an invite page (kept encrypted); iCloud is checked every few minutes, since it sends no change notices.

0.2.11 Holidays
- Public holidays as calendars, only from sources free for commercial use with redistribution rights. First set:
  python-holidays (Vacanza, MIT), UK Government Bank Holidays (Open Government Licence v3.0), US OPM federal holidays
  (public domain), Victoria Government Important Dates (CC BY 4.0). For calendars those don't cover: Holibase
  (MIT / CC BY 4.0), date-holidays (ISC / CC BY-SA 3.0). Each licence's terms are checked when 0.2.11 is planned.

0.3 Backups
- Backups.

0.4 Additional Users
- Login via authentik.
- Each new login is a new user. The new user will need to add their own calendars unless a calendar has been shared with them
- Add share calendar with other users toggle to the top right of status and setup
- build the login on OpenID Connect in general, with authentik as the tested provider, so Authelia, Keycloak or Google logins also work.
- keep the built-in login as a fallback admin, so a broken authentik doesn't lock you out. And today's data should belong to whoever logs in first.
- put the share switch on each source and destination rather than one page-wide toggle. Sharing is per calendar, and you may want to share your schedule but not a personal feed.
- An unlock e-mail or code for a sign-in that's locked out.

0.5 Notifications
- triggers  are defined in rules say the may be resued
  - trip added, changed or dropped
  - failed sync, a sign-in rejected
  - settings allows options for (Apprise library): email, ntfy, Pushover, Telegram and others

0.6 Invitations/Booking
- (Filled in at its first PLAN.)

0.7 Theming

0.8 Admin dashboard
- API usage.
- A business dashboard of usage and cost: APIs, subscriptions, servers, domains, internet, PC purchases.

0.9 Documentation

0.10 Business website

## Low findings

Low findings from whole-app reviews (build_rules/4-review.md), done when that code is next changed. Each: the audit
issue, #N, file:line, what to do. Taken off when done.
