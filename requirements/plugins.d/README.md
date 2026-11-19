# plugins.d: one feature file per plugin

A plugin is what a connection needs before it can work (for example the Google plugin, the API client every Google connection requires). This folder holds one feature file for each plugin; what every plugin does is written once in `../plugins.md`.

Rules for this folder (in addition to `../README.md` and `../connections.d/README.md`):

1. **One file per plugin**, with its own ID prefix listed in `../README.md`.
2. **`../plugins.md` is the template** for a new plugin: the file states what it requires of every plugin and links to the rest (rule 5 of `../README.md`).
3. **A plugin knows nothing of its connections.** Behavior of a connection that uses the plugin is in `../connections.d/`, which links to the plugin; the plugin file never describes a connection.
4. Follow `../README.md` for the line format, statuses, links, `oldkey.md` and the check.
