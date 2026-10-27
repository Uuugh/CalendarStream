import 'dart:convert';

import 'package:calendarstream_core/calendarstream_core.dart';
import 'package:test/test.dart';

void main() {
  const writer = IcsWriter();
  final stamp = DateTime.utc(2026, 10, 27);

  test('all-day, reminders, transparency and hidden events', () {
    final feed = writer.buildFeed(
      const [
        CalendarEvent(
          uid: 'rdo@example',
          title: 'RDO',
          start: '2026-10-12',
          end: '2026-10-13',
          allDay: true,
          free: true,
          alarms: '15,60,15',
        ),
        CalendarEvent(
          uid: 'hidden@example',
          title: 'SECRET',
          start: '2026-10-12',
          end: '2026-10-13',
          allDay: true,
          hidden: true,
        ),
      ],
      name: 'My schedule',
      timezone: 'America/Chicago',
      generatedAt: stamp,
    );
    expect(feed, contains('DTSTART;VALUE=DATE:20261012\r\n'));
    expect(feed, contains('DTEND;VALUE=DATE:20261013\r\n'));
    expect(feed, contains('TRANSP:TRANSPARENT\r\n'));
    expect(feed, contains('DTSTAMP:20261027T000000Z\r\n'));
    expect(feed, contains('TRIGGER:-PT60M\r\n'));
    expect(feed, contains('TRIGGER:-PT15M\r\n'));
    expect(feed, isNot(contains('SECRET')));
    expect(feed.endsWith('END:VCALENDAR\r\n'), isTrue);
  });

  test('timed events convert offset to UTC', () {
    final feed = writer.buildFeed(
      const [
        CalendarEvent(
          uid: 'flight@example',
          title: 'Flight',
          start: '2026-10-12T10:00:00-04:00',
          end: '2026-10-12T11:00:00-04:00',
          origin: 'custom',
        ),
      ],
      name: 'Schedule',
      timezone: 'America/New_York',
      generatedAt: stamp,
    );
    expect(feed, contains('DTSTART:20261012T140000Z\r\n'));
    expect(feed, contains('DTEND:20261012T150000Z\r\n'));
    expect(feed, contains('X-CALENDAR-STREAM:added\r\n'));
  });

  test('text escapes and UTF-8 lines fold at 75 octets', () {
    final feed = writer.buildFeed(
      [
        CalendarEvent(
          uid: 'long@example',
          title: "${List.filled(30, '🛫').join()} a,b;c\\d",
          start: '2026-10-12',
          end: '2026-10-13',
          allDay: true,
          description: 'one\ntwo',
        ),
      ],
      name: 'My, schedule',
      timezone: 'America/Chicago',
      generatedAt: stamp,
    );
    expect(feed, contains('X-WR-CALNAME:My\\, schedule\r\n'));
    expect(feed, contains('DESCRIPTION:one\\ntwo\r\n'));
    expect(feed, contains(r'a\,b\;c\\d'));
    for (final line in feed.split('\r\n')) {
      if (line.isNotEmpty) {
        expect(utf8.encode(line).length, lessThanOrEqualTo(75));
      }
    }
    expect(feed, contains('\r\n '));
  });

  test('rejects timed events without explicit offset', () {
    expect(
      () => writer.buildFeed(
        const [
          CalendarEvent(
            uid: 'bad',
            title: 'Bad',
            start: '2026-10-12T10:00:00',
            end: '2026-10-12T11:00:00',
          ),
        ],
        name: 'Test',
        timezone: 'UTC',
      ),
      throwsFormatException,
    );
  });
}
