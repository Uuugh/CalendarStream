// Holds: the usage-against-estimate figures (DSH-09.c, DSH-09.d): per story fraction and over-estimate, sprint totals.
// Depends on: Sprint, Story. Used by: UsagePanel. Reads or writes: nothing.

import 'sprint.dart';
import 'story.dart';

/// Pure usage figures; usage points are one percent of the 5-hour allowance (DSH-09.b).
class UsageSummary {
  const UsageSummary(this.sprint);

  final Sprint sprint;

  /// The sum of all estimates (DSH-09.d).
  double get totalEstimate => sprint.stories.fold(0.0, (a, s) => a + s.estimate);

  /// The sum of all usage (DSH-09.d).
  double get totalUsage => sprint.stories.fold(0.0, (a, s) => a + s.usage);

  /// True when the sprint's usage is above its estimate.
  bool get over => totalUsage > totalEstimate;

  /// True when [story]'s usage is above its estimate (DSH-09.c).
  static bool isOver(Story story) => story.usage > story.estimate;

  /// Usage divided by estimate, clamped to 0..1; 1 when there is usage but no estimate, 0 when there is neither.
  static double fraction(double usage, double estimate) {
    if (usage <= 0) return 0;
    if (estimate <= 0) return 1;
    return (usage / estimate).clamp(0.0, 1.0);
  }
}
