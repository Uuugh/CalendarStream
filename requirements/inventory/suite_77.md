# Suite 77: Refactor contracts using unittest

Source: [`tests/suite_77.py`](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py) at `2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8`.

Static inventory only. These are candidate behavior observations, not approved requirements or a claim that the suite was executed. `Sxx-NN` identifies evidence in this inventory, not a permanent requirement ID.

## Setup and scope

Nine unittest methods with made-up ICS/events and in-memory collaborators; no app/database/browser. Scans/imports calendars, rule_engine, runtime, services and routes modules. Uses injected fake stores/providers, coroutine calls and Secret/CSRF-related helpers. Rows inventory 33 self.assert* call sites (including exception contexts) plus one conditional self.fail callback; there are no ok() calls.

## Checks

| Evidence | Candidate feature | Behavior checked | Source |
|---|---|---|---|
| S77-01 | process | Each sampled module docstring has the required header label, except the explicit calendars __init__ exemption. | [L74](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L74) |
| S77-02 | process | Sampled module ASTs have at most one top-level class, or at most four for errors.py. | [L75](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L75) |
| S77-03 | process | No sampled from-import has module exactly main. | [L81](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L81) |
| S77-04 | process | No sampled from-import names main in its import list. | [L82](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L82) |
| S77-05 | process | No sampled function AST contains an import statement, including in nested walked nodes. | [L84](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L84) |
| S77-06 | process | After importing all sampled modules, app.main is absent from sys.modules. | [L92](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L92) |
| S77-07 | sources / feeds | Parsing, feeding and reparsing the synthetic ICS preserves event title/start/end triples. | [L99](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L99) |
| S77-08 | sources | The noncalendar HTML payload raises SourceError in check_calendar. | [L103](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L103) |
| S77-09 | sources | The malformed ICS payload raises SourceError in parsing. | [L105](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L105) |
| S77-10 | events | Applying empty edits/hidden inputs preserves the fixture event list. | [L107](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L107) |
| S77-11 | rules | A no-end starter rule yields the expected two-hour end in the changed event. | [L121](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L121) |
| S77-12 | rules | The original input event's end remains unchanged. | [L122](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L122) |
| S77-13 | sources | A valid stored local default wins over source order. | [L131](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L131) |
| S77-14 | sources | An invalid stored default falls back to the first local source. | [L135](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L135) |
| S77-15 | sources | ensure_local on no sources saves the generated local ID as default. | [L146](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L146) |
| S77-16 | feeds | That creation adds the new local ID to the sampled destination's source list. | [L147](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L147) |
| S77-17 | event_templates | Template normalization ignores the invalid ID, collapses title spaces and raises a one-minute duration to five. | [L162](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L162) |
| S77-18 | settings | Public addresses are deduplicated with the main address first and valid extra second. | [L165](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L165) |
| S77-19 | sources | State.record prefixes the sampled log with the injected calendar name. | [L189](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L189) |
| S77-20 | sources | After replacing the store provider, the old store still has only its first log. | [L195](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L195) |
| S77-21 | sources | Saving through the replacement provider stores the current status under the source key. | [L196](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L196) |
| S77-22 | events | Failure callback: recursive follow_links must not call the supplied guard-state setter, which invokes self.fail. | [L206](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L206) |
| S77-23 | account | Two generated CSRF tokens differ. | [L215](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L215) |
| S77-24 | account | Checking a token against a different expected token raises an exception. | [L217](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L217) |
| S77-25 | account | That mismatched-token exception has status_code 400. | [L219](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L219) |
| S77-26 | sources | The calsync curl-version function returns the patched cached version. | [L223](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L223) |
| S77-27 | sources | The patched cached-version value remains unchanged after the call. | [L224](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L224) |
| S77-28 | google | A new GoogleJob starts with full=true. | [L228](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L228) |
| S77-29 | google | A new GoogleJob starts with running=false. | [L229](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L229) |
| S77-30 | google | A new GoogleJob wake event is initially unset. | [L230](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L230) |
| S77-31 | history | Change.done returns the injected state.record result seven. | [L247](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L247) |
| S77-32 | history | The captured Undo before snapshot contains the original value one. | [L248](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L248) |
| S77-33 | history | The captured Undo after snapshot contains the changed value two. | [L249](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L249) |
| S77-34 | history | Completing the Change calls the injected undo-trimming collaborator once. | [L250](https://github.com/Uuugh/CalendarStream/blob/2784fd02c28e1ca903ec8ffc336a5ce10e1ee6c8/tests/suite_77.py#L250) |

## Direct assertions

No direct Python `assert` statements. See the setup section for the unittest/failure-guard evidence units.

## Coverage limits and reconciliation notes

- These are unittest call sites, not ok() calls. Exception context rows prove the enclosed call raises; the conditional self.fail callback fails only if the recursion guard setter is reached. The whole method also implicitly fails on unexpected collaborator access/exceptions.
- Structural scans cover selected immediate *.py folders and top-level classes; they do not prove every layer dependency, file or dynamic import complies. Header content is searched by label presence. The no-app.main result depends on isolated suite process/import state.
- Calendar round trip compares title/start/end only. No-op edit equality and no-end input immutability sample one fixture. Default creation checks stored ID and one destination update, not a database transaction.
- The valid-CSRF check is an unasserted call that must not raise; rows 23–25 explicitly cover token difference and mismatch. Curl-version checks patch cache rather than invoking curl. Change snapshot tests use dictionary-returning collaborators rather than persistent History.
- Overlaps: suites 62 rule/helper separation; suites 63/70 defaults/security; suite 75 process headers; suite 69 job/decision types.
