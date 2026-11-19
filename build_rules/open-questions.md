# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **GGL-13** (google) A client change is refused while the checked account is connected. How does this restriction relate to the later editable/reconnect setup flow? 
  Answer:
- **GGL-33** (google) Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? 
  Answer:
- **GGL-34** (google) If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? 
  Answer:
- **GGL-42** (google) A watch is renewed shortly before it expires and the old one stopped; a fresh watch is reused, and a changed public address replaces the target rather than accumulating watches. The tested samples renew two hours before expiry on a weekly schedule; what renewal lead time is required? 
  Answer:
- **GGL-43** (google) Refused instant updates report the reason without preventing ordinary autosync; a refusal that repeats unchanged is recorded once (HIS-33), and a later successful retry clears the error. The checked retry occurs after seven hours; what is the required retry interval? 
  Answer:
- **HIS-02** (history) Activity reports Healthy when the checked source state is healthy and Unhealthy when that source is in error. How should mixed source states determine the overall Activity status? 
  Answer:
- **HIS-19** (history) History keeps the number of changes set in Settings, 100 by default (DEF-01); saving a different number updates the effective retention and the displayed value. The input offers the limits in DEF-01; are they enforced on every save? 
  Answer:
- **SHL-12** (shell) The page provides Calendar, Sources, Feeds/Destinations, Rules, Event Templates and Activity/History sections, with the Beta section after Activity. Historical source labels differ; which final section vocabulary should be canonical? 
  Answer:
- **SHL-18** (shell) An opened section remains open when freshly observed; an open section older than twenty-five hours is closed and its closed state saved independently of another recently opened section. What is the exact expiry rule rather than this tested point? 
  Answer:
- **SRC-42** (sources) If a future event disappears from a subsequent source upload, its deletion is retained with its title. How long should this retained deletion remain available? 
  Answer:
- **SRC-56** (sources) Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Answer:
- **CAL-69** (calendar) Each print sheet fits one physical Letter or A4 page without cutting event content. What overflow policy should apply when the selected events cannot fit at a readable size? 
  Answer:
- **CAL-74** (calendar) On a phone, the calendar initially uses List view before the user chooses a view. Should the initial choice follow available window space rather than device type under UI-14? 
  Answer:
- **DEP-26** (deployment) Startup retries establishing a database connection while the database is not ready. What retry budget and terminal failure behavior should be required? 
  Answer:
- **GGL-101** (google) Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? 
  Answer:
- **SHL-27** (shell) Should the saved section-open state be shared across browsers and restored after signing in again, or stay on each device like the other view settings (SET-06)? Expiry follows SHL-18. 
  Answer:
- **SRC-60** (sources) The user can add source calendars and outgoing feeds without an application-defined count limit. How does this promise relate to the one-CCS+ constraint SRC-17? 
  Answer:
- **SRC-63** (sources) A source download that unexpectedly returns an empty calendar preserves the previous schedule. How is an unexpected empty response distinguished from an intentionally emptied source? 
  Answer:
- **SRC-80** (sources) An upgrade creates its initial Local calendar once. Is it then added to every existing feed, or does each feed decide which calendars it carries (FED-30)? 
  Answer:
- **GGL-80** (google) Transient failures, including rate limits, are retried with a bounded, increasing, randomized delay and a maximum number of attempts; a longer server Retry-After is honored, including 120 seconds. What default delays and attempt limits should be required (they would go in DEF-01)? 
  Answer:
- **ACC-01.f** (account) A legacy page login is imported with a hashed password; saved page passwords are not stored in plaintext. Is this still needed after the port, given that DEP-14 does not carry the page password over? 
  Answer:
- **ACC-02.f** (account) After sign-in the user goes to the page they asked for when it is on this site. A destination on another site, including one written with a leading //, is never followed; the destination's query and fragment are kept. The Python app also rejects "hidden-tab redirect tricks": what exactly is that? 
  Answer:
- **ACC-04.c** (account) Is an empty password accepted, given that a password is never refused for its strength? 
  Answer:
- **ACC-05.d** (account) A secret is never shown on a page. The Google traffic view (GGL-02) shows tokens and the client secret to the signed-in Developer: should it hide them? 
  Answer:
