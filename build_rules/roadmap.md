# Roadmap (subject to change)

Read when planning a version.



0.3 Theming
0.3.0 Phone mode: Settings a full page, with a back button in its left corner.
0.3.1 Printing
0.3.2 More themes
- option to change based on local time (vs system)
0.3.3 Cloud / attachment integration
- Attachments in an area at the bottom of an event's Notes

0.4 More sources and destinations 
0.4.1 Microsoft 365 / Outlook
- Outlook 1-way and 2-way Sync through Microsoft 365 OAuth (Microsoft Graph), for work-calendar integrations: a Microsoft API module in ☰ Settings (an app registered once
  in Microsoft's Azure portal), then Connect me / Invite someone in each module, like Google.
0.4.2 Apple
- Apple iCloud 2-way Sync (CalDAV): an app-specific password per person (made at account.apple.com), entered on
  an invite page (kept encrypted); iCloud is checked every few minutes, since it sends no change notices.

0.4.3 Holidays
- Public holidays as calendars, only from sources free for commercial use with redistribution rights. First set:
  python-holidays (Vacanza, MIT), UK Government Bank Holidays (Open Government Licence v3.0), US OPM federal holidays
  (public domain), Victoria Government Important Dates (CC BY 4.0). For calendars those don't cover: Holibase
  (MIT / CC BY 4.0), date-holidays (ISC / CC BY-SA 3.0). Each licence's terms are checked when 0.2.11 is planned.

0.4.4 Generic CalDAV
- Nextcloud, Fastmail and other self-hosted calendars.

0.4.5 CCS+ via iCal? (an idea to look into)

0.5 Backups

0.6 Additional Users
- Login via authentik.
- Each new login is a new user. The new user will need to add their own calendars unless a calendar has been shared with them
- Add share calendar with other users toggle to the top right of status and setup
- build the login on OpenID Connect in general, with authentik as the tested provider, so Authelia, Keycloak or Google logins also work.
- keep the built-in login as a fallback admin, so a broken authentik doesn't lock you out. And today's data should belong to whoever logs in first.
- put the share switch on each source and destination rather than one page-wide toggle. Sharing is per calendar, and you may want to share your schedule but not a personal feed.
- An unlock e-mail or code for a sign-in that's locked out.
- 0.6.1 Multi-user accounts and permissions, for family / team installs (the first part of this).
- 0.6.2 Privacy / busy-only output rules, for safe work / personal sharing.
- 0.6.3 A public REST API and webhooks, for outside automation.

0.7 App integration
0.7.0 NextCloud

0.8 Notifications
0.8.1 triggers  are defined in rules say the may be resued
  - trip added, changed or dropped
  - failed sync, a sign-in rejected
  - settings allows options for (Apprise library): email, ntfy, Pushover, Telegram and others

0.9 Invitations/Booking
0.9.1 Booking links and availability, like the scheduling platforms (the first part of this). The rest is filled in at its first PLAN.

0.10 Admin dashboard
- API usage.
- A business dashboard of usage and cost: APIs, subscriptions, servers, domains, internet, PC purchases.

0.11 Documentation

0.12 Native mobile apps
- Beyond the responsive web page.

0.13 Business website
