// Holds: the error raised when a status change breaks StatusRule (DSH-13.c). Depends on: nothing.
// Used by: LocalBackend, HttpBackend, DashboardServer, the page. Reads or writes: nothing.

/// A status change was refused; [reason] is shown as {reason} of msg:dshMoveRefused.
class StatusRefused implements Exception {
  const StatusRefused(this.reason);

  final String reason;

  @override
  String toString() => reason;
}
