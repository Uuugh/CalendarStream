/// Text patterns and matching.
///
/// Holds: [wildcardToRegex], [patternError], [TextCondition], [textMatcher].
/// Depends on: nothing in the app.
/// Used by: rule matching and validation, the regex test box.
/// Reads/writes: nothing.
/// Ported from: app/rule_engine/text_matching.py. Requirements: RUL-03, RUL-04, RUL-20, RUL-22.
///
/// Known gaps against the Python app (decisions needed, see build_rules/open-questions.md):
/// - Dart's RegExp has no time limit, so RUL-22 (a pathological regex is stopped within a second)
///   is NOT met here; it needs a guard run in an isolate by the server.
/// - Regex error wording comes from Dart's engine, so it differs from Python's.
library;

/// A simple pattern as a regular expression source: `*` any text, `#` a digit, `?` one character,
/// the rest as typed; it must match the whole text (`*E####`: anything ending in E and four digits).
String wildcardToRegex(String value) {
  final out = StringBuffer();
  for (final rune in value.runes) {
    final ch = String.fromCharCode(rune);
    switch (ch) {
      case '*':
        out.write('.*');
      case '#':
        out.write(r'\p{Nd}');
      case '?':
        out.write('.');
      default:
        out.write(RegExp.escape(ch));
    }
  }
  return '^\\s*$out\\s*\$';
}

/// Why a regex cannot be used (empty when it can), for the page. Only the `regex` kind can fail.
String patternError(String value, String op) {
  if (op != 'regex') return '';
  try {
    RegExp(value, unicode: true);
  } on FormatException catch (e) {
    return 'Not a valid regex: ${e.message}.';
  }
  return '';
}

/// One text condition: how to compare (`is`, `contains`, `word`, `begins`, `ends`, `regex`, `pattern`),
/// the value, and whether capitals matter.
class TextCondition {
  const TextCondition(this.op, this.value, {this.caseSensitive = false});

  final String op;
  final String value;
  final bool caseSensitive;
}

const String _wordChar = r'[\p{L}\p{N}_]';

/// The condition as a compiled pattern. Fixed kinds are escaped text.
RegExp compileText(TextCondition c) {
  final v = RegExp.escape(c.value);
  final insensitive = !c.caseSensitive;
  switch (c.op) {
    case 'regex':
      return RegExp(c.value, caseSensitive: !insensitive, unicode: true);
    case 'pattern':
      return RegExp(wildcardToRegex(c.value), caseSensitive: !insensitive, dotAll: true, unicode: true);
    case 'is':
      return RegExp('^\\s*$v\\s*\$', caseSensitive: !insensitive, unicode: true);
    case 'contains':
      return RegExp(v, caseSensitive: !insensitive, unicode: true);
    case 'word':
      return RegExp('(?<!$_wordChar)$v(?!$_wordChar)', caseSensitive: !insensitive, unicode: true);
    case 'begins':
      return RegExp('^\\s*$v', caseSensitive: !insensitive, unicode: true);
    case 'ends':
      return RegExp('$v\\s*\$', caseSensitive: !insensitive, unicode: true);
  }
  throw ArgumentError('unknown text operation: ${c.op}');
}

/// A function that says whether the condition matches a text.
bool Function(String) textMatcher(TextCondition c) {
  final rx = compileText(c);
  return (text) => rx.hasMatch(text);
}

/// The regex test box: for each sample text, whether it matches and the matched span.
class TextTestResult {
  const TextTestResult(this.error, this.results);

  final String error;
  final List<TextTestMatch> results;
}

class TextTestMatch {
  const TextTestMatch(this.text, this.match, this.span);

  final String text;
  final bool match;

  /// `[start, end]`, or empty when there is no match.
  final List<int> span;
}

TextTestResult testText(String value, String op, bool caseSensitive, List<String> samples) {
  final error = patternError(value, op);
  if (error.isNotEmpty || value.isEmpty) return TextTestResult(error, const []);
  final rx = compileText(TextCondition(op, value, caseSensitive: caseSensitive));
  final results = <TextTestMatch>[];
  for (final text in samples.take(30)) {
    final m = rx.firstMatch(text);
    results.add(TextTestMatch(text, m != null, m == null ? const [] : [m.start, m.end]));
  }
  return TextTestResult('', results);
}
