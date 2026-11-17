# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-S: later steps





## Q-P: the port

- **Q-P1** Dart's regex engine has no time limit, so RUL-22 (a pathological regex such as `(a|aa)+$` is stopped within a
  second, "Too slow") cannot be met inside the pure domain package. Options: (1) run each user regex in a short-lived
  isolate with a timeout in the Dart server (accurate, more code); (2) refuse regexes with nested repeats when saving
  (simple, but refuses some valid patterns); (3) accept the risk for a self-hosted single-user app. Claude recommends 1.
  Answer:
- **Q-P2** Regex error wording will differ from Python's ("Not a valid regex: missing )"), because the engines differ.
  Accept Dart's wording, or keep the Python wording for the common cases?
  Answer:
