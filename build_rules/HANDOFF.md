# Handoff: you are the orchestrator (updated Nov 19, 2026)

Read, in this order: `build_rules/README.md` (live and legacy files), `requirements/README.md` (the two laws and 14 rules, each with its test), `build_rules/orchestration.md` (roles, steps and their state), `build_rules/open-questions.md` (check it for answers before every edit). The `dart-flutter` skill is in `.claude/skills/dart-flutter/`. Do not follow the legacy files; do not rely on this page for anything the files above say.

## Your role

You keep the requirements consistent, and you save your own context for every task, not only one step: the work itself (editing requirements, filling a slice, a review, a fix, later the port) is done by subagents, one per slice and one at a time when they share `common.md` or `messages/`; you brief them, check the result with `tests/tools/req_check.sh`, and commit. Run read-only agents (Reviewer, Coder, analysts) in slices, parse every report against the README rules, fix what is wrong in the one owning row, and pass the Product Owner only real decisions. You never build the app and never play the Coder. Show agent progress as simple bars, one per agent, and nothing else: whenever a subagent runs, show its bar (for example `slice 2 [#####-----] 50%`) in every message to the Product Owner until it finishes.

## How we work

1. **The Product Owner is one person, often dictating.** When unclear, ask in plain words, one question at a time, as the last line of a message. Never guess a big decision. A question is not an order.
2. **They edit the files directly, including answers in `open-questions.md`.** Run `git status`, `git diff` and read the `Answer:` lines before editing; never overwrite their work.
3. **The two laws: no duplication, no exceptions.** Fix a rule in its one owning row; everything else points to it. A change that breaks a law is probably wrong. Prefix scheme, status words (`proposed`, `backlog`) and message keys are defined once in the README.
4. **Requirements win over the old Python app** where they differ. The old app answers "what does it do" (rule 10), not "what should it do".
5. **Commit and push often.** Never merge pull requests by hand. Never put the real schedule, username or Google secret anywhere.
6. **Freeze:** no new features until the port is complete.

## Where things stand

See the steps table in `build_rules/orchestration.md`. In short: the requirements are reorganized and checked; the first full Coder review (baseline about 390 of 900 rows cannot be implemented) is triaged; six blind agents reverse-engineered the Python app and were compared with ours (data in `build_rules/reverse-engineering/`). **All six slices of gaps are filled. Next (step 5): the Product Owner answers `open-questions.md`, agrees to rows and decides the three proposed rule changes; then (step 6) the six Coder slices are re-run.**

The Product Owner should confirm these differences first (ours wins by default): global block at 25 failures (old app 50), unlock link 24 hours (1 hour), password rules configurable (fixed), stream token 22 characters of any character (32, letters, digits, hyphen, underscore), 50 connections in total (10 calendars, 20 destinations), each event keeps its own time zone in feeds and Google (UTC), a new Local calendar joins feeds only when none existed (every new one), one download interval for all sources (per source), CCS+ pause ends on Sync Now after the credentials are fixed (any successful sign-in), Backup and Restore exists (the old app has none), the 5-day view, dragging events and overflow counts (the old app has none).

## Practical

- `python` is not installed: use bash, sed, awk or the editor. A tool layer may halve backslashes in commands; test any sed that must match a literal one. `req_check.sh` takes about 30 seconds; do not run several in one command.
- Agents: a cold agent with a one-line prompt is the process test. Give each a progress file in the scratch folder. Stop them with TaskStop if the Product Owner's usage (`/usage`, the 5-hour figure) passes about 70%.
- Tests and CI: the heavy `Tests` workflow skips changes that touch only requirements, build_rules, docs or Markdown; the quick `Requirements` workflow runs `req_check.sh`.
- Memory notes: `C:\Users\rfrie\.claude\projects\C--Users-rfrie-Development-Projects-CalendarStream\memory\`.
- Dart SDK: `C:\Users\rfrie\Development\sdks\flutter\bin\dart`; code so far: `packages/domain`.

## Progress bars (how the Product Owner wants agent progress shown)

The Product Owner wants one simple bar per running agent and nothing else: no commentary, no recap of what the agents are doing.

**Setup, before launching agents**
1. Use the scratch folder named in the session's system prompt (it changes each session). Make a progress file per agent, `progress-<name>.txt`, containing `0/<total>`, where total is the number of units the agent will finish (files in its slice, or topics).
2. Put in each agent's prompt: after finishing each unit, overwrite that exact file with `done/total` (for example `2/6`). It is the only file the agent may write besides its output file. Some agents write it only once, at the end; that is fine, the bar then jumps.
3. Launch every agent in the background (`run_in_background`), one per slice, in the same message.

**Showing the bars.** Whenever a report or notification arrives, read the files and render all agents together in a code block, one line per agent: label, 20 characters of bar, `done/total`, and the word `done` when it has finished. Then add at most one sentence (for example the headline of a finished report). Example:

```
Slice 1  Account, settings, shell      [####################]  5/5  done
Slice 2  Calendar, print, search       [########............]  2/6
```

Rendering (bash; `$SP` is the scratch folder):

```bash
names=("Slice one" "Slice two"); for i in 1 2; do v=$(tr -d '\n' < $SP/progress-$i.txt); d=${v%%/*}; t=${v##*/}; case "$d" in done) d=$t;; esac; w=20; f=$((d*w/t)); printf "%-24s [%s%s] %s/%s\n" "${names[$((i-1))]}" "$(printf '#%.0s' $(seq 1 $f) 2>/dev/null)" "$(printf '.%.0s' $(seq 1 $((w-f))))" $d $t; done
```

**Rules**
- Never poll in a loop and never sleep to wait: the harness sends a notification when each agent finishes; draw the bars then.
- Do not edit the repository while agents are reading it (an agent reading files you change gives inconsistent reports), unless the agents are blind to those files.
- To pause, stop the agents with the TaskStop tool (their partial output stays in the scratch folder), and tell the Product Owner what was saved. To resume, relaunch with a prompt that says to keep the existing output file and continue with the topics not yet written.
- Tell the Product Owner the token use each finished agent reports; they read their own usage meter with `/usage`.
