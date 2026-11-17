/// Text patterns and matching.
///
/// Holds: [wildcardToRegex], [patternError], [TextCondition], [textMatcher].
/// Depends on: nothing in the app.
/// Used by: rule matching and validation, the regex test box.
/// Reads/writes: nothing.
/// Ported from: app/rule_engine/text_matching.py. Requirements: RUL-03, RUL-04, RUL-20, RUL-22.
///
/// Known gaps against the Python app (decisions needed, see build_rules/open-questions.md):
/// - Dart's RegExp (ECMAScript, backtracking, per the Dart docs) has no time limit, so RUL-22 is NOT met here;
///   the server runs user regexes in an isolate with a timeout (decision in layer-map.md).
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
String patternError(String value, String op) {  if (op != 'regex') return '';  final problem = regexProblem(value);  if (problem == null) return '';  return 'Not a valid regex: ${problem.message} (at character ${problem.start + 1}).';}

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

/// What is wrong with a typed regex and where: the message and the character range `[start, end)` to
/// highlight. Dart reports the message but not the position, so the position is found here.
class RegexProblem {
  const RegexProblem(this.message, this.start, this.end);

  final String message;
  final int start;
  final int end;
}

/// Null when [pattern] is a legal regex; otherwise the problem and the broken part of the pattern.
RegexProblem? regexProblem(String pattern) {
  late final String message;
  try {
    RegExp(pattern, unicode: true);
    return null;
  } on FormatException catch (e) {
    message = e.message;
  }
  if (message.startsWith('Unterminated')) {
    final opener = _unmatchedOpener(pattern);
    if (opener >= 0) return RegexProblem(message, opener, opener + 1);
  }
  // The first prefix that fails with the same message ends at the broken character.
  for (var k = 1; k <= pattern.length; k++) {
    try {
      RegExp(pattern.substring(0, k), unicode: true);
    } on FormatException catch (e) {
      if (e.message != message) continue;
      var start = k - 1;
      if (message == 'Invalid group') start = pattern.lastIndexOf('(', k - 1).clamp(0, k - 1);
      if (message.contains('quantifier')) start = pattern.lastIndexOf('{', k - 1).clamp(0, k - 1);
      return RegexProblem(message, start, k);
    }
  }
  return RegexProblem(message, 0, pattern.length);
}

/// The index of the group or character class that is never closed, or -1.
int _unmatchedOpener(String pattern) {
  final open = <int>[];
  var classStart = -1;
  for (var i = 0; i < pattern.length; i++) {
    final ch = pattern[i];
    if (ch == r'\') {
      i++;
    } else if (classStart >= 0) {
      if (ch == ']') classStart = -1;
    } else if (ch == '[') {
      classStart = i;
    } else if (ch == '(') {
      open.add(i);
    } else if (ch == ')' && open.isNotEmpty) {
      open.removeLast();
    }
  }
  if (classStart >= 0) return classStart;
  return open.isEmpty ? -1 : open.last;
}
