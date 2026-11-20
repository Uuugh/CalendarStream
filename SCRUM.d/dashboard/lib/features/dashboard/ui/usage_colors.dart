// Holds: the color of a usage bar (DSH-09.c), derived from the ColorScheme (THM-02) in one function.
// Depends on: nothing. Used by: UsagePanel. Reads or writes: nothing.

import 'package:flutter/material.dart';

/// Usage bar colors: the warning color (the scheme's error color) above the estimate, the primary color otherwise.
class UsageColors {
  const UsageColors._();

  static Color of(ColorScheme scheme, {required bool over}) => over ? scheme.error : scheme.primary;
}
