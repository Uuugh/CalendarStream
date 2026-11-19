# Requirements: common

| ID | status | statement | test | was |
|---|---|---|---|---|
| TIM-01 | backlog | Every event's start and end are stored in UTC together with the time zone each was recorded in. | — | Developer, Nov 17 |
| TIM-02 | backlog | An event's time zone is set when it is created (imported: from the source, or the zone the source's calendar reports; added: the system zone, or the calendar's zone if one is selected, EVT-01) and stays as recorded until the user edits the event with Edit Event. | — | Developer, Nov 17 |
| TIM-03 | backlog | The calendar shows every event in the Local time zone: the system (device) zone, or the fixed zone chosen in Settings > Time Zones (SET-02). Changing the Local zone changes only how times are shown. | — | Developer, Nov 17 |
| TIM-04 | backlog | An all-day event is a 24-hour event, local midnight to the next local midnight in its own time zone, stored in UTC like any other. It is shown like any other event, so it is one day in its own zone and can span two days in another. When it is sent to an outside calendar that has an all-day type (Google, calendar feeds), it is sent as an all-day event for its stored time zone, with that zone's local dates. | — | Developer, Nov 17 |
| TIM-05 | backlog | Rules do not depend on a time zone. A rule is applied to an event, and the event's recorded time zone decides what "Friday" or "22:00" means. Only a rule that is literally about a time zone uses a zone. | — | Developer, Nov 17 |
| TIM-06 | backlog | Syncing with an outside calendar reads the time zone of that calendar and of each incoming event and records it with the event (TIM-02), and sends each event's recorded time zone with its times. | — | Developer, Nov 17 |
| TIM-07 | backlog | Calendar feeds carry each event's times with its time zone. | — | Developer, Nov 17 |
| TIM-10 | backlog | The time format (12-hour, such as 1:30pm, or 24-hour, such as 13:30) is a user setting (SET-01) and applies to every time shown in every feature. Until the user chooses, it defaults to 12-hour when the device is in a US time zone and 24-hour elsewhere. One control switches it (CAL-06.a). The notation inside each format is a Theme setting (SET-03). | — | Developer, Nov 17; F15.2, F43, S19-03, S19-04, S21-05, S21-07, S21-08, S21-09, S66-16, S79-10..13 |
| UIC-12 | backlog | One shared multi-select dropdown (the language dropdown and the Calendar filter use it): it opens from a single icon; a single click or tap toggles an item and takes effect at once; Ctrl and Shift select several on a keyboard; choosing outside the dropdown (losing focus) closes it. | — | Developer |
| UIC-13 | backlog | A change the user makes (a filter, a view, a theme, a setting) is shown at once: nothing needs a page reload or an Apply step. | — | Developer |
| UIC-14 | backlog | Every row of controls has left, center and right zones, aligned left, centered and right by default, each keeping its own alignment; a feature stipulates the order of the items in each zone. A row that is too narrow is handled in this order: (1) the zones stack, left on top, then center, then right; (2) fonts and icons scale down within their zone, never below readable text and a 24×24 px target (scaling is always tried before clipping); (3) what still does not fit depends on the zone's kind: a control zone clips it at its edge and ends the text with a triple dot, a content zone (calendar grid, list, table, log) scrolls it. The layout does not mirror for right-to-left languages. No component has its own responsive rule (build_rules/theme.md, 13a). | — | Developer, Nov 17 |
| UIC-15 | backlog | A badge or other overlay on an image or control is placed by one of nine anchor points of its parent (the corners, the edge middles and the center) plus an offset relative to the parent's size, both defined in the theme (build_rules/theme.md, 13b); no component places its own badge. | — | Developer, Nov 17 |
| UIC-16 | backlog | One shared resize bar. The UI defines its look and operation: a bar centered at the bottom of what it resizes, drawn as two rows of six dots like a slider's; dragging it, or pressing the up and down keys, resizes in whole units; beside it one arrow collapses to the fewest units needed (arrow up when expanded) or expands to the bottom of the visible window (arrow down when collapsed). Collapse and expand are single actions: the size is kept when the window is resized. The feature that uses the bar defines its unit and what is resized in each of its views. | — | Developer, Nov 17; F51 |
| UIC-17 | backlog | UI components are kept separate from the features that use them: a component's look comes only from the theme, and a feature supplies only its content and what the component does there. So changing the theme restyles every feature at once, and a new feature reuses the components as they are. | — | Developer, Nov 17 |
| UIC-18 | proposed | One shared strength bar appears directly beneath any field where the user enters a secret (a password, a feed token), showing how strong the entry is as they type. It measures randomness (bits), not length alone; the bar only shows, and the field's feature decides whether an entry is accepted. Beside it, a hint recommends what to do (for example, the recommended minimum, or to use the generated value). The field's feature supplies the recommendation. | — | Developer, Nov 18 |
| UIC-19 | proposed | An entry that is not valid is marked at its own field with a note saying what is wrong, and it does not affect the other fields' valid values. A feature row says which entries are valid, and refers here for how the problem is shown. | — | SET-04, SET-06, SET-04 |
| UIC-20 | proposed | A color that is not in the shared palette (from an older rule, an import, or a destination that supports fewer colors) is represented by the nearest palette color wherever it is shown or sent (UIC-10). | — | RUL-58, CGOW-03, CGOW-03 |
| UIC-21 | proposed | One shared filter, used by the Calendar filter and History (and any feature with a filter). It is built on the shared dropdown (UIC-12): the user can select one, several, all or none of its choices; Select all shows everything and Select none shows nothing; the filter shows when it is active; the choices are saved and kept; a change applies at once (UIC-13). A feature supplies only the choices and what they filter. | — | FLT-01, FLT-01 |
| UIC-24 | proposed | A section whose items can be added has a + control as the rightmost item of its header's right zone; it opens the dialog for adding (UIC-01). | — | Developer, Nov 19 |
| UIC-25 | proposed | A button that does one thing and shows no state (an icon button, +, Copy, Open, Expand, Close) just does it; Copy then shows "Copied" in place of its icon for the time in DEF-01. | — | theme.md section 5; picture 2·5 |
| UIC-26 | proposed | A field that saves in place shows ✓ once saved, and ✕ \| ✓ while the user types: ✕ puts the saved value back, ✓ saves. | — | theme.md section 5 |
| UIC-27 | proposed | A Cancel \| Save pair sits at the bottom of what it saves and works as the rows below say. | — | theme.md section 6; picture 2·6 |
| UIC-27.a | backlog | Pressing a side fills the pair with its word ("Saved" or "Cancelled") for the time in DEF-01; then the pair is idle. | — | theme.md section 6 |
| UIC-27.b | backlog | With nothing to save both sides are disabled: not focusable and announced as unavailable. A pop-up's Cancel, which only closes it, and the buttons of a + Add pop-up, which can be saved with its defaults, stay available. | — | theme.md section 6 |
| UIC-27.c | backlog | The first change turns the pair on, and Save pulses for the time in DEF-01 and then stays in full color; saving or cancelling returns the pair to idle. | — | theme.md section 6 |
| UIC-27.d | backlog | A question's answers can be the same pair (No \| Yes, UIC-06). | — | theme.md section 6 |
| UIC-27.e | backlog | Adding something (+ Add a calendar…) ends with the same Cancel \| Save pair as editing it. | — | theme.md Clarifications |
| UIC-28 | proposed | A Status/Action button shows a status chip over the action that updates it (Sync Now, Check now, Update now, Connect, Fix), and a status looks one way for one meaning everywhere. | — | theme.md section 7; picture 2·7 |
| UIC-28.a | backlog | The four meanings are: done or OK; in action, or waiting on the user; a problem outside CalendarStream, or an entry that was refused; CalendarStream itself failed. Each has its one look (THM-05), whether it appears as a chip, a button, a done or failed state, or a line of text. | — | theme.md section 7 |
| UIC-28.b | backlog | Every copy of an action (the top bar and Settings; Feeds and Settings) shows the same words at the same moment and ends together. | — | theme.md section 7 |
| UIC-28.c | backlog | Inside a Status/Action button a status word always shows its icon and words together and never loses a word. Elsewhere a status word shows its icon and words for the time in DEF-01, then collapses to its icon (the words stay as its tooltip and accessible name); a one-off confirmation (such as "Saved") then vanishes and gives its line back, while an ongoing health status stays. | — | theme.md section 8 |
| UIC-28.d | backlog | While an update runs only the words of the top-bar Update now change, never a blank pill, and a bar slides under them until the app restarts. | — | theme.md section 7 |
| UIC-29 | proposed | Every connection is a module: a header that is all a folded module shows, with its details below when expanded. | — | theme.md section 9; picture 2·9 |
| UIC-29.a | backlog | The header's first line shows the color box, the kind (fixed text), "Last synced" with its time and the Status/Action buttons on the right. Its second line shows the label, with an (i), and "Next check @" with its time on the right. | — | theme.md section 9 |
| UIC-29.b | backlog | Expand sits in the module's bottom border (▸ Expand ◂, pointing at the words); when open, a Close line sits under the header (its triangles point up). While expanded the label is a field of the same size. | — | theme.md section 9 |
| UIC-29.c | backlog | Status lines are unboxed, right-aligned next to their Status/Action button, and visible only while the module is collapsed. | — | theme.md section 9 |
| UIC-29.d | backlog | Default sits right of a CalendarStream calendar's title; while expanded, the other local calendars offer it as a button and read-only calendars show it disabled (CLCL-03). | — | theme.md section 9 |
| UIC-29.e | backlog | On \| Off sits inline before an expanded module's note; Off dims the module and keeps its settings. | — | theme.md section 9 |
| UIC-29.f | backlog | (i) is info about the module: what it is, then its note when it has one. (?) is help (UIC-07.a). | — | theme.md section 9 |
| UIC-30 | proposed | A list of modules or rule lines can be reordered with one handle in the margin on the left of each line: ▲ above, a grip, ▼ below. | — | theme.md section 10; picture 2·10 |
| UIC-30.a | backlog | The handle is always visible and takes no extra space; there is none when there is nothing to reorder (a list of one). | — | theme.md section 10 |
| UIC-30.b | backlog | Dragging the grip reorders; ▲ and ▼ reorder with the keyboard. The grips are on the left, or on the right when the user chooses (SET-03). | — | theme.md section 10 |
| UIC-31 | proposed | Every + opens a dialog (UIC-01) centered; a question is a dialog too, never the browser's own alert or confirm box. | — | theme.md section 11; picture 2·11 |
| UIC-31.a | backlog | A question's answers are on one line, or one under the other when they are sentences; a second line under the question is a note, muted and not bold. | — | theme.md section 11 |
| UIC-31.b | backlog | A choice of calendars is a drop-down of ticks. | — | theme.md section 11 |
| UIC-31.c | backlog | The anchored month, view and language menus do not dim the page and do not fill the phone; they keep their compact panel. | — | theme.md section 11 |
| UIC-32 | proposed | In-page words are click paths and short lines (Place › Place › Field: value › Button), with no paragraphs; the why goes in a (?). Status words are a word or two (UIC-28). No sentence on the page is longer than 20 words, apart from a (?), the calendar and the log. | — | theme.md section 13; picture 2·13 |
| UIC-33 | proposed | The Import row is the same in every calendar: the heading, the file field (a file icon and "Choose Calendar.ics…", filling the line), the dates (UIC-23) and the button on the right. For CCS+ it is Manual Upload, which replaces the schedule, so it has no dates. | — | theme.md section 14; picture 2·14 |
| UIC-34 | proposed | A box means the user can change it: fixed text (a title, the release channel) is plain text, never in a field box. A part that looks like a module but has nothing to fold (Settings > Updates) uses the module header layout, always open, with no Expand. | — | theme.md Clarifications |
| UIC-35 | proposed | A Copy button sits inside its field, like the password box's eye. A pair of credential fields (client ID and secret) is laid out like a login, connected or not. | — | theme.md Clarifications |
| UIC-36 | proposed | In every dialog and form a field has a muted label over it and a value that cannot be changed (an event's calendar) is plain text; related fields share a line (Calendar \| Title; Starts \| Ends, each with its Time under it). | — | theme.md Clarifications |
| UIC-37 | backlog | One shared image editor sets an image for a place in the app (the logo, the favicon): the user picks a file, crops it, and the editor saves it as a PNG that fits the limits in DEF-01 for that place. | — |
| UIC-37.a | proposed | The editor accepts PNG, SVG, WebP, JPEG and ICO files. | — |
| UIC-37.b | proposed | The crop frame keeps the shape within the minimum and maximum aspect ratio of the place (DEF-01); the user moves and zooms the picture under the frame and sees the result before saving. | — |
| UIC-37.c | backlog | The saved image is always a PNG, redrawn as pixels (so nothing in an uploaded file can run), with its long side at most the output size in DEF-01 and its file no larger than the place's file size in DEF-01; if the file is still too large the image is scaled down until it fits. | — |
| UIC-23 | proposed | Wherever a range of dates is asked for (Print Preview, search, feeds, destinations, import) one shared control is used: From | To | All. Either end may be left empty; All means an empty range and clears both dates; the fields show hints in the date's format; an end before the start is not valid (UIC-19). | — | CFED-01 and CFED-14 (S evidence), SRH-01, theme.md section 14 |

## Time (TIM)

| ID | status | statement |
|---|---|---|
| TIM-08 | backlog | An imported event that carries no time zone gets the installation's default zone (DEP-05). | — | Developer, Nov 17 |
| TIM-09 | proposed | A time zone is always one of the real zones: the zone picker offers only real zones, and an imported event that names a zone that does not exist is given the default zone (TIM-08) instead. |

Decided elsewhere, not repeated: UTC instants hide daylight-saving jumps, and the default rule "24-hour events" (RUL-06) realigns a
fixed 24-hour source span to the local day.

## UI (UI)

| ID | status | statement | evidence |
|---|---|---|---|
| UIC-01 | proposed | A dialog opens centered over a dimmed backdrop. In a phone-width window it fills the screen and shows a Back control instead of the dialog header. | S44-27, S57-20, S36-57, S57-37 |
| UIC-02 | proposed | Back closes the dialog. Escape closes only the topmost open layer (a menu, time list or picker) and a second Escape closes the dialog. A dialog opened from another returns to it when closed. | S57-28..30, S58-32, S37-36, S67-15..17 |
| UIC-03 | proposed | A dialog fits the window height; its content area grows with a taller field (such as Notes). | S57-23, S57-24 |
| UIC-05 | proposed | A section (Calendar, Sources, Feeds, All Rules, Event Templates, History...) is a header and a body; its body stays hidden until expanded, and clicking the title alone does not expand it. | S33-24, S38-01, S38-13, S61-02 |
| UIC-05.a | backlog | Every section's header reads: icon, title, space, status lines, health, + (UIC-24). Calendars and Feeds have no status lines; All Rules and Event Templates have up to three (the conflicts or errors, otherwise how many); + is in the top right corner. | theme.md Clarifications |
| UIC-05.b | backlog | A folded section says "Expand to Configure" (Calendars, Feeds, All Rules, Event Templates) or "Expand for Details" (History). | theme.md Clarifications |
| UIC-05.c | proposed | A section the user left open folds by itself after the time in DEF-01; each section is judged on its own. | S61-13, S61-14 |
| UIC-05.d | proposed | The open or closed state of a section is a user setting (SET-01). | changelog_gaps_2101-2336:24 |
| UIC-05.e | proposed | A section that contains modules lists them in their saved order and reorders them as UIC-30 says; the new order is saved immediately. | — |
| UIC-05.f | proposed | The + of a section opens a dialog listing the kinds of connection the section can add, by their kind text (CON-02.d); choosing one opens that connection's own setup. | — |
| UIC-06 | proposed | An action that hides or deletes something asks first with a No \| Yes pair; cancelling changes nothing. | S57-33, S58-24, S58-25, S58-35, S44-26 |
| UIC-07 | backlog | One shared popover, like the info dot: clicking or tapping an info dot, or the triple dot that ends clipped text (UIC-14), shows its full text in a popover next to it, above or below as space allows. The popover is never wider than the window and its text wraps inside it, so it adds no horizontal scroll bar; if it is taller than the window it scrolls vertically. It closes when the user chooses outside it. The item's own click still works. The triple dot's click area is at least 24×24 px. This is the global definition of the triple dot;. | — | Developer, Nov 17; S58-01, S58-34, S57-35, S66-18 |
| UIC-07.a | backlog | A (?) is help: how to do something. It sits right after the word it explains; hover, focus or a click shows it. Its pop-up opens with its upper left at the icon; past the window's right edge, its upper right sits at that edge; past the bottom, its lower corners sit at the bottom. Explanations live in an (i) or a (?), never on the page. | — | theme.md section 12; picture 2·12 |
| UIC-08 | proposed | A checkbox's label ticks it when clicked; empty space beside the label does not. | S21-19, S21-20 |
| UIC-09 | proposed | The calendar picker is a small month calendar with previous/next month and Today; it opens on a given month, can mark items unselectable, and closes when an item is picked. | S58-07..12, S58-28..30 |
| UIC-10 | proposed | One shared color palette of named colors (Google's eleven event colors) is used wherever a color is chosen (rule action, event, calendar); the event editor adds a "calendar default" choice. A picked color shows and closes the palette. | S19-08, S19-41, S19-44, S40-09..11 |
| UIC-10.a | backlog | A click opens the palette (in a module, while it is expanded); the choice goes with the module's Save. The colors are THM-09. | — | theme.md section 11 |
| UIC-11 | proposed | One shared emoji picker, with search, is used wherever an emoji is chosen. | S44-41 |
| UIC-11.a | backlog | The common emoji sit beside the field; a rounded "Search for more emojis" field opens every emoji (up to Emoji 13.0, no flags, drawn by the device), ten a line, scrolling, filtered as the user types. | — | theme.md section 11 |
| UIC-11.b | proposed | Newer emoji display older-Windows compatibility guidance, while older compatible choices do not. Editing or choosing an older emoji clears the compatibility warning; choosing a newer one displays it. Shared explanatory help follows UIC-07. | S55-37, S55-41, S55-43, S55-44, S55-45, S55-46, S55-47 |

## Capabilities (CAP)

What a user may do with a calendar or an event follows from where it comes from, stated once here. Features reference these rows
instead of listing "never for read-only", "not for rule events" and similar exceptions. Origins: **imported** (from a source CalendarStream only reads, such as CCS+), **custom** (added in
CalendarStream), **rule** (made by a rule).

| ID | status | statement |
|---|---|---|
| CAP-01 | proposed | Imported and custom events can be edited; a rule event cannot be opened for editing, because its rule controls it (remote edits to it are corrected on sync, CGTW-01). |
| CAP-02 | proposed | An imported event can be hidden and shown again, never deleted from its source; a custom event can be deleted, and a deletion can be undone. |
| CAP-03 | proposed | Only custom events can be moved to another calendar; an imported event of a read-only source never is (EVT-06). |
| CAP-04 | proposed | Imported and custom events can be link targets; a rule event cannot. |
| CAP-05 | proposed | Any calendar CalendarStream owns (a Local calendar) can be the default calendar; a read-only source calendar cannot. |
| CAP-06 | proposed | Sync Now is offered only for calendars that download from outside; a Local calendar has nothing to download. |

## Defaults and limits (DEF)

| ID | status | statement | test | was |
|---|---|---|---|---|
| DEF-01 | backlog | Every default and limit is defined once, in the table below, and a feature row refers to it instead of repeating the number. A value that an admin setting exposes is stored in the database and overrides the default (DEP-05); the others stay as the defaults. | — | Developer, Nov 17 |
| DEF-02 | proposed | Every list that grows with use (logs, failure records, pending sign-ins) has a stated limit in the table below, and entries no longer needed are forgotten first, so memory cannot fill. A feature row refers to the limit instead of repeating it. | — | Developer, Nov 18 |
| DEF-03 | proposed | Wherever a limit or a count is in characters (a password length, a name length, a token length), a character is what the user sees as one character (a Unicode extended grapheme cluster), not a code unit; a special character is any character that is not a letter or a digit. | — | Developer, Nov 19 |

| Name | Default | Limit | Stored |
|---|---|---|---|
| Update check schedule | weekly | hourly, weekly, monthly (30 days), never | database (Site Admin) |
| Running-update memory | 15 minutes | | default only |
| Animation intensity | 100 % | 0 to 200 % | device |
| Animation duration | 100 % | 25 to 300 % | device |
| CCS+ sync interval | 60 minutes | 15 to 1,440 minutes | database |
| History kept | 100 changes | 1 to 200 | database |
| Login failures per address | 5 (15-minute lock) | | default only |
| Login failures in total | 25 within 15 minutes | | default only |
| Trusted address period | 7 days | | default only |
| Page sign-in session | 30 days | | default only |
| Page refresh after an update restarts | 15 seconds | | default only |
| Copied shown | 1.8 seconds | | default only |
| Saved or Cancelled shown | 3 seconds | | default only |
| Save pulse after the first change | about 5 seconds | | default only |
| Done, failed or found result held | 2.4 seconds | | default only |
| Good status word shown before it shrinks | 2.4 seconds | | default only |
| Working status shown at least | 0.7 seconds (Check now), 0.5 seconds per Connect step | | default only |
| Typing delay before a search or a regex test | 300 milliseconds | | default only |
| Google retry: first wait | 5 seconds, doubled each attempt | longest wait 15 minutes | default only |
| Google retry: attempts | 5 | 5 | default only |
| Google retry: jitter | up to 25 % added | | default only |
| Instant-update renewal | 1 day before it expires | | default only |
| Instant-update retry after refusal | 6 hours | | default only |
| Section left open folds after | 24 hours | | default only |
| Database connection retry | every 3 seconds, for up to 60 seconds | | default only |
| Phone-width window | 700 px wide or narrower | | default only |
| Stream token: generated length and strength | 22 characters, at least 128 bits of randomness | 1 to 128 characters | default only |
| Failure records kept (sign-in) | 10,000 addresses | 10,000 | default only |
| Known-good addresses kept | 1,000 | 1,000 | default only |
| Container log lines held | 3,000 | 3,000 | default only |
| Pending Google sign-ins | 20 | 20 | default only |
| Password minimum length | 11 characters | 8 or more | database (Site Admin) |
| Password minimum capital letters | 1 | 0 or more | database (Site Admin) |
| Password minimum lowercase letters | 1 | 0 or more | database (Site Admin) |
| Password minimum numbers | 1 | 0 or more | database (Site Admin) |
| Password minimum special characters | 1 | 0 or more | database (Site Admin) |
| Unlock link valid | 24 hours | | default only |
| Drag step in Week and Day | 15 minutes | | default only |
| Long-press time | 0.5 seconds | 0.3 to 1.5 seconds | device |
| Hour height | 2 event lines | 1 to 6 | device |
| Calendar key name length | 25 characters | | default only |
| Hourly grid scroll start | the first event, or 7 am | | default only |
| Search results per feature | 6 | | device |
| Conditions per rule | 12 | 12 | default only |
| Actions per rule | 6 | 6 | default only |
| Pattern evaluation budget | 0.05 seconds | | default only |
| Whole-day recognition tolerance | 5 minutes | | default only |
| Events kept per download | 5,000 | 5,000 | default only |
| Download size | 5 MB | 5 MB | default only |
| Redirects followed (CCS+) | 5 | 5 | default only |
| Recurrence expansion | 1 year back, 2 years ahead | | default only |
| CCS+ browser-patient attempts | 3 attempts, 90 seconds each | | default only |
| Rejected CCS+ sign-ins before pause | 2 | | default only |
| Google consent state valid | 15 minutes | | default only |
| Google invitation link valid | 7 days | | default only |
| Google instant-update lifetime requested | 7 days | | default only |
| Shortest event template duration | 5 minutes | | default only |
| Reminders per event | 5 | | default only |
| Longest reminder lead | 1 week | | default only |
| Networks trusted during a global block | 192.168.0.0/16, 10.10.0.0/16 and loopback | | default only |
| Connections | | at most 50 | default only |
| Logo image ratio (width to height) | | 1:1 to 1.2:1 | default only |
| Logo file size | | at most 256 KB | default only |
| Favicon image ratio (width to height) | | 1:1 to 1:1 | default only |
| Favicon file size | | at most 256 KB | default only |
| Image editor output size | | at most 512 px on the long side | default only |
