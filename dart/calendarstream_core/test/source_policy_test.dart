import 'package:calendarstream_core/calendarstream_core.dart';
import 'package:test/test.dart';

void main() {
  test('calendar URLs require HTTPS and no embedded credentials', () {
    expect(
      CalendarSourcePolicy.validateUrl('https://example.com/calendar.ics').host,
      'example.com',
    );
    for (final url in [
      'http://example.com/calendar.ics',
      'file:///tmp/calendar.ics',
      'https://user:pass@example.com/calendar.ics',
      'https://example.com/calendar.ics#fragment',
      'https:///calendar.ics',
    ]) {
      expect(() => CalendarSourcePolicy.validateUrl(url), throwsFormatException);
    }
  });

  test('credentials never follow a cross-origin redirect', () {
    final source = Uri.parse('https://example.com/calendar.ics');
    expect(
      CalendarSourcePolicy.mayForwardCredentials(
        source,
        Uri.parse('https://example.com/next.ics'),
      ),
      isTrue,
    );
    expect(
      CalendarSourcePolicy.mayForwardCredentials(
        source,
        Uri.parse('https://other.example.com/next.ics'),
      ),
      isFalse,
    );
    expect(
      CalendarSourcePolicy.mayForwardCredentials(
        source,
        Uri.parse('http://example.com/next.ics'),
      ),
      isFalse,
    );
    expect(CalendarSourcePolicy.maxResponseBytes, 5 * 1024 * 1024);
    expect(CalendarSourcePolicy.maxRedirects, 5);
  });
}
