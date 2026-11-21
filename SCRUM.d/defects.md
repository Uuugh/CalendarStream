# Defects and questions waiting for the Product Owner

Only unanswered entries are listed (the marks are Or-02.e in `SCRUM.d/README.md`). Answer on the `Answer:` line under a question (or tell the orchestrator); the orchestrator applies the answer to the requirement rows and removes the question. Before asking, the orchestrator looks in the other requirements, the retired Python app and its reverse-engineering notes (`WORKING.d/CalendarStream.old/build_rules/reverse-engineering/`) and https://docs.flutter.dev/ and https://dart.dev/.

## 🟡 Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **CGOW-04.d** Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? 
  Answer:
- **CGOW-04.e** If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? 
  Answer:
  Code check: the old app makes a new calendar when a sync finds it missing (deleted in Google), drops the stored per-event state, writes everything again and notes it (reverse-engineering R5-20.f). Our CGOW-06.h and PGAP-02.c say a missing calendar pauses recovery: which wins?
- **CGOW-04.j** Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? 
  Answer:

- **CCCS-02.l** Existing CCS+ credentials can be imported from the old configuration, stored encrypted, and recorded as imported activity. Is this still needed after the port, given that the migration tool (DEP-05) copies the saved credentials? 
  Answer:
- **CON-06.l** Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Code check (Nov 19): only CCS+ retries (CCCS-03.b and CCCS-03.c give its plans); every other download makes one attempt per check. Suggestion: reword CON-06.l to say a failed download is tried again at the next check, and leave retry plans to CCCS-03.
  Answer:

## Found by a cold read of the requirements (test of the process)

- **Removing the Google API client:** CGOW-01.r keeps the Google connections in their sections needing their account restored. Does publishing stop, which status do they show, and is the user asked to confirm before removing the client?
  Answer:

- **One-way and two-way Google rows:** CGOW-04.k says one-way sync publishes and does not read back, yet CGOW-04.b, CGOW-04.c, CGOW-04.g and the instant updates (CGOW-05) describe reading Google's changes, which are two-way behaviors. Code check: the old app agrees (one-way only writes and puts back what changed in Google; two-way reads Google first during a full check: reverse-engineering R5-28). Recommended: move those rows to `google_two_way.md`. Is that right?
  Answer:


## 🔴 Q-P: lines of the process files that may break a Law (from the Retrospective of the ocean sprint)

Each is a line that may break a Law. Answer on the Answer line; the orchestrator applies the answer and removes the question.

- **`AGENTS.md` has no `**Method:**` on its rules** (Law 3), and its Environment and "Your role" have no `**Test:**`. Should each standing rule state a Method, and which tests should the other two get?
  Answer:
- **`tests/README.md` rules without a Test line:** the old-app fixtures rule, Results and Layout. Should each get a Test line, or be removed as old-app wording?
  Answer:
- **Prefix list in `requirements/README.md`:** it shows `UIC` while the text says `UI`, and `DEF` is missing. Which is right?
  Answer:
- **"moved with the old app" references** in `requirements/README.md` point at files that no longer exist. Delete the references, or give a path?
  Answer:
- **The freeze statement in `requirements/README.md`** repeats the one in `AGENTS.md`. Remove it from the requirements README?
  Answer:
