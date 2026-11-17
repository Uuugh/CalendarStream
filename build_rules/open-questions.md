# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-S: later steps






## Q-D: deployment

- **Q-D1** GPT's README scan (requirements/drafts/readme_gaps.md) found about 25 README promises about installing and running the
  app (supported hosts, installer prompts, second install, generated database credentials, environment settings such as TZ
  and trusted proxies, updater, backups) that belong to no feature. Add a `deployment` feature (requirements only for now; in
  the port it is the Docker/installer/updater side), or leave them in `documentation` as what the README must say?
  Claude recommends a `deployment` feature.
  Answer:
