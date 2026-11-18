# Requirements scan 1 (Nov 17): duplications and lessons from the calendar review

Run after the calendar.md review, over all 17 requirement files (about 470 rows). Applied changes are marked **done**; the rest are for the
Developer's decision.

## Lessons learned in the calendar review (apply to every feature)

1. **One owner per behavior.** A behavior used by several features lives once in `common.md` (TIM time, UI components, CAP what an origin
   allows) and features only reference it. New this review: UI-14 zones, UI-15 anchors, UI-16 resize bar, UI-17 components separate from features.
2. **No exceptions.** Fix the general rule (zone kinds, CAP) instead of a per-feature carve-out.
3. **Look vs behavior.** What a component looks like and where it sits is the theme (13a to 13d); a feature keeps only what a test can check about
   its own content. (Placement of a specific icon can stay in the feature row, as in CAL-04.)
4. **A control that cannot produce a bad value needs no "refused" rule** (CAL-23 was removed). Rows that say "an unknown X is refused" are
   candidates when X is chosen from a list or toggle.
5. **Units are relative, not pixels** (event lines, theme sizes); pixel limits are retired.
6. **Where a setting lives:** view settings (language, clock, theme, time zone choice) on the device; the installation's default zone and other
   deployment settings in the database, which overrides `.env` (DEP-28).
7. **Web-page mechanics do not exist in the client** (reload, refresh, page address): UI-13 (changes show at once) covers them.
8. **Python-test wording is not a requirement** ("saves that choice again", "the sampled ...", "the fixture").
9. **Cross-feature settings belong in common or the top bar** (the 12/24 format left the calendar for the top bar, TIM-10).

## Done in this scan

- Calendar duplicates removed: CAL-53 (Full page, same as CAL-04; evidence moved), CAL-58 (restated CAL-57 and CAL-59), CAL-43 (same as CAL-39; evidence
  moved), CAL-45 (same as FLT-05), CAL-61 (merged into CAL-60, orientation as one row, with the automatic rule from the gap triage), CAL-62 (replaced by
  nothing: its question is answered by UI-14, since Print prints the view, CAL-66).
- DOC-09 removed (same as SHL-03, the logo files); TPL-06 removed (same as RUL-23, a rule that names a missing template is refused).

## For the Developer to decide

| Finding | Rows | Suggestion |
|---|---|---|
| Restates a common rule | CAL-19 vs TIM-03 and SET-47; CAL-65 vs TIM-04 | Keep one: delete CAL-19 and CAL-65 (they are your agreed rows, so only you remove them), TIM-03 and TIM-04 say it. |
| Restates common rules | GGL-85 vs TIM-04 and TIM-06 | Shorten GGL-85 to "Google sync follows TIM-04 and TIM-06". |
| Reminders sent out twice | FED-17 and GGL-25 | One common rule: an outgoing calendar carries the event's reminders. |
| "Refused" rows a control already prevents | 73 rows say refused, rejected, invalid or unknown; likely impossible by control: SHL-06, SHL-14 (language), SET-17, EVT-16, FED-08 | Review each when its feature is reviewed. |
| Python-test wording ("sampled", "fixture", "the checked") | 24 rows: ACC-19, CAL-60..63 (fixed), FED-25, 27, 30, GGL-13, 42, 43, 63, 77, HIS-02, 08, RUL-44, SET-14, 19, 22, 23, 37, 39, 40, 41, SHL-17 | Reword during each feature's review. |
| Web-page mechanics | ACC-06, DIA-01, FED-03, GGL-12, 15, SET-05, 14, 31, 37, SHL-05, 12, 16, 17, 19, SRC-08 | Restate for the client (UI-13) during each feature's review. |
| UI mechanics inside features | EVT-01, 02, 04, 25, 32, GGL-03, 04, RUL-01, 36, 41, SET-06, 07, 39, SHL-01, 02, 09, 17, FLT-01, SRH-01 | Check against UI-01 to UI-17 during each feature's review. |
