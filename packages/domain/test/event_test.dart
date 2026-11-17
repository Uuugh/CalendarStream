import 'package:domain/domain.dart';
import 'package:test/test.dart';

void main() {
  group('Event', () {
    test('alarm minutes: earliest first, duplicates and junk dropped', () {
      final e = Event(title: 't', start: 's', end: 'e', alarms: '15,60,7,60,x');
      expect(e.alarmMinutes(), [60, 15, 7]);
    });

    test('alarm minutes: none', () {
      expect(Event(title: 't', start: 's', end: 'e').alarmMinutes(), isEmpty);
    });

    test('fingerprint matches the Python app (sha1 of the joined fields)', () {
      // Python: hashlib.sha1("T|2026-10-14T09:00|2026-10-14T10:00|False|L|D".encode()).hexdigest()
      final e = Event(
        title: 'T', start: '2026-10-14T09:00', end: '2026-10-14T10:00', location: 'L', description: 'D');
      expect(e.fingerprint(), '72be6a94709d46ce57cd603256a106226d31a6b2');
    });

    test('fingerprint changes when the event changes', () {
      final a = Event(title: 'T', start: 's', end: 'e');
      final b = Event(title: 'T2', start: 's', end: 'e');
      expect(a.fingerprint(), isNot(b.fingerprint()));
    });
  });
}
