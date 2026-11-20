// Holds: the fixed palette of assignee dot colors (DSH-06.d) and the stable pick of one per name.
// Depends on: nothing. Used by: AssigneeDot. Reads or writes: nothing.

import 'package:flutter/material.dart';

/// One color per assignee name, the same on every card and in every run.
class AssigneeColors {
  const AssigneeColors._();

  static const List<Color> palette = [
    Colors.red,
    Colors.pink,
    Colors.purple,
    Colors.indigo,
    Colors.blue,
    Colors.teal,
    Colors.green,
    Colors.orange,
    Colors.brown,
    Colors.blueGrey,
  ];

  /// The palette color for [name]; the same name always gives the same color.
  static Color of(String name) {
    var h = 0;
    for (final unit in name.codeUnits) {
      h = (h * 31 + unit) & 0x7fffffff;
    }
    return palette[h % palette.length];
  }
}
