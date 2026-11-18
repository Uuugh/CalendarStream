# Transition plan: Python to Dart/Flutter, feature-first, requirements-driven

DRAFT for the Developer's approval. Nothing in app/ or tests/ has been moved. This file is the working record of the
decisions, so a new conversation (or another AI) can resume from it. Sizes are Python line counts at 0.2.8-beta.46.

## Decisions so far (Developer, this conversation)

- **Total freeze:** no new features or requirements until the transition is complete. Python stays the running app.
- **Letters:** [F]eature = a capability or section of the app (a module, a distinct function such as printing).
  [R]equirement = one checkable rule of behavior of a feature. [I]ssue = a component identified as not meeting a
  requirement. [P]rocess = how work is done here (was the old R). "Rule" now only means a rule in the app's Rules feature.
- **Requirements live in the repo**, one list per feature, with a Planned section (a waiting F becomes a planned
  requirement; a built F becomes a verified one). **Issues** go to a database, keeping their numbers (default:
  GitHub Issues titled "I22: …" with a feature label; the Dashboard reads from it).
- **History is not kept:** old F, I and R items are converted; CHANGELOG.md, build-costs.md and beta entries stay as
  they are. README and documentation items become planned requirements of a `documentation` feature.
- **Port, not a Python restructure.** The Python app is the reference and its suites are the oracle. Structure lives in
  the Dart project. Python splits happen only where they make a clearer specification (the `Store` split into
  repositories; Google api/sync into service and repository halves).
- **Dart on the client and the server.** The domain layer is one package shared by both.
- **No transition build publishes a beta**; one beta ships at the end, then a stable release after the Developer's test.
- **Plan order:** 1 the tree (this file) · 1a update the Processes (new letters; remove rules that contradict the
  method) · 2 move Features into requirements · 3 move Issues to the database and redesign the Dashboard ·
  4 the port, feature by feature · 5 retire Python.

## The Dart layout

```
calendarstream/
├─ requirements/                   language-neutral spec, one file per feature (read by both implementations)
│  └─ <feature>.md                 verified requirements, then a Planned section; each line: ID | status | statement | test
├─ packages/
│  ├─ domain/                      pure Dart: no Flutter, no I/O. Shared by the server and the app.
│  │  ├─ lib/<feature>.dart        a feature's public surface (the only thing others import)
│  │  ├─ lib/<feature>/src/        models, logic, use_cases (private by Dart's own rule)
│  │  └─ test/<feature>/           mirrors lib/; each test names its requirement ID
│  ├─ contract/                    request/response types (JSON) used by the server and the app, so they cannot drift
│  └─ testing/                     fakes (FakeEventRepository, FakeGoogleCalendarService …) and made-up test data
│                                  (Demo.ics, work.ics; never real data); mirrors Flutter's testing/ subpackage
├─ server/                         Dart server (Docker, Postgres): scheduled downloads, feeds, Google sync, the JSON API
│  ├─ bin/main.dart                composition only
│  ├─ lib/shared/                  database (pool, schema), utils (clock, crypto, logging), config
│  ├─ lib/features/<feature>/
│  │  ├─ data/                     repositories/ (source of truth for one kind of stored data), services/ (one external source)
│  │  └─ http/                     JSON routes
│  └─ test/                        mirrors lib/
├─ client/                         Flutter app: web, phone, desktop from one codebase
│  ├─ lib/main.dart (+ main_development.dart)
│  ├─ lib/shell/                   the frame: top bar, modules and sections, navigation, routing, the adaptive
│  │                               layout choices (by window size, never device type). May import every feature.
│  ├─ lib/shared/ui/               common widgets: pop-up shell (full-screen on a phone, modal when wide), field with
│  │                               its note, Cancel | Save row, status words, legend, theme tokens, icons, i18n
│  ├─ lib/features/<feature>/
│  │  ├─ data/                     client repositories (call the server through `contract`), platform services
│  │  └─ ui/                       views and view models (one view + one view model per screen)
│  └─ test/ · integration_test/    mirrors lib/; the thin end-to-end set
├─ app/ and tests/                 the Python app and its suites: frozen reference, deleted at step 5
├─ build_rules/                    Process: P rules, roadmap.md (planned versions only), low-findings.md, build-costs.md
├─ docs/                           screenshots/, development/ (unchanged)
└─ README.md, CHANGELOG.md, AGENTS.md, CLAUDE.md, VERSION
```

