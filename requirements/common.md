# Requirements: common

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | was |
|---|---|---|---|---|
| TIM-01 | planned | Every event's start and end are stored in UTC together with the time zone each was recorded in. | — | Developer, Nov 17 |
| TIM-02 | planned | An event's time zone is set when it is created (imported: from the source, or the zone the source's calendar reports; added: the system zone, or the calendar's zone if one is selected, EVT-05) and stays as recorded until the user edits the event with Edit Event. | — | Developer, Nov 17 |
| TIM-03 | planned | The calendar shows every event in the Local time zone: the system (device) zone, or the fixed zone chosen in Settings > Time Zones (SET-47). Changing the Local zone changes only how times are shown. | — | Developer, Nov 17 |
| TIM-04 | planned | An all-day event is a 24-hour event, local midnight to the next local midnight in its own time zone, stored in UTC like any other. It is shown like any other event, so it is one day in its own zone and can span two days in another (CAL-65). When it is sent to an outside calendar that has an all-day type (Google, calendar feeds), it is sent as an all-day event for its stored time zone, with that zone's local dates. | — | Developer, Nov 17 |
| TIM-05 | planned | Rules do not depend on a time zone. A rule is applied to an event, and the event's recorded time zone decides what "Friday" or "22:00" means. Only a rule that is literally about a time zone uses a zone. | — | Developer, Nov 17 |
| TIM-06 | planned | Syncing with an outside calendar reads the time zone of that calendar and of each incoming event and records it with the event (TIM-02), and sends each event's recorded time zone with its times. | — | Developer, Nov 17 |
| TIM-07 | planned | Calendar feeds carry each event's times with its time zone. | — | Developer, Nov 17 |
| UI-12 | planned | One shared multi-select dropdown (the language dropdown and the Calendar filter use it): it opens from a single icon; a single click or tap toggles an item and takes effect at once; Ctrl and Shift select several on a keyboard; Select all and Select none are offered; choosing outside the dropdown (losing focus) closes it. (Developer, Nov 17) | — | Developer |
| UI-13 | planned | A change the user makes (a filter, a view, a theme, a setting) is shown at once: nothing needs a page reload or an Apply step. (Developer, Nov 17: the client redraws only the element that changed.) | — | Developer |
