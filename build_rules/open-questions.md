# Open questions for the Developer

Only unanswered questions are listed; Claude removes a question once it acts on the answer (the decision is recorded in layer-map.md or the requirements files). To answer, type your answer after the question's `Answer:` line in this file (or just tell Claude). Claude checks this file on every 15-minute pass and whenever you message. Started Nov 17.

## Q-X: questions from the drafts (rows marked (?))

Each question is the (?) text of a proposed requirement. Answer on the Answer line; Claude updates the row and removes the question.

- **GOW-04.d** Advancing the synchronization window leaves past remote events alone while dropping obsolete tracking; extending it backward can republish eligible events. The backward-extension check is permissive: what exact write behavior should be guaranteed? 
  Answer:
- **GOW-04.e** If the remote calendar is deleted, synchronization recreates it with a new mapping and publishes eligible events. How does this automatic repair interact with the later missing-calendar paused recovery policy? 
  Answer:
- **GOW-04.j** Eligible local changes and valid remote change notices trigger reconciliation within seconds under normal service availability. What measurable latency target should replace “within seconds”? 
  Answer:
- **HIS-01.j** Activity reports Healthy when its source is healthy and Unhealthy when its source is in error. How should mixed source states determine the overall Activity status? 
  Answer:
- **SET-03.e** A custom logo can be uploaded and shown; without one the default logo is used. Which image types and sizes are allowed (the old app accepted PNG, SVG, WebP, JPEG and ICO up to 256 KB), and an image that can carry script is not accepted? 
  Answer:
- **CCS-02.l** Existing CCS+ credentials can be imported from the old configuration, stored encrypted, and recorded as imported activity. Is this still needed after the port, given that the migration tool (DEP-05) copies the saved credentials? 
  Answer:
- **CON-06.l** Automatic downloading retries a transient nonreply and can succeed on a later attempt; a persistent nonreply eventually fails. What retry budget and timing should be promised beyond the observed attempts? 
  Code check (Nov 19): only CCS+ retries (CCS-03.b and CCS-03.c give its plans); every other download makes one attempt per check. Suggestion: reword CON-06.l to say a failed download is tried again at the next check, and leave retry plans to CCS-03.
  Answer:
- **CON-06.n** A source download that unexpectedly returns an empty calendar preserves the previous schedule. How is an unexpected empty response distinguished from an intentionally emptied source? 
  Answer:

## Process question for the Product Owner

- **Tests workflow:** Every push to main, including one that only changes `requirements/`, runs the whole heavy Tests workflow, while the quick Requirements workflow already checks those files. Should the heavy workflow skip pushes and pull requests that only touch `requirements/`, `build_rules/`, `docs/` or Markdown files? Recommended: yes, to keep usage low. I did not change it because it alters the checks that guard the app.
  Answer:

## Connections and sections (Nov 19)

- **No limit on connections:** CON-01.d says the number of connections is not limited, but DEF-02 says every list that grows has a stated limit. Which wins: a limit in DEF-01, or an exception?
  Answer:

- **CCS-03.g** The CCS+ site address can be overridden with a custom HTTPS address (a setting of the old app). Does the custom address still belong in the port?
  Answer:

## Found by a cold read of the requirements (test of the process)

- **Kind text per connection:** CON-02.d used to list five kind texts (CalendarStream, United Airlines CCS+, Google Calendar, Apple Calendar, Calendar Feed) in the common file, which every new connection would have to edit. Each connection now states its own kind text, but none does yet. Recommended: Local calendar = CalendarStream; CCS+ = United Airlines CCS+; calendar link = Google Calendar, Apple Calendar or Calendar Feed by its preset (LNK-01.c); Google one-way and two-way = Google Calendar. Is that right?
  Answer:
- **Removing the Google API client:** GOW-01.r keeps the Google connections in their sections needing their account restored. Does publishing stop, which status do they show, and is the user asked to confirm before removing the client?
  Answer:
- **Feeds in the shared status line:** CON-03 says a module shows "Last synced" and "Next check @", but a feed is read by others (FED-05 "last read") and has no download schedule. What does a feed's status line show?
  Answer:

- **One-way and two-way Google rows:** GOW-04.k says one-way sync publishes and does not read back, yet GOW-04.b, GOW-04.c, GOW-04.g and the instant updates (GOW-05) describe reading Google's changes, which are two-way behaviors. Recommended: move those rows to `google_two_way.md`, so one-way holds only publishing and health. Is that right?
  Answer:
