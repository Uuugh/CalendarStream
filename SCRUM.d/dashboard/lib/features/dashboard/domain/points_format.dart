// Holds: the one way usage points are written as text (DSH-09.b, DSH-02.b): whole numbers without decimals.
// Depends on: nothing. Used by: SprintRepository (the file), StoryCard and UsagePanel (the screen). Reads or writes: nothing.

/// Formats and parses usage points.
class PointsFormat {
  const PointsFormat._();

  /// `3` for 3.0, `2.5` for 2.5.
  static String format(double n) => n == n.roundToDouble() ? n.toInt().toString() : n.toString();

  /// The points written in [text] (a comma counts as the decimal point), or null when it is not a number of 0 or more.
  static double? parse(String text) {
    final n = double.tryParse(text.trim().replaceAll(',', '.'));
    return n == null || n.isNaN || n.isInfinite || n < 0 ? null : n;
  }
}
