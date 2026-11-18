# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **FED-08** (feeds) A stream name accepts letters such as OneWay, but refuses spaces and punctuation such as an exclamation mark; malformed input identifies the stream field. What is the complete allowed character set? 
  Answer:
- **FED-25** (feeds) Feed creation supplies a generated stream token and explains how an old feed link can be reused. The checked generated tokens contain at least twenty characters. Is twenty the guaranteed minimum rather than just the tested generator length? 
  Answer:
- **FED-27** (feeds) A stream name may contain one through 128 characters; 129 characters and embedded spaces are refused by the checked validator. Does the same limit apply to every save route? 
  Answer:
- **FED-30** (feeds) When creating the required Local calendar, it is included in the destination checked by the oracle. Should this inclusion apply to every existing destination or only the combined/default destination? 
  Answer:
- **GGL-13** (google) A client change is refused while the checked account is connected. How does this restriction relate to the later editable/reconnect setup flow? 
  Answer:
- **GGL-33** (google) Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? 
  Answer:
- **GGL-34** (google) If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? 
  Answer:
- **GGL-42** (google) A watch nearing expiry is replaced and the old watch stopped; a fresh watch is reused. Changing the public address replaces its target rather than accumulating watches. The checked renewal point is two hours before expiry; what exact renewal threshold is required? 
  Answer:
- **GGL-43** (google) Refused instant updates report the reason without preventing ordinary autosync; repeated refusal is warned once, and a later successful retry clears the error. The checked retry occurs after seven hours; what is the required retry interval? 
  Answer:
- **GGL-80** (google) Transient retries use bounded increasing delay with jitter and a maximum attempt budget; a longer server Retry-After is honored, including 120 seconds. Exact default delays and attempt limits need Developer confirmation beyond tested samples. 
  Answer:
- **HIS-02** (history) Activity reports Healthy when the checked source state is healthy and Unhealthy when that source is in error. How should mixed source states determine the overall Activity status? 
  Answer:
- **HIS-19** (history) History retains 100 changes by default, and saving a retention choice of 37 updates the effective retention and displayed value. The input offers bounds of 1 through 200; are these bounds enforced on every save path? 
  Answer:
- **SHL-12** (shell) The page provides Calendar, Sources, Feeds/Destinations, Rules, Event Templates and Activity/History sections, with the Beta section after Activity. Historical source labels differ; which final section vocabulary should be canonical? 
  Answer:
- **SHL-18** (shell) An opened section remains open when freshly observed; an open section older than twenty-five hours is closed and its closed state saved independently of another recently opened section. What is the exact expiry rule rather than this tested point? 
  Answer:
- **SRC-42** (sources) If a future event disappears from a subsequent source upload, its deletion is retained with its title. How long should this retained deletion remain available? 
  Answer:
- **SRC-56** (sources) Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Answer:







