# Requirements: events

The event pop-up, linked events, hiding and reverting. Issues against this feature: none open on the Dashboard.

| ID | status | statement | test | was |
|---|---|---|---|---|
| EVT-01 | planned | When editing an event, the event dialog has a Duplicate icon immediately right of "Edit <event>" and immediately left of the Print icon (today it sits to the right of Print). Duplicate opens an editor holding a copy of the event in the same calendar; the user may then choose a different calendar with the calendar dropdown before saving. The Duplicate icon in the calendar view (the event tools) stays as it is. | — | F62 |
| EVT-02 | planned | Right of Duplicate there is a Move icon, shown only for events CalendarStream itself owns, never for a read-only source such as CCS+ (United) (CAP-03). | — | F62 |
| EVT-03 | planned | Print includes the event card, not only the calendar grid. | — | F62 |
| EVT-05 | planned | A new event defaults to the system clock's time zone, or to the calendar's time zone when the calendar has one selected (Developer, Nov 17). It can be saved into any calendar chosen in the source selector; with none chosen it goes to the initial Local calendar. A custom event appears on its calendar page. | — | S19-33, S26-30, S36-21, S65-04 |
