// Holds: the color of each stage column (DSH-06.c), derived from the theme (THM-02) in one function.
// Depends on: Stage, StatusColors. Used by: SprintBoard. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../theme/app_theme.dart';
import '../domain/stage.dart';

/// Stage colors: every stage gets its own color from the theme's muted, accent and status colors.
class StageColors {
  const StageColors._();

  static Color of(ThemeData theme, Stage stage) {
    final scheme = theme.colorScheme;
    final status = StatusColors.of(theme);
    return switch (stage) {
      Stage.backlog => scheme.outline,
      Stage.ready => scheme.primary,
      Stage.build => status.warn,
      Stage.test => Color.lerp(scheme.primary, status.ok, 0.5)!,
      Stage.review => Color.lerp(scheme.primary, status.bad, 0.5)!,
      Stage.done => status.ok,
    };
  }
}
