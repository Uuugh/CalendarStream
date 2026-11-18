# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-S: later steps


## Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **CAL-35** (calendar) The sampled week header omits the redundant “times in” and event-count wording. Is this omission intended for every view? 
  Answer:
- **CAL-37** (calendar) The key omits separate Timed, All-day and Added here color labels in the sampled views. Should this apply to every key variant? 
  Answer:
- **CAL-57** (calendar) The calendar stretch amount is saved for the sampled negative values -300 and -120; -301 is refused, and a request for 1500 is limited to at most 1200. Are the complete accepted range and clamping rules intended to be specified beyond these samples? 
  Answer:
- **CAL-59** (calendar) An hour height of 64 is saved; heights 10 and 500 are refused. What is the complete accepted hour-height range? 
  Answer:
- **CAL-62** (calendar) For Letter and A4, the sampled month print produces one landscape PDF page and the sampled day print starts with a portrait PDF page; the sampled Letter week print has at least two pages. Are these pagination expectations specific to the fixture content? 
  Answer:
- **CAL-63** (calendar) The sampled portrait month print produces one portrait PDF page. Is single-page output required only for this fixture size? 
  Answer:
- **DEP-10** (deployment) The updater never updates the database, never checks for updates on its own, and removes old images. Conflicts with auto-update (SET-32): which wins? 
  Answer:
- **DEP-12** (deployment) The database is backed up with pg_dump; keeping the deployment secrets is required to read the encrypted credentials after a restore. Is a restore procedure part of the product? 
  Answer:
- **EVT-34** (events) Applying empty edits or hidden inputs leaves the event list unchanged. 
  Answer:
- **FED-08** (feeds) A stream name accepts letters such as OneWay, but refuses spaces and punctuation such as an exclamation mark; malformed input identifies the stream field. What is the complete allowed character set? 
  Answer:
- **FED-16** (feeds) Saving a source does not replace an unrelated unsaved feed-name edit. Is preserving unrelated pending edits a shared saving rule for all features? 
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
- **GGL-73** (google) Published descriptions place a meeting URL before the original notes; reading fields back avoids duplicating the meeting URL in notes. The reverse-read predicate is permissive: which exact note representation is required? 
  Answer:
- **GGL-77** (google) An account email is accepted only when the checked identity-token audience matches the configured client. This evidence does not establish full identity-token validation. 
  Answer:
- **GGL-80** (google) Transient retries use bounded increasing delay with jitter and a maximum attempt budget; a longer server Retry-After is honored, including 120 seconds. Exact default delays and attempt limits need Developer confirmation beyond tested samples. 
  Answer:
- **GGL-83** (google) Saved health error text is limited to 300 characters. Is this truncation a user-facing diagnostic limit or only a storage policy? 
  Answer:
- **HIS-02** (history) Activity reports Healthy when the checked source state is healthy and Unhealthy when that source is in error. How should mixed source states determine the overall Activity status? 
  Answer:
- **HIS-08** (history) History identifies the change type, including Rule, Event, Calendar or Sync in the checked cases. Is this a closed list or may other types be displayed? 
  Answer:
- **HIS-19** (history) History retains 100 changes by default, and saving a retention choice of 37 updates the effective retention and displayed value. The input offers bounds of 1 through 200; are these bounds enforced on every save path? 
  Answer:
- **HIS-20** (history) Completing an undoable change records the before and after states for restoration. The oracle directly captures a change from one to two; what state categories must be included in every snapshot? 
  Answer:
- **SET-14** (settings) When opened through a host different from the configured public host, the page warns and identifies both hosts; it omits that warning for the configured host or the checked LAN-IP access. Is LAN-IP suppression intended for all private network addresses? 
  Answer:
- **SET-19** (settings) Versions compare numeric beta sequence numbers in order and place a release after its beta. Unknown installed versions or the checked unrecognized version forms do not produce a newer-version result. Which complete version grammar should be supported? 
  Answer:
- **SET-22** (settings) Never disables automatic checks. Hourly checks become due between the checked 30- and 61-minute points, and monthly checks between 29 and 31 days. What exact schedule and meaning of monthly should be promised? 
  Answer:
- **SET-25** (settings) A manual update check does not clear the stored version already marked as logged. Is this marker intended to suppress repeated update notices? 
  Answer:
- **SET-36** (settings) A pending update exposes its target version, but an update marker older than sixteen minutes or belonging to a different starting version is no longer effective. What is the exact expiry boundary? 
  Answer:
- **SET-37** (settings) While an observed update loses contact with the app, progress changes from Downloading to Restarting; once contact returns, the page reloads after a settling delay. What delay should be required beyond the checked timing samples? 
  Answer:
- **SET-40** (settings) Animation intensity and duration preferences are saved; the checked settings 150 and 50 yield factors 1.5 and 0.5. Intensity 500 is refused. What complete ranges and units should users be promised? 
  Answer:
- **SHL-12** (shell) The page provides Calendar, Sources, Feeds/Destinations, Rules, Event Templates and Activity/History sections, with the Beta section after Activity. Historical source labels differ; which final section vocabulary should be canonical? 
  Answer:
- **SHL-18** (shell) An opened section remains open when freshly observed; an open section older than twenty-five hours is closed and its closed state saved independently of another recently opened section. What is the exact expiry rule rather than this tested point? 
  Answer:
- **SRC-42** (sources) If a future event disappears from a subsequent source upload, its deletion is retained with its title. How long should this retained deletion remain available? 
  Answer:
- **SRC-56** (sources) Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Answer:


## Q-M: the migration

- **Q-M1** Your page password is stored as a scrypt hash. The migration can (a) carry the hash over, so you sign in with the
  same password (Dart then needs a scrypt check), or (b) leave the password out, so you set a new one at the first start
  (simpler, and this is a single-user app). Claude recommends (b).
  Answer:
- **Q-M2** The migration tool is Python and deleted with the Python app (step 5). Should the Developer run it once on the real
  database, with Claude present, or should Claude also test it against a made-up demo database first? Claude recommends the
  demo database first, then your copy, then the real database.
  Answer:

## Q-T: time storage (Developer, Nov 17: all times are stored in UTC; an event's time zone is for entry and display)

- **Q-T2** Rules match on day of week and time of day (RUL-07, RUL-08: Fri-Mon, overnight 22:00-06:00). In which zone should a
  rule judge an event: the event's own zone, or the page's display zone? (Python uses the display zone.) Claude recommends
  the event's own zone, since "Friday 22:00" means the place the event happens.
  Answer:
- **Q-T5** An all-day event is shown on its own local date, whatever the page's display zone is (a New York all-day event stays
  on its New York day when you view the calendar from Los Angeles). Timed events still follow the display zone (CAL-25). Right?
  Answer:
- **Q-T6** "System time zone" (CAL-19, EVT-05): the zone of the device running the app (your phone or computer, which the Flutter
  client knows), or the server's `TZ` setting (README: default America/Chicago)? Claude recommends the device's zone, with the
  server's TZ only as the default for scheduled work (downloads, sync) that has no device.
  Answer:
- **Q-T7** CAL-19 says existing events are viewed with the new offset. For an all-day event that would move it to another day
  when the Local zone is far from its own zone (Q-T5). Do all-day events follow the Local zone like timed ones, or stay on their
  own date?
  Answer:
