# Requirements: google

Google sign-in and 2-way sync, health and recovery, the Beta: Google Traffic section. Issues against this feature
(kept in the issues database): I5, I41, I42, I47, I50.

| ID | status | statement | test | was |
|---|---|---|---|---|
| GGL-01 | built | A Beta section on the main page, below Activity, lets the Developer start the Google API sync by hand. | — | F59 |
| GGL-02 | built | The Beta section shows all message traffic between the app and Google, with nothing hidden (tokens and client secret included), and only to the signed-in Developer. | — | F59 |
| GGL-03 | built | The normal Sync Now button and health chip are duplicated in each Google module of the Beta section. | — | F59 |
| GGL-04 | built | A Copy all button next to Clear copies every call currently shown, collapsed rows included, with full request and response, in one click. | — | F64.2 |
