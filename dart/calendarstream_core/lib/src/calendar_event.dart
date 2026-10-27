import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Immutable event compatible with the stored fields in app/calsync.py.
///
/// All-day start/end are ISO dates (end exclusive). Timed start/end are ISO
/// datetimes with explicit UTC offsets.
class CalendarEvent {
  const CalendarEvent({
    required this.uid,
    required this.title,
    required this.start,
    required this.end,
    this.allDay = false,
    this.location = '',
    this.description = '',
    this.origin = 'united',
    this.edited = false,
    this.stale = false,
    this.hidden = false,
    this.free = false,
    this.color = '',
    this.source = 'ccs',
    this.alarms = '',
    this.ruleColor = '',
  });

  final String uid;
  final String title;
  final String start;
  final String end;
  final bool allDay;
  final String location;
  final String description;
  final String origin;
  final bool edited;
  final bool stale;
  final bool hidden;
  final bool free;
  final String color;
  final String source;
  final String alarms;
  final String ruleColor;

  /// Unique nonnegative alarm lead times, largest first (Python parity).
  List<int> get alarmMinutes {
    final values = <int>{};
    for (final part in alarms.split(',')) {
      final trimmed = part.trim();
      if (!RegExp(r'^[0-9]+$').hasMatch(trimmed)) continue;
      final minutes = int.tryParse(trimmed);
      if (minutes != null) values.add(minutes);
    }
    return values.toList()..sort((a, b) => b.compareTo(a));
  }

  /// Matches the original Python Event.fingerprint() for edit detection.
  ///
  /// SHA-1 is used only for legacy compatibility, not password hashing.
  String fingerprint() {
    final fields = [
      title,
      start,
      end,
      allDay ? 'True' : 'False',
      location,
      description,
    ];
    return sha1.convert(utf8.encode(fields.join('|'))).toString();
  }
}
