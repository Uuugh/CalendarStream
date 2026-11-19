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

- **Update channel (beta is gone):** With no beta release, is there still more than one update channel? SET-05.e (changing the update channel clears the previous check result), DEP-02.h (the installer accepts stable and latest as names for the stable channel) and SET-07.c (the channel is selectable: Stable, Beta or Other; deferred) still speak of channels. Recommended: delete SET-05.e and SET-07.c and keep DEP-02.h.
  Answer:
