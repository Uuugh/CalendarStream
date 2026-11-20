// Static checks on the dashboard's files: DSH-01.d (no text in code; every dsh message exists in every locale) and
// DSH-01.g (no widget names a color; the theme carries the THM-02 colors in light and dark).
// Run from tests/dashboard. One run covers each ID named in the test name.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/theme_colors.dart';

final libDir = Directory('../../SCRUM.d/dashboard/lib');
const messagesDir = '../../requirements/messages';
const locales = ['en', 'de', 'es', 'fr', 'nl', 'pt'];

/// The dashboard's own source files (not the generated l10n).
List<File> sources() => libDir
    .listSync(recursive: true)
    .whereType<File>()
    .where((f) => f.path.endsWith('.dart'))
    .where((f) => !f.path.replaceAll('\\', '/').contains('/lib/l10n/'))
    .toList();

String withoutComments(String text) => text.replaceAll(RegExp(r'//.*'), '');

Map<String, dynamic> arb(String locale) => jsonDecode(File('$messagesDir/app_$locale.arb').readAsStringSync()) as Map<String, dynamic>;

/// The text of the string literal that opens at [i], without its $name and ${...} interpolations.
String staticText(String src, int i) {
  final quote = src[i];
  final out = StringBuffer();
  var j = i + 1;
  while (j < src.length && src[j] != quote) {
    if (src[j] == r'\') {
      j += 2;
    } else if (src[j] == r'$' && j + 1 < src.length && src[j + 1] == '{') {
      var depth = 1;
      j += 2;
      while (j < src.length && depth > 0) {
        if (src[j] == '{') depth++;
        if (src[j] == '}') depth--;
        j++;
      }
    } else if (src[j] == r'$') {
      j++;
      while (j < src.length && RegExp(r'\w').hasMatch(src[j])) {
        j++;
      }
    } else {
      out.write(src[j]);
      j++;
    }
  }
  return out.toString();
}

Set<String> placeholders(String message) => RegExp(r'\{(\w+)\}').allMatches(message).map((m) => m.group(1)!).toSet();

