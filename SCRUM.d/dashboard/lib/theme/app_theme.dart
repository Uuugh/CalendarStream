// Holds: the light and dark ThemeData built from the THM-02 color tokens (DSH-01.g) and StatusColors, the theme
// extension with the status colors ok, run, warn, bad and their backgrounds. This is the only file that names a color.
// Depends on: Flutter material. Used by: main.dart and every widget that reads a color. Reads or writes: nothing.

import 'package:flutter/material.dart';

/// The status colors of THM-02.h-k: each with the background it is shown on. Read with [StatusColors.of].
@immutable
class StatusColors extends ThemeExtension<StatusColors> {
  const StatusColors({
    required this.ok,
    required this.okBg,
    required this.run,
    required this.runBg,
    required this.warn,
    required this.warnBg,
    required this.bad,
    required this.badBg,
  });

  final Color ok;
  final Color okBg;
  final Color run;
  final Color runBg;
  final Color warn;
  final Color warnBg;
  final Color bad;
  final Color badBg;

  /// The extension of [theme]; the palette of its brightness when the theme was not built by [AppTheme].
  static StatusColors of(ThemeData theme) =>
      theme.extension<StatusColors>() ?? (theme.brightness == Brightness.dark ? AppTheme.darkStatus : AppTheme.lightStatus);

  @override
  StatusColors copyWith({
    Color? ok,
    Color? okBg,
    Color? run,
    Color? runBg,
    Color? warn,
    Color? warnBg,
    Color? bad,
    Color? badBg,
  }) =>
      StatusColors(
        ok: ok ?? this.ok,
        okBg: okBg ?? this.okBg,
        run: run ?? this.run,
        runBg: runBg ?? this.runBg,
        warn: warn ?? this.warn,
        warnBg: warnBg ?? this.warnBg,
        bad: bad ?? this.bad,
        badBg: badBg ?? this.badBg,
      );

  @override
  StatusColors lerp(ThemeExtension<StatusColors>? other, double t) {
    if (other is! StatusColors) return this;
    return StatusColors(
      ok: Color.lerp(ok, other.ok, t)!,
      okBg: Color.lerp(okBg, other.okBg, t)!,
      run: Color.lerp(run, other.run, t)!,
      runBg: Color.lerp(runBg, other.runBg, t)!,
      warn: Color.lerp(warn, other.warn, t)!,
      warnBg: Color.lerp(warnBg, other.warnBg, t)!,
      bad: Color.lerp(bad, other.bad, t)!,
      badBg: Color.lerp(badBg, other.badBg, t)!,
    );
  }
}

/// The app's themes: [light] and [dark] (THM-02, DSH-01.g).
class AppTheme {
  const AppTheme._();

  static const lightStatus = StatusColors(
    ok: Color(0xFF2F7D62),
    okBg: Color(0xFFEEF5F0),
    run: Color(0xFF40609C),
    runBg: Color(0xFFEEF1F7),
    warn: Color(0xFF946A24),
    warnBg: Color(0xFFFAF3E6),
    bad: Color(0xFFB4483C),
    badBg: Color(0xFFFAEEEB),
  );

  static const darkStatus = StatusColors(
    ok: Color(0xFF4ADE80),
    okBg: Color(0xFF0F2A20),
    run: Color(0xFF93B4FF),
    runBg: Color(0xFF14203D),
    warn: Color(0xFFFBBF24),
    warnBg: Color(0xFF2B2110),
    bad: Color(0xFFF87171),
    badBg: Color(0xFF2D1414),
  );

  static final ThemeData light = _build(
    brightness: Brightness.light,
    bg: const Color(0xFFF7F6F3),
    card: const Color(0xFFFDFCFA),
    soft: const Color(0xFFF1EFEB),
    line: const Color(0xFFE8E4DE),
    text: const Color(0xFF2B2F36),
    muted: const Color(0xFF626C7C),
    accent: const Color(0xFF40609C),
    onAccent: const Color(0xFFFFFFFF),
    status: lightStatus,
  );

  static final ThemeData dark = _build(
    brightness: Brightness.dark,
    bg: const Color(0xFF0F1218),
    card: const Color(0xFF171B23),
    soft: const Color(0xFF1D222C),
    line: const Color(0xFF2A303B),
    text: const Color(0xFFE6E8EC),
    muted: const Color(0xFF98A2B3),
    accent: const Color(0xFF93B4FF),
    onAccent: const Color(0xFF0F1218),
    status: darkStatus,
  );

  static ThemeData _build({
    required Brightness brightness,
    required Color bg,
    required Color card,
    required Color soft,
    required Color line,
    required Color text,
    required Color muted,
    required Color accent,
    required Color onAccent,
    required StatusColors status,
  }) {
    final scheme = ColorScheme(
      brightness: brightness,
      primary: accent,
      onPrimary: onAccent,
      secondary: muted,
      onSecondary: card,
      tertiary: status.warn,
      onTertiary: card,
      error: status.bad,
      onError: card,
      surface: card,
      onSurface: text,
      onSurfaceVariant: muted,
      outline: muted,
      outlineVariant: line,
      surfaceContainerLowest: card,
      surfaceContainerLow: card,
      surfaceContainer: soft,
      surfaceContainerHigh: soft,
      surfaceContainerHighest: soft,
    );
    return ThemeData(
      useMaterial3: true,
      brightness: brightness,
      colorScheme: scheme,
      scaffoldBackgroundColor: bg,
      canvasColor: card,
      cardColor: card,
      dividerColor: line,
      dividerTheme: DividerThemeData(color: line),
      appBarTheme: AppBarTheme(backgroundColor: card, foregroundColor: text, surfaceTintColor: card),
      extensions: [status],
    );
  }
}
