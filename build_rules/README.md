# build_rules: working notes (read this first)

Almost everything here is **legacy** from the Python era and must not be followed. Only the files in the first table are live. Everything about how requirements are written is in `requirements/README.md`.

## Live

| File | What it is |
|---|---|
| `orchestration.md` | The roles, the steps still to do with their state, and how incoming work is checked. |
| `HANDOFF.md` | One page for a new conversation: the orchestrator's role and where things stand. |
| `open-questions.md` | The questions waiting for the Product Owner. Check it for answers before every edit. |
| `coder-review-1.md` | The first full Coder review (baseline of rows that could not be implemented) and how it was triaged. |
| `review-findings-1.md` | The process tests and the Reviewer's findings, sorted by what each needs. |
| `reverse-engineering/` | Requirements reverse-engineered from the Python app by six agents that never saw ours (`reverse/`), and their comparison with ours (`compare/`): the gaps, the differences, and the rows only we have. Working data for filling the gaps; delete when done. |
| `layer-map.md` | The record of decisions for the port (target layout, testing, time zones). Its status lines and "resume here" are out of date; trust `requirements/` where they differ. |

## Legacy (do not follow; the Product Owner retires these in step 5 of `orchestration.md`)

`0-overview.md`, `1-plan.md`, `2-build.md`, `3-test.md`, `4-review.md`, `5-deploy.md` (the DASH, PLAN, BUILD, TEST, REVIEW and DEPLOY commands), `dashboard.md`, `roadmap.md`, `low-findings.md`, `build-costs.md`, `dependencies.md`, `ui_ux.md`, `theme.md` and `theme-map.md` (converted into `requirements/theme.md` and `common.md`), `gpt-tasks.md` (the ChatGPT task queue, finished), `requirements-scan-1.md`, `oracle-coverage-notes.md`.
