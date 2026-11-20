# AGENTS.md

For any AI agent (or person) working on CalendarStream: a self-hosted calendar app (Python today, being ported to
Dart/Flutter, one feature at a time, with `requirements/` as the spec). Read this file, then the README of the area
you will touch.

## The two laws

1. **No duplication. Say it once.** A rule is written in one place and referenced everywhere else (code, tests,
   requirements and process files alike). **Test:** `tests/tools/req_check.sh` lists identical statements; review: name
   the one place that owns the rule, and every other place only links to it.
2. **No exceptions.** If a rule has an exception, the rule is wrong: change it so it holds for every case, or give the
   different case its own rule. Never write "except", "never for" or "only when X is not". A new kind of thing follows the
   existing rules. **Test:** `req_check.sh` lists exception wording (a condition saying when something happens is fine);
   review: would the rule hold unchanged for the next new connection or component?

## Standing rules

- **The Product Owner decides.** Questions for them go in `requirements/open-questions.md`, one at a time, never in a
  handoff or a chat only; answers are read from its `Answer:` lines. **Test:** review: is every decision traceable to
  an `Answer:` line or an edit by the Product Owner?
- **Never revert or overwrite the Product Owner's edits.** They edit files directly; a status they leave blank means
  backlog. **Test:** before and after any change run `git status` and `git diff`; no status goes backwards
  (`backlog` or blank to `proposed`).
- **Requirements win over the Python app** where they differ. **Test:** review: no requirement is changed to match the old app.
- **The freeze:** no new features until the port is complete. **Test:** review: every new row traces to the old app or a
  Product Owner answer.
- **Never put real data or secrets anywhere** (the real schedule, username, Google secret). **Test:** review the diff;
  tests use made-up data.
- **Push after each verified commit; never merge a pull request by hand.** **Test:** `git status` is clean and
  `git log origin/<branch>` matches before you stop.

## Environment

No Python is installed: use bash, sed and awk. A tool layer may halve backslashes in commands; test any sed that must
match one. Line-ending warnings are harmless. `tests/tools/req_check.sh` takes about 30 seconds, writes no files, and
is run once at a time.

## Table of contents

| Path | What it holds |
|---|---|
| `requirements/` | The spec, one file per feature; `README.md` has the rules for writing it; `open-questions.md` (for now `build_rules/open-questions.md`) the questions for the Product Owner |
| `scrum/` | Roles, stories, sprints, definition of done, how the Orchestrator briefs and checks agents |
| `WORKING.md`, `WORKING.d/` | The temporary checklist: work in progress or awaiting action |
| `packages/`, `server/`, `client/` | The Dart port; `packages/README.md` holds its rules |
| `app/`, `tests/` | The Python app and its suites: the running app and the reference until the port is complete |
| `build_rules/` | Old working notes; `build_rules/README.md` says which files are live; do not follow the rest |
| `.claude/skills/dart-flutter/` | The Dart and Flutter skill |
| `docs/`, `tools/` | Screenshots; the Product Owner's scratch work (never read it) and tools |

## Before touching an area

Read the README of that area first (`requirements/README.md`, `packages/README.md`, `scrum/README.md`); it holds the
rules that apply there.

## Responsibilities

Who does what (Product Owner, Orchestrator, Coder, Tester, Reviewer) and how agents are briefed and checked: `scrum/README.md`.
