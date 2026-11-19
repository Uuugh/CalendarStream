# Slice 2 comparison (A = calendar.md, calendar_filter.md, print.md, search.md; B = reverse/slice2.md)
B group header rows (R2-01, R2-02 ... 31 of them) are not counted; the 198 lettered rows are.
File key: CAL=calendar.md, FLT=calendar_filter.md, PRT=print.md, SRH=search.md, EVT=events requirements (event details/colors), common=common.md/DEF-01.

## GAP (B ID | behavior and values | A file)
R2-01.c | View button tooltip "View: <name>", accessible name "View" | CAL (CAL-06.c)
R2-01.e | Choosing a view saves it and redraws in place, no reload (A has UIC-13 generally, not stated for view) | CAL
R2-01.g/h/i | Default view Month; unknown stored value = Month; invalid view refused; a view named in the request applies to that request only, default unchanged | CAL (CAL-06.b says default goes in the control's row; none is given)
R2-02.a | Top-left of calendar: previous, next, Today, then title | CAL
R2-02.b/c | Prev/next step: 1 month in Month and List (lands on last day of previous month / first day of next), 7 days Week, 1 day Day | CAL (CAL-01.c has only Week)
R2-02.d | Prev/next tooltips and names "Previous/Next month|week|day" | CAL
R2-02.f | Prev/next/Today redraw in place; Ctrl/Cmd/Shift/middle click opens a new tab | CAL
R2-02.h | Swipe counts only if >=50 px horizontal and >=1.5x vertical; multi-finger ignored | CAL (CAL-01.j)
R2-03.a/b/c/d | Calendar date: missing/invalid or year outside 2000-2100 = today; month-only = 1st of that month (today if current month); month valid 2000-2100, 1-12; address keeps date/month, not view | CAL
R2-04.a/c | Titles: Month/List "Month Year" capitalised in page language; Day "weekday month day, year" | CAL
R2-04.e | Month picker year row: previous/next year, no limit, starts at displayed year | CAL (CAL-01.d)
R2-04.f | Picker shows 12 abbreviated month names, current year-month marked | CAL
R2-04.i | Year outside 2000-2100 from the picker opens on today (unsure in B) | CAL
R2-05.a | Month shows whole weeks, Sunday first, 4-6 weeks | CAL
R2-05.b | Week is 7 days Sunday to Saturday containing the date | CAL
R2-05.d | List shows one row per day with events of the date's month; none: "No events this month." | CAL
R2-05.e | Weekday headings two letters (Su Mo ...), Sunday first | CAL
R2-05.f | Month days outside the displayed month are muted | CAL
R2-05.g | Month cell shows day number and a hover/focus "+" (always visible, dimmed, without hover) | CAL
R2-05.h | Clicking an empty spot of a day cell/column/all-day cell opens Add event for that date; tooltip text | CAL
R2-05.j/k | List row: day number, day text, hover "+"; at <=600 px date sits above events, else 150 px column | CAL
R2-06.c | Compact calendar controls 28 px, nav buttons 34 px; wrap re-evaluated on resize (80 ms) and font load | CAL/theme
R2-07.b/c/d/e | Zone list: group Common (14 listed US/world zones, fixed order) and All time zones (area/city, excluding Etc/SystemV/posix/right, plus UTC); server's zone starred | CAL
R2-07.k | Clock button only writes 12 or 24, never back to auto | CAL (TIM-10)
R2-10.a | Source-deleted ("gone") events never shown | CAL
R2-10.b/c/d | Day placement: every day covered in display zone; timed end exactly at midnight excludes new day; end<=start = start day only; all-day end exclusive, at least first day | CAL
R2-10.e | Order within a day = start order | CAL
R2-10.f | App-added then deleted event vanishes; source-deleted event stays struck through and grey | CAL
R2-11.a | Event line: time label, title, marks; wraps in grid/List/all-day, ellipsis in Month | CAL
R2-11.b | Line tooltip = title + " (<where deleted>)" or " (hidden from Google)" | CAL
R2-11.c/d/e | Labels: "start-end"; multi-day "start ->", "-> end", middle days "cont."; all-day none, multi-day all-day "cont." after day one | CAL
R2-11.g | Marks: warning (source changed since edit; "United changed..." for CCS) else edit else rule-added icon; none when deleted; reminder icon | EVT/CAL
R2-11.h | Click opens details inline (title, range, location pin, notes, state lines, tools), stays open across redraws until Close | EVT
R2-11.i | Range text formats incl. "(all day)" | EVT
R2-11.j | State lines in details (where deleted, hidden, stale, edited, added here, added by rule, linked) | EVT
R2-11.k | Calendar name shown in details only when more than one calendar | EVT
R2-11.l | Deleted event shows Restore, except rule-deleted ("change or remove the rule") | EVT
R2-11.m | Tools row: Close left; link, reminders, edit, duplicate, delete/hide right; confirmation texts | EVT
R2-12.b | Month grid min 640 px wide, scrolls sideways; none in Full page | CAL
R2-12.d | In Month all-day and timed events look alike (one-line bar) | CAL
R2-13.b | Hour labels 12am..11pm / 00:00..23:00, midnight label hidden | CAL
R2-13.c | Timed event top/height by minutes; min drawn 15 min; cut at 24:00, continues from 00:00 | CAL
R2-13.f | Hour area at most 560 px + stretch tall (Full page: space left, min 200 px) | CAL
R2-13.h | Event text 11.5 px; opened event expands to full column width with shadow, on top | CAL
R2-14.a-d | Lane rule: sort by start then longer first; cluster breaks when start >= latest end (touching events do not overlap); first free lane; width 1/lanes minus 3 px, left lane/lanes plus 1 px | CAL (CAL-01.h only "side by side")
R2-14.e | Lanes per day; multi-day event has own segment per day | CAL
R2-15.a | Color precedence: own, rule, calendar, default #1d4ed8 | EVT/CAL
R2-15.b | Bar = color mixed with card 18% dark/12% light; text mixed 70%/60% | theme
R2-15.c | "Custom" look for app-added/rule events (dark #2e1a47/#e9d5ff, light #f4eef8/#5e3f7a) (precedence unsure) | theme
R2-15.d | Hidden: struck through 55% opaque; deleted: 85% grayscale, 45% opaque | theme/CAL
R2-15.e | Event's own color is one of Google's 11 colors | EVT
R2-16.b | All-day dates not shifted by display zone | CAL
R2-17.b | Lanes only in Week and Day | CAL
R2-31.g | Slider ARIA: range -300..1200 label and arrow labels (A: lines, UIC-16) | common (UIC-16)
R2-31.i | Stretch spread equally over weeks in Month; enlarges hour area in Week/Day | CAL
R2-32.c | Hour-height validation (refused outside range, bad stored value reads default) | CAL
R2-33.e | Only Month in Full page adds extra weeks | CAL
R2-33.f | Full-page height = window - body top - key height - 36 px, min 260 px | CAL
R2-33.g | Full page: Week/Day limit hour area to available height (min 200 px); List scrolls inside | CAL
R2-33.h | Resize bar not shown in Full page (nor List) | CAL
R2-33.i | Full page refits on resize (80 ms) and font load | CAL
R2-33.j | Full-page Month cell has no min height, scrolls its own content | CAL
R2-51.c | Week print: one page per week (Sun-Sat) from week of From; max 60 pages | PRT/CAL
R2-51.d | 5-day print: same weeks, Mon-Fri always; max 60 | PRT/CAL
R2-51.e | Day print: one page per day, max 62 | PRT/CAL
R2-51.g/h | "Include weekends" choice (default on): Week, Month, Itinerary drop Sat/Sun; Day and 5-day unaffected | PRT
R2-51.i | Week, 5-day, Day, Itinerary pages show " · location" and calendar name if >1 calendar; Month shows neither | PRT
R2-51.j | Week/Month page title = calendar title; Day page = day title | PRT
R2-51.k | Day page with no events says "No events." | PRT
R2-51.m | Printed Month shades days outside the month | PRT
R2-52.b | Date defaults: From = 1st of current month, To = last day of From's month; invalid falls back | PRT
R2-52.e | Range limited to 731 days after From | PRT
R2-53.d | Print type scales with the sheet; heading 1.7x base | PRT
R2-53.f | Saved orientation values land/port/auto | PRT
R2-54.b | Background colors printed exactly | PRT
R2-54.c | Saved theme values dark/light, else light | PRT
R2-54.d | Printed event tint: own/rule color; calendar color only for United events; custom look; hidden struck 60% | PRT
R2-56.a | Browser-printing the status page prints only the calendar (everything else hidden, black on white, titles wrap, no open details, cells do not split) | PRT
R2-60.c | Opening search focuses the box | SRH
R2-60.g | Identical search address not requested again | SRH
R2-61.a | Query split on whitespace, case-insensitive, every word must be in title, location or notes | SRH
R2-61.b | Query trimmed, first 100 characters; empty = no search | SRH
R2-61.e | Multi-day event listed once, on first day inside range; outside range not listed | SRH
R2-62.d | Result events open details like calendar; open details kept on redraw | SRH
R2-62.e | Search not saved; address keeps only query and filters | SRH
R2-70.f | Calendars and Key share width equally with rule between; >700 px each keeps at least its list width | FLT
R2-71.d/e/f | State hiding semantics: Hidden hides non-deleted hidden; "changed since" hides non-deleted stale; Edited hides edited not stale not deleted | FLT
R2-71.h | Filter saved as list of keys (src:id, edited, stale, hidden, deleted), max 60, invalid refused, "-" = none | FLT

## DIFFERENT (B ID | A ID | A says | B says)
R2-01.a | CAL-01.b | Month, Week, 5-day, Day, List | exactly Month, Week, Day, List
R2-01.b | CAL-01.b | 5-day is a view | no 5-day view (only in Print Preview), "not implemented"
R2-01.k | CAL-06.b/CAL-02.a | view is a user setting, device-kept | view saved on server, same default in every browser
R2-02.e | CAL-01.e | Today returns to current month | Today goes to current date in the current view
R2-06.a | CAL-06.a | right zone: Time Zone, View, 12/24, Print, Full page, + | Time Zone, view, clock, Search, Print, +; Full page is in the title bar
R2-07.f | CAL-02.a | zone choice kept on the device | saved on the server; choosing the configured zone clears it; unknown refused
R2-07.i | CAL-06.b/UIC-13 | change shows at once, no reload | clicking clock reloads the whole page
R2-07.j | TIM-10 | default 12h in US zone else 24h; user setting | auto = 12h for English, 24h other languages (saved values auto/12/24)
R2-12.a | CAL-01.g | day cell shows count of events that do not fit | cells grow, no "+N more"
R2-17.a | CAL-01.g | overflow count exists | no overflow count in any view
R2-13.e | CAL-04.d/DEF-01 | hour height in event lines, 1-6, default 2 | 44 px default, 20-120 px
R2-30.a | CAL-03 | events move by long-press drag (Week/Day snap 15 min, Month by day) | no drag move; edit in form
R2-31.b | CAL-04.b | height in whole event lines, no pixel limits | stretch in px, -300..1200, default 0
R2-31.c | CAL-04.b/UIC-16 | whole-line steps | 1 px per px, saved after 400 ms
R2-31.e | CAL-04.c | collapse = fewest lines the view needs | collapse = stretch -300
R2-32.b | CAL-04.d | whole lines per hour | 1 px per 6 px dragged, keys +/-4 px, 20-120
R2-33.a | CAL-04.a/CAL-06.a | Full page in calendar right zone, restore-down icon | title-bar button left of settings menu, shows "Back"
R2-52.d | UIC-23 | an end before the start is not valid | To before From are swapped
R2-53.e | PRT-01.d | each print sheet fits one page | Itinerary flows over several pages in 12 px type, not fitted
R2-60.a | SRH-01.a | search in top bar, searches events, rules, calendars, feeds, templates, History | calendar-only search line toggled under the calendar top line
R2-60.b | SRH-01.e | narrow by calendar and date range | box (100 char max), calendar select, From/To, close button
R2-60.d | SRH-02.b | results fill as each feature answers | updates 300 ms after typing stops, immediately on select/date change
R2-62.a/c | SRH-02.a | grouped by feature, calendar events first, 6 per feature, "more" in steps | events listed by day in List form, n found
R2-70.c | FLT-01.a/f | Key: rule colors and states "Edited", "Changed by the source since the edit", "Hidden from Google", "Deleted" | "United changed it since" wording; rule swatches first
R2-70.d | FLT-01.h | rule key name cut to DEF-01 length, tooltip full | 25 chars; text = rule title, else first text condition, else label; All-calendar rules not listed
R2-71.k | FLT-01.f | clicking any Key item dims/hides | rule color entries are informational, not clickable

## A-ONLY (A ID | phrase)
CAL-03.a | long-press drag moves editable events
CAL-03.b | Week/Day drag snaps to drag step (15 min)
CAL-03.c | Month drag keeps time, changes day
CAL-03.d | long-press time from Settings > Theme
CAL-01.b (5-day) | 5-day view with hourly grid
CAL-01.g | overflow count in a day cell
CAL-04.c | collapse/expand by lines (B uses px)
CAL-04.d | hour height in lines within DEF-01 limits
CAL-04.e | Full page hides footer (B 33.a also: covered; only listed for completeness, not A-only)
CAL-06.b | all right-zone control states are user settings
CAL-06.c | icon-only wrap to second line rule is covered; A-only part: Search not in zone
FLT-01.a | one filter icon with dropdown listing calendars and states (B has only the Key buttons)
FLT-01.b | filter follows common filter rules UIC-21
FLT-01.c | filter choices kept leaving Full page
FLT-01.i | no Timed/All-day/Added color labels
PRT-01.g | Print Preview as dialog with shared date range
PRT-01.h | every section printable (Rules, Templates, History layouts TBD)
PRT-01.i | 5 mm margins (B 53.b also states 5 mm: covered)
PRT-01.b | print choices are user settings (device), B saves print choices on server (covered, differs in place)
CAL-05.e | one event prints as Day (B 50.d covered)
SRH-01.a/b | global top-bar search across features
SRH-01.f/g | typed query kept; closing returns to previous view (partly B 60.e/f)
SRH-02.a | per-feature result groups, 6 default, more in steps
(Real A-only list: CAL-03.a-d, CAL-01.g, CAL-04.b-d in lines, CAL-06.b, FLT-01.a-c and .i, PRT-01.g-h, SRH-01.a, SRH-02.a-b; the other lines above are partly supported and are noted as such.)

## Counts
B rows (198 lettered): covered 62, different 27, gap 109; A rows only-in-A: 25 (CAL-03.a-d, CAL-01.g, CAL-04.b-d, CAL-06.b, FLT-01.a-c, FLT-01.i, PRT-01.g-h, SRH-01.a, SRH-02.a-b, plus partly: CAL-01.b 5-day, CAL-04.e, CAL-05.e, PRT-01.b, SRH-01.f-g)
