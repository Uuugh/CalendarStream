# Dependencies (made by `tests/tools/deps.py`; do not edit)

Which `app/` file imports which, leaves first: port a file when everything under **Depends on** is ported.
A file marked ⟲ is in an import cycle (it can't be ported before the files it cycles with are split). Suite 75
checks this file is current; rebuild it with `python3 tests/tools/deps.py`.

| Order | File | Depends on | Used by |
|---|---|---|---|
| 1 | `app/__init__.py` | nothing | `app.updates` |
| 2 | `app/calendars/defaults.py` | nothing | `app.calsync` |
| 3 | `app/calendars/event.py` | nothing | `app.calsync` |
| 4 | `app/config.py` | nothing | `app.main`, `app.routes.destinations`, `app.routes.page`, `app.routes.settings`, `app.routes.sources`, `app.routes.status` |
| 5 | `app/google/__init__.py` | nothing | nothing |
| 6 | `app/google/errors.py` | nothing | `app.google.api`, `app.google.failure_classifier`, `app.google.sync`, `app.gsync` |
| 7 | `app/google/failure_kind.py` | nothing | `app.google.failure_classifier`, `app.google.recovery_policy` |
| 8 | `app/google/health_state.py` | nothing | `app.google.health`, `app.google.recovery_decision`, `app.google.recovery_policy` |
| 9 | `app/google/readiness.py` | nothing | `app.routes.google` |
| 10 | `app/google/traffic_entry.py` | nothing | `app.google.api`, `app.google.traffic_log` |
| 11 | `app/i18n.py` | nothing | `app.main`, `app.routes.destinations`, `app.routes.page`, `app.routes.sources` |
| 12 | `app/icons.py` | nothing | `app.main`, `app.routes.page` |
| 13 | `app/routes/__init__.py` | nothing | nothing |
| 14 | `app/rules_words.py` | nothing | `app.rules` |
| 15 | `app/secretbox.py` | nothing | `app.google.api`, `app.logins`, `app.main` |
| 16 | `app/calsync.py` | `app.calendars.defaults`, `app.calendars.event` | `app.google.sync`, `app.links`, `app.main`, `app.routes.destinations`, `app.routes.events`, `app.routes.page`, `app.routes.sources`, `app.rules`, `app.store` |
| 17 | `app/google/failure_classifier.py` | `app.google.errors`, `app.google.failure_kind` | `app.google.health` |
| 18 | `app/google/recovery_decision.py` | `app.google.health_state` | `app.google.health`, `app.google.recovery_policy` |
| 19 | `app/google/traffic_log.py` | `app.google.traffic_entry` | `app.google.api`, `app.main` |
| 20 | `app/logins.py` | `app.secretbox` | `app.main`, `app.routes.account`, `app.routes.settings`, `app.routes.sources` |
| 21 | `app/updates.py` | `app` | `app.main`, `app.routes.settings`, `app.routes.status` |
| 22 | `app/google/api.py` | `app.google.errors`, `app.google.traffic_entry`, `app.google.traffic_log`, `app.secretbox` | `app.google.sync`, `app.gsync` |
| 23 | `app/google/recovery_policy.py` | `app.google.failure_kind`, `app.google.health_state`, `app.google.recovery_decision` | `app.google.health` |
| 24 | `app/links.py` | `app.calsync` | `app.main`, `app.rules` |
| 25 | `app/store.py` | `app.calsync` | `app.main`, `app.routes.destinations` |
| 26 | `app/google/health.py` | `app.google.failure_classifier`, `app.google.health_state`, `app.google.recovery_decision`, `app.google.recovery_policy` | `app.main` |
| 27 | `app/google/sync.py` | `app.calsync`, `app.google.api`, `app.google.errors` | `app.gsync` |
| 28 | `app/rules.py` | `app.calsync`, `app.links`, `app.rules_words` | `app.main`, `app.routes.events`, `app.routes.page`, `app.routes.rules`, `app.routes.sources` |
| 29 | `app/gsync.py` | `app.google.api`, `app.google.errors`, `app.google.sync` | `app.main`, `app.routes.events`, `app.routes.google`, `app.routes.page` |
| 30 | `app/main.py` ⟲ | `app.calsync`, `app.config`, `app.google.health`, `app.google.traffic_log`, `app.gsync`, `app.i18n`, `app.icons`, `app.links`, `app.logins`, `app.routes.account`, `app.routes.events`, `app.routes.page`, `app.routes.rules`, `app.rules`, `app.secretbox`, `app.store`, `app.updates` | `app.routes.account`, `app.routes.destinations`, `app.routes.events`, `app.routes.google`, `app.routes.history`, `app.routes.page`, `app.routes.rules`, `app.routes.settings`, `app.routes.sources`, `app.routes.status` |
| 31 | `app/routes/account.py` ⟲ | `app.logins`, `app.main` | `app.main` |
| 32 | `app/routes/destinations.py` ⟲ | `app.calsync`, `app.config`, `app.i18n`, `app.main`, `app.routes.page`, `app.store` | nothing |
| 33 | `app/routes/events.py` ⟲ | `app.calsync`, `app.gsync`, `app.main`, `app.rules` | `app.main` |
| 34 | `app/routes/google.py` ⟲ | `app.google.readiness`, `app.gsync`, `app.main` | nothing |
| 35 | `app/routes/history.py` ⟲ | `app.main` | nothing |
| 36 | `app/routes/page.py` ⟲ | `app.calsync`, `app.config`, `app.gsync`, `app.i18n`, `app.icons`, `app.main`, `app.rules` | `app.main`, `app.routes.destinations` |
| 37 | `app/routes/rules.py` ⟲ | `app.main`, `app.rules` | `app.main` |
| 38 | `app/routes/settings.py` ⟲ | `app.config`, `app.logins`, `app.main`, `app.updates` | nothing |
| 39 | `app/routes/sources.py` ⟲ | `app.calsync`, `app.config`, `app.i18n`, `app.logins`, `app.main`, `app.rules` | nothing |
| 40 | `app/routes/status.py` ⟲ | `app.config`, `app.main`, `app.updates` | nothing |