Features (each has a requirements file; the domain package and the server/client folders carry the same names):
`calendar` · `sources` · `feeds` · `rules` · `event_templates` · `events` · `history` · `google` · `settings` ·
`account` · `diagnostics` (status, Report a problem, health, debug captures) · `documentation` (requirements only, no code).
`shell` is not a feature: it is the client's own area.

### Rules of the layout

- **Layers** (Flutter's, R18/R26): `domain` imports nothing from `data`, `http` or `ui`. A **Repository** is the source of
  truth for one kind of stored data and never imports another; a **Service** wraps one external source and holds no
  state; a use case combines them.
- **Features depend one way:** `calendar, sources, feeds, history` → `events`, `rules` → `shared`;
  `event_templates` → `events` (a template is an event with no date) → `shared`; `google` → `events`, `feeds`, `rules`;
  `settings`, `account`, `diagnostics` → `shared`. The Event model sits in `shared`, so Rules never imports Events.
  No cycles. A feature imports another only through its public file (`lib/<feature>.dart`; `src/` is private).
- **UI is standardized once.** Generic widgets are in `shared/ui`; a widget that must know what a rule or an event is
  belongs to its owning feature and is exported: the rule editor (Rules), the event editor (Events, also used by
  Event Templates), the calendar picker (Sources). A second copy of either is a defect.
- **Platform differences stay in the UI layer and in platform services:** layout is chosen by measured window size
  (compact, medium, expanded); `defaultTargetPlatform`, not `dart:io`, for UI branches.
- **`main` composes and nothing else** (target: under about 200 lines each for `bin/main.dart` and `lib/main.dart`).
- **Tests:** `test/` mirrors `lib/`; every requirement has a test that names its ID and every such ID exists (a script
  checks both ways); fakes come from `packages/testing`. During the port a feature is done when the Dart version meets
  its requirements and the Python suites that cover them agree.

## Where each Python file goes (the porting map)

`D` domain · `R` repository · `S` service · `U` use case · `V` view model · `W` view.

**Shared (domain/server/client).** `calendars/event.py`, `defaults.py` → domain `shared`. `calendars/errors.py`,
`download.py`, `google/errors.py`, `rule_engine/rule_error.py` → closed error families in `domain`. `store.py` (460) →
server `shared/database` + one repository per feature. `config.py`, `secretbox.py`, `clock.py`, `logging_setup.py`,
`log_tail.py`, `item_order.py` → server `shared`. `i18n.py`, `icons.py`, `templates/index.html` macros, `_theme.html`,
`js/01-base`, `07-saving`, `10-fields`, `12-handles-checks`, `14-status-fold`, `15-field-notes`, `topbar.html`,
`styles` shared parts, `static/`, `locales/` → client `shared/ui` and `shell`. `main.py` (1955: 157 functions that
mostly forward to services for old callers and monkeypatching), `runtime/`, `calsync.py`, `gsync.py`, `rules.py`
(facades) → nothing; they are not ported.

**calendar:** `services/calendar_view.py` (V), `calendars/view_helpers.py`, `routes/page.py` (calendar and print
parts, 1045), `calendar.html`, `js/02-calendar`, `11-reminders-print`, `styles/19-calendar*.css`.
**sources:** `calendars/downloads.py` (437, S), `parsing.py` (D), `validation.py` (D), `services/calendar_sources.py` (R),
`source_jobs.py` (U), `routes/sources.py` (904), `logins.py` CCS part (R), `sources.html`, `js/09-remove-import`.
**feeds:** `calendars/feed.py` (D), `services/calendar_destinations.py` (R), `publishing.py` (U),
`routes/destinations.py` (474), `feeds.html`, `js/13-feeds`.
**rules:** `rule_engine/*` (about 1000 lines, D), `rules_words.py`, `services/rule_settings.py` (R), `rule_migration.py`,
`routes/rules.py` (428), `rules.html`, `rule-dialog.html`, `js/06-rules`; exports the rule editor.
**event_templates:** `services/event_templates.py` (R), `templates.html`, `templates-dialog.html`, its parts of `routes/rules.py`.
**events:** `calendars/edits.py`, `meeting.py` (D), `services/event_links.py`, `links.py` (U), `deletions.py` (R),
`routes/events.py` (790), `event-pick.html`, `js/08-events`; exports the event editor.
**history:** `services/history.py`, `change.py`, `state.py`, `event_history.py` (R, U), `routes/history.py`, `history.html`.
**google:** `google/api.py` (466; split into `GoogleAuthService`, `GoogleCalendarService`, `GoogleTokenRepository`),
`google/sync.py` (685; API half to the service, decisions to a use case), `health.py`, `failure_classifier.py`,
`recovery_policy.py`, `readiness.py` and enums (D), `traffic_*` (R), `services/google_*.py`, `accounts.py`, `invites.py`,
`routes/google.py` (728), `js/16-beta-traffic`.
**settings:** `services/page_settings.py`, `addresses.py`, `administrator.py`, `updates.py` (S: `UpdateCheckService`),
`update_jobs.py`, `routes/settings.py` (328), `settings.html`, `js/03-topbar-settings`, `04-modules`.
**account:** `services/authentication.py` (259), `logins.py` status-page part (R), `routes/account.py` (274).
**diagnostics:** `routes/status.py` (187), `report-dialog.html`, `js/05-report`.

Not ported: Jinja templates, the page script and the stylesheets (they are rewritten as widgets; the pixel-diff
tooling stays for the Python page only).

## Port order

1. Features with only domain logic and clear tests: `rules`, `event_templates`, then `events`, `calendar`'s view logic.
2. Data-heavy: `sources`, `feeds`, `history`.
3. External: `google` (risky; reviewed by the other AI, as 2-build.md already requires), `settings`, `account`.
4. The `shell` and `shared/ui` as the first screens need them.
5. Retire Python only when every requirement passes on the Dart side and the Developer has tested it.

## Other rules this touches (found by checking build_rules/ and AGENTS.md)

1. "New behavior gets tests in a new suite (the next number)" (2-build.md; tests/README.md) and "one suite per version"
   (4-review.md) contradict tests that mirror the feature. Removed in step 1a.
2. The review-area table (4-review.md) is by Python path and already stale (low-findings BR04): becomes by feature.
3. `dependencies.md` is made by `tests/tools/deps.py` and checked by a test; it describes the Python tree and goes with it.
4. The paused parallel-test design (ports 8200 + suite number, shard timings by suite number) is for the Python
   suites only; it stays useful for running the oracle in shards on another machine.
5. AGENTS.md's "Where things are" and code map are rewritten for the Dart tree. Its `services/` (application
   services) contradicts R26's Service (one external source, no state); the Dart layout resolves it.
