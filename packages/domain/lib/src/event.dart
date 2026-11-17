/// Calendar event model.
///
/// Holds: [Event].
/// Depends on: nothing in the app (only `crypto` for the fingerprint).
/// Used by: rules, events, calendar, sources, feeds, history, google features.
/// Reads/writes: nothing.
/// Ported from: app/calendars/event.py (Python), the oracle until step 5.
library;

import 'dart:convert';

import 'package:crypto/crypto.dart';

/// One calendar event. Times are ISO strings in the display time zone; an all-day event holds
/// ISO dates with the end exclusive.
class Event {
  Event({
    required this.title,
    required this.start,
    required this.end,
    this.allDay = false,
    this.location = '',
    this.description = '',
    this.uid = '',
    this.origin = 'united',
    this.edited = false,
    this.stale = false,
    this.hidden = false,
    this.free = false,
    this.color = '',
    this.source = 'ccs',
    this.alarms = '',
    this.ruleColor = '',
    this.deleted = '',
    this.meeting = '',
    this.noEnd = false,
    this.ruled = false,
  });

  String title;
  String start;
  String end;
  bool allDay;
  String location;
  String description;
  String uid;

  /// `united` (from the source), `custom` (added on the page) or `rule` (made by a rule).
  String origin;

  /// A source event changed on the page.
  bool edited;

  /// The source changed this event after it was edited here.
  bool stale;

  /// Left out of the Google feed.
  bool hidden;

  /// Shown as "free" rather than "busy".
  bool free;

  /// A color chosen for this event (`#rrggbb`); overrides rules.
  String color;

  /// The calendar source it belongs to (`ccs` or a feed source's ID).
  String source;

  /// Reminders, minutes before the start (`15,60`).
  String alarms;

  /// The color its rules give it (`#rrggbb`) or empty; its own color still wins.
  String ruleColor;

  /// Deleted but kept until Undo pops off: `<where>|<when>`, or `gone` after that.
  String deleted;

  /// Its online meeting link (Zoom, Meet, Teams, Webex) or empty.
  String meeting;

  // Not stored: set while a download is read, for the rules.
  /// It had no end time (its end is its start).
  bool noEnd;

  /// A rule changed its time.
  bool ruled;

  /// The reminders, as minutes before the start, largest (earliest) first.
  List<int> alarmMinutes() {
    final minutes = <int>{};
    for (final part in alarms.split(',')) {
      final text = part.trim();
      if (text.isNotEmpty && RegExp(r'^\d+$').hasMatch(text)) {
        minutes.add(int.parse(text));
      }
    }
    return minutes.toList()..sort((a, b) => b.compareTo(a));
  }

  /// Identifies the source's version of an event, to notice when it changes after an edit.
  String fingerprint() {
    final key = [title, start, end, allDay ? 'True' : 'False', location, description].join('|');
    return sha1.convert(utf8.encode(key)).toString();
  }
}
