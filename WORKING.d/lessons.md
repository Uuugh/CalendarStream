# Lessons (temporary; turn into agent-actionable rules, then delete)

Collected Nov 20 while rewriting `requirements/README.md`. Each ends as a rule with an owner and a test, or a stated reason.

1. Every rule has a Test and every Test has an owner. The README rules had no Method line and no owner for the tests. Proposed: one default Method and test owner under the rules heading (Author; Orchestrator runs `req_check.sh`, Reviewer runs `review:` tests).
2. No test ever read the READMEs. A `review:` test has no schedule; the cold test (SCRUM.d step 10) reads only AGENTS.md. Proposed: after any README change the Orchestrator launches a cold agent with only that README and realistic tasks (the `doc-coauthoring` Stage 3), and checks its answers against the rules.
3. A new agent rewrote a whole README at once and lost detail. Work one line at a time with the Product Owner; split before you cut; record every cut.
4. A new agent asked many questions at once. One decision at a time, with a recommendation.
5. A skill's own workflow (long question rounds) overrode "one decision at a time". Say the project rules win over a skill.
6. A rule or definition that cannot be tested is not a rule. A definition stays only if a rule needs it to be unambiguous.
7. Renumbering rules breaks citations. Record who cites a number first (`rule-key.md`), update after.
8. Long run-on text in rule files breaks agents. One statement per line, one rule per block, definitions apart from rules.
9. The harness blocks discarding uncommitted work; the Product Owner may be editing a file. Check `git status` and ask before overwriting.
11. An agent turned a word into a role: "Author" (`SCRUM.d/README.md:9`, commit 85d4cad) is not a role the Product Owner defined. Roles are the closed list in `SCRUM.d/README.md` Roles, and an agent never adds one. Remove "Author" there. Proposed test: a script lists any role name used in a rule file that is not in that list.