6. The command letters change: `BUILD R` (old: README, docs, rules; no version) becomes `BUILD P`.
7. theme.md's paths (`app/styles`, `app/templates/js`, `_theme.html`) change; its visual rules carry over.
8. No conflict found with R18, R19, R26, the checkpoint rules or ui_ux.md.

## Resume here (updated at each checkpoint)

- Done: decisions above; this file; step 1a for 0-overview.md, 1-plan.md, 2-build.md, 4-review.md, 5-deploy.md
  (letters, `BUILD P`, tests named by requirement, no new per-version suites, ChatGPT handoff access).
- Step 1a is done (dashboard.md, 3-test.md, AGENTS.md also updated). Next: step 2 (requirements), starting with the
  reconciliation of the Python suites (ChatGPT Task A below); the review-area table in 4-review.md changes at the port.
- ChatGPT Task A (inventory of the Python suites into `requirements/inventory/`) was handed over Nov 17 and is
  in progress on `chatgpt/inventory-*` branches; Claude reviews each pull request.
- Work can be split with ChatGPT through GitHub (2-build.md, "Handing BUILD to another AI"): content is pasted, never
  the Dashboard link; each task is scoped and checkable; Claude reviews what comes back.
- Step 2, first pass (Nov 17): the Dashboard's waiting F items are converted into `requirements/{calendar,settings,events,
  google,diagnostics,shell}.md` (statuses: verified / built / open / planned; the Developer's Good | Bad verdicts were
  read first). Still to do in step 2: the I items stay for step 3; R18–R28 are already in the process files (now P);
  verified requirements come from ChatGPT's inventory plus the README and CHANGELOG, one feature at a time for approval.
- Step 3, first part (Nov 17): the 20 open Issues on the Dashboard are now GitHub issues #22 to #41, titled "I<n>: …"
  with labels `issue` and `feature:<name>` and a Requirement line in the body (same I numbers). Not yet done: the
  Dashboard still shows them; its redesign to read GitHub (and the generated requirements summary) is the rest of step 3.
  I22 has a Bad verdict but no Dashboard item (F65 absorbed it): not created, to be decided with the Developer.
- Step 2: ChatGPT's PR #42 (inventory of suites 12-21, `requirements/inventory/`) reviewed by Claude and merged by the
  Developer's instruction (Nov 17). Next batches: suites 22-31 and on. I22 is GitHub issue #43 (open; conflicts with SET-06).
- I22 (#43) closed Nov 17: the Developer chose to keep the separate Settings pop-ups; SET-06 stands. Inventory PRs #44-#48
  merged (suites 22-71); #49 (72-81) awaits a README conflict fix by ChatGPT.
- Dashboard (decided Nov 17): it is redone after all other steps are done, as a live web page, not an artifact. A public
  read-only page on GitHub Pages (built in CI from GitHub issues and `requirements/*.md`) is possible, but GitHub Pages is
  public, so the Developer's private files (`docs/development/*`, gitignored) and Good | Bad verdicts never go there.
  They move into the app itself, in `diagnostics`, behind the app's login, served by the Dart server and never committed.
- Answered Nov 17: Q-M (GitHub auto-merge Action for inventory PRs: .github/workflows/inventory-automerge.yml), Q-R1 (layout measurements left to theme), Q-R2 (migration requirement kept until ported), Q-R3 (responsive web layout; phone app reuses the theme), Q-R4 (RUL-03..43 verified in requirements/rules.md).
- Answers Nov 17: (Q-S1) Claude drafts the requirements for ALL features first, then the Developer reviews them. (Q-S3)
  Taichi: Ollama at 192.168.0.109 (reachable from this machine, port 11434, no model loaded yet; models to be chosen
  together with the Developer). (Q-S4) Dart/Flutter SDKs are at C:\Users\rfrie\Development\sdks (flutter, android);
  Claude uses them from there. (Q-S5) Yes: Claude may push a branch to run the full Python suites in CI as the baseline.
- Step order (Developer, Nov 17): 1 tree, 1a processes, 2 requirements, 3 issues, 4 the port, 5 retire Python, then
  **6 analyze parallel testing** (new: how the Dart tests are split and run in parallel, now that the Flutter port
  removes many of the Python suites' problems: ports, shared Postgres, shard timings), then **7 the Dashboard**.
  The paused Python test overhaul is therefore not continued (see Q-S2). The Dashboard must be able to monitor testing
  progress (runs, shards, pass/fail per requirement), so step 6 decides what the test runs report and where.
- Q-S2 answered Nov 17: the paused Python test overhaul (sharding, ports, suite 82, workflow changes) is parked on the
  branch `paused/test-parallel` (commit 85f404b, pushed) and is the input for step 6 (analyze parallel testing). It is
  not merged and not continued on main. The working tree on main is clean.
- Step 2 rule (Developer, Nov 17): feature requirements state what the feature does; behavior shared by several features is
  written once in `requirements/drafts/shared_ui.md` (UI-NN) and referenced. **When all feature drafts are built, Claude
  runs a duplication review across every draft (same behavior stated in two features, UI mechanics inside a feature,
  overlaps with approved requirements such as RUL-36/41 and planned EVT-01..03) and fixes it BEFORE the Developer
  reviews.** The Developer reviews only the de-duplicated set. Shared UI rows moved so far: UI-01..UI-10.
- Answers Nov 17: Q-R5 yes: RUL-37, 39, 40, 41, 43 reworded without UI mechanics; RUL-38 and RUL-42 dropped (rules.md now
  has RUL-03..37, 39..41, 43). Q-U1: palettes and emoji pickers are common tools: UI-10 is one shared palette (the event
  editor adds a "calendar default" choice), UI-11 one shared emoji picker. Q-E1 (Claude's decision, the Developer did not
  know the question): EVT-25 merged into the planned EVT-01 (Duplicate).
- Answers Nov 17 (Q-P1, Q-P2: the Developer pointed to the Dart RegExp docs, api.flutter.dev/flutter/dart-core/RegExp-class.html).
  The docs confirm Dart's RegExp implements the ECMAScript specification with a backtracking engine that cannot be replaced
  and has no time limit; a pathological pattern such as `^(a*|b)*c` doubles in time with each extra character. Decisions
  (Claude, from the docs): (1) RUL-22 is met in the Dart server by running each user regex in a short-lived isolate with a
  timeout (the domain package keeps the pure matcher); (2) the regex error wording is Dart's own, prefixed "Not a valid
  regex:", so tests assert the prefix, not Python's text. New risk: Python-only regex syntax does not compile in Dart
  (asked as Q-P3).
- Q-P3 answered Nov 17 (Developer): use Dart's regex, matching Python's syntax is not needed; the requirement is that the user
  can build a rule or search with a regex, and the site checks its legality and highlights the broken part (new RUL-44,
  built and tested in packages/domain: `regexProblem` finds the position, because Dart gives only a message). Saved rules
  that use Python-only syntax will fail to compile; the port flags them as broken at migration instead of dropping them.
- Q-D1 answered Nov 17: `deployment` is a feature (requirements only for now; in the port, the Docker, installer and updater
  side). Draft: requirements/drafts/deployment.md (DEP-01..13, from GPT's README scan). Prefix DEP.
- Duplication review (Nov 17, Claude): done across requirements/drafts/*. Moved to one owner and referenced: secrets and
  tokens (ACC-11, referenced by SRC-08 and GGL-07; GGL-39 dropped), form security (ACC-13/14, referenced by SRC-05), public
  address (SET-08..16, referenced by GGL-45), feed name suggestions (FED-15 absorbs FED-26; FED-20 dropped), read/write round
  trip (FED-29 only; SRC-60 dropped), view change (CAL-33 absorbs CAL-36), templates picker (TPL-05/07; EVT-26 dropped);
  reload/phone-width mechanics removed from CAL-45/49, SRC-24/31/33. Questions from all (?) rows are in open-questions.md.
- Q-L1 answered Nov 17 (Developer): the data must be kept. The Dart server reads and writes the SAME Postgres database the
  Python app uses (tables kv, events, event_edits, custom_events, google_events, calendar_files, debug_files, activity_log).
  No table or column changes are needed. Compatibility work for the port: (1) Fernet decryption of kv secrets (key = PBKDF2-
  SHA256, 390,000 rounds, from DB_PASSWORD, salt in each sealed value), (2) scrypt (n=2^14, r=8, p=1) page-password hashes,
  (3) the same jsonb shapes in kv (rules, sources, destinations; keep unknown fields), (4) the idempotent startup
  statements (ALTER ... IF NOT EXISTS) run unchanged, never renaming or dropping, (5) Python-only regexes in saved rules are
  flagged (Q-P3 decision). The Dart app is first run against a COPY of the database; Python stays able to read it until step 5.
- Data plan REVISED Nov 17 (Developer's suggestion, supersedes the "same schema" plan above): the Dart server owns a NEW
  database with a schema designed for Dart (typed columns and Dart-owned migrations, not the Python app's kv blob), and a
  one-time Python migration tool (`tools/migrate_to_dart.py`, built before step 5, deleted with Python) copies the data from
  the old database. The old database is only read, never changed, so Python and the old data stay usable until the Developer
  accepts the result. The tool decrypts the Fernet secrets with the Python code and re-encrypts them for Dart, so Dart needs no
  Fernet; it carries events, edits, custom events, History, rules, sources, destinations, settings, Google connection and
  feeds, flags rules whose regex is Python-only, and prints a report (row counts and a comparison) to check. The port order gains
  step 4a: the Dart database schema and the migration tool, after the domain packages and before the server features that store data.
- Answers Nov 17 (Developer): ACC-16: 5 failures per address, 25 together (Python: 50), 15 minutes, 7 days of trust, 24-hour
  unlock link (Python: 1 hour); ACC-17: own networks 192.168.0.0 and 10.10.0.0 (taken as /16, to confirm) plus loopback and
  the public domain; CAL-54: hidden key choices are preserved when leaving Full page, CAL-07 reworded to match CAL-08.
- Time decision (Developer, Nov 17): all times are stored in UTC; an event's time zone is for data entry and display. This
  changes the Python model (ISO strings with an offset, in the display zone): the Dart `Event` will hold UTC instants plus
  the zone name for start and end, and all-day events as dates (Q-T1). Touches CAL-24/25, EVT-05/13, FED-03, GGL-11/26,
  RUL-07/08/16, the fingerprint and recurrence expansion; migration needs a zone for old offset-only times (Q-T3).
- Q-T1 answered Nov 17 (Developer): an all-day event is stored as a 24-hour event, local midnight to local midnight (00:00 to
  23:59, or 00:01 to 00:00, whichever codes better), with the UTC offset of its local time. The local time zone is the default
  from the imported event, or whatever was selected when the event was created. Q-T3 (Developer): the migration follows Q-T2's
  zone rule. Open: Q-T2 (zone for rules), Q-T4 (DST days), Q-T5 (all-day display date).
- Time zones (Developer, Nov 17): CAL-19 defines Local time: events are viewed in the Local zone the user chose (or the system
  clock's zone); each event keeps its creation zone in the database until edited with Edit Event; a new event defaults to the system
  zone, or to the calendar's zone if one is selected (EVT-05). Drafts CAL-19, CAL-25 (CAL-26 merged), EVT-05 updated.
