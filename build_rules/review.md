# Review checklists

For the Reviewers of Deploy steps a and b. A Reviewer gets the repo and the diff since the last
stable release (`git diff v<STABLE>..HEAD`), not the author's notes or conversation. Report each
finding with its file and line, what goes wrong, and how much it matters; number them #1, #2…

## a. Programming Review

- Design: Is the code well-designed and appropriate for CalendarStream, a self-hosted Docker web app that may later become a standalone app? The app runs in a Linux container; the installer and Docker setup must work on Linux, macOS (Docker Desktop) and Windows (WSL). New code shouldn't add needless ties to Docker, Postgres or the web page: keep the calendar logic separate from where it runs and how it's shown.
- Functionality: Does the code behave as the author likely intended? Is the way the code behaves good for its users?
- Complexity: Could the code be made simpler? Would another programmer be able to easily understand and use this code when they come across it in the future?
- Tests: Does the code have correct and well-designed automated tests? (`tests/`: one suite per version; `tests/run.sh` runs them.) Does the new behavior have a suite that checks it?
- Naming: Did the author choose clear names for variables, classes, methods, etc.?
- Comments: Are the comments clear and useful?
- Style: Does the code follow our style guides? PEP 8 and PEP 257 (Python), Google HTML/CSS and JavaScript style guides; ruff runs automatically.
- Documentation: Did the author also update relevant documentation (README.md, CHANGELOG.md, build_rules/)?

## b. Security Review

- OWASP ASVS and Top 10, applied to what the diff touches. In particular:
  - every route that changes something needs the login and the form token (`gui_auth`, `check_csrf`);
  - downloads of calendar links (`app/calsync.py`): https only, redirects, size and time limits, no credentials sent to other hosts;
  - secrets (passwords, the Google client secret and tokens) stay encrypted at rest and out of logs, reports and pages;
  - anything a user types that ends up in a page is escaped.
- Automated scans, with their results in the report: `pip-audit -r requirements.txt`, `bandit -r app`, `trivy image ghcr.io/uuugh/calendarstream:beta`.
- A scanner's finding that doesn't apply is explained, not just dismissed.
