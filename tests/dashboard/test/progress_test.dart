// Tests reading one progress file's content: DSH-12.a (name and done/total) and DSH-12.d (content that is not done/total).
// Reading the folder is in local_backend_test.dart. One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/domain/progress_entry.dart';
import 'package:dashboard/features/dashboard/domain/progress_file.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('DSH-12.a: the label is the file name without .progress; done, total and the text done/total are read', () {
    final e = ProgressFile.parse('agent-one.progress', '3/10')!;
    expect([e.label, e.done, e.total, e.text], ['agent-one', 3, 10, '3/10']);
    expect(e.fraction, closeTo(0.3, 1e-9));
  });

  test('DSH-12.a: spaces and a final newline around the fraction are allowed', () {
    final e = ProgressFile.parse('b.progress', ' 4 / 8 \n')!;
    expect([e.done, e.total], [4, 8]);
  });

  test('DSH-12.a: the bar is the fraction, kept between 0 and 1', () {
    expect(const ProgressEntry('a', 5, 10).fraction, 0.5);
    expect(const ProgressEntry('a', 12, 10).fraction, 1);
    expect(const ProgressEntry('a', 0, 0).fraction, 0);
  });

  test('DSH-12.d: content that is not done/total gives no entry', () {
    for (final text in ['', 'three of ten', '3', '3/', '/10', '-1/5', '1.5/3', '3/10 extra', 'x3/10', '3/10/2']) {
      expect(ProgressFile.parse('a.progress', text), isNull, reason: '"$text"');
    }
  });

  test('DSH-12.a: an entry round trips through JSON', () {
    final back = ProgressEntry.fromJson(const ProgressEntry('a', 2, 5).toJson());
    expect([back.label, back.done, back.total], ['a', 2, 5]);
  });
}
