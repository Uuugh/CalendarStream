# Requirements: account

Approved by the Developer (decisions and reviewed rows). Statuses: planned = approved, not built yet.

| ID | status | statement | test | was |
|---|---|---|---|---|
| ACC-16 | planned | Sign-in failures are limited: 5 failures from one address lock that address for 15 minutes; 25 failures from all addresses together within 15 minutes start a global block, during which a new outside address is refused even with the right password. An address that signed in successfully in the last 7 days can still authenticate. (The Developer, Nov 17; the Python app uses 50 together, so this changes it.) | — | S23-19, S23-20, S23-21, S53-10 |
| ACC-17 | planned | During the global block, requests from the networks 192.168.0.0 and 10.10.0.0 (taken as the /16 ranges) and from loopback, and from CalendarStream's own public domain, are not blocked. An address is judged from what a trusted proxy reports (DEP-07). | — | S53-11, S53-12; Developer, Nov 17 |
