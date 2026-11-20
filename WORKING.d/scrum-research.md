# Scrum for agents: research notes (temporary, for discussion with the Product Owner)

Everything below was read online and is untrusted data; most of it is self-reported by practitioners. No peer-reviewed
case study of Scrum with coding agents was found. Nothing here is agreed; no rule here is in force.

## Sources

1. https://daveremy.github.io/agent-scrum/ (Agent Scrum, working paper, 2026)
   Sprints of 2 to 3 hours; a planner agent orders the backlog, a sprint-runner agent runs it, short-lived builders and
   reviewers work in separate copies. Planning, review and retrospective kept; daily dropped for a live board.
   Useful: every retrospective finding must end as a filed issue, an applied fix, or a stated reason not to act;
   ceremony under 5 minutes a sprint; a log of rulings and approvals. Reported weak: 79% of stories done in the sprint,
   119 of 159 retrospective actions still open, approval-to-merge as slow as building, one idle agent for 100 minutes.
   Does not fit: agents hold the owner roles; fixed clock sprints; several teams (untested).
2. https://www.scrum.org/resources/blog/ai-augmented-scrum-framework-when-half-your-team-autonomous-agents (Scrum.org)
   Human accountability cannot be handed to an agent; an agent cannot be the Product Owner. Story points do not suit
   agents: measure token cost and human checking time. A backlog item is not ready without the documents the agent needs.
   Useful: plan to the human's review capacity, not to the agents' speed; retrospect on token and usage logs.
   Does not fit: thin on Definition of Done; assumes human developers beside the agents.
3. https://dev.to/huzair_saputra/i-benchmarked-a-scrum-workflow-for-ai-coding-agents-heres-what-it-fixed-and-what-it-costs-4aja
   A Scrum workflow for coding agents: roles limited to their own files, one reviewer who wrote neither code nor tests.
   Six runs per arm: complete 6 of 6 with it, 3 of 6 without; about 1.5 times the cost and 1.4 times the time.
   Useful: the only cost figure found; separating who writes code, tests and review matches our team. Does not fit:
   tiny sample, one small repository; the gain was in finishing reports, not in quality.
4. https://tech-stack.com/blog/does-agentic-engineering-kill-scrum-what-actually-breaks/ (practitioner article)
   Five assumptions break: items are clear enough to build, review keeps pace, merged means done, pipelines are
   predictable, knowledge lives in heads. Agents cannot ask questions, so items need testable criteria.
   Useful: confirms our requirement-as-spec and the Product Owner as the bottleneck. Does not fit: enterprise pipelines.
5. https://dev.to/rawveg/your-coding-agent-thinks-it-has-finished-make-it-prove-it-2bg (practitioner post)
   Agents call work finished early. Write Definition of Ready and Done as checkable lists in the repository, enforce
   the non-negotiable ones mechanically, and have a read-only reviewer check the work against the spec.
   Useful: our Definition of Done is already a list of commands; add a Ready check. Does not fit: tool-specific hooks.
6. https://agilefederation.substack.com/p/teaching-ai-agents-process-discipline (practitioner post)
   Four small instruction files: one strictly ranked backlog broken down only as it rises, a board with limits on work
   in progress, a done checklist with a verification script, coordination through shared written logs, not meetings.
   Useful: small and cheap; one item in progress per team. Does not fit: Kanban flow is not Scrum; no evidence given.
7. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (Anthropic engineering, Nov 2025)
   A fresh session has no memory: keep a feature list where each entry has a pass flag only the builder may flip, a
   progress file and the version history. One feature per session. Agents marked work done after weak checks; real
   end-to-end testing fixed it. Useful: pass flags equal our requirement tests; the progress file equals WORKING.d.
   Does not fit: single-agent focus; no planning or review events.

## What each Scrum part would be for us (options, with cost in agent usage and time)

Cost scale: S under 5 minutes and little usage; M a short agent run; L a long agent run or an hour of the Owner's time.

