---
name: scrum
description: Use when designing, reviewing or changing how Scrum is applied to CalendarStream (the roles, events, artifacts and commitments in SCRUM.d/), or when asked what Scrum says about something. General Scrum knowledge only; this project's own rules live in SCRUM.d/README.md.
---

# Scrum, as the Scrum Guide (2020) defines it

Source: https://scrumguides.org/scrum-guide.html (verify wording there; this is a summary). This skill holds general
Scrum knowledge. It holds no CalendarStream rule: those are in `SCRUM.d/README.md` and `AGENTS.md`.

## Theory
Scrum is a lightweight framework for solving complex problems adaptively. It rests on empiricism (knowledge comes from
experience; decide from what is observed) with three pillars: **transparency** (the work and its state are visible),
**inspection** (check progress and artifacts often enough to catch problems) and **adaptation** (adjust as soon as a
deviation is found). Values: commitment, focus, openness, respect, courage.

## One team, three accountabilities
- **Product Owner**: maximizes the value of the product. Accountable for the **Product Backlog**: developing and
  communicating the Product Goal, creating and communicating items, ordering them, making it transparent. One person,
  not a committee; the organization respects their decisions.
- **Scrum Master**: accountable for Scrum's effectiveness: coaches the team, helps the Product Owner with backlog
  management, removes impediments, ensures events happen and stay productive. A servant-leader, not a project manager.
- **Developers**: the people who create any aspect of a usable **Increment** each Sprint: plan the Sprint Backlog,
  instill quality by adhering to the Definition of Done, adapt daily toward the Sprint Goal, hold each other accountable.
- The Scrum Team is small (typically 10 or fewer), cross-functional and self-managing: it decides who does what, when and how.

## Events (all inside the Sprint)
- **The Sprint**: a fixed length of one month or less; a container for all other events. No changes are made that
  endanger the Sprint Goal; quality does not decrease; the Product Backlog is refined as needed; scope may be clarified
  and renegotiated with the Product Owner as more is learned. Only the Product Owner can cancel it.
- **Sprint Planning**: why is this Sprint valuable (the **Sprint Goal**), what can be done (items pulled from the
  Product Backlog), how will the chosen work get done (a plan).
- **Daily Scrum**: 15 minutes for Developers to inspect progress toward the Sprint Goal and adapt the Sprint Backlog.
- **Sprint Review**: the team presents results to stakeholders, progress toward the Product Goal is discussed, and the
  Product Backlog is adapted. A working session, not a presentation.
- **Sprint Retrospective**: the team plans ways to increase quality and effectiveness: inspects how the Sprint went
  (people, interactions, processes, tools, Definition of Done) and what to change.

## Artifacts and their commitments
- **Product Backlog** (commitment: the **Product Goal**): the ordered list of what is needed to improve the product.
  Refinement is the ongoing activity of breaking items down and defining them; it is an activity, not an event.
- **Sprint Backlog** (commitment: the **Sprint Goal**): the Sprint Goal, the items selected for the Sprint, and the
  actionable plan to deliver the Increment. Owned by the Developers; updated through the Sprint.
- **Increment** (commitment: the **Definition of Done**): a concrete step toward the Product Goal; usable, and every
  Increment meets the Definition of Done, a formal description of the state when it meets the quality measures. Work is
  not part of an Increment unless it meets the Definition of Done.

## Common practices that are not Scrum itself
User stories with acceptance criteria, story points and velocity, burndown charts, a Kanban board, work-in-progress
limits, a team Definition of Ready. These are optional additions; the Guide does not require them.

## Adapting Scrum to a team of agents (considerations, not rules)
- Events exist to create transparency, inspection and adaptation. Where an event costs more than it returns, keep its
  purpose and shrink its form (a short written record in place of a meeting).
- Usage cost and elapsed time are real constraints: the cheapest practice that still gives inspection and adaptation wins.
- A person who is the Product Owner is still one accountable person; the remaining roles may be played by agents.
- Each artifact must stay visible to every agent that needs it, and exist once.
