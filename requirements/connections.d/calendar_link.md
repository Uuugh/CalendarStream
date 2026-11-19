# Requirements: calendar link

The calendar-link connection: a calendar published at a web address (webcal or HTTPS), downloaded as a read-only calendar. Download rules are in `connections.md`.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| CLNK-01 | proposed | A calendar link, such as a secret address from Google, Outlook or iCloud, is downloaded as a connection. | — | — |
| CLNK-01.d | proposed | A calendar link is a source. | — | — |
| CLNK-01.a | proposed | A webcal source address is saved as its equivalent HTTPS address with its chosen name; duplicate source addresses are refused. | — | S26-08, S26-09 |
| CLNK-01.b | proposed | Calendar links from Outlook, Microsoft 365 and iCloud can be downloaded as source calendars. | — | readme_gaps:21 |
| CLNK-01.c | proposed | Source presets identify the provider and offer provider-specific setup guidance, including Google secret-address guidance and the United Airlines CCS+ name. Choosing Apple selects the Apple preset. | — | S33-01, S33-02, S33-23 |
| CLNK-01.e | proposed | A calendar link is downloaded over HTTPS: a plain HTTP address is not valid. | — | S23-28, S26-07, S60-21 |
