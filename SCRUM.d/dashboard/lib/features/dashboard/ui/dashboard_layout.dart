// Holds: the sizes and the dash of the dashboard's layout, written once (DSH-15, DSH-05.d). Depends on: nothing.
// Used by: every widget of the dashboard page. Reads or writes: nothing.

/// Layout constants. The window shares (board and columns) are in DashboardLimits; these are paddings and widths.
class DashboardLayout {
  const DashboardLayout._();

  /// Shown where an issue has no feature, requirement or assignee (DSH-05.d).
  static const String dash = '—';

  static const double gap = 8;
  static const double pad = 8;

  /// The width of a block at the top of the board.
  static const double blockWidth = 320;

  /// The height of a usage bar and of a usage meter's track.
  static const double barHeight = 6;
  static const double meterHeight = 22;
}
