# Suite 41: Module edges and handles at desktop/phone widths

Source: [`tests/suite_41.py`](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_41.py) at `d70343f7476177a25f32827262d991cdc95c045f`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Postgres; app server 8097; seed.demo and fake work.ics download; background loops patched. Chromium loops over 1230×900 and 390×900. In each width, two module/section pairs are measured: CCS+ in Sources and the first matching destination module. No explicit palette loop.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S41-01 | sources / feeds | At both widths and in each sampled section, the module's right edge is within one pixel of its section plus control's right edge. | [L38](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_41.py#L38) |
| S41-02 | sources / feeds | Each sampled handle's right edge is at or before the module right edge and its left edge is at or after the section left edge. | [L39](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_41.py#L39) |
| S41-03 | shell | At each sampled width, document scroll width does not exceed the viewport width. | [L40](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_41.py#L40) |
| S41-04 | shell | No pageerror events are collected at either sampled width. | [L41](https://github.com/Uuugh/CalendarStream/blob/d70343f7476177a25f32827262d991cdc95c045f/tests/suite_41.py#L41) |

## Direct assertions

No direct `assert` statements; the observations above cover all `ok()` call sites.

## Coverage limits and reconciliation notes

- Rows 01/02 are each repeated for two sections at two widths, so four call sites produce twelve runtime checks when all paths execute.
- The old docstring says right margin, while the later row label says left margin. The predicate only bounds handle edges inside the sampled horizontal section/module limits; it does not compare the handle to the module's left edge to prove a distinct margin.
- Only CCS+ and the first matching destination are measured, not every module. No dark-mode, drag interaction, height or overlap assertion is made.
- Overlaps: suite 34 handle presence; suite 31 responsive section layout; suite 35 phone overflow.
