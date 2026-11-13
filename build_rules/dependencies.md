# Dependencies (made by `tests/tools/deps.py`; do not edit)

Which `app/` file imports which, leaves first: port a file when everything under **Depends on** is ported.
A file marked ⟲ is in an import cycle (it can't be ported before the files it cycles with are split). Suite 75
checks this file is current; rebuild it with `python3 tests/tools/deps.py`.

| Order | File | Depends on | Used by |
|---|---|---|---|
| 1 | `app/__init__.py` | nothing | `app.updates` |
| 2 | `app/calendars/defaults.py` | nothing | `app.calendars.parsing`, `app.calsync` |
| 3 | `app/calendars/download.py` | nothing | `app.calendars.downloads`, `app.calsync` |
| 4 | `app/calendars/errors.py` | nothing | `app.calendars.downloads`, `app.calendars.parsing`, `app.calendars.validation`, `app.calsync` |
| 5 | `app/calendars/event.py` | nothing | `app.calendars.edits`, `app.calendars.feed`, `app.calendars.parsing`, `app.calsync`, `app.links`, `app.rule_engine.matching`, `app.rule_engine.ruleset`, `app.rules`, `app.services.calendar_view`, `app.services.deletions`, `app.services.event_history`, `app.services.event_links`, `app.services.google_sync`, `app.services.publishing`, `app.services.route_helpers` |
| 6 | `app/calendars/meeting.py` | nothing | `app.calendars.parsing`, `app.calsync` |
| 7 | `app/calendars/view_helpers.py` | nothing | `app.main` |
| 8 | `app/config.py` | nothing | `app.main`, `app.routes.destinations`, `app.routes.page`, `app.routes.settings`, `app.routes.sources`, `app.routes.status` |
| 9 | `app/google/__init__.py` | nothing | nothing |
| 10 | `app/google/errors.py` | nothing | `app.google.api`, `app.google.failure_classifier`, `app.google.sync`, `app.gsync` |
| 11 | `app/google/failure_kind.py` | nothing | `app.google.failure_classifier`, `app.google.recovery_policy` |
| 12 | `app/google/health_state.py` | nothing | `app.google.health`, `app.google.recovery_decision`, `app.google.recovery_policy` |
| 13 | `app/google/readiness.py` | nothing | `app.routes.google` |
| 14 | `app/google/traffic_entry.py` | nothing | `app.google.api`, `app.google.traffic_log` |
| 15 | `app/i18n.py` | nothing | `app.main`, `app.routes.destinations`, `app.routes.page`, `app.routes.sources`, `app.services.event_history`, `app.services.page_settings` |
| 16 | `app/icons.py` | nothing | `app.main`, `app.routes.page` |
| 17 | `app/log_tail.py` | nothing | `app.main` |
| 18 | `app/routes/history.py` | nothing | `app.routes` |
| 19 | `app/rule_engine/__init__.py` | nothing | nothing |
| 20 | `app/rule_engine/rule_error.py` | nothing | `app.rule_engine.validation`, `app.rules` |
| 21 | `app/rule_engine/schema.py` | nothing | `app.rule_engine.conflicts`, `app.rule_engine.matching`, `app.rule_engine.migration`, `app.rule_engine.text_matching`, `app.rule_engine.validation`, `app.rules` |
| 22 | `app/rules_words.py` | nothing | `app.rule_engine.conflicts`, `app.rule_engine.matching`, `app.rule_engine.ruleset`, `app.rule_engine.validation`, `app.rules` |
| 23 | `app/runtime/__init__.py` | nothing | nothing |
| 24 | `app/secretbox.py` | nothing | `app.google.api`, `app.logins`, `app.main` |
| 25 | `app/services/__init__.py` | nothing | nothing |
| 26 | `app/services/addresses.py` | nothing | `app.main` |
| 27 | `app/services/administrator.py` | nothing | `app.main` |
| 28 | `app/services/authentication.py` | nothing | `app.main` |
| 29 | `app/services/calendar_destinations.py` | nothing | `app.main` |
| 30 | `app/services/calendar_sources.py` | nothing | `app.main` |
| 31 | `app/services/change.py` | nothing | `app.runtime.change` |
| 32 | `app/services/clock.py` | nothing | `app.main` |
| 33 | `app/services/event_templates.py` | nothing | `app.main` |
| 34 | `app/services/field_error.py` | nothing | `app.main` |
| 35 | `app/services/google_changes.py` | nothing | `app.main` |
| 36 | `app/services/google_job.py` | nothing | `app.main` |
| 37 | `app/services/google_view.py` | nothing | `app.main` |
| 38 | `app/services/http.py` | nothing | `app.main` |
| 39 | `app/services/invites.py` | nothing | `app.main` |
| 40 | `app/services/lifecycle.py` | nothing | `app.main` |
| 41 | `app/services/logging_setup.py` | nothing | `app.main` |
| 42 | `app/services/rule_migration.py` | nothing | `app.main` |
| 43 | `app/services/source_jobs.py` | nothing | `app.main` |
| 44 | `app/services/state.py` | nothing | `app.runtime.state`, `app.services.history` |
| 45 | `app/services/update_jobs.py` | nothing | `app.main` |
| 46 | `app/calendars/edits.py` | `app.calendars.event` | `app.calsync` |
| 47 | `app/calendars/feed.py` | `app.calendars.event` | `app.calsync` |
| 48 | `app/calendars/parsing.py` | `app.calendars.defaults`, `app.calendars.errors`, `app.calendars.event`, `app.calendars.meeting` | `app.calsync` |
| 49 | `app/calendars/validation.py` | `app.calendars.errors` | `app.calendars.downloads`, `app.calsync` |
| 50 | `app/google/failure_classifier.py` | `app.google.errors`, `app.google.failure_kind` | `app.google.health` |
| 51 | `app/google/recovery_decision.py` | `app.google.health_state` | `app.google.health`, `app.google.recovery_policy` |
| 52 | `app/google/traffic_log.py` | `app.google.traffic_entry` | `app.google.api`, `app.main` |
| 53 | `app/links.py` | `app.calendars.event` | `app.main`, `app.rule_engine.ruleset`, `app.rules` |
| 54 | `app/logins.py` | `app.secretbox` | `app.main`, `app.routes.account`, `app.routes.settings`, `app.routes.sources` |
| 55 | `app/rule_engine/conflicts.py` | `app.rule_engine.schema`, `app.rules_words` | `app.rules` |
| 56 | `app/rule_engine/text_matching.py` | `app.rule_engine.schema` | `app.rule_engine.matching`, `app.rule_engine.validation`, `app.rules` |
| 57 | `app/runtime/change.py` | `app.services.change` | `app.main` |
| 58 | `app/runtime/state.py` | `app.services.state` | `app.main` |
| 59 | `app/services/calendar_view.py` | `app.calendars.event` | `app.main` |
| 60 | `app/services/deletions.py` | `app.calendars.event` | `app.main` |
| 61 | `app/services/event_history.py` | `app.calendars.event`, `app.i18n` | `app.main` |
| 62 | `app/services/event_links.py` | `app.calendars.event` | `app.main` |
| 63 | `app/services/history.py` | `app.services.state` | `app.main` |
| 64 | `app/services/page_settings.py` | `app.i18n` | `app.main` |
| 65 | `app/services/route_helpers.py` | `app.calendars.event` | `app.main` |
| 66 | `app/updates.py` | `app` | `app.main`, `app.routes.settings`, `app.routes.status` |
| 67 | `app/calendars/downloads.py` | `app.calendars.download`, `app.calendars.errors`, `app.calendars.validation` | `app.calsync` |
| 68 | `app/google/api.py` | `app.google.errors`, `app.google.traffic_entry`, `app.google.traffic_log`, `app.secretbox` | `app.google.sync`, `app.gsync` |
| 69 | `app/google/recovery_policy.py` | `app.google.failure_kind`, `app.google.health_state`, `app.google.recovery_decision` | `app.google.health` |
| 70 | `app/routes/account.py` | `app.logins` | `app.main`, `app.routes` |
| 71 | `app/routes/settings.py` | `app.config`, `app.logins`, `app.updates` | `app.routes` |
| 72 | `app/routes/status.py` | `app.config`, `app.updates` | `app.routes` |
| 73 | `app/rule_engine/matching.py` | `app.calendars.event`, `app.rule_engine.schema`, `app.rule_engine.text_matching`, `app.rules_words` | `app.rule_engine.ruleset`, `app.rules` |
| 74 | `app/rule_engine/validation.py` | `app.rule_engine.rule_error`, `app.rule_engine.schema`, `app.rule_engine.text_matching`, `app.rules_words` | `app.rule_engine.migration`, `app.rules` |
| 75 | `app/calsync.py` | `app.calendars.defaults`, `app.calendars.download`, `app.calendars.downloads`, `app.calendars.edits`, `app.calendars.errors`, `app.calendars.event`, `app.calendars.feed`, `app.calendars.meeting`, `app.calendars.parsing`, `app.calendars.validation` | `app.google.sync`, `app.main`, `app.routes.destinations`, `app.routes.events`, `app.routes.page`, `app.routes.sources`, `app.store` |
| 76 | `app/google/health.py` | `app.google.failure_classifier`, `app.google.health_state`, `app.google.recovery_decision`, `app.google.recovery_policy` | `app.main` |
| 77 | `app/rule_engine/migration.py` | `app.rule_engine.schema`, `app.rule_engine.validation` | `app.rules` |
| 78 | `app/rule_engine/ruleset.py` | `app.calendars.event`, `app.links`, `app.rule_engine.matching`, `app.rules_words` | `app.rules` |
| 79 | `app/google/sync.py` | `app.calsync`, `app.google.api`, `app.google.errors` | `app.gsync` |
| 80 | `app/rules.py` | `app.calendars.event`, `app.links`, `app.rule_engine.conflicts`, `app.rule_engine.matching`, `app.rule_engine.migration`, `app.rule_engine.rule_error`, `app.rule_engine.ruleset`, `app.rule_engine.schema`, `app.rule_engine.text_matching`, `app.rule_engine.validation`, `app.rules_words` | `app.item_order`, `app.main`, `app.routes.events`, `app.routes.page`, `app.routes.rules`, `app.routes.sources`, `app.services.publishing`, `app.services.rule_settings` |
| 81 | `app/store.py` | `app.calsync` | `app.main`, `app.routes.destinations` |
| 82 | `app/gsync.py` | `app.google.api`, `app.google.errors`, `app.google.sync` | `app.main`, `app.routes.events`, `app.routes.google`, `app.routes.page`, `app.services.accounts`, `app.services.google_sync` |
| 83 | `app/item_order.py` | `app.rules` | `app.main` |
| 84 | `app/routes/destinations.py` | `app.calsync`, `app.config`, `app.i18n`, `app.store` | `app.routes` |
| 85 | `app/routes/rules.py` | `app.rules` | `app.main`, `app.routes` |
| 86 | `app/routes/sources.py` | `app.calsync`, `app.config`, `app.i18n`, `app.logins`, `app.rules` | `app.routes` |
| 87 | `app/services/publishing.py` | `app.calendars.event`, `app.rules` | `app.main` |
| 88 | `app/services/rule_settings.py` | `app.rules` | `app.main` |
| 89 | `app/routes/events.py` | `app.calsync`, `app.gsync`, `app.rules` | `app.main`, `app.routes` |
| 90 | `app/routes/google.py` | `app.google.readiness`, `app.gsync` | `app.routes` |
| 91 | `app/routes/page.py` | `app.calsync`, `app.config`, `app.gsync`, `app.i18n`, `app.icons`, `app.rules` | `app.main`, `app.routes` |
| 92 | `app/services/accounts.py` | `app.gsync` | `app.main` |
| 93 | `app/services/google_sync.py` | `app.calendars.event`, `app.gsync` | `app.main` |
| 94 | `app/routes/__init__.py` | `app.routes.account`, `app.routes.destinations`, `app.routes.events`, `app.routes.google`, `app.routes.history`, `app.routes.page`, `app.routes.rules`, `app.routes.settings`, `app.routes.sources`, `app.routes.status` | `app.main` |
| 95 | `app/main.py` | `app.calendars.view_helpers`, `app.calsync`, `app.config`, `app.google.health`, `app.google.traffic_log`, `app.gsync`, `app.i18n`, `app.icons`, `app.item_order`, `app.links`, `app.log_tail`, `app.logins`, `app.routes`, `app.routes.account`, `app.routes.events`, `app.routes.page`, `app.routes.rules`, `app.rules`, `app.runtime.change`, `app.runtime.state`, `app.secretbox`, `app.services.accounts`, `app.services.addresses`, `app.services.administrator`, `app.services.authentication`, `app.services.calendar_destinations`, `app.services.calendar_sources`, `app.services.calendar_view`, `app.services.clock`, `app.services.deletions`, `app.services.event_history`, `app.services.event_links`, `app.services.event_templates`, `app.services.field_error`, `app.services.google_changes`, `app.services.google_job`, `app.services.google_sync`, `app.services.google_view`, `app.services.history`, `app.services.http`, `app.services.invites`, `app.services.lifecycle`, `app.services.logging_setup`, `app.services.page_settings`, `app.services.publishing`, `app.services.route_helpers`, `app.services.rule_migration`, `app.services.rule_settings`, `app.services.source_jobs`, `app.services.update_jobs`, `app.store`, `app.updates` | nothing |
