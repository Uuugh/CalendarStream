// Holds: the numbers of the dashboard that DEF-01 sets (DSH-05.f). Depends on: nothing.
// Used by: IssueService, the dashboard page. Reads or writes: nothing.

/// The DEF-01 values of the dashboard, written once.
class DashboardLimits {
  const DashboardLimits._();

  /// The most issues the issue list holds (DSH-05.f).
  static const int issues = 200;
}
