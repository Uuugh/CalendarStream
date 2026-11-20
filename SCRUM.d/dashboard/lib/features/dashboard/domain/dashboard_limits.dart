// Holds: the numbers of the dashboard that DEF-01 sets, written once (DSH-05.e, DSH-11.a, DSH-15, DSH-12.c, DSH-14.d).
// Depends on: nothing. Used by: IssueService, the page, UsageChart. Reads or writes: nothing.

/// The DEF-01 values of the dashboard. The server's port is in DashboardServerConfig.
class DashboardLimits {
  const DashboardLimits._();

  /// The most issues the issue list holds (DSH-05.e).
  static const int issues = 200;

  /// The board takes [boardShareParts] of [boardShareOf] of the window's height (DSH-15.a).
  static const int boardShareParts = 2;
  static const int boardShareOf = 5;

  /// The number of columns below the board (DSH-15.a).
  static const int columns = 3;

  /// The indent of a sub-requirement under its requirement, in characters of the body text (DSH-11.a).
  static const int subRequirementIndent = 3;

  /// How often the progress bars are read again (DSH-12.c).
  static const Duration progressRefresh = Duration(seconds: 5);

  /// The share an estimate may be off by, plus and minus (DSH-14.d).
  static const double estimateRange = 0.2;

  /// The window sizes nothing may overflow at (DSH-15.c).
  static const int windowLargeWidth = 1920;
  static const int windowLargeHeight = 1080;
  static const int windowSmallWidth = 1280;
  static const int windowSmallHeight = 720;
}
