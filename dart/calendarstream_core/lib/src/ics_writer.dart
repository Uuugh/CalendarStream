import 'dart:convert';

import 'calendar_event.dart';

/// Pure Dart counterpart to app/calsync.py's build_feed().
///
/// RFC 5545 output uses CRLF, UTF-8-aware 75-octet folding, escaped text,
/// exclusive all-day end dates and UTC timestamps. Parsing and recurrence
/// expansion are separate migration milestones.
class IcsWriter {
  const IcsWriter();

  String buildFeed(
    Iterable<CalendarEvent> events, {
    required String name,
    required String timezone,
    String color = '',
    DateTime? generatedAt,
  }) {
    if (color.isNotEmpty && !RegExp(r'^#[0-9a-fA-F]{6}$').hasMatch(color)) {
      throw const FormatException('Color must be a six-digit hex value.');
    }
    final stamp = _utcStamp((generatedAt ?? DateTime.now()).toUtc());
    final lines = <String>[
      'BEGIN:VCALENDAR',
      'PRODID:-//calendar_stream//EN',
      'VERSION:2.0',
      'X-WR-CALNAME:${_escape(name)}',
      'NAME:${_escape(name)}',
      'X-WR-TIMEZONE:${_escape(timezone)}',
      'REFRESH-INTERVAL;VALUE=DURATION:PT1H',
      'X-PUBLISHED-TTL:PT1H',
      if (color.isNotEmpty) 'X-APPLE-CALENDAR-COLOR:${color.toUpperCase()}',
    ];
    for (final event in events) {
      if (event.hidden) continue;
      if (event.uid.isEmpty) {
        throw const FormatException('An exported event needs a UID.');
      }
      lines.addAll([
        'BEGIN:VEVENT',
        'UID:${_escape(event.uid)}',
        'DTSTAMP:$stamp',
        'SUMMARY:${_escape(event.title)}',
      ]);
      if (event.allDay) {
        lines.add('DTSTART;VALUE=DATE:${_date(event.start)}');
        lines.add('DTEND;VALUE=DATE:${_date(event.end)}');
      } else {
        lines.add('DTSTART:${_timed(event.start)}');
        lines.add('DTEND:${_timed(event.end)}');
      }
      if (event.free) lines.add('TRANSP:TRANSPARENT');
      if (event.location.isNotEmpty) {
        lines.add('LOCATION:${_escape(event.location)}');
      }
      if (event.description.isNotEmpty) {
        lines.add('DESCRIPTION:${_escape(event.description)}');
      }
      final marker = switch (event.origin) {
        'custom' => 'added',
        'rule' => 'rule',
        _ => event.edited ? 'edited' : 'source',
      };
      lines.add('X-CALENDAR-STREAM:$marker');
      for (final minutes in event.alarmMinutes) {
        lines.addAll([
          'BEGIN:VALARM',
          'ACTION:DISPLAY',
          'DESCRIPTION:${_escape(event.title)}',
          'TRIGGER:-PT${minutes}M',
          'END:VALARM',
        ]);
      }
      lines.add('END:VEVENT');
    }
    lines.add('END:VCALENDAR');
    return "${lines.map(_fold).join('\r\n')}\r\n";
  }

  String _date(String iso) {
    if (!RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(iso)) {
      throw FormatException('All-day dates must be YYYY-MM-DD: $iso');
    }
    final parsed = DateTime.parse(iso);
    final normalized = "${parsed.year.toString().padLeft(4, '0')}-"
        "${parsed.month.toString().padLeft(2, '0')}-"
        "${parsed.day.toString().padLeft(2, '0')}";
    if (normalized != iso) throw FormatException('Invalid date: $iso');
    return iso.replaceAll('-', '');
  }

  String _timed(String iso) {
    if (!RegExp(r'(?:Z|[+-]\d{2}:\d{2})$').hasMatch(iso)) {
      throw FormatException('Timed events require a UTC offset: $iso');
    }
    return _utcStamp(DateTime.parse(iso).toUtc());
  }

  String _utcStamp(DateTime value) {
    final utc = value.toUtc();
    String pad(int n, int width) => n.toString().padLeft(width, '0');
    return "${pad(utc.year, 4)}${pad(utc.month, 2)}${pad(utc.day, 2)}"
        "T${pad(utc.hour, 2)}${pad(utc.minute, 2)}${pad(utc.second, 2)}Z";
  }

  String _escape(String value) {
    return value
        .replaceAll(r'\', r'\\')
        .replaceAll('\r\n', '\n')
        .replaceAll('\r', '\n')
        .replaceAll('\n', r'\n')
        .replaceAll(';', r'\;')
        .replaceAll(',', r'\,');
  }

  String _fold(String line) {
    final result = StringBuffer();
    var length = 0;
    for (final rune in line.runes) {
      final char = String.fromCharCode(rune);
      final bytes = utf8.encode(char).length;
      if (length + bytes > 75) {
        result.write('\r\n ');
        length = 1;
      }
      result.write(char);
      length += bytes;
    }
    return result.toString();
  }
}
