# DRAFT requirements: time (shared by every feature; for the Developer's review)

Not approved. The one place that says how time works. Calendar, events, rules, google and feeds reference these rows and do not
restate them (Developer, Nov 17: "we are creating lots of exception rules; I want the guidance to be clear"). Prefix TIM.

| ID | status | statement |
|---|---|---|
| TIM-01 | proposed | Every event's start and end are stored in UTC together with the time zone each was recorded in. |
| TIM-02 | proposed | An event's time zone is set when it is created (imported: from the source; added: the system zone, or the calendar's zone if one is selected, EVT-05) and stays as recorded until the user edits the event with Edit Event. |
| TIM-03 | proposed | The calendar shows every event in the Local time zone: the system (device) zone, or the fixed zone chosen in Settings > Time Zones (SET-47). Changing the Local zone changes only how times are shown. |
| TIM-04 | proposed | An all-day event is a 24-hour event, local midnight to the next local midnight in its own time zone, stored in UTC like any other. It is shown like any other event, so it is one day in its own zone and can span two days in another (CAL-65). |
| TIM-05 | proposed | Rules do not depend on a time zone. A rule is applied to an event, and the event's recorded time zone decides what "Friday" or "22:00" means. Only a rule that is literally about a time zone uses a zone. |
| TIM-06 | proposed | Google receives each event's time zone with its times (syncing the zone). An all-day event is sent as the 24-hour timed event it is. |
| TIM-07 | proposed | Calendar feeds carry each event's times with its time zone. |
| TIM-08 | proposed (?) | An imported event that carries no time zone gets a default zone (open: Q-T9). |

Decided elsewhere, not repeated: UTC instants hide daylight-saving jumps, and the default rule "24-hour events" (RUL-29) realigns a
fixed 24-hour source span to the local day.
