// Holds: where the dashboard's files are inside the repository (DSH-01.a), written once.
// Depends on: nothing. Used by: DashboardServer, HttpFileAccess, the platform backends.
// Reads or writes: nothing.

/// Repository-relative locations of the files the dashboard reads and writes.
class DashboardPaths {
  const DashboardPaths._();

  /// The sprint file (DSH-02).
  static const sprint = 'SCRUM.d/sprint.md';

  /// The requirements folder (DSH-03).
  static const requirements = 'requirements';

  /// The usage readings (DSH-14.a).
  static const usage = 'SCRUM.d/usage.md';
}
