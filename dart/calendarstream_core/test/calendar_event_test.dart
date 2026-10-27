import 'package:calendarstream_core/calendarstream_core.dart';
import 'package:test/test.dart';

void main() {
  test('fingerprint matches the Python all-day fixture', () {
    const event = CalendarEvent(
      uid: 'rdo',
      title: 'RDO',
      start: '2026-10-12',
      end: '2026-10-13',
      allDay: true,
    );
    expect(event.fingerprint(), '6ef298767329d2c4d02134a1ad22bf0daea084b0');
  });

  test('alarm minutes are deduplicated and ordered', () {
    const event = CalendarEvent(
      uid: 'a',
      title: 'Test',
      start: '2026-10-12',
      end: '2026-10-13',
      alarms: '15,60,15,0,-5,bad, 30,999999999999999999999999999999',
    );
    expect(event.alarmMinutes, [60, 30, 15, 0]);
  });
}
