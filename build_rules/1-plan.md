# 1. Plan

Command: **PLAN**. Read when the Developer says PLAN, and before every BUILD.

## Inputs

- The Developer gives F, I, R and ? at any time, in any wording.
- Claude keeps the waiting list:
  - each input tidied: spelling, grammar, numbering;
  - dictation slips corrected ("Texas" → "text is", "safe" → "Save", "subscription" → "subsection"), telling
    the Developer which reading it took;
  - a **?** answered with Claude's suggestion; it joins the list only when the Developer agrees.

## PLAN shows

1. Every waiting F, I and R, numbered.
2. For each, what Claude would do, in a line or two.
3. For an R that changes these rules: the actual new wording. BUILD is then the Developer's yes to exactly that.
4. Anything to decide first, as a question with Claude's suggested answer.

The same list is shown before every BUILD, including what that BUILD leaves waiting, so the Developer's messages keep
the record if a session ends.

## Big or unclear inputs

Planning is cheaper than rebuilding: when an input is big, unclear or could be built several ways, PLAN asks
first (one short question, with a suggested answer) rather than guessing in the build.