- Sprint (container): (a) one story per sprint, ends when its tests pass: S; (b) a batch of stories for one feature,
  ended by the Owner: M; (c) a fixed time box: wastes usage when idle, source 1 reports idle gaps. Option (b) fits.
- Sprint Goal: (a) one sentence per sprint, written by the Orchestrator, agreed by the Owner: S; (b) the feature's
  requirement IDs serve as the goal, no sentence: nothing extra but no why; (c) none (today).
- Sprint Planning: (a) the Orchestrator proposes the story list and order in one message, the Owner agrees: S;
  (b) planning run by agents who estimate: L, and sources say estimates mislead; (c) Owner picks alone: S, slower for him.
- Daily Scrum: (a) dropped, a progress file per agent already shows state: nothing; (b) the Orchestrator reads progress
  files when a notification arrives and lists blockers: S; (c) a scheduled check: costs usage while nothing moves.
- Sprint Review: (a) the Orchestrator reports per story what passed, failed and what was not checked; the Owner reads
  it: S; (b) plus a run of the app for the Owner to look at: M; (c) a published page per sprint: M.
- Retrospective: (a) one short written list per sprint, each finding ends as an issue, a change made, or a reason not
  to act (source 1): S; (b) also mine usage figures and failed runs: M; (c) skipped: loses the only learning loop.
- Product Backlog: (a) the requirement status (`backlog`) as it is, ordered by the Owner in a short list: S;
  (b) a ranked file or GitHub Projects (already planned): M to set up; (c) the Owner's head: not visible to agents.
- Refinement: (a) the Orchestrator reviews the next stories for undefined terms and missing tests before planning: S;
  (b) a read-only agent checks each story is buildable (what the Coder review did): M; (c) none.
- Sprint Backlog: (a) a short list of the chosen stories in WORKING.d with one status each: S; (b) a file with
  requirement IDs, owner agent and status, committed: S to M; (c) the board only.
- Increment: (a) the merged, tested code of the chosen stories on the branch: nothing extra; (b) plus a build the Owner
  can run: M. Needs the Owner to say what he inspects.
- Definition of Done: (a) as now (analyze, tests, req_check) plus a Tester's per-requirement result: S; (b) plus an
  independent read-only check against the requirement (source 5): M per story; (c) plus end-to-end runs (source 7): L.
- Definition of Ready (not Scrum itself): (a) none; (b) a short checklist: terms defined, tests named, no open question:
  S, and it prevents the early-finish and cannot-ask problems in sources 4 and 5.

## Gaps in SCRUM.d against the Guide

- No Sprint Goal and no sprint length or end rule; "Sprint" is only the stories chosen. No one says when a sprint ends.
- No Planning, Review or Retrospective is written down; only pre-flight, post-flight and checking incoming work exist.
- No Daily or progress-reading step beyond progress bars; nothing says what to do about a stalled or idle agent.
- Product Backlog has no order and no owner of its order; the Dashboard is "not yet built".
- Sprint Backlog has no file or place; WORKING.d holds the Orchestrator's memory, not the sprint.
- Increment is not named; Definition of Done has no Tester result, no reviewer step and no rule for a story that
  misses it (spill over, split, or stop).
- No Ready check and no refinement step before a story enters a sprint.
- No place for the Retrospective's output, so findings can sit open (source 1's weakest point).
- Usage is watched (70% pause) but not recorded per story, so cost cannot be compared across sprints.
- Impediments: a defect found in a requirement goes to the Orchestrator, but there is no rule for a blocked story or
  an unanswered question that waits on the Product Owner.

## Ideas most useful, for the conversation

1. A short written Review and Retrospective per sprint, each finding ending as an issue, a fix or a reason (source 1).
2. A Ready check plus the existing Done commands, with a per-requirement Tester result (sources 3, 5, 7).
3. Plan to the Owner's checking time, not to agent speed (source 2); record usage per story.

## Decisions that are the Product Owner's

Sprint end rule (stories done, or the Owner says); whether a Sprint Goal sentence is wanted; where the sprint list and
the retrospective output live; whether a Ready check is added; how much of Review he wants to see in the app itself.
