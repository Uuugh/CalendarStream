import 'package:domain/domain.dart';
import 'package:test/test.dart';

bool m(String op, String value, String text, {bool cs = false}) =>
    textMatcher(TextCondition(op, value, caseSensitive: cs))(text);

void main() {
  regexProblemTests();
  // RUL-03 (S36-01)
  group('RUL-03 text conditions', () {
    test('is, contains, whole word, begins, ends match', () {
      expect(m('is', 'RDO', ' RDO '), isTrue);
      expect(m('contains', 'RDO', 'xRDOx'), isTrue);
      expect(m('word', 'RDO', 'RDO-1'), isTrue);
      expect(m('begins', 'RDO', 'RDO x'), isTrue);
      expect(m('ends', 'RDO', 'x RDO'), isTrue);
    });
    test('whole word RDO does not match RDOS', () => expect(m('word', 'RDO', 'RDOS'), isFalse));
    test('capitals ignored unless asked', () {
      expect(m('contains', 'rdo', 'RDO'), isTrue);
      expect(m('contains', 'rdo', 'RDO', cs: true), isFalse);
    });
    test('regex', () => expect(m('regex', r'^R\wO$', 'RDO'), isTrue));
    test('regex ignores capitals by default (S52-04)', () => expect(m('regex', 'rdo', 'RDO'), isTrue));
    test('whole word works with non-ASCII letters', () {
      expect(m('word', 'café', 'un café noir'), isTrue);
      expect(m('word', 'caf', 'un café noir'), isFalse);
    });
  });

  // RUL-04 (S49-04, S52-03)
  group('RUL-04 wildcard', () {
    test('*E#### matches Trip E1234 and e9999, not E12345', () {
      expect(m('pattern', '*E####', 'Trip E1234'), isTrue);
      expect(m('pattern', '*E####', 'e9999'), isTrue);
      expect(m('pattern', '*E####', 'E12345'), isFalse);
    });
    test('? is one character, other characters as typed', () {
      expect(m('pattern', 'R?O', 'RDO'), isTrue);
      expect(m('pattern', 'a.b', 'axb'), isFalse);
    });
  });

  // RUL-20 / RUL-22 test box (S49-05, S49-06, S49-07)
  group('regex test box', () {
    test('valid regex reports match and span (S49-06)', () {
      final r = testText(r'E\d{4}', 'regex', false, ['Trip E1234', 'RDO']);
      expect(r.error, '');
      expect(r.results.map((x) => x.match), [true, false]);
      expect(r.results[0].span, [5, 10]);
    });
    test('a broken regex is reported (S49-05)', () {
      expect(patternError('(', 'regex'), startsWith('Not a valid regex'));
      expect(patternError('*', 'regex'), startsWith('Not a valid regex'));
    });
    test('only the regex kind can fail', () => expect(patternError('(', 'contains'), ''));
    test('empty value gives no results', () => expect(testText('', 'regex', false, ['a']).results, isEmpty));
  });
}

// RUL-44: the site checks a typed regex and shows which part is broken.
void regexProblemTests() {
  group('RUL-44 regex problem and position', () {
    RegexProblem? p(String s) => regexProblem(s);
    test('a legal regex has no problem', () {
      expect(p(r'E\d{4}'), isNull);
      expect(p('(a|aa)+\$'), isNull);
    });
    test('unterminated group points at its opening bracket', () {
      final r = p('ab(cd')!;
      expect([r.start, r.end], [2, 3]);
    });
    test('unterminated class points at its [', () {
      final r = p('x[abc')!;
      expect([r.start, r.end], [1, 2]);
    });
    test('nothing to repeat points at the quantifier', () {
      final r = p('a**')!;
      expect(r.message, 'Nothing to repeat');
      expect([r.start, r.end], [2, 3]);
    });
    test('unmatched closing bracket', () {
      final r = p('ab)')!;
      expect([r.start, r.end], [2, 3]);
    });
    test('Python-only syntax is refused (inline flag, named group)', () {
      expect(p('(?i)x'), isNotNull);
      expect(p('(?P<n>x)'), isNotNull);
    });
    test('patternError says where (1-based)', () {
      expect(patternError('ab(cd', 'regex'), 'Not a valid regex: Unterminated group (at character 3).');
    });
    test('escaped brackets are not openers', () => expect(p(r'a\(b'), isNull));
  });
}
