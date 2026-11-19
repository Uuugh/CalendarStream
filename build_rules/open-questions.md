# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **GGL-33** (google) Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? 
  Answer:
- **GGL-34** (google) If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? 
  Answer:
- **HIS-02** (history) Activity reports Healthy when the checked source state is healthy and Unhealthy when that source is in error. How should mixed source states determine the overall Activity status? 
  Answer:
- **SRC-56** (sources) Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Answer:
- **PRT-01.d** (print) Each print sheet fits one Letter or A4 page without cutting content. What should happen when the content cannot fit at a readable size? 
  Answer:
- **GGL-101** (google) Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? 
  Answer:
- **SRC-63** (sources) A source download that unexpectedly returns an empty calendar preserves the previous schedule. How is an unexpected empty response distinguished from an intentionally emptied source? 
  Answer:
- **ACC-01.f** (account) A legacy page login is imported with a hashed password; saved page passwords are not stored in plaintext. Is this still needed after the port, given that DEP-14 does not carry the page password over? 
  Answer:

## Other questions for the Product Owner (not tied to one requirement row)

- **Theme order:** Convert sections 5 to 8 of the legacy theme file next (buttons, the Cancel | Save pair, the Status/Action buttons, transitions)? Recommended: yes.
  Answer:
- **Manual Google sync:** The deleted Beta section also let the user start the Google sync by hand. Is the normal Sync Now enough? Recommended: yes.
  Answer:
- **Special character:** A password's special character is any character that is not a letter or a digit (a space counts). Right? Recommended: yes.
  Answer:
- **Date range:** The shared date range (UI-23) says All clears both dates and greys them, and typing is done after unticking it. Is that behavior of the control, as written? Recommended: yes.
  Answer:
- **Right zone:** The "+" new-event button is not in the calendar header's right-zone order (Time Zone, View, 12/24 clock, Print, Full page). Where does it go? Recommended: the left of the order, first.
  Answer:
- **Print users:** Is Print used by any feature besides the Calendar and Events?
  Answer:
