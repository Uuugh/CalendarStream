# Handoff: you are the orchestrator (updated Nov 19, 2026)

Read, in this order: `build_rules/README.md` (live and legacy files), `requirements/README.md` (the two laws and 14 rules, each with its test), `build_rules/orchestration.md` (roles, steps and their state), `build_rules/open-questions.md` (check it for answers before every edit). The `dart-flutter` skill is in `.claude/skills/dart-flutter/`. Do not follow the legacy files; do not rely on this page for anything the files above say.

## Your role

You keep the requirements consistent, run read-only agents (Reviewer, Coder, analysts) in slices, parse every report against the README rules, fix what is wrong in the one owning row, and pass the Product Owner only real decisions. You never build the app and never play the Coder. Show agent progress as simple bars, one per agent, and nothing else.

## How we work

1. **The Product Owner is one person, often dictating.** When unclear, ask in plain words, one question at a time, as the last line of a message. Never guess a big decision. A question is not an order.
2. **They edit the files directly, including answers in `open-questions.md`.** Run `git status`, `git diff` and read the `Answer:` lines before editing; never overwrite their work.
3. **The two laws: no duplication, no exceptions.** Fix a rule in its one owning row; everything else points to it. A change that breaks a law is probably wrong. Prefix scheme, status words (`proposed`, `backlog`) and message keys are defined once in the README.
4. **Requirements win over the old Python app** where they differ. The old app answers "what does it do" (rule 10), not "what should it do".
5. **Commit and push often.** Never merge pull requests by hand. Never put the real schedule, username or Google secret anywhere.
6. **Freeze:** no new features until the port is complete.

## Where things stand

See the steps table in `build_rules/orchestration.md`. In short: the requirements are reorganized and checked; the first full Coder review (baseline about 390 of 900 rows cannot be implemented) is triaged; six blind agents reverse-engineered the Python app and were compared with ours (data in `build_rules/reverse-engineering/`). **Next: fill the gaps slice by slice, starting with `compare/slice1.md` (account, settings, shell), then re-run the Coder review.**

The Product Owner should confirm these differences first (ours wins by default): global block at 25 failures (old app 50), unlock link 24 hours (1 hour), password rules configurable (fixed), stream token 22 characters of any character (32, letters, digits, hyphen, underscore), 50 connections in total (10 calendars, 20 destinations), each event keeps its own time zone in feeds and Google (UTC), a new Local calendar joins feeds only when none existed (every new one), one download interval for all sources (per source), CCS+ pause ends on Sync Now after the credentials are fixed (any successful sign-in), Backup and Restore exists (the old app has none), the 5-day view, dragging events and overflow counts (the old app has none).

## Practical

- `python` is not installed: use bash, sed, awk or the editor. A tool layer may halve backslashes in commands; test any sed that must match a literal one. `req_check.sh` takes about 30 seconds; do not run several in one command.
- Agents: a cold agent with a one-line prompt is the process test. Give each a progress file in the scratch folder. Stop them with TaskStop if the Product Owner's usage (`/usage`, the 5-hour figure) passes about 70%.
- Tests and CI: the heavy `Tests` workflow skips changes that touch only requirements, build_rules, docs or Markdown; the quick `Requirements` workflow runs `req_check.sh`.
- Memory notes: `C:\Users\rfrie\.claude\projects\C--Users-rfrie-Development-Projects-CalendarStream\memory\`.
- Dart SDK: `C:\Users\rfrie\Development\sdks\flutter\bin\dart`; code so far: `packages/domain`.
