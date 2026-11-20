// Holds: the palette of assignee dot colors (DSH-06.d), derived from the theme's tokens, and the stable pick of one
// per name. Depends on: StatusColors. Used by: AssigneeDot. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../theme/app_theme.dart';

/// One color per assignee name, the same on every card and in every run.
class AssigneeColors {
  const AssigneeColors._();

  /// The ten palette colors of [theme]: its accent, ok, warn and bad colors and the mixes of each pair.
  static List<Color> palette(ThemeData theme) {
    final a = theme.colorScheme.primary;
    final s = StatusColors.of(theme);
    Color mix(Color x, Color y) => Color.lerp(x, y, 0.5)!;
    return [a, s.ok, s.warn, s.bad, mix(a, s.ok), mix(a, s.warn), mix(a, s.bad), mix(s.ok, s.warn), mix(s.ok, s.bad),
      mix(s.warn, s.bad)];
  }

  /// The palette color of [theme] for [name]; the same name always gives the same color.
  static Color of(ThemeData theme, String name) {
    var h = 0;
    for (final unit in name.codeUnits) {
      h = (h * 31 + unit) & 0x7fffffff;
    }
    final colors = palette(theme);
    return colors[h % colors.length];
  }
}
