# requirements/drafts: NOT requirements

Everything in this folder is **input**, not a requirement. The requirements are in `requirements/<feature>.md` and `requirements/common.md`.

- `readme_gaps.md`, `changelog_gaps_*.md`: ChatGPT's scans of README.md and CHANGELOG.md for behavior no requirement covers.
- `gaps_<feature>.md`: ChatGPT's triage of those gaps into proposed requirements, one file per feature (Task E in `build_rules/gpt-tasks.md`).

Claude folds the proposals into `requirements/<feature>.md` as `proposed` rows (renumbering where an ID is already taken, merging duplicates, applying the rules
in `build_rules/HANDOFF.md`), and then this folder is deleted (the history stays in git). Never edit a requirement here.
