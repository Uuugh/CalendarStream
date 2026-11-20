// Holds: the color of each stage column (DSH-06.c), derived from the ColorScheme (THM-02) in one function.
// Depends on: Stage. Used by: SprintBoard, StoryCard. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../domain/stage.dart';

/// Stage colors: every stage gets its own color from the scheme.
class StageColors {
  const StageColors._();

  static Color of(ColorScheme scheme, Stage stage) => switch (stage) {
        Stage.backlog => scheme.outline,
        Stage.ready => scheme.secondary,
        Stage.build => scheme.primary,
        Stage.test => scheme.tertiary,
        Stage.review => Color.lerp(scheme.primary, scheme.tertiary, 0.5)!,
        Stage.done => Color.lerp(scheme.secondary, scheme.error, 0.5)!,
      };
}
