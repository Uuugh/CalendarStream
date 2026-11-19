# connections.d: one feature file per kind of connection

A connection is a module in a section that synchronizes calendar events locally, one-way or two-way. This folder holds one feature file for each kind of connection; what every connection does is written once in `../connections.md` and is not repeated here.

Rules for this folder (in addition to `../README.md`):

1. **One file per kind**: `local_calendar.md`, `generic_feed.md`, `ccs.md`, `calendar_link.md`, `google_one_way.md`, `google_two_way.md`. A new kind of connection is a new file with its own ID prefix, listed in `../README.md` (Prefixes and Index).
2. **`../connections.md` is the template** for a new connection: the file states what it requires of every connection and links to the rest (rule 5 of `../README.md`).
3. **A new kind of connection** (for example Outlook or Apple, not yet created) is a new file that states its role; if it is both a source and a feed, the sections already contain it by CON-01.c, with no exception. **A connection that extends another** (Google two-way over Google one-way) holds only what it adds and links to the one it extends.
4. **Section behavior is not here.** How a section lists, orders, folds or adds modules is the section's feature file (for example `../sources.md`) and the shared UI (`../common.md`, UI-29, UI-30).
5. **Plugins** a connection needs are in `../plugins.d/`; the connection links to the plugin's requirement and does not restate it.
6. Follow `../README.md` for the line format, statuses, links, `oldkey.md` and the check (`tests/tools/req_check.sh`, which also reads this folder).
