# Method: constructing definitions and rules (draft; trial first, then the Product Owner places it)

Source of every line below: the Product Owner's corrections in the session of 2026-11-20. Read `SCRUM.d/README.md` ("How to read the rules") for the row format.

1. **Keep every word.** Each rule came from a lesson. Move, split and fill columns; never cut or compress. A statement you cannot place goes to "Not yet placed" at the bottom with the reason. Only the Product Owner deletes.
2. **Sort each sentence.** A definition says what a thing is or is for (a role, an artifact, an event). A rule says what an agent must do or never do, with a trigger. A sentence that is both is split into a definition and a rule.
3. **Define once, use everywhere.** A term (Team, Sprint, Ready) is defined once in Definitions; rules only use it. Use only terms and codes the Product Owner gave; flag any other and ask. A role is a definition marked `*ROLE*`.
4. **Questions first.** For each role list the questions a cold agent asks, in the order it meets them: who am I, what must I never do, who do I wait for, when do I act, what do I do, how, who checks me. Write a rule only to answer one question. A rule that answers none is words for the sake of words: move it to "Not yet placed".
5. **A rule binds the agent that acts.** The ID prefix is that agent. A fact about the Product Owner (a human) is a definition of authority; its effect is a limit on an agent ("never launches a sprint").
6. **Flows are parents.** A flow (a sprint, pre-flight, a review) is one parent rule ("runs a sprint") whose sub-rules are the steps in order. The parent answers "what do I do for X?" and the sub-rules inherit with `^`.
7. **Closed loop.** A row has what, how, when acted, who tests, when tested, how tested. A blank is missing, `^` is the parent's value, `—` is none, stated. A trigger is an event (defined once) or a condition an agent can observe. A test is a script or a review step that names what the reviewer looks for.
8. **Actionable by a cold agent.** The row lets an agent decide yes or no without judgment. Replace a judgment ("short work", "saves usage") with a closed list or an observable condition.
9. **Say it once.** Before writing a row, search the other READMEs for the same rule; the README of the area it governs owns it, and the others link.
   Where a sentence carries a "Test:" tail, the tail goes to **How tested** and the rest to **What**; the file's word "Method:" is the **How** column. A constraint that holds always (no real data) has **When acted** `^` (always). A group of sub-rules that are not a flow is unordered; only a flow's sub-rules are in order.
10. **A sentence with no actor** (a format, a layout, what a result is) is a definition. A sentence that names no actor and cannot be a definition goes to "Not yet placed" and is asked about; do not guess the actor.
11. **Verify with a cold trial.** Give a fresh agent only `AGENTS.md` and the file plus the role's questions. Each question it cannot answer from a row, each ambiguity and each conflict is a finding. Fix the file, never explain the answer to the agent.
12. **One decision at a time.** Give options A, B, C, what each changes, and a recommendation; expand a question when asked. Never ask what the Product Owner already decided: search the conversation, `WORKING.d/` and the branches first, and record each decision in the file of the rule it changes.
13. **Fix or propose.** Fix a line (keeping every word) in a file built under the Product Owner's instruction; propose to the Product Owner (Or-02.e.c) when the change removes words or alters a rule not written in this build.
14. **Mark lines** (Or-02.e): 🟡 a question, 🟠 an agent cannot act on it (the Orchestrator rewrites it), 🔴 it breaks a Law or contradicts another line (the Product Owner decides); in the first cell, removed when answered.
15. **Check the file before editing.** A file can change on disk (an open editor can save an older copy over it); re-read before a run of edits and verify after.
16. **A role's report is its evidence.** Accept a Tester's report that names the command and one result per requirement; rerun only when it lacks either (Or-03).
17. **Test in two steps.** A cold paper trial per role group first, then one small real sprint; the real sprint finds what paper trials miss (usage steps, the gate, commits, who checks what).
