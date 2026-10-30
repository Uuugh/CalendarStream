# 0. Overview

Always loaded (imported by CLAUDE.md). The whole picture on one page; each step's file has its details.

## The steps

| Step | Command | Who | What happens | Details |
|---|---|---|---|---|
| 0. Overview | **DASH** (or **DASHBOARD**) | Claude | Opens the CalendarStream Dashboard beside the chat: the commands (each copies on a tap), every waiting F, I and R, who is being waited on, the likely next step and the roadmap. Claude keeps it up to date, so DASH only opens it. | this file |
| 1. Plan | **PLAN** | Developer › Claude | The Developer gives F, I, R and ?; PLAN shows the waiting list and what Claude would do for each, so it's corrected before it's built. | 1-plan.md |
| 2. Build | **BUILD** `[F\|f I\|i R\|r] [b m M]` | Claude | Builds the waiting inputs as the next beta: tests, publishes, reports. | 2-build.md |
| 3. Test (optional) | **TEST** | Developer + Claude, together | The Developer tries the beta in a browser and Claude follows along: each TEST, Claude looks at the page, its console and requests, and problems are talked through and written up as I items. | 3-test.md |
| 4. Review | **REVIEW** | ChatGPT ⇄ Claude; the Developer decides | The agents check without the Developer: Claude › ChatGPT › Claude › ChatGPT, then the Developer decides anything still disputed. REVIEW starts it; each REVIEW after that passes the turn. | 4-review.md |
| 5. Deploy | **DEPLOY** | Claude; the Developer tests | The first DEPLOY prepares the release (a whole-app review, translations, docs) and asks the Developer to test it; the second DEPLOY releases it as Stable/Latest. | 5-deploy.md |

**STOP** / **WAIT**: stop all work. No commit or push; no time, credits or tokens spent until the Developer says to continue.

Usual order: PLAN › BUILD › TEST if wanted, as often as needed › REVIEW whenever wanted › DEPLOY for a stable release.

**The Dashboard:**
- The step in progress has its command in green, like a status box; amber when something in it is missing.
  A line under it says where Claude is.
- "Waiting on" lists only who is being waited on, each line starting (Claude), (Rich) or (ChatGPT). Claude's
  requests appear under their item in amber.
- Every waiting item ends with its state in blue: approved, understood or resolved (and, once planned, which
  build it's in).
- The waiting list is sorted I, then F, then R, in number order; each number in blue, amber when Claude is
  asking something under it.
- "Waiting on" spells out the recommended path: the exact command to say next, when (for example after a usage
  reset), in which conversation, and how the remaining builds are split, with the reason when it saves usage (a
  new conversation, a smaller build, waiting for a reset).
- It is one artifact, "CalendarStream Dashboard", kept from conversation to conversation: a new conversation
  opens it from the link in the handoff (or the artifact list) and updates that one, never a copy.

## Conversations

- Every BUILD ends with a handoff (2-build.md, After). Claude's last two messages in that conversation are
  "New conversation CalendarStream v<version>" (the version now current; an R-only build keeps it) and the
  message for the Developer to paste as the new conversation's first.
- A new conversation starts from the handoff, this repo and the Dashboard: it reads these rules, runs
  `tests/tools/setup.sh`, and reads the Dashboard for the waiting list.
- TEST or REVIEW of the beta just built can stay in the same conversation while it's short. When the Developer
  carries on in a conversation that has already been summarized, Claude reminds them, in one line at the top of
  each reply, to start a new one from the handoff.
- The Developer doesn't need reminding about REVIEW.

## Commands

- Commands count only in capitals, so the same word in ordinary talk or dictation never starts anything. A
  command, with its options, ends the message ("Fix the title. BUILD", "BUILD b FI"); STOP and WAIT count anywhere in it.
- A command starts its step; said again while the step is open, it continues it (TEST: look now; REVIEW passes
  the turn; the second DEPLOY releases).
- A step in progress uses only what existed when it started. New F, I and R wait for the next PLAN and BUILD.
  To bring them into a step that's running, STOP it and start it again with its command. What happens inside
  a step is part of it: a review's findings, Claude's fixes for them, the Developer's decisions on them.
- GO and EOF are aliases of BUILD and work the same (GO R = BUILD R). MENU was DASH's name until 0.2.8-beta.18.

## Who does what

- **Developer**: the human. Owns the intent (F, I, R) and the decisions.
- **Claude**: the AI working on the project in the current session. Plans, builds, tests, releases: the
  author of the code.
- **Reviewer**: a separate AI from another vendor (ChatGPT for now). Checks Claude's work; never changes it.

## Inputs

- **F** = a feature request · **I** = an issue (something wrong) · **R** = the README, documentation or these
  rules. Either case (F or f). Numbered F1, F1.1…; numbers start again after each BUILD.
- **?** = a question: the Developer wants Claude's suggestion. It isn't an input until the Developer agrees.

## Ground rules

- Pull before editing, and keep the Developer's own edits.
- Anything with a link (a run, an issue, a release, a page to open) is given as that link, in messages and on
  the Dashboard.
- Never push half-finished or broken work.
- Never modify CCS+ (United's system): CalendarStream only reads it.
- Downloads identify themselves honestly: never disguise a client to get past United's bot protection.
- The Developer's real schedule (Calendar.ics), username and Google client secret never go into the repo, the
  tests, screenshots or messages. Use the made-up demo schedule (`tests/data/Demo.ics`, Username U123456).

## References (not steps)

- `theme.md`: how the page looks, with the Theme Rules pictures.
- `roadmap.md`: what's planned, and Low review findings waiting for their code to change.