void main() {
  test('DSH-01.d and DSH-01.g: the source folders exist (the scans would pass on nothing)', () {
    expect(libDir.existsSync(), isTrue);
    expect(sources().length, greaterThan(10));
  });

  test('DSH-01.d: no string literal given to Text() or to a label, hint, tooltip or title holds a letter', () {
    final start = RegExp(r'''(?:\bText\(|\b(?:labelText|hintText|helperText|errorText|tooltip|semanticLabel|semanticsLabel|label|title)\s*:)\s*(?=['"])''');
    final found = <String>[];
    for (final f in sources()) {
      final src = withoutComments(f.readAsStringSync());
      for (final m in start.allMatches(src)) {
        final literal = staticText(src, m.end);
        if (RegExp(r'\p{L}', unicode: true).hasMatch(literal)) found.add('${f.path}: ${src.substring(m.start, (m.end + 40).clamp(0, src.length))}');
      }
    }
    expect(found, isEmpty, reason: 'text shown to the user must be a message (rule 14)');
  });

  test('DSH-01.d: the scan reads a literal, ignores interpolations, and would find text with a letter', () {
    expect(staticText(r"'Hello $name ${a['x']} there'", 0), 'Hello   there');
    expect(staticText("'-'", 0), '-');
    expect(RegExp(r'\p{L}', unicode: true).hasMatch(staticText("'Save'", 0)), isTrue);
  });

  test('DSH-01.d: every dsh key of app_en.arb exists in the other five locale files, with the same placeholders', () {
    final en = arb('en');
    final keys = en.keys.where((k) => k.startsWith('dsh')).toList();
    expect(keys, isNotEmpty);
    for (final l in locales.skip(1)) {
      final other = arb(l);
      for (final k in keys) {
        expect(other[k], isA<String>(), reason: '$l lacks $k');
        expect((other[k] as String).trim(), isNotEmpty, reason: '$l has an empty $k');
        expect(placeholders(other[k] as String), placeholders(en[k] as String), reason: '$l: placeholders of $k');
      }
    }
  });

  test('DSH-01.d: every message key the new rows cite exists in English', () {
    final en = arb('en');
    for (final k in [
      'dshStatusBacklog', 'dshStatusProposed', 'dshLoadFailed', 'dshIssuesTruncated', 'dshIssuePartial',
      'dshServerUnreachable', 'dshTrackerUnreachable', 'dshReload', 'dshShownOf', 'dshColumnCount', 'dshIssueFailed', 'cancel',
    ]) {
      expect(en[k], isA<String>(), reason: k);
    }
  });

  test('DSH-01.g: no source file outside lib/theme/app_theme.dart names a color', () {
    final named = RegExp(r'\bColors\.|\bColor\(\s*0x|\bColor\.from|\bCupertinoColors\.');
    final found = <String>[];
    for (final f in sources()) {
      if (f.path.replaceAll('\\', '/').endsWith('lib/theme/app_theme.dart')) continue;
      final src = withoutComments(f.readAsStringSync());
      for (final m in named.allMatches(src)) {
        final line = src.substring(0, m.start).split('\n').length;
        found.add('${f.path}:$line ${m.group(0)}');
      }
    }
    expect(found, isEmpty, reason: 'colors come from the theme (THM-02)');
  });

  test('DSH-01.g: the theme (light and dark) carries the THM-02.a-k colors', () {
    const light = {
      'bg': 0xFFF7F6F3, 'card': 0xFFFDFCFA, 'soft': 0xFFF1EFEB, 'line': 0xFFE8E4DE, 'text': 0xFF2B2F36,
      'muted': 0xFF626C7C, 'accent': 0xFF40609C, 'onaccent': 0xFFFFFFFF,
    };
    const dark = {
      'bg': 0xFF0F1218, 'card': 0xFF171B23, 'soft': 0xFF1D222C, 'line': 0xFF2A303B, 'text': 0xFFE6E8EC,
      'muted': 0xFF98A2B3, 'accent': 0xFF93B4FF, 'onaccent': 0xFF0F1218,
    };
    for (final e in {AppTheme.light: light, AppTheme.dark: dark}.entries) {
      final have = themeColors(e.key);
      for (final t in e.value.entries) {
        expect(have, contains(t.value), reason: '${e.key.brightness.name} ${t.key}');
      }
    }
    expect(AppTheme.light.brightness, Brightness.light);
    expect(AppTheme.dark.brightness, Brightness.dark);
    expect(AppTheme.light.scaffoldBackgroundColor, const Color(0xFFF7F6F3));
    expect(AppTheme.dark.scaffoldBackgroundColor, const Color(0xFF0F1218));
    expect(AppTheme.light.colorScheme.primary, const Color(0xFF40609C));
    expect(AppTheme.dark.colorScheme.primary, const Color(0xFF93B4FF));
    expect(AppTheme.light.colorScheme.onPrimary, const Color(0xFFFFFFFF));
    expect(AppTheme.dark.colorScheme.onPrimary, const Color(0xFF0F1218));
  });

  test('DSH-01.g: the status colors ok, run, warn and bad with their backgrounds are the THM-02.h-k values, in both themes', () {
    void check(StatusColors s, List<int> v) {
      expect([s.ok, s.okBg, s.run, s.runBg, s.warn, s.warnBg, s.bad, s.badBg].map((c) => c.toARGB32()), v);
    }
    check(AppTheme.lightStatus, [
      0xFF2F7D62, 0xFFEEF5F0, 0xFF40609C, 0xFFEEF1F7, 0xFF946A24, 0xFFFAF3E6, 0xFFB4483C, 0xFFFAEEEB,
    ]);
    check(AppTheme.darkStatus, [
      0xFF4ADE80, 0xFF0F2A20, 0xFF93B4FF, 0xFF14203D, 0xFFFBBF24, 0xFF2B2110, 0xFFF87171, 0xFF2D1414,
    ]);
    expect(StatusColors.of(AppTheme.light).warn, AppTheme.lightStatus.warn);
    expect(StatusColors.of(AppTheme.dark).warn, AppTheme.darkStatus.warn);
  });
}
