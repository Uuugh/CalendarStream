# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-S: later steps





## Q-P: the port

- **Q-P3** Dart's RegExp is ECMAScript, Python's `regex` module is not: Python-only syntax such as inline flags `(?i)`,
  named groups `(?P<name>...)`, `\A` / `\Z` and possessive or atomic groups does not compile in Dart. Do any of your saved
  rules use a typed regex with that kind of syntax? (If not, nothing to do; if so, tell Claude which, and the port will
  convert them when it migrates the rules.)
  Answer:
