// Holds: the color of a usage bar (DSH-09.c), taken from the theme (THM-02) in one function.
// Depends on: StatusColors. Used by: UsagePanel. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../theme/app_theme.dart';

/// Usage bar colors: the warn color (THM-02.j) above the estimate, the accent color otherwise.
class UsageColors {
  const UsageColors._();

  static Color of(ThemeData theme, {required bool over}) =>
      over ? StatusColors.of(theme).warn : theme.colorScheme.primary;
}
