# Dashboard rules

Read before any change to the Dashboard (the "CalendarStream Dashboard" artifact), including a cleanup. The short
form is in 0-overview.md; this is the detail, kept here so it survives conversations.

## Before changing Inputs Status

1. **Read the verdicts first**: the `tests` collection (ArtifactData `list`), every time, even for a small edit. The
   Developer clicks Good | Bad on the live page while Claude works, so what was read earlier is out of date.
2. **Good** → the item comes off. **Bad** → it stays (reopened) with the remark added as an amber note. A remark
   that asks for something new is a new F or I. A remark that says "move to roadmap" → a bullet in roadmap.md
   (0.3 Theming for look and feel), and the item comes off.
3. **Never remove an item without its verdict read.** An age, a beta number or a long list is not a reason: only a
   Good or a move to the roadmap removes an item.
4. **IDs**: never reuse an ID that has a verdict in `tests` (delete the stale verdict if an ID must be reused). A
   merged item says which items it absorbed, and each absorbed one comes off.

## Order and form

- After every edit, re-sort Inputs Status: grouped first by **Section** (All, Settings, Calendar, Sources, Feeds,
  Rules, Events, Misc — "All" for anything that reads as cross-cutting page chrome, not one feature area; "Misc"
  for branding/favicon and for R items, since build/process rules aren't a page feature), then within each section
  **I, then F, then R, each in number order**, and check it (list the IDs). New items go to their section's sorted
  place, never to the top. Each section is preceded by a divider: an `<hr>`-style rule with the section's name
  overlapping it, fieldset-legend style (`.sectionrule`/`.sectionrule span` in the Dashboard's own CSS). A section
  with no items is skipped, not shown empty.
- Each item: its headline, a tag (recorded · built · beta.N · reopened · open), the Developer's words ("As given"),
  then Claude's notes. A request from Claude to the Developer is an amber note.
- New inputs are only recorded (no plan, no build) until PLAN or BUILD.
- A file, class or function named in an item's notes is colored by the checkpoint that touched it: green for new,
  blue for touched (0-overview.md). Use the Dashboard's own CSS classes for this, not inline color, so both themes
  stay correct.

## Cost graph

- Plotted values are real readings on the 0–100% scale. A value over 100 (a build that crossed a session reset)
  is drawn as a triangle on the 100% line with the real number in its tooltip. Never plot an extrapolation as a dot.
- The slider is neutral gray, never the blue of the data.

## Editing it

- Edit a local copy with a script that checks each replacement matches exactly once; sort and count `<li>` before
  publishing; publish with the same artifact URL; never create a copy.
- Replies about the Dashboard are bullets, short, with links; things needing the Developer's attention first.
