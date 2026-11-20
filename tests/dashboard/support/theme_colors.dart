// The colors a theme carries, for tests that check a widget's color comes from the theme (DSH-01.g).
// Depends on the dashboard theme; used by the board, panel and theme tests; reads only the ThemeData it is given.
import 'package:dashboard/theme/app_theme.dart';
import 'package:flutter/material.dart';

/// Every color of [theme] as 0xAARRGGBB: the color scheme, the status colors, and the page, card, divider and text colors.
Set<int> themeColors(ThemeData theme) {
  final s = theme.colorScheme;
  final status = StatusColors.of(theme);
  final text = theme.textTheme;
  final colors = <Color?>[
    s.primary, s.onPrimary, s.primaryContainer, s.onPrimaryContainer, s.secondary, s.onSecondary,
    s.secondaryContainer, s.onSecondaryContainer, s.tertiary, s.onTertiary, s.tertiaryContainer,
    s.onTertiaryContainer, s.error, s.onError, s.errorContainer, s.onErrorContainer, s.surface, s.onSurface,
    s.surfaceContainerHighest, s.surfaceContainerHigh, s.surfaceContainer, s.surfaceContainerLow,
    s.surfaceContainerLowest, s.onSurfaceVariant, s.outline, s.outlineVariant,
    status.ok, status.okBg, status.run, status.runBg, status.warn, status.warnBg, status.bad, status.badBg,
    theme.scaffoldBackgroundColor, theme.cardColor, theme.dividerColor, theme.canvasColor,
    for (final t in [text.bodyLarge, text.bodyMedium, text.bodySmall, text.titleLarge, text.titleMedium, text.titleSmall, text.labelLarge, text.labelMedium, text.labelSmall])
      t?.color,
  ];
  return {for (final c in colors) if (c != null) c.toARGB32()};
}

int rgb(Color c) => c.toARGB32() & 0xFFFFFF;
